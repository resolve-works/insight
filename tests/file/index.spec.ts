import { test, expect } from '../../playwright';

test('create_folder', async ({ file_index_page }) => {
	await file_index_page.create_folder(file_index_page.FOLDER);
	const inode = file_index_page.get_inode(file_index_page.FOLDER);
	await expect(inode).toBeVisible();
});

test('error_on_duplicate_folder', async ({ file_index_page, page }) => {
	await file_index_page.create_folder();
	await file_index_page.create_folder();
	await expect(page.getByTestId('error-message')).toBeVisible();
});

test('upload_file', async ({ file_index_page }) => {
	await file_index_page.upload_file(file_index_page.FILE);
	const inode = file_index_page.get_inode(file_index_page.FILE);
	await expect(inode).toBeVisible();
});

test('error_on_duplicate_file', async ({ file_index_page, page }) => {
	await file_index_page.upload_file();
	await file_index_page.upload_file();
	// TODO - look for error message in upload
	await expect(page.getByTestId('error-message')).toBeVisible();
});

test('error_on_wrong_filetype', async ({ file_index_page }) => {
	const name = 'ccheart_red.svg';
	await file_index_page.upload_file(name);
	const inode = file_index_page.get_inode(name);
	await expect(inode.getByTestId('inode-error')).toHaveAttribute('title', 'unsupported_file_type');
});

test('error_on_corrupted_file', async ({ file_index_page }) => {
	const name = 'corrupted.pdf';
	await file_index_page.upload_file(name);
	const inode = file_index_page.get_inode(name);
	await expect(inode.getByTestId('inode-error')).toHaveAttribute('title', 'corrupted_file');
});

test('upload_special_characters', async ({ file_index_page }) => {
	const name = 'test(0).pdf';
	await file_index_page.upload_file(name);
	// Wait for processing to trigger first, then to finish
	const inode = file_index_page.get_inode(name);

	await expect(inode.getByTestId('inode-loader')).toBeVisible();
	await expect(inode.getByTestId('inode-loader')).not.toBeVisible();
});
