"""
Extract Form Definitions for WYSIWYG Comparison
Script to capture component properties from Form 41 (Template C) and Form 44 (Template D)
"""
import sys
import json
sys.path.insert(0, '.')

from common.database import SessionLocal
from sqlalchemy import text


def extract_component_properties(component: dict, depth: int = 0) -> dict:
    """Extract relevant properties from a component for comparison"""
    prefix = "  " * depth
    
    props = component.get('props', {})
    
    extracted = {
        'id': component.get('id'),
        'type': component.get('type'),
        'x': component.get('x'),
        'y': component.get('y'),
        'width': component.get('width'),
        'height': component.get('height'),
        'props': {
            # Layout properties
            'layout': props.get('layout'),
            'gap': props.get('gap'),
            'labelWidth': props.get('labelWidth'),
            
            # Typography - Label
            'labelFontFamily': props.get('labelFontFamily'),
            'labelFontSize': props.get('labelFontSize'),
            'labelFontWeight': props.get('labelFontWeight'),
            'labelColor': props.get('labelColor'),
            'labelAlignment': props.get('labelAlignment'),
            
            # Typography - Input
            'inputFontFamily': props.get('inputFontFamily'),
            'inputFontSize': props.get('inputFontSize'),
            'inputFontWeight': props.get('inputFontWeight'),
            'inputColor': props.get('inputColor'),
            
            # Typography - Help
            'helpFontFamily': props.get('helpFontFamily'),
            'helpFontSize': props.get('helpFontSize'),
            'helpFontWeight': props.get('helpFontWeight'),
            'helpColor': props.get('helpColor'),
            
            # Border properties
            'borderWidth': props.get('borderWidth'),
            'borderColor': props.get('borderColor'),
            'borderRadius': props.get('borderRadius'),
            'inputBorderWidth': props.get('inputBorderWidth'),
            'inputBorderColor': props.get('inputBorderColor'),
            'inputBorderRadius': props.get('inputBorderRadius'),
            
            # Background
            'backgroundColor': props.get('backgroundColor'),
            'inputBackgroundColor': props.get('inputBackgroundColor'),
            
            # Content
            'label': props.get('label'),
            'placeholder': props.get('placeholder'),
            'helpText': props.get('helpText'),
            
            # Validation
            'required': props.get('required'),
            'validation': props.get('validation'),
            
            # Object Layout
            'objectLayout': props.get('objectLayout'),
        }
    }
    
    # Remove None values for cleaner output
    extracted['props'] = {k: v for k, v in extracted['props'].items() if v is not None}
    
    # Handle children recursively
    if component.get('children'):
        extracted['children'] = [
            extract_component_properties(child, depth + 1) 
            for child in component['children']
        ]
    
    return extracted


def get_form_definition(db, form_id: int) -> dict:
    """Get form definition from database"""
    # Get the latest version for the form (not filtering by IsActive since drafts may not be active)
    result = db.execute(text('''
        SELECT fv.DefinitionJSON, f.FormName 
        FROM dbo.FormVersion fv
        JOIN dbo.Form f ON fv.FormID = f.FormID
        WHERE fv.FormID = :form_id
        ORDER BY fv.VersionNumber DESC
    '''), {'form_id': form_id}).fetchone()
    
    if not result:
        return None
    
    defn = json.loads(result[0]) if isinstance(result[0], str) else result[0]
    return {
        'formName': result[1],
        'definition': defn
    }


def main():
    db = SessionLocal()
    try:
        # Extract Form 41 (Template C)
        print("=" * 80)
        print("FORM 41 (Template C) - Component Properties")
        print("=" * 80)
        
        form41 = get_form_definition(db, 41)
        if form41:
            print(f"Form Name: {form41['formName']}")
            defn = form41['definition']
            print(f"Schema Version: {defn.get('schemaVersion')}")
            print(f"Global Styles: {json.dumps(defn.get('globalStyles'), indent=2) if defn.get('globalStyles') else 'None'}")
            print(f"\nCanvas Settings: {json.dumps(defn.get('canvasSettings'), indent=2) if defn.get('canvasSettings') else 'None'}")
            print(f"\nTheme: {json.dumps(defn.get('theme'), indent=2) if defn.get('theme') else 'None'}")
            
            print("\n--- COMPONENTS ---")
            all_components = []
            for page in defn.get('pages', []):
                print(f"\nPage: {page.get('id')}")
                for comp in page.get('components', []):
                    extracted = extract_component_properties(comp)
                    all_components.append(extracted)
                    print(f"\n  Component: {comp.get('type')} (ID: {comp.get('id')})")
                    print(f"    Position: x={comp.get('x')}, y={comp.get('y')}")
                    print(f"    Size: width={comp.get('width')}, height={comp.get('height')}")
                    print(f"    Props: {json.dumps(extracted['props'], indent=6)}")
            
            # Save full extraction
            with open('form41_components.json', 'w') as f:
                json.dump({
                    'formId': 41,
                    'formName': form41['formName'],
                    'globalStyles': defn.get('globalStyles'),
                    'canvasSettings': defn.get('canvasSettings'),
                    'theme': defn.get('theme'),
                    'components': all_components
                }, f, indent=2)
            print(f"\n[Saved to form41_components.json]")
        else:
            print("Form 41 not found")
        
        # Extract Form 44 (Template D)
        print("\n" + "=" * 80)
        print("FORM 44 (Template D) - Component Properties")
        print("=" * 80)
        
        form44 = get_form_definition(db, 44)
        if form44:
            print(f"Form Name: {form44['formName']}")
            defn = form44['definition']
            print(f"Schema Version: {defn.get('schemaVersion')}")
            print(f"Global Styles: {json.dumps(defn.get('globalStyles'), indent=2) if defn.get('globalStyles') else 'None'}")
            print(f"\nCanvas Settings: {json.dumps(defn.get('canvasSettings'), indent=2) if defn.get('canvasSettings') else 'None'}")
            print(f"\nTheme: {json.dumps(defn.get('theme'), indent=2) if defn.get('theme') else 'None'}")
            
            print("\n--- COMPONENTS ---")
            all_components = []
            for page in defn.get('pages', []):
                print(f"\nPage: {page.get('id')}")
                for comp in page.get('components', []):
                    extracted = extract_component_properties(comp)
                    all_components.append(extracted)
                    print(f"\n  Component: {comp.get('type')} (ID: {comp.get('id')})")
                    print(f"    Position: x={comp.get('x')}, y={comp.get('y')}")
                    print(f"    Size: width={comp.get('width')}, height={comp.get('height')}")
                    print(f"    Props: {json.dumps(extracted['props'], indent=6)}")
            
            # Save full extraction
            with open('form44_components.json', 'w') as f:
                json.dump({
                    'formId': 44,
                    'formName': form44['formName'],
                    'globalStyles': defn.get('globalStyles'),
                    'canvasSettings': defn.get('canvasSettings'),
                    'theme': defn.get('theme'),
                    'components': all_components
                }, f, indent=2)
            print(f"\n[Saved to form44_components.json]")
        else:
            print("Form 44 not found")
            
    finally:
        db.close()


if __name__ == "__main__":
    main()
