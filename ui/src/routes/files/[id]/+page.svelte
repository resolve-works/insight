
<script>
    import Page from '$lib/Page.svelte';
    import Meta from './Meta.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    export let data;
</script>

<Page class="with-sidebar-right">
    <PDFViewer url={data.url} index={'1'} />
</Page>

<aside>
    <Meta {...data.file} />
</aside>

<style>
    aside {
        background: var(--color-primary);
        display: grid;
        grid-row: 1 / 4;
        grid-template-rows: subgrid;
        padding: 0 var(--padding-x);
        color: var(--text-color-light);
    }
</style>
