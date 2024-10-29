import { test, expect } from '.';

test('Mark folder as public', async ({ folder_detail_page, folder_edit_page, page }) => {
	// Upload file
	await folder_detail_page.upload_file();
	await expect(page.getByTestId('inode-title')).toHaveCount(1);

	// Go to folder edit page & set public
	await page.getByRole('navigation').getByRole('link', { name: 'Files' }).click();
	await page.getByTestId('inode-actions').click();
	await page.getByTestId('edit-inode').click();
	await folder_edit_page.update_public_state(true);

	// Go to file edit page to check public state
	await page.getByRole('navigation').getByRole('link', { name: 'Files' }).click();
	await page.getByTestId('inode-title').click();
	await page.getByTestId('inode-actions').click();
	await page.getByTestId('edit-inode').click();

	await expect(page.getByTestId('inode-is-public-input')).toBeChecked();
});

test('Mark file in folder as public', async ({ folder_detail_page, folder_edit_page, page }) => {
	// Upload file
	await folder_detail_page.upload_file();
	await expect(page.getByTestId('inode-title')).toHaveCount(1);

	// Go to file edit page & set public
	await page.getByTestId('inode-actions').click();
	await page.getByTestId('edit-inode').click();
	await folder_edit_page.update_public_state(true);

	// Go to folder edit page to check public state
	await page.getByRole('navigation').getByRole('link', { name: 'Files' }).click();
	await page.getByTestId('inode-actions').click();
	await page.getByTestId('edit-inode').click();

	await expect(page.getByTestId('inode-is-public-input')).toBeChecked();
});
