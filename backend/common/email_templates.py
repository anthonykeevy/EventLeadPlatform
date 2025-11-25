import os

def get_approval_email_template(form_name, requestor_name, cost, approval_url=None, reject_url=None, view_url=None):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Approval Request</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background-color: #ffffff;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 1px solid #e5e7eb;
            padding-bottom: 20px;
        }}
        .logo {{
            font-size: 24px;
            font-weight: bold;
            color: #0d9488; /* Teal-600 */
            margin-bottom: 5px;
        }}
        .title {{
            font-size: 20px;
            color: #1f2937;
            margin: 0;
        }}
        .content {{
            margin-bottom: 30px;
        }}
        .info-box {{
            background-color: #f0fdfa; /* Teal-50 */
            border: 1px solid #ccfbf1; /* Teal-100 */
            border-radius: 6px;
            padding: 15px;
            margin: 20px 0;
        }}
        .info-item {{
            margin-bottom: 10px;
        }}
        .info-label {{
            font-weight: bold;
            color: #0f766e; /* Teal-700 */
        }}
        .actions {{
            text-align: center;
            margin-top: 30px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            margin: 0 10px;
            transition: background-color 0.3s;
        }}
        .btn-primary {{
            background-color: #0d9488;
            color: white;
        }}
        .btn-primary:hover {{
            background-color: #0f766e;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            font-size: 12px;
            color: #6b7280;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">EventLead</div>
            <h1 class="title">Approval Required</h1>
        </div>
        
        <div class="content">
            <p>Hello Admin,</p>
            
            <p><strong>{requestor_name}</strong> has submitted a form for approval.</p>
            
            <div class="info-box">
                <div class="info-item">
                    <span class="info-label">Form Name:</span> {form_name}
                </div>
                <div class="info-item">
                    <span class="info-label">Deployment Cost:</span> ${cost}
                </div>
            </div>
            
            <p>Please review this request to ensure it complies with company policies.</p>
            
            <div class="actions">
                {f'<a href="{view_url}" class="button btn-primary">View Form & Decide</a>' if view_url else ''}
            </div>
        </div>
        
        <div class="footer">
            <p>This is an automated notification from EventLead Platform.</p>
            <p>&copy; 2025 EventLead Platform. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

def get_decision_email_template(form_name, decision, reason=None, view_url=None):
    color = "#059669" if decision.lower() == "approved" else "#dc2626" # Green or Red
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form {decision}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background-color: #ffffff;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 1px solid #e5e7eb;
            padding-bottom: 20px;
        }}
        .logo {{
            font-size: 24px;
            font-weight: bold;
            color: #0d9488;
            margin-bottom: 5px;
        }}
        .status-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            background-color: {color};
            color: white;
            font-weight: bold;
            font-size: 16px;
            margin-top: 10px;
            text-transform: uppercase;
        }}
        .content {{
            margin-bottom: 30px;
        }}
        .reason-box {{
            background-color: #f9fafb;
            border-left: 4px solid {color};
            padding: 15px;
            margin: 20px 0;
            font-style: italic;
        }}
        .actions {{
            text-align: center;
            margin-top: 30px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            background-color: #0d9488;
            color: white;
            transition: background-color 0.3s;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            font-size: 12px;
            color: #6b7280;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">EventLead</div>
            <div class="status-badge">{decision}</div>
        </div>
        
        <div class="content">
            <p>Hello,</p>
            
            <p>Your form <strong>{form_name}</strong> has been <strong>{decision.lower()}</strong>.</p>
            
            {f'<div class="reason-box"><strong>Reason:</strong> {reason}</div>' if reason else ''}
            
            <p>You can now proceed with the next steps on the platform.</p>
            
            <div class="actions">
                {f'<a href="{view_url}" class="button">View Form</a>' if view_url else ''}
            </div>
        </div>
        
        <div class="footer">
            <p>This is an automated notification from EventLead Platform.</p>
            <p>&copy; 2025 EventLead Platform. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

