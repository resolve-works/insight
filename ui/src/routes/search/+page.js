
import { PUBLIC_API_ENDPOINT } from '$env/static/public';

export async function load({ url, fetch }) {
    const data = {
        "_source": {"excludes": ["insight:pages"]},
        "query": {
            "nested": {
                "path": "insight:pages",
                "query": {"match": {"insight:pages.contents": url.searchParams.get('query')}},
                "inner_hits": {
                    "highlight": {
                        "fields": {"insight:pages.contents": {}},
                    },
                },
            },
        },
    }

    const res = await fetch(PUBLIC_API_ENDPOINT + '/index/_search', {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    })

	return res.json()
}
