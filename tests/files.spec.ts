import path from 'path'
import { test, expect } from '../playwright/fixtures';

const FILENAME = 'test.pdf';

const with_upload = test.extend({
    page: async ({ page }, use) => {
        await page.goto('/uploads/');
        await page.locator('css=input[type=file]').setInputFiles(path.join(__dirname, FILENAME));

        // Expect upload progress to show
        await expect(page.getByRole('progressbar')).toBeVisible();
        // Expect upload to be done and wait for ingest progress to be gone
        await expect(page.getByRole('progressbar')).toHaveCount(0, { timeout: 10000 });

        await use(page)
    }
})

with_upload('splits files', async ({ page }) => {
    await page.getByRole('link', { name: FILENAME }).click();

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
