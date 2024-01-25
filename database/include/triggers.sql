
create or replace trigger set_file_owner before insert on private.files for each row execute function set_file_owner();
create or replace trigger set_updated_at before update on private.files for each row execute function set_updated_at()

