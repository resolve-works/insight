
export async function load({ url, parent, data, fetch }) {
    const { access_token } = await parent();
    const query = url.searchParams.get('query');

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
                    "query": {
                        "query_string": {
                            "query": `${query}`,
                            "default_field": "insight:pages.contents"
                        }
                    },
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
        hits: body['hits']['hits'].map(hit => {
            return {
                filename: hit['_source']['insight:filename'],
                pages: hit["inner_hits"]["insight:pages"]["hits"]["hits"]
                    .filter(page => "highlight" in page)
                    .map(page => {
                        return {
                            index: page['_source']['index'] + 1,
                            highlights: page["highlight"]["insight:pages.contents"],
                        }
                    })
            }
        }),
    }
}
