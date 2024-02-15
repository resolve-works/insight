
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

// Original document also contains "status" and maybe other things, we don't
// want those to mark the document as changed
export function subset({ name, from_page, to_page }: Document) {
    return { name, from_page, to_page }
}

export const documents: Derived<DocumentInput[]> = derived([existing, changed, created], ([$existing, $changed, $created]) => {
    return [
        ...$existing.map(original => {
            // Only add to changed when its not in there to prevent overwriting user changes
            if( ! (original.id in $changed)) {
                $changed[original.id] = subset(original)
                $changed = $changed;
            }

            let document = { 
                original, 
                changes: $changed[original.id],
            }

            return {
                ...document,
                is_changed: JSON.stringify(subset(document.original)) != JSON.stringify(document.changes),
            }
        }),
        ...$created.map(document => ({ original: {}, changes: document, is_changed: true }))
    ]
})
