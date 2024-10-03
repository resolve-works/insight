
import {test, expect} from '../playwright';
import path from 'path';

test('Create folder', async ({file_index_page, page}) => {
    await file_index_page.create_folder()
    await expect(page.getByTestId('inode-title')).toHaveCount(1)
})

test('Upload file', async ({file_index_page, page}) => {
    await file_index_page.upload_file()
    await expect(page.getByTestId('inode-title')).toHaveCount(1)
})

test('Upload wrong file type', async ({file_index_page, page}) => {
    await file_index_page.upload_file(path.join(__dirname, 'file_index.spec.ts'))
    await expect(page.getByTestId('inode-error')).toHaveAttribute('title', 'unsupported_file_type')
})

test('Upload corrupted file', async ({file_index_page, page}) => {
    await file_index_page.upload_file(path.join(__dirname, 'corrupted.pdf'))
    await expect(page.getByTestId('inode-error')).toHaveAttribute('title', 'corrupted_file')
})

test('Upload special characters file', async ({file_index_page, page}) => {
    await file_index_page.upload_file(path.join(__dirname, 'test\(0\).pdf'))
    // Wait for processing to trigger first, then to finish
    await expect(page.getByTestId('inode-loader')).toHaveCount(1);
    await expect(page.getByTestId('inode-loader')).toHaveCount(0);
})

test('Upload same file twice', async ({file_index_page, page}) => {
    await file_index_page.upload_file()
    await file_index_page.upload_file()
    await expect(page.getByTestId('upload-error')).toHaveCount(1);
})
