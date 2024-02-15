
create or replace trigger set_file_owner before insert on private.files for each row execute function set_owner();
create or replace trigger set_prompt_owner before insert on private.prompts for each row execute function set_owner();
create or replace trigger set_document_owner before insert on private.documents for each row execute function set_owner();

create or replace trigger set_file_updated_at before update on private.files for each row execute function set_updated_at();
create or replace trigger set_prompt_updated_at before update on private.prompts for each row execute function set_updated_at();
create or replace trigger set_document_updated_at before update on private.documents for each row execute function set_updated_at();

