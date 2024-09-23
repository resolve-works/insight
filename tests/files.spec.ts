
import {test, expect} from '../playwright/fixtures';
import path from 'path';

const FOLDER = 'test folder'
const FILE = 'test.pdf'

test('Creates folders', async ({files_index_page, page}) => {
    await files_index_page.create_folder(FOLDER)
    await expect(page.getByTestId('inode-title')).toContainText(FOLDER);
})

test('Uploads files', async ({files_index_page, page}) => {
    await files_index_page.upload_file(path.join(__dirname, FILE))
    await expect(page.getByTestId('inode-title')).toContainText(FILE);
})

/*
const files_detail = files_index.extend({
    page: async ({page}, use) => {
        await page.locator('header').filter({hasText: FILE}).getByRole('button').click();
        await page.getByRole('link', {name: 'Split'}).click();
        await use(page)
    }
})

files_detail('validates form', async ({page}) => {
    await page.getByPlaceholder('Document name').fill('new.pdf');
    await page.getByRole('button', {name: 'Create'}).click();

    await expect(page.getByText('Number must be greater than')).toHaveCount(2)
})

files_detail('creates new splits', async ({page}) => {
    await page.getByPlaceholder('Document name').fill('new.pdf');
    await page.getByPlaceholder('1').fill('3');
    await page.getByPlaceholder('6').fill('6');
    await page.getByRole('button', {name: 'Create'}).click();

    await expect(page.getByRole('link', {name: 'pdf'})).toHaveCount(2);
    await expect(page.getByRole('progressbar')).toHaveCount(0, {timeout: 10000});
});
*/
