
create type file_status as enum ('uploading', 'analyzing', 'deleting', 'idle');

create table if not exists private.files (
    id uuid default gen_random_uuid(),
    owner_id uuid not null,

    path text generated always as (owner_id::text || '/' || id::text || '.pdf') stored,
    name text not null,
    pages integer,

    status file_status not null default 'uploading',

    created_at timestamp with time zone default current_timestamp,
    updated_at timestamp with time zone default current_timestamp,

    primary key (id)
);
alter table private.files replica identity full;

create type document_status as enum ('ingesting', 'deleting', 'idle');

create table private.documents (
    id uuid default gen_random_uuid(),
    owner_id uuid not null,
    file_id uuid not null,

    name text,
    path text generated always as (owner_id::text || '/' || file_id::text || '/' || id::text || '.pdf') stored,
    from_page integer not null,
    to_page integer not null,

    status document_status not null default 'idle',

    created_at timestamp with time zone default current_timestamp,
    updated_at timestamp with time zone default current_timestamp,

    primary key (id),
    foreign key (file_id) references private.files (id) on delete restrict
);


create type prompt_status as enum ('answering', 'idle');

create table if not exists private.prompts (
    id uuid default gen_random_uuid(),
    owner_id uuid not null,

    query text not null,
    similarity_top_k integer not null default 3,
    response text,

    status prompt_status not null default 'answering',

    created_at timestamp with time zone default current_timestamp,
    updated_at timestamp with time zone default current_timestamp,

    primary key (id)
);


create table if not exists private.sources (
    prompt_id uuid not null,
    file_id uuid not null,
    index integer not null,
    score float not null,

    foreign key (prompt_id) references private.prompts(id) on delete cascade,
    foreign key (file_id) references private.files(id) on delete cascade
);

