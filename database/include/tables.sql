
create table if not exists private.pagestream (
    id uuid not null,
    owner_id uuid not null,
    path text not null,
    name text not null,
    created_at timestamp with time zone default current_timestamp,
    updated_at timestamp with time zone default current_timestamp,

    primary key (id)
);
grant select, insert on private.pagestream to external_user;

create table private.file (
    id uuid default gen_random_uuid(),
    owner_id uuid not null,
    pagestream_id uuid not null,
    path text generated always as (owner_id::text || '/' || pagestream_id::text || '/' || id::text || '.pdf') stored,
    from_page integer not null,
    to_page integer not null,
    name text not null,

    primary key (id),
    foreign key(pagestream_id) references private.pagestream (id) match simple on delete restrict not valid
);
grant select on private.file to external_user;
grant select, insert on private.file to internal_worker;


create table if not exists private.prompt (
    id uuid default gen_random_uuid(),
    query text not null,
    response text,

    primary key (id)
);
grant select, update, insert on private.prompt to external_user;


create table if not exists private.source (
    prompt_id uuid not null,
    pagestream_id uuid not null,
    index integer not null,
    score float not null,

    constraint fk_prompt foreign key(prompt_id) references private.prompt(id) on delete cascade,
    constraint fk_pagestream foreign key(pagestream_id) references private.pagestream(id) on delete cascade
);
grant select, insert on private.source to external_user;

