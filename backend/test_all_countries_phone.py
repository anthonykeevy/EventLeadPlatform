import requests
import json

tests = [
    (1, '0412345678', 'Australia Mobile'),
    (14, '0212345678', 'New Zealand Mobile'),
    (15, '4155551234', 'USA Phone'),
    (16, '07912345678', 'UK Mobile'),
    (17, '4165551234', 'Canada Phone')
]

print('=' * 80)
print('TESTING INTERNATIONAL PHONE VALIDATION')
print('=' * 80)

for country_id, value, desc in tests:
    print(f'\n{desc} (CountryID={country_id}):')
    print(f'  Input: {value}')
    
    r = requests.post(
        f'http://localhost:8000/api/countries/{country_id}/validate',
        json={'rule_type': 'phone', 'value': value}
    )
    
    result = r.json()
    print(f'  Valid: {result["is_valid"]}')
    if result['is_valid']:
        print(f'  Normalized (storage): {result["formatted_value"]}')
        print(f'  Display (user sees): {result["display_value"]}')
    else:
        print(f'  Error: {result["error_message"]}')

print('\n' + '=' * 80)

