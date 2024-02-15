
import { writable, derived } from 'svelte/store';
import type { Writable, Derived } from 'svelte/store';

// TODO - non-lazy typing
export type Document = Record<string, any>
export type DocumentInput = {
    original: Document,
    changes: Document,
    is_changed: boolean,
}

export const existing: Writable<Document[]> = writable([])
export const changed: Writable<Record<string, Document>> = writable({})
export const created: Writable<Document[]> = writable([])

export const documents: Derived<DocumentInput[]> = derived([existing, changed, created], ([$existing, $changed, $created]) => {
    return [
        ...$existing.map(original => {
            if( ! (original.id in $changed)) {
                $changed[original.id] = structuredClone(original)
                $changed = $changed;
            }

            let document = { 
                original, 
                changes: $changed[original.id],
            }

            return {
                ...document,
                is_changed: JSON.stringify(document.original) != JSON.stringify(document.changes),
            }
        }),
        ...$created.map(document => ({ original: {}, changes: document, is_changed: true }))
    ]
})
