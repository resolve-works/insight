
create or replace view pagestream as 
    select id, name, path, status, created_at, updated_at from private.pagestream;
grant select, insert, update on pagestream to external_user;

create or replace view file as 
    select id, pagestream_id, path, from_page, to_page, name from private.file;
grant select on file to external_user;
grant select, insert on file to internal_worker;

create or replace view source as select * from private.source;
grant select, insert on source to external_user;

create or replace view prompt as select * from private.prompt;
grant select, insert on prompt to external_user;

