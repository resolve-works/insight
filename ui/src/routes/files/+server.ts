
import { json } from '@sveltejs/kit'
import sign from '$lib/sign.ts'

export async function POST({ locals, request, fetch }) {
    const { access_token } = locals

    // Should we seed data?
    if( ! request.body) {
        const res = await fetch('/api/v1/rpc/seed_pagestream', {
            method: 'POST',
            headers: { 
                Authorization: `Bearer ${access_token}`,
                Accept: 'application/json',
            },
        })

        const pagestream = await res.json()
        return json({ ...pagestream, url: sign(pagestream.path, locals, 'PUT') })
    }

    // Create pagestream for seeded upload
    const res = await fetch('/api/v1/pagestream', {
        method: 'POST',
        headers: { 
            Authorization: `Bearer ${access_token}`,
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
        },
        body: await request.text(),
    })

    const pagestreams = await res.json();
    return json(pagestreams[0])

}

