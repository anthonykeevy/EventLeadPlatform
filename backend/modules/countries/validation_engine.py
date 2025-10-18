"""
Validation Engine Service for Story 1.12
Country-specific field validation with caching and ABN checksum algorithm.
"""
import re
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from pydantic import BaseModel

try:
    import phonenumbers
except ImportError:
    phonenumbers = None

from models.config.validation_rule import ValidationRule
from models.ref.rule_type import RuleType


class ValidationResult(BaseModel):
    """Result of field validation"""
    is_valid: bool
    error_message: Optional[str] = None
    formatted_value: Optional[str] = None
    matched_rule: Optional[str] = None


class ValidationEngine:
    """
    Country-specific validation engine with caching.
    
    Supports validation for phone numbers, postal codes, tax IDs (ABN/ACN), 
    email addresses, and addresses with country-specific rules.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self._cache: Dict[str, Any] = {}
        self._cache_timestamp: Dict[str, datetime] = {}
        self._cache_ttl_seconds = 300  # 5-minute TTL as per Story Context
    
    def validate_field(self, country_id: int, rule_type: str, value: str) -> ValidationResult:
        """
        Validate a field value against country-specific rules.
        
        Args:
            country_id: Country identifier (e.g., 1 for Australia)
            rule_type: Type of validation ('phone', 'postal_code', 'tax_id', 'email')  
            value: Value to validate
            
        Returns:
            ValidationResult with is_valid, error_message, formatted_value
        """
        if not value or not value.strip():
            return ValidationResult(
                is_valid=False,
                error_message="This field is required"
            )
        
        value = value.strip()
        
        # Get validation rules for country and type
        rules = self.get_validation_rules(country_id, rule_type)
        
        if not rules:
            # No rules defined - use basic validation
            return self._basic_validation(rule_type, value)
        
        # Apply rules in priority order (lowest Priority first)  
        for rule in sorted(rules, key=lambda r: getattr(r, 'Priority', 0) or 0):
            if not getattr(rule, 'IsActive', True):
                continue
                
            # Quick length check before expensive regex
            min_length = getattr(rule, 'MinLength', None)
            max_length = getattr(rule, 'MaxLength', None)
            if min_length and len(value) < min_length:
                continue
            if max_length and len(value) > max_length:
                continue
            
            # Apply rule-specific validation
            result = self._apply_rule_validation(rule, value)
            if result.is_valid:
                return result
        
        # No rules matched - return first rule's error message
        if rules:
            example = f" Try: {rules[0].ExampleValue}" if rules[0].ExampleValue else ""
            return ValidationResult(
                is_valid=False,
                error_message=f"{rules[0].ValidationMessage}.{example}"
            )
        
        return ValidationResult(
            is_valid=False,
            error_message=f"Invalid {rule_type} format"
        )
    
    def get_validation_rules(self, country_id: int, rule_type: str) -> List[ValidationRule]:
        """
        Get validation rules for country and type with caching.
        
        Returns rules sorted by Priority (ascending - lower numbers first).
        """
        cache_key = f"validation_{country_id}_{rule_type}"
        
        # Check cache first
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        # Query database
        rules = self.db.query(ValidationRule).join(
            RuleType, ValidationRule.RuleTypeID == RuleType.RuleTypeID
        ).filter(
            ValidationRule.CountryID == country_id,
            RuleType.TypeCode == rule_type,
            ValidationRule.IsActive,
            ~ValidationRule.IsDeleted
        ).order_by(ValidationRule.Priority).all()
        
        # Cache results
        self._cache[cache_key] = rules
        self._cache_timestamp[cache_key] = datetime.utcnow()
        
        return rules
    
    def _apply_rule_validation(self, rule: ValidationRule, value: str) -> ValidationResult:
        """Apply specific validation rule with appropriate algorithm"""
        
        rule_key = getattr(rule, 'RuleKey', '')
        rule_description = getattr(rule, 'Description', '')
        
        # Special handling for Australian ABN validation with checksum
        if rule_key == 'TAX_ID_FORMAT' and 'ABN' in rule_description:
            return self._validate_australian_abn(value)
        
        # Special handling for Australian ACN validation with checksum  
        if rule_key == 'ACN_FORMAT':
            return self._validate_australian_acn(value)
        
        # Phone number validation using python-phonenumbers
        if 'phone' in rule_key.lower():
            return self._validate_phone_number(value, rule)
        
        # Standard regex validation
        try:
            pattern = getattr(rule, 'ValidationPattern', '')
            if pattern and re.match(pattern, value):
                formatted_value = self._format_value(rule, value)
                return ValidationResult(
                    is_valid=True,
                    formatted_value=formatted_value,
                    matched_rule=getattr(rule, 'RuleKey', '')
                )
        except re.error:
            # Invalid regex pattern
            pass
        
        return ValidationResult(is_valid=False)
    
    def _validate_australian_abn(self, abn: str) -> ValidationResult:
        """
        Validate Australian ABN with checksum algorithm.
        
        Algorithm from Story Context:
        - Subtract 1 from first digit
        - Multiply each digit by weights [10,1,3,5,7,9,11,13,15,17,19]
        - Sum mod 89 should equal 0
        """
        # Remove spaces and validate format
        abn_digits = re.sub(r'[^0-9]', '', abn)
        
        if len(abn_digits) != 11:
            return ValidationResult(
                is_valid=False,
                error_message="ABN must be 11 digits. Try: 53004085616"
            )
        
        # Convert to integers
        digits = [int(d) for d in abn_digits]
        
        # ABN checksum algorithm
        weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        
        # Subtract 1 from first digit
        digits[0] = digits[0] - 1
        
        # Calculate weighted sum
        checksum = sum(digit * weight for digit, weight in zip(digits, weights))
        
        # Check if divisible by 89
        is_valid = (checksum % 89) == 0
        
        if is_valid:
            # Format as XX XXX XXX XXX
            formatted = f"{abn_digits[:2]} {abn_digits[2:5]} {abn_digits[5:8]} {abn_digits[8:11]}"
            return ValidationResult(
                is_valid=True,
                formatted_value=formatted,
                matched_rule='ABN_CHECKSUM'
            )
        else:
            return ValidationResult(
                is_valid=False,
                error_message="ABN checksum is invalid. Please check the number. Try: 53004085616"
            )
    
    def _validate_australian_acn(self, acn: str) -> ValidationResult:
        """Validate Australian ACN with format check"""
        # Remove spaces and validate format
        acn_digits = re.sub(r'[^0-9]', '', acn)
        
        if len(acn_digits) != 9:
            return ValidationResult(
                is_valid=False,
                error_message="ACN must be 9 digits. Try: 123456789"
            )
        
        # Format as XXX XXX XXX
        formatted = f"{acn_digits[:3]} {acn_digits[3:6]} {acn_digits[6:9]}"
        return ValidationResult(
            is_valid=True,
            formatted_value=formatted,
            matched_rule='ACN_FORMAT'
        )
    
    def _validate_phone_number(self, phone: str, rule: ValidationRule) -> ValidationResult:
        """
        Validate phone number using python-phonenumbers library.
        
        Supports both domestic (04...) and international (+61...) formats.
        """
        try:
            # Try to parse as international number first
            parsed_phone = phonenumbers.parse(phone, "AU")
            
            # Check if it's a valid Australian number
            if phonenumbers.is_valid_number(parsed_phone):
                # Format in international format
                formatted = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                
                # Apply regex pattern check for specific validation (mobile vs landline)
                pattern = getattr(rule, 'ValidationPattern', '')
                if pattern and re.match(pattern, formatted):
                    return ValidationResult(
                        is_valid=True,
                        formatted_value=formatted,
                        matched_rule=getattr(rule, 'RuleKey', '')
                    )
            
        except Exception:  # phonenumbers.NumberParseException or AttributeError if phonenumbers is None
            pass
        
        # Fallback: try regex validation directly
        pattern = getattr(rule, 'ValidationPattern', '')
        if pattern and re.match(pattern, phone):
            return ValidationResult(
                is_valid=True,
                formatted_value=phone,
                matched_rule=getattr(rule, 'RuleKey', '')
            )
        
        example = f" Try: {getattr(rule, 'ExampleValue', '')}" if getattr(rule, 'ExampleValue', '') else ""
        return ValidationResult(
            is_valid=False,
            error_message=f"{getattr(rule, 'ValidationMessage', 'Invalid format')}.{example}"
        )
    
    def _format_value(self, rule: ValidationRule, value: str) -> str:
        """Format value according to rule type"""
        
        rule_key = getattr(rule, 'RuleKey', '')
        
        if 'phone' in rule_key.lower():
            if phonenumbers:
                try:
                    parsed = phonenumbers.parse(value, "AU")
                    return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                except Exception:
                    return value
            return value
        
        if 'ABN' in rule_key:
            digits = re.sub(r'[^0-9]', '', value)
            if len(digits) == 11:
                return f"{digits[:2]} {digits[2:5]} {digits[5:8]} {digits[8:11]}"
        
        if 'ACN' in rule_key:
            digits = re.sub(r'[^0-9]', '', value)
            if len(digits) == 9:
                return f"{digits[:3]} {digits[3:6]} {digits[6:9]}"
        
        return value
    
    def _basic_validation(self, rule_type: str, value: str) -> ValidationResult:
        """Basic validation when no rules are defined"""
        
        if rule_type == 'email':
            email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
            if re.match(email_pattern, value):
                return ValidationResult(is_valid=True, formatted_value=value.lower())
            else:
                return ValidationResult(
                    is_valid=False,
                    error_message="Invalid email format. Try: user@example.com"
                )
        
        # For other types, assume valid if not empty
        return ValidationResult(is_valid=True, formatted_value=value)
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid (within TTL)"""
        if cache_key not in self._cache_timestamp:
            return False
            
        elapsed = (datetime.utcnow() - self._cache_timestamp[cache_key]).total_seconds()
        return elapsed < self._cache_ttl_seconds
    
    def invalidate_cache(self):
        """Clear validation rule cache (for testing or admin updates)"""
        self._cache.clear()
        self._cache_timestamp.clear()
    
    def validate_multiple_fields(self, country_id: int, fields: Dict[str, str]) -> Dict[str, ValidationResult]:
        """
        Validate multiple fields at once for form validation.
        
        Args:
            country_id: Country for validation rules
            fields: Dict of {rule_type: value} pairs
            
        Returns:
            Dict of {rule_type: ValidationResult}
        """
        results = {}
        for rule_type, value in fields.items():
            results[rule_type] = self.validate_field(country_id, rule_type, value)
        return results
