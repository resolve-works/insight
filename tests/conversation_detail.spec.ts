import { test as base, expect } from '../playwright';
import { ConversationDetailPage } from '../playwright/fixtures';

export const test = base.extend<{ empty_conversation_detail_page: ConversationDetailPage }>({
	empty_conversation_detail_page: async ({ file_index_page, page }, use) => {
		await file_index_page.start_conversation();
		const conversation_detail_page = new ConversationDetailPage(page);
		await use(conversation_detail_page);
	}

	/*
	conversation_detail_page: async ({ file_index_page, page }, use) => {
		await file_index_page.upload_file();
		await expect(page.getByTestId('inode-loader')).toHaveCount(1);
		await expect(page.getByTestId('inode-loader')).toHaveCount(0);
		await file_index_page.start_conversation();
		const conversation_detail_page = new ConversationDetailPage(page);
		await use(conversation_detail_page);
	}
    */
});

test('Create prompt', async ({ empty_conversation_detail_page, page }) => {
	const query = 'Return a single word';
	await empty_conversation_detail_page.prompt(query);
	await expect(page.getByTestId('human-message')).toContainText(query);
	await expect(page.getByTestId('streamed-answer')).toHaveCount(0);
	await expect(page.getByTestId('machine-message')).toHaveCount(2);
});

test('Empty prompt', async ({ empty_conversation_detail_page, page }) => {
	await empty_conversation_detail_page.prompt('');
	await expect(page.getByTestId('error-message')).toHaveCount(1);
});

test('High similarity', async ({ empty_conversation_detail_page, page }) => {
	await empty_conversation_detail_page.prompt('test', 100);
	await expect(page.getByTestId('error-message')).toHaveCount(1);
});

test('Exceed context of embedding model', async ({ empty_conversation_detail_page, page }) => {
	const query = 'This is a test string, ';
	// Exceed openai limit
	await empty_conversation_detail_page.prompt(query.repeat(8192 / 5));
	await expect(page.getByTestId('error-message')).toHaveCount(1);
});

// TODO
// I tested this locally with a big PDF because we need quite a bit of data in
// the system to exceed the context of the completion model.
//test('Exceed context of completion model')
