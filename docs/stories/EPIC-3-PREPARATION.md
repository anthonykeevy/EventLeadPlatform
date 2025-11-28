# Epic 3 Preparation: Form Builder & Logic Engine

**Epic Goal:** Create a powerful, drag-and-drop Form Builder and a flexible Logic Engine to power dynamic forms.

## 1. Core Objectives
1.  **Visual Editor:** A WYSIWYG editor for users to build forms without code.
2.  **Schema Engine:** A robust JSON-based schema to store form definitions (questions, types, validation).
3.  **Logic Engine:** A rule engine to handle conditional visibility ("Show Question B if Question A is 'Yes'") and branching.
4.  **Renderer:** A high-performance frontend component to render forms from the schema.

## 2. Clarifications & Architectural Decisions (Based on User Feedback)

### **A. Schema Engine vs. Database Schema**
*   **Distinction:**
    *   **Database Schema (SQL):** This handles the *relational structure* (e.g., `Form`, `FormVersion`, `FormSubmission`). We will design this **upfront in Story 3.1** to ensure we have a place to store the JSON blobs.
    *   **Schema Engine (JSON):** This is the *content definition* stored inside a single column (e.g., `FormVersion.DefinitionJSON`). It tells the frontend *what* to render (e.g., "Question 1 is a Text Input").
*   **Why JSON?** Forms are highly dynamic. A relational table for every single question (e.g., `Question` table) becomes a nightmare for performance when fetching a complex form. Storing the entire form definition as a structured JSON blob allows for instant retrieval and rendering.

### **B. Offline-First Architecture**
*   **Requirement:** Forms must work offline and sync when online.
*   **Solution:**
    *   **Service Workers:** Use Progressive Web App (PWA) technologies to cache the "Slim Renderer" and the form definition.
    *   **IndexedDB:** Store collected leads locally in the browser's IndexedDB while offline.
    *   **Background Sync:** Use the Background Sync API to automatically upload stored leads when connectivity is restored.

### **C. Responsive Canvas & Normalization**
*   **Requirement:** Support diverse device sizes.
*   **Solution:**
    *   **Fluid Grid System:** The builder output will use a responsive grid (like CSS Grid/Flexbox) rather than absolute pixel positioning.
    *   **Preview Mode:** The builder will include a "Device Preview" toggle (Mobile, Tablet, Desktop) to verify layouts instantly.

### **D. Scalability & Queueing**
*   **Requirement:** Handle thousands of simultaneous forms and submission spikes.
*   **Solution:**
    *   **Async Submission:** The submission API (`POST /submit`) will essentially be a "producer".
    *   **Message Queue:** Submissions will be pushed to a queue (e.g., **RabbitMQ** or **Azure Service Bus**) for asynchronous processing.
    *   **Worker Consumers:** Separate worker services will pull from the queue to validate data and insert into the SQL database, preventing database lockups during spikes.

### **E. Build-Time vs. Run-Time Separation (The "Slim Renderer" Strategy)**
*   **Problem:** How to keep the hosted form lightweight and independent of the heavy Builder logic?
*   **Solution: "Schema-Driven Rendering"**
    *   **The Builder (Complex):** Contains drag-and-drop libraries, property editors, complex validation rules designers, and layout tools. It outputs a **JSON Schema**.
    *   **The Schema (The Contract):** A standard JSON file that describes the form:
        ```json
        {
          "title": "Lead Capture",
          "components": [
            { "type": "text", "label": "Name", "required": true },
            { "type": "email", "label": "Email" }
          ]
        }
        ```
    *   **The Renderer (Slim):** A tiny, highly-optimized React component (or even vanilla JS) that takes the JSON Schema as input and loops through it to render standard HTML elements.
    *   **Hosting:** When a customer "Publishes" a form, we don't deploy a new website. We just serve the **Slim Renderer App** and inject the specific **JSON Schema** for that form ID.
    *   **Benefit:** The renderer has zero knowledge of "dragging" or "editing". It only knows how to display an input field and check if it's empty. This keeps it incredibly fast and cacheable.

## 3. Technical Recommendations (From Epic 2 Retro)

### **A. Data Structure (JSON Schema)**
*   **Standard:** Adopt a modified version of **Formio.js** or **SurveyJS** schema standards, or define a custom strict schema using **Zod**.
*   **Storage:** Store form definitions in a `FormVersion` table (Versioning is critical from Day 1).
*   **Migration:** Ensure the schema allows for easy future migrations (e.g., adding new question types).

### **B. Frontend Architecture**
*   **State Management:** Use **Zustand** for the Form Builder state. It is lighter than Redux but more capable than React Context for frequent updates (drag-and-drop).
*   **Performance:** Use **React.memo** aggressively. Rendering a form with 100 fields can be slow if the entire tree re-renders on every keystroke.
*   **Libraries:** Evaluate **Dnd-kit** for drag-and-drop (accessible, modern) over older libraries like `react-beautiful-dnd`.

### **C. Backend Services**
*   **FormService:** Needs to expand to handle `FormVersion` management (Draft vs. Published versions).
*   **ValidationService:** The backend must be able to validate submissions against the schema *dynamically*. If the schema says "Field A is required", the backend must enforce it without hardcoded Pydantic models for every form.

## 4. Proposed Domain Breakdown

### **Domain 1: Schema & Versioning**
*   Story 3.1: Form Versioning Architecture (Backend SQL + JSON Storage)
*   Story 3.2: JSON Schema Definition & Validation

### **Domain 2: Visual Builder**
*   Story 3.3: Drag-and-Drop Canvas Foundation
*   Story 3.4: Question Component Library (Text, Select, Radio, etc.)
*   Story 3.5: Properties Panel (Editing Field Settings)

### **Domain 3: Logic Engine**
*   Story 3.6: Conditional Logic UI (Builder Side)
*   Story 3.7: Rule Evaluation Engine (Renderer Side)

### **Domain 4: Rendering & Submission (High Scale)**
*   Story 3.8: Public Form Renderer (PWA/Offline Support)
*   Story 3.9: Dynamic Submission Handling & Queue Integration

## 5. Immediate Next Steps
1.  Create `EPIC-3-STATUS.md`.
2.  Create `EPIC-3-WORKFLOW-GUIDE.md`.
3.  Begin Story 3.1 (Versioning Architecture).
