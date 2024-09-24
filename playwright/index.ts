import {test as base} from '@playwright/test';
import {randomUUID} from 'crypto';
import {OIDCProvider} from './oidc';
import type {Fixtures} from './fixtures';
import {FilesIndexPage} from './fixtures'

export * from '@playwright/test'

export const test = base.extend<Fixtures>({
    page: async ({page, baseURL}, use) => {
        if (!baseURL) {
            throw new Error('baseURL unconfigured');
        }

        if (!process.env.KEYCLOAK_ADMIN || !process.env.KEYCLOAK_ADMIN_PASSWORD) {
            throw new Error('Keycloak admin credentials not set');
        }

        // Admin login to OIDC
        const provider = new OIDCProvider()
        await provider.authenticate(process.env.KEYCLOAK_ADMIN, process.env.KEYCLOAK_ADMIN_PASSWORD)

        // Create a user
        const username = randomUUID();
        const password = "insight";
        const res = await provider.create_user(username, password)
        const url = res.headers.get('location')
        if (!url) {
            throw new Error('User location not found in headers')
        }

        // Login as user in browser session
        await page.goto(baseURL);
        await page.getByLabel('Username or email').fill(username)
        await page.getByLabel('Password', {exact: true}).fill(password);
        await page.getByRole('button', {name: 'Sign In'}).click();
        await page.waitForURL(baseURL);

        await use(page);

        // Clean up
        await provider.delete_user(url)
    },

    files_index_page: async ({page}, use) => {
        const files_index = new FilesIndexPage(page)
        await files_index.goto()

        await use(files_index)

        // Could be we navigated away.
        await files_index.goto();
        await files_index.remove_all();
    },

    files_detail_page: async ({page}, use) => {
        const files_index = new FilesIndexPage(page)
        await files_index.goto()
    },
})
