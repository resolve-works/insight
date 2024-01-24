
<script lang="ts">
    import { onMount } from 'svelte';
    import Card from '$lib/Card.svelte';
    import { uploads } from '$lib/stores';
    import { invalidate } from '$app/navigation';

    export let file: File;

    let total = file.size;
    let loaded = 0;

    onMount(async () => {
        const response = await fetch('/files', { method: 'POST' })
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
            const { id, path } = pagestream;
            const response = await fetch('/files', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, path, name: file.name })
            })
            if(response.status == 200) {
                uploads.update(uploads => uploads.filter(f => f.name != file.name))
            }

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
