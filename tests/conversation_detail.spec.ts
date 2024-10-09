
import {test, expect} from '../playwright';

test('Create prompt', async ({empty_conversation_detail_page, page}) => {
    const query = 'Return a single word'
    await empty_conversation_detail_page.prompt(query)
    await expect(page.getByTestId('human-message')).toContainText(query)
    await expect(page.getByTestId('message-loader')).toHaveCount(1);
    // OpenAI can be sloow
    await expect(page.getByTestId('message-loader')).toHaveCount(0, {timeout: 10000});
})

test('Exceed context of embedding model', async ({empty_conversation_detail_page, page}) => {
    const query = 'This is a test string, '
    // Exceed openai gpt-4-turbo limit
    await empty_conversation_detail_page.prompt(query.repeat(8192 / 5))
    await expect(page.getByTestId('message-loader')).toHaveCount(0);
    await expect(page.getByTestId('error-message')).toHaveCount(1)
})

// TODO
// I tested this locally with a big PDF because we need quite a bit of data in
// the system to exceed the context of the completion model (gpt-4-turbo).
//test('Exceed context of completion model')
