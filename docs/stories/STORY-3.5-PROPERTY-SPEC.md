# Story 3.5 Property Specification

**Purpose:** Define all controllable properties for the Properties Panel, their scope (Global vs. Individual), and the cascading behavior that enables enterprise-grade brand consistency.

---

## 🎯 Strategic Vision: "Brand DNA" System

### The Problem We're Solving
Marketing departments invest significant effort creating **Brand Guidelines** - precise specifications for colors, fonts, spacing, and visual identity. Currently, every new form requires manually recreating these settings, leading to:
- Inconsistent brand application
- Wasted time on repetitive configuration
- Frustration when onboarding new team members
- Difficulty maintaining standards across events

### The "Sticky" Solution
**One-Time Setup, Perpetual Value:**
1. **Company-Level Brand Profile** (Future: Story 3.X): Import or configure brand guidelines once per company.
2. **Form-Level Global Styles** (This Story): Set defaults that apply to all components in the form.
3. **Component-Level Overrides** (This Story): Fine-tune individual components when needed.

**Result:** Creating a new form takes seconds because the "Brand DNA" is already embedded. The detailed work is done **once**.

---

## 📊 Property Categories

### Category 1: Typography Properties

| Property | Type | Global | Individual | Default | Description |
|----------|------|:------:|:----------:|---------|-------------|
| `fontFamily` | Dropdown | ✅ | ✅ | Inter | Primary typeface |
| `fontSize` | Number (px) | ✅ | ✅ | 14 | Base text size |
| `fontWeight` | Dropdown | ✅ | ✅ | 400 | Normal, Medium, Bold |
| `lineHeight` | Number (ratio) | ✅ | ✅ | 1.5 | Line spacing multiplier |
| `letterSpacing` | Number (px) | ✅ | ✅ | 0 | Character spacing |
| `textTransform` | Dropdown | ✅ | ✅ | none | none, uppercase, capitalize |
| `labelFontSize` | Number (px) | ✅ | ✅ | 14 | Label-specific size |
| `labelFontWeight` | Dropdown | ✅ | ✅ | 500 | Label weight (often bolder) |
| `helpTextFontSize` | Number (px) | ✅ | ✅ | 12 | Help/validation text size |

---

### Category 2: Color Properties

| Property | Type | Global | Individual | Default | Description |
|----------|------|:------:|:----------:|---------|-------------|
| `primaryColor` | Color | ✅ | ✅ | #0055FF | Brand primary (buttons, focus) |
| `secondaryColor` | Color | ✅ | ❌ | #6B7280 | Secondary accents |
| `textColor` | Color | ✅ | ✅ | #1F2937 | Primary text |
| `labelColor` | Color | ✅ | ✅ | #374151 | Label text |
| `placeholderColor` | Color | ✅ | ✅ | #9CA3AF | Placeholder text |
| `helpTextColor` | Color | ✅ | ✅ | #6B7280 | Help/validation text |
| `errorColor` | Color | ✅ | ❌ | #DC2626 | Validation error |
| `successColor` | Color | ✅ | ❌ | #059669 | Success state |
| `backgroundColor` | Color | ✅ | ✅ | #FFFFFF | Input background |
| `borderColor` | Color | ✅ | ✅ | #D1D5DB | Input border |
| `focusBorderColor` | Color | ✅ | ✅ | {primaryColor} | Border on focus |

---

### Category 3: Spacing Properties (Critical for Consistency)

| Property | Type | Global | Individual | Default | Description |
|----------|------|:------:|:----------:|---------|-------------|
| `baseSpacing` | Number (px) | ✅ | ❌ | 8 | The "grid unit" all spacing derives from |
| `componentMargin` | Number (multiplier) | ✅ | ✅ | 2 | Margin between components (baseSpacing × 2 = 16px) |
| `labelGap` | Number (multiplier) | ✅ | ✅ | 1 | Gap between label and input (baseSpacing × 1 = 8px) |
| `inputPaddingX` | Number (multiplier) | ✅ | ✅ | 1.5 | Horizontal padding inside input (12px) |
| `inputPaddingY` | Number (multiplier) | ✅ | ✅ | 1 | Vertical padding inside input (8px) |
| `helpTextGap` | Number (multiplier) | ✅ | ✅ | 0.5 | Gap between input and help text (4px) |
| `sectionSpacing` | Number (multiplier) | ✅ | ❌ | 4 | Gap between form sections (32px) |

