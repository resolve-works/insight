begin;

\set pg_api_user `echo $PG_API_USER`
\set pg_api_password `echo $PG_API_PASSWORD`
\set pg_ingest_user `echo $PG_INGEST_USER`
\set pg_ingest_password `echo $PG_INGEST_PASSWORD`
\set pg_worker_user `echo $PG_WORKER_USER`
\set pg_worker_password `echo $PG_WORKER_PASSWORD`
\set web_anon `echo $PG_ANONYMOUS`

create schema insight;

create role :web_anon nologin;
create role web_user nologin;

create role :pg_api_user noinherit login password :'pg_api_password';
grant :web_anon to :pg_api_user;
grant web_user to :pg_api_user;

create role :pg_ingest_user noinherit login password :'pg_ingest_password';
alter role :pg_ingest_user set search_path = "$user", insight;
create role :pg_worker_user noinherit login password :'pg_worker_password';
alter role :pg_worker_user set search_path = "$user", insight;

grant usage on schema insight to web_user;
grant usage on schema insight to :pg_ingest_user;
grant usage on schema insight to :pg_worker_user;

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
    primary key (id)
);
grant all on insight.pagestream to web_user;
grant all on insight.pagestream to :pg_ingest_user;

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
grant all on insight.file to :pg_ingest_user;

create trigger notify_file
after insert on insight.file for each row 
execute function notify();

create table insight.page (
    id uuid not null default gen_random_uuid(),
    pagestream_id uuid not null,
    index integer not null,
    content text,

    primary key (id),
    foreign key(pagestream_id) references insight.pagestream (id) match simple on delete restrict not valid
);
grant all on insight.page to web_user;
grant all on insight.page to :pg_ingest_user;
grant all on insight.page to :pg_worker_user;

create trigger notify_page
after insert on insight.page for each row 
execute function notify();

commit;
