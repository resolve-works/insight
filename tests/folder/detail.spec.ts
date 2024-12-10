import path from 'path';
import { test, expect } from '.';

test('Upload file in folder', async ({ folder_detail_page, page }) => {
	// Upload file
	await folder_detail_page.goto();
	await expect(page.getByTestId('title')).toHaveText('folder_detail');
	//await folder_detail_page.upload_file(path.join(__dirname, '..', 'test_data', 'test.pdf'));

	//await expect(page.getByTestId('inode-title').filter({ hasText: 'test.pdf' })).toHaveCount(1);
});
