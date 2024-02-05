
<script lang="ts">
    import Icon from '$lib/Icon.svelte';
    import { invalidate } from '$app/navigation';
    import { documents } from './stores.ts'
    import { ssp, queryParam } from 'sveltekit-search-params'
    export let pages: number
    export let index: number
    export let access_token: string

    $: is_changed = JSON.stringify($documents[index].original) != JSON.stringify($documents[index].changes)
    $: is_idle = $documents[index].original.status == 'idle'

	let page = queryParam('page', ssp.number());
    async function change(e: Event) {
        $page = parseInt((e.target as HTMLInputElement).value)
    }

    async function remove() {
        // Mark model for deletion
        const patch_response = await fetch(`/api/v1/documents?id=eq.${$documents[index].original.id}`, { 
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

        await invalidate(url => url.pathname == '/api/v1/files')

        // Trigger delete job
        const ingest_response = await fetch('/api/v1/rpc/delete_document', { 
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,
            },
            body: JSON.stringify({ id: $documents[index].original.id })
        })
        if(ingest_response.status != 204) {
            throw new Error('Could not trigger delete job for document')
        }
    }

    function cancel_adding() {
        $documents.splice(index, 1)
        $documents = $documents;
    }

    function cancel_changes() {
        $documents[index].changes = structuredClone($documents[index].original)
        $documents = $documents
    }
</script>

<div class="embed">
    <input 
        type="text" 
        placeholder="Document name"
        disabled={!is_idle}
        bind:value={$documents[index].changes.name}
        class:changed={$documents[index].changes.name != $documents[index].original.name} 
        />

    <div class="row">
        <input 
            type="number" 
            bind:value={$documents[index].changes.from_page} 
            on:change={change}
            disabled={!is_idle}
            class:changed={$documents[index].changes.from_page != $documents[index].original.from_page} 
            min="1" 
            max={$documents[index].changes.to_page} 
            />
        <span>to</span>
        <input 
            type="number" 
            bind:value={$documents[index].changes.to_page} 
            on:change={change}
            disabled={!is_idle}
            class:changed={$documents[index].changes.to_page != $documents[index].original.to_page} 
            min={$documents[index].changes.from_page}
            max={pages} 
            />

        {#if $documents[index].original.id}
            {#if ! is_idle}
                <span class="status">
                    <Icon class="gg-loadbar" /> {$documents[index].original.status}
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

    .row {
        display: flex;
        align-items: center;
    }

    span {
        margin: 0.5rem;
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
