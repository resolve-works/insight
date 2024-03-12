
CREATE TYPE document_status AS ENUM (
    'ingesting',
    'indexing'
);

CREATE TABLE private.documents (
    id uuid DEFAULT gen_random_uuid (),
    file_id uuid NOT NULL,
    name text,
    path text NOT NULL,
    from_page integer NOT NULL,
    to_page integer NOT NULL,
    status document_status DEFAULT 'ingesting',
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (file_id) REFERENCES private.files (id) ON DELETE CASCADE
);

GRANT ALL PRIVILEGES ON private.documents TO insight_worker;

CREATE TABLE IF NOT EXISTS private.pages (
    id bigserial,
    file_id uuid NOT NULL,
    index integer NOT NULL,
    contents text NOT NULL,
    embedding vector (1536),
    FOREIGN KEY (file_id) REFERENCES private.files (id) ON DELETE CASCADE,
    PRIMARY KEY (id)
);

GRANT ALL PRIVILEGES ON private.pages TO insight_worker;
GRANT ALL PRIVILEGES ON private.pages_id_seq TO insight_worker;
GRANT usage, SELECT ON private.pages_id_seq TO external_user;

CREATE OR REPLACE FUNCTION set_document_path ()
    RETURNS TRIGGER
    AS $$
DECLARE
    owner_id uuid;
BEGIN
    SELECT
        files.owner_id INTO owner_id
    FROM
        files
    WHERE
        id = NEW.file_id;
    -- TODO - name files with name
    NEW.path = format('%s/%s/%s.pdf', owner_id, NEW.file_id, NEW.id);
    RETURN NEW;
END
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE TRIGGER set_document_path
    BEFORE INSERT ON private.documents
    FOR EACH ROW
    EXECUTE FUNCTION set_document_path ();

CREATE OR REPLACE TRIGGER set_document_updated_at
    BEFORE UPDATE ON private.documents
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at ();

CREATE OR REPLACE VIEW documents AS
SELECT
    id,
    file_id,
    path,
    from_page,
    to_page,
    name,
    status,
    is_deleted
FROM
    private.documents 
WHERE private.documents.is_deleted = false;

GRANT ALL PRIVILEGES ON documents TO insight_worker;
GRANT SELECT, INSERT, UPDATE, DELETE ON documents TO external_user;

CREATE OR REPLACE VIEW pages AS
SELECT
    id,
    file_id,
    index,
    contents
FROM
    private.pages;

GRANT ALL PRIVILEGES ON pages TO insight_worker;
GRANT SELECT ON pages TO external_user;

CREATE OR REPLACE FUNCTION document (pages)
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

