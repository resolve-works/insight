import {test as base, expect} from '@playwright/test';
import {randomUUID} from 'crypto';
import {OIDCProvider} from './oidc';
import type {Fixtures} from './fixtures';
import {FileIndexPage, FileEditPage, ConversationDetailPage} from './fixtures'

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

    file_index_page: async ({page}, use) => {
        const file_index_page = new FileIndexPage(page)
        await page.goto('/files')

        await use(file_index_page)

        await page.goto('/files')
        await file_index_page.remove_all();
    },

    file_edit_page: async ({file_index_page, page}, use) => {
        await file_index_page.upload_file()
        await expect(page.getByTestId('inode')).toHaveCount(1)
        await page.getByTestId('inode-actions-toggle').click()
        await page.getByTestId('edit-inode').click()

        await use(new FileEditPage(page))
    },

    file_detail_page: async ({file_index_page, page}, use) => {
        await file_index_page.upload_file()
        await page.getByTestId('inode-title').click()

        await use(page)
    },

    folder_detail_page: async ({file_index_page, page}, use) => {
        await file_index_page.create_folder()
        await page.getByTestId('inode-title').click()

        const folder_detail_page = new FileIndexPage(page)
        await use(folder_detail_page)
    },

    empty_conversation_detail_page: async ({file_index_page, page}, use) => {
        await file_index_page.start_conversation()
        const conversation_detail_page = new ConversationDetailPage(page)
        await use(conversation_detail_page)
    },

    conversation_detail_page: async ({file_index_page, page}, use) => {
        await file_index_page.upload_file()
        await expect(page.getByTestId('inode-loader')).toHaveCount(1);
        await expect(page.getByTestId('inode-loader')).toHaveCount(0);
        await file_index_page.start_conversation()
        const conversation_detail_page = new ConversationDetailPage(page)
        await use(conversation_detail_page)
    }
})
