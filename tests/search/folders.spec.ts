import type { Page } from '@playwright/test';
import { test as base, expect } from '../../playwright';
import { FileIndexPage } from '../../playwright/fixtures';

export * from '@playwright/test';

type Fixtures = {
	search_index_page: Page;
};

export const test = base.extend<Fixtures>({
	search_index_page: async ({ file_index_page, page }, use) => {
		// Create folders
		const folder_paths = [
			await file_index_page.create_folder('folder 1'),
			await file_index_page.create_folder('folder 2'),
			await file_index_page.create_folder('folder 3')
		];

		const folder_detail_pages = folder_paths.map(
			(folder_path) => new FileIndexPage(page, folder_path)
		);

		// Upload a file in every folder and wait for them to be indexed
		for (const folder_detail_page of folder_detail_pages) {
			await folder_detail_page.goto();
			await folder_detail_page.upload_file(folder_detail_page.FILE);
			const inode = folder_detail_page.get_inode(folder_detail_page.FILE);

			await expect(inode.getByTestId('inode-loader')).toBeVisible();
			await expect(inode.getByTestId('inode-loader')).not.toBeVisible();
		}

		await page.goto('/search');

		// Use it as a index page
		await use(page);
	}
});

test('load_folder_filter', async ({ search_index_page }) => {
	await expect(search_index_page.getByText('files found')).toBeVisible();
});
