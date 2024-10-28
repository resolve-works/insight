import { test as base, expect } from '../playwright';
import { FileIndexPage } from '../playwright/fixtures';

export const test = base.extend<{ folder_detail_page: FileIndexPage }>({
	folder_detail_page: async ({ file_index_page, page }, use) => {
		await file_index_page.create_folder();
		await page.getByTestId('inode-title').click();

		const folder_detail_page = new FileIndexPage(page);
		await use(folder_detail_page);
	}
});

test('Upload file in folder', async ({ folder_detail_page, page }) => {
	// Create folder and navigate to it
	await expect(page.getByTestId('title')).toContainText(folder_detail_page.FOLDER);

	// Upload file
	await folder_detail_page.upload_file();
	await expect(page.getByTestId('inode-title')).toHaveCount(1);
});
