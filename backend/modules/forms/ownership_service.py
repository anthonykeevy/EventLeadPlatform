"""
Form Ownership Transfer Service
Business logic for bulk form ownership transfer operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any, Optional
from fastapi import HTTPException, status

from models.user import User
from models.ref.user_role import UserRole
from models.user_company import UserCompany
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_company_status import UserCompanyStatus
from common.logger import get_logger

logger = get_logger(__name__)


async def transfer_form_ownership(
    db: Session,
    from_user_id: int,
    to_user_id: int,
    company_id: int,
    performed_by: int,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """
    Transfer form ownership from one user to another within a company.
    
    Uses stored procedure sp_TransferFormOwnership which:
    - Validates permissions (Company Admin or System Admin)
    - Updates Form.CreatedBy for all forms owned by from_user_id
    - Updates FormAccessControl.UserID entries
    - Creates audit trail records
    
    Args:
        db: Database session
        from_user_id: User ID to transfer ownership FROM
        to_user_id: User ID to transfer ownership TO
        company_id: Company ID (must match company of both users)
        performed_by: User ID performing the transfer (must be Company Admin or System Admin)
        reason: Optional reason for transfer
        
    Returns:
        Dictionary with transfer results:
        - FormsTransferred: int (number of forms transferred)
        - AccessControlsTransferred: int (number of access control entries transferred)
        - Success: bool
        
    Raises:
        HTTPException: 403 if unauthorized, 400 if validation fails
    """
    # Validate performed_by has permissions
    has_permission = await _validate_transfer_permissions(
        db, performed_by, company_id
    )
    
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Company Admin or System Admin can transfer form ownership"
        )
    
    # Validate users are in company
    if not await _validate_user_in_company(db, from_user_id, company_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"FromUserID {from_user_id} is not an active member of company {company_id}"
        )
    
    if not await _validate_user_in_company(db, to_user_id, company_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ToUserID {to_user_id} is not an active member of company {company_id}"
        )
    
    # Validate from_user_id != to_user_id
    if from_user_id == to_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="FromUserID and ToUserID must be different"
        )
    
    try:
        # Call stored procedure
        # The stored procedure returns a result set with FormsTransferred, AccessControlsTransferred, Status, Message
        result = db.execute(
            text("""
                EXEC [dbo].[sp_TransferFormOwnership]
                    @FromUserID = :from_user_id,
                    @ToUserID = :to_user_id,
                    @CompanyID = :company_id,
                    @PerformedBy = :performed_by,
                    @Reason = :reason
            """),
            {
                "from_user_id": from_user_id,
                "to_user_id": to_user_id,
                "company_id": company_id,
                "performed_by": performed_by,
                "reason": reason or "Bulk ownership transfer"
            }
        )
        
        # Fetch the result set returned by the stored procedure
        row = result.fetchone()
        
        if row is None:
            raise Exception("Stored procedure did not return expected result set")
        
        # The stored procedure returns: FormsTransferred, AccessControlsTransferred, Status, Message
        forms_transferred = int(row[0]) if row[0] is not None else 0
        access_controls_transferred = int(row[1]) if row[1] is not None else 0
        status = row[2] if len(row) > 2 else "SUCCESS"
        message = row[3] if len(row) > 3 else "Ownership transfer completed successfully"
        
        # Commit the transaction (stored procedure handles its own transaction, but we commit here for safety)
        db.commit()
        
        logger.info(
            f"Form ownership transferred: FromUserID={from_user_id}, "
            f"ToUserID={to_user_id}, CompanyID={company_id}, "
            f"FormsTransferred={forms_transferred}, "
            f"AccessControlsTransferred={access_controls_transferred}, "
            f"Status={status}"
        )
        
        return {
            "FormsTransferred": forms_transferred,
            "AccessControlsTransferred": access_controls_transferred,
            "Status": status,
            "Message": message,
            "Success": True
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error transferring form ownership: {str(e)}")
        
        # Check if it's a SQL Server error (RAISERROR)
        error_message = str(e)
        if "RAISERROR" in error_message or "User performing transfer" in error_message:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User performing transfer must be Company Admin for the company or System Admin"
            )
        elif "FromUserID must be" in error_message or "ToUserID must be" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error transferring form ownership: {str(e)}"
            )


async def _validate_transfer_permissions(
    db: Session,
    user_id: int,
    company_id: int
) -> bool:
    """
    Validate that user has permissions to transfer ownership.
    
    User must be:
    - System Admin, OR
    - Company Admin for the specified company
    
    Args:
        db: Database session
        user_id: User ID to check
        company_id: Company ID
        
    Returns:
        True if user has permissions, False otherwise
    """
    # Check if System Admin
    system_admin = db.execute(
        text("""
            SELECT 1
            FROM [dbo].[User] u
            INNER JOIN ref.UserRole ur ON u.UserRoleID = ur.UserRoleID
            WHERE u.UserID = :user_id
              AND u.IsDeleted = 0
              AND ur.RoleCode = 'system_admin'
        """),
        {"user_id": user_id}
    ).fetchone()
    
    if system_admin:
        return True
    
    # Check if Company Admin
    company_admin = db.execute(
        text("""
            SELECT 1
            FROM dbo.UserCompany uc
            INNER JOIN ref.UserCompanyRole ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
            INNER JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID
            WHERE uc.UserID = :user_id
              AND uc.CompanyID = :company_id
              AND uc.IsDeleted = 0
              AND ucs.StatusCode = 'active'
              AND ucr.RoleCode = 'company_admin'
        """),
        {"user_id": user_id, "company_id": company_id}
    ).fetchone()
    
    return company_admin is not None


async def _validate_user_in_company(
    db: Session,
    user_id: int,
    company_id: int
) -> bool:
    """
    Validate that user is an active member of the company.
    
    Args:
        db: Database session
        user_id: User ID to check
        company_id: Company ID
        
    Returns:
        True if user is active member, False otherwise
    """
    result = db.execute(
        text("""
            SELECT 1
            FROM dbo.UserCompany uc
            INNER JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID
            WHERE uc.UserID = :user_id
              AND uc.CompanyID = :company_id
              AND uc.IsDeleted = 0
              AND ucs.StatusCode = 'active'
        """),
        {"user_id": user_id, "company_id": company_id}
    ).fetchone()
    
    return result is not None

