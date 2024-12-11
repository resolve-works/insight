import { test, expect } from '../../playwright';
import { FileIndexPage } from '../../playwright/fixtures';

export * from '@playwright/test';

test('load_folder_filter', async ({ file_index_page, page }) => {
	// Create folders
	const folder_paths = [
		await file_index_page.create_folder('folder_1'),
		await file_index_page.create_folder('folder_2'),
		await file_index_page.create_folder('folder_3')
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

	const all_folders_response = await page.request.get(`/search/folders`);
	expect(all_folders_response.ok()).toBeTruthy();
	const all_folders = await all_folders_response.json();
	expect(all_folders.length).toBeGreaterThanOrEqual(3);

	const query_folders_response = await page.request.get(`/search/folders?query=folder_1`);
	expect(query_folders_response.ok()).toBeTruthy();
	const query_folders = await query_folders_response.json();
	expect(query_folders.length).toBeLessThan(all_folders.length);
});
