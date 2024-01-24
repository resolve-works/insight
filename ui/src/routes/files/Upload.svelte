
<script lang="ts">
    import { onMount } from 'svelte';
    import Card from '$lib/Card.svelte';

    export let file: File;

    onMount(async () => {
        console.log(`Uploading ${file.name}`)
    
        const response = await fetch('/files', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: file.name }),
        })

        console.log(await response.json())
    })
</script>

<Card>
    <h3>{file.name}</h3>
    <p>Uploading...</p>
    <progress value="70" max="100"></progress>
</Card>

<style>
    progress {
        width: 100%;
        accent-color: var(--color-primary);
    }
</style>
