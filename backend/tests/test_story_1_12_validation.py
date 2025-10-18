"""
Tests for Story 1.12: International Foundation & Country-Specific Validation
Comprehensive unit and integration tests for validation engine and API.
"""
import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from modules.countries.validation_engine import ValidationEngine, ValidationResult
from modules.countries.schemas import ValidationRequest, MultiFieldValidationRequest
from models.config.validation_rule import ValidationRule
from models.ref.rule_type import RuleType
from models.ref.country import Country


class TestValidationEngine:
    """Unit tests for ValidationEngine service"""
    
    def test_validate_field_valid_input(self, db_session: Session):
        """Test validation with valid input"""
        # Create mock validation rule
        mock_rule = Mock(spec=ValidationRule)
        mock_rule.RuleKey = 'PHONE_MOBILE_FORMAT'
        mock_rule.ValidationPattern = r'^\+61[4-5][0-9]{8}$'
        mock_rule.ValidationMessage = 'Mobile phone must be +61 followed by 4 or 5 and 8 digits'
        mock_rule.MinLength = 12
        mock_rule.MaxLength = 13
        mock_rule.ExampleValue = '+61412345678'
        mock_rule.IsActive = True
        mock_rule.Priority = 10
        mock_rule.Description = 'Australian mobile phone format validation'
        
        engine = ValidationEngine(db_session)
        
        # Mock get_validation_rules to return our test rule
        engine.get_validation_rules = Mock(return_value=[mock_rule])
        
        # Test valid phone number
        result = engine.validate_field(1, 'phone', '+61412345678')
        
        assert result.is_valid is True
        assert result.formatted_value == '+61412345678'
        assert result.matched_rule == 'PHONE_MOBILE_FORMAT'
    
    def test_validate_field_invalid_input(self, db_session: Session):
        """Test validation with invalid input"""
        mock_rule = Mock(spec=ValidationRule)
        mock_rule.RuleKey = 'PHONE_MOBILE_FORMAT'
        mock_rule.ValidationPattern = r'^\+61[4-5][0-9]{8}$'
        mock_rule.ValidationMessage = 'Mobile phone must be +61 followed by 4 or 5 and 8 digits'
        mock_rule.MinLength = 12
        mock_rule.MaxLength = 13
        mock_rule.ExampleValue = '+61412345678'
        mock_rule.IsActive = True
        mock_rule.Priority = 10
        
        engine = ValidationEngine(db_session)
        engine.get_validation_rules = Mock(return_value=[mock_rule])
        
        # Test invalid phone number
        result = engine.validate_field(1, 'phone', '123456789')
        
        assert result.is_valid is False
        assert 'Mobile phone must be +61' in result.error_message
        assert '+61412345678' in result.error_message  # Example included
    
    def test_validate_australian_abn_valid_checksum(self, db_session: Session):
        """Test ABN validation with valid checksum"""
        engine = ValidationEngine(db_session)
        
        # Test with known valid ABN: 53004085616
        result = engine._validate_australian_abn('53004085616')
        
        assert result.is_valid is True
        assert result.formatted_value == '53 004 085 616'
        assert result.matched_rule == 'ABN_CHECKSUM'
    
    def test_validate_australian_abn_invalid_checksum(self, db_session: Session):
        """Test ABN validation with invalid checksum"""
        engine = ValidationEngine(db_session)
        
        # Test with invalid ABN
        result = engine._validate_australian_abn('12345678901')
        
        assert result.is_valid is False
        assert 'checksum is invalid' in result.error_message
    
    def test_validate_australian_abn_wrong_length(self, db_session: Session):
        """Test ABN validation with wrong length"""
        engine = ValidationEngine(db_session)
        
        # Test with wrong length
        result = engine._validate_australian_abn('1234567890')
        
        assert result.is_valid is False
        assert 'must be 11 digits' in result.error_message
    
    def test_validate_australian_acn(self, db_session: Session):
        """Test ACN validation and formatting"""
        engine = ValidationEngine(db_session)
        
        # Test valid ACN
        result = engine._validate_australian_acn('123456789')
        
        assert result.is_valid is True
        assert result.formatted_value == '123 456 789'
        assert result.matched_rule == 'ACN_FORMAT'
    
    def test_validate_multiple_fields(self, db_session: Session):
        """Test multi-field validation"""
        engine = ValidationEngine(db_session)
        
        # Mock validation for multiple fields
        def mock_validate(country_id, rule_type, value):
            if rule_type == 'phone' and value == '+61412345678':
                return ValidationResult(is_valid=True, formatted_value='+61 412 345 678')
            elif rule_type == 'postal_code' and value == '2000':
                return ValidationResult(is_valid=True, formatted_value='2000')
            else:
                return ValidationResult(is_valid=False, error_message='Invalid format')
        
        engine.validate_field = Mock(side_effect=mock_validate)
        
        fields = {
            'phone': '+61412345678',
            'postal_code': '2000'
        }
        
        results = engine.validate_multiple_fields(1, fields)
        
        assert len(results) == 2
        assert results['phone'].is_valid is True
        assert results['postal_code'].is_valid is True
    
    def test_cache_functionality(self, db_session: Session):
        """Test validation rule caching"""
        engine = ValidationEngine(db_session)
        
        # Mock database query
        mock_rules = [Mock(spec=ValidationRule)]
        with patch.object(engine.db, 'query') as mock_query:
            mock_query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = mock_rules
            
            # First call should query database
            rules1 = engine.get_validation_rules(1, 'phone')
            
            # Second call should use cache
            rules2 = engine.get_validation_rules(1, 'phone')
            
            assert rules1 == rules2
            # Database should only be queried once due to caching
            mock_query.assert_called_once()


