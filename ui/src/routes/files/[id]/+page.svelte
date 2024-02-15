
<script lang="ts">
    import { onMount } from 'svelte';
    import { invalidate } from '$app/navigation';
    import Page from '$lib/Page.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    import Document from './Document.svelte';
    import { existing, created, documents } from './stores.ts'
    import { page } from '$app/stores';
    export let data;

    $: $existing = data.documents;
    const { access_token } = data;

    // TODO - Poor mans event system
    onMount(() => {
        const interval = setInterval(() => {
            invalidate(url => url.pathname == '/api/v1/documents')
        }, 3000)

        return () => {
            clearInterval(interval)
        }
    })

    function store_documents() {

    }

    function add_document() {
        $created = [ ...$created, { from_page: 1, to_page: 1, name: '' }]
    }

    $: is_changed = $documents.some(document => document.is_changed)
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
        {#each $documents as document}
            <Document {access_token} {document} pages={data.pages} />
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
