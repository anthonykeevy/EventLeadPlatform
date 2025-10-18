"""
Validation API Schemas for Story 1.12
Request/response models for validation endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict


class ValidationRequest(BaseModel):
    """Request schema for field validation"""
    rule_type: str = Field(..., description="Type of validation (phone, postal_code, tax_id, email)")
    value: str = Field(..., description="Value to validate")


class ValidationResponse(BaseModel):
    """Response schema for field validation"""
    is_valid: bool = Field(..., description="Whether the value is valid")
    error_message: Optional[str] = Field(None, description="Error message if validation failed")
    formatted_value: Optional[str] = Field(None, description="Formatted version of the value")
    matched_rule: Optional[str] = Field(None, description="Rule that matched (for debugging)")


class MultiFieldValidationRequest(BaseModel):
    """Request schema for validating multiple fields at once"""
    fields: Dict[str, str] = Field(..., description="Dictionary of rule_type: value pairs")


class MultiFieldValidationResponse(BaseModel):
    """Response schema for multi-field validation"""
    results: Dict[str, ValidationResponse] = Field(..., description="Validation result for each field")
    all_valid: bool = Field(..., description="True if all fields are valid")


class ValidationRuleResponse(BaseModel):
    """Response schema for validation rule information"""
    rule_key: str
    rule_type: str  
    validation_pattern: str
    error_message: str
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    example_value: Optional[str] = None
    is_active: bool
    priority: int
