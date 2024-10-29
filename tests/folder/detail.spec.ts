import { test, expect } from '.';

test('Upload file in folder', async ({ folder_detail_page, page }) => {
	// Upload file
	await folder_detail_page.upload_file();
	await expect(page.getByTestId('inode-title')).toHaveCount(1);
});
