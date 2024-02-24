import { test, expect } from '../playwright/fixtures';

test('has title', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Insight FOIA search' })).toBeVisible();
});
