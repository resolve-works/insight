
create or replace function ingest_pagestream(id uuid) returns void as $$
    import json
    plan = plpy.prepare("update pagestream set status='ingesting' where id=$1", ["uuid"])
    plpy.execute(plan, [id])

    plan = plpy.prepare("select * from pagestream where id=$1", ["uuid"])
    results = plpy.execute(plan, [id])

    plan = plpy.prepare("notify pagestream, '{payload}'".format(payload=json.dumps(results[0])))
    plpy.execute(plan)
$$ language plpython3u;
grant execute on function ingest_pagestream to external_user;

create or replace function set_updated_at() returns trigger as $$
begin
    new.updated_at = current_timestamp;
    return new;
end;
$$ language plpgsql;

create or replace function private.pagestream_set_owner() returns trigger as $$
declare
    owner_id uuid := current_setting('request.jwt.claims', true)::json->>'sub';
begin
    new.owner_id = owner_id;
    return new;
end
$$ language plpgsql;

create or replace function create_prompt(query text, similarity_top_k integer) returns json as $$
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
    query_engine = vector_store_index.as_query_engine(similarity_top_k=similarity_top_k)
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
$$ language plpython3u;

create or replace function file(private.source) returns setof private.file rows 1 as $$
  select * from private.file where pagestream_id = $1.pagestream_id and from_page <= $1.index and to_page > $1.index
$$ stable language sql;

