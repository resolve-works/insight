
import { json } from '@sveltejs/kit'

export async function POST({ locals, request, fetch }) {
    const { access_token } = locals;

    const res = await fetch(`/api/v1/pagestream`, {
        method: 'POST',
        headers: { 
            Authorization: `Bearer ${access_token}`, 
            Prefer: 'return=representation',
            'Content-Type': 'application/json', 
        },
        body: await request.text()
    })

    // TODO presign post url
    const pagestreams = await res.json();

    return json(pagestreams[0])
}
