
<script lang="ts">
    import { onMount, getContext } from 'svelte';
    import Card from '$lib/Card.svelte';
    import { uploads } from './stores.ts';
    import { invalidate } from '$app/navigation';

    import type { Insight } from '$lib/insight';
    const insight: Insight = getContext('insight')

    export let upload: File

    let total = upload.size;
    let loaded = 0;

    onMount(async () => {
        const file = await insight.post('/files', { name: upload.name })

        // Get presigned upload url
        const response = await fetch('/sign', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
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
            await insight.patch('/files', file.id, { status: 'analyzing' })

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
