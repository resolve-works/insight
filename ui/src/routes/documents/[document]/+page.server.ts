
import sign from '$lib/sign.ts';

export async function load({ params, fetch, locals }) {
    const { access_token } = locals;

    const res = await fetch(`/api/v1/documents?id=eq.${params.document}`, {
        headers: { Authorization: `Bearer ${access_token}` }
    })
    const documents = await res.json();
    const document = documents[0]

    return {
        ...document,
        url: sign(document.path, locals),
    }
}
