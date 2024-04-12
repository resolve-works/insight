import { test as base } from '@playwright/test';
import { randomUUID } from 'crypto';

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

        const { access_token } = await res.json()
        this.access_token = access_token
    }

    create_user(username: string, password: string) {
        const data = {
            enabled: true,
            username,
            email: `${username}@example.com`,
            firstName: username,
            lastName: "insight",
            credentials: [ { type: "password", value: password, temporary: false, } ]
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
            method: 'DELETE' ,
            headers: {
                'Authorization': `Bearer ${this.access_token}`,
            }
        })
    }
}

export * from '@playwright/test'

export const test = base.extend({
    page: async ({ page, baseURL }, use) => {
        if( ! baseURL ) {
            throw new Error('baseURL unconfigured');
        }

        if( ! process.env.KEYCLOAK_ADMIN || ! process.env.KEYCLOAK_ADMIN_PASSWORD ) {
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
        if( ! url ) {
            throw new Error('User location not found in headers')
        }

        // Login as user in browser session
        await page.goto(baseURL);
        await page.getByLabel('Username or email').fill(username)
        await page.getByLabel('Password', { exact: true }).fill(password);
        await page.getByRole('button', { name: 'Sign In' }).click();
        await page.waitForURL(baseURL);

        await use(page);

        // Clean up
        await provider.delete_user(url)
    }
})

