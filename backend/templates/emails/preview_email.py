"""
Email Template Preview Script
Renders email templates with sample data for preview/testing
"""
import os
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Add parent directory to path to import email service if needed
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def preview_email_template(template_name: str, output_file: str = None):
    """
    Render an email template with sample data and save to HTML file.
    
    Args:
        template_name: Name of template (e.g., 'event_approved', 'event_rejected')
        output_file: Optional output file path (defaults to template_name_preview.html)
    """
    # Template directory
    template_dir = Path(__file__).parent
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    
    # Sample data for different templates
    sample_data = {
        'event_approved': {
            'event_name': 'Consumer Electronics Show 2025',
            'event_status': 'PUBLISHED',  # Try 'PUBLISHED', 'DRAFT', or 'CANCELLED'
            'comment': 'Great event! All details look professional.',
            'event_url': 'https://app.eventlead.com/dashboard/events/123',
            'guidelines_url': 'https://eventlead.com/policies/public-event-guidelines'
        },
        'event_rejected': {
            'event_name': 'Tech Innovation Summit 2025',
            'feedback': '''We appreciate your event submission. However, we need a few adjustments before we can approve it for public visibility:

1. Please add a more detailed description of the event
2. The event description contains some placeholder text that should be replaced
3. Please ensure all location details are complete

Once you've made these changes, you can resubmit the event for review. Thank you for your understanding!''',
            'event_edit_url': 'https://app.eventlead.com/dashboard/events/456/edit',
            'guidelines_url': 'https://eventlead.com/policies/public-event-guidelines'
        }
    }
    
    # Get template and render
    try:
        template = env.get_template(f"{template_name}.html")
        data = sample_data.get(template_name, {})
        html = template.render(**data)
        
        # Save to file
        if not output_file:
            output_file = f"{template_name}_preview.html"
        
        output_path = template_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[OK] Template rendered successfully!")
        print(f"Output saved to: {output_path}")
        print(f"Open in browser: file://{output_path.absolute()}")
        print(f"\nTip: Right-click the file in Cursor and select 'Open in Default Browser'")
        
        return output_path
    except Exception as e:
        print(f"[ERROR] Error rendering template: {e}")
        return None


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Preview email templates')
    parser.add_argument('template', nargs='?', default='event_approved',
                       help='Template name (e.g., event_approved, event_rejected)')
    parser.add_argument('-o', '--output', help='Output file path')
    
    args = parser.parse_args()
    
    preview_email_template(args.template, args.output)

