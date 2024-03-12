
CREATE TYPE prompt_status AS enum (
    'answering'
);

CREATE TABLE IF NOT EXISTS private.prompts (
    id bigserial,
    owner_id uuid NOT NULL,
    query text NOT NULL,
    similarity_top_k integer NOT NULL DEFAULT 3,
    response text,
    status prompt_status DEFAULT 'answering',
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

GRANT ALL PRIVILEGES ON private.prompts TO insight_worker;
GRANT ALL PRIVILEGES ON private.prompts_id_seq TO insight_worker;
GRANT usage, SELECT ON private.prompts_id_seq TO external_user;

CREATE TABLE IF NOT EXISTS private.sources (
    id bigserial,
    prompt_id bigint NOT NULL,
    page_id bigint NOT NULL,
    similarity float NOT NULL,
    FOREIGN KEY (prompt_id) REFERENCES private.prompts (id) ON DELETE CASCADE,
    FOREIGN KEY (page_id) REFERENCES private.pages (id) ON DELETE CASCADE,
    PRIMARY KEY (id)
);

GRANT ALL PRIVILEGES ON private.sources TO insight_worker;
GRANT ALL PRIVILEGES ON private.sources_id_seq TO insight_worker;
GRANT usage, SELECT ON private.sources_id_seq TO external_user;

CREATE OR REPLACE TRIGGER set_prompt_owner
    BEFORE INSERT ON private.prompts
    FOR EACH ROW
    EXECUTE FUNCTION set_owner ();

CREATE OR REPLACE TRIGGER set_prompt_updated_at
    BEFORE UPDATE ON private.prompts
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at ();

CREATE OR REPLACE VIEW prompts AS
SELECT
    *
FROM
    private.prompts;

GRANT SELECT, INSERT ON prompts TO external_user;

CREATE OR REPLACE VIEW sources AS
SELECT
    *
FROM
    private.sources;

GRANT SELECT ON sources TO external_user;

