# Phone Validation Guide - Country-Specific Regex

**Author:** Dimitri 🔍 (Data Domain Architect)  
**Date:** October 13, 2025  
**Purpose:** Comprehensive phone number validation using Country table regex patterns

---

## Overview

The `Country` table stores regex patterns for **4 types of phone numbers** per country:

1. **Landline** - Fixed-line phones (e.g., +61 2 9215 7100)
2. **Mobile** - Cell phones (e.g., +61 400 123 456)
3. **Free Call** - Toll-free numbers (e.g., 1800 123 456, 1300 123 456)
4. **Special** - Short codes, premium numbers (e.g., 13 1234, 1900 XXX XXX)

---

## Australian Phone Number Formats

### 1. Landline (Fixed-Line)
**Format:** `+61 [2|3|7|8] XXXX XXXX`

**Area Codes:**
- **02** - New South Wales, Australian Capital Territory
- **03** - Victoria, Tasmania
- **07** - Queensland
- **08** - South Australia, Western Australia, Northern Territory

**Regex:** `^\+61\s?[2378]\s?\d{4}\s?\d{4}$`

**Valid Examples:**
- `+61 2 9215 7100` (ICC Sydney, NSW)
- `+61 3 9292 8000` (Melbourne Convention Centre, VIC)
- `+61 7 3308 3000` (Brisbane Convention Centre, QLD)
- `+61 8 8212 4099` (Adelaide Convention Centre, SA)

**Invalid Examples:**
- `+61 1 9215 7100` ❌ (area code must be 2, 3, 7, or 8)
- `+61 2 921 7100` ❌ (wrong digit count)
- `02 9215 7100` ❌ (missing country code +61)

---

### 2. Mobile (Cell Phone)
**Format:** `+61 4XX XXX XXX`

**Mobile Prefix:** Always starts with **04** (or +61 4 in international format)

**Regex:** `^\+61\s?4\d{2}\s?\d{3}\s?\d{3}$`

**Valid Examples:**
- `+61 400 123 456`
- `+61 412 345 678`
- `+61 499 999 999`

**Alternative Format (Local):**
- `0400 123 456` (without +61, starting with 0)
- Regex for local: `^0?4\d{2}\s?\d{3}\s?\d{3}$`

**Invalid Examples:**
- `+61 500 123 456` ❌ (must start with 4, not 5)
- `+61 4 123 456` ❌ (too short)

---

### 3. Free Call (Toll-Free / Local Rate)
**Format:** `1800 XXX XXX` or `1300 XXX XXX`

**Types:**
- **1800** - Toll-free (free from landlines and mobiles)
- **1300** - Local rate (charged at local call rate)

**Regex:** `^(1800|1300)\s?\d{3}\s?\d{3}$`

**Valid Examples:**
- `1800 123 456` (toll-free)
- `1300 123 456` (local rate)
- `1800123456` (no spaces - also valid)

**Invalid Examples:**
- `+61 1800 123 456` ❌ (no country code for 1800/1300)
- `1900 123 456` ❌ (1900 is premium, not free call)

---

### 4. Special (Short Codes / Premium)
**Format:** `13 XXXX` (6 digits) or `1900 XXX XXX` (premium)

**Types:**
- **13 XXXX** - 6-digit short codes (e.g., 13 1234 for Telstra)
- **1900 XXX XXX** - Premium rate numbers (expensive, $2-5/min)

**Regex:** `^(13\s?\d{4}|1900\s?\d{6})$`

**Valid Examples:**
- `13 1234` (short code)
- `13 2345` (6 digits total)
- `1900 123 456` (premium rate)

**Invalid Examples:**
- `13 123` ❌ (too short - must be 6 digits total)
- `14 1234` ❌ (must start with 13, not 14)

**Note:** Emergency numbers (000, 112) are NOT validated for safety reasons.

---

## Implementation Example (Python FastAPI)

### 1. Phone Validation Service

