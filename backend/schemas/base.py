"""
Base Pydantic Schemas
Common response patterns and pagination
"""
from typing import Any, Optional, Generic, TypeVar, List
from pydantic import BaseModel, Field, ConfigDict


# Generic type for paginated responses
T = TypeVar('T')


class BaseResponse(BaseModel):
    """
    Standard API response wrapper.
    
    Attributes:
        success: Whether operation was successful
        message: Human-readable message
        data: Response data (optional)
        
    Example:
        {
            "success": true,
            "message": "User created successfully",
            "data": {"user_id": 123, "email": "user@example.com"}
        }
    """
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Human-readable message describing the result")
    data: Optional[Any] = Field(None, description="Response data")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {"id": 123, "name": "Example"}
            }
        }
    )


class ErrorResponse(BaseModel):
    """
    Standard API error response.
    
    Attributes:
        success: Always False for errors
        error: Error type or code
        message: Human-readable error message
        details: Additional error details (optional)
        
    Example:
        {
            "success": false,
            "error": "ValidationError",
            "message": "Email address is required",
            "details": {"field": "email", "constraint": "required"}
        }
    """
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error type or code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Any] = Field(None, description="Additional error context")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "error": "ValidationError",
                "message": "Invalid input data",
                "details": {"field": "email", "issue": "Invalid email format"}
            }
        }
    )


class PaginationParams(BaseModel):
    """
    Pagination parameters for list endpoints.
    
    Attributes:
        page: Page number (1-based)
        page_size: Number of items per page
        sort_by: Field to sort by (optional)
        sort_order: Sort order ('asc' or 'desc')
        
    Example:
        {
            "page": 1,
            "page_size": 20,
            "sort_by": "created_date",
            "sort_order": "desc"
        }
    """
    page: int = Field(1, ge=1, description="Page number (1-based)")
    page_size: int = Field(20, ge=1, le=100, description="Items per page (max 100)")
    sort_by: Optional[str] = Field(None, description="Field to sort by")
    sort_order: str = Field("asc", pattern="^(asc|desc)$", description="Sort order: 'asc' or 'desc'")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "page": 1,
                "page_size": 20,
                "sort_by": "created_date",
                "sort_order": "desc"
            }
        }
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Paginated response wrapper.
    
    Attributes:
        success: Whether operation was successful
        message: Human-readable message
        data: Paginated data
        pagination: Pagination metadata
        
    Example:
        {
            "success": true,
            "message": "Users retrieved successfully",
            "data": [
                {"id": 1, "email": "user1@example.com"},
                {"id": 2, "email": "user2@example.com"}
            ],
            "pagination": {
                "page": 1,
                "page_size": 20,
                "total_items": 2,
                "total_pages": 1
            }
        }
    """
    success: bool = Field(True, description="Whether the operation was successful")
    message: str = Field(..., description="Human-readable message")
    data: List[T] = Field(..., description="List of items for current page")
    pagination: dict = Field(..., description="Pagination metadata")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Items retrieved successfully",
                "data": [
                    {"id": 1, "name": "Item 1"},
                    {"id": 2, "name": "Item 2"}
                ],
                "pagination": {
                    "page": 1,
                    "page_size": 20,
                    "total_items": 2,
                    "total_pages": 1
                }
            }
        }
    )
    
    @classmethod
    def create(
        cls,
        items: List[T],
        page: int,
        page_size: int,
        total_items: int,
        message: str = "Items retrieved successfully"
    ) -> "PaginatedResponse[T]":
        """
        Create a paginated response from items and pagination params.
        
        Args:
            items: List of items for current page
            page: Current page number
            page_size: Items per page
            total_items: Total number of items across all pages
            message: Response message
            
        Returns:
            PaginatedResponse: Formatted paginated response
        """
        total_pages = (total_items + page_size - 1) // page_size  # Ceiling division
        
        return cls(
            success=True,
            message=message,
            data=items,
            pagination={
                "page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1
            }
        )

