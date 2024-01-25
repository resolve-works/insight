
export async function load({ parent, fetch }) {
    const { access_token } = await parent();

    const res = await fetch('/api/v1/pagestreams?status=neq.uploading&select=id,name,status,created_at,updated_at,documents(id, name)&order=created_at.desc', {
        headers: { Authorization: `Bearer ${access_token}` }
    })

    const pagestreams = await res.json()
    return { pagestreams }
}
