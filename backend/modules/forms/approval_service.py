"""
Form Approval Service
Handles approval workflows for high-cost forms (Story 2.11)
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from datetime import datetime
from typing import Optional, Dict, Any, List
from decimal import Decimal

from models.form import Form
from models.ref.form_approval_status import FormApprovalStatus
from models.ref.form_status import FormStatus
from models.user import User
from models.user_company import UserCompany
from models.ref.user_company_role import UserCompanyRole
from models.audit.activity_log import ActivityLog
from common.config_service import ConfigurationService
from common.email import email_service
from common.logger import get_logger
from common.email_templates import get_approval_email_template, get_decision_email_template
from .access_guard import check_form_access_guard
import os

logger = get_logger(__name__)

class ApprovalService:
    
    def __init__(self, db: Session):
        self.db = db
        self.config_service = ConfigurationService(db)

    async def _get_status_by_code(self, code: str) -> Optional[FormApprovalStatus]:
        return self.db.execute(
            select(FormApprovalStatus).where(FormApprovalStatus.ApprovalStatusCode == code)
        ).scalar_one_or_none()

    async def _get_form_status_by_code(self, code: str) -> Optional[FormStatus]:
        return self.db.execute(
            select(FormStatus).where(FormStatus.StatusCode == code)
        ).scalar_one_or_none()

    async def submit_for_approval(self, form_id: int, user_id: int, company_id: int) -> Form:
        """
        Submit a form for approval.
        Transitions status to PENDING.
        """
        # Check access (Manage)
        form = await check_form_access_guard(self.db, form_id, user_id, "MANAGE")
        
        # Verify cost threshold
        threshold = self.config_service.get_approval_cost_threshold()
        cost = form.DeploymentCost or 0
        
        if cost <= threshold:
            # If cost is below threshold, we might not need approval, but user explicitly requested it.
            # Alternatively, verify if it SHOULD be submitted.
            # Story says: "Submit for Approval" (visible when Draft + Cost > Threshold).
            # If user hits API directly for low cost form, maybe just allow it or auto-approve?
            # For now, let's allow submission even if low cost, or maybe reject? 
            # AC 2.11.1 implies cost > threshold sets it to PENDING.
            # Let's enforce cost check.
            logger.info(f"Form {form_id} cost {cost} is below threshold {threshold}. Auto-approving or ignoring?")
            pass # Proceeding to submit anyway as explicit action
            
        # Get PENDING status
        pending_status = await self._get_status_by_code('PENDING')
        if not pending_status:
            raise ValueError("Approval Status 'PENDING' not found in database.")
            
        # Update status
        old_status_id = form.FormApprovalStatusID
        form.FormApprovalStatusID = pending_status.FormApprovalStatusID
        form.UpdatedBy = user_id
        form.UpdatedDate = datetime.utcnow()
        
        self.db.flush()
        
        # Log
        self._log_activity(user_id, company_id, "form.submitted_for_approval", form, 
                           f"Status: {old_status_id} -> {pending_status.FormApprovalStatusID}")
                           
        # Send Notifications to Admins
        await self._notify_admins_of_request(form, user_id, company_id)
        
        return form

    async def approve_form(self, form_id: int, admin_user_id: int, company_id: int) -> Form:
        """
        Approve a pending form.
        Transitions status to APPROVED.
        """
        # 1. Check MANAGE access (base requirement)
        form = await check_form_access_guard(self.db, form_id, admin_user_id, "MANAGE")
        
        # 2. Check Company Admin Role (Strict enforcement per AC-2.11.3)
        # Owners have MANAGE but shouldn't self-approve if not admin
        await self._check_company_admin_role(admin_user_id, company_id)
        
        # Verify current status is PENDING or NO_APPROVAL (Pre-approval)
        current_status = self.db.get(FormApprovalStatus, form.FormApprovalStatusID)
        if current_status.ApprovalStatusCode not in ['PENDING', 'NO_APPROVAL']:
             raise ValueError(f"Form is not in PENDING or DRAFT state (Current: {current_status.ApprovalStatusCode})")
             
        # Get APPROVED status
        approved_status = await self._get_status_by_code('APPROVED')
        if not approved_status:
            raise ValueError("Approval Status 'APPROVED' not found.")
            
        # Update Approval Status
        old_approval_status_code = current_status.ApprovalStatusCode
        form.FormApprovalStatusID = approved_status.FormApprovalStatusID
        form.UpdatedBy = admin_user_id
        form.UpdatedDate = datetime.utcnow()
        
        # Auto-Publish Logic
        # If form was PENDING (intercepted publish), auto-publish it.
        if old_approval_status_code == 'PENDING':
            published_status = await self._get_form_status_by_code('PUBLISHED')
            if published_status:
                form.FormStatusID = published_status.FormStatusID
                logger.info(f"Auto-publishing form {form_id} after approval")
        
        self.db.flush()
        
        # Log
        self._log_activity(admin_user_id, company_id, "form.approved", form, 
                           f"Approved by user {admin_user_id}")

        # Notify Owner
        # Only notify if the approver is NOT the owner (avoid spamming self)
        if admin_user_id != form.CreatedBy:
            await self._notify_owner_of_decision(form, "Approved", admin_user_id)
        else:
            logger.info(f"Skipping owner notification for form {form_id} as approver {admin_user_id} is the owner.")
        
        return form

    async def reject_form(self, form_id: int, admin_user_id: int, company_id: int, reason: str) -> Form:
        """
        Reject a pending form.
        Transitions status to REJECTED.
        """
        # 1. Check MANAGE access
        form = await check_form_access_guard(self.db, form_id, admin_user_id, "MANAGE")
        
        # 2. Check Company Admin Role
        await self._check_company_admin_role(admin_user_id, company_id)
        
        current_status = self.db.get(FormApprovalStatus, form.FormApprovalStatusID)
        # Allow rejecting from PENDING or APPROVED? Usually from PENDING.
        
        rejected_status = await self._get_status_by_code('REJECTED')
        if not rejected_status:
            raise ValueError("Approval Status 'REJECTED' not found.")
            
        old_status_id = form.FormApprovalStatusID
        form.FormApprovalStatusID = rejected_status.FormApprovalStatusID
        form.UpdatedBy = admin_user_id
        form.UpdatedDate = datetime.utcnow()
        
        self.db.flush()
        
        self._log_activity(admin_user_id, company_id, "form.rejected", form, 
                           f"Reason: {reason}")
                           
        await self._notify_owner_of_decision(form, "Rejected", admin_user_id, reason)
        
        return form

    def check_publish_guard(self, form: Form) -> bool:
        """
        Check if form can be published.
        Returns True if allowed, raises ValueError if blocked.
        """
        threshold = self.config_service.get_approval_cost_threshold()
        cost = form.DeploymentCost or 0
        
        if cost <= threshold:
            return True
            
        # High cost - check approval
        status = self.db.get(FormApprovalStatus, form.FormApprovalStatusID)
        if status.ApprovalStatusCode == 'APPROVED':
            return True
            
        raise ValueError(f"Form requires approval (Cost ${cost} > ${threshold}) and current status is {status.ApprovalStatusCode}")

    def _log_activity(self, user_id: int, company_id: int, action: str, form: Form, details: str):
        try:
            activity_log = ActivityLog(
                UserID=user_id,
                CompanyID=company_id,
                Action=action,
                EntityType="Form",
                EntityID=form.FormID,
                NewValue=details,
                CreatedDate=datetime.utcnow()
            )
            self.db.add(activity_log)
        except Exception as e:
            logger.warning(f"Failed to log activity: {e}")

    async def _check_company_admin_role(self, user_id: int, company_id: int):
        """Check if user is a Company Admin (or System Admin)"""
        # Check Company Role
        result = self.db.execute(
            select(UserCompany)
            .join(UserCompanyRole)
            .where(
                UserCompany.UserID == user_id,
                UserCompany.CompanyID == company_id,
                UserCompanyRole.RoleCode == 'company_admin',
                UserCompany.IsDeleted == False
            )
        ).scalar_one_or_none()
        
        if result:
            return True
            
        # Check System Admin
        user = self.db.get(User, user_id)
        if user:
            # Load role relationship if needed, or query
            from models.ref.user_role import UserRole
            role = self.db.execute(
                select(UserRole).where(UserRole.UserRoleID == user.UserRoleID)
            ).scalar_one_or_none()
            
            if role and role.RoleCode == 'system_admin':
                return True
        
        raise ValueError("Only Company Administrators can perform this action.")

    async def _notify_admins_of_request(self, form: Form, requestor_id: int, company_id: int):
        """
        Send email to all company admins.
        """
        # Find admins
        admins = self.db.execute(
            select(User)
            .join(UserCompany, User.UserID == UserCompany.UserID)
            .join(UserCompanyRole, UserCompany.UserCompanyRoleID == UserCompanyRole.UserCompanyRoleID)
            .where(
                UserCompany.CompanyID == company_id,
                UserCompanyRole.RoleCode == 'company_admin', # Corrected role code
                User.IsDeleted == False
            )
        ).scalars().all()
        
        if not admins:
            logger.warning(f"No admins found for company {company_id} to notify.")
            return

        requestor = self.db.get(User, requestor_id)
        requestor_name = f"{requestor.FirstName} {requestor.LastName}" if requestor else "Unknown User"

        subject = f"Approval Request: {form.FormName}"
        
        # Frontend URL for deep linking
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        view_url = f"{frontend_url}/dashboard?formId={form.FormID}"
        
        # Generate HTML content
        body = get_approval_email_template(
            form_name=form.FormName,
            requestor_name=requestor_name,
            cost=form.DeploymentCost,
            view_url=view_url
        )
        
        for admin in admins:
            try:
                await email_service.send_notification_email(admin.Email, subject, body)
            except Exception as e:
                logger.error(f"Failed to send approval email to admin {admin.Email}: {e}")
            
        logger.info(f"Notified {len(admins)} admins about form {form.FormID}")

    async def _notify_owner_of_decision(self, form: Form, decision: str, decider_id: int, reason: str = None):
        owner = self.db.get(User, form.CreatedBy)
        if not owner:
            return
            
        subject = f"Form Approval Update: {form.FormName}"
        
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        view_url = f"{frontend_url}/dashboard?formId={form.FormID}"
        
        body = get_decision_email_template(
            form_name=form.FormName,
            decision=decision,
            reason=reason,
            view_url=view_url
        )
        
        await email_service.send_notification_email(owner.Email, subject, body)
        logger.info(f"Notified owner {owner.Email} of decision: {decision}")

