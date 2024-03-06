
<script lang="ts">
    import Page from '$lib/Page.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    import Document from './Document.svelte';
    import { existing, changed, created, documents } from './stores.ts'
    import { page } from '$app/stores';
    import { enhance } from '$app/forms';

    export let data;
    $: $existing = data.documents;
    $: is_changed = $documents.some(document => document.is_changed)

    async function store() {
        // Clear stores that track form state
        return async ({ update }) => {
			await update();
            $changed = {};
            $created = [];
        }
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

    <form method="POST" action="?/store" use:enhance={store}>
        {#each $documents as document}
            <Document {document} pages={data.pages} />
        {/each}

        <!--TODO progressive enhance-->
        <button on:click|preventDefault={add}>Add split</button>
        {#if is_changed}
            <button class="secondary">Store changes</button>
        {/if}
    </form>
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
