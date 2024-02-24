import { test as baseTest } from '@playwright/test';
import fs from 'fs';
import path from 'path';

export * from '@playwright/test';
export const test = baseTest.extend<{}, { workerStorageState: string }>({
  // Use the same storage state for all tests in this worker.
  storageState: ({ workerStorageState }, use) => use(workerStorageState),

  // Authenticate once per worker with a worker-scoped fixture.
  workerStorageState: [async ({ browser }, use) => {
    // Important: make sure we authenticate in a clean environment by unsetting storage state.
    const page = await browser.newPage({ storageState: undefined, ignoreHTTPSErrors: true });
    const id = test.info().parallelIndex;
    const fileName = path.resolve(test.info().project.outputDir, `.auth/${id}.json`);

    if (fs.existsSync(fileName)) {
      await use(fileName);
      return;
    }

    // Perform authentication steps. Replace these actions with your own.
    await page.goto('https://insight:8080');
    await page.getByLabel('Username or email').fill('test')
    await page.getByLabel('Password').fill('test');
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Wait until the page receives the cookies.
    await page.waitForURL('https://insight:8080');
    // End of authentication steps.

    await page.context().storageState({ path: fileName });
    await page.close();
    await use(fileName);
  }, { scope: 'worker' }],
});
