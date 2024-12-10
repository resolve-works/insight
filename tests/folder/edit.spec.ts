import { test, expect } from '.';
import { FileEditPage } from '../../playwright/fixtures';

test('marks_children_public', async ({ folder_detail_page, page }) => {
	// Upload file
	await folder_detail_page.goto();
	const file_path = await folder_detail_page.upload_file();

	// Go to folder edit page & set public
	const folder_edit_page = new FileEditPage(page, folder_detail_page.path + '/edit');
	await folder_edit_page.goto();
	await folder_edit_page.update_public_state(true);

	// Go to file edit page to check public state
	await page.goto(file_path + '/edit');
	await expect(page.getByTestId('inode-is-public-input')).toBeChecked();
});

test('marks_self_public', async ({ folder_detail_page, page }) => {
	// Upload file
	await folder_detail_page.goto();
	const file_path = await folder_detail_page.upload_file();

	// Go to file edit page & set public
	const file_edit_page = new FileEditPage(page, file_path + '/edit');
	await file_edit_page.goto();
	await file_edit_page.update_public_state(true);

	// Go to folder edit page to check public state
	await page.goto(folder_detail_page.path + '/edit');
	await expect(page.getByTestId('inode-is-public-input')).toBeChecked();
});

test('marks_self_private_after_unpublish', async ({ folder_detail_page, page }) => {
	// Upload files
	await folder_detail_page.goto();
	const first_file_path = await folder_detail_page.upload_file();
	const second_file_path = await folder_detail_page.upload_file('test(0).pdf');

	// Set folder to be public
	const folder_edit_page = new FileEditPage(page, folder_detail_page.path + '/edit');
	await folder_edit_page.goto();
	await folder_edit_page.update_public_state(true);

	// Mark first file private
	const first_file_edit_page = new FileEditPage(page, first_file_path + '/edit');
	await first_file_edit_page.goto();
	await first_file_edit_page.update_public_state(false);

	// Check folder public state
	await folder_edit_page.goto();
	await expect(page.getByTestId('inode-is-public-input')).toBeChecked();

	// Mark second file private
	const second_file_edit_page = new FileEditPage(page, second_file_path + '/edit');
	await second_file_edit_page.goto();
	await second_file_edit_page.update_public_state(false);

	// Go to folder edit page to check public state
	await folder_edit_page.goto();
	await expect(page.getByTestId('inode-is-public-input')).toBeChecked({ checked: false });
});

test('marks_self_private_after_delete', async ({ folder_detail_page, page }) => {
	// Upload file
	await folder_detail_page.goto();
	await folder_detail_page.upload_file();

	// Go to file edit page & set public
	const folder_edit_page = new FileEditPage(page, folder_detail_page.path + '/edit');
	await folder_edit_page.goto();
	await folder_edit_page.update_public_state(true);

	// Go back to folder and delete file
	await folder_detail_page.goto();
	await folder_detail_page.delete_file();

	// Go to folder edit and check public state
	await folder_edit_page.goto();
	await expect(page.getByTestId('inode-is-public-input')).toBeChecked({ checked: false });
});
