
import {test, expect} from '../playwright';

test('Create folder', async ({file_index_page, page}) => {
    await file_index_page.create_folder()
    await expect(page.getByTestId('inode-title')).toHaveCount(1)
})

test('Upload file', async ({file_index_page, page}) => {
    await file_index_page.upload_file()
    await expect(page.getByTestId('inode-title')).toHaveCount(1)
})

