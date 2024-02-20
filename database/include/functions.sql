
create or replace function set_updated_at() returns trigger as $$
begin
    new.updated_at = current_timestamp;
    return new;
end;
$$ language plpgsql;

create or replace function set_owner() returns trigger as $$
declare
    owner_id uuid := current_setting('request.jwt.claims', true)::json->>'sub';
begin
    new.owner_id = owner_id;
    return new;
end
$$ language plpgsql;

create or replace function answer_prompt(id uuid) returns void as $$
    import os
    from llama_index import VectorStoreIndex
    from llama_index.vector_stores import PGVectorStore

    plan = plpy.prepare("select * from prompts where id=$1", ["uuid"])
    prompt = plpy.execute(plan, [id])[0]

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
    query_engine = vector_store_index.as_query_engine(similarity_top_k=prompt['similarity_top_k'])
    response = query_engine.query(prompt['query'])

    plan = plpy.prepare("update prompts set response=$1 where id=$2", ["text", "uuid"])
    plpy.execute(plan, [response.response, id])

    plan = plpy.prepare(
        "insert into sources (prompt_id, file_id, index, score) values ($1, $2, $3, $4)",
        ["uuid", "uuid", "integer", "float"]
    )
    for node in response.source_nodes:
        source_data = [id, node.metadata['file_id'], node.metadata['index'], node.get_score()]
        node = plpy.execute(plan, source_data)
$$ language plpython3u;
grant execute on function answer_prompt to external_user;

create or replace function document(sources) returns setof documents rows 1 as $$
  select * from documents where file_id = $1.file_id and from_page <= $1.index and to_page > $1.index
$$ stable language sql;
grant execute on function document to external_user;

