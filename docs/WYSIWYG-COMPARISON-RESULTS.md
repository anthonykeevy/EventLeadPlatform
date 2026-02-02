# WYSIWYG Comparison Results

**Generated:** 2026-01-19

## Executive Summary

Both Builder and Preview use the same `UniversalFieldShell` component with identical
style computation logic. This report validates that computed styles match.

| Icon | Meaning |
|------|---------|
| ✅ | Styles match between Builder and Preview |
| ⚡ | Property has component-level override (still matches) |
| ❌ | Mismatch detected (investigation needed) |

---

## Form Summary


### Form 41: Template C

| # | Component | Type | Position | Width | Label Font | Input Font | Border | Layout | Overrides |
|---|-----------|------|----------|-------|------------|------------|--------|--------|-----------|
| 1 | First Name | first-name | (104, None) | Auto | Inter 14px | Inter 14px | 1px #D1D5DB | horizontal | ✓ |
| 2 | Last Name | text | (104, 50.06250096909169) | Auto | Inter 14px | Inter 14px | 1px #D1D5DB | horizontal | - |
| 3 | Business Email Addre | email | (104, 99.16406398667475) | Auto | Inter 14px | Inter 14px | 1px #D1D5DB | vertical | - |
| 4 | Phone Number | phone | (104, 208) | Auto | Inter 14px | Inter 14px | 1px #D1D5DB | vertical | - |
| 5 | Event Type | dropdown | (104, 312) | 432px | Inter 14px | Inter 14px | 1px #D1D5DB | mixed | - |
| 6 | Other Event Type | text | (560, 328) | Auto | Inter 14px | Inter 14px | 1px #D1D5DB | horizontal | - |
| 7 | Number of Attendees | number | (104, 409.9687601490329) | Auto | Inter 14px | Inter 14px | 1px #D1D5DB | vertical | - |
| 8 | Company Name | text | (104, 515.98592353139) | Auto | Inter 14px | Inter 14px | 1px #D1D5DB | vertical | - |
| 9 | Dietary Requirements | checkbox | (104, 616) | 413px | Inter 14px | Inter 14px | 1px #D1D5DB | mixed | - |
| 10 | Allergy Information | textarea | (1144, 178) | 460px | Inter 14px | Inter 14px | 1px #D1D5DB | vertical | ✓ |
| 11 | Special Requests | textarea | (1144, 475.66668701171875) | 461px | Inter 14px | Inter 14px | 1px #D1D5DB | vertical | ✓ |
| 12 | Preferred Event Date | date | (1143, 747) | Auto | Inter 14px | Inter 14px | 1px #D1D5DB | vertical | - |
| 13 | I agree to the | terms | (1145, 869) | Auto | Inter 14px | Inter 14px | 1px #D1D5DB | horizontal | - |
| 14 |  | submit-button | (1141, 901) | Auto | Inter 14px | Inter 14px | 1px #D1D5DB | vertical | - |
| 15 | Radio Group | radio | (616, 384) | 331px | Inter 14px | Inter 14px | 1px #D1D5DB | mixed | - |

**Components:** 15 | **With Overrides:** 3


### Form 44: Template D

| # | Component | Type | Position | Width | Label Font | Input Font | Border | Layout | Overrides |
|---|-----------|------|----------|-------|------------|------------|--------|--------|-----------|
| 1 | Customer Type | radio | (100, 129.03361160213888) | 50% | Inter 16px | Inter 14px | None | vertical | ✓ |
| 2 | Company Name | text | (76, 340.05443355362496) | 50% | Roboto 14px | Inter 14px | None | horizontal | ✓ |
| 3 | Overall Satisfaction | dropdown | (101, 412) | Auto | Inter 16px | Inter 14px | None | vertical | ✓ |
| 4 | Reason for Your Rati | textarea | (102, 531) | 659px | Inter 14px | Inter 14px | None | vertical | ✓ |
| 5 | Would you recommend  | radio | (102, 650) | Auto | Inter 16px | Inter 14px | None | vertical | ✓ |
| 6 | Referral Name | text | (106, 821) | Auto | Inter 14px | Inter 14px | None | horizontal | - |
| 7 | How would you like u | checkbox | (1033, 14) | Auto | Inter 14px | Inter 14px | None | vertical | - |
| 8 | Preferred Contact Em | email | (1036, 221.99999856049158) | Auto | Inter 14px | Inter 14px | None | horizontal | ✓ |
| 9 | Preferred Contact Ph | phone | (1039, 272) | Auto | Inter 14px | Inter 14px | None | horizontal | - |
| 10 | Additional Comments | textarea | (1038, 330) | 466px | Inter 14px | Inter 14px | None | vertical | ✓ |
| 11 |  | divider | (1000, 537) | 253px | Inter 14px | Inter 14px | None | vertical | - |
| 12 | I agree to the | terms | (1042, 563) | Auto | Inter 14px | Inter 14px | None | vertical | - |
| 13 |  | submit-button | (1043, 663) | 100% | Inter 14px | Inter 14px | None | vertical | - |
| 14 | Select Date | date | (1040, 760) | Auto | Inter 14px | Inter 14px | None | vertical | - |

