
<script>
    import { onMount } from 'svelte'
    import { invalidate } from '$app/navigation';
    import Layout from '$lib/Layout.svelte';
    import File from './File.svelte';
    import Uploader from './Uploader.svelte';
    import Upload from './Upload.svelte';
    import { uploads } from '$lib/stores.ts';

    export let data;
    const { access_token } = data;

    // TODO - Poor mans event system
    onMount(() => {
        const interval = setInterval(() => {
            invalidate(url => url.pathname == '/api/v1/files')
        }, 5000)

        return () => {
            clearInterval(interval)
        }
    })
</script>


<Layout>
    <main>
        <Uploader />

        {#each $uploads as upload (upload.name) }
            <Upload upload={upload} access_token={access_token} />
        {/each}

        {#each data.files as file (file.id)}
            <File {...file} />
        {/each}
    </main>
</Layout>

<style>
</style>
