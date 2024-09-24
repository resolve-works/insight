
import path from 'path';
import type {Page, Locator} from '@playwright/test';

const FOLDER = 'test folder'
const FILE = 'test.pdf'

export class FileIndexPage {
    page: Page;
    inodes: Locator;

    FOLDER = FOLDER;
    FILE = FILE;
    PATH = path.join(__dirname, FILE);

    constructor(page: Page) {
        this.page = page
        this.inodes = this.page.getByTestId('inode');
    }

    async create_folder(name: string = this.FOLDER) {
        await this.page.getByRole('button', {name: 'Create Folder'}).click();
        await this.page.getByPlaceholder('Folder name').fill(name)
        await this.page.getByRole('button', {name: 'Create', exact: true}).click();
    }

    async upload_file(path: string = this.PATH) {
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

export type Fixtures = {
    file_index_page: FileIndexPage,
    folder_detail_page: FileIndexPage,
    file_detail_page: Page,
    file_edit_page: Page,
}

