
import { uploads_index, expect, FILENAME } from '../playwright/fixtures'

const documents_edit = uploads_index.extend({
    page: async ({ page }, use) => {
        await page.locator('header').filter({ hasText: FILENAME }).getByRole('button').click();
        await page.getByRole('link', { name: 'Edit' }).click();
        await expect(page.getByRole('heading', { name: 'Edit "test.pdf"' })).toHaveCount(1)
        await use(page)
    }
})

documents_edit('updates name', async ({ page }) => {
    // change name
    await page.getByPlaceholder('Document name').fill('new.pdf');
    await page.getByRole('button', { name: 'Change name' }).click();
    await expect(page.getByRole('progressbar')).toHaveCount(0, { timeout: 3000 });

    // Check document index
    await page.getByRole('link', { name: 'Documents', exact: true }).click()
    await expect(page.getByRole('link', { name: 'new.pdf' })).toHaveCount(1);
})

documents_edit('updates pagerange', async ({ page }) => {
    // Check validation
    await page.getByPlaceholder('1').fill('');
    await page.getByRole('button', { name: 'Update split' }).click();
    await expect(page.getByText('Number must be greater than')).toHaveCount(1)

    // Update range
    await page.getByPlaceholder('1').fill('2');
    await page.getByPlaceholder('6').fill('3');
    await page.getByRole('button', { name: 'Update split' }).click();
    await expect(page.getByRole('progressbar')).toHaveCount(0, { timeout: 3000 });

    await expect(page.getByRole('heading', { name: 'Split file' })).toHaveCount(1)
    await expect(page.getByPlaceholder('1')).toHaveValue('2')
    await expect(page.getByPlaceholder('6')).toHaveValue('3')
})
