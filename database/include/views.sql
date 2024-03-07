CREATE OR REPLACE VIEW files AS
SELECT
    id,
    owner_id,
    name,
    path,
    number_of_pages,
    status,
    created_at,
    updated_at
FROM
    private.files;

GRANT SELECT, INSERT, UPDATE, DELETE ON files TO external_user;

CREATE OR REPLACE VIEW documents AS
SELECT
    id,
    file_id,
    path,
    from_page,
    to_page,
    name,
    status
FROM
    private.documents;

GRANT SELECT, INSERT, UPDATE, DELETE ON documents TO external_user;

CREATE OR REPLACE VIEW prompts AS
SELECT
    *
FROM
    private.prompts;

GRANT SELECT, INSERT, UPDATE ON prompts TO external_user;

CREATE OR REPLACE VIEW sources AS
SELECT
    *
FROM
    private.sources;

GRANT SELECT, INSERT ON sources TO external_user;

