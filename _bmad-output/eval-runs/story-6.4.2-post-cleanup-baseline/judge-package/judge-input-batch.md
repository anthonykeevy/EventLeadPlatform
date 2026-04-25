# Form AI Judge Input Batch

Run ID: `story-6.4.2-post-cleanup-baseline`
Benchmark set: `prompts-v1.0`
Rubric version: `rubric_v1`

Use `rubric_v1.md` and return JSON matching `judge-output-template.json`.
Judge only the anonymised package content below.

## Row 1: `p-01-event-registration-conference__r01`

- Prompt ID: `p-01-event-registration-conference`
- Repetition: `1`
- Variant: `post-642-capability-cleanup`
- EvalRunID: `13`
- GenerationRunID: `107`
- Definition source: `dbo.GenerationArtifact`

### Prompt

Create a conference event registration form for a technology summit. Collect attendee contact details, organisation, role, session interests, t-shirt size, dietary needs, accessibility requests, and consent to event terms and marketing updates. Include a placeholder for payment acknowledgement but do not process payments.

### Prompt Metadata

```json
{
  "pii_adjacent": true,
  "source_type": "conference event registration",
  "tricky_edges": [
    "multi-consent",
    "payment-placeholder",
    "t-shirt-size"
  ]
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 65572,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 2104,
    "width": 960
  },
  "formId": "tech-summit-registration",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Please complete your details below to register for the Technology Summit. We will use this information to send your confirmation, manage workshop allocations, and arrange any special requirements.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Given name",
            "placeholder": "e.g. Priya",
            "required": true,
            "tabOrder": 2,
            "validation": {
              "required": true
            },
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 384,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Surname",
            "placeholder": "e.g. Smith",
            "required": true,
            "tabOrder": 3,
            "validation": {
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Include country code +61 if sending from overseas. We'll only use this for event updates and emergency contact.",
            "label": "Mobile",
            "placeholder": "04xx xxx xxx",
            "required": false,
            "tabOrder": 4,
            "validation": {
              "phone": true,
              "required": false
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "email-5",
          "position": {
            "x": 384,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Confirmation and tickets will be sent to this email address.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "required": true,
            "tabOrder": 5,
            "validation": {
              "email": true,
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Organisation name as you would like it to appear on your name badge.",
            "label": "Organisation",
            "placeholder": "e.g. Acme Solutions",
            "required": true,
            "tabOrder": 6,
            "validation": {
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "text-7",
          "position": {
            "x": 384,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Role / Job title",
            "placeholder": "e.g. Senior Engineer, Product Manager",
            "required": false,
            "tabOrder": 7,
            "validation": {
              "required": false
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Tick all sessions or tracks you're interested in \u2014 we'll use this to recommend a personalised schedule.",
            "label": "Session interests (tick any that apply)",
            "options": [
              {
                "label": "AI & Machine Learning",
                "value": "ai_ml"
              },
              {
                "label": "Cloud & Infrastructure",
                "value": "cloud_infra"
              },
              {
                "label": "Cybersecurity",
                "value": "cybersecurity"
              },
              {
                "label": "Data & Analytics",
                "value": "data_analytics"
              },
              {
                "label": "Developer Tools & DevOps",
                "value": "devops"
              },
              {
                "label": "Product Management & Design",
                "value": "product_design"
              },
              {
                "label": "Startups & Venture",
                "value": "startups"
              },
              {
                "label": "Workshops (half-day)",
                "value": "workshops"
              }
            ],
            "required": false,
            "tabOrder": 8,
            "validation": {
              "required": false
            },
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "dropdown-9",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 110,
            "helpText": "Select the t-shirt size for conference merchandise. We will order based on this selection.",
            "label": "T-shirt size",
            "options": [
              {
                "label": "XS",
                "value": "xs"
              },
              {
                "label": "S",
                "value": "s"
              },
              {
                "label": "M",
                "value": "m"
              },
              {
                "label": "L",
                "value": "l"
              },
              {
                "label": "XL",
                "value": "xl"
              },
              {
                "label": "XXL",
                "value": "xxl"
              },
              {
                "label": "Prefer not to say",
                "value": "prefer_not_say"
              }
            ],
            "placeholder": "Select your size",
            "required": true,
            "tabOrder": 9,
            "validation": {
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "Select any dietary needs to help us plan catering.",
            "label": "Dietary requirements",
            "options": [
              {
                "label": "Vegetarian",
                "value": "vegetarian"
              },
              {
                "label": "Vegan",
                "value": "vegan"
              },
              {
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Halal",
                "value": "halal"
              },
              {
                "label": "Kosher",
                "value": "kosher"
              },
              {
                "label": "Dairy-free",
                "value": "dairy_free"
              },
              {
                "label": "Nut-free",
                "value": "nut_free"
              },
              {
                "label": "Shellfish-free",
                "value": "shellfish_free"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "required": false,
            "tabOrder": 10,
            "validation": {
              "required": false
            },
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 200,
            "helpText": "If you selected 'Other' above, please provide details here.",
            "label": "If Other, please specify dietary needs",
            "placeholder": "Please describe any other dietary requirements",
            "required": false,
            "tabOrder": 11,
            "validation": {
              "maxLength": 500,
              "required": false
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "textarea-12",
          "position": {
            "x": 40,
            "y": 1224
          },
          "props": {
            "height": 200,
            "helpText": "Examples: mobility access, hearing loop, dietary communication needs, quiet room request. We will contact you to discuss arrangements where needed.",
            "label": "Accessibility or assistance requests",
            "placeholder": "Please let us know if you need any accessibility support or adjustments",
            "required": false,
            "tabOrder": 12,
            "validation": {
              "maxLength": 1000,
              "required": false
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-13",
          "position": {
            "x": 40,
            "y": 1528
          },
          "props": {
            "height": 120,
            "helpText": "This form does not process payments. By ticking this box you acknowledge that any registration fee will be collected separately (invoice or external payment page).",
            "label": "Payment acknowledgement",
            "options": [
              {
                "label": "I acknowledge that payment will be handled separately and this form does not process payments",
                "value": "ack_payment"
              }
            ],
            "required": true,
            "tabOrder": 13,
            "validation": {
              "required": true
            },
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1672
          },
          "props": {
            "height": 120,
            "helpText": "Please read the terms before agreeing. The full terms are available via the link.",
            "label": "I agree to the technology summit terms and conditions.",
            "required": true,
            "tabOrder": 14,
            "validation": {
              "required": true
            },
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "terms-15",
          "position": {
            "x": 40,
            "y": 1816
          },
          "props": {
            "height": 120,
            "helpText": "You can opt out at any time. We will use this consent to send you promotional emails and updates.",
            "label": "I agree to receive marketing communications about this event and future events (optional).",
            "required": false,
            "tabOrder": 15,
            "validation": {
              "required": false
            },
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-16",
          "position": {
            "x": 40,
            "y": 1960
          },
          "props": {
            "height": 72,
            "label": "Register",
            "tabOrder": 16,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Technology Summit \u2014 Registration"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 2: `p-02-lead-gen-saas-demo__r01`

- Prompt ID: `p-02-lead-gen-saas-demo`
- Repetition: `1`
- Variant: `post-642-capability-cleanup`
- EvalRunID: `14`
- GenerationRunID: `108`
- Definition source: `dbo.GenerationArtifact`

### Prompt

Create a short SaaS demo request lead form for an AI form builder, collecting business contact details, team size, use case, and preferred meeting time.

### Prompt Metadata

```json
{
  "pii_adjacent": true,
  "source_type": "SaaS demo lead-gen",
  "tricky_edges": [
    "minimal-context"
  ]
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 51922,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1662,
    "width": 960
  },
  "formId": "saas-demo-ai-form-builder",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Tell us a few details about your business and preferences and we'll get back to arrange a short demo tailored to your needs.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Given name",
            "placeholder": "e.g. Alex",
            "required": true,
            "tabOrder": 2,
            "validation": {
              "required": true
            },
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Surname",
            "placeholder": "e.g. Smith",
            "required": true,
            "tabOrder": 3,
            "validation": {
              "maxLength": 80,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Your company or team name",
            "label": "Organisation",
            "placeholder": "e.g. Acme Pty Ltd",
            "required": true,
            "tabOrder": 4,
            "validation": {
              "maxLength": 120,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll use this to send demo scheduling details",
            "label": "Business email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "required": true,
            "tabOrder": 5,
            "validation": {
              "email": true,
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-6",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Preferred contact number (optional). Include +61 if outside Australia.",
            "label": "Mobile",
            "placeholder": "04xx xxx xxx",
            "tabOrder": 6,
            "validation": {
              "phone": true
            },
            "width": "280px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "label": "Team size",
            "options": [
              {
                "label": "1\u201310",
                "value": "1-10"
              },
              {
                "label": "11\u201350",
                "value": "11-50"
              },
              {
                "label": "51\u2013200",
                "value": "51-200"
              },
              {
                "label": "201\u20131000",
                "value": "201-1000"
              },
              {
                "label": "1000+",
                "value": "1000+"
              }
            ],
            "placeholder": "Select team size",
            "required": true,
            "tabOrder": 7,
            "validation": {
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "dropdown-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Choose the closest match for how you plan to use the form builder",
            "label": "Primary use case",
            "options": [
              {
                "label": "Internal forms & workflows",
                "value": "internal_workflows"
              },
              {
                "label": "Customer-facing data capture",
                "value": "customer_capture"
              },
              {
                "label": "Research & surveys",
                "value": "research_surveys"
              },
              {
                "label": "Integration with CRM/BI",
                "value": "crm_bi_integration"
              },
              {
                "label": "Proof of concept / Pilot",
                "value": "pilot"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select a use case",
            "required": true,
            "tabOrder": 8,
            "validation": {
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 helps us tailor the demo",
            "label": "If Other, please describe briefly",
            "placeholder": "A short description of your use case (optional)",
            "tabOrder": 9,
            "validation": {
              "maxLength": 500
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "date-10",
          "position": {
            "x": 40,
            "y": 936
          },
          "props": {
            "height": 110,
            "helpText": "If you have a preferred date, select it here (optional)",
            "label": "Preferred meeting date",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 10,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "date"
        },
        {
          "id": "dropdown-11",
          "position": {
            "x": 424,
            "y": 936
          },
          "props": {
            "height": 110,
            "helpText": "All times local to your location",
            "label": "Preferred time of day",
            "options": [
              {
                "label": "Morning (9\u201311am)",
                "value": "morning"
              },
              {
                "label": "Midday (11am\u20132pm)",
                "value": "midday"
              },
              {
                "label": "Afternoon (2\u20135pm)",
                "value": "afternoon"
              },
              {
                "label": "Any",
                "value": "any"
              }
            ],
            "placeholder": "Select a time window",
            "required": true,
            "tabOrder": 11,
            "validation": {
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-12",
          "position": {
            "x": 40,
            "y": 1070
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 this helps us prepare a tailored demo",
            "label": "Any specific goals or priorities for the demo?",
            "placeholder": "E.g. focus on integrations, reporting, or custom branding",
            "tabOrder": 12,
            "validation": {
              "maxLength": 800
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-13",
          "position": {
            "x": 40,
            "y": 1374
          },
          "props": {
            "height": 120,
            "helpText": "Read our Privacy Policy before submitting. You can opt out of marketing emails at any time.",
            "label": "I agree to the Privacy Policy and to be contacted about this demo request.",
            "required": true,
            "tabOrder": 13,
            "validation": {
              "required": true
            },
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-14",
          "position": {
            "x": 40,
            "y": 1518
          },
          "props": {
            "height": 72,
            "label": "Request demo",
            "tabOrder": 14,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "AI Form Builder \u2014 Demo request"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 3: `p-03-survey-nps__r01`

- Prompt ID: `p-03-survey-nps`
- Repetition: `1`
- Variant: `post-642-capability-cleanup`
- EvalRunID: `15`
- GenerationRunID: `109`
- Definition source: `dbo.GenerationArtifact`

### Prompt

Create a customer NPS survey. Ask for a 0 to 10 recommendation rating, the main reason for the score, what could improve, whether the customer agrees to be contacted about feedback, and optional contact details.

### Prompt Metadata

```json
{
  "pii_adjacent": true,
  "source_type": "NPS survey",
  "tricky_edges": [
    "rating-component",
    "long-textarea"
  ]
}
```

### Category A Metrics

```json
{
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 98913,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1460,
    "width": 960
  },
  "formId": "nps-customer-survey",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "We value your feedback. This short survey takes less than 2 minutes and helps us improve our service.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "divider-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 20,
            "tabOrder": 2,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "rating-3",
          "position": {
            "x": 40,
            "y": 140
          },
          "props": {
            "height": 88,
            "helpText": "0 = Not at all likely, 10 = Extremely likely",
            "label": "How likely are you to recommend our organisation to a friend or colleague?",
            "required": true,
            "tabOrder": 3,
            "validation": {
              "max": 10.0,
              "min": 0.0,
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 88,
            "width": 360
          },
          "type": "rating"
        },
        {
          "id": "textarea-4",
          "position": {
            "x": 40,
            "y": 252
          },
          "props": {
            "height": 200,
            "helpText": "Please be as specific as you can \u2014 this helps us understand your experience.",
            "label": "What's the main reason for your score?",
            "placeholder": "Tell us the primary reason for your rating",
            "required": true,
            "tabOrder": 4,
            "validation": {
              "maxLength": 1000,
              "minLength": 10,
              "required": true
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "textarea-5",
          "position": {
            "x": 40,
            "y": 556
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 any ideas to help us serve you better.",
            "label": "What could we do to improve your experience?",
            "placeholder": "Suggestions or improvements you'd like to see",
            "required": false,
            "tabOrder": 5,
            "validation": {
              "maxLength": 1000,
              "required": false
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "divider-6",
          "position": {
            "x": 40,
            "y": 860
          },
          "props": {
            "height": 20,
            "tabOrder": 6,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "terms-7",
          "position": {
            "x": 40,
            "y": 904
          },
          "props": {
            "height": 120,
            "helpText": "Tick to allow us to follow up regarding your responses. You can opt out at any time.",
            "label": "I agree to be contacted about my feedback",
            "required": false,
            "tabOrder": 7,
            "validation": {
              "required": false
            },
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "first-name-8",
          "position": {
            "x": 40,
            "y": 1048
          },
          "props": {
            "height": 110,
            "helpText": "Provide if you are happy for us to contact you about your feedback.",
            "label": "Given name (optional)",
            "placeholder": "e.g. Kerry",
            "required": false,
            "tabOrder": 8,
            "validation": {
              "maxLength": 100,
              "required": false
            },
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-9",
          "position": {
            "x": 424,
            "y": 1048
          },
          "props": {
            "height": 110,
            "helpText": "Provide if you are happy for us to contact you about your feedback.",
            "label": "Surname (optional)",
            "placeholder": "e.g. Smith",
            "required": false,
            "tabOrder": 9,
            "validation": {
              "maxLength": 100,
              "required": false
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-10",
          "position": {
            "x": 40,
            "y": 1182
          },
          "props": {
            "height": 110,
            "helpText": "We'll only use this if you agreed to be contacted. Enter a preferred email address.",
            "label": "Email (optional)",
            "placeholder": "[SCRUBBED_EMAIL]",
            "required": false,
            "tabOrder": 10,
            "validation": {
              "email": true,
              "maxLength": 254,
              "required": false
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-11",
          "position": {
            "x": 424,
            "y": 1182
          },
          "props": {
            "height": 110,
            "helpText": "AU mobiles: 04xx xxx xxx. Include country code (+61 or +64) if outside Australia/New Zealand. We'll only call/SMS if you agreed to be contacted.",
            "label": "Mobile (optional)",
            "placeholder": "04xx xxx xxx",
            "required": false,
            "tabOrder": 11,
            "validation": {
              "phone": true,
              "required": false
            },
            "width": "280px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "submit-button-12",
          "position": {
            "x": 40,
            "y": 1316
          },
          "props": {
            "height": 72,
            "label": "Send feedback",
            "tabOrder": 12,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Customer NPS Survey"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 4: `p-04-waiver-gym-membership__r01`

- Prompt ID: `p-04-waiver-gym-membership`
- Repetition: `1`
- Variant: `post-642-capability-cleanup`
- EvalRunID: `16`
- GenerationRunID: `110`
- Definition source: `dbo.GenerationArtifact`

### Prompt

Create a gym membership waiver form. Collect member contact details, emergency contact, relevant health notes, membership type, acknowledgement of physical activity risks, and agreement to gym terms in a popup.

### Prompt Metadata

```json
{
  "pii_adjacent": true,
  "source_type": "gym waiver",
  "tricky_edges": [
    "mandatory-acknowledgement",
    "terms-popup"
  ]
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 21,
  "duration_ms": 65840,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 2134,
    "width": 960
  },
  "formId": "gym-waiver-form",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Please provide your contact details, emergency contact, and any relevant health information. You must agree to the acknowledgements and the gym waiver terms to complete registration.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Given name",
            "placeholder": "e.g. Jamie",
            "required": true,
            "tabOrder": 2,
            "validation": {
              "minLength": 1,
              "required": true
            },
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Surname",
            "placeholder": "e.g. Smith",
            "required": true,
            "tabOrder": 3,
            "validation": {
              "minLength": 1,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "date-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Use DD/MM/YYYY. You must be over the minimum age specified by your chosen membership.",
            "label": "Date of birth",
            "placeholder": "DD/MM/YYYY",
            "required": true,
            "tabOrder": 4,
            "validation": {
              "required": true
            },
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 220
          },
          "type": "date"
        },
        {
          "id": "email-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "We will send membership receipts and important updates to this address.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "required": true,
            "tabOrder": 5,
            "validation": {
              "email": true,
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-6",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide an Australian or New Zealand mobile number. Include country code if outside AU/NZ (+61 / +64).",
            "label": "Mobile",
            "placeholder": "04xx xxx xxx",
            "required": true,
            "tabOrder": 6,
            "validation": {
              "phone": true,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "address-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and Postcode. If you do not wish to provide an address, enter your suburb and Postcode only.",
            "label": "Address",
            "placeholder": "123 George Street, Sydney NSW 2000",
            "required": false,
            "tabOrder": 7,
            "validation": {
              "required": false
            },
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "divider-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 20,
            "tabOrder": 8,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "text-9",
          "position": {
            "x": 40,
            "y": 676
          },
          "props": {
            "height": 110,
            "helpText": "Person we should contact in an emergency.",
            "label": "Emergency contact - Full name",
            "placeholder": "Given name and Surname",
            "required": true,
            "tabOrder": 9,
            "validation": {
              "minLength": 1,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-10",
          "position": {
            "x": 424,
            "y": 676
          },
          "props": {
            "height": 110,
            "label": "Relationship to member",
            "placeholder": "e.g. Partner, Parent, Friend",
            "required": true,
            "tabOrder": 10,
            "validation": {
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "phone-11",
          "position": {
            "x": 40,
            "y": 810
          },
          "props": {
            "height": 110,
            "helpText": "Provide the best contact number for emergencies.",
            "label": "Emergency contact - Mobile",
            "placeholder": "04xx xxx xxx",
            "required": true,
            "tabOrder": 11,
            "validation": {
              "phone": true,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "divider-12",
          "position": {
            "x": 40,
            "y": 944
          },
          "props": {
            "height": 20,
            "tabOrder": 12,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "textarea-13",
          "position": {
            "x": 40,
            "y": 988
          },
          "props": {
            "height": 200,
            "helpText": "This information helps our staff provide a safe workout environment. Your details will be handled in accordance with our Privacy Policy.",
            "label": "Relevant health information / medical conditions",
            "placeholder": "List any conditions, medications, recent surgeries, injuries or allergies. If none, write 'None'.",
            "required": false,
            "tabOrder": 13,
            "validation": {
              "minLength": 0,
              "required": false
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "file-upload-14",
          "position": {
            "x": 40,
            "y": 1292
          },
          "props": {
            "height": 132,
            "helpText": "Accepted: PDF, JPG, PNG. Max file size 10MB. Upload only if you have a doctor's clearance you wish to attach.",
            "label": "Medical clearance (optional)",
            "placeholder": "Upload a medical certificate if required",
            "required": false,
            "tabOrder": 14,
            "validation": {
              "required": false
            },
            "width": "480px"
          },
          "style": {
            "height": 132,
            "width": 480
          },
          "type": "file-upload"
        },
        {
          "id": "divider-15",
          "position": {
            "x": 40,
            "y": 1480
          },
          "props": {
            "height": 20,
            "tabOrder": 15,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "dropdown-16",
          "position": {
            "x": 40,
            "y": 1524
          },
          "props": {
            "height": 110,
            "helpText": "Choose the membership plan you are applying for.",
            "label": "Membership type",
            "options": [
              {
                "label": "Standard",
                "value": "standard"
              },
              {
                "label": "Premium (includes group classes and PT discounts)",
                "value": "premium"
              },
              {
                "label": "Concession (student/senior)",
                "value": "concession"
              },
              {
                "label": "Family",
                "value": "family"
              },
              {
                "label": "Trial (7-day)",
                "value": "trial"
              }
            ],
            "placeholder": "Select membership type",
            "required": true,
            "tabOrder": 16,
            "validation": {
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "date-17",
          "position": {
            "x": 424,
            "y": 1524
          },
          "props": {
            "height": 110,
            "helpText": "Enter the date you want your membership to begin.",
            "label": "Membership start date",
            "placeholder": "DD/MM/YYYY",
            "required": true,
            "tabOrder": 17,
            "validation": {
              "required": true
            },
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "divider-18",
          "position": {
            "x": 40,
            "y": 1658
          },
          "props": {
            "height": 20,
            "tabOrder": 18,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "terms-19",
          "position": {
            "x": 40,
            "y": 1702
          },
          "props": {
            "height": 120,
            "helpText": "This is a legal acknowledgement of risk and is required to proceed.",
            "label": "I acknowledge that participating in physical activity carries a risk of injury. I confirm I have disclosed all relevant medical conditions and will follow staff instructions and safety guidelines.",
            "required": true,
            "tabOrder": 19,
            "validation": {
              "required": true
            },
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "terms-20",
          "position": {
            "x": 40,
            "y": 1846
          },
          "props": {
            "height": 120,
            "helpText": "Tapping the link will open the gym waiver terms in a popup. Please read before agreeing.",
            "label": "I have read and agree to the gym waiver terms.",
            "required": true,
            "tabOrder": 20,
            "validation": {
              "required": true
            },
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-21",
          "position": {
            "x": 40,
            "y": 1990
          },
          "props": {
            "height": 72,
            "helpText": "By submitting you confirm the information provided is true and complete.",
            "label": "Agree and Join",
            "tabOrder": 21,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Gym Membership Waiver"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 5: `p-05-rsvp-wedding__r01`

- Prompt ID: `p-05-rsvp-wedding`
- Repetition: `1`
- Variant: `post-642-capability-cleanup`
- EvalRunID: `17`
- GenerationRunID: `111`
- Definition source: `dbo.GenerationArtifact`

### Prompt

Create a wedding RSVP form. Collect guest contact details, attendance, plus-one name if applicable, meal choice, dietary requirements, song request, and a short message for the couple.

### Prompt Metadata

```json
{
  "pii_adjacent": true,
  "source_type": "wedding RSVP",
  "tricky_edges": [
    "plus-one",
    "meal-choice",
    "dietary-notes"
  ]
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 17,
  "duration_ms": 47835,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 2110,
    "width": 960
  },
  "formId": "wedding-rsvp",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "helpText": "If you are not attending, you can still send a message to the couple. If you are bringing a guest, please include their name.",
            "label": "RSVP instructions",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Given name",
            "placeholder": "e.g. Emma",
            "required": true,
            "tabOrder": 2,
            "validation": {
              "maxLength": 60,
              "required": true
            },
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Surname",
            "placeholder": "e.g. Smith",
            "required": true,
            "tabOrder": 3,
            "validation": {
              "maxLength": 80,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "required": true,
            "tabOrder": 4,
            "validation": {
              "email": true,
              "maxLength": 254,
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Include country code if outside Australia/New Zealand (e.g. +61 4xx xxx xxx).",
            "label": "Mobile",
            "placeholder": "04xx xxx xxx",
            "tabOrder": 5,
            "validation": {
              "phone": true
            },
            "width": "280px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "divider-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 20,
            "label": "Attendance",
            "tabOrder": 6,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 408
          },
          "props": {
            "height": 120,
            "label": "Will you attend our wedding?",
            "options": [
              {
                "label": "Yes \u2014 we will attend",
                "value": "attending"
              },
              {
                "label": "No \u2014 regretfully cannot attend",
                "value": "decline"
              }
            ],
            "required": true,
            "tabOrder": 7,
            "validation": {
              "required": true
            },
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "radio"
        },
        {
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 552
          },
          "props": {
            "height": 120,
            "helpText": "If yes, please provide your guest's name below.",
            "label": "Are you bringing a plus-one?",
            "options": [
              {
                "label": "No, attending alone",
                "value": "no_plus_one"
              },
              {
                "label": "Yes, I will bring a guest",
                "value": "with_plus_one"
              }
            ],
            "required": true,
            "tabOrder": 8,
            "validation": {
              "required": true
            },
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "radio"
        },
        {
          "id": "text-9",
          "position": {
            "x": 40,
            "y": 696
          },
          "props": {
            "height": 110,
            "helpText": "Only complete if you are bringing a guest.",
            "label": "Plus-one's Given name and Surname",
            "placeholder": "e.g. James Brown",
            "tabOrder": 9,
            "validation": {
              "maxLength": 140
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "dropdown-10",
          "position": {
            "x": 40,
            "y": 830
          },
          "props": {
            "height": 110,
            "helpText": "Please select a meal for each attending guest where applicable. If not attending, leave blank.",
            "label": "Meal choice (main course)",
            "options": [
              {
                "label": "Seared barramundi (fish)",
                "value": "barramundi"
              },
              {
                "label": "Free-range chicken with seasonal veg",
                "value": "chicken"
              },
              {
                "label": "Roast scotch fillet (beef)",
                "value": "beef"
              },
              {
                "label": "Vegetarian seasonal risotto",
                "value": "vegetarian"
              },
              {
                "label": "Vegan option",
                "value": "vegan"
              },
              {
                "label": "Children's meal",
                "value": "child_meal"
              }
            ],
            "placeholder": "Select main course",
            "required": false,
            "tabOrder": 10,
            "validation": {
              "required": false
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-11",
          "position": {
            "x": 40,
            "y": 964
          },
          "props": {
            "height": 120,
            "helpText": "Select any that apply. Use the field below to give full details if needed.",
            "label": "Dietary requirements (select all that apply)",
            "options": [
              {
                "label": "No special requirements",
                "value": "none"
              },
              {
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Dairy-free",
                "value": "dairy_free"
              },
              {
                "label": "Nut allergy",
                "value": "nut_allergy"
              },
              {
                "label": "Shellfish allergy",
                "value": "shellfish_allergy"
              },
              {
                "label": "Halal",
                "value": "halal"
              },
              {
                "label": "Kosher",
                "value": "kosher"
              },
              {
                "label": "Other (please specify below)",
                "value": "other"
              }
            ],
            "required": false,
            "tabOrder": 11,
            "validation": {
              "required": false
            },
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-12",
          "position": {
            "x": 40,
            "y": 1108
          },
          "props": {
            "height": 200,
            "helpText": "Give as much detail as possible so we can accommodate you safely.",
            "label": "Dietary details / allergy information",
            "placeholder": "Please list ingredients to avoid, severity of allergy, or any other details we should know.",
            "tabOrder": 12,
            "validation": {
              "maxLength": 500
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "text-13",
          "position": {
            "x": 40,
            "y": 1412
          },
          "props": {
            "height": 110,
            "helpText": "We'll do our best to play requests but can't guarantee every song.",
            "label": "Song request",
            "placeholder": "Song title and artist \u2014 e.g. 'Dancing Queen \u2014 ABBA'",
            "tabOrder": 13,
            "validation": {
              "maxLength": 140
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "textarea-14",
          "position": {
            "x": 40,
            "y": 1546
          },
          "props": {
            "height": 200,
            "helpText": "We may read some messages on the day \u2014 feel free to keep it short and sweet.",
            "label": "Message for the couple",
            "placeholder": "Write a short message or well wishes to the couple",
            "tabOrder": 14,
            "validation": {
              "maxLength": 600
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "divider-15",
          "position": {
            "x": 40,
            "y": 1850
          },
          "props": {
            "height": 20,
            "label": "Privacy",
            "tabOrder": 15,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "paragraph-16",
          "position": {
            "x": 40,
            "y": 1894
          },
          "props": {
            "height": 48,
            "helpText": "Your RSVP details will be used by the wedding hosts to manage guest lists and catering. By submitting this form you consent to your details being stored for wedding planning purposes.",
            "label": "Privacy note",
            "tabOrder": 16,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "submit-button-17",
          "position": {
            "x": 40,
            "y": 1966
          },
          "props": {
            "height": 72,
            "label": "Send RSVP",
            "tabOrder": 17,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Wedding RSVP"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 6: `p-06-feedback-post-event__r01`

- Prompt ID: `p-06-feedback-post-event`
- Repetition: `1`
- Variant: `post-642-capability-cleanup`
- EvalRunID: `18`
- GenerationRunID: `112`
- Definition source: `dbo.GenerationArtifact`

### Prompt

Create a simple post-event feedback form asking what attendees liked, what should improve, overall satisfaction, and whether they want updates about next year's event.

### Prompt Metadata

```json
{
  "pii_adjacent": true,
  "source_type": "post-event feedback",
  "tricky_edges": [
    "minimal-context",
    "emergent-structure"
  ]
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 34938,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1282,
    "width": 960
  },
  "formId": "post-event-feedback",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Please tell us what you liked, what could be improved, and how satisfied you were overall. You can also opt in to receive updates about next year's event.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "textarea-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 200,
            "helpText": "Be as specific as you like. Max 1000 characters.",
            "label": "What did you like about the event?",
            "placeholder": "Highlights, sessions, speakers, networking \u2014 tell us what stood out.",
            "required": false,
            "tabOrder": 2,
            "validation": {
              "maxLength": 1000,
              "required": false
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "textarea-3",
          "position": {
            "x": 40,
            "y": 400
          },
          "props": {
            "height": 200,
            "helpText": "Your suggestions help us improve future events. Max 1000 characters.",
            "label": "What should we improve for next time?",
            "placeholder": "Content, format, venue, timing, accessibility, or anything else we could do better.",
            "required": false,
            "tabOrder": 3,
            "validation": {
              "maxLength": 1000,
              "required": false
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "rating-4",
          "position": {
            "x": 40,
            "y": 704
          },
          "props": {
            "height": 88,
            "helpText": "1 = Very dissatisfied, 5 = Very satisfied.",
            "label": "Overall satisfaction",
            "required": true,
            "tabOrder": 4,
            "validation": {
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 88,
            "width": 360
          },
          "type": "rating"
        },
        {
          "id": "email-5",
          "position": {
            "x": 40,
            "y": 816
          },
          "props": {
            "height": 110,
            "helpText": "We will only use your email if you opt in to receive updates about next year's event.",
            "label": "Email (optional)",
            "placeholder": "[SCRUBBED_EMAIL]",
            "required": false,
            "tabOrder": 5,
            "validation": {
              "email": true,
              "maxLength": 254,
              "required": false
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "terms-6",
          "position": {
            "x": 40,
            "y": 950
          },
          "props": {
            "height": 120,
            "helpText": "You can withdraw consent at any time. See our Privacy Notice for details.",
            "label": "I agree to receive email updates about next year's event (optional).",
            "required": false,
            "tabOrder": 6,
            "validation": {
              "required": false
            },
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "divider-7",
          "position": {
            "x": 40,
            "y": 1094
          },
          "props": {
            "height": 20,
            "tabOrder": 7,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "submit-button-8",
          "position": {
            "x": 40,
            "y": 1138
          },
          "props": {
            "height": 72,
            "label": "Submit feedback",
            "tabOrder": 8,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Post-event feedback"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 7: `p-07-booking-consultation__r01`

- Prompt ID: `p-07-booking-consultation`
- Repetition: `1`
- Variant: `post-642-capability-cleanup`
- EvalRunID: `19`
- GenerationRunID: `113`
- Definition source: `dbo.GenerationArtifact`

### Prompt

Create a consultation booking form for a professional services firm. Collect contact details, preferred consultation type, preferred date, available time window, topic summary, urgency, and consent to receive appointment reminders.

### Prompt Metadata

```json
{
  "pii_adjacent": true,
  "source_type": "consultation booking",
  "tricky_edges": [
    "calendar-slots",
    "conditional-reminder"
  ]
}
```

### Category A Metrics

```json
{
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 100986,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1502,
    "width": 960
  },
  "formId": "consultation-booking-form",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Please complete your contact details and your preferred times. We\u2019ll contact you to confirm the appointment.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Given name",
            "placeholder": "Given name",
            "required": true,
            "tabOrder": 2,
            "validation": {
              "maxLength": 60,
              "required": true
            },
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Surname",
            "placeholder": "Surname",
            "required": true,
            "tabOrder": 3,
            "validation": {
              "maxLength": 60,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "text-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "If you\u2019re booking on behalf of an organisation, enter the organisation name.",
            "label": "Organisation (optional)",
            "placeholder": "Organisation",
            "required": false,
            "tabOrder": 4,
            "validation": {
              "maxLength": 100,
              "required": false
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send appointment confirmation and reminders to this email.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "required": true,
            "tabOrder": 5,
            "validation": {
              "email": true,
              "maxLength": 254,
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-6",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Local mobile preferred. Include +61 if outside Australia.",
            "label": "Mobile",
            "placeholder": "04xx xxx xxx",
            "required": true,
            "tabOrder": 6,
            "validation": {
              "phone": true,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Choose how you\u2019d like to meet.",
            "label": "Preferred consultation type",
            "options": [
              {
                "label": "Phone call",
                "value": "phone"
              },
              {
                "label": "Video meeting (Zoom/Teams)",
                "value": "video"
              },
              {
                "label": "In\u2011person meeting",
                "value": "in_person"
              },
              {
                "label": "Email or written advice",
                "value": "email_advice"
              }
            ],
            "placeholder": "Select consultation type",
            "required": true,
            "tabOrder": 7,
            "validation": {
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "date-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Enter your preferred date in DD/MM/YYYY format. If flexible, choose the earliest date that suits you.",
            "label": "Preferred date",
            "placeholder": "DD/MM/YYYY",
            "required": true,
            "tabOrder": 8,
            "validation": {
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "text-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "Use 24\u2011hour time (HH:MM).",
            "label": "Available from (local time)",
            "placeholder": "09:00",
            "required": true,
            "tabOrder": 9,
            "validation": {
              "pattern": "^(?:[01]\\d|2[0-3]):[0-5]\\d$",
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-10",
          "position": {
            "x": 424,
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "Use 24\u2011hour time (HH:MM).",
            "label": "Available to (local time)",
            "placeholder": "12:30",
            "required": true,
            "tabOrder": 10,
            "validation": {
              "pattern": "^(?:[01]\\d|2[0-3]):[0-5]\\d$",
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 766
          },
          "props": {
            "height": 200,
            "helpText": "Provide enough detail so we can prepare. 2000 character limit.",
            "label": "Topic summary",
            "placeholder": "Briefly describe the topic you want to discuss (what outcome you\u2019re seeking, key questions or documents).",
            "required": true,
            "tabOrder": 11,
            "validation": {
              "maxLength": 2000,
              "minLength": 20,
              "required": true
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "radio-12",
          "position": {
            "x": 40,
            "y": 1070
          },
          "props": {
            "height": 120,
            "helpText": "Select how soon you need the consultation.",
            "label": "Urgency",
            "options": [
              {
                "label": "Routine (within 4 weeks)",
                "value": "routine"
              },
              {
                "label": "Priority (within 7 days)",
                "value": "priority"
              },
              {
                "label": "Urgent (within 48 hours)",
                "value": "urgent"
              }
            ],
            "required": true,
            "tabOrder": 12,
            "validation": {
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "terms-13",
          "position": {
            "x": 40,
            "y": 1214
          },
          "props": {
            "height": 120,
            "helpText": "You may withdraw consent at any time. View the consultation booking terms for more information.",
            "label": "I agree to receive appointment confirmations and reminders by email or SMS as needed.",
            "required": true,
            "tabOrder": 13,
            "validation": {
              "required": true
            },
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-14",
          "position": {
            "x": 40,
            "y": 1358
          },
          "props": {
            "height": 72,
            "label": "Request consultation",
            "tabOrder": 14,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Consultation booking form"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 8: `p-08-onboarding-new-employee__r01`

- Prompt ID: `p-08-onboarding-new-employee`
- Repetition: `1`
- Variant: `post-642-capability-cleanup`
- EvalRunID: `20`
- GenerationRunID: `114`
- Definition source: `dbo.GenerationArtifact`

### Prompt

Create a new employee onboarding form. Collect synthetic employee personal details, emergency contact, start date, department, equipment needs, payroll setup notes, policy acknowledgements, and optional accessibility support requirements.

### Prompt Metadata

```json
{
  "pii_adjacent": true,
  "source_type": "employee onboarding",
  "tricky_edges": [
    "multi-section",
    "pii-heavy-synthetic"
  ]
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 23,
  "duration_ms": 80864,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 2564,
    "width": 960
  },
  "formId": "employee-onboarding-form",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "We collect the following details to set up your employment record. Fields marked required must be completed before submission.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Given name",
            "placeholder": "e.g. Maria",
            "required": true,
            "tabOrder": 2,
            "validation": {
              "required": true
            },
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Surname",
            "placeholder": "e.g. Nguyen",
            "required": true,
            "tabOrder": 3,
            "validation": {
              "maxLength": 100,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Use your preferred contact email. We will send onboarding information to this address.",
            "label": "Work email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "required": true,
            "tabOrder": 4,
            "validation": {
              "email": true,
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Enter an AU or NZ mobile (include +61 / +64 if calling internationally).",
            "label": "Mobile",
            "placeholder": "04xx xxx xxx",
            "required": true,
            "tabOrder": 5,
            "validation": {
              "phone": true,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide your current residential address. Use format: street address, Suburb, State, Postcode.",
            "label": "Residential address",
            "placeholder": "123 George Street, Sydney NSW 2000",
            "required": true,
            "tabOrder": 6,
            "validation": {
              "required": true
            },
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "divider-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 20,
            "tabOrder": 7,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "date-8",
          "position": {
            "x": 40,
            "y": 542
          },
          "props": {
            "height": 110,
            "helpText": "Planned first day of employment (DD/MM/YYYY).",
            "label": "Start date",
            "placeholder": "DD/MM/YYYY",
            "required": true,
            "tabOrder": 8,
            "validation": {
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "date"
        },
        {
          "id": "dropdown-9",
          "position": {
            "x": 424,
            "y": 542
          },
          "props": {
            "height": 110,
            "label": "Department",
            "options": [
              {
                "label": "Human Resources (HR)",
                "value": "hr"
              },
              {
                "label": "Finance",
                "value": "finance"
              },
              {
                "label": "Information Technology (IT)",
                "value": "it"
              },
              {
                "label": "Marketing",
                "value": "marketing"
              },
              {
                "label": "Operations",
                "value": "operations"
              },
              {
                "label": "Customer Service",
                "value": "customer_service"
              },
              {
                "label": "Legal",
                "value": "legal"
              },
              {
                "label": "Research & Development",
                "value": "rnd"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select department",
            "required": true,
            "tabOrder": 9,
            "validation": {
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 676
          },
          "props": {
            "height": 120,
            "helpText": "Select any items you require for your role. Additional requests can be noted below.",
            "label": "Equipment needs",
            "options": [
              {
                "label": "Laptop",
                "value": "laptop"
              },
              {
                "label": "Docking station",
                "value": "docking_station"
              },
              {
                "label": "Monitor",
                "value": "monitor"
              },
              {
                "label": "Keyboard & mouse",
                "value": "keyboard_mouse"
              },
              {
                "label": "Mobile phone",
                "value": "mobile_phone"
              },
              {
                "label": "Headset",
                "value": "headset"
              },
              {
                "label": "Software licences",
                "value": "software_licenses"
              },
              {
                "label": "Ergonomic chair",
                "value": "ergonomic_chair"
              },
              {
                "label": "Other (please specify below)",
                "value": "other"
              }
            ],
            "tabOrder": 10,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 820
          },
          "props": {
            "height": 200,
            "helpText": "Use this field for model preferences, accessibility-related equipment, or other notes.",
            "label": "Additional equipment requests",
            "placeholder": "Specify models, special requirements or other items...",
            "tabOrder": 11,
            "validation": {
              "maxLength": 1000
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "textarea-12",
          "position": {
            "x": 40,
            "y": 1124
          },
          "props": {
            "height": 200,
            "helpText": "Do not include your Tax File Number (TFN) here. Banking and tax information are handled in a secure payroll portal.",
            "label": "Payroll setup notes",
            "placeholder": "Any notes for payroll (banking details will be collected securely later)...",
            "tabOrder": 12,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "divider-13",
          "position": {
            "x": 40,
            "y": 1428
          },
          "props": {
            "height": 20,
            "tabOrder": 13,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "text-14",
          "position": {
            "x": 40,
            "y": 1472
          },
          "props": {
            "height": 110,
            "label": "Emergency contact \u2014 Given name",
            "placeholder": "e.g. John",
            "required": true,
            "tabOrder": 14,
            "validation": {
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-15",
          "position": {
            "x": 424,
            "y": 1472
          },
          "props": {
            "height": 110,
            "label": "Emergency contact \u2014 Surname",
            "placeholder": "e.g. Smith",
            "required": true,
            "tabOrder": 15,
            "validation": {
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "phone-16",
          "position": {
            "x": 40,
            "y": 1606
          },
          "props": {
            "height": 110,
            "helpText": "Provide a number we can call in an emergency. Include +61/+64 if international.",
            "label": "Emergency contact \u2014 Phone",
            "placeholder": "04xx xxx xxx or (02) xxxx xxxx",
            "required": true,
            "tabOrder": 16,
            "validation": {
              "phone": true,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "text-17",
          "position": {
            "x": 424,
            "y": 1606
          },
          "props": {
            "height": 110,
            "label": "Relationship to you",
            "placeholder": "e.g. Partner, Parent, Friend",
            "required": true,
            "tabOrder": 17,
            "validation": {
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "divider-18",
          "position": {
            "x": 40,
            "y": 1740
          },
          "props": {
            "height": 20,
            "tabOrder": 18,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "checkbox-19",
          "position": {
            "x": 40,
            "y": 1784
          },
          "props": {
            "height": 120,
            "helpText": "Tick if you require workplace adjustments or support (optional).",
            "label": "Accessibility support",
            "options": [
              {
                "label": "I require accessibility support or adjustments",
                "value": "access_support"
              }
            ],
            "tabOrder": 19,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-20",
          "position": {
            "x": 40,
            "y": 1928
          },
          "props": {
            "height": 200,
            "helpText": "Provide any details that will help us prepare adjustments for your first day. This is optional and will be handled sensitively.",
            "label": "Accessibility support details (optional)",
            "placeholder": "Describe any adjustments, equipment or support you need...",
            "tabOrder": 20,
            "validation": {
              "maxLength": 1000
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "divider-21",
          "position": {
            "x": 40,
            "y": 2232
          },
          "props": {
            "height": 20,
            "tabOrder": 21,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "terms-22",
          "position": {
            "x": 40,
            "y": 2276
          },
          "props": {
            "height": 120,
            "helpText": "Please open and read the policies before agreeing.",
            "label": "I acknowledge that I have read and agree to the company's policies referenced in the employee policy acknowledgement.",
            "required": true,
            "tabOrder": 22,
            "validation": {
              "required": true
            },
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-23",
          "position": {
            "x": 40,
            "y": 2420
          },
          "props": {
            "height": 72,
            "label": "Submit onboarding",
            "tabOrder": 23,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "New Employee Onboarding Form"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 9: `p-09-application-scholarship__r01`

- Prompt ID: `p-09-application-scholarship`
- Repetition: `1`
- Variant: `post-642-capability-cleanup`
- EvalRunID: `21`
- GenerationRunID: `115`
- Definition source: `dbo.GenerationArtifact`

### Prompt

Create a scholarship application form. Collect applicant contact details, study program, eligibility confirmations, two short essay responses, optional supporting document note, referee contact, and agreement to application terms.

### Prompt Metadata

```json
{
  "pii_adjacent": true,
  "source_type": "scholarship application",
  "tricky_edges": [
    "long-form-essays",
    "file-upload-intent",
    "terms"
  ]
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 20,
  "duration_ms": 59973,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 2566,
    "width": 960
  },
  "formId": "scholarship-application-au",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "helpText": "Fill in your contact details, confirm your eligibility, provide two short essays, supply a referee contact, and agree to the scholarship application terms. Fields marked required must be completed.",
            "label": "Application instructions",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Given name",
            "placeholder": "Given name",
            "required": true,
            "tabOrder": 2,
            "validation": {
              "minLength": 1,
              "required": true
            },
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Surname",
            "placeholder": "Surname",
            "required": true,
            "tabOrder": 3,
            "validation": {
              "minLength": 1,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We'll use this to contact you about your application.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "required": true,
            "tabOrder": 4,
            "validation": {
              "email": true,
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Include country code if outside Australia/NZ (e.g. +61).",
            "label": "Mobile",
            "placeholder": "04xx xxx xxx",
            "required": true,
            "tabOrder": 5,
            "validation": {
              "phone": true,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Include Suburb, State and Postcode.",
            "label": "Postal address",
            "placeholder": "123 George Street, Sydney NSW 2000",
            "required": true,
            "tabOrder": 6,
            "validation": {
              "required": true
            },
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Choose the programme level for which you are seeking a scholarship.",
            "label": "Study programme",
            "options": [
              {
                "label": "Undergraduate (Bachelor)",
                "value": "undergraduate"
              },
              {
                "label": "Postgraduate (Master / Graduate Diploma)",
                "value": "postgraduate"
              },
              {
                "label": "Doctoral (PhD)",
                "value": "doctoral"
              },
              {
                "label": "Vocational / Certificate",
                "value": "vocational"
              },
              {
                "label": "Short course / Professional development",
                "value": "short_course"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select the programme level you are applying for",
            "required": true,
            "tabOrder": 7,
            "validation": {
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "text-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "label": "Intended course / field of study",
            "placeholder": "e.g. Bachelor of Science (Environmental Science)",
            "required": true,
            "tabOrder": 8,
            "validation": {
              "maxLength": 200,
              "minLength": 2,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Tick each box that correctly describes your eligibility. You must select the statements that apply.",
            "label": "Eligibility confirmations",
            "options": [
              {
                "label": "I am an Australian or New Zealand citizen or permanent resident",
                "value": "citizen_resident"
              },
              {
                "label": "I am currently enrolled or have an offer to commence the nominated programme",
                "value": "enrolled_or_offer"
              },
              {
                "label": "I am not in receipt of a full-time scholarship from another provider that would prevent me from accepting this award",
                "value": "no_conflict_scholarship"
              },
              {
                "label": "I can meet any additional eligibility requirements specified by the scholarship",
                "value": "meet_additional_requirements"
              }
            ],
            "required": true,
            "tabOrder": 9,
            "validation": {
              "required": true
            },
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-10",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 200,
            "helpText": "Focus on your academic goals, financial need and how the scholarship will support your studies.",
            "label": "Short essay: Personal statement \u2014 Why do you deserve this scholarship?",
            "placeholder": "Provide a concise statement outlining your need, goals and suitability (250\u2013500 words recommended).",
            "required": true,
            "tabOrder": 10,
            "validation": {
              "maxLength": 3000,
              "minLength": 150,
              "required": true
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 1080
          },
          "props": {
            "height": 200,
            "helpText": "Include awards, leadership roles, community work or research experience.",
            "label": "Short essay: Achievements and impact \u2014 Describe relevant academic or community achievements",
            "placeholder": "Outline up to three key achievements and their impact (250\u2013500 words recommended).",
            "required": true,
            "tabOrder": 11,
            "validation": {
              "maxLength": 3000,
              "minLength": 150,
              "required": true
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "textarea-12",
          "position": {
            "x": 40,
            "y": 1384
          },
          "props": {
            "height": 200,
            "helpText": "If you will upload documents below, briefly list them here. This field is optional.",
            "label": "Supporting documents (optional) \u2014 note",
            "placeholder": "List any supporting documents you'll upload or include (e.g. academic transcript, CV, referee reports).",
            "required": false,
            "tabOrder": 12,
            "validation": {
              "maxLength": 1000,
              "required": false
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "file-upload-13",
          "position": {
            "x": 40,
            "y": 1688
          },
          "props": {
            "height": 132,
            "helpText": "Accepted: PDF, DOC, DOCX, JPG, PNG. Max 10MB per file. You may upload up to 5 files.",
            "label": "Upload supporting documents (optional)",
            "options": [
              {
                "label": "acceptedFileTypes",
                "value": ".pdf,.doc,.docx,.jpg,.jpeg,.png"
              },
              {
                "label": "maxFiles",
                "value": 5
              }
            ],
            "required": false,
            "tabOrder": 13,
            "validation": {
              "required": false
            },
            "width": "480px"
          },
          "style": {
            "height": 132,
            "width": 480
          },
          "type": "file-upload"
        },
        {
          "id": "first-name-14",
          "position": {
            "x": 40,
            "y": 1876
          },
          "props": {
            "height": 110,
            "label": "Referee given name",
            "placeholder": "Given name",
            "required": true,
            "tabOrder": 14,
            "validation": {
              "required": true
            },
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-15",
          "position": {
            "x": 424,
            "y": 1876
          },
          "props": {
            "height": 110,
            "label": "Referee surname",
            "placeholder": "Surname",
            "required": true,
            "tabOrder": 15,
            "validation": {
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-16",
          "position": {
            "x": 40,
            "y": 2010
          },
          "props": {
            "height": 110,
            "label": "Referee organisation",
            "placeholder": "e.g. University of Sydney / Company name",
            "required": false,
            "tabOrder": 16,
            "validation": {
              "maxLength": 200,
              "required": false
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "phone-17",
          "position": {
            "x": 40,
            "y": 2144
          },
          "props": {
            "height": 110,
            "label": "Referee phone",
            "placeholder": "04xx xxx xxx",
            "required": true,
            "tabOrder": 17,
            "validation": {
              "phone": true,
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "email-18",
          "position": {
            "x": 424,
            "y": 2144
          },
          "props": {
            "height": 110,
            "label": "Referee email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "required": true,
            "tabOrder": 18,
            "validation": {
              "email": true,
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "terms-19",
          "position": {
            "x": 40,
            "y": 2278
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the scholarship application terms to submit your application.",
            "label": "I have read and agree to the scholarship application terms",
            "required": true,
            "tabOrder": 19,
            "validation": {
              "required": true
            },
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-20",
          "position": {
            "x": 40,
            "y": 2422
          },
          "props": {
            "height": 72,
            "helpText": "Click to submit your application. You will receive an email confirmation if your submission is successful.",
            "label": "Submit application",
            "tabOrder": 20,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Scholarship application form"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 10: `p-10-donation-charity__r01`

- Prompt ID: `p-10-donation-charity`
- Repetition: `1`
- Variant: `post-642-capability-cleanup`
- EvalRunID: `22`
- GenerationRunID: `116`
- Definition source: `dbo.GenerationArtifact`

### Prompt

Create a charity donation interest form. Collect donor contact details, donation amount preference, whether the gift is one-off or recurring, gift-aid or tax receipt details, message of support, and consent to receive campaign updates.

### Prompt Metadata

```json
{
  "pii_adjacent": true,
  "source_type": "charity donation",
  "tricky_edges": [
    "amount-selection",
    "gift-aid",
    "recurring-toggle"
  ]
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 51973,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1924,
    "width": 960
  },
  "formId": "charity-donation-interest",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "We appreciate your support. This short form helps us understand your donation intentions so we can provide the right information about giving options and receipts.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Given name",
            "placeholder": "Given name",
            "required": true,
            "tabOrder": 2,
            "validation": {
              "required": true
            },
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Surname",
            "placeholder": "Surname",
            "required": true,
            "tabOrder": 3,
            "validation": {
              "required": true
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We will send donation information and receipts to this address.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "required": true,
            "tabOrder": 4,
            "validation": {
              "email": true,
              "required": true
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Preferred contact number. Include +61 if you are outside Australia.",
            "label": "Mobile",
            "placeholder": "04xx xxx xxx",
            "required": true,
            "tabOrder": 5,
            "validation": {
              "phone": true,
              "required": true
            },
            "width": "280px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Enter street, Suburb, State and Postcode. Leave blank if you prefer email-only communications.",
            "label": "Postal address",
            "placeholder": "123 George Street, Sydney NSW 2000",
            "required": false,
            "tabOrder": 6,
            "validation": {
              "required": false
            },
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Choose a suggested amount, or select Other to enter a custom amount.",
            "label": "Donation amount preference (AUD)",
            "options": [
              {
                "label": "$25",
                "value": "25"
              },
              {
                "label": "$50",
                "value": "50"
              },
              {
                "label": "$100",
                "value": "100"
              },
              {
                "label": "$250",
                "value": "250"
              },
              {
                "label": "Other (enter amount below)",
                "value": "other"
              }
            ],
            "required": true,
            "tabOrder": 7,
            "validation": {
              "required": true
            },
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "radio"
        },
        {
          "id": "number-8",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 110,
            "helpText": "Enter whole dollars only. Leave blank unless you chose Other above.",
            "label": "If Other, enter amount (AUD)",
            "placeholder": "Enter whole dollar amount, e.g. 150",
            "required": false,
            "tabOrder": 8,
            "validation": {
              "max": 100000.0,
              "min": 1.0,
              "required": false
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "number"
        },
        {
          "id": "radio-9",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "If you choose recurring, select a frequency below.",
            "label": "Is this gift one-off or recurring?",
            "options": [
              {
                "label": "One-off",
                "value": "one_off"
              },
              {
                "label": "Recurring",
                "value": "recurring"
              }
            ],
            "required": true,
            "tabOrder": 9,
            "validation": {
              "required": true
            },
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "radio"
        },
        {
          "id": "dropdown-10",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 110,
            "helpText": "Choose how often you'd like payments processed. Leave blank if one-off.",
            "label": "If recurring, choose frequency",
            "options": [
              {
                "label": "Monthly",
                "value": "monthly"
              },
              {
                "label": "Quarterly",
                "value": "quarterly"
              },
              {
                "label": "Annually",
                "value": "annually"
              }
            ],
            "placeholder": "Select frequency (optional)",
            "required": false,
            "tabOrder": 10,
            "validation": {
              "required": false
            },
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "radio-11",
          "position": {
            "x": 40,
            "y": 1054
          },
          "props": {
            "height": 120,
            "helpText": "Receipts will be issued to the name and email provided above for donations eligible for tax deduction.",
            "label": "Would you like a tax receipt for your donation?",
            "options": [
              {
                "label": "Yes, please issue a receipt",
                "value": "yes"
              },
              {
                "label": "No, I do not need a receipt",
                "value": "no"
              }
            ],
            "required": true,
            "tabOrder": 11,
            "validation": {
              "required": true
            },
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "radio"
        },
        {
          "id": "text-12",
          "position": {
            "x": 40,
            "y": 1198
          },
          "props": {
            "height": 110,
            "helpText": "Useful if the donation is made on behalf of an organisation or another person.",
            "label": "Name for receipt (leave blank to use donor name)",
            "placeholder": "Name as you want it on the receipt",
            "required": false,
            "tabOrder": 12,
            "validation": {
              "maxLength": 200,
              "required": false
            },
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "textarea-13",
          "position": {
            "x": 40,
            "y": 1332
          },
          "props": {
            "height": 200,
            "helpText": "Your message may be shared internally with fundraising staff and volunteers.",
            "label": "Message of support (optional)",
            "placeholder": "Write a short message to the charity (max 1000 characters)",
            "required": false,
            "tabOrder": 13,
            "validation": {
              "maxLength": 1000,
              "required": false
            },
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1636
          },
          "props": {
            "height": 120,
            "helpText": "You can view full donation terms via the linked document.",
            "label": "I consent to receive campaign updates and fundraising communications. I understand I can withdraw consent at any time.",
            "required": false,
            "tabOrder": 14,
            "validation": {
              "required": false
            },
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-15",
          "position": {
            "x": 40,
            "y": 1780
          },
          "props": {
            "height": 72,
            "helpText": "We'll contact you with options and next steps.",
            "label": "Submit interest",
            "tabOrder": 15,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Charity donation interest form"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```
