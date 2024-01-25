
<script>
    import Layout from '$lib/Layout.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    import { page } from '$app/stores';
    export let data;
</script>

<Layout>
    <article>
        <PDFViewer url={data.url} index={$page.url.searchParams.get('page') ?? '1'} />
    </article>
</Layout>

<style>
    article {
        display: grid;
        justify-content: center;
    }
</style>
