
create or replace function create_prompt(query text) returns json language plpython3u as $$
    import os
    import json
    import logging
    from llama_index import VectorStoreIndex
    from llama_index.vector_stores import PGVectorStore

    vector_store = PGVectorStore.from_params(
        host="127.0.0.1",
        port=5432,
        user=os.environ.get('PG_WORKER_USER'),
        password=os.environ.get("PG_WORKER_PASSWORD"),
        database="insight",
        schema_name="private",
        table_name="page",
        perform_setup=False,
        embed_dim=1536,
    )
    vector_store_index = VectorStoreIndex.from_vector_store(vector_store)
    query_engine = vector_store_index.as_query_engine()
    response = query_engine.query(query)
    logging.info(response.source_nodes)

    plan = plpy.prepare(
        "insert into private.prompt (query, response) values ($1, $2) returning *",
        ["text", "text"]
    )
    results = plpy.execute(plan, [query, response])
    return json.dumps(results[0])
$$;

create table if not exists private.prompt (
    id uuid default gen_random_uuid(),
    query text not null,
    response text,

    primary key (id)
);

create table if not exists private.source (
    prompt_id uuid not null,
    pagestream_id uuid not null,
    index integer not null,

    constraint fk_prompt foreign key(prompt_id) references private.prompt(id) on delete cascade,
    constraint fk_pagestream foreign key(pagestream_id) references private.pagestream(id) on delete cascade
);

grant select, insert on private.prompt to web_user;
grant select, insert on private.source to web_user;
