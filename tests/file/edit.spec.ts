import { test as base, expect } from '../../playwright';
import { FileEditPage } from '../../playwright/fixtures';

export const test = base.extend<{ file_edit_page: FileEditPage }>({
	file_edit_page: async ({ file_index_page, page }, use) => {
		const file_path = await file_index_page.upload_file();
		const file_edit_page = new FileEditPage(page, file_path + '/edit');
		await file_edit_page.goto();
		await use(file_edit_page);
	}
});

// TODO - edit page
test('edit_file', async ({ file_edit_page, page }) => {
	const name = 'New name';
	await file_edit_page.update_name(name);
	await expect(page.getByTestId('title')).toContainText(name);
});

test('error_on_empty_filename', async ({ file_edit_page, page }) => {
	await file_edit_page.update_name('');
	await expect(page.getByTestId('error-message')).toContainText('must contain at least 1');
});
