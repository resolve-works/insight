
create or replace function create_prompt(query text) returns json language plpython3u as $$
    import os
    import json
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

    plan = plpy.prepare("insert into private.prompt (query, response) values ($1, $2) returning id", ["text", "text"])
    prompts = plpy.execute(plan, [query, response.response])

    plan = plpy.prepare(
        "insert into private.source (prompt_id, pagestream_id, index, score) values ($1, $2, $3, $4)",
        ["uuid", "uuid", "integer", "float"]
    )
    for node in response.source_nodes:
        node = plpy.execute(
            plan, 
            [prompts[0]['id'], node.metadata['pagestream_id'], node.metadata['index'], node.get_score()]
        )
    return json.dumps(list(prompts))
$$;

create table if not exists private.prompt (
    id uuid default gen_random_uuid(),
    query text not null,
    response text,

    primary key (id)
);
grant select, update, insert on private.prompt to insight_user;

create table if not exists private.source (
    prompt_id uuid not null,
    pagestream_id uuid not null,
    index integer not null,
    score float not null,

    constraint fk_prompt foreign key(prompt_id) references private.prompt(id) on delete cascade,
    constraint fk_pagestream foreign key(pagestream_id) references private.pagestream(id) on delete cascade
);
grant select, insert on private.source to insight_user;

create or replace view source as select * from private.source;
grant select, insert on public.source to insight_user;

create or replace view prompt as select * from private.prompt;
grant select, insert on public.prompt to insight_user;

create or replace function file(source) returns setof file rows 1 as $$
  select * from file where pagestream_id = $1.pagestream_id and from_page <= $1.index and to_page > $1.index
$$ stable language sql;