```python
# backend/modules/common/phone_validator.py
import re
from typing import Optional, Dict, Literal
from sqlalchemy.orm import Session
from backend.modules.countries.models import Country

PhoneType = Literal["landline", "mobile", "freecall", "special"]


class PhoneValidator:
    """
    Phone number validation using Country table regex patterns
    """
    
    def __init__(self, db: Session):
        self.db = db
        self._country_cache: Dict[str, Country] = {}
    
    def _get_country(self, country_code: str) -> Optional[Country]:
        """Get country from cache or database"""
        if country_code not in self._country_cache:
            country = self.db.query(Country).filter(
                Country.CountryCode == country_code,
                Country.IsDeleted == 0
            ).first()
            if country:
                self._country_cache[country_code] = country
        return self._country_cache.get(country_code)
    
    def validate(
        self, 
        phone: str, 
        country_code: str, 
        phone_type: Optional[PhoneType] = None
    ) -> Dict[str, any]:
        """
        Validate phone number against country regex patterns
        
        Args:
            phone: Phone number to validate (e.g., "+61 2 9215 7100")
            country_code: ISO country code (e.g., "AU")
            phone_type: Specific type to validate (optional - will try all if None)
            
        Returns:
            {
                "valid": True,
                "type": "landline",  # or "mobile", "freecall", "special"
                "formatted": "+61 2 9215 7100",
                "country": "AU"
            }
            
        Raises:
            ValueError: If country not found or phone invalid
        """
        # Get country
        country = self._get_country(country_code)
        if not country:
            raise ValueError(f"Country {country_code} not found or not supported")
        
        # Clean phone number (remove extra spaces, dashes)
        phone_clean = phone.strip()
        
        # If phone_type specified, validate against specific regex
        if phone_type:
            regex = self._get_regex(country, phone_type)
            if regex and re.match(regex, phone_clean):
                return {
                    "valid": True,
                    "type": phone_type,
                    "formatted": self._format_phone(phone_clean, country, phone_type),
                    "country": country_code
                }
            return {"valid": False, "error": f"Invalid {phone_type} format"}
        
        # Try all phone types
        for ptype in ["landline", "mobile", "freecall", "special"]:
            regex = self._get_regex(country, ptype)
            if regex and re.match(regex, phone_clean):
                return {
                    "valid": True,
                    "type": ptype,
                    "formatted": self._format_phone(phone_clean, country, ptype),
                    "country": country_code
                }
        
        return {"valid": False, "error": "Phone number does not match any valid format"}
    
    def _get_regex(self, country: Country, phone_type: PhoneType) -> Optional[str]:
        """Get regex pattern for phone type"""
        if phone_type == "landline":
            return country.PhoneLandlineRegex
        elif phone_type == "mobile":
            return country.PhoneMobileRegex
        elif phone_type == "freecall":
            return country.PhoneFreeCallRegex
        elif phone_type == "special":
            return country.PhoneSpecialRegex
        return None
    
    def _format_phone(self, phone: str, country: Country, phone_type: PhoneType) -> str:
        """
        Format phone number for display (add spaces, consistent format)
        """
        # Australian formatting examples
        if country.CountryCode == "AU":
            if phone_type == "landline":
                # +61 2 9215 7100 → ensure spaces
                phone = re.sub(r'^\+61\s?([2378])\s?(\d{4})\s?(\d{4})$', r'+61 \1 \2 \3', phone)
            elif phone_type == "mobile":
                # +61 400 123 456 → ensure spaces
                phone = re.sub(r'^\+61\s?(4\d{2})\s?(\d{3})\s?(\d{3})$', r'+61 \1 \2 \3', phone)
            elif phone_type == "freecall":
                # 1800 123 456 → ensure spaces
                phone = re.sub(r'^(1[38]00)\s?(\d{3})\s?(\d{3})$', r'\1 \2 \3', phone)
            elif phone_type == "special":
                # 13 1234 → ensure space
                phone = re.sub(r'^(13)\s?(\d{4})$', r'\1 \2', phone)
        
        return phone
    
    def get_format_hint(self, country_code: str) -> str:
        """
        Get format examples for UI (placeholder text)
        """
        country = self._get_country(country_code)
        if country and country.PhoneFormatExample:
            return country.PhoneFormatExample
        return "Enter phone number"


# Example usage
def example_usage():
    db = get_db()
    validator = PhoneValidator(db)
    
    # Validate landline
    result = validator.validate("+61 2 9215 7100", "AU", "landline")
    print(result)
    # Output: {"valid": True, "type": "landline", "formatted": "+61 2 9215 7100", "country": "AU"}
    
    # Validate mobile
    result = validator.validate("+61 400 123 456", "AU", "mobile")
    print(result)
    # Output: {"valid": True, "type": "mobile", "formatted": "+61 400 123 456", "country": "AU"}
    
    # Validate free call
    result = validator.validate("1800 123 456", "AU", "freecall")
    print(result)
    # Output: {"valid": True, "type": "freecall", "formatted": "1800 123 456", "country": "AU"}
    
    # Auto-detect type (no phone_type specified)
    result = validator.validate("+61 2 9215 7100", "AU")
    print(result)
    # Output: {"valid": True, "type": "landline", "formatted": "+61 2 9215 7100", "country": "AU"}
    
    # Invalid phone
    result = validator.validate("+61 1 9215 7100", "AU")
    print(result)
    # Output: {"valid": False, "error": "Phone number does not match any valid format"}
```

