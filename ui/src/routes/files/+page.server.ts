import type { Actions } from './$types';

export async function load({ fetch, depends }) {
    depends('api:files')

    const res = await fetch('/api/v1/files?status=neq.uploading&select=id,name,status,created_at,updated_at,documents(id,name,status)&order=created_at.desc')

    const files = await res.json()
    return { files }
}

export const actions = {
    // Remove a single file
    remove: async ({ request, fetch }) => {
        const data = await request.formData();
        await fetch(`/api/v1/files?id=eq.${data.get('id')}`, { method: 'DELETE' })
    },
} satisfies Actions;
