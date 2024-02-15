
<script lang="ts">
    import Icon from '$lib/Icon.svelte';
    import { invalidate } from '$app/navigation';
    import { created, changed } from './stores.ts'
    import type { DocumentInput } from './stores.ts'
    import { ssp, queryParam } from 'sveltekit-search-params'
    export let pages: number
    export let document: DocumentInput;
    export let access_token: string

    $: is_changed = JSON.stringify(document.original) != JSON.stringify(document.changes)
    $: can_edit = ! ('status' in document.original) || document.original.status == 'idle'

	let page = queryParam('page', ssp.number());
    async function go_to_page(e: Event) {
        $page = parseInt((e.target as HTMLInputElement).value)
        $changed = $changed;
    }

    async function remove() {
        // Mark model for deletion
        const patch_response = await fetch(`/api/v1/documents?id=eq.${document.original.id}`, { 
            method: 'PATCH',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,
            },
            body: JSON.stringify({ status: 'deleting' })
        })
        if(patch_response.status != 204) {
            throw new Error('Could not mark document as deleting')
        }

        invalidate(url => url.pathname == '/api/v1/documents')

        // Trigger delete job
        const ingest_response = await fetch('/api/v1/rpc/delete_document', { 
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,
            },
            body: JSON.stringify({ id: document.original.id })
        })
        if(ingest_response.status != 204) {
            throw new Error('Could not trigger delete job for document')
        }
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
        placeholder="Document name"
        disabled={!can_edit}
        on:change={() => $changed = $changed}
        bind:value={document.changes.name}
        class:changed={document.changes.name != document.original.name} 
        />

    <div class="row">
        <input 
            type="number" 
            bind:value={document.changes.from_page} 
            on:change={go_to_page}
            disabled={!can_edit}
            class:changed={document.changes.from_page != document.original.from_page} 
            min="1" 
            max={document.changes.to_page} 
            />
        <span>to</span>
        <input 
            type="number" 
            bind:value={document.changes.to_page} 
            on:change={go_to_page}
            disabled={!can_edit}
            class:changed={document.changes.to_page != document.original.to_page} 
            min={document.changes.from_page}
            max={pages} 
            />

        {#if document.original.id}
            {#if ! can_edit}
                <span class="status">
                    <Icon class="gg-loadbar" /> {document.original.status}
                </span>
            {:else}
                {#if is_changed}
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
