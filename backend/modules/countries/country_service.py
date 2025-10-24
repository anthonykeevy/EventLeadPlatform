"""
Country Service - Story 1.20
Provides country information for frontend consumption
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models.ref.country import Country


def get_active_countries(db: Session) -> List[Dict[str, Any]]:
    """
    Get list of active countries with validation configuration.
    
    Returns country data formatted for frontend consumption including
    labels for postal codes, tax, states, etc.
    
    Story 1.20: Used by frontend to dynamically load country options.
    """
    countries = db.query(Country).filter(
        Country.IsActive == True,
        ~Country.IsDeleted
    ).order_by(Country.SortOrder).all()
    
    # Country-specific configuration
    country_config = {
        'AU': {
            'postal_label': 'Postcode',
            'postal_example': '2000',
            'state_label': 'State',
            'tax_id_label': 'ABN (Australian Business Number)',
            'tax_id_example': '53004085616',
            'tax_id_required': True,
            'has_company_search': True,
            'company_search_label': 'Search ABN/ACN'
        },
        'NZ': {
            'postal_label': 'Postcode',
            'postal_example': '1010',
            'state_label': 'Region',
            'tax_id_label': 'NZBN (NZ Business Number)',
            'tax_id_example': '9429031595513',
            'tax_id_required': False,
            'has_company_search': False,
            'company_search_label': None
        },
        'US': {
            'postal_label': 'ZIP Code',
            'postal_example': '94102',
            'state_label': 'State',
            'tax_id_label': 'EIN (Employer ID Number)',
            'tax_id_example': '12-3456789',
            'tax_id_required': False,
            'has_company_search': False,
            'company_search_label': None
        },
        'GB': {
            'postal_label': 'Postcode',
            'postal_example': 'SW1A 1AA',
            'state_label': 'County',
            'tax_id_label': 'VAT Number',
            'tax_id_example': 'GB123456789',
            'tax_id_required': False,
            'has_company_search': True,
            'company_search_label': 'Search Companies House'
        },
        'CA': {
            'postal_label': 'Postal Code',
            'postal_example': 'M5H 2N2',
            'state_label': 'Province',
            'tax_id_label': 'BN (Business Number)',
            'tax_id_example': '123456789RC0001',
            'tax_id_required': False,
            'has_company_search': False,
            'company_search_label': None
        }
    }
    
    result = []
    for country in countries:
        country_code = str(country.CountryCode) if country.CountryCode else ''
        config = country_config.get(country_code, {})
        
        result.append({
            'id': country.CountryID,
            'code': country.CountryCode,
            'name': country.CountryName,
            'phone_prefix': country.PhonePrefix,
            'currency_code': country.CurrencyCode,
            'currency_symbol': country.CurrencySymbol,
            'tax_name': country.TaxName,
            'tax_rate': float(country.TaxRate) if country.TaxRate else None,
            'postal_label': config.get('postal_label', 'Postal Code'),
            'postal_example': config.get('postal_example', ''),
            'state_label': config.get('state_label', 'State/Province'),
            'tax_id_label': config.get('tax_id_label', 'Tax ID'),
            'tax_id_example': config.get('tax_id_example', ''),
            'tax_id_required': config.get('tax_id_required', False),
            'has_company_search': config.get('has_company_search', False),
            'company_search_label': config.get('company_search_label')
        })
    
    return result

