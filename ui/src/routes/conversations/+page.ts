
export async function load({ parent, fetch }) {
    const { access_token } = await parent();

    const res = await fetch('/api/v1/prompts?select=query,response,sources(score,index,...document(id,name,from_page))&order=created_at.desc&sources.order=score.desc&limit=1', {
        headers: { Authorization: `Bearer ${access_token}` }
    })

    const prompts = await res.json()
    return { prompts }
}
