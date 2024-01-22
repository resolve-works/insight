
<script>
    import Layout from '../Layout.svelte';
    import Pagestream from './Pagestream.svelte';
    import Uploader from './Uploader.svelte'

    export let data;
</script>


<Layout>
    <main>
        <Uploader />

        {#each data.pagestreams as pagestream }
            <Pagestream {...pagestream} />
        {/each}
    </main>
</Layout>

<style>
</style>
