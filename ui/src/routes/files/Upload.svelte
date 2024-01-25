
<script lang="ts">
    import { onMount } from 'svelte';
    import Card from '$lib/Card.svelte';
    import { uploads } from '$lib/stores';
    import { invalidate } from '$app/navigation';

    export let upload: File
    export let access_token: string

    let total = upload.size;
    let loaded = 0;

    async function create_file(name: string) {
        const response = await fetch('/api/v1/files', { 
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,
                'Prefer': 'return=representation',
            },
            body: JSON.stringify({ name })
        })
        const files = await response.json()
        return files[0]
    }

    onMount(async () => {
        const file = await create_file(upload.name)

        // Get presigned upload url
        const response = await fetch('/sign', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ method: 'PUT', path: file.path })
        })

        const url = await response.json()

        // https://github.com/whatwg/fetch/issues/607
        // Fetch doesn't allow tracking progress for now
        const xhr = new XMLHttpRequest()
        xhr.upload.addEventListener("progress", e => {
            loaded = e.loaded;
            total = e.total;
        });

        // When upload is done, strip upload
        xhr.upload.addEventListener("loadend", async () => {
            const patch_response = await fetch(`/api/v1/files?id=eq.${file.id}`, { 
                method: 'PATCH',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${access_token}`,
                },
                body: JSON.stringify({ status: 'idle' })
            })
            if(patch_response.status != 204) {
                throw new Error('Could not mark file as uploaded')
            }

            // TODO - Send STOMP message through rabbitmq websocket instead
            const ingest_response = await fetch('/api/v1/rpc/ingest_file', { 
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${access_token}`,
                },
                body: JSON.stringify({ id: file.id })
            })
            if(ingest_response.status != 204) {
                throw new Error('Could not trigger ingest of file')
            }

            // TODO - Proper error handling. The web is unstable, uploads fail

            uploads.update(uploads => uploads.filter(f => f != upload))
            invalidate(url => url.pathname == '/api/v1/files')
        });

        xhr.open("PUT", url, true);
        xhr.send(upload);
    })
</script>

<Card>
    <h3>{upload.name}</h3>
    <p>Uploading...</p>
    <progress value={loaded} max={total}></progress>
</Card>

<style>
    progress {
        width: 100%;
        accent-color: var(--color-primary);
    }
</style>
