begin;

\set pg_api_user `echo $PG_API_USER`
\set pg_api_password `echo $PG_API_PASSWORD`
\set pg_ingest_user `echo $PG_INGEST_USER`
\set pg_ingest_password `echo $PG_INGEST_PASSWORD`
\set web_anon `echo $PG_ANONYMOUS`

create role :web_anon nologin;
create role web_user nologin;

create role :pg_api_user noinherit login password :'pg_api_password';
grant :web_anon to :pg_api_user;
grant web_user to :pg_api_user;

create role :pg_ingest_user noinherit login password :'pg_ingest_password';

create schema insight;
grant usage on schema insight to web_user;

create table insight.pagestreams (
    id uuid not null default gen_random_uuid(),
    path text not null,
    name text not null,
    primary key (id)
);
grant all on insight.pagestreams to web_user;

create or replace function pagestreams_notify()
returns trigger language plpgsql as
$$
begin
    perform pg_notify('pagestreams', to_json(new)::text);
    return null;
end;
$$;

create trigger pagestreams_notify
after insert on pagestreams for each row 
execute function pagestreams_notify();

create table insight.files (
    id uuid not null default gen_random_uuid(),
    pagestream_id uuid not null,
    name text not null,

    primary key (id),
    foreign key(pagestream_id) references insight.pagestreams (id) match simple on delete restrict not valid
);
grant all on insight.files to web_user;
grant all on insight.files to :pg_ingest_user;

commit;
