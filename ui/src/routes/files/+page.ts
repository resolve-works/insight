
export async function load({ parent, fetch }) {
    const { access_token } = await parent();

    const res = await fetch('/api/v1/pagestream?status=neq.uploading&select=id,name,status,created_at,updated_at,file(id, name)&order=created_at.desc', {
        headers: { Authorization: `Bearer ${access_token}` }
    })

    const pagestreams = await res.json()
    return { pagestreams }
}
