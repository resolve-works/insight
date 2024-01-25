
create type file_status as enum ('uploading', 'ingesting', 'idle');

create table if not exists private.files (
    id uuid default gen_random_uuid(),
    owner_id uuid not null,

    path text generated always as (owner_id::text || '/' || id::text || '.pdf') stored,
    name text not null,
    status file_status not null default 'uploading',

    created_at timestamp with time zone default current_timestamp,
    updated_at timestamp with time zone default current_timestamp,

    primary key (id)
);
grant select, insert on private.files to external_user;

create table private.documents (
    id uuid default gen_random_uuid(),
    owner_id uuid not null,
    file_id uuid not null,
    path text generated always as (owner_id::text || '/' || file_id::text || '/' || id::text || '.pdf') stored,
    from_page integer not null,
    to_page integer not null,
    name text not null,

    primary key (id),
    foreign key(file_id) references private.files (id) match simple on delete restrict not valid
);
grant select on private.documents to external_user;
grant select, insert on private.documents to internal_worker;


create table if not exists private.prompts (
    id uuid default gen_random_uuid(),
    query text not null,
    response text,

    primary key (id)
);
grant select, update, insert on private.prompts to external_user;


create table if not exists private.sources (
    prompt_id uuid not null,
    file_id uuid not null,
    index integer not null,
    score float not null,

    constraint fk_prompt foreign key(prompt_id) references private.prompts(id) on delete cascade,
    constraint fk_file foreign key(file_id) references private.files(id) on delete cascade
);
grant select, insert on private.sources to external_user;

