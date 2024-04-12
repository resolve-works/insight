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

    async delete_user(username: string) {
        console.log(`deleting ${username}`)
    }
}

export const test = base.extend({
    page: async ({ page, baseURL }, use) => {
        if( ! baseURL ) {
            throw new Error('baseURL unconfigured');
        }

        if( ! process.env.KEYCLOAK_ADMIN || ! process.env.KEYCLOAK_ADMIN_PASSWORD ) {
            throw new Error('Keycloak admin credentials not set');
        }

        const provider = new OIDCProvider()
        await provider.authenticate(process.env.KEYCLOAK_ADMIN, process.env.KEYCLOAK_ADMIN_PASSWORD)

        const username = randomUUID();
        const password = "insight";
        await provider.create_user(username, password)

        await page.goto(baseURL);
        await page.getByLabel('Username or email').fill(username)
        await page.getByLabel('Password', { exact: true }).fill(password);
        await page.getByRole('button', { name: 'Sign In' }).click();
        await page.waitForURL(baseURL);

        await use(page);
        
        await provider.delete_user(username)
    }
})

