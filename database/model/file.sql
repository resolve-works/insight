

create table private.file (
    id uuid default gen_random_uuid(),
    pagestream_id uuid not null,
    from_page integer not null,
    to_page integer not null,
    name text not null,

    primary key (id),
    foreign key(pagestream_id) references private.pagestream (id) match simple on delete restrict not valid
);
grant select on private.file to insight_user;
grant select, insert on private.file to insight_worker;

create view public.file as select * from private.file;
grant select on public.file to insight_user;
grant select, insert on public.file to insight_worker;
