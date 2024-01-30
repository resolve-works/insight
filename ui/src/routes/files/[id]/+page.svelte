
<script>
    import Page from '$lib/Page.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    import Embed from './Embed.svelte';
    export let data;

    const { documents } = data.file;
</script>

<Page class="with-sidebar-right">
    <PDFViewer url={data.url} index={'1'} />
</Page>

<aside>
    <header>
        <h2>{documents.length} embedded document{documents.length == 1 ? '' : 's'}</h2>
    </header>

    {#each documents as document, index}
        <Embed {...document} />
    {/each}
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

    header {
        display: grid;
        align-items: center;
    }
</style>
