"""
Form Version Router
Endpoints for managing form versions
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from modules.forms.version_service import FormVersionService
from schemas.form_version import (
    FormVersionCreate,
    FormVersionResponse,
    FormVersionListResponse,
    FormVersionUpdate
)
from common.logger import get_logger

logger = get_logger(__name__)

# Router for /versions endpoints
versions_router = APIRouter(prefix="/api/forms/{form_id}/versions", tags=["form-versions"])

# Router for /live endpoints
active_version_router = APIRouter(prefix="/api/forms/{form_id}/live", tags=["form-versions"])

@versions_router.post(
    "",
    response_model=FormVersionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new version",
    description="Create a new draft version for the form"
)
async def create_version(
    form_id: int,
    request: FormVersionCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        service = FormVersionService(db)
        version = await service.create_version(
            form_id=form_id,
            user_id=current_user.user_id,
            definition=request.definition,
            comment=request.version_comment
        )
        db.commit()
        return version
    except ValueError as e:
        logger.warning(f"Invalid version creation: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating version: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create version")

@versions_router.get(
    "",
    response_model=FormVersionListResponse,
    summary="List versions",
    description="Get all versions for the form"
)
async def list_versions(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        service = FormVersionService(db)
        versions = await service.get_versions(form_id, current_user.user_id)
        return FormVersionListResponse(versions=versions)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing versions: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list versions")

@versions_router.get(
    "/{version_number}",
    response_model=FormVersionResponse,
    summary="Get version",
    description="Get a specific version"
)
async def get_version(
    form_id: int,
    version_number: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        service = FormVersionService(db)
        version = await service.get_version(form_id, version_number, current_user.user_id)
        if not version:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Version not found")
        return version
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving version: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve version")

@versions_router.put(
    "/{version_number}",
    response_model=FormVersionResponse,
    summary="Update version",
    description="Update a draft version"
)
async def update_version(
    form_id: int,
    version_number: int,
    request: FormVersionUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        service = FormVersionService(db)
        version = await service.update_version(
            form_id=form_id,
            version_number=version_number,
            user_id=current_user.user_id,
            definition=request.definition,
            comment=request.version_comment
        )
        db.commit()
        return version
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating version: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update version")

@versions_router.post(
    "/{version_number}/publish",
    response_model=FormVersionResponse,
    summary="Publish version",
    description="Make this version the active one"
)
async def publish_version(
    form_id: int,
    version_number: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        service = FormVersionService(db)
        version = await service.publish_version(form_id, version_number, current_user.user_id)
        db.commit()
        return version
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error publishing version: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to publish version")

@active_version_router.get(
    "",
    response_model=FormVersionResponse,
    summary="Get active version",
    description="Get the currently published version"
)
async def get_active_version(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        service = FormVersionService(db)
        version = await service.get_active_version(form_id, current_user.user_id)
        if not version:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active version found")
        return version
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving active version: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve active version")
