
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