class TestValidationAPI:
    """Integration tests for validation API endpoints"""
    
    def test_validate_endpoint_valid_phone(self, client, db_session):
        """Test validation endpoint with valid phone number"""
        # Create test validation rule
        test_rule = ValidationRule(
            ValidationRuleID=1,
            RuleKey='PHONE_MOBILE_FORMAT',
            RuleTypeID=1,
            CountryID=1,
            ValidationPattern=r'^\+61[4-5][0-9]{8}$',
            ValidationMessage='Mobile phone must be +61 followed by 4 or 5 and 8 digits',
            Description='Australian mobile phone format validation',
            MinLength=12,
            MaxLength=13,
            ExampleValue='+61412345678',
            IsActive=True,
            Priority=10
        )
        
        # Mock the database query
        with patch('modules.countries.validation_engine.ValidationEngine.get_validation_rules') as mock_get_rules:
            mock_get_rules.return_value = [test_rule]
            
            response = client.post(
                "/api/countries/1/validate",
                json={
                    "rule_type": "phone",
                    "value": "+61412345678"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["is_valid"] is True
            assert data["formatted_value"] == "+61412345678"
    
    def test_validate_endpoint_invalid_phone(self, client, db_session):
        """Test validation endpoint with invalid phone number"""
        test_rule = ValidationRule(
            ValidationRuleID=1,
            RuleKey='PHONE_MOBILE_FORMAT',
            RuleTypeID=1,
            CountryID=1,
            ValidationPattern=r'^\+61[4-5][0-9]{8}$',
            ValidationMessage='Mobile phone must be +61 followed by 4 or 5 and 8 digits',
            Description='Australian mobile phone format validation',
            MinLength=12,
            MaxLength=13,
            ExampleValue='+61412345678',
            IsActive=True,
            Priority=10
        )
        
        with patch('modules.countries.validation_engine.ValidationEngine.get_validation_rules') as mock_get_rules:
            mock_get_rules.return_value = [test_rule]
            
            response = client.post(
                "/api/countries/1/validate",
                json={
                    "rule_type": "phone",
                    "value": "123456789"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["is_valid"] is False
            assert "Mobile phone must be +61" in data["error_message"]
    
    def test_validate_abn_endpoint(self, client, db_session):
        """Test ABN-specific validation endpoint"""
        with patch('modules.countries.validation_engine.ValidationEngine.validate_field') as mock_validate:
            mock_validate.return_value = ValidationResult(
                is_valid=True,
                formatted_value='53 004 085 616',
                matched_rule='ABN_CHECKSUM'
            )
            
            response = client.post(
                "/api/countries/1/validate-abn",
                json={
                    "rule_type": "tax_id",
                    "value": "53004085616"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["is_valid"] is True
            assert data["formatted_value"] == '53 004 085 616'
    
    def test_multi_field_validation_endpoint(self, client, db_session):
        """Test multi-field validation endpoint"""
        def mock_validate_multiple(country_id, fields):
            return {
                'phone': ValidationResult(is_valid=True, formatted_value='+61 412 345 678'),
                'postal_code': ValidationResult(is_valid=True, formatted_value='2000'),
                'tax_id': ValidationResult(is_valid=False, error_message='Invalid ABN checksum')
            }
        
        with patch('modules.countries.validation_engine.ValidationEngine.validate_multiple_fields') as mock_validate:
            mock_validate.side_effect = mock_validate_multiple
            
            response = client.post(
                "/api/countries/1/validate-multiple",
                json={
                    "fields": {
                        "phone": "+61412345678",
                        "postal_code": "2000",
                        "tax_id": "12345678901"
                    }
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["all_valid"] is False  # Because tax_id is invalid
            assert data["results"]["phone"]["is_valid"] is True
            assert data["results"]["postal_code"]["is_valid"] is True
            assert data["results"]["tax_id"]["is_valid"] is False
    
    def test_validation_rules_endpoint(self, client, db_session):
        """Test validation rules retrieval endpoint"""
        test_rule = ValidationRule(
            ValidationRuleID=1,
            RuleKey='PHONE_MOBILE_FORMAT',
            RuleTypeID=1,
            CountryID=1,
            ValidationPattern=r'^\+61[4-5][0-9]{8}$',
            ValidationMessage='Mobile phone must be +61 followed by 4 or 5 and 8 digits',
            Description='Australian mobile phone format validation',
            MinLength=12,
            MaxLength=13,
            ExampleValue='+61412345678',
            IsActive=True,
            Priority=10
        )
        
        with patch('modules.countries.validation_engine.ValidationEngine.get_validation_rules') as mock_get_rules:
            mock_get_rules.return_value = [test_rule]
            
            response = client.get("/api/countries/1/validation-rules/phone")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["rule_key"] == "PHONE_MOBILE_FORMAT"
            assert data[0]["validation_pattern"] == r'^\+61[4-5][0-9]{8}$'
            assert data[0]["example_value"] == "+61412345678"


class TestABNValidation:
    """Specific tests for ABN checksum algorithm"""
    
    def test_valid_abn_checksums(self, db_session):
        """Test known valid ABNs"""
        engine = ValidationEngine(db_session)
        
        # Test cases with known valid ABNs
        valid_abns = [
            '53004085616',  # Atlassian
            '51824753556',  # Google Australia
            '47001586760'   # Microsoft
        ]
        
        for abn in valid_abns:
            result = engine._validate_australian_abn(abn)
            assert result.is_valid is True, f"ABN {abn} should be valid"
            assert len(result.formatted_value.replace(' ', '')) == 11
    
    def test_invalid_abn_checksums(self, db_session):
        """Test invalid ABNs that fail checksum"""
        engine = ValidationEngine(db_session)
        
        invalid_abns = [
            '12345678901',  # Random digits
            '11111111111',  # All 1s
            '00000000000'   # All 0s
        ]
        
        for abn in invalid_abns:
            result = engine._validate_australian_abn(abn)
            assert result.is_valid is False, f"ABN {abn} should be invalid"
            assert 'checksum' in result.error_message.lower()


class TestPhoneNumberValidation:
    """Tests for international phone number validation"""
    
    @patch('modules.countries.validation_engine.phonenumbers')
    def test_phone_validation_with_library(self, mock_phonenumbers, db_session):
        """Test phone validation when phonenumbers library is available"""
        # Mock successful parsing
        mock_phone = Mock()
        mock_phonenumbers.parse.return_value = mock_phone
        mock_phonenumbers.is_valid_number.return_value = True
        mock_phonenumbers.format_number.return_value = '+61 412 345 678'
        mock_phonenumbers.PhoneNumberFormat.INTERNATIONAL = 1
        
        mock_rule = Mock(spec=ValidationRule)
        mock_rule.RuleKey = 'PHONE_MOBILE_FORMAT'
        mock_rule.ValidationPattern = r'^\+61[4-5][0-9]{8}$'
        mock_rule.ValidationMessage = 'Invalid mobile phone'
        mock_rule.ExampleValue = '+61412345678'
        
        engine = ValidationEngine(db_session)
        result = engine._validate_phone_number('+61412345678', mock_rule)
        
        mock_phonenumbers.parse.assert_called_once_with('+61412345678', 'AU')
        assert result.is_valid is True
    
    def test_phone_validation_without_library(self, db_session):
        """Test phone validation when phonenumbers library is not available"""
        with patch('modules.countries.validation_engine.phonenumbers', None):
            mock_rule = Mock(spec=ValidationRule)
            mock_rule.RuleKey = 'PHONE_MOBILE_FORMAT'
            mock_rule.ValidationPattern = r'^\+61[4-5][0-9]{8}$'
            mock_rule.ValidationMessage = 'Invalid mobile phone'
            mock_rule.ExampleValue = '+61412345678'
            
            engine = ValidationEngine(db_session)
            
            # Should fall back to regex validation
            result = engine._validate_phone_number('+61412345678', mock_rule)
            assert result.is_valid is True


class TestCachingBehavior:
    """Tests for validation rule caching"""
    
    def test_cache_hit_performance(self, db_session):
        """Test that caching improves performance"""
        engine = ValidationEngine(db_session)
        
        mock_rules = [Mock(spec=ValidationRule)]
        
        with patch.object(engine.db, 'query') as mock_query:
            mock_query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = mock_rules
            
            # First call - should hit database
            rules1 = engine.get_validation_rules(1, 'phone')
            
            # Second call - should use cache
            rules2 = engine.get_validation_rules(1, 'phone')
            
            assert rules1 == rules2
            # Database should only be queried once
            mock_query.assert_called_once()
    
    def test_cache_invalidation(self, db_session):
        """Test cache invalidation functionality"""
        engine = ValidationEngine(db_session)
        
        # Add something to cache
        engine._cache['test_key'] = 'test_value'
        assert 'test_key' in engine._cache
        
        # Invalidate cache
        engine.invalidate_cache()
        assert 'test_key' not in engine._cache


class TestEdgeCases:
    """Tests for edge cases and error handling"""
    
    def test_empty_value_validation(self, db_session):
        """Test validation with empty or None values"""
        engine = ValidationEngine(db_session)
        
        # Test empty string
        result = engine.validate_field(1, 'phone', '')
        assert result.is_valid is False
        assert 'required' in result.error_message.lower()
        
        # Test whitespace only
        result = engine.validate_field(1, 'phone', '   ')
        assert result.is_valid is False
        assert 'required' in result.error_message.lower()
    
    def test_no_validation_rules_found(self, db_session):
        """Test validation when no rules are defined for country/type"""
        engine = ValidationEngine(db_session)
        engine.get_validation_rules = Mock(return_value=[])
        
        # Should fall back to basic validation
        result = engine.validate_field(999, 'unknown_type', 'test_value')
        
        # Basic validation should accept non-empty values
        assert result.is_valid is True
    
    def test_invalid_regex_pattern_handling(self, db_session):
        """Test handling of invalid regex patterns"""
        engine = ValidationEngine(db_session)
        
        mock_rule = Mock(spec=ValidationRule)
        mock_rule.RuleKey = 'INVALID_REGEX'
        mock_rule.ValidationPattern = '[invalid regex('  # Invalid regex
        mock_rule.IsActive = True
        mock_rule.MinLength = None
        mock_rule.MaxLength = None
        
        # Should handle regex error gracefully
        result = engine._apply_rule_validation(mock_rule, 'test_value')
        assert result.is_valid is False


# Fixtures and test configuration
@pytest.fixture
def db_session():
    """Mock database session for testing"""
    return Mock(spec=Session)


@pytest.fixture  
def client():
    """Mock FastAPI test client"""
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app)
