import { test as base } from '@playwright/test';

type FixtureContext = {
    // Add specific contexts here later like 'seedUser'
};

export const test = base.extend<FixtureContext>({
    // Add fixtures here following the pure function -> fixture wrapper pattern
});

export { expect } from '@playwright/test';