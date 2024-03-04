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
    SELECT
        files.owner_id INTO owner_id
    FROM
        files
    WHERE
        id = NEW.file_id;
    NEW.path = format('%s/%s/%s.pdf', owner_id, NEW.file_id, NEW.id);
    RETURN NEW;
END
$$
LANGUAGE PLPGSQL;

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

