
create or replace function answer_prompt() returns trigger language plpython3u as $$
    import os
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

    TD["new"]["response"] = query_engine.query(TD["new"]["query"])
    return "MODIFY"
$$;

create table if not exists public.prompt (
    id uuid not null default gen_random_uuid(),
    query text not null,
    response text,

    primary key (id)
);
create or replace trigger answer_prompt before insert on public.prompt for each row execute function answer_prompt();

