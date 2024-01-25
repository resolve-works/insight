
<script>
    import Layout from '$lib/Layout.svelte';
    import Meta from './Meta.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    export let data;
</script>

<Layout>
    <Meta {...data.file} slot="subnav" />

    <article>
        <PDFViewer url={data.url} index={'1'} />
    </article>
</Layout>

<style>
    article {
        display: grid;
        justify-content: center;
    }
</style>
