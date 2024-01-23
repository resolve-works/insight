
<script>
    import Layout from '../Layout.svelte';
    import Pagestream from './Pagestream.svelte';
    import Uploader from './Uploader.svelte';
    import Upload from './Upload.svelte';
    import { uploads } from './stores.ts';

    export let data;
</script>


<Layout>
    <main>
        <Uploader />

        {#each $uploads as upload }
            <Upload upload={upload} />
        {/each}

        {#each data.pagestreams as pagestream }
            <Pagestream {...pagestream} />
        {/each}
    </main>
</Layout>

<style>
</style>
