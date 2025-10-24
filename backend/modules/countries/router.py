"""
Countries API Router for Story 1.12
Validation endpoints for country-specific field validation.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from common.database import get_db
from modules.countries.validation_engine import ValidationEngine
from modules.countries.country_service import get_active_countries
from modules.countries.schemas import (
    ValidationRequest, 
    ValidationResponse,
    MultiFieldValidationRequest,
    MultiFieldValidationResponse,
    ValidationRuleResponse
)

router = APIRouter(prefix="/api/countries", tags=["countries"])


@router.get("", response_model=List[dict])
def list_countries(db: Session = Depends(get_db)):
    """
    Get list of active countries with validation configuration.
    
    Story 1.20: Frontend fetches this to dynamically load country options.
    Returns country metadata including labels for postal codes, tax IDs, states, etc.
    
    This ensures frontend CountryIDs always match database, avoiding sync issues.
    """
    return get_active_countries(db)


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
            display_value=result.display_value,
            matched_rule=result.matched_rule,
            display_format=result.display_format,
            spacing_pattern=result.spacing_pattern
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
                display_value=result.display_value,
                matched_rule=result.matched_rule,
                display_format=result.display_format,
                spacing_pattern=result.spacing_pattern
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


@router.get("/{country_id}/validation-rules/{rule_type}", response_model=dict)
def get_validation_rules(
    country_id: int,
    rule_type: str,
    db: Session = Depends(get_db)
):
    """
    Get validation rules metadata for a country and rule type.
    
    Story 1.20: Frontend uses this to set input constraints (maxLength, pattern hints).
    Returns aggregated metadata to ensure frontend rules match backend rules.
    """
    try:
        validation_engine = ValidationEngine(db)
        rules = validation_engine.get_validation_rules(country_id, rule_type)
        
        if not rules:
            return {
                "has_rules": False,
                "min_length": None,
                "max_length": None,
                "example_value": None
            }
        
        # Aggregate metadata from all rules (use most permissive)
        max_lengths = [getattr(r, 'MaxLength') for r in rules if getattr(r, 'MaxLength', None)]
        min_lengths = [getattr(r, 'MinLength') for r in rules if getattr(r, 'MinLength', None)]
        
        return {
            "has_rules": True,
            "min_length": min(min_lengths) if min_lengths else None,
            "max_length": max(max_lengths) if max_lengths else None,  # Most permissive
            "example_value": getattr(rules[0], 'ExampleValue', None),
            "display_format": getattr(rules[0], 'DisplayFormat', None),
            "spacing_pattern": getattr(rules[0], 'SpacingPattern', None)
        }
        
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
            display_value=result.display_value,
            matched_rule=result.matched_rule,
            display_format=result.display_format,
            spacing_pattern=result.spacing_pattern
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ABN validation failed: {str(e)}"
        )
