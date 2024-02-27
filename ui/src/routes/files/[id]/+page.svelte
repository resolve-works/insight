
<script lang="ts">
    import { onMount, getContext } from 'svelte';
    import { invalidate } from '$app/navigation';
    import Page from '$lib/Page.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    import Document from './Document.svelte';
    import { existing, changed, created, documents } from './stores.ts'
    import { page } from '$app/stores';
    import type { Insight } from '$lib/insight.ts';

    export let data;
    $: $existing = data.documents;
    $: is_changed = $documents.some(document => document.is_changed)
    let is_disabled = false;

    const insight: Insight = getContext('insight');

    // TODO - Poor mans event system
    onMount(() => {
        const interval = setInterval(() => {
            invalidate(url => url.pathname == '/api/v1/documents')
        }, 3000)

        return () => {
            clearInterval(interval)
        }
    })

    async function store() {
        is_disabled = true;

        for(const document of $documents.filter(document => document.is_changed)) {
            const changes = {
                ...document.changes,
                // Pages are 0 indexed in database, 1 indexed in inputs as to not confuse the humans
                from_page: document.changes.from_page - 1,
            }

            if('id' in document.original) {
                // Existing documents
                await insight.patch('/documents', document.original.id, changes)
            } else {
                // New documents
                await insight.post('/documents', { ...changes, file_id: data.file_id, })
            }
        }

        // Get new list of documents
        await invalidate(url => url.pathname == '/api/v1/documents')

        // Clear stores that track form state
        $changed = {};
        $created = [];

        is_disabled = false;
    }

    function add() {
        $created = [ ...$created, { from_page: 1, to_page: data.pages, name: '' }]
    }
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
            <Document {document} pages={data.pages} />
        {/each}

        <button on:click={add}>Add split</button>
        {#if is_changed}
            <button class="secondary" disabled={is_disabled} on:click={store}>Store changes</button>
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
