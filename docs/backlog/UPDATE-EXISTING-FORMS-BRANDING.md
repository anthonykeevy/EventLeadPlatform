# Backlog: Form Builder - Synchronize Existing Forms with Company Branding Defaults

## Context
During UAT (Story 5.9), it was confirmed that modifying global "Company Defaults" (colors, fonts) only applies to *newly created* forms. This is a standard industry practice to avoid breaking live/published form UI layouts accidentally. However, customers may still want the choice to bulk-update or individually sync existing forms when their company's brand kit changes.

## Requirement
Provide an explicit and safe UX pattern to allow form creators to pull updated Company Defaults into an existing form without forcing an automatic retroactive override.

## Proposed Solutions / Acceptance Criteria
1. **Form-Level "Sync with Company Default" Button**:
   - In the Form Builder's "Appearance" or "Branding" property panel, add a clear button/action: **"Reset to Company Defaults"**.
   - When clicked, this should overwrite the form's local branding settings with the current company-wide settings.
   - The user must explicitly hit "Save" or "Publish" after verifying the layout looks correct on the canvas with the new colors/fonts.
2. **Opt-In Modal on Settings Change (Optional)**:
   - When a Company Admin saves new Company Defaults, display a confirmation modal offering a checkbox: "Also apply these changes to existing *Unpublished* forms."
   - If selected, update only DRAFT or PENDING forms, protecting any form that is actively PUBLISHED.