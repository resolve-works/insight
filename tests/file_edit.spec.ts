import { test as base, expect } from '../playwright';
import { FileEditPage } from '../playwright/fixtures';

export const test = base.extend<{ file_edit_page: FileEditPage }>({
	file_edit_page: async ({ file_index_page, page }, use) => {
		await file_index_page.upload_file();
		await expect(page.getByTestId('inode')).toHaveCount(1);
		await page.getByTestId('inode-actions-toggle').click();
		await page.getByTestId('edit-inode').click();

		await use(new FileEditPage(page));
	}
});

// TODO - edit page
test('Edit file', async ({ file_edit_page, page }) => {
	const name = 'New name';
	await file_edit_page.update_name(name);
	await expect(page.getByTestId('title')).toContainText(name);
});

test('Edit no filename', async ({ file_edit_page, page }) => {
	await file_edit_page.update_name('');
	await expect(page.getByTestId('error-message')).toContainText('must contain at least 1');
});
