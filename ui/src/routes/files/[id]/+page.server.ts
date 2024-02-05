
import sign from '$lib/sign.ts';

export async function load({ params, fetch, locals }) {
    const { access_token } = locals;

    const res = await fetch(`/api/v1/files?id=eq.${params.id}&select=name,path,pages,documents(id,name,path,from_page,to_page,status)`, {
        headers: { Authorization: `Bearer ${access_token}` }
    })
    const files = await res.json();
    const file = files[0]

    return { 
        // Humans index from 1
        //
        // When you say "to 137" to a human, they expect 137 to be in the
        // range. We are counting to document.length, which is not in the
        // range. Therefore we don't have to increment to_page with 1
        pages: file.pages,
        documents: file.documents.map(document => ({ ...document, from_page: document.from_page + 1 })),
        url: sign(file.path, locals),
    }
}
