
export async function load({ url, parent, fetch }) {
    const { access_token } = await parent();
    const query = url.searchParams.get('query');

    const res = await fetch('/api/v1/index/_search', {
        method: 'post',
        headers: { 
            'Content-Type': 'application/json', 
            'Authorization': `Bearer ${access_token}` 
        },
        body: JSON.stringify({
            "_source": {"excludes": ["pages"]},
            "query": {
                "nested": {
                    "path": "pages",
                    "query": {
                        "query_string": {
                            "query": `${query ? query : '*'}`,
                            "default_field": "pages.contents"
                        }
                    },
                    "inner_hits": {
                        "highlight": {
                            "fields": {
                                "pages.contents": {
                                    fragment_size: 200,
                                }
                            },
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
                filename: hit['_source']['filename'],
                pages: hit["inner_hits"]["pages"]["hits"]["hits"]
                    .filter(page => "highlight" in page)
                    .map(page => {
                        const page_url = new URL(url);
                        const index = page['_source']['index'] + 1;
                        page_url.pathname = `/search/${hit['_id']}`;
                        page_url.searchParams.set('page', index)

                        return {
                            index,
                            url: page_url,
                            highlights: page["highlight"]["pages.contents"],
                        }
                    })
            }
        }),
    }
}
