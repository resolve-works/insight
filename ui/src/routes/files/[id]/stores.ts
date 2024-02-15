
import { writable, derived } from 'svelte/store';
import type { Writable, Derived } from 'svelte/store';

// TODO - non-lazy typing
export type Document = Record<string, any>
export type DocumentInput = {
    original: Document,
    changes: Document,
}

export const existing: Writable<Document[]> = writable([])
export const changed: Writable<Record<string, Document>[]> = writable([])
export const created: Writable<Document[]> = writable([])



export const documents: Derived<DocumentInput[]> = derived([existing, changed, created], ([$existing, $changed, $created]) => {
    return [
        ...$existing.map(original => {
            if( ! (original.id in $changed)) {
                $changed[original.id] = original;
            }

            return { 
                original, 
                changes: $changed[original.id],
            }
        }),
        ...$created.map(document => ({ original: {}, changes: document }))
    ]
})
