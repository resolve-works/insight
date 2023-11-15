
create table private.file (
    id uuid not null default gen_random_uuid(),
    pagestream_id uuid not null,
    from_page integer not null,
    to_page integer not null,
    name text not null,

    primary key (id),
    foreign key(pagestream_id) references private.pagestream (id) match simple on delete restrict not valid
);
create trigger notify_file after insert on private.file for each row execute function notify();

