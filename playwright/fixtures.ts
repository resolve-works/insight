import type { Page } from '@playwright/test';

export class FileIndexPage {
	page: Page;
	path: string;

	constructor(page: Page, path: string) {
		this.page = page;
		this.path = path;
	}

	async goto() {
		await this.page.goto(this.path);
	}

	async create_folder(name: string) {
		await this.page.getByTestId('show-folder-form').click();
		await this.page.getByTestId('folder-name-input').fill(name);
		await this.page.getByTestId('create-folder').click();
	}

	async upload_file(file_path: string) {
		// Trigger upload
		await this.page.getByTestId('files-input').setInputFiles(file_path);
	}

	async start_conversation() {
		await this.page.getByTestId('start-conversation').click();
	}

	async remove_all() {
		const inode_actions = this.page.getByTestId('inode-actions');

		while ((await inode_actions.count()) > 0) {
			const actions = inode_actions.first();
			await actions.getByTestId('inode-actions-toggle').click();
			await actions.getByTestId('delete-inode').click();
			await actions.waitFor({ state: 'hidden' });
		}
	}
}

export class FileEditPage {
	page: Page;

	constructor(page: Page) {
		this.page = page;
	}

	async update_name(name: string) {
		await this.page.getByTestId('inode-name-input').fill(name);
		await this.page.getByTestId('update-inode').click();
	}

	async update_public_state(is_public: boolean) {
		await this.page.getByTestId('inode-is-public-input').setChecked(is_public);
		await this.page.getByTestId('update-inode').click();
	}
}

export class ConversationDetailPage {
	page: Page;

	constructor(page: Page) {
		this.page = page;
	}

	async prompt(query: string, similarity_top_k: number | undefined = undefined) {
		await this.page.getByTestId('query-input').fill(query);
		if (similarity_top_k) {
			await this.page.getByTestId('similarity-top-k-input').fill(similarity_top_k.toString());
		}
		await this.page.getByTestId('create-prompt').click();
	}
}
