
import { json } from '@sveltejs/kit'
import sign from '$lib/sign.ts'

export async function POST({ locals, request, fetch }) {
    const { access_token } = locals

    // TODO - Can we pipe response body?
    const res = await fetch(`/api/v1/pagestream`, {
        method: 'POST',
        headers: { 
            Authorization: `Bearer ${access_token}`, 
            Prefer: 'return=representation',
            'Content-Type': 'application/json', 
        },
        body: await request.text()
    })

    const pagestreams = await res.json()

    return json({ ...pagestreams[0], url: sign(pagestreams[0].path, locals, 'PUT') })
}
