
<script lang="ts">
    import Page from '$lib/Page.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    import Document from './Document.svelte';
    import { documents } from './stores.ts'
    import { page } from '$app/stores';
    export let data;

    $documents = data.documents.map(document => ({ original: document, changes: structuredClone(document) }))
    const { access_token } = data;

    function store_documents() {

    }

    function add_document() {
        $documents = [ ...$documents, { original: {}, changes: { from_page: 1, to_page: 1, name: '' }, }]
    }

    $: is_changed = $documents
        .map(({ original, changes }) => JSON.stringify(original) != JSON.stringify(changes))
        .reduce((a, b) => a || b);
</script>

<Page class="with-sidebar-right">
    <PDFViewer url={data.url} index={parseInt($page.url.searchParams.get('page') ?? '1')} />
</Page>

<aside>
    <header>
        {#if $documents.length == 1}
            <h2>Single document</h2>
        {:else}
            <h2>File split in {$documents.length} documents</h2>
        {/if}
    </header>

    <div class="documents">
        {#each $documents as _, index}
            <Document {access_token} {index} pages={data.pages} />
        {/each}

        <button on:click={add_document}>Add split</button>
        {#if is_changed}
            <button class="secondary" on:click={store_documents}>Store changes</button>
        {/if}
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
        border-color: var(--color-subnavigation-darker);
    }
</style>
