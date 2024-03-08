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

GRANT SELECT, INSERT, UPDATE, DELETE ON files TO external_user;

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

GRANT SELECT, INSERT, UPDATE, DELETE ON documents TO external_user;

CREATE OR REPLACE VIEW pages AS
SELECT
    id,
    file_id,
    index,
    contents
FROM
    private.pages;

GRANT SELECT ON pages TO external_user;

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

