begin;

\set authenticator `echo $PGUSER`
\set authenticator_password `echo $PGPASSWORD`
\set web_anon `echo $PGRST_DB_ANON_ROLE`

create role :web_anon nologin;
create role web_user nologin;

create role :authenticator noinherit login password :'authenticator_password';
grant :web_anon to :authenticator;
grant web_user to :authenticator;

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

commit;
