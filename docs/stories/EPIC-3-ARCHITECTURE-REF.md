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
        *   *Simple:* Label, Required.
        *   *Complex:* API Keys, Region Restrictions, Map Styles.
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

**Example Schema:**
```json
{
  "formId": "uuid-123",
  "version": 1,
  "theme": {
    "primaryColor": "#0055FF",
    "fontFamily": "Inter"
  },
  "components": [
    {
      "id": "q1",
      "type": "text-input", 
      "props": {
        "label": "Full Name",
        "required": true,
        "style": { "width": "100%" } // Resolved style
      }
    },
    {
      "id": "q2",
      "type": "custom-agency-widget",
      "props": {
        "agencyId": "coca-cola",
        "mode": "dark",
        "apiKey": "enc_..." // Complex config stored simply
      }
    }
  ]
}
```

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
*   Story 3.4: Drag-and-Drop Canvas (The "Assembler")
*   Story 3.5: Properties Panel & Custom Object Support

### **Domain 3: Logic Engine**
*   Story 3.6: Conditional Logic UI
*   Story 3.7: Rule Evaluation Engine

### **Domain 4: Rendering & Submission**
*   Story 3.8: Public Form Renderer (The "Player")
*   Story 3.9: Async Submission Pipeline
