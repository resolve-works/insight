
export async function load({ parent, fetch }) {
    const { access_token } = await parent();

    const res = await fetch('/api/v1/pagestream?select=id,name,file(id)', {
        headers: { Authorization: `Bearer ${access_token}` }
    })

    return {
        pagestreams: await res.json()
    }
}
