
import type { Actions } from './$types';

export async function load({ fetch, depends }) {
    depends('api:conversations')

    // TODO - Handle removed documents gracefully
    const res = await fetch('/api/v1/prompts?select=query,response,sources(score,index,...document(id,name,from_page))&order=created_at.desc&sources.order=score.desc&limit=1')

    const prompts = await res.json()
    return { prompts }
}

export const actions = {
    default: async ({ request, fetch }) => {
        // Strip keys=>value that are empty
        const entries = Array.from(await request.formData()).filter(([key, value]) => !!value);
        await fetch('/api/v1/prompts', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(entries)),
            headers: { 'Content-Type': 'application/json', }
        })
    }
} satisfies Actions
