
create or replace trigger pagestream_set_owner before insert on private.pagestream for each row execute function private.pagestream_set_owner();
create or replace trigger set_updated_at before update on private.pagestream for each row execute function set_updated_at()

