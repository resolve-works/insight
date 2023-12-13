
<script>
    import Layout from '../../../Layout.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    import { page } from '$app/stores';
    export let data;
</script>

<Layout>
    <PDFViewer url={data.url} index={$page.params.page} />
</Layout>

<style>
    header {
        display: grid;
        grid-template-columns: auto auto;
        justify-content: space-between;
        align-items: center;
        padding-bottom: var(--padding-y);
    }
</style>
