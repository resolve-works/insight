
create or replace view files as 
    select id, owner_id, name, path, status, created_at, updated_at from private.files;
grant select, insert, update on files to external_user;
grant select, update on files to internal_worker;

create or replace view documents as 
    select id, owner_id, file_id, path, from_page, to_page, name from private.documents;
grant select on documents to external_user;
grant select, insert on documents to internal_worker;

create or replace view sources as select * from private.sources;
grant select, insert on sources to external_user;

create or replace view prompts as select * from private.prompts;
grant select, insert on prompts to external_user;

