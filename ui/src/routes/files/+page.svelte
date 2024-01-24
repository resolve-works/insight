
<script>
    import Layout from '../Layout.svelte';
    import Pagestream from './Pagestream.svelte';
    import Uploader from './Uploader.svelte';
    import Upload from './Upload.svelte';
    import { uploads } from '$lib/stores.ts';

    export let data;
</script>


<Layout>
    <main>
        <Uploader />

        {#each $uploads as file }
            <Upload file={file} />
        {/each}

        {#each data.pagestreams as pagestream }
            <Pagestream name={pagestream.name} />
        {/each}
    </main>
</Layout>

<style>
</style>
