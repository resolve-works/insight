
create or replace function ingest_pagestream(id uuid) returns void language plpython3u as $$
    import json
    plan = plpy.prepare("select * from private.pagestream where id=$1", ["uuid"])
    results = plpy.execute(plan, [id])

    plan = plpy.prepare("notify pagestream, '{payload}'".format(payload=json.dumps(results[0])))
    plpy.execute(plan)
$$;

create or replace function private.pagestream_set_owner() returns trigger language plpgsql as $$
declare
    owner_id uuid := current_setting('request.jwt.claims', true)::json->>'sub';
begin
    new.owner_id = owner_id;
    return new;
end
$$;

create table if not exists private.pagestream (
    id uuid default gen_random_uuid(),
    owner_id uuid not null,
    path text generated always as (owner_id::text || '/' || id::text || '.pdf') stored,
    name text not null,
    primary key (id)
);
grant select, insert on private.pagestream to external_user;

create or replace view pagestream as select * from private.pagestream;
grant insert, select on pagestream to external_user;

create or replace trigger pagestream_set_owner before insert on private.pagestream for each row execute function private.pagestream_set_owner();

