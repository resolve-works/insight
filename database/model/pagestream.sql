
create or replace function create_pagestream(name text) returns json language plpython3u as $$
    import json
    from os import environ as env
    from minio import Minio

    plan = plpy.prepare("insert into private.pagestream (name) values ($1) returning *", ["text"])
    results = plpy.execute(plan, [name])

    client = Minio(
        env.get("STORAGE_ENDPOINT"), 
        access_key=env.get("STORAGE_ACCESS_KEY"), 
        secret_key=env.get("STORAGE_SECRET_KEY"),
        secure=env.get("STORAGE_SECURE").lower() == "true"
    )
    results[0]["url"] = client.presigned_put_object(env.get("STORAGE_BUCKET"), results[0]["id"])
    return json.dumps(results[0])
$$;

create table if not exists private.pagestream (
    id uuid not null default gen_random_uuid(),
    name text not null,
    is_merged boolean not null default false,
    primary key (id)
);

grant select, insert on private.pagestream to web_user;

