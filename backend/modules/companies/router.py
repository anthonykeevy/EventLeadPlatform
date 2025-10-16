"""
Company Management Router
Endpoints for company creation and management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from modules.auth.jwt_service import create_access_token, create_refresh_token
from .schemas import CreateCompanySchema, CreateCompanyResponse
from .service import create_company
from common.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/companies", tags=["companies"])


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

