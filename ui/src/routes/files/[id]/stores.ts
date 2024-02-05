
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';

export type Document = Record<string, any>

export const documents: Writable<{ original: Document, changes: Document }[]> = writable([]);
