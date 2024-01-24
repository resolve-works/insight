
export async function load({ parent, fetch }) {
    const { access_token } = await parent();

    const res = await fetch('/api/v1/pagestream?select=id,name,created_at,updated_at,file(id, name)&order=created_at.desc', {
        headers: { Authorization: `Bearer ${access_token}` }
    })

    const pagestreams = await res.json()
    return { pagestreams }
}
