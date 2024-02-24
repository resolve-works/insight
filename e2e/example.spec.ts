import path from 'path'
import { test, expect } from '../playwright/fixtures';

test('has heading', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Search documents' })).toBeVisible();
});

test('uploads files', async ({ page }) => {
    await page.goto('/files');
    await page.locator('css=input[type=file]').setInputFiles(path.join(__dirname, 'test.pdf'));

    // Expect upload progress to show
    await expect(page.getByRole('progressbar')).toBeVisible();
    // Expect upload to be done and wait for ingest progress to be gone
    await expect(page.getByRole('link', { name: 'test.pdf' })).toBeVisible();
    await expect(page.getByRole('progressbar')).toHaveCount(0, { timeout: 10000 });
});
