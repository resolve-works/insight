
import { uploads_index, expect, FILENAME } from '../playwright/fixtures'

const documents_edit = uploads_index.extend({
    page: async ({ page }, use) => {
        await page.locator('header').filter({ hasText: FILENAME }).getByRole('button').click();
        await page.getByRole('link', { name: 'Edit' }).click();
        await expect(page.getByRole('heading', { name: 'Edit "test.pdf"' })).toHaveCount(1)
        await use(page)
    }
})

documents_edit('validates form', async ({ page }) => {
    await page.getByPlaceholder('1').click();
    await page.getByPlaceholder('1').fill('');
    await page.getByRole('button', { name: 'Update split' }).click();

    await expect(page.getByText('Number must be greater than')).toHaveCount(1)
})