---

### 2. FastAPI Endpoint

```python
# backend/modules/companies/routes.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from backend.common.phone_validator import PhoneValidator, PhoneType

router = APIRouter(prefix="/api/companies", tags=["companies"])


class PhoneValidationRequest(BaseModel):
    phone: str = Field(..., description="Phone number to validate")
    country_code: str = Field(..., min_length=2, max_length=2, description="ISO country code")
    phone_type: Optional[PhoneType] = Field(None, description="Specific phone type (optional)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+61 2 9215 7100",
                "country_code": "AU",
                "phone_type": "landline"
            }
        }


@router.post("/validate-phone")
async def validate_phone(
    request: PhoneValidationRequest,
    db: Session = Depends(get_db)
):
    """
    Validate phone number against country-specific regex patterns
    
    **Phone Types:**
    - `landline` - Fixed-line phones (e.g., +61 2 9215 7100)
    - `mobile` - Cell phones (e.g., +61 400 123 456)
    - `freecall` - Toll-free numbers (e.g., 1800 123 456)
    - `special` - Short codes (e.g., 13 1234)
    
    **Auto-detection:** If `phone_type` not specified, tries all types
    """
    validator = PhoneValidator(db)
    
    try:
        result = validator.validate(
            request.phone,
            request.country_code.upper(),
            request.phone_type
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

### 3. Frontend Integration (React/TypeScript)

```typescript
// src/services/phoneValidator.ts
import { api } from './api';

export type PhoneType = 'landline' | 'mobile' | 'freecall' | 'special';

export interface PhoneValidationResult {
  valid: boolean;
  type?: PhoneType;
  formatted?: string;
  country?: string;
  error?: string;
}

export class PhoneValidator {
  /**
   * Validate phone number via backend API
   */
  async validate(
    phone: string,
    countryCode: string,
    phoneType?: PhoneType
  ): Promise<PhoneValidationResult> {
    try {
      const response = await api.post<PhoneValidationResult>('/companies/validate-phone', {
        phone,
        country_code: countryCode,
        phone_type: phoneType
      });
      return response.data;
    } catch (error: any) {
      return { valid: false, error: error.response?.data?.detail || 'Validation failed' };
    }
  }
  
  /**
   * Format phone number as user types (Australian format)
   */
  formatAsYouType(value: string, phoneType: PhoneType): string {
    // Remove non-digits (except + for international)
    let cleaned = value.replace(/[^\d+]/g, '');
    
    // Australian landline: +61 2 9215 7100
    if (phoneType === 'landline') {
      if (cleaned.startsWith('+61')) {
        cleaned = cleaned.replace(/^\+61(\d)(\d{4})(\d{4})/, '+61 $1 $2 $3');
      }
    }
    
    // Australian mobile: +61 400 123 456
    else if (phoneType === 'mobile') {
      if (cleaned.startsWith('+61')) {
        cleaned = cleaned.replace(/^\+61(4\d{2})(\d{3})(\d{3})/, '+61 $1 $2 $3');
      } else if (cleaned.startsWith('04')) {
        cleaned = cleaned.replace(/^(04\d{2})(\d{3})(\d{3})/, '$1 $2 $3');
      }
    }
    
    // Free call: 1800 123 456
    else if (phoneType === 'freecall') {
      cleaned = cleaned.replace(/^(1[38]00)(\d{3})(\d{3})/, '$1 $2 $3');
    }
    
    // Special: 13 1234
    else if (phoneType === 'special') {
      if (cleaned.startsWith('13')) {
        cleaned = cleaned.replace(/^(13)(\d{4})/, '$1 $2');
      }
    }
    
    return cleaned;
  }
}

export const phoneValidator = new PhoneValidator();
```

```tsx
// src/components/CompanyOnboarding/PhoneInput.tsx
import React, { useState } from 'react';
import { phoneValidator, PhoneType } from '../../services/phoneValidator';

interface PhoneInputProps {
  label: string;
  phoneType: PhoneType;
  countryCode: string;
  value: string;
  onChange: (value: string) => void;
}

