import { test as base } from '../../playwright';
import { FileIndexPage } from '../../playwright/fixtures';

export * from '@playwright/test';

type Fixtures = {
	folder_detail_page: FileIndexPage;
};

export const test = base.extend<Fixtures>({
	folder_detail_page: async ({ file_index_page, page }, use) => {
		const folder = 'folder_detail';
		// Create folder and get the link for it
		const folder_path = await file_index_page.create_folder(folder);

		// Create new index page for folder
		const folder_detail_page = new FileIndexPage(page, folder_path);
		await use(folder_detail_page);
	}
});
