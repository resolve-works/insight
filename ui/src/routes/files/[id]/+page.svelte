
<script lang="ts">
    import Page from '$lib/Page.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    import Document from './Document.svelte';
    import { documents } from './stores.ts'
    export let data;

    documents.set(data.file.documents)

    function store_documents() {

    }

    function add_document() {
        documents.update(documents => {
            return [ ...documents, {}, ]
        })
    }
</script>

<Page class="with-sidebar-right">
    <PDFViewer url={data.url} index={'1'} />
</Page>

<aside>
    <header>
        <h2>{$documents.length} embedded document{$documents.length == 1 ? '' : 's'}</h2>
    </header>

    <div class="documents">
        {#each $documents as document, index}
            <Document {document} {index} />
        {/each}

        <button on:click={add_document}>Add split</button>
        <button class="secondary" on:click={store_documents}>Store changes</button>
    </div>
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

    button {
        display: block;
        width: 100%;
        margin-top: 1rem;
    }
</style>