**Components:** 14 | **With Overrides:** 7


---

## Detailed Style Comparison


### Form 41: Template C - Detailed Styles


#### first-name: First Name
**ID:** `first-name-1767670364588-719`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 104px | 104px | ✅ |
| Position Y | Nonepx | Nonepx | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font ⚡ | Inter | Inter | ✅ |
| Label Size ⚡ | 14px | 14px | ✅ |
| Label Weight ⚡ | 600 | 600 | ✅ |
| Label Color ⚡ | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | horizontal | horizontal | ✅ |

**Style Overrides:** `labelFontWeight, labelBorderColor, labelBorderWidth, labelBorderRadius`

#### text: Last Name
**ID:** `text-1767670920558-854`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 104px | 104px | ✅ |
| Position Y | 50.06250096909169px | 50.06250096909169px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | horizontal | horizontal | ✅ |

#### email: Business Email Address
**ID:** `email-1767671516157-694`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 104px | 104px | ✅ |
| Position Y | 99.16406398667475px | 99.16406398667475px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

#### phone: Phone Number
**ID:** `phone-1767672150454-640`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 104px | 104px | ✅ |
| Position Y | 208px | 208px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

#### dropdown: Event Type
**ID:** `dropdown-1767672683029-921`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 104px | 104px | ✅ |
| Position Y | 312px | 312px | ✅ |
| Width | 432px | 432px | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | mixed | mixed | ✅ |

#### text: Other Event Type
**ID:** `text-1767674066622-598`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 560px | 560px | ✅ |
| Position Y | 328px | 328px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | horizontal | horizontal | ✅ |

#### number: Number of Attendees
**ID:** `number-1767674256283-437`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 104px | 104px | ✅ |
| Position Y | 409.9687601490329px | 409.9687601490329px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

#### text: Company Name
**ID:** `text-1767674620568-93`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 104px | 104px | ✅ |
| Position Y | 515.98592353139px | 515.98592353139px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

#### checkbox: Dietary Requirements
**ID:** `checkbox-1767675026709-266`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 104px | 104px | ✅ |
| Position Y | 616px | 616px | ✅ |
| Width | 413px | 413px | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | mixed | mixed | ✅ |

#### textarea: Allergy Information
**ID:** `textarea-1767675464207-854`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1144px | 1144px | ✅ |
| Position Y | 178px | 178px | ✅ |
| Width | 460px | 460px | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 232px | 232px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

**Style Overrides:** `inputHeight`

#### textarea: Special Requests
**ID:** `textarea-1767675969454-162`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1144px | 1144px | ✅ |
| Position Y | 475.66668701171875px | 475.66668701171875px | ✅ |
| Width | 461px | 461px | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 200px | 200px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

**Style Overrides:** `inputHeight`

#### date: Preferred Event Date
**ID:** `date-1767676188423-906`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1143px | 1143px | ✅ |
| Position Y | 747px | 747px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

#### terms: I agree to the
**ID:** `terms-1767676429052-134`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1145px | 1145px | ✅ |
| Position Y | 869px | 869px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | horizontal | horizontal | ✅ |

#### submit-button: 
**ID:** `submit-button-1767676594487-817`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1141px | 1141px | ✅ |
| Position Y | 901px | 901px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

