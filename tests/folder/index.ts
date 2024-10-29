import { test as base, expect } from '../../playwright';
import { FileIndexPage, FileEditPage } from '../../playwright/fixtures';

export * from '@playwright/test';

type Fixtures = {
	folder_detail_page: FileIndexPage;
	folder_edit_page: FileEditPage;
};

export const test = base.extend<Fixtures>({
	folder_detail_page: async ({ file_index_page, page }, use) => {
		// Create folder and navigate to it
		await file_index_page.create_folder();
		await page.getByTestId('inode-title').click();
		await expect(page.getByTestId('title')).toContainText(file_index_page.FOLDER);

		// Use it as a index page
		const folder_detail_page = new FileIndexPage(page);
		await use(folder_detail_page);
	},

	folder_edit_page: async ({ page }, use) => {
		await use(new FileEditPage(page));
	}
});
