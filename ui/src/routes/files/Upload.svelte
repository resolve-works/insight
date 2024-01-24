
<script lang="ts" context="module">
    export class Upload {
        file: File;

        constructor(file: File) {
            this.file = file;
        }
    }
</script>

<script lang="ts">
    import Card from '$lib/Card.svelte';

    export let upload: Upload;
</script>

<Card>
    <h3>{upload.file.name}</h3>
    <p>Uploading...</p>
    <progress value="70" max="100"></progress>
</Card>

<style>
    progress {
        width: 100%;
        accent-color: var(--color-primary);
    }
</style>
