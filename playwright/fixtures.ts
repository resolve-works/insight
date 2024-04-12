import { test as base } from '@playwright/test';
import fs from 'fs';
import path from 'path';

const get_admin_credentials = async () => {
    const data = {
        username: process.env.KEYCLOAK_ADMIN || '',
        password: process.env.KEYCLOAK_ADMIN_PASSWORD || '',
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

    return res.json()
}

const create_account = async id => {
    const { access_token } = await get_admin_credentials()

    const username = `user-${id}`;
    const password = "insight";

    const data = {
        enabled: true,
        username,
        email: `${username}@example.com`,
        firstName: username,
        lastName: "insight",
        credentials: [
            {
                type: "password",
                value: password,
                temporary: false,
            }
        ]
    }

    const res = await fetch('https://localhost:8000/admin/realms/insight/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`,
        },
        body: JSON.stringify(data),
    })

    return { username, password }
}

export * from '@playwright/test';
export const test = base.extend<{}, { workerStorageState: string }>({
  // Use the same storage state for all tests in this worker.
  storageState: ({ workerStorageState }, use) => use(workerStorageState),

  // Authenticate once per worker with a worker-scoped fixture.
  workerStorageState: [async ({ browser }, use) => {
    // Important: make sure we authenticate in a clean environment by unsetting storage state.
    const id = test.info().parallelIndex;
    const filename = path.resolve(test.info().project.outputDir, `.auth/${id}.json`);

    if (fs.existsSync(filename)) {
      await use(filename);
      return;
    }

    const { username, password } = await create_account(id)

    // Important: make sure we authenticate in a clean environment by unsetting storage state.
    const page = await browser.newPage({ storageState: undefined, ignoreHTTPSErrors: true });

    // Perform authentication steps. Replace these actions with your own.
    await page.goto('http://localhost:3000');
    // This 'test' user should exist in the insight_test OIDC realm
    await page.getByLabel('Username or email').fill(username)
    await page.getByLabel('Password', { exact: true }).fill(password);
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Wait until the page receives the cookies.
    await page.waitForURL('http://localhost:3000');

    await page.context().storageState({ path: filename });
    await page.close();
    await use(filename);
  }, { scope: 'worker' }],
});
