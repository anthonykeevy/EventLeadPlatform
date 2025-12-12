# Epic 3 Architecture Reference - The "Slim Renderer" & "Component Framework"

**Epic Goal:** Build a scalable, offline-first Form Builder and Renderer with a flexible Component Framework.

---

## 1. Core Architectural Concepts

### **A. Separation of Concerns: The Factory vs. The Player**
*   **The Builder (The Factory):**
    *   **Role:** A complex "Design Environment" (React).
    *   **Responsibility:** Loads the **Component Framework** (definitions, rules, defaults), allows the user to compose them, and compiles the result into a **DefinitionJSON**.
    *   **Intelligence:** High. Knows about Tenancy, Region-specific widgets, and validation logic.
*   **The Renderer (The Player):**
    *   **Role:** A lightweight "Runtime Engine" (React).
    *   **Responsibility:** Takes the **DefinitionJSON** and executes it.
    *   **Intelligence:** Low (Dumb). It does not "know" business rules; it just follows the instructions in the JSON (e.g., "Render Component X with Config Y").

### **B. The "Component Framework" (The Bricks)**
To support drag-and-drop, custom objects, and global styling without hardcoding everything, we use a **Registry-Based Architecture**.

1.  **The Component Registry (Code):**
    *   A map in the Frontend code linking a `type` string to a React Component.
    *   *Example:* `'text-input' -> <StandardInput />`, `'uk-postcode' -> <UKPostcodeLookup />`.
    *   **Extensibility:** New custom objects can be added to the registry and they automatically become renderable if the JSON requests them.
    *   **Complexity Handling:** The Registry abstracts complexity. A "Text Box" and a "Google Maps Address Lookup" are treated identically by the framework: they both receive a `config` object and return data. The internal complexity (API calls, state) is encapsulated within the component itself.

2.  **The Component Definition (Metadata):**
    *   Defines the *capabilities* of a component for the Builder.
    *   **Properties Schema:** A definition (Zod/JSON Schema) of what the user can edit in the Properties Panel.
    *   **Default Config:** The baseline settings (Global Defaults).

### **C. The "DefinitionJSON" (The Contract)**
The schema is the single source of truth. It is "compiled" by the Builder and stored in `FormVersion.DefinitionJSON`.
It is strictly validated by the backend using **Pydantic** before saving.

**Validation Layer:**
*   **Service:** `FormVersionService`
*   **Schema File:** `backend/schemas/form_definition.py`
*   **Enforcement:** Strict Type checking, Unique ID enforcement, `schemaVersion` check.

**Structure Strategy:**
*   **Global Theme:** Defines the CSS variables (Fonts, Colors, Spacing) at the root.
*   **Components Tree:** A flat or nested list of component instances.
*   **Resolved Props:** The Builder calculates the "Defaults + Overrides" and saves the *final* configuration for the Renderer.
*   **Serialization Limit:** Only serializable data (JSON) is stored. Custom logic must be registered as "Action Keys" (strings) in the registry, not raw code.

---

## 1.1 Property Handling (Story 3.5 - Properties Panel)

This section documents how **Global Styles**, **Component Overrides**, **Bulk Edit**, and **Undo/Redo** work together in the Builder.

### **A. Storage Model**
- **Form-level defaults:** `formDefinition.globalStyles`
- **Per-component overrides:** `component.props.styleOverrides`

### **B. Cascade / Resolution**
The Builder preview resolves effective styling at render time using the cascade:
\[
\text{effective} = \text{globalStyles} \;\;+\;\; \text{styleOverrides}
\]

- `undefined` means “no override; inherit global”.
- Certain values are intentionally explicit overrides, e.g. `backgroundColor: 'transparent'` means “force transparent”, not “unset”.

**Primary implementation:** `frontend/src/features/builder/utils/styleUtils.ts`

### **C. Reset-to-Global Semantics**
“Reset” clears overrides by removing the key (or setting to `undefined`), returning the component to inheritance.

