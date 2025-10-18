"""
Countries API Router for Story 1.12
Validation endpoints for country-specific field validation.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from common.database import get_db
from modules.countries.validation_engine import ValidationEngine
from modules.countries.schemas import (
    ValidationRequest, 
    ValidationResponse,
    MultiFieldValidationRequest,
    MultiFieldValidationResponse,
    ValidationRuleResponse
)

router = APIRouter(prefix="/api/countries", tags=["countries"])


@router.post("/{country_id}/validate", response_model=ValidationResponse)
def validate_field(
    country_id: int,
    request: ValidationRequest,
    db: Session = Depends(get_db)
):
    """
    Validate a field value using country-specific validation rules.
    
    Supports validation for:
    - phone: Phone numbers with international format
    - postal_code: Postal/zip codes  
    - tax_id: Tax identifiers (ABN/ACN for Australia)
    - email: Email addresses
    
    Returns validation result with formatted value and error messages.
    """
    try:
        validation_engine = ValidationEngine(db)
        result = validation_engine.validate_field(
            country_id=country_id,
            rule_type=request.rule_type,
            value=request.value
        )
        
        return ValidationResponse(
            is_valid=result.is_valid,
            error_message=result.error_message,
            formatted_value=result.formatted_value,
            matched_rule=result.matched_rule
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation failed: {str(e)}"
        )


@router.post("/{country_id}/validate-multiple", response_model=MultiFieldValidationResponse)
def validate_multiple_fields(
    country_id: int,
    request: MultiFieldValidationRequest,
    db: Session = Depends(get_db)
):
    """
    Validate multiple fields at once for form validation.
    
    Request body:
    {
      "fields": {
        "phone": "+61412345678",
        "postal_code": "2000",
        "tax_id": "53004085616"
      }
    }
    
    Returns validation results for all fields.
    """
    try:
        validation_engine = ValidationEngine(db)
        results = validation_engine.validate_multiple_fields(
            country_id=country_id,
            fields=request.fields
        )
        
        # Convert ValidationResult objects to ValidationResponse
        response_results = {}
        all_valid = True
        
        for field_type, result in results.items():
            response_results[field_type] = ValidationResponse(
                is_valid=result.is_valid,
                error_message=result.error_message,
                formatted_value=result.formatted_value,
                matched_rule=result.matched_rule
            )
            if not result.is_valid:
                all_valid = False
        
        return MultiFieldValidationResponse(
            results=response_results,
            all_valid=all_valid
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Multi-field validation failed: {str(e)}"
        )


@router.get("/{country_id}/validation-rules/{rule_type}", response_model=List[ValidationRuleResponse])
def get_validation_rules(
    country_id: int,
    rule_type: str,
    db: Session = Depends(get_db)
):
    """
    Get all validation rules for a country and rule type.
    
    Useful for frontend to show validation requirements or examples.
    """
    try:
        validation_engine = ValidationEngine(db)
        rules = validation_engine.get_validation_rules(country_id, rule_type)
        
        response_rules = []
        for rule in rules:
            response_rules.append(ValidationRuleResponse(
                rule_key=getattr(rule, 'RuleKey', ''),
                rule_type=rule_type,
                validation_pattern=getattr(rule, 'ValidationPattern', ''),
                error_message=getattr(rule, 'ValidationMessage', ''),
                min_length=getattr(rule, 'MinLength', None),
                max_length=getattr(rule, 'MaxLength', None),
                example_value=getattr(rule, 'ExampleValue', None),
                is_active=getattr(rule, 'IsActive', True),
                priority=getattr(rule, 'Priority', 0)
            ))
        
        return response_rules
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get validation rules: {str(e)}"
        )


@router.post("/{country_id}/validate-abn", response_model=ValidationResponse)
def validate_abn(
    country_id: int,
    request: ValidationRequest,
    db: Session = Depends(get_db)
):
    """
    Specific ABN validation endpoint with checksum verification.
    
    Only works for Australia (country_id=1).
    Validates both format and checksum algorithm.
    """
    if country_id != 1:  # Australia only for now
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ABN validation only supported for Australia"
        )
    
    try:
        validation_engine = ValidationEngine(db)
        result = validation_engine.validate_field(
            country_id=country_id,
            rule_type='tax_id',
            value=request.value
        )
        
        return ValidationResponse(
            is_valid=result.is_valid,
            error_message=result.error_message,
            formatted_value=result.formatted_value,
            matched_rule=result.matched_rule
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ABN validation failed: {str(e)}"
        )