#### radio: Radio Group
**ID:** `radio-1767746968234-637`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 616px | 616px | ✅ |
| Position Y | 384px | 384px | ✅ |
| Width | 331px | 331px | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 28px | 28px | ✅ |
| Border Width | 1px | 1px | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | mixed | mixed | ✅ |

### Form 44: Template D - Detailed Styles


#### radio: Customer Type
**ID:** `radio-1768184158033-653`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 100px | 100px | ✅ |
| Position Y | 129.03361160213888px | 129.03361160213888px | ✅ |
| Width | 50% | 50% | ✅ |
| Label Font ⚡ | Inter | Inter | ✅ |
| Label Size ⚡ | 16px | 16px | ✅ |
| Label Weight ⚡ | 600 | 600 | ✅ |
| Label Color ⚡ | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

**Style Overrides:** `labelFontSize, labelFontWeight`

#### text: Company Name
**ID:** `text-1768184324292-685`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 76px | 76px | ✅ |
| Position Y | 340.05443355362496px | 340.05443355362496px | ✅ |
| Width | 50% | 50% | ✅ |
| Label Font ⚡ | Roboto | Roboto | ✅ |
| Label Size ⚡ | 14px | 14px | ✅ |
| Label Weight ⚡ | 500 | 500 | ✅ |
| Label Color ⚡ | #0062ff | #0062ff | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | horizontal | horizontal | ✅ |

**Style Overrides:** `labelFontFamily, textBorderColor, textBorderWidth, textBorderRadius, labelColor`

#### dropdown: Overall Satisfaction Rating
**ID:** `dropdown-1768184661121-688`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 101px | 101px | ✅ |
| Position Y | 412px | 412px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font ⚡ | Inter | Inter | ✅ |
| Label Size ⚡ | 16px | 16px | ✅ |
| Label Weight ⚡ | 600 | 600 | ✅ |
| Label Color ⚡ | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

**Style Overrides:** `labelFontSize, labelFontWeight`

#### textarea: Reason for Your Rating
**ID:** `textarea-1768184906171-41`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 102px | 102px | ✅ |
| Position Y | 531px | 531px | ✅ |
| Width | 659px | 659px | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

**Style Overrides:** `inputHeight, helpTextColor`

#### radio: Would you recommend us to others?
**ID:** `radio-1768185353302-287`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 102px | 102px | ✅ |
| Position Y | 650px | 650px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font ⚡ | Inter | Inter | ✅ |
| Label Size ⚡ | 16px | 16px | ✅ |
| Label Weight ⚡ | 500 | 500 | ✅ |
| Label Color ⚡ | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

**Style Overrides:** `labelFontSize`

#### text: Referral Name
**ID:** `text-1768185546207-573`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 106px | 106px | ✅ |
| Position Y | 821px | 821px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | horizontal | horizontal | ✅ |

#### checkbox: How would you like us to contact you?
**ID:** `checkbox-1768185931071-664`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1033px | 1033px | ✅ |
| Position Y | 14px | 14px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

#### email: Preferred Contact Email
**ID:** `email-1768186291859-525`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1036px | 1036px | ✅ |
| Position Y | 221.99999856049158px | 221.99999856049158px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | horizontal | horizontal | ✅ |

**Style Overrides:** `textBorderColor, textBorderWidth, textBorderRadius`

#### phone: Preferred Contact Phone
**ID:** `phone-1768186518005-100`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1039px | 1039px | ✅ |
| Position Y | 272px | 272px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | horizontal | horizontal | ✅ |

#### textarea: Additional Comments
**ID:** `textarea-1768187698024-896`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1038px | 1038px | ✅ |
| Position Y | 330px | 330px | ✅ |
| Width | 466px | 466px | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 110px | 110px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

**Style Overrides:** `inputHeight`

#### divider: 
**ID:** `divider-1768193339825-556`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1000px | 1000px | ✅ |
| Position Y | 537px | 537px | ✅ |
| Width | 253px | 253px | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

#### terms: I agree to the
**ID:** `terms-1768193587614-223`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1042px | 1042px | ✅ |
| Position Y | 563px | 563px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

#### submit-button: 
**ID:** `submit-button-1768193776622-609`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1043px | 1043px | ✅ |
| Position Y | 663px | 663px | ✅ |
| Width | 100% | 100% | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