In multi-select and bulk operations, the system merges patch updates into each selected component’s existing override object (so unrelated overrides are preserved).

**Primary implementation:** `frontend/src/features/builder/components/PropertiesPanel.tsx`

### **D. Multi-select Bulk Edit**
- Selection state is tracked as a primary selection plus a set:
  - `selectedComponentId` (primary)
  - `selectedComponentIds` (multi-select set)
- Ctrl+Click toggles membership in `selectedComponentIds` (add/remove).
- Bulk changes apply to all selected components via store helpers.

**Primary implementation:** `frontend/src/features/builder/stores/useBuilderStore.ts`

### **E. Undo/Redo Coverage**
Undo/redo stores bounded snapshots of the full `formDefinition` prior to significant user actions:
- Add component
- Move/resize/scale changes
- Single-component property edits
- Multi-select bulk edits
- Global style edits

**Primary implementation:** `frontend/src/features/builder/stores/useBuilderStore.ts`

---

## 1.2 Logic Rules (Story 3.6 - Conditional Logic UI)

Story 3.6 introduces **rule authoring + persistence** only. The **runtime evaluation engine** is explicitly deferred to **Story 3.7**.

### **A. DefinitionJSON Storage Model**
- Rules are persisted into the form definition as structured JSON:
  - `formDefinition.logic.rules: LogicRule[]`
- Each rule references components by their **stable component IDs** (`FormComponent.id`).

**Canonical Rule JSON Shape:**

```json
{
  "logic": {
    "rules": [
      {
        "id": "rule-<uuid>",
        "enabled": true,
        "name": "Optional user-friendly label",
        "when": {
          "sourceComponentId": "comp-2",
          "operator": "equals",
          "value": "Yes"
        },
        "then": {
          "targetComponentId": "comp-5",
          "action": "show"
        }
      }
    ]
  }
}
```

**Operators:**
- `equals`, `notEquals`, `contains`, `isEmpty`

**Actions:**
- `show` / `hide`
- `require` / `unrequire`
- `enable` / `disable`

**Serialization constraint (critical):**
- Only JSON-serializable data is stored (no functions/code).
- For `isEmpty`, `when.value` is omitted (or null) by convention.

### **B. Builder UI Patterns (Authoring UX)**
- The right panel supports a dedicated **Logic tab** alongside the Inspector.
- Rules are shown as a **scannable list** with a sentence-style summary (e.g., “If A equals X → Show B”).
- The Logic panel includes:
  - **Create / Edit / Delete**
  - **Enable/Disable**
  - **Reorder** via Move Up/Down (keyboard accessible)
  - Filters: **All / Enabled / With errors** + an **error count** badge

### **C. Validation & Guardrails (UI-time)**
- Prevent saving incomplete rules with clear inline messages.
- Block invalid rules:
  - Source field cannot equal target field
  - `contains` only available for text-capable fields
  - `isEmpty` does not accept a value
- If referenced components are deleted, rules remain persisted but surface **broken reference** errors for user correction.

### **D. Separation from the Runtime Engine (Story 3.7)**
- Story 3.6 does not apply rule effects to the builder canvas or renderer.
- Story 3.7 will interpret `logic.rules` and apply actions at runtime.

### **D. Drag-and-Drop Architecture (Story 3.3 & 3.4)**
The Visual Builder uses **@dnd-kit** for its accessible, robust drag-and-drop capabilities.

*   **State Management:** `useBuilderStore` (Zustand) holds the ephemeral state of the drag operation and the persistent state of the form structure.
*   **Interaction Behaviors (Updated Story 3.4):**
    *   **Viewport Scaling:** The Canvas uses CSS Transform (`scale`) to fit large layouts (1920x980) into the viewport.
    *   **Inverse-Scale Dragging:** Drag coordinates are divided by the `scale` factor to ensure mouse movements align 1:1 with component movement on the scaled canvas.
    *   **Lock on Drop:** Items are positioned absolutely (`x`, `y`).
    *   **Grid Snapping:** 8px magnetic grid logic is applied during `onDragEnd` if the grid is enabled.
    *   **Collision Prevention:** Invalid drops are rejected.
