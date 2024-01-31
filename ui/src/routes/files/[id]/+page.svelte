
<script context="module" lang="ts">
    export type Document = {
        id?: string,
        name?: string,
        from_page: number,
        to_page: number,
    }

    export type EmbedData = {
        is_edited: boolean,
        document: Document,
    }
</script>

<script lang="ts">
    import Page from '$lib/Page.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    import Embed from './Embed.svelte';
    import { writable } from 'svelte/store';
    import type { Writable } from 'svelte/store';
    export let data;


    export const embeds: Writable<EmbedData[]> = writable([]);

    const { documents } = data.file;
    embeds.set(documents.map((document: Document) => ({ document, is_edited: false })))

    function store_embeds() {

    }

    function add_embed() {
        embeds.update(embeds => {
            const document = {
                from_page: 0, 
                to_page: 1,
            }

            return [
                ...embeds,
                { document, is_edited: true },
            ]
        })
    }
</script>

<Page class="with-sidebar-right">
    <PDFViewer url={data.url} index={'1'} />
</Page>

<aside>
    <header>
        <h2>{$embeds.length} embedded document{$embeds.length == 1 ? '' : 's'}</h2>
    </header>

    <div>
        {#each $embeds as embed, index}
            <Embed embeds={embeds} {...embed} index={index} />
        {/each}

        <button on:click={add_embed}>Add split</button>
        <button class="secondary" on:click={store_embeds}>Store splits</button>
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

    div {
        overflow-x: hidden;
        margin-bottom: 1rem;
    }

    button {
        display: block;
        width: 100%;
        margin-top: 1rem;
    }
</style>