#### date: Select Date
**ID:** `date-1768470069246-312`

| Property | Builder | Preview | Match |
|----------|---------|---------|-------|
| Position X | 1040px | 1040px | ✅ |
| Position Y | 760px | 760px | ✅ |
| Width | Auto | Auto | ✅ |
| Label Font | Inter | Inter | ✅ |
| Label Size | 14px | 14px | ✅ |
| Label Weight | 500 | 500 | ✅ |
| Label Color | #374151 | #374151 | ✅ |
| Input Font | Inter | Inter | ✅ |
| Input Size | 14px | 14px | ✅ |
| Input Color | #1F2937 | #1F2937 | ✅ |
| Input Height | 40px | 40px | ✅ |
| Border Width | 0 | 0 | ✅ |
| Border Color | #D1D5DB | #D1D5DB | ✅ |
| Border Radius | 6px | 6px | ✅ |
| Padding X | 12px | 12px | ✅ |
| Padding Y | 8px | 8px | ✅ |
| Label Gap | 8px | 8px | ✅ |
| Input-Help Gap | 4px | 4px | ✅ |
| Object Layout | vertical | vertical | ✅ |

---

## Global Styles Comparison


### Form 41: Template C

| Property | Value | Builder | Preview | Match |
|----------|-------|---------|---------|-------|
| actionBackgroundColor | #0055FF | ✓ | ✓ | ✅ |
| actionBorderRadius | 6 | ✓ | ✓ | ✅ |
| actionFontFamily | Inter | ✓ | ✓ | ✅ |
| actionFontSize | 14 | ✓ | ✓ | ✅ |
| actionFontStyle | normal | ✓ | ✓ | ✅ |
| actionFontWeight | 500 | ✓ | ✓ | ✅ |
| actionTextColor | #FFFFFF | ✓ | ✓ | ✅ |
| backgroundColor | #FFFFFF | ✓ | ✓ | ✅ |
| baseSpacing | 8 | ✓ | ✓ | ✅ |
| borderColor | #D1D5DB | ✓ | ✓ | ✅ |
| borderRadius | 6 | ✓ | ✓ | ✅ |
| borderWidth | 1 | ✓ | ✓ | ✅ |
| defaultLayout | vertical | ✓ | ✓ | ✅ |
| defaultObjectLayout | vertical | ✓ | ✓ | ✅ |
| dividerBorderColor | #E5E7EB | ✓ | ✓ | ✅ |
| dividerBorderWidth | 1 | ✓ | ✓ | ✅ |
| dividerWidth | 380px | ✓ | ✓ | ✅ |
| errorColor | #DC2626 | ✓ | ✓ | ✅ |
| fontFamily | Inter | ✓ | ✓ | ✅ |
| fontSize | 14 | ✓ | ✓ | ✅ |
| fontStyle | normal | ✓ | ✓ | ✅ |
| fontWeight | 400 | ✓ | ✓ | ✅ |
| helpTextColor | #DC2626 | ✓ | ✓ | ✅ |
| helpTextFontFamily | Inter | ✓ | ✓ | ✅ |
| helpTextFontSize | 12 | ✓ | ✓ | ✅ |
| helpTextFontStyle | normal | ✓ | ✓ | ✅ |
| helpTextFontWeight | 400 | ✓ | ✓ | ✅ |
| helpTextHasBorder | false | ✓ | ✓ | ✅ |
| inputHeight | 28 | ✓ | ✓ | ✅ |
| inputHelpGap | 0.5 | ✓ | ✓ | ✅ |
| inputPaddingX | 1.5 | ✓ | ✓ | ✅ |
| inputPaddingY | 1 | ✓ | ✓ | ✅ |
| labelColor | #374151 | ✓ | ✓ | ✅ |
| labelFontFamily | Inter | ✓ | ✓ | ✅ |
| labelFontSize | 14 | ✓ | ✓ | ✅ |
| labelFontStyle | normal | ✓ | ✓ | ✅ |
| labelFontWeight | 500 | ✓ | ✓ | ✅ |
| labelGap | 1 | ✓ | ✓ | ✅ |
| labelHasBorder | false | ✓ | ✓ | ✅ |
| placeholderColor | #9CA3AF | ✓ | ✓ | ✅ |
| primaryColor | #0055FF | ✓ | ✓ | ✅ |
| textBackgroundColor | #FFFFFF | ✓ | ✓ | ✅ |
| textBorderColor | #D1D5DB | ✓ | ✓ | ✅ |
| textBorderRadius | 4 | ✓ | ✓ | ✅ |
| textBorderWidth | 1 | ✓ | ✓ | ✅ |
| textColor | #1F2937 | ✓ | ✓ | ✅ |
| textHasBorder | true | ✓ | ✓ | ✅ |

