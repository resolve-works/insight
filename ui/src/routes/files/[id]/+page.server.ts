import type { Actions } from './$types';

import { sign } from '$lib/sign.ts';
import { Channel } from '$lib/amqp.ts';

export async function load({ params, fetch, locals, depends }) {
    depends('api:files')

    const res = await fetch(`/api/v1/files?id=eq.${params.id}&select=path,number_of_pages,documents(id,name,path,from_page,to_page,status)`)
    const files = await res.json();
    const { path, documents, number_of_pages } = files[0]

    return { 
        number_of_pages, 
        // Humans index from 1
        //
        // When you say "to 137" to a human, they expect 137 to be in the
        // range. We are counting to document.length, which is not in the
        // range. Therefore we don't have to increment to_page with 1
        documents: documents.map(document => ({ ...document, from_page: document.from_page + 1 })),
        url: sign(path, locals) 
    }
}

export const actions = {
    // Store created & updated documents
    store: async ({ request, fetch, params, locals }) => {
        const data = await request.formData();

        // This was something very abstract and complex, kept simple for a reason
        const id = data.getAll('id');
        const name = data.getAll('name');
        // Machines index from 0, the HtmlInput is 1 indexed, see load function
        const from_page = data.getAll('from_page')
            .map(value => parseInt(value.toString()) - 1);
        const to_page = data.getAll('to_page')
            .map(value => parseInt(value.toString()));

        const documents = id.map((id, i) => {
            const document = { 
                name: name[i], 
                from_page: from_page[i], 
                to_page: to_page[i],
            }
            // Add file id when creating, or ID when it's set to update
            return id ? { id: id.toString(), ...document } : { file_id: params.id, ...document };
        })

        const channel = await Channel.connect(locals.access_token)

        // Update existing documents
        const to_be_updated = documents.filter(document => 'id' in document);
        for(const document of to_be_updated) {
            await fetch(`/api/v1/documents?id=eq.${document.id}`, { 
                method: 'PATCH', 
                body: JSON.stringify(document),
                headers: { 'Content-Type': 'application/json' }
            })
            channel.publish('ingest_document', { id: document.id });
        }

        // Bulk insert new ones
        const to_be_created = documents.filter(document => ! ('id' in document))
        if(to_be_created.length) {
            const response = await fetch('/api/v1/documents', {
                method: 'POST',
                body: JSON.stringify(to_be_created),
                headers: { 
                    'Content-Type': 'application/json',
                    'Prefer': 'return=representation',
                }
            })

            const created_documents = await response.json()
            for(const document of created_documents) {
                channel.publish('ingest_document', { id: document.id });
            }
        }

        channel.close()
    },

    // Remove a single document
    remove: async ({ request, fetch, locals }) => {
        const data = await request.formData();
        await fetch(`/api/v1/documents?id=eq.${data.get('id')}`, { method: 'DELETE' })

        const channel = await Channel.connect(locals.access_token)
        channel.publish('delete_document', { id:`${data.get('id')}` });
        channel.close()
    },
} satisfies Actions;
