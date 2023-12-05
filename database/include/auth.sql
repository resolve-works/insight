
create table private.user (
    id uuid not null,
    email text not null,

    primary key (id)
);
grant select, insert on private.user to external_user;
grant select on private.user to internal_worker;

create or replace function private.upsert_user() returns void language plpgsql as $$
declare
    jwt_id uuid := current_setting('request.jwt.claims', true)::json->>'sub';
    jwt_email text := current_setting('request.jwt.claims', true)::json->>'email';
begin
    insert into private.user (id, email) values (jwt_id, jwt_email) 
        on conflict (id) do update set email=jwt_email;
end
$$;