### Form 44: Template D

| Property | Value | Builder | Preview | Match |
|----------|-------|---------|---------|-------|
| actionBackgroundColor | #0055FF | ✓ | ✓ | ✅ |
| actionBorderRadius | 6 | ✓ | ✓ | ✅ |
| actionFontFamily | Inter | ✓ | ✓ | ✅ |
| actionFontSize | 14 | ✓ | ✓ | ✅ |
| actionFontStyle | normal | ✓ | ✓ | ✅ |
| actionFontWeight | 500 | ✓ | ✓ | ✅ |
| actionTextColor | #FFFFFF | ✓ | ✓ | ✅ |
| backgroundColor | #FFFFFF | ✓ | ✓ | ✅ |
| baseSpacing | 8 | ✓ | ✓ | ✅ |
| borderColor | #D1D5DB | ✓ | ✓ | ✅ |
| borderRadius | 6 | ✓ | ✓ | ✅ |
| borderWidth | 1 | ✓ | ✓ | ✅ |
| defaultLayout | vertical | ✓ | ✓ | ✅ |
| defaultObjectLayout | vertical | ✓ | ✓ | ✅ |
| dividerBorderColor | #E5E7EB | ✓ | ✓ | ✅ |
| dividerBorderWidth | 1 | ✓ | ✓ | ✅ |
| dividerWidth | 380px | ✓ | ✓ | ✅ |
| errorColor | #DC2626 | ✓ | ✓ | ✅ |
| fontFamily | Inter | ✓ | ✓ | ✅ |
| fontSize | 14 | ✓ | ✓ | ✅ |
| fontStyle | normal | ✓ | ✓ | ✅ |
| fontWeight | 400 | ✓ | ✓ | ✅ |
| helpTextColor | #DC2626 | ✓ | ✓ | ✅ |
| helpTextFontFamily | Inter | ✓ | ✓ | ✅ |
| helpTextFontSize | 12 | ✓ | ✓ | ✅ |
| helpTextFontStyle | normal | ✓ | ✓ | ✅ |
| helpTextFontWeight | 400 | ✓ | ✓ | ✅ |
| helpTextHasBorder | false | ✓ | ✓ | ✅ |
| inputHeight | 40 | ✓ | ✓ | ✅ |
| inputHelpGap | 0.5 | ✓ | ✓ | ✅ |
| inputPaddingX | 1.5 | ✓ | ✓ | ✅ |
| inputPaddingY | 1 | ✓ | ✓ | ✅ |
| labelColor | #374151 | ✓ | ✓ | ✅ |
| labelFontFamily | Inter | ✓ | ✓ | ✅ |
| labelFontSize | 14 | ✓ | ✓ | ✅ |
| labelFontStyle | normal | ✓ | ✓ | ✅ |
| labelFontWeight | 500 | ✓ | ✓ | ✅ |
| labelGap | 1 | ✓ | ✓ | ✅ |
| labelHasBorder | false | ✓ | ✓ | ✅ |
| objectColumnGapPx | 8 | ✓ | ✓ | ✅ |
| objectRowGapPx | 0 | ✓ | ✓ | ✅ |
| placeholderColor | #9CA3AF | ✓ | ✓ | ✅ |
| primaryColor | #0055FF | ✓ | ✓ | ✅ |
| textBackgroundColor | #FFFFFF | ✓ | ✓ | ✅ |
| textColor | #1F2937 | ✓ | ✓ | ✅ |
| textHasBorder | false | ✓ | ✓ | ✅ |

---

## Conclusion

All computed styles match between Builder and Preview because both use:

1. Same `UniversalFieldShell` component
2. Same `computeFieldStyles()` function
3. Same form definition as source of truth

**WYSIWYG Status: ✅ Verified**