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
    formatted_value: Optional[str] = None  # International format for storage
    display_value: Optional[str] = None  # Local format for display (Story 1.20)
    matched_rule: Optional[str] = None
    display_format: Optional[str] = None  # Pattern like '04XX XXX XXX'
    spacing_pattern: Optional[str] = None  # How to space digits


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
        
        # Apply rules in precedence order (lowest SortOrder first)  
        for rule in sorted(rules, key=lambda r: getattr(r, 'SortOrder', 999)):
            if not getattr(rule, 'IsActive', True):
                continue
                
            # Quick length check before expensive regex
            min_length = getattr(rule, 'MinLength', None)
            max_length = getattr(rule, 'MaxLength', None)
            if min_length and len(value) < min_length:
                continue
            if max_length and len(value) > max_length:
                continue
            
            # Apply rule-specific validation (pass country_id for normalization)
            result = self._apply_rule_validation(rule, value, country_id)
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
        
        Returns rules sorted by SortOrder (ascending - lower numbers first).
        Story 1.20: Standardized to SortOrder from Priority.
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
        ).order_by(ValidationRule.SortOrder).all()  # Story 1.20: Use SortOrder not Priority
        
        # Cache results
        self._cache[cache_key] = rules
        self._cache_timestamp[cache_key] = datetime.utcnow()
        
        return rules
    
    def _apply_rule_validation(self, rule: ValidationRule, value: str, country_id: int) -> ValidationResult:
        """Apply specific validation rule with appropriate algorithm"""
        
        rule_key = getattr(rule, 'RuleKey', '')
        rule_description = getattr(rule, 'Description', '')
        
        # Special handling for Australian ABN validation with checksum
        if rule_key == 'TAX_ID_FORMAT' and 'ABN' in rule_description:
            return self._validate_australian_abn(value)
        
        # Special handling for Australian ACN validation with checksum  
        if rule_key == 'ACN_FORMAT':
            return self._validate_australian_acn(value)
        
        # Phone number validation (Story 1.20: pass country_id for normalization)
        if 'phone' in rule_key.lower():
            return self._validate_phone_number(value, rule, country_id)
        
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
    
    def _validate_phone_number(self, phone: str, rule: ValidationRule, country_id: int) -> ValidationResult:
        """
        Validate phone number with support for multiple formats.
        
        Story 1.20: Supports all countries with country-specific normalization.
        Auto-normalizes to international format for storage.
        
        Args:
            phone: Phone number to validate
            rule: ValidationRule being applied
            country_id: Country ID for correct prefix normalization
        """
        # Strip spaces, dashes, parentheses
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        # Get the regex pattern for this rule
        pattern = getattr(rule, 'ValidationPattern', '')
        
        # Check if the cleaned phone matches the rule's pattern
        if pattern and re.match(pattern, cleaned_phone):
            # Phone matches! Now normalize to international format with correct country prefix
            normalized = self._normalize_phone_by_country(cleaned_phone, country_id)
            
            # Calculate display value (Story 1.20)
            display_val = self._get_display_value(normalized, rule)
            
            return ValidationResult(
                is_valid=True,
                formatted_value=normalized,
                display_value=display_val,
                matched_rule=getattr(rule, 'RuleKey', ''),
                display_format=getattr(rule, 'DisplayFormat', None),
                spacing_pattern=getattr(rule, 'SpacingPattern', None)
            )
        
        # Pattern didn't match - return error with example
        example = f" Try: {getattr(rule, 'ExampleValue', '')}" if getattr(rule, 'ExampleValue', '') else ""
        return ValidationResult(
            is_valid=False,
            error_message=f"{getattr(rule, 'ValidationMessage', 'Invalid format')}.{example}"
        )
    
    def _normalize_phone_by_country(self, phone: str, country_id: int) -> str:
        """
        Normalize phone numbers to international format based on country.
        
        Story 1.20: Country-aware normalization for all supported countries.
        
        Args:
            phone: Phone number in local or international format
            country_id: Country ID (1=AU, 14=NZ, 15=US, 16=GB, 17=CA)
            
        Returns:
            Phone in international format with country prefix
        """
        # Already in international format
        if phone.startswith('+'):
            return phone
        
        # Australia (ID=1): 04... → +614..., 02... → +612...
        if country_id == 1:
            if phone.startswith('0'):
                return '+61' + phone[1:]
            if phone.startswith('1'):  # 1800, 1300
                return '+61' + phone
        
        # New Zealand (ID=14): 0... → +64...
        elif country_id == 14:
            if phone.startswith('0'):
                return '+64' + phone[1:]
        
        # USA (ID=15): 10 digits → +1...
        elif country_id == 15:
            if len(phone) == 10 and not phone.startswith('+'):
                return '+1' + phone
        
        # UK (ID=16): 0... → +44...
        elif country_id == 16:
            if phone.startswith('0'):
                return '+44' + phone[1:]
        
        # Canada (ID=17): 10 digits → +1...
        elif country_id == 17:
            if len(phone) == 10 and not phone.startswith('+'):
                return '+1' + phone
        
        # Fallback: return as-is
        return phone
    
    def _normalize_australian_phone(self, phone: str) -> str:
        """
        Normalize Australian phone numbers to international format.
        
        Story 1.20: Comprehensive normalization for all Australian formats.
        
        Rules:
        - 04XXXXXXXX → +614XXXXXXXX (mobile)
        - 02XXXXXXXX → +612XXXXXXXX (NSW/ACT landline)
        - 03XXXXXXXX → +613XXXXXXXX (VIC/TAS landline)
        - 07XXXXXXXX → +617XXXXXXXX (QLD landline)
        - 08XXXXXXXX → +618XXXXXXXX (SA/WA/NT landline)
        - 1800XXXXXX → +611800XXXXXX (toll-free)
        - 1300XXXXXX → +611300XXXXXX (local rate)
        - 13XXXX → +6113XXXX (short code)
        - +61... → +61... (already normalized)
        """
        # Already in international format
        if phone.startswith('+61'):
            return phone
        
        # Local format starting with 0 (mobile/landline)
        if phone.startswith('0'):
            return '+61' + phone[1:]  # Replace leading 0 with +61
        
        # Business numbers (1800, 1300, 13)
        if phone.startswith('1'):
            return '+61' + phone  # Prepend +61
        
        # Fallback: return as-is (shouldn't happen with proper validation)
        return phone
    
    def _get_display_value(self, international_value: str, rule: ValidationRule) -> str:
        """
        Convert international format to local display format.
        
        Story 1.20: Shows users their familiar local format (builds trust).
        - +61412345678 → 0412345678 (Australian sees local format)
        - +14155551234 → 4155551234 (American sees local format)
        
        Args:
            international_value: Phone in international format (+61...)
            rule: ValidationRule with StripPrefix and DisplayFormat
            
        Returns:
            Phone in local display format
        """
        strip_prefix = getattr(rule, 'StripPrefix', False)
        
        if not strip_prefix:
            # Don't strip (e.g., UK already uses local format)
            return international_value
        
        # Strip international prefix based on pattern
        # Australian: +61... → 0...
        if international_value.startswith('+61'):
            return '0' + international_value[3:]  # +61412345678 → 0412345678
        
        # New Zealand: +64... → 0...
        if international_value.startswith('+64'):
            return '0' + international_value[3:]
        
        # USA/Canada: +1... → just the 10 digits
        if international_value.startswith('+1'):
            return international_value[2:]  # +14155551234 → 4155551234
        
        # UK: +44... → 0...
        if international_value.startswith('+44'):
            return '0' + international_value[3:]
        
        # Fallback: return as-is
        return international_value
    
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
        
        # Story 1.20 Fix: Don't assume valid - return error if no rules defined
        return ValidationResult(
            is_valid=False,
            error_message=f"No validation rules configured for {rule_type}. Please contact support."
        )
    
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
