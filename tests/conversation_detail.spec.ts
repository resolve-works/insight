
import {test, expect} from '../playwright';

test('Answer prompt', async ({conversation_detail_page, page}) => {
    const query = 'Return a single word'
    await conversation_detail_page.prompt(query)
    await expect(page.getByTestId('human-message')).toContainText(query)
    await expect(page.getByTestId('message-loader')).toHaveCount(1);
    await expect(page.getByTestId('message-loader')).toHaveCount(0);
})
