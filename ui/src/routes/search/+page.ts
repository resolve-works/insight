
export async function load({ url, parent, data, fetch }) {
    const { access_token } = await parent();
    const query = url.searchParams.get('query')

    const res = await fetch('/api/v1/index/_search', {
        method: 'post',
        headers: { 
            'Content-Type': 'application/json', 
            'Authorization': `Bearer ${access_token}` 
        },
        body: JSON.stringify({
            "_source": {"excludes": ["insight:pages"]},
            "query": {
                "nested": {
                    "path": "insight:pages",
                    "query": {"match": {"insight:pages.contents": `${query}`}},
                    "inner_hits": {
                        "highlight": {
                            "fields": {"insight:pages.contents": {}},
                        },
                    },
                },
            },
        }),
    })

    const body = await res.json()
    return {
        query,
        total: body['hits']['total']['value'],
        hits: body['hits']['hits'],
    }
}
