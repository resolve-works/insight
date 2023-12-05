
create or replace function ingest_pagestream(id uuid) returns void language plpython3u as $$
    import json
    plan = plpy.prepare("select * from private.pagestream where id=$1", ["uuid"])
    results = plpy.execute(plan, [id])

    plan = plpy.prepare("notify pagestream, '{payload}'".format(payload=json.dumps(results[0])))
    plpy.execute(plan)
$$;

create table if not exists private.pagestream (
    id uuid default gen_random_uuid(),
    name text not null,
    is_merged boolean not null default false,
    primary key (id)
);
grant select, insert on private.pagestream to external_user;

create or replace view pagestream as select * from private.pagestream;
grant insert, select on pagestream to external_user;
