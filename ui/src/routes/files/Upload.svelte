
<script lang="ts">
    import { onMount } from 'svelte';
    import Card from '$lib/Card.svelte';
    import { uploads } from './stores.ts';
    import { invalidate } from '$app/navigation';

    export let upload: File

    let total = upload.size;
    let loaded = 0;

    onMount(async () => {
        // https://github.com/whatwg/fetch/issues/607
        // Fetch doesn't allow tracking progress for now
        const xhr = new XMLHttpRequest()
        xhr.upload.addEventListener("progress", e => {
            loaded = e.loaded;
            total = e.total;
        });

        // When upload is done, strip upload
        xhr.upload.addEventListener("loadend", async () => {
            uploads.update(uploads => uploads.filter(f => f != upload))
            invalidate('api:files')
        });

        xhr.open("POST", '?/upload', true);
        const data = new FormData();
        data.append('files', upload)
        xhr.send(data);
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