*   **Accessibility:** Fully supports keyboard reordering via `KeyboardSensor`.

### **E. Component Visual Structure (The "3-Part Standard")**
Every draggable Input Component must adhere to a standard visual structure to ensure consistency and usability:
1.  **Label Area (Top/Left):** For the field name/question.
2.  **Input Area (Middle):** The actual interactive element (box, dropdown, checkbox).
3.  **Validation Area (Bottom):** Reserved space for error messages/help text.

**Skyline Border (New):**
*   Components are wrapped in a `<SmartBorder>` component.
*   This uses `ResizeObserver` to generate a dynamic SVG path that "shrink-wraps" the 3 parts, creating a non-rectangular "Skyline" shape.
*   The SVG path serves as the draggable hitbox.

---

## 2. Database Architecture

### **Tables**

#### `FormVersion` (Implemented)
| Column | Type | Description |
|--------|------|-------------|
| `FormVersionID` | PK (BigInt) | Identity key |
| `FormID` | FK (BigInt) | Link to existing Form table |
| `VersionNumber` | Int | 1, 2, 3... |
| `DefinitionJSON` | NVARCHAR(MAX) | The full "Compiled" Schema |
| `VersionComment` | NVARCHAR(500) | User comment for version history |
| `Status` | String(20) | DRAFT, PUBLISHED, ARCHIVED |
| `IsActive` | Boolean | Flag for currently live version |
| `CreatedDate` | DateTime | |
| `CreatedBy` | FK (BigInt) | UserID |
| `PublishedDate` | DateTime | |
| `PublishedBy` | FK (BigInt) | UserID |

#### `FormSubmission` (Planned)
| Column | Type | Description |
|--------|------|-------------|
| `SubmissionID` | PK (UUID) | UUID for offline sync |
| `FormVersionID` | FK (Int) | Link to the specific schema version used |
| `DataJSON` | NVARCHAR(MAX) | The raw answers |
| `SubmittedAt` | DateTime | Server time |

---

## 3. "Offline-First" Strategy

1.  **Service Worker:** Caches the "Slim Renderer" app shell.
2.  **Schema Caching:** The specific `DefinitionJSON` for a form is fetched and cached in `localStorage`/`IndexedDB`.
3.  **Submission:**
    *   **Online:** POST directly to API.
    *   **Offline:** Save to `IndexedDB` (Outbox).
    *   **Sync:** Service Worker pushes Outbox to API when connectivity returns.

---

## 4. Scalability Strategy

*   **Async Submission:** `POST /submit` -> **Message Queue** (RabbitMQ/Service Bus) -> `202 Accepted`.
*   **Workers:** Consume queue -> Validate -> Insert into SQL.

---

## 5. Domain Breakdown (Updated)

### **Domain 1: Schema & Versioning**
*   Story 3.1: Form Versioning Architecture (Backend SQL + JSON Storage)
*   Story 3.2: JSON Schema Definition (The Contract Structure)

### **Domain 2: The Framework & Builder**
*   Story 3.3: Component Registry Foundation (The "Factory" Logic & Complexity Handling)
*   Story 3.4: Component Library & Layout (Toolbox, Scalable Canvas, Skyline Borders)
*   Story 3.5: Properties Panel & Configuration (Global vs Individual Settings, Layout Toggles)

### **Domain 3: Logic Engine**
*   Story 3.6: Conditional Logic UI
*   Story 3.7: Rule Evaluation Engine

### **Domain 4: Rendering & Submission**
*   Story 3.8: Public Form Renderer (The "Player")
*   Story 3.9: Async Submission Pipeline
