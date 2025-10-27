"""
Invitations Router
Public and protected endpoints for invitation viewing and acceptance
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from modules.auth.jwt_service import create_access_token, create_refresh_token
from models.company import Company
from models.ref.user_company_role import UserCompanyRole
from .schemas import InvitationDetailsResponse, AcceptInvitationResponse
from .service import (
    get_invitation_details,
    accept_invitation,
    get_invitation_by_token
)
from common.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/invitations", tags=["invitations"])


@router.get(
    "/{token}",
    response_model=InvitationDetailsResponse,
    summary="View invitation details",
    description="Public endpoint to view invitation details by token (no authentication required)"
)
async def view_invitation(
    token: str,
    db: Session = Depends(get_db)
) -> InvitationDetailsResponse:
    """
    View invitation details (AC-1.7.1, AC-1.7.2).
    
    Public endpoint - does not require authentication.
    Returns company name, role, inviter name, and expiry information.
    Does not expose sensitive data.
    """
    try:
        details = await get_invitation_details(db, token)
        
        if not details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitation not found"
            )
        
        invitation, company, inviter, role, inv_status = details
        
        # Check if expired
        is_expired = invitation.ExpiresAt < datetime.utcnow()  # type: ignore
        
        return InvitationDetailsResponse(
            invitation_id=int(invitation.UserInvitationID),  # type: ignore
            company_name=str(company.CompanyName),  # type: ignore
            role_name=str(role.RoleName),  # type: ignore
            inviter_name=f"{inviter.FirstName} {inviter.LastName}",
            invited_email=str(invitation.Email),  # type: ignore
            invited_first_name=str(invitation.FirstName),  # type: ignore
            invited_last_name=str(invitation.LastName),  # type: ignore
            expires_at=invitation.ExpiresAt,  # type: ignore
            is_expired=bool(is_expired),  # type: ignore
            status=str(inv_status.StatusCode)  # type: ignore
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error viewing invitation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve invitation details"
        )


@router.post(
    "/{token}/accept",
    response_model=AcceptInvitationResponse,
    status_code=status.HTTP_200_OK,
    summary="Accept team invitation",
    description="Accept invitation and join company (requires authentication)"
)
async def accept_team_invitation(
    token: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AcceptInvitationResponse:
    """
    Accept team invitation (AC-1.7.3, AC-1.7.4, AC-1.7.7, AC-1.7.8).
    
    Requires authentication.
    
    Process:
    1. Validate token and check expiry
    2. Verify invitation email matches authenticated user's email
    3. Create UserCompany relationship with invited role
    4. Mark invitation as accepted
    5. Issue new JWT with updated role and company_id
    6. Log to audit
    """
    try:
        # Accept invitation
        invitation, user_company = await accept_invitation(
            db=db,
            token=token,
            user_id=current_user.user_id,
            user_email=current_user.email
        )
        
        # Get role for response
        role = db.execute(
            select(UserCompanyRole).where(
                UserCompanyRole.UserCompanyRoleID == user_company.UserCompanyRoleID
            )
        ).scalar_one()
        
        # Issue new JWT with role and company_id (AC-1.7.8)
        access_token = create_access_token(
            user_id=current_user.user_id,
            email=current_user.email,
            role=str(role.RoleCode),  # type: ignore
            company_id=int(user_company.CompanyID)  # type: ignore
        )
        
        refresh_token = create_refresh_token(
            user_id=current_user.user_id
        )
        
        logger.info(
            f"Invitation accepted and JWT issued: UserID={current_user.user_id}, "
            f"CompanyID={user_company.CompanyID}, Role={role.RoleCode}"
        )
        
        return AcceptInvitationResponse(
            success=True,
            message="Invitation accepted successfully",
            company_id=int(user_company.CompanyID),  # type: ignore
            role=str(role.RoleCode),  # type: ignore
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    except ValueError as e:
        logger.warning(f"Invalid invitation acceptance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error accepting invitation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to accept invitation"
        )

