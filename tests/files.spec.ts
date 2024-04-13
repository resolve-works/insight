import path from 'path'
import { test, expect } from '../playwright/fixtures';

const FILENAME = 'test.pdf';

const uploads_index = test.extend({
    page: async ({ page }, use) => {
        await page.goto('/uploads/');
        await page.locator('css=input[type=file]').setInputFiles(path.join(__dirname, FILENAME));

        // Expect upload progress to show
        await expect(page.getByRole('progressbar')).toBeVisible();
        // Expect upload to be done and wait for ingest progress to be gone
        await expect(page.getByRole('progressbar')).toHaveCount(0, { timeout: 10000 });

        await use(page)

        await page.locator('header').filter({ hasText: FILENAME }).getByRole('button').click();
        await page.getByRole('button', { name: 'Delete' }).click();
    }
})

uploads_index('uploads files', async ({ page }) => {
    await expect(page.getByRole('link', { name: FILENAME })).toBeVisible();
})

/*
const uploads_detail = uploads_index.extend({
    page: async ({ page }, use) => {
        await page.getByRole('link', { name: FILENAME }).click();
        await page.getByRole('link', { name: 'Split' }).click();

        await use(page)

        await page.goto('/uploads/');
    }
})

uploads_detail('splits files', async ({ page }) => {
    await page.getByPlaceholder('6').click();
    await page.getByPlaceholder('6').fill('3');
    await page.getByRole('button', { name: 'Update split' }).click();

    await expect(page.getByRole('progressbar')).toHaveCount(0, { timeout: 10000 });
});
*/
