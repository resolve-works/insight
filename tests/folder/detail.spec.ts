import { test, expect } from '.';

test('file_upload', async ({ folder_detail_page }) => {
	await folder_detail_page.upload_file(folder_detail_page.FILE);

	const inode = folder_detail_page.get_inode(folder_detail_page.FILE);
	await expect(inode).toBeVisible();
});
