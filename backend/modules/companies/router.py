"""
Company Management Router
Endpoints for company creation and management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
import os

from backend.common.database import get_db
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.models import CurrentUser
from backend.modules.auth.jwt_service import create_access_token, create_refresh_token
from backend.common.rbac import require_company_admin_for_company
from backend.models.user import User
from backend.models.company import Company
from backend.models.ref.user_company_role import UserCompanyRole
from backend.models.ref.user_invitation_status import UserInvitationStatus
from backend.services.email_service import get_email_service
from .schemas import (
    CreateCompanySchema, CreateCompanyResponse,
    SendInvitationSchema, SendInvitationResponse,
    ListInvitationsResponse, InvitationDetails,
    ResendInvitationResponse, CancelInvitationResponse
)
from .service import create_company
from .invitation_service import (
    send_invitation, resend_invitation, cancel_invitation,
    list_company_invitations, get_invitation_details,
    INVITATION_EXPIRY_DAYS
)
from backend.common.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/companies", tags=["companies"])


# Frontend URL for invitation acceptance (from environment)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


@router.post(
    "",
    response_model=CreateCompanyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create first company",
    description="Create company during onboarding and assign user as company_admin"
)
async def create_first_company(
    request: CreateCompanySchema,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> CreateCompanyResponse:
    """
    Create user's first company (AC-1.5.3, AC-1.5.4, AC-1.5.5, AC-1.5.6, AC-1.5.8, AC-1.5.9).
    
    Requires authentication.
    
    Process:
    1. Validate ABN/ACN if provided
    2. Check user doesn't already have company
    3. Create Company record
    4. Create UserCompany with role='company_admin'
    5. Issue new JWT with role and company_id
    6. Log to audit tables
    
    Returns new access token and refresh token with updated claims.
    """
    try:
        # Create company and user-company relationship
        company, user_company = await create_company(
            db=db,
            user_id=current_user.user_id,
            company_name=request.company_name,
            abn=request.abn,
            acn=request.acn,
            phone=request.phone,
            email=request.email,
            website=request.website,
            country_id=request.country_id,
            industry_id=request.industry_id
        )
        
        # Issue new JWT with role and company_id (AC-1.5.6)
        access_token = create_access_token(
            user_id=current_user.user_id,
            email=current_user.email,
            role="company_admin",
            company_id=int(company.CompanyID)  # type: ignore
        )
        
        refresh_token = create_refresh_token(
            user_id=current_user.user_id
        )
        
        logger.info(
            f"Company created and JWT issued: UserID={current_user.user_id}, "
            f"CompanyID={company.CompanyID}, Role=company_admin"
        )
        
        return CreateCompanyResponse(
            success=True,
            message="Company created successfully",
            company_id=int(company.CompanyID),  # type: ignore
            user_company_id=int(user_company.UserCompanyID),  # type: ignore
            access_token=access_token,
            refresh_token=refresh_token,
            role="company_admin"
        )
        
    except ValueError as e:
        logger.warning(f"Invalid company creation request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating company: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create company"
        )


# ============================================================================
# Team Invitation Endpoints (Story 1.6)
# ============================================================================

@router.post(
    "/{company_id}/invite",
    response_model=SendInvitationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send team invitation",
    description="Invite team member to company (requires company_admin role)"
)
async def send_team_invitation(
    company_id: int,
    request: SendInvitationSchema,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> SendInvitationResponse:
    """
    Send team invitation (AC-1.6.1, AC-1.6.2, AC-1.6.3, AC-1.6.4, AC-1.6.5, AC-1.6.6).
    
    Requires company_admin role and membership in the company.
    
    Process:
    1. Verify admin belongs to company
    2. Validate role is allowed
    3. Check email not already in company
    4. Create invitation with 7-day expiry token
    5. Send invitation email
    6. Log to audit
    """
    try:
        # Verify user is company admin for this company (AC-1.6.1)
        require_company_admin_for_company(current_user, company_id)
        
        # Send invitation
        invitation = await send_invitation(
            db=db,
            company_id=company_id,
            invited_by_user_id=current_user.user_id,
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            role_code=request.role
        )
        
        # Get company and inviter details for email
        company = db.execute(
            select(Company).where(Company.CompanyID == company_id)
        ).scalar_one()
        
        inviter = db.execute(
            select(User).where(User.UserID == current_user.user_id)
        ).scalar_one()
        
        role = db.execute(
            select(UserCompanyRole).where(UserCompanyRole.RoleCode == request.role)
        ).scalar_one()
        
        # Build invitation URL (AC-1.6.4)
        invitation_url = f"{FRONTEND_URL}/invitations/accept?token={invitation.InvitationToken}"
        
        # Send invitation email (AC-1.6.4)
        email_service = get_email_service()
        await email_service.send_team_invitation_email(
            to=request.email,
            invitee_name=f"{request.first_name} {request.last_name}",
            inviter_name=f"{inviter.FirstName} {inviter.LastName}",
            company_name=str(company.CompanyName),
            role_name=str(role.RoleName),  # type: ignore
            invitation_url=invitation_url,
            expiry_days=INVITATION_EXPIRY_DAYS
        )
        
        logger.info(
            f"Team invitation sent: UserInvitationID={invitation.UserInvitationID}, "
            f"Email={request.email}, CompanyID={company_id}, InvitedBy={current_user.user_id}"
        )
        
        return SendInvitationResponse(
            success=True,
            message="Invitation sent successfully",
            invitation_id=int(invitation.UserInvitationID),  # type: ignore
            expires_at=invitation.ExpiresAt  # type: ignore
        )
        
    except ValueError as e:
        logger.warning(f"Invalid invitation request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending invitation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send invitation"
        )


@router.get(
    "/{company_id}/invitations",
    response_model=ListInvitationsResponse,
    summary="List company invitations",
    description="List all invitations for company (requires company_admin role)"
)
async def list_invitations(
    company_id: int,
    status_filter: Optional[str] = Query(None, description="Filter by status (pending, accepted, expired, cancelled)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ListInvitationsResponse:
    """
    List company invitations (AC-1.6.9).
    
    Requires company_admin role.
    Supports filtering by status and pagination.
    """
    try:
        # Verify user is company admin for this company
        require_company_admin_for_company(current_user, company_id)
        
        # Get invitations
        invitations, total = await list_company_invitations(
            db=db,
            company_id=company_id,
            status_filter=status_filter,
            page=page,
            page_size=page_size
        )
        
        # Build response
        invitation_details = []
        for inv in invitations:
            # Get inviter details
            inviter = db.execute(
                select(User).where(User.UserID == inv.InvitedBy)
            ).scalar_one()
            
            # Get role
            role = db.execute(
                select(UserCompanyRole).where(
                    UserCompanyRole.UserCompanyRoleID == inv.UserCompanyRoleID
                )
            ).scalar_one()
            
            # Get status
            status_obj = db.execute(
                select(UserInvitationStatus).where(
                    UserInvitationStatus.UserInvitationStatusID == inv.StatusID
                )
            ).scalar_one()
            
            invitation_details.append(InvitationDetails(
                invitation_id=int(inv.UserInvitationID),  # type: ignore
                company_id=int(inv.CompanyID),  # type: ignore
                email=str(inv.Email),  # type: ignore
                first_name=str(inv.FirstName),  # type: ignore
                last_name=str(inv.LastName),  # type: ignore
                role=str(role.RoleCode),  # type: ignore
                status=str(status_obj.StatusCode),  # type: ignore
                invited_by=f"{inviter.FirstName} {inviter.LastName}",
                invited_at=inv.InvitedAt,  # type: ignore
                expires_at=inv.ExpiresAt,  # type: ignore
                accepted_at=inv.AcceptedAt,  # type: ignore
                cancelled_at=inv.CancelledAt,  # type: ignore
                declined_at=inv.DeclinedAt,  # type: ignore
                resend_count=int(inv.ResendCount or 0),  # type: ignore
                last_resent_at=inv.LastResentAt  # type: ignore
            ))
        
        return ListInvitationsResponse(
            invitations=invitation_details,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing invitations: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list invitations"
        )


@router.post(
    "/{company_id}/invitations/{invitation_id}/resend",
    response_model=ResendInvitationResponse,
    summary="Resend invitation",
    description="Resend pending invitation (requires company_admin role)"
)
async def resend_team_invitation(
    company_id: int,
    invitation_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ResendInvitationResponse:
    """
    Resend invitation (AC-1.6.7).
    
    Extends expiry date and resends email.
    Only works for pending invitations.
    """
    try:
        # Verify user is company admin for this company
        require_company_admin_for_company(current_user, company_id)
        
        # Resend invitation
        invitation = await resend_invitation(
            db=db,
            invitation_id=invitation_id,
            company_id=company_id,
            resent_by_user_id=current_user.user_id
        )
        
        # Get details for email
        company = db.execute(
            select(Company).where(Company.CompanyID == company_id)
        ).scalar_one()
        
        inviter = db.execute(
            select(User).where(User.UserID == current_user.user_id)
        ).scalar_one()
        
        role = db.execute(
            select(UserCompanyRole).where(
                UserCompanyRole.UserCompanyRoleID == invitation.UserCompanyRoleID
            )
        ).scalar_one()
        
        # Build invitation URL
        invitation_url = f"{FRONTEND_URL}/invitations/accept?token={invitation.InvitationToken}"
        
        # Resend email
        email_service = get_email_service()
        await email_service.send_team_invitation_email(
            to=str(invitation.Email),
            invitee_name=f"{invitation.FirstName} {invitation.LastName}",
            inviter_name=f"{inviter.FirstName} {inviter.LastName}",
            company_name=str(company.CompanyName),
            role_name=str(role.RoleName),  # type: ignore
            invitation_url=invitation_url,
            expiry_days=INVITATION_EXPIRY_DAYS
        )
        
        logger.info(
            f"Invitation resent: UserInvitationID={invitation_id}, "
            f"ResendCount={invitation.ResendCount}"
        )
        
        return ResendInvitationResponse(
            success=True,
            message="Invitation resent successfully",
            invitation_id=int(invitation.UserInvitationID),  # type: ignore
            new_expires_at=invitation.ExpiresAt,  # type: ignore
            resend_count=int(invitation.ResendCount or 0)  # type: ignore
        )
        
    except ValueError as e:
        logger.warning(f"Invalid resend request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resending invitation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to resend invitation"
        )


@router.delete(
    "/{company_id}/invitations/{invitation_id}",
    response_model=CancelInvitationResponse,
    summary="Cancel invitation",
    description="Cancel pending invitation (requires company_admin role)"
)
async def cancel_team_invitation(
    company_id: int,
    invitation_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> CancelInvitationResponse:
    """
    Cancel invitation (AC-1.6.8).
    
    Marks invitation as cancelled and invalidates token.
    Only works for pending invitations.
    """
    try:
        # Verify user is company admin for this company
        require_company_admin_for_company(current_user, company_id)
        
        # Cancel invitation
        invitation = await cancel_invitation(
            db=db,
            invitation_id=invitation_id,
            company_id=company_id,
            cancelled_by_user_id=current_user.user_id,
            reason="Cancelled by admin"
        )
        
        logger.info(
            f"Invitation cancelled: UserInvitationID={invitation_id}, "
            f"CancelledBy={current_user.user_id}"
        )
        
        return CancelInvitationResponse(
            success=True,
            message="Invitation cancelled successfully",
            invitation_id=int(invitation.UserInvitationID)  # type: ignore
        )
        
    except ValueError as e:
        logger.warning(f"Invalid cancel request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling invitation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel invitation"
        )

