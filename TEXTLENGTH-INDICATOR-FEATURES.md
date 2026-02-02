# TextLengthIndicator Feature Comparison

## Features Found and Implemented

### ✅ StandardInput Features (Toolbox)

1. **Text Length Indicator (Text)**
   - Shows: `~{maxLength} chars ({estimatedWidth}px)`
   - Position: Bottom-right corner
   - Status: ✅ Now working on canvas

2. **Green Bar Indicator**
   - Visual bar showing estimated width
   - Position: Bottom of input, spanning full width
   - Color: Green (`rgba(34, 197, 94, 0.6)`)
   - Status: ✅ Now working on canvas

3. **Line Estimate Badge (Textarea Only)**
   - Shows: `≈ {needed} lines for max length (fits ~{fits})`
   - Position: Bottom-right, above text indicator
   - Color coding:
     - Green background if `fits >= needed` (sufficient height)
     - White background if `fits < needed` (needs more height)
   - Status: ✅ Now implemented

### 📋 Implementation Details

#### Line Estimate Calculation (Textarea)

**Formula:**
```typescript
// Character width estimation
approximateCharWidth = fontSize * 0.55

// Usable width (accounting for padding and borders)
chromeWidth = (visualPaddingX + borderWidth) * 2
usableWidth = containerWidth - chromeWidth

// Characters per line
charsPerLine = floor(usableWidth / approximateCharWidth)

// Lines needed for maxLength
needed = ceil(maxLength / charsPerLine)

// Lines that fit in current height
lineHeight = fontSize * 1.4
fits = floor(textareaHeight / lineHeight)
```

**Visual Display:**
- Badge positioned at `bottom: 20px, right: 6px` (above text indicator)
- Font size: `fontSize - 2` (slightly smaller)
- Border radius: `6px`
- Padding: `2px 6px`
- Z-index: `15` (above green bar, below text indicator)

### 🔍 Other Component Features Checked

#### Select Component
- **Icon handling**: ✅ Already handled in renderer
- **Dropdown arrow**: ✅ Already rendered in `StyledSelect`
- **No special TextLengthIndicator features**: N/A (select doesn't use maxLength indicator)

#### Number Component
- **No special features**: Uses standard input renderer
- **TextLengthIndicator**: ✅ Works with default maxLength (12)

#### Email Component
- **No special features**: Uses standard input renderer
- **TextLengthIndicator**: ✅ Works with default maxLength (254)

#### Date Component
- **No special features**: Uses standard input renderer
- **TextLengthIndicator**: N/A (date inputs don't typically use maxLength)

#### Phone Component
- **No special features**: Uses standard input renderer
- **TextLengthIndicator**: ✅ Works with default maxLength (20)

### 📊 Feature Matrix

| Component Type | Text Indicator | Green Bar | Line Estimate | Special Features |
|----------------|----------------|-----------|---------------|------------------|
| **text** | ✅ | ✅ | ❌ | None |
| **textarea** | ✅ | ✅ | ✅ | Line estimate badge |
| **email** | ✅ | ✅ | ❌ | None |
| **number** | ✅ | ✅ | ❌ | None |
| **phone** | ✅ | ✅ | ❌ | None |
| **select** | ❌ | ❌ | ❌ | N/A (no maxLength) |
| **date** | ❌ | ❌ | ❌ | N/A (no maxLength) |

### 🎯 Status Summary

**All StandardInput TextLengthIndicator features are now implemented in UniversalFieldShell:**

1. ✅ Text portion (`~{maxLength} chars ({estimatedWidth}px)`)
2. ✅ Green bar indicator (visual width guide)
3. ✅ Line estimate badge for textarea (shows lines needed vs lines that fit)

### 🔧 Technical Implementation

**Files Modified:**
1. `frontend/src/features/builder/components/ui/TextLengthIndicator.tsx`
   - Added `lineEstimate` prop
   - Added `componentType` prop
   - Added line estimate badge rendering

2. `frontend/src/features/builder/utils/objectRenderers.tsx`
   - Added line estimate calculation for textarea
   - Passes `lineEstimate` and `componentType` to `TextLengthIndicator`

**Key Changes:**
- Line estimate only calculated in `builderMode`
- Line estimate only displayed for `textarea` component type
- Badge color coding matches StandardInput (green when sufficient, white when insufficient)
- Positioned above text indicator to avoid overlap

### 📝 Next Steps

1. ✅ TextLengthIndicator with green bar - **COMPLETE**
2. ✅ Line estimate for textarea - **COMPLETE**
3. ⏭️ Ready to implement Option 2 (Use UniversalFieldShell in Toolbox)






