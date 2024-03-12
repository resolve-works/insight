
CREATE TYPE file_status AS ENUM (
    'analyzing'
);

CREATE TABLE IF NOT EXISTS private.files (
    id uuid DEFAULT gen_random_uuid (),
    owner_id uuid NOT NULL,
    path text NOT NULL,
    name text NOT NULL,
    number_of_pages integer,
    status file_status DEFAULT 'analyzing',
    is_uploaded boolean NOT NULL DEFAULT false,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

GRANT ALL PRIVILEGES ON private.files TO insight_worker;

CREATE OR REPLACE FUNCTION set_file_path ()
    RETURNS TRIGGER
    AS $$
BEGIN
    -- TODO - name files with name
    NEW.path = format('%s/%s.pdf', NEW.owner_id, NEW.id);
    RETURN NEW;
END
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE TRIGGER set_file_owner
    BEFORE INSERT ON private.files
    FOR EACH ROW
    EXECUTE FUNCTION set_owner ();

CREATE OR REPLACE TRIGGER set_file_path
    BEFORE INSERT ON private.files
    FOR EACH ROW
    EXECUTE FUNCTION set_file_path ();

CREATE OR REPLACE TRIGGER set_file_updated_at
    BEFORE UPDATE ON private.files
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at ();

CREATE OR REPLACE VIEW files AS
SELECT
    id,
    owner_id,
    name,
    path,
    number_of_pages,
    is_uploaded,
    status,
    created_at,
    updated_at,
    is_deleted
FROM
    private.files 
WHERE private.files.is_deleted = false;

GRANT ALL PRIVILEGES ON files TO insight_worker;
GRANT SELECT, INSERT, UPDATE, DELETE ON files TO external_user;

