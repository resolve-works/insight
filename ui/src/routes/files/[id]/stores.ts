
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';

export type Document = {
    id?: string;
    name?: string;
    from_page?: number;
    to_page?: number;
}

export const documents: Writable<{ original: Document, changes: Document }[]> = writable([]);

