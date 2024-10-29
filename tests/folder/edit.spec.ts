import path from 'path';
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

test('Mark public files in folder as private', async ({
	folder_detail_page,
	folder_edit_page,
	page
}) => {
	// Upload files
	await folder_detail_page.upload_file();
	await folder_detail_page.upload_file(
		path.join(__dirname, '..', '..', 'test_data', 'test(0).pdf')
	);
	await expect(page.getByTestId('inode-title')).toHaveCount(2);

	// Go to file edit page & set public
	await page.getByRole('navigation').getByRole('link', { name: 'Files' }).click();
	await page.getByTestId('inode-actions').click();
	await page.getByTestId('edit-inode').click();
	await folder_edit_page.update_public_state(true);

	// Go to folder and mark first file private
	await page.getByRole('navigation').getByRole('link', { name: 'Files' }).click();
	await page.getByTestId('inode-title').click();
	await page.getByTestId('inode-actions').first().click();
	await page.getByTestId('edit-inode').first().click();
	await folder_edit_page.update_public_state(false);

	// Go to folder edit page to check public state
	await page.getByRole('navigation').getByRole('link', { name: 'Files' }).click();
	await page.getByTestId('inode-actions').click();
	await page.getByTestId('edit-inode').click();
	await expect(page.getByTestId('inode-is-public-input')).toBeChecked();

	// Go to folder and mark second file private
	await page.getByRole('navigation').getByRole('link', { name: 'Files' }).click();
	await page.getByTestId('inode-title').click();
	await page.getByTestId('inode-actions').last().click();
	await page.getByTestId('edit-inode').last().click();
	await folder_edit_page.update_public_state(false);

	// Go to folder edit page to check public state
	await page.getByRole('navigation').getByRole('link', { name: 'Files' }).click();
	await page.getByTestId('inode-actions').click();
	await page.getByTestId('edit-inode').click();
	await expect(page.getByTestId('inode-is-public-input')).toBeChecked({ checked: false });
});

// TODO - remove public file from folder
