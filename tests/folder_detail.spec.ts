
import {test, expect} from '../playwright';

test('Upload file in folder', async ({folder_detail_page, page}) => {
    // Create folder and navigate to it
    await expect(page.getByTestId('title')).toContainText(folder_detail_page.FOLDER)

    // Upload file
    await folder_detail_page.upload_file()
    await expect(page.getByTestId('inode-title')).toHaveCount(1)
})
