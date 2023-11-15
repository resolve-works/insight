
create or replace function create_pagestream(name text) returns json language plpython3u as $$
    import json
    plan = plpy.prepare("INSERT INTO private.pagestream (name) VALUES ($1)", ["text"])
    plpy.execute(plan, [name])

    return json.dumps({ 'name': name })
$$;

create table if not exists private.pagestream (
    id uuid not null default gen_random_uuid(),
    name text not null,
    is_merged boolean not null default false,
    status pagestream_status not null default 'uploading',
    primary key (id)
);

grant insert on private.pagestream to web_user;

