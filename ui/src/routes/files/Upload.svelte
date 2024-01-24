
<script lang="ts">
    import { onMount } from 'svelte';
    import Card from '$lib/Card.svelte';
    import { uploads } from '$lib/stores';

    export let file: File;

    let total = file.size;
    let loaded = 0;

    onMount(async () => {
        const pagestream_response = await fetch('/files', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: file.name }),
        })
    
        const pagestream = await pagestream_response.json()

        // https://github.com/whatwg/fetch/issues/607
        // Fetch doesn't allow tracking progress for now
        const xhr = new XMLHttpRequest()
        xhr.upload.addEventListener("progress", e => {
            loaded = e.loaded;
            total = e.total;
        });

        // When upload is done, strip upload
        xhr.upload.addEventListener("loadend", e => {
            uploads.update(uploads => uploads.filter(f => f != file))
        });

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