**Why Multipliers?**  
Using a base unit with multipliers ensures **proportional scaling**. Changing `baseSpacing` from 8 to 10 automatically scales all related spacing values, maintaining visual harmony.

---

### Category 4: Border & Shape Properties

| Property | Type | Global | Individual | Default | Description |
|----------|------|:------:|:----------:|---------|-------------|
| `borderRadius` | Number (px) | ✅ | ✅ | 6 | Corner rounding |
| `borderWidth` | Number (px) | ✅ | ✅ | 1 | Border thickness |
| `borderStyle` | Dropdown | ✅ | ✅ | solid | solid, dashed, none |
| `focusRingWidth` | Number (px) | ✅ | ❌ | 2 | Focus outline width |
| `focusRingOffset` | Number (px) | ✅ | ❌ | 2 | Focus ring gap from border |
| `shadowStyle` | Dropdown | ✅ | ✅ | none | none, subtle, medium, strong |

---

### Category 5: Sizing Properties

| Property | Type | Global | Individual | Default | Description |
|----------|------|:------:|:----------:|---------|-------------|
| `inputHeight` | Number (px) | ✅ | ✅ | 40 | Standard input height |
| `inputMinWidth` | Number (px) | ✅ | ✅ | 200 | Minimum input width |
| `inputMaxWidth` | Number (px) | ✅ | ✅ | 400 | Maximum input width |
| `labelWidth` | Number (px) | ❌ | ✅ | auto | Fixed label width (horizontal layout) |
| `componentScale` | Number (%) | ❌ | ✅ | 100 | Overall component scaling factor |

---

### Category 6: Layout Properties

| Property | Type | Global | Individual | Default | Description |
|----------|------|:------:|:----------:|---------|-------------|
| `layout` | Dropdown | ✅ | ✅ | vertical | vertical, horizontal |
| `labelAlign` | Dropdown | ✅ | ✅ | left | left, center, right |
| `inputAlign` | Dropdown | ✅ | ✅ | left | left, center, right |
| `requiredIndicator` | Dropdown | ✅ | ❌ | asterisk | asterisk, text, none |
| `requiredPosition` | Dropdown | ✅ | ❌ | after | before, after |

---

### Category 7: Behavior Properties (Component-Only)

| Property | Type | Global | Individual | Default | Description |
|----------|------|:------:|:----------:|---------|-------------|
| `label` | Text | ❌ | ✅ | "" | Field label text |
| `placeholder` | Text | ❌ | ✅ | "" | Input placeholder |
| `helpText` | Text | ❌ | ✅ | "" | Helper/description text |
| `required` | Boolean | ❌ | ✅ | false | Is field mandatory? |
| `disabled` | Boolean | ❌ | ✅ | false | Is field disabled? |
| `readOnly` | Boolean | ❌ | ✅ | false | Is field read-only? |
| `autoFocus` | Boolean | ❌ | ✅ | false | Focus on load? |

---

### Category 8: Validation Properties (Component-Only)

| Property | Type | Global | Individual | Default | Description |
|----------|------|:------:|:----------:|---------|-------------|
| `minLength` | Number | ❌ | ✅ | null | Minimum characters |
| `maxLength` | Number | ❌ | ✅ | null | Maximum characters |
| `pattern` | Regex | ❌ | ✅ | null | Regex validation pattern |
| `minValue` | Number | ❌ | ✅ | null | Minimum number value |
| `maxValue` | Number | ❌ | ✅ | null | Maximum number value |
| `customError` | Text | ❌ | ✅ | null | Custom error message |

---

## 🔄 Proportional Scaling Behavior

### The Question
> *"If a user is changing the size of a component, do we automatically increase the padding and font size for that object?"*

### The Answer: **Yes, with the Component Scale Factor**

When a user resizes a component using `componentScale`, the following properties scale proportionally:

| Property | Scaling Behavior |
|----------|------------------|
| `fontSize` | Scales proportionally |
| `labelFontSize` | Scales proportionally |
| `helpTextFontSize` | Scales proportionally |
| `inputPaddingX` | Scales proportionally |
| `inputPaddingY` | Scales proportionally |
| `labelGap` | Scales proportionally |
| `borderRadius` | Scales proportionally |
| `inputHeight` | Scales proportionally |

**Example:**
- Component at `100%` scale: fontSize=14, padding=12, height=40
- Component at `150%` scale: fontSize=21, padding=18, height=60

**Implementation Formula:**
```typescript
effectiveValue = baseValue * (componentScale / 100)
```

### Explicit Override
Users can always "break" proportional scaling by setting an explicit override on any individual property. The UI should show a warning: *"This property has been manually set and will not scale automatically."*

