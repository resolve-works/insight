import { test, expect } from '../playwright/fixtures';

test('has heading', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Search documents' })).toBeVisible();
});
