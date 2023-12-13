
<script>
    import Layout from '../../../Layout.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    import { page } from '$app/stores';
    export let data;
</script>

<Layout>
    <article>
        <PDFViewer url={data.url} index={$page.params.page} />
    </article>
</Layout>

<style>
    article {
        display: grid;
        justify-content: center;
    }
</style>
