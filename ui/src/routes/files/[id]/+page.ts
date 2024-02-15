
export async function load({ params, fetch, parent, data }) {
    const { access_token } = await parent();

    const res = await fetch(`/api/v1/documents?file_id=eq.${params.id}&select=id,name,path,from_page,to_page,status`, {
        headers: { Authorization: `Bearer ${access_token}` }
    })
    const documents = await res.json();

    return { 
        ...data,
        // Humans index from 1
        //
        // When you say "to 137" to a human, they expect 137 to be in the
        // range. We are counting to document.length, which is not in the
        // range. Therefore we don't have to increment to_page with 1
        documents: documents.map(document => ({ ...document, from_page: document.from_page + 1 })),
    }
}
