
import {test, expect} from '../playwright';

// TODO - edit page
test('Edit file', async ({file_edit_page, file_index_page}) => {
    const name = "New name"
    await file_edit_page.getByTestId('inode-name-input').fill(name)
    await file_edit_page.getByTestId('change-inode-name').click()

    await expect(file_edit_page.getByTestId('title')).toContainText(name);
})
