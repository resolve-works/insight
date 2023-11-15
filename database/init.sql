begin;

\set pg_api_user `echo $PG_API_USER`
\set pg_api_password `echo $PG_API_PASSWORD`
\set pg_worker_user `echo $PG_WORKER_USER`
\set pg_worker_password `echo $PG_WORKER_PASSWORD`

create schema insight;
create schema private;

create extension if not exists vector;

create role web_anon nologin;
create role web_user nologin;
grant usage on schema insight to web_user;

create role :pg_api_user noinherit login password :'pg_api_password';
grant web_anon to :pg_api_user;
grant web_user to :pg_api_user;

create role :pg_worker_user noinherit login password :'pg_worker_password';
alter role :pg_worker_user set search_path = "$user", insight;
grant usage on schema insight to :pg_worker_user;
grant usage on schema private to :pg_worker_user;

create or replace function notify()
returns trigger language plpgsql as
$$
begin
    perform pg_notify(tg_table_name, to_json(new)::text);
    return null;
end;
$$;

create table insight.pagestream (
    id uuid not null default gen_random_uuid(),
    path text not null,
    name text not null,
    is_merged boolean not null default false,
    primary key (id)
);
grant all on insight.pagestream to web_user;
grant all on insight.pagestream to :pg_worker_user;

create trigger notify_pagestream
after insert on insight.pagestream for each row 
execute function notify();

create table insight.file (
    id uuid not null default gen_random_uuid(),
    pagestream_id uuid not null,
    from_page integer not null,
    to_page integer not null,
    name text not null,

    primary key (id),
    foreign key(pagestream_id) references insight.pagestream (id) match simple on delete restrict not valid
);
grant all on insight.file to web_user;
grant all on insight.file to :pg_worker_user;

create trigger notify_file
after insert on insight.file for each row 
execute function notify();

create table insight.prompt (
    id uuid not null default gen_random_uuid(),
    query text,

    primary key (id)
);
grant all on insight.prompt to web_user;
grant all on insight.prompt to :pg_worker_user;

create trigger notify_prompt
after insert on insight.prompt for each row 
execute function notify();

create table insight.response (
    id uuid not null default gen_random_uuid(),
    prompt_id uuid not null,
    response text,

    primary key (id),
    foreign key(prompt_id) references insight.prompt (id) match simple on delete restrict not valid
);
grant all on insight.response to web_user;
grant all on insight.response to :pg_worker_user;


create table private.page (
    id bigint not null,
    text character varying not null,
    metadata_ json,
    node_id character varying,
    embedding vector(1536)
);
grant all on private.page to :pg_worker_user;

create sequence private.page_id_seq
    start with 1
    increment by 1
    no minvalue
    no maxvalue
    cache 1;

grant all on private.page_id_seq to :pg_worker_user;

alter sequence private.page_id_seq owned by private.page.id;
alter table private.page alter column id set default nextval('private.page_id_seq'::regclass);
alter table private.page add constraint page_pkey primary key (id);

commit;