export const PhoneInput: React.FC<PhoneInputProps> = ({
  label,
  phoneType,
  countryCode,
  value,
  onChange
}) => {
  const [validating, setValidating] = useState(false);
  const [validation, setValidation] = useState<any>(null);
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const formatted = phoneValidator.formatAsYouType(e.target.value, phoneType);
    onChange(formatted);
  };
  
  const handleBlur = async () => {
    if (!value) return;
    
    setValidating(true);
    const result = await phoneValidator.validate(value, countryCode, phoneType);
    setValidation(result);
    setValidating(false);
    
    // If valid, update to formatted version
    if (result.valid && result.formatted) {
      onChange(result.formatted);
    }
  };
  
  return (
    <div className="form-group">
      <label>{label}</label>
      <input
        type="tel"
        value={value}
        onChange={handleChange}
        onBlur={handleBlur}
        placeholder={getPlaceholder(phoneType)}
        className={validation?.valid === false ? 'error' : ''}
      />
      
      {validating && <small className="text-muted">Validating...</small>}
      
      {validation?.valid === true && (
        <small className="text-success">
          ✓ Valid {validation.type}
        </small>
      )}
      
      {validation?.valid === false && (
        <small className="text-error">
          ✗ {validation.error}
        </small>
      )}
    </div>
  );
};

function getPlaceholder(phoneType: PhoneType): string {
  switch (phoneType) {
    case 'landline': return '+61 2 9215 7100';
    case 'mobile': return '+61 400 123 456';
    case 'freecall': return '1800 123 456';
    case 'special': return '13 1234';
  }
}
```

---

## Testing Strategies

### Unit Tests (pytest)

```python
# tests/test_phone_validator.py
import pytest
from backend.common.phone_validator import PhoneValidator

@pytest.fixture
def validator(db_session):
    return PhoneValidator(db_session)


def test_validate_landline_valid(validator):
    """Test valid Australian landline"""
    result = validator.validate("+61 2 9215 7100", "AU", "landline")
    assert result["valid"] is True
    assert result["type"] == "landline"
    assert result["formatted"] == "+61 2 9215 7100"


def test_validate_mobile_valid(validator):
    """Test valid Australian mobile"""
    result = validator.validate("+61 400 123 456", "AU", "mobile")
    assert result["valid"] is True
    assert result["type"] == "mobile"


def test_validate_freecall_valid(validator):
    """Test valid Australian toll-free"""
    result = validator.validate("1800 123 456", "AU", "freecall")
    assert result["valid"] is True
    assert result["type"] == "freecall"


def test_validate_special_valid(validator):
    """Test valid Australian 6-digit short code"""
    result = validator.validate("13 1234", "AU", "special")
    assert result["valid"] is True
    assert result["type"] == "special"


def test_validate_landline_invalid_area_code(validator):
    """Test invalid area code (1 instead of 2/3/7/8)"""
    result = validator.validate("+61 1 9215 7100", "AU", "landline")
    assert result["valid"] is False


def test_validate_auto_detect(validator):
    """Test auto-detection (no phone_type specified)"""
    result = validator.validate("+61 2 9215 7100", "AU")
    assert result["valid"] is True
    assert result["type"] == "landline"
```

---

## Database Query Examples

### Get Country Phone Patterns:

```sql
-- Get all phone patterns for Australia
SELECT 
    CountryCode,
    CountryName,
    PhoneCountryCode,
    PhoneLandlineRegex,
    PhoneMobileRegex,
    PhoneFreeCallRegex,
    PhoneSpecialRegex,
    PhoneFormatExample
FROM Country
WHERE CountryCode = 'AU'
  AND IsDeleted = 0;
```

---

## Future Enhancements

### Additional Countries (Phase 2+):

**United States:**
- Landline: `^\+1\s?\([2-9]\d{2}\)\s?\d{3}-?\d{4}$`
- Mobile: Same as landline (no distinction)
- Toll-free: `^\+1\s?(800|888|877|866|855|844|833)\s?\d{3}\s?\d{4}$`

**United Kingdom:**
- Landline: `^\+44\s?[1-9]\d{8,9}$`
- Mobile: `^\+44\s?7\d{9}$`
- Toll-free: `^\+44\s?(800|808)\s?\d{6,7}$`

**New Zealand:**
- Landline: `^\+64\s?[3-9]\s?\d{3}\s?\d{4}$`
- Mobile: `^\+64\s?2\d{1}\s?\d{3}\s?\d{4}$`
- Toll-free: `^0800\s?\d{3}\s?\d{3}$`

---

## Summary

✅ **Country table stores 4 regex patterns** per country  
✅ **Australian patterns fully defined** (landline, mobile, free call, special)  
✅ **PhoneValidator service** validates against country-specific rules  
✅ **Auto-detection** if phone type not specified  
✅ **Format-as-you-type** for better UX  
✅ **Backend validation** prevents invalid data  
✅ **International-ready** (add new countries by inserting Country rows)

---

*Dimitri - Data Domain Architect* 🔍  
*"Phone validation: regex patterns done right"*



