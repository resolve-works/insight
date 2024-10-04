
import {test, expect} from '../playwright';

// TODO - edit page
test('Edit file', async ({file_edit_page, page}) => {
    const name = "New name"
    await file_edit_page.update_name(name)
    await expect(page.getByTestId('title')).toContainText(name);
})

test('Edit no filename', async ({file_edit_page, page}) => {
    await file_edit_page.update_name('')
    await expect(page.getByTestId('error-message')).toContainText('must contain at least 1');
})
