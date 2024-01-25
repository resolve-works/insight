
create or replace view pagestreams as 
    select id, owner_id, name, path, status, created_at, updated_at from private.pagestreams;
grant select, insert, update on pagestreams to external_user;
grant select, update on pagestreams to internal_worker;

create or replace view documents as 
    select id, owner_id, pagestream_id, path, from_page, to_page, name from private.documents;
grant select on documents to external_user;
grant select, insert on documents to internal_worker;

create or replace view source as select * from private.source;
grant select, insert on source to external_user;

create or replace view prompt as select * from private.prompt;
grant select, insert on prompt to external_user;

