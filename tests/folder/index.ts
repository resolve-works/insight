import { test as base, expect } from '../../playwright';
import { FileIndexPage, FileEditPage } from '../../playwright/fixtures';

export * from '@playwright/test';

type Fixtures = {
	folder_detail_page: FileIndexPage;
	folder_edit_page: FileEditPage;
};

export const test = base.extend<Fixtures>({
	folder_detail_page: async ({ file_index_page, page }, use) => {
		const folder = 'folder_detail';
		// Create folder and get the link for it
		await file_index_page.create_folder(folder);
		const href = await page
			.getByTestId('inode-link')
			.filter({ hasText: folder })
			.first()
			.getAttribute('href');

		expect(href).not.toBeNull();

		// Create new index page for folder
		const folder_detail_page = new FileIndexPage(page, href);
		await use(folder_detail_page);
	},

	folder_edit_page: async ({ page }, use) => {
		await use(new FileEditPage(page));
	}
});
