
import { json } from '@sveltejs/kit'
import sign from '$lib/sign.ts'

export async function POST({ locals, request, fetch }) {
    const { access_token } = locals

    const res = await fetch('/api/v1/pagestream', {
        method: 'POST',
        headers: { 
            Authorization: `Bearer ${access_token}`,
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
        },
        body: await request.text(),
    })

    const pagestream = (await res.json())[0]
    return json({ ...pagestream, url: sign(pagestream.path, locals, 'PUT') })
}

