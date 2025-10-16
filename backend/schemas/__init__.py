"""
Pydantic Schemas
Base schemas and common patterns for API requests/responses
"""
from backend.schemas.base import BaseResponse, ErrorResponse, PaginationParams, PaginatedResponse
from backend.schemas.common import validate_email, validate_australian_phone, validate_abn, validate_acn

__all__ = [
    # Base response patterns
    "BaseResponse",
    "ErrorResponse",
    "PaginationParams",
    "PaginatedResponse",
    # Common validators
    "validate_email",
    "validate_australian_phone",
    "validate_abn",
    "validate_acn",
]

