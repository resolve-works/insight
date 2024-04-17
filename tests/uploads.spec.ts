
import { uploads_index, expect, FILENAME } from '../playwright/fixtures';

uploads_index('uploads files', async ({ page }) => {
    await expect(page.getByRole('link', { name: FILENAME })).toBeVisible();
})

const uploads_detail = uploads_index.extend({
    page: async ({ page }, use) => {
        await page.locator('header').filter({ hasText: FILENAME }).getByRole('button').click();
        await page.getByRole('link', { name: 'Split' }).click();
        await use(page)
    }
})

uploads_detail('validates form', async ({ page }) => {
    await page.getByPlaceholder('Document name').fill('new.pdf');
    await page.getByRole('button', { name: 'Create' }).click();

    await expect(page.getByText('Number must be greater than')).toHaveCount(2)
})

uploads_detail('creates new splits', async ({ page }) => {
    await page.getByPlaceholder('Document name').fill('new.pdf');
    await page.getByPlaceholder('1').fill('3');
    await page.getByPlaceholder('6').fill('6');
    await page.getByRole('button', { name: 'Create' }).click();

    await expect(page.getByRole('link', { name: 'pdf' })).toHaveCount(2);
    await expect(page.getByRole('progressbar')).toHaveCount(0, { timeout: 10000 });
});

