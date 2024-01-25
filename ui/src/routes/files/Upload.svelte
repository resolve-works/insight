
<script lang="ts">
    import { onMount } from 'svelte';
    import Card from '$lib/Card.svelte';
    import { uploads } from '$lib/stores';
    import { invalidate } from '$app/navigation';

    export let file: File
    export let access_token: string

    let total = file.size;
    let loaded = 0;

    onMount(async () => {
        const response = await fetch('/files', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: file.name })
        })
        const pagestream = await response.json()

        // https://github.com/whatwg/fetch/issues/607
        // Fetch doesn't allow tracking progress for now
        const xhr = new XMLHttpRequest()
        xhr.upload.addEventListener("progress", e => {
            loaded = e.loaded;
            total = e.total;
        });

        // When upload is done, strip upload
        xhr.upload.addEventListener("loadend", async () => {
            const patch_response = await fetch(`/api/v1/pagestream?id=eq.${pagestream.id}`, { 
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
            const ingest_response = await fetch('/api/v1/rpc/ingest_pagestream', { 
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${access_token}`,
                },
                body: JSON.stringify({ id: pagestream.id })
            })
            if(ingest_response.status != 204) {
                throw new Error('Could not trigger ingest of file')
            }

            // TODO - Proper error handling. The web is unstable, uploads fail

            uploads.update(uploads => uploads.filter(f => f != file))
            await invalidate(url => url.pathname == '/api/v1/pagestream')
        });

        // TODO - error

        xhr.open("PUT", pagestream.url, true);
        xhr.send(file);
    })
</script>

<Card>
    <h3>{file.name}</h3>
    <p>Uploading...</p>
    <progress value={loaded} max={total}></progress>
</Card>

<style>
    progress {
        width: 100%;
        accent-color: var(--color-primary);
    }
</style>
