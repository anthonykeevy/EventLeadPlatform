"""
Service for managing company access requests.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from datetime import datetime

from models.company_switch_request import CompanySwitchRequest
from models.user_company import UserCompany
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_company_status import UserCompanyStatus
from models.ref.joined_via import JoinedVia
from models.ref.company_switch_request_status import CompanySwitchRequestStatus
from models.ref.company_switch_request_type import CompanySwitchRequestType
from common.logger import get_logger

logger = get_logger(__name__)


class AccessRequestService:
    def __init__(self, db: Session):
        self.db = db

    def create_access_request(self, user_id: int, target_company_id: int, reason: Optional[str]) -> CompanySwitchRequest:
        """
        Creates a new request for a user to access a company.
        """
        # Get IDs for reference types
        req_type = self.db.execute(select(CompanySwitchRequestType).where(CompanySwitchRequestType.TypeName == 'access_request')).scalar_one()
        pending_status = self.db.execute(select(CompanySwitchRequestStatus).where(CompanySwitchRequestStatus.StatusName == 'pending')).scalar_one()

        # Check for existing pending request
        existing_request = self.db.execute(select(CompanySwitchRequest).where(
            CompanySwitchRequest.UserID == user_id,
            CompanySwitchRequest.ToCompanyID == target_company_id,
            CompanySwitchRequest.StatusID == pending_status.CompanySwitchRequestStatusID
        )).scalars().first()
        
        if existing_request:
            raise ValueError("A pending access request for this company already exists.")

        new_request = CompanySwitchRequest(
            UserID=user_id,
            ToCompanyID=target_company_id,
            RequestTypeID=req_type.CompanySwitchRequestTypeID,
            StatusID=pending_status.CompanySwitchRequestStatusID,
            RequestedBy=user_id,
            Reason=reason,
            CreatedBy=user_id,
            UpdatedBy=user_id
        )
        
        self.db.add(new_request)
        self.db.commit()
        self.db.refresh(new_request)

        logger.info(f"Access request created: RequestID={new_request.CompanySwitchRequestID}, UserID={user_id}, ToCompanyID={target_company_id}")
        return new_request

    def get_pending_access_requests(self, company_id: int) -> List[CompanySwitchRequest]:
        """
        Gets all pending access requests for a company. (For admins)
        """
        pending_status = self.db.execute(select(CompanySwitchRequestStatus).where(CompanySwitchRequestStatus.StatusName == 'pending')).scalar_one()
        stmt = select(CompanySwitchRequest).where(
            CompanySwitchRequest.ToCompanyID == company_id,
            CompanySwitchRequest.StatusID == pending_status.CompanySwitchRequestStatusID
        ).order_by(CompanySwitchRequest.RequestedAt.asc())
        
        return self.db.execute(stmt).scalars().all()

    def approve_access_request(self, request_id: int, approved_by_user_id: int) -> CompanySwitchRequest:
        """
        Approves an access request, creating a UserCompany record.
        """
        pending_status = self.db.execute(select(CompanySwitchRequestStatus).where(CompanySwitchRequestStatus.StatusName == 'pending')).scalar_one()
        
        request = self.db.get(CompanySwitchRequest, request_id)
        if not request or request.StatusID != pending_status.CompanySwitchRequestStatusID:
            raise ValueError("Access request not found or is not in a pending state.")

        # Create UserCompany record
        company_user_role = self.db.execute(select(UserCompanyRole).where(UserCompanyRole.RoleCode == 'company_user')).scalar_one()
        active_status = self.db.execute(select(UserCompanyStatus).where(UserCompanyStatus.StatusCode == 'active')).scalar_one()
        joined_via_request = self.db.execute(select(JoinedVia).where(JoinedVia.MethodCode == 'access_request')).scalar_one()

        new_user_company = UserCompany(
            UserID=request.UserID,
            CompanyID=request.ToCompanyID,
            UserCompanyRoleID=company_user_role.UserCompanyRoleID,
            StatusID=active_status.UserCompanyStatusID,
            IsPrimaryCompany=False,
            JoinedViaID=joined_via_request.JoinedViaID,
            CreatedBy=approved_by_user_id,
            UpdatedBy=approved_by_user_id
        )
        self.db.add(new_user_company)

        # Update request status
        approved_status = self.db.execute(select(CompanySwitchRequestStatus).where(CompanySwitchRequestStatus.StatusName == 'approved')).scalar_one()
        request.StatusID = approved_status.CompanySwitchRequestStatusID
        request.ApprovedBy = approved_by_user_id
        request.ApprovedAt = datetime.utcnow()
        request.UpdatedBy = approved_by_user_id
        self.db.add(request)

        self.db.commit()
        self.db.refresh(request)
        
        logger.info(f"Access request approved: RequestID={request_id} by UserID={approved_by_user_id}")
        # TODO: Send notification email to requester
        
        return request

    def reject_access_request(self, request_id: int, rejected_by_user_id: int, reason: Optional[str]) -> CompanySwitchRequest:
        """
        Rejects an access request.
        """
        pending_status = self.db.execute(select(CompanySwitchRequestStatus).where(CompanySwitchRequestStatus.StatusName == 'pending')).scalar_one()
        
        request = self.db.get(CompanySwitchRequest, request_id)
        if not request or request.StatusID != pending_status.CompanySwitchRequestStatusID:
            raise ValueError("Access request not found or is not in a pending state.")

        rejected_status = self.db.execute(select(CompanySwitchRequestStatus).where(CompanySwitchRequestStatus.StatusName == 'rejected')).scalar_one()
        request.StatusID = rejected_status.CompanySwitchRequestStatusID
        request.RejectedBy = rejected_by_user_id
        request.RejectedAt = datetime.utcnow()
        request.RejectionReason = reason
        request.UpdatedBy = rejected_by_user_id
        self.db.add(request)

        self.db.commit()
        self.db.refresh(request)

        logger.info(f"Access request rejected: RequestID={request_id} by UserID={rejected_by_user_id}")
        # TODO: Send notification email to requester

        return request
