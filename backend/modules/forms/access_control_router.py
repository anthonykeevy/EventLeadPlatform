"""
Form Access Control Router
API endpoints for form access control operations
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
from datetime import datetime

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from .access_control_service import (
    grant_access,
    revoke_access,
    get_form_access_list,
    check_user_access,
    get_user_access_level
)
from .access_control_schemas import (
    GrantAccessRequest,
    GrantAccessResponse,
    RevokeAccessResponse,
    AccessListResponse,
    AccessCheckResponse,
    AccessControlResponse,
    AccessTypeResponse,
    RelationshipTypeResponse,
    UserResponse,
    CompanyResponse
)
# Import models in correct order to avoid SQLAlchemy relationship resolution issues
# Import all models that have relationships to ensure they're all registered
from models.company_relationship import CompanyRelationship  # Must be before CompanyRelationshipType
from models.ref.company_relationship_type import CompanyRelationshipType
from models.ref.form_access_control_access_type import FormAccessControlAccessType
from models.form_access_control import FormAccessControl  # This depends on CompanyRelationshipType
from models.user import User
from models.company import Company
from models.form import Form  # This triggers model configuration
from sqlalchemy import select
from common.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/forms", tags=["forms-access-control"])


@router.post(
    "/{form_id}/access",
    response_model=GrantAccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Grant form access",
    description="Grant access to a form for a user/company with specified access type"
)
async def grant_form_access(
    form_id: int,
    request: GrantAccessRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> GrantAccessResponse:
    """
    Grant access to a form (AC-2.9.13).
    
    Requires user to have Manage access to the form.
    """
    try:
        # Validate user has Manage access to form
        has_manage_access = await check_user_access(db, form_id, current_user.user_id, "MANAGE")
        if not has_manage_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must have Manage access to grant form access"
            )
        
        # Get form to determine form owner's company
        form = db.execute(
            select(Form).where(
                Form.FormID == form_id,
                Form.IsDeleted == False
            )
        ).scalar_one_or_none()
        
        if not form:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Form not found: {form_id}"
            )
        
        # Form owner's company (the company that owns the form)
        form_company_id = form.CompanyID
        
        # Grant access - handle user_id OR company_id
        # If user_id provided: grant access to specific user
        # If company_id provided: grant access to all users in that company (company-wide access)
        if request.user_id:
            # Grant access to specific user
            access_control = await grant_access(
                db=db,
                form_id=form_id,
                user_id=request.user_id,
                company_id=form_company_id,  # Form owner's company
                granted_by=current_user.user_id,
                access_type_id=request.form_access_control_access_type_id,
                relationship_type_id=request.company_relationship_type_id,
                expiry_date=request.expiry_date
            )
        elif request.company_id:
            # For company-wide access, we need to grant access to each user in the target company
            # This is a limitation of the current schema (UserID is required)
            # For now, we'll raise an error and ask user to select specific users
            # TODO: Implement company-wide access by granting to all users in the company
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company-wide access not yet implemented. Please grant access to specific users from the company."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either userId or companyId must be provided"
            )
        
        db.commit()
        db.refresh(access_control)
        
        # Convert to response
        access_response = _access_control_to_response(access_control, db)
        
        target_user_id = request.user_id if request.user_id else request.company_id
        logger.info(f"Form access granted: FormID={form_id}, UserID={target_user_id}")
        
        return GrantAccessResponse(
            success=True,
            message="Access granted successfully",
            access_control=access_response
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Invalid access grant request: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_detail = str(e)
        logger.error(f"Error granting form access: {error_detail}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to grant form access: {error_detail}"
        )


@router.get(
    "/{form_id}/access",
    response_model=AccessListResponse,
    summary="Get form access list",
    description="Get all access grants for a form"
)
async def get_form_access_list_endpoint(
    form_id: int,
    access_type_id: int = None,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AccessListResponse:
    """
    Get access list for a form (AC-2.9.13).
    
    Requires user to have View access to the form.
    """
    try:
        # Validate user has View access to form
        has_view_access = await check_user_access(db, form_id, current_user.user_id, "VIEW")
        if not has_view_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to view this form's access list"
            )
        
        # Get access list
        access_list = await get_form_access_list(
            db=db,
            form_id=form_id,
            company_id=current_user.company_id,
            access_type_id=access_type_id
        )
        
        # Convert to response
        access_responses = []
        for ac in access_list:
            try:
                response = _access_control_to_response(ac, db)
                # Log user/company info for debugging
                if response.user:
                    logger.debug(f"Access entry {ac.FormAccessControlID}: User={response.user.email} (ID={ac.UserID})")
                elif ac.UserID:
                    logger.warning(f"Access entry {ac.FormAccessControlID}: UserID={ac.UserID} but user details not found")
                if response.company:
                    logger.debug(f"Access entry {ac.FormAccessControlID}: Company={response.company.company_name} (ID={ac.CompanyID})")
                elif ac.CompanyID:
                    logger.warning(f"Access entry {ac.FormAccessControlID}: CompanyID={ac.CompanyID} but company details not found")
                access_responses.append(response)
            except Exception as e:
                logger.error(f"Error converting access entry {ac.FormAccessControlID} to response: {str(e)}", exc_info=True)
                # Continue with other entries
                continue
        
        logger.info(f"Retrieved {len(access_responses)} access entries for FormID={form_id}")
        
        return AccessListResponse(
            access_entries=access_responses,
            total_count=len(access_responses)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching form access list: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch form access list"
        )


@router.delete(
    "/{form_id}/access/{access_id}",
    response_model=RevokeAccessResponse,
    summary="Revoke form access",
    description="Revoke access to a form (soft delete)"
)
async def revoke_form_access(
    form_id: int,
    access_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> RevokeAccessResponse:
    """
    Revoke access to a form (AC-2.9.13).
    
    Requires user to have Manage access to the form.
    """
    try:
        # Validate user has Manage access to form
        has_manage_access = await check_user_access(db, form_id, current_user.user_id, "MANAGE")
        if not has_manage_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must have Manage access to revoke form access"
            )
        
        # Revoke access
        await revoke_access(
            db=db,
            access_id=access_id,
            form_id=form_id,
            revoked_by=current_user.user_id,
            company_id=current_user.company_id
        )
        
        db.commit()
        
        logger.info(f"Form access revoked: FormID={form_id}, AccessID={access_id}")
        
        return RevokeAccessResponse(
            success=True,
            message="Access revoked successfully",
            access_id=access_id
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Invalid access revocation request: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_detail = str(e)
        logger.error(f"Error revoking form access: {error_detail}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to revoke form access: {error_detail}"
        )


@router.get(
    "/{form_id}/access/check",
    response_model=AccessCheckResponse,
    summary="Check form access",
    description="Check current user's access level to a form"
)
async def check_form_access_endpoint(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AccessCheckResponse:
    """
    Check current user's access level to a form (AC-2.9.13).
    """
    try:
        # Get user's access level
        access_level = await get_user_access_level(db, form_id, current_user.user_id)
        
        # Get access type if access granted
        access_type_response = None
        if access_level:
            access_type = db.execute(
                select(FormAccessControlAccessType).where(
                    FormAccessControlAccessType.AccessTypeCode == access_level,
                    FormAccessControlAccessType.IsDeleted == False,
                    FormAccessControlAccessType.IsActive == True
                )
            ).scalar_one_or_none()
            
            if access_type:
                access_type_response = AccessTypeResponse(
                    form_access_control_access_type_id=access_type.FormAccessControlAccessTypeID,
                    access_type_code=access_type.AccessTypeCode,
                    access_type_name=access_type.AccessTypeName,
                    access_type_description=access_type.AccessTypeDescription,
                    is_active=access_type.IsActive,
                    sort_order=access_type.SortOrder
                )
        
        return AccessCheckResponse(
            has_access=access_level is not None,
            access_level=access_level,
            access_type=access_type_response
        )
        
    except Exception as e:
        logger.error(f"Error checking form access: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check form access"
        )


@router.get(
    "/access-types",
    response_model=List[AccessTypeResponse],
    summary="Get access types",
    description="Get all form access control access types"
)
async def get_access_types(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[AccessTypeResponse]:
    """
    Get all access types (AC-2.9.14).
    """
    try:
        logger.info(f"Fetching access types for user {current_user.user_id}")
        access_types = db.execute(
            select(FormAccessControlAccessType).where(
                FormAccessControlAccessType.IsDeleted == False,
                FormAccessControlAccessType.IsActive == True
            ).order_by(FormAccessControlAccessType.SortOrder)
        ).scalars().all()
        
        logger.info(f"Found {len(access_types)} access types")
        
        # Create response objects - FastAPI will serialize with aliases automatically
        response_objects = []
        for at in access_types:
            try:
                response_obj = AccessTypeResponse(
                    form_access_control_access_type_id=at.FormAccessControlAccessTypeID,
                    access_type_code=at.AccessTypeCode,
                    access_type_name=at.AccessTypeName,
                    access_type_description=at.AccessTypeDescription,
                    is_active=at.IsActive,
                    sort_order=at.SortOrder
                )
                response_objects.append(response_obj)
            except Exception as e:
                logger.error(f"Error creating access type response {at.FormAccessControlAccessTypeID}: {str(e)}", exc_info=True)
                raise
        
        logger.info(f"Successfully created {len(response_objects)} access type responses")
        return response_objects
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching access types: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch access types: {str(e)}"
        )


@router.get(
    "/relationship-types",
    response_model=List[RelationshipTypeResponse],
    summary="Get relationship types",
    description="Get all company relationship types for form access control"
)
async def get_relationship_types(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[RelationshipTypeResponse]:
    """
    Get all relationship types (AC-2.9.14).
    """
    try:
        logger.info(f"Fetching relationship types for user {current_user.user_id}")
        relationship_types = db.execute(
            select(CompanyRelationshipType).where(
                CompanyRelationshipType.IsDeleted == False,
                CompanyRelationshipType.IsActive == True
            ).order_by(CompanyRelationshipType.TypeName)
        ).scalars().all()
        
        logger.info(f"Found {len(relationship_types)} relationship types")
        
        # Create response objects - FastAPI will serialize with aliases automatically
        response_objects = []
        for rt in relationship_types:
            try:
                response_obj = RelationshipTypeResponse(
                    company_relationship_type_id=rt.CompanyRelationshipTypeID,
                    type_name=rt.TypeName,
                    type_description=rt.TypeDescription,
                    is_active=rt.IsActive
                )
                response_objects.append(response_obj)
            except Exception as e:
                logger.error(f"Error creating relationship type response {rt.CompanyRelationshipTypeID}: {str(e)}", exc_info=True)
                raise
        
        logger.info(f"Successfully created {len(response_objects)} relationship type responses")
        return response_objects
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching relationship types: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch relationship types: {str(e)}"
        )


@router.get(
    "/search-users",
    response_model=List[UserResponse],
    summary="Search users",
    description="Search for users by name or email (for access control selection)"
)
async def search_users(
    query: str = Query(..., min_length=2, description="Search query (name or email)"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[UserResponse]:
    """
    Search for users by name or email (AC-2.9.15).
    Returns active users matching the search query.
    """
    try:
        search_pattern = f"%{query}%"
        users = db.execute(
            select(User).where(
                User.IsDeleted == False,
                User.IsActive == True,
                or_(
                    func.concat(User.FirstName, ' ', User.LastName).ilike(search_pattern),
                    User.Email.ilike(search_pattern),
                    User.FirstName.ilike(search_pattern),
                    User.LastName.ilike(search_pattern)
                )
            ).order_by(User.FirstName, User.LastName).limit(limit)
        ).scalars().all()
        
        return [
            UserResponse(
                user_id=user.UserID,
                email=user.Email,
                first_name=user.FirstName,
                last_name=user.LastName
            )
            for user in users
        ]
    except Exception as e:
        logger.error(f"Error searching users: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search users"
        )


@router.get(
    "/{form_id}/company-members",
    response_model=List[UserResponse],
    summary="Get company members for form",
    description="Get all active users in the form's company (for dropdown selection)"
)
async def get_company_members_for_form(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[UserResponse]:
    """
    Get all active users in the form's company (AC-2.9.15).
    Returns users for dropdown selection when granting access.
    """
    try:
        # Get form to determine form owner's company
        form = db.execute(
            select(Form).where(
                Form.FormID == form_id,
                Form.IsDeleted == False
            )
        ).scalar_one_or_none()
        
        if not form:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Form not found: {form_id}"
            )
        
        # Verify user has Manage access
        has_manage_access = await check_user_access(db, form_id, current_user.user_id, "MANAGE")
        if not has_manage_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must have Manage access to grant form access"
            )
        
        form_company_id = form.CompanyID
        
        # Get all active users in the form's company
        # Import here to avoid circular dependencies
        from models.user_company import UserCompany
        from models.ref.user_company_status import UserCompanyStatus
        
        # Get active status ID
        active_status = db.execute(
            select(UserCompanyStatus).where(
                UserCompanyStatus.StatusCode == 'active'
            )
        ).scalar_one_or_none()
        
        if not active_status:
            return []
        
        # Query users through UserCompany relationship
        # Exclude the current user (can't grant access to yourself)
        users = db.execute(
            select(User).join(
                UserCompany, User.UserID == UserCompany.UserID
            ).where(
                UserCompany.CompanyID == form_company_id,
                UserCompany.StatusID == active_status.UserCompanyStatusID,
                UserCompany.IsDeleted == False,
                User.IsDeleted == False,
                User.UserID != current_user.user_id  # Exclude current user
            ).order_by(User.FirstName, User.LastName)
        ).scalars().all()
        
        return [
            UserResponse(
                user_id=user.UserID,
                email=user.Email,
                first_name=user.FirstName,
                last_name=user.LastName
            )
            for user in users
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching company members: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch company members"
        )


@router.get(
    "/{form_id}/related-companies",
    response_model=List[CompanyResponse],
    summary="Get related companies for form",
    description="Get all companies with relationships to the form's company (for dropdown selection)"
)
async def get_related_companies_for_form(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[CompanyResponse]:
    """
    Get all companies with relationships to the form's company (AC-2.9.15).
    Returns companies for dropdown selection when granting access.
    """
    try:
        # Get form to determine form owner's company
        form = db.execute(
            select(Form).where(
                Form.FormID == form_id,
                Form.IsDeleted == False
            )
        ).scalar_one_or_none()
        
        if not form:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Form not found: {form_id}"
            )
        
        # Verify user has Manage access
        has_manage_access = await check_user_access(db, form_id, current_user.user_id, "MANAGE")
        if not has_manage_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must have Manage access to grant form access"
            )
        
        form_company_id = form.CompanyID
        
        # Get related company IDs (companies with relationships to form's company)
        from models.company_relationship import CompanyRelationship
        related_companies = db.execute(
            select(CompanyRelationship).where(
                or_(
                    CompanyRelationship.ParentCompanyID == form_company_id,
                    CompanyRelationship.ChildCompanyID == form_company_id
                ),
                CompanyRelationship.IsDeleted == False,
                CompanyRelationship.Status == 'active'
            )
        ).scalars().all()
        
        related_company_ids = set()
        for rel in related_companies:
            if rel.ParentCompanyID == form_company_id:
                related_company_ids.add(rel.ChildCompanyID)
            else:
                related_company_ids.add(rel.ParentCompanyID)
        
        if not related_company_ids:
            return []
        
        # Get company details
        companies = db.execute(
            select(Company).where(
                Company.CompanyID.in_(related_company_ids),
                Company.IsDeleted == False,
                Company.IsActive == True
            ).order_by(Company.CompanyName)
        ).scalars().all()
        
        return [
            CompanyResponse(
                company_id=company.CompanyID,
                company_name=company.CompanyName
            )
            for company in companies
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching related companies: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch related companies"
        )


@router.get(
    "/{form_id}/search-companies",
    response_model=List[CompanyResponse],
    summary="Search companies for form access",
    description="Search for companies by name that can be granted access to a specific form. Filters by form company relationships."
)
async def search_companies_for_form(
    form_id: int,
    query: str = Query(..., min_length=2, description="Search query (company name)"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[CompanyResponse]:
    """
    Search for companies by name that can be granted access to a form (AC-2.9.15).
    
    Note: Company-wide access is not yet implemented. This endpoint returns companies
    with relationships to the form's company for reference.
    
    Returns active companies matching the search query, filtered to:
    1. Companies with relationships to the form's company
    """
    try:
        # Get form to determine form owner's company
        form = db.execute(
            select(Form).where(
                Form.FormID == form_id,
                Form.IsDeleted == False
            )
        ).scalar_one_or_none()
        
        if not form:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Form not found: {form_id}"
            )
        
        # Verify user has Manage access to grant access
        has_manage_access = await check_user_access(db, form_id, current_user.user_id, "MANAGE")
        if not has_manage_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must have Manage access to grant form access"
            )
        
        form_company_id = form.CompanyID
        
        # Get related company IDs (companies with relationships to form's company)
        from models.company_relationship import CompanyRelationship
        related_companies = db.execute(
            select(CompanyRelationship).where(
                or_(
                    CompanyRelationship.ParentCompanyID == form_company_id,
                    CompanyRelationship.ChildCompanyID == form_company_id
                ),
                CompanyRelationship.IsDeleted == False,
                CompanyRelationship.Status == 'active'
            )
        ).scalars().all()
        
        related_company_ids = set()
        for rel in related_companies:
            if rel.ParentCompanyID == form_company_id:
                related_company_ids.add(rel.ChildCompanyID)
            else:
                related_company_ids.add(rel.ParentCompanyID)
        
        if not related_company_ids:
            return []
        
        # Search companies by name, filtered to related companies
        search_pattern = f"%{query}%"
        companies = db.execute(
            select(Company).where(
                Company.CompanyID.in_(related_company_ids),
                Company.IsDeleted == False,
                Company.IsActive == True,
                Company.CompanyName.ilike(search_pattern)
            ).order_by(Company.CompanyName).limit(limit)
        ).scalars().all()
        
        # Create response objects using snake_case field names (Pydantic v2)
        # FastAPI will automatically serialize with camelCase aliases
        return [
            CompanyResponse(
                company_id=company.CompanyID,
                company_name=company.CompanyName
            )
            for company in companies
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching companies: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search companies"
        )


# Helper function to convert FormAccessControl to response
def _access_control_to_response(access_control, db: Session) -> AccessControlResponse:
    """Convert FormAccessControl model to AccessControlResponse schema."""
    # Get access type
    access_type_response = None
    if access_control.access_type:
        access_type_response = AccessTypeResponse(
            form_access_control_access_type_id=access_control.access_type.FormAccessControlAccessTypeID,
            access_type_code=access_control.access_type.AccessTypeCode,
            access_type_name=access_control.access_type.AccessTypeName,
            access_type_description=access_control.access_type.AccessTypeDescription,
            is_active=access_control.access_type.IsActive,
            sort_order=access_control.access_type.SortOrder
        )
    
    # Get relationship type
    relationship_type_response = None
    if access_control.relationship_type:
        relationship_type_response = RelationshipTypeResponse(
            company_relationship_type_id=access_control.relationship_type.CompanyRelationshipTypeID,
            type_name=access_control.relationship_type.TypeName,
            type_description=access_control.relationship_type.TypeDescription,
            is_active=access_control.relationship_type.IsActive
        )
    
    # Get granted by user
    granted_by_response = None
    if access_control.granted_by_user:
        granted_by_response = UserResponse(
            user_id=access_control.granted_by_user.UserID,
            email=access_control.granted_by_user.Email,
            first_name=access_control.granted_by_user.FirstName,
            last_name=access_control.granted_by_user.LastName
        )
    
    # Get user details (if user access) - use loaded relationship if available
    user_response = None
    if access_control.UserID:
        # Try to use the loaded relationship first
        user = access_control.user if hasattr(access_control, 'user') and access_control.user else None
        # Fallback to database fetch if relationship not loaded
        if not user:
            user = db.get(User, access_control.UserID)
        if user:
            user_response = UserResponse(
                user_id=user.UserID,
                email=user.Email,
                first_name=user.FirstName,
                last_name=user.LastName
            )
    
    # Get company details (if company access or user's company) - use loaded relationship if available
    company_response = None
    if access_control.CompanyID:
        # Try to use the loaded relationship first
        company = access_control.company if hasattr(access_control, 'company') and access_control.company else None
        # Fallback to database fetch if relationship not loaded
        if not company:
            company = db.get(Company, access_control.CompanyID)
        if company:
            company_response = CompanyResponse(
                company_id=company.CompanyID,
                company_name=company.CompanyName
            )
    
    # Check if expired
    # Use timezone-aware UTC datetime for comparison
    from datetime import timezone
    is_expired = False
    if access_control.ExpiryDate:
        # ExpiryDate from database is timezone-naive UTC, so compare with naive UTC
        # But to be safe, ensure we're comparing like with like
        expiry_date = access_control.ExpiryDate
        if expiry_date.tzinfo is None:
            # Database datetime is naive, assume UTC
            current_utc = datetime.now(timezone.utc).replace(tzinfo=None)  # Compare naive with naive
            is_expired = expiry_date < current_utc
        else:
            # If somehow timezone-aware, compare properly
            current_utc = datetime.now(timezone.utc)
            is_expired = expiry_date < current_utc
    
    return AccessControlResponse(
        form_access_control_id=access_control.FormAccessControlID,
        form_id=access_control.FormID,
        user_id=access_control.UserID,
        company_id=access_control.CompanyID,
        form_access_control_access_type_id=access_control.FormAccessControlAccessTypeID,
        company_relationship_type_id=access_control.CompanyRelationshipTypeID,
        access_type=access_type_response,
        relationship_type=relationship_type_response,
        user=user_response,
        company=company_response,
        granted_by=granted_by_response,
        granted_date=access_control.GrantedDate,
        expiry_date=access_control.ExpiryDate,
        is_expired=is_expired,
        created_date=access_control.CreatedDate,
        updated_date=access_control.UpdatedDate
    )

