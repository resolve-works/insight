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
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

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
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (file_id) REFERENCES private.files (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS private.pages (
    id bigserial,
    file_id uuid NOT NULL,
    index integer NOT NULL,
    contents text NOT NULL,
    embedding vector (1536),
    FOREIGN KEY (file_id) REFERENCES private.files (id) ON DELETE CASCADE,
    PRIMARY KEY (id)
);

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

CREATE TABLE IF NOT EXISTS private.sources (
    id bigserial,
    prompt_id bigint NOT NULL,
    page_id bigint NOT NULL,
    similarity float NOT NULL,
    FOREIGN KEY (prompt_id) REFERENCES private.prompts (id) ON DELETE CASCADE,
    FOREIGN KEY (page_id) REFERENCES private.pages (id) ON DELETE CASCADE,
    PRIMARY KEY (id)
);

