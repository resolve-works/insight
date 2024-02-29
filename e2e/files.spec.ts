import path from 'path'
import { test, expect } from '../playwright/fixtures';

test('uploads files', async ({ page }) => {
    await page.goto('/files/');
    await page.locator('css=input[type=file]').setInputFiles(path.join(__dirname, 'test.pdf'));

    // Expect upload progress to show
    await expect(page.getByRole('progressbar')).toBeVisible();
    // Expect upload to be done and wait for ingest progress to be gone
    await expect(page.getByRole('link', { name: 'test.pdf' })).toBeVisible();
    await expect(page.getByRole('progressbar')).toHaveCount(0, { timeout: 10000 });
});

test('splits files', async ({ page }) => {
    await page.goto('/files/');
    await page.getByRole('link', { name: 'test.pdf' }).click();

    // Change first documents length
    await page.getByRole('spinbutton').nth(1).click();
    await page.getByRole('spinbutton').nth(1).fill('3');

    // Add a second document
    await page.getByRole('button', { name: 'Add split' }).click();
    await page.getByRole('spinbutton').nth(2).click();
    await page.getByRole('spinbutton').nth(2).fill('4');

    // Store & wait for processing
    await page.getByRole('button', { name: 'Store changes' }).click();
    await expect(page.getByRole('progressbar')).toHaveCount(0, { timeout: 10000 });
});
