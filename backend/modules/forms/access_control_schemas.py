"""
Form Access Control Schemas
Pydantic models for form access control requests and responses
"""
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List
from datetime import datetime


class GrantAccessRequest(BaseModel):
    """Request schema for granting form access."""
    user_id: Optional[int] = Field(None, alias="userId", description="User ID to grant access to (optional if company_id provided)")
    company_id: Optional[int] = Field(None, alias="companyId", description="Company ID to grant access to (optional if user_id provided)")
    form_access_control_access_type_id: int = Field(..., alias="formAccessControlAccessTypeId", description="FormAccessControlAccessType ID")
    company_relationship_type_id: int = Field(..., alias="companyRelationshipTypeId", description="CompanyRelationshipType ID")
    expiry_date: Optional[datetime] = Field(None, alias="expiryDate", description="Optional expiry date (NULL = permanent access)")
    
    @model_validator(mode='after')
    def validate_user_or_company(self):
        """At least one of user_id or company_id must be provided."""
        if not self.user_id and not self.company_id:
            raise ValueError("Either userId or companyId must be provided")
        return self
    
    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "userId": 123,
                "formAccessControlAccessTypeId": 1,
                "companyRelationshipTypeId": 1,
                "expiryDate": "2025-12-31T23:59:59Z"
            }
        }
    }


class AccessTypeResponse(BaseModel):
    """Response schema for access type reference data."""
    form_access_control_access_type_id: int = Field(..., alias="formAccessControlAccessTypeId")
    access_type_code: str = Field(..., alias="accessTypeCode")
    access_type_name: str = Field(..., alias="accessTypeName")
    access_type_description: Optional[str] = Field(None, alias="accessTypeDescription")
    is_active: bool = Field(..., alias="isActive")
    sort_order: int = Field(..., alias="sortOrder")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "formAccessControlAccessTypeId": 1,
                "accessTypeCode": "VIEW",
                "accessTypeName": "View",
                "accessTypeDescription": "Can view form and basic information",
                "isActive": True,
                "sortOrder": 1
            }
        }
    )


class RelationshipTypeResponse(BaseModel):
    """Response schema for relationship type reference data."""
    company_relationship_type_id: int = Field(..., alias="companyRelationshipTypeId")
    type_name: str = Field(..., alias="typeName")
    type_description: Optional[str] = Field(None, alias="typeDescription")
    is_active: bool = Field(..., alias="isActive")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "companyRelationshipTypeId": 1,
                "typeName": "Partner",
                "typeDescription": "Business partner relationship",
                "isActive": True
            }
        }
    )


class UserResponse(BaseModel):
    """Response schema for user data in access control."""
    user_id: int = Field(..., alias="userId")
    email: str
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    
    model_config = {
        "populate_by_name": True
    }


class CompanyResponse(BaseModel):
    """Response schema for company data in access control."""
    company_id: int = Field(..., alias="companyId")
    company_name: str = Field(..., alias="companyName")
    
    model_config = {
        "populate_by_name": True
    }


class AccessControlResponse(BaseModel):
    """Response schema for form access control entry."""
    form_access_control_id: int = Field(..., alias="formAccessControlId")
    form_id: int = Field(..., alias="formId")
    user_id: Optional[int] = Field(None, alias="userId")
    company_id: Optional[int] = Field(None, alias="companyId")
    form_access_control_access_type_id: int = Field(..., alias="formAccessControlAccessTypeId")
    company_relationship_type_id: Optional[int] = Field(None, alias="companyRelationshipTypeId")
    access_type: Optional[AccessTypeResponse] = Field(None, alias="accessType")
    relationship_type: Optional[RelationshipTypeResponse] = Field(None, alias="relationshipType")
    user: Optional[UserResponse] = Field(None, alias="user")
    company: Optional[CompanyResponse] = Field(None, alias="company")
    granted_by: Optional[UserResponse] = Field(None, alias="grantedBy")
    granted_date: datetime = Field(..., alias="grantedDate")
    expiry_date: Optional[datetime] = Field(None, alias="expiryDate")
    is_expired: bool = Field(..., alias="isExpired")
    created_date: datetime = Field(..., alias="createdDate")
    updated_date: Optional[datetime] = Field(None, alias="updatedDate")
    
    class Config:
        populate_by_name = True


class AccessListResponse(BaseModel):
    """Response schema for access list."""
    access_entries: List[AccessControlResponse] = Field(..., alias="accessEntries")
    total_count: int = Field(..., alias="totalCount")
    
    class Config:
        populate_by_name = True


class AccessCheckResponse(BaseModel):
    """Response schema for access check."""
    has_access: bool = Field(..., alias="hasAccess")
    access_level: Optional[str] = Field(None, alias="accessLevel")
    access_type: Optional[AccessTypeResponse] = Field(None, alias="accessType")
    
    class Config:
        populate_by_name = True


class GrantAccessResponse(BaseModel):
    """Response schema for grant access operation."""
    success: bool
    message: str
    access_control: AccessControlResponse = Field(..., alias="accessControl")
    
    class Config:
        populate_by_name = True


class RevokeAccessResponse(BaseModel):
    """Response schema for revoke access operation."""
    success: bool
    message: str
    access_id: int = Field(..., alias="accessId")
    
    class Config:
        populate_by_name = True