---

## 💾 Serialization Strategy

### Why This Matters
> *"I feel this approach will allow us to easily capture the properties so we can easily recreate that component when we deploy in production."*

All properties must be serializable to JSON for:
1. **Storage** in `FormVersion.DefinitionJSON`
2. **Transfer** to the Slim Renderer
3. **Export** for backup/migration
4. **API** responses

### The "Resolved Props" Pattern

**What We Store:**
```json
{
  "component": {
    "id": "field-123",
    "type": "text",
    "props": {
      "label": "First Name",
      "placeholder": "Enter your name",
      "required": true,
      "fontSize": null,        // null = use global
      "layout": "horizontal",  // explicit override
      "componentScale": 120    // 120% scale
    }
  }
}
```

**What the Renderer Receives (Resolved):**
```json
{
  "component": {
    "id": "field-123",
    "type": "text",
    "resolvedProps": {
      "label": "First Name",
      "placeholder": "Enter your name",
      "required": true,
      "fontSize": 16.8,         // 14 * 1.2 (scaled from global)
      "layout": "horizontal",
      "inputPaddingX": 14.4,    // 12 * 1.2 (scaled)
      "inputHeight": 48,        // 40 * 1.2 (scaled)
      "_scale": 1.2,
      "_isOverridden": ["layout"]
    }
  }
}
```

**Benefits:**
- Renderer is "dumb" - just applies resolved values
- Builder handles the complexity of cascading/scaling
- Easy to debug (what you see is what's stored)
- Portable across environments

---

## 🏢 Future: Company Brand Profile (Not in Story 3.5)

### The Vision
```
Company Brand Profile
         ↓ (imports defaults)
    Form Global Styles
         ↓ (cascades to)
   Component Properties
         ↓ (overrides as needed)
    Individual Values
```

### Brand Profile Fields (Future Reference)
| Field | Description |
|-------|-------------|
| `companyName` | For watermarks/footers |
| `primaryBrandColor` | Main brand color |
| `secondaryBrandColor` | Accent color |
| `brandFonts` | List of approved typefaces |
| `logoUrl` | Company logo for headers |
| `brandSpacingSystem` | 4px, 8px, or custom base |
| `defaultBorderRadius` | Brand corner style (sharp, rounded, pill) |

### Import Sources (Future)
- **Manual Entry:** Form-based configuration
- **Brand Guidelines PDF:** AI extraction (advanced)
- **Figma/Sketch Import:** Design tool integration
- **CSS Variables Import:** From existing stylesheets

---

## 📐 Professional Quality Expectations

This Properties Panel must reflect the **enterprise-grade** nature of the platform:

### Visual Polish
- **Clean, organized sections** with collapsible accordions
- **Consistent iconography** for property types
- **Subtle animations** on state changes
- **Clear visual hierarchy** (Global → Override indicators)

### Precision Controls
- **Number inputs with steppers** (+/- buttons)
- **Sliders for visual properties** (opacity, scale)
- **Color pickers with brand palette presets**
- **Live preview thumbnails** where appropriate

### Professional UX Patterns
- **Undo/Redo support** (Ctrl+Z, Ctrl+Y)
- **Reset to Default** at property and section level
- **"Apply to All"** batch operations
- **Copy/Paste styles** between components
- **Keyboard shortcuts** for power users

### Error Prevention
- **Validation on input** (prevent invalid values)
- **Range constraints** with helpful messages
- **Preview before commit** for dangerous operations
- **Confirmation dialogs** for destructive actions

---

## 📋 Story 3.5 Scope Summary

### In Scope (This Story)
| Category | Included Properties |
|----------|---------------------|
| Typography | fontFamily, fontSize, labelFontSize, helpTextFontSize |
| Colors | primaryColor, textColor, backgroundColor, borderColor |
| Spacing | baseSpacing, componentMargin, labelGap, inputPaddingX/Y |
| Borders | borderRadius, borderWidth |
| Sizing | inputHeight, componentScale |
| Layout | layout (vertical/horizontal), labelAlign |
| Behavior | label, placeholder, required, helpText |
| Validation | minLength, maxLength, pattern, customError |

### Out of Scope (Future Stories)
- Company Brand Profile integration
- Figma/design tool import
- AI-powered brand extraction
- Advanced copy/paste styles
- Full undo/redo history

---

*Property Specification for Story 3.5 - Properties Panel & Configuration*  
*Document Version: 1.0*  
*Created: 2025-11-30*

