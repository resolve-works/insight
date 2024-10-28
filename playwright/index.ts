import { test as base } from '@playwright/test';
import type { Page } from '@playwright/test';
import { OIDCProvider } from './oidc';
import { FileIndexPage } from './fixtures';

export * from '@playwright/test';

async function get_provider() {
	if (!process.env.KEYCLOAK_ADMIN || !process.env.KEYCLOAK_ADMIN_PASSWORD) {
		throw new Error('Keycloak admin credentials not set');
	}

	// Admin login to OIDC
	const provider = new OIDCProvider();
	await provider.authenticate(process.env.KEYCLOAK_ADMIN, process.env.KEYCLOAK_ADMIN_PASSWORD);

	return provider;
}

async function authenticated_page({ page, baseURL }, use: Function) {
	if (!baseURL) {
		throw new Error('baseURL unconfigured');
	}

	const provider = await get_provider();

	const { url, username, password } = await provider.create_user();

	// Login as user in browser session
	await page.goto(baseURL);
	await page.getByLabel('Username or email').fill(username);
	await page.getByLabel('Password', { exact: true }).fill(password);
	await page.getByRole('button', { name: 'Sign In' }).click();
	await page.waitForURL(baseURL);

	await use(page);

	// Clean up
	await provider.delete_user(url);
}

type MultiUserFixtures = {
	my_page: Page;
	their_page: Page;
};

export const multiuser_test = base.extend<MultiUserFixtures>({
	my_page: async ({ browser, baseURL }, use) => {
		const context = await browser.newContext();
		const page = await context.newPage();

		await authenticated_page({ page, baseURL }, use);

		await context.close();
	},

	their_page: async ({ browser, baseURL }, use) => {
		const context = await browser.newContext();
		const page = await context.newPage();

		await authenticated_page({ page, baseURL }, use);

		await context.close();
	}
});

export const test = base.extend<{ file_index_page: FileIndexPage }>({
	page: authenticated_page,

	file_index_page: async ({ page }, use) => {
		const file_index_page = new FileIndexPage(page);
		await page.goto('/files');

		await use(file_index_page);

		await page.goto('/files');
		await file_index_page.remove_all();
	}
});
