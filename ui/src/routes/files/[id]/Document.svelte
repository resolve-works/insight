
<script lang="ts">
    import { getContext } from 'svelte';
    import Icon from '$lib/Icon.svelte';
    import { invalidate } from '$app/navigation';
    import { created, changed } from './stores.ts'
    import type { DocumentInput } from './stores.ts'
    import { ssp, queryParam } from 'sveltekit-search-params'
    import type { Insight } from '$lib/insight.ts'; 
    
    export let pages: number
    export let document: DocumentInput;
    
    const insight: Insight = getContext('insight');

    // Document can be editted when it's new, or when it's not being ingested
    $: is_disabled = 'status' in document.original && document.original.status != 'idle'

	let page = queryParam('page', ssp.number());
    async function go_to_page(e: Event) {
        $page = parseInt((e.target as HTMLInputElement).value)
        $changed = $changed;
    }

    async function remove() {
        // Mark model for deletion
        await insight.patch('/documents', document.original.id, { status: 'deleting' })
        invalidate(url => url.pathname == '/api/v1/documents')
        // Trigger delete job
        await insight.rpc('/delete_document', document.original.id)
    }

    function cancel_adding() {
        $created = $created.filter(obj => ! Object.is(obj, document.changes))
    }

    function cancel_changes() {
        $changed[document.original.id] = structuredClone(document.original);
    }
</script>

<div class="embed">
    <input 
        type="text" 
        placeholder="Document name (leave empty to generate)"
        disabled={is_disabled}
        on:change={() => $changed = $changed}
        bind:value={document.changes.name}
        class:changed={document.changes.name != document.original.name} 
        />

    <div class="row">
        <input 
            type="number" 
            bind:value={document.changes.from_page} 
            on:change={go_to_page}
            disabled={is_disabled}
            class:changed={document.changes.from_page != document.original.from_page} 
            min="1" 
            max={document.changes.to_page} 
            />
        <span>to</span>
        <input 
            type="number" 
            bind:value={document.changes.to_page} 
            on:change={go_to_page}
            disabled={is_disabled}
            class:changed={document.changes.to_page != document.original.to_page} 
            min={document.changes.from_page}
            max={pages} 
            />

        {#if document.original.id}
            {#if is_disabled}
                <span class="status">
                    <Icon class="gg-loadbar" /> {document.original.status}
                </span>
            {:else}
                {#if document.is_changed}
                    <button class="outline" on:click={cancel_changes}>Cancel changes</button>
                {:else}
                    <button class="outline" on:click={remove}>Remove</button>
                {/if}
            {/if}
        {:else}
            <button class="outline" on:click={cancel_adding}>Cancel adding</button>
        {/if}
    </div>
</div>

<style>
    .embed {
        margin-bottom: 1rem;
    }

    button,
    input {
        border-color: var(--color-subnavigation-darker);
    }

    input.changed {
        border-color: var(--color-secondary);
        background: #FFFAEB;
    }

    input[type=text] {
        width: 100%;
        margin-bottom: 0.5rem;
    }

    input[type=number] {
        width: 6rem;
        padding-right: 0.5rem;
    }

    .row,
    .status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .status {
        margin-left: auto;
    }

    button {
        margin-left: 0.5rem;
    }

    .outline {
        margin-left: auto;
        background: none;
        color: var(--text-color-light);
    }
</style>
