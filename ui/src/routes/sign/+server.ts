
import { json } from '@sveltejs/kit'
import sign from '$lib/sign.ts'

export async function POST({ locals, request }) {
    const { path, method = "GET" } = await request.json()

    return json(sign(path, locals, method))
}

