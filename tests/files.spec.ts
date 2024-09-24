
import {test, expect} from '../playwright';

test('Create folder', async ({files_index_page, page}) => {
    await files_index_page.create_folder()
    await expect(page.getByTestId('inode-title')).toContainText(files_index_page.FOLDER);
})

test('Upload file', async ({files_index_page, page}) => {
    await files_index_page.upload_file()
    await expect(page.getByTestId('inode-title')).toContainText(files_index_page.FILE);
})

test('Upload file in folder', async ({files_index_page, page}) => {
    // Create folder and navigate to it
    await files_index_page.create_folder()
    await page.getByTestId('inode-title').click()
    await expect(page.getByTestId('title')).toContainText(files_index_page.FOLDER)

    // Upload file
    await files_index_page.upload_file()
    await expect(page.getByTestId('inode-title')).toContainText(files_index_page.FILE);
})

test('Edit file', async ({files_index_page, page}) => {
    const name = "New name"
    await files_index_page.upload_file()
    await page.getByTestId('inode-actions-toggle').click()
    await page.getByTestId('edit-inode').click()

    await page.getByTestId('inode-name-input').fill(name)
    await page.getByTestId('change-inode-name').click()

    await files_index_page.goto()
    await expect(page.getByTestId('inode-title')).toContainText(name);
})
