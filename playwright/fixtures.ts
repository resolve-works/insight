import type {Page, Locator} from '@playwright/test';
import {test as base} from '@playwright/test';
import {randomUUID} from 'crypto';

class OIDCProvider {
    access_token: string

    async authenticate(username: string, password: string) {
        const data = {
            username,
            password,
            grant_type: "password",
            client_id: "admin-cli",
        }

        const res = await fetch('https://localhost:8000/realms/master/protocol/openid-connect/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams(data).toString(),
        });

        const {access_token} = await res.json()
        this.access_token = access_token
    }

    create_user(username: string, password: string) {
        const data = {
            enabled: true,
            username,
            email: `${username}@example.com`,
            firstName: username,
            lastName: "insight",
            credentials: [{type: "password", value: password, temporary: false, }]
        }

        return fetch('https://localhost:8000/admin/realms/insight/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.access_token}`,
            },
            body: JSON.stringify(data),
        })
    }

    delete_user(url: string) {
        return fetch(url, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${this.access_token}`,
            }
        })
    }
}

class FilesIndexPage {
    page: Page;
    inodes: Locator;

    constructor(page: Page) {
        this.page = page
        this.inodes = this.page.getByTestId('inode');
    }

    async goto() {
        await this.page.goto('/files/');
    }

    async create_folder(name: string) {
        await this.page.getByRole('button', {name: 'Create Folder'}).click();
        await this.page.getByPlaceholder('Folder name').fill(name)
        await this.page.getByRole('button', {name: 'Create', exact: true}).click();
    }

    async upload_file(path: string) {
        // Trigger upload
        await this.page.locator('css=input[type=file]').setInputFiles(path);
    }

    async remove_all() {
        while ((await this.inodes.count()) > 0) {
            const inode = this.inodes.first()
            await inode.getByTestId('inode-actions-toggle').click()
            await inode.getByTestId('delete-inode').click()
            await inode.waitFor({state: "hidden"})
        }
    }
}


type Fixtures = {
    files_index_page: FilesIndexPage,
}

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

        await files_index.remove_all();
    }
})
