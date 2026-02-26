import { test, expect } from '../support/fixtures';
import { createUserData } from '../support/helpers/data-factories';

test.describe('Example E2E Flow', () => {
  test('user can access the home page - deterministic', async ({ page }) => {
    // Navigate without arbitrary timeouts
    await page.goto('/');

    // Check for a generic element that should be on the app (like a header or logo)
    // Replace this with actual data-testid based locators once known
    const rootElement = page.locator('#root');
    await expect(rootElement).toBeVisible();
    
    // Example: Network-first approach (if calling API on load)
    // const apiResponse = page.waitForResponse('**/api/config');
    // await page.goto('/');
    // await apiResponse;
  });

  test('example of data factory pattern', async ({}) => {
    // Using isolated, parallel-safe data
    const user = createUserData({ first_name: 'Custom' });
    expect(user.first_name).toBe('Custom');
    expect(user.email).toContain('@example.com');
  });
});
