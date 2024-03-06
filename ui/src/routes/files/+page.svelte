
<script>
    import Page from '$lib/Page.svelte';
    import File from './File.svelte';
    import Uploader from './Uploader.svelte';
    import Upload from './Upload.svelte';
    import { uploads } from './stores.ts';

    export let data;
</script>

<Page>
    <Uploader />

    {#each $uploads as upload (upload.name) }
        <Upload upload={upload} />
    {/each}

    {#each data.files as file (file.id)}
        <File {...file} />
    {/each}
</Page>

