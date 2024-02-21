CREATE OR REPLACE FUNCTION set_updated_at ()
    RETURNS TRIGGER
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION set_owner ()
    RETURNS TRIGGER
    AS $$
DECLARE
    owner_id uuid := current_setting('request.jwt.claims', TRUE)::json ->> 'sub';
BEGIN
    NEW.owner_id = owner_id;
    RETURN NEW;
END
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION set_file_path ()
    RETURNS TRIGGER
    AS $$
BEGIN
    NEW.path = format('%s/%s.pdf', NEW.owner_id, NEW.id);
    RETURN NEW;
END
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION set_document_path ()
    RETURNS TRIGGER
    AS $$
DECLARE
    owner_id uuid;
BEGIN
    SELECT files.owner_id INTO owner_id FROM files WHERE id=NEW.file_id;
    NEW.path = format('%s/%s/%s.pdf', owner_id, NEW.file_id, NEW.id);
    RETURN NEW;
END
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION answer_prompt (id uuid)
    RETURNS VOID
    AS $$
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
$$
LANGUAGE PLPYTHON3U;

GRANT EXECUTE ON FUNCTION answer_prompt TO external_user;

CREATE OR REPLACE FUNCTION document (sources)
    RETURNS SETOF documents ROWS 1
    AS $$
    SELECT
        *
    FROM
        documents
    WHERE
        file_id = $1.file_id
        AND from_page <= $1.INDEX
        AND to_page > $1.INDEX
$$
LANGUAGE SQL;

GRANT EXECUTE ON FUNCTION document TO external_user;

