
import {test, expect} from '../playwright/fixtures';
import path from 'path';

const FOLDER = 'test folder'
const FILE = 'test.pdf'
const PATH = path.join(__dirname, FILE)

test('Create folder', async ({files_index_page, page}) => {
    await files_index_page.create_folder(FOLDER)
    await expect(page.getByTestId('inode-title')).toContainText(FOLDER);
})

test('Upload file', async ({files_index_page, page}) => {
    await files_index_page.upload_file(PATH)
    await expect(page.getByTestId('inode-title')).toContainText(FILE);
})

test('Upload file in folder', async ({files_index_page, page}) => {
    // Create folder and navigate to it
    await files_index_page.create_folder(FOLDER)
    await page.getByTestId('inode-title').click()
    await expect(page.getByTestId('title')).toContainText(FOLDER)

    // Upload file
    await files_index_page.upload_file(PATH)
    await expect(page.getByTestId('inode-title')).toContainText(FILE);
})

test('Edit file', async ({files_index_page, page}) => {
    const name = "New name"
    await files_index_page.upload_file(PATH)
    await page.getByTestId('inode-actions-toggle').click()
    await page.getByTestId('edit-inode').click()

    await page.getByTestId('inode-name-input').fill(name)
    await page.getByTestId('change-inode-name').click()

    await files_index_page.goto()
    await expect(page.getByTestId('inode-title')).toContainText(name);
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
