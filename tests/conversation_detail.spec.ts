
import {test, expect} from '../playwright';

test('Answer prompt', async ({conversation_detail_page, page}) => {
    const query = 'State purpose'
    await conversation_detail_page.prompt(query)
    await expect(page.getByTestId('human-message')).toContainText(query)
})
