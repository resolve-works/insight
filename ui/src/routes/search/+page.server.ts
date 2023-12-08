
export async function load({ url, fetch }) {
    const query = url.searchParams.get('query')
    const body = {
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
    }

    const res = await fetch('/api/v1/index/_search', {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    })

	const data = await res.json()
    return {
        query,
        total: data['hits']['total']['value'],
        hits: data['hits']['hits'],
    }
}
