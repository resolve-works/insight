
<script>
    import { onMount } from 'svelte'
    import { invalidate } from '$app/navigation';
    import Layout from '../Layout.svelte';
    import Pagestream from './Pagestream.svelte';
    import Uploader from './Uploader.svelte';
    import Upload from './Upload.svelte';
    import { uploads } from '$lib/stores.ts';

    export let data;
    const { access_token } = data;

    // TODO - Poor mans event system
    onMount(() => {
        const interval = setInterval(() => {
            invalidate(url => url.pathname == '/api/v1/pagestream')
        }, 5000)

        return () => {
            clearInterval(interval)
        }
    })
</script>


<Layout>
    <main>
        <Uploader />

        {#each $uploads as file (file.name) }
            <Upload file={file} access_token={access_token} />
        {/each}

        {#each data.pagestreams as pagestream (pagestream.id)}
            <Pagestream {...pagestream} />
        {/each}
    </main>
</Layout>

<style>
</style>
