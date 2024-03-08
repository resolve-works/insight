import type { Actions } from './$types';
import { sign } from '$lib/sign';
import { Channel } from '$lib/amqp.js';

export async function load({ fetch, depends }) {
    depends('api:files')

    const res = await fetch('/api/v1/files?is_uploaded=eq.true&select=id,name,status,documents(id,name,status)&order=created_at.desc')

    const files = await res.json()
    return { files }
}

export const actions = {
    upload: async ({ request, fetch, locals }) => {
        const data = await request.formData();
        const uploads: File[] = data.getAll('files') as File[]

        // Filter for 0 size files as submitting empty file input results in single 0 size file?
        for(const upload of uploads.filter(file => file.size > 0)) {
            const response = await fetch('/api/v1/files', {
                method: 'POST',
                body: JSON.stringify({ name: upload.name }),
                headers: { 
                    'Content-Type': 'application/json',
                    'Prefer': 'return=representation',
                }
            })
            const files = await response.json()
            const file = files[0]
            const url = sign(file.path, locals, 'PUT')
            const storage_response = await fetch(url, { 
                method: 'PUT', 
                body: upload.stream(), 
                // @ts-ignore
                duplex: 'half',
                headers: {
                    'Content-Type': upload.type,
                    'Content-Length': upload.size.toString(),
                }
            })

            const patch_response = await fetch(`/api/v1/files?id=eq.${file.id}`, {
                method: 'PATCH',
                body: JSON.stringify({ is_uploaded: true }),
                headers: { 'Content-Type': 'application/json', }
            })

            const channel = await Channel.connect(locals.access_token)
            channel.publish('analyze_file', { id: file.id });
            channel.close()
        }
    },

    remove: async ({ request, fetch, locals }) => {
        const data = await request.formData();
        await fetch(`/api/v1/files?id=eq.${data.get('id')}`, { 
            method: 'PATCH', 
            body: JSON.stringify({ is_deleted: true }),
            headers: { 'Content-Type': 'application/json' }
        })

        const channel = await Channel.connect(locals.access_token)
        channel.publish('delete_file', { id:`${data.get('id')}` });
        channel.close()
    },
} satisfies Actions;
