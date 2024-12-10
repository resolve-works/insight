import { test, expect } from '.';

test('Upload file in folder', async ({ folder_detail_page, page }) => {
	await folder_detail_page.goto();
	await folder_detail_page.upload_file();

	await expect(
		page.getByTestId('inode-title').filter({ hasText: folder_detail_page.FILE })
	).toHaveCount(1);
});
