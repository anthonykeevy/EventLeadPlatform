# EventLead Platform Test Architecture

This directory houses the unified end-to-end (E2E) testing framework for the EventLead Platform, powered by Playwright for browser interactions and Pytest for backend testing.

## Overview

The testing architecture follows the TEA (Test Architecture Enterprise) methodology, prioritizing determinism, isolation, speed, and explicit assertions.

### Principles

1. **Deterministic Execution:** No hard waits (`waitForTimeout`). Use explicit state checks or network interception (`waitForResponse`).
2. **Test Isolation:** Tests must not share state. Use data factories to generate unique entities (e.g., unique emails via Faker/Date-based generators).
3. **Fixture Composition:** Prefer `mergeTests` and isolated capability fixtures over monolithic inheritance structures (Page Object Models).
4. **Self-Cleaning:** If a test creates data, its associated fixture or teardown block must clean it up.

## Directory Structure

- `e2e/`: Core End-to-End browser tests written in Playwright.
- `support/fixtures/`: Playwright custom fixtures following pure function patterns (e.g., `api-request`, `auth`).
- `support/helpers/`: Utility functions and data factories (`data-factories.ts`).

## Setup & Execution

### Environment Variables
Copy `.env.example` to `.env` and configure:
- `BASE_URL`: The URL of the frontend (default: `http://localhost:5173`)
- `API_URL`: The URL of the backend API (default: `http://localhost:8000/api`)

### Running Tests (Playwright)

```bash
# Run all tests headlessly (CI mode)
npm run test:e2e

# Run tests with UI mode for debugging
npm run test:e2e -- --ui

# Run tests in a specific browser
npm run test:e2e -- --project=chromium

# Run tests in debug mode
npm run test:e2e -- --debug
```

### Running Tests (Pytest - Backend)

```bash
# From the /backend directory
pytest

# Run with coverage
pytest --cov

# Run specific integration tests
pytest -m integration
```

## Best Practices

- **Selectors:** Always prefer `data-testid` attributes (`page.getByTestId(...)`) over fragile CSS or XPath selectors.
- **Assertions:** Keep `expect()` statements explicit within the test body. Do not hide assertions inside helper functions.
- **Data Setup:** Utilize API requests within tests to seed data rapidly rather than navigating through the UI to create prerequisites.