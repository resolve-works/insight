
<script lang="ts">
    import Icon from '$lib/Icon.svelte';
    import { enhance } from '$app/forms';
    import { created, changed } from './stores.ts'
    import type { DocumentInput } from './stores.ts'
    import { ssp, queryParam } from 'sveltekit-search-params'

    export let number_of_pages: number
    export let document: DocumentInput;

    // Document can be editted when it's new, or when it's not being ingested
    $: is_disabled = !! document.original.status

	let page = queryParam('page', ssp.number());
    async function go_to_page(e: Event) {
        $page = parseInt((e.target as HTMLInputElement).value)
        $changed = $changed;
    }

    function cancel_adding() {
        $created = $created.filter(obj => ! Object.is(obj, document.changes))
    }

    function cancel_changes() {
        $changed[document.original.id] = structuredClone(document.original);
    }
</script>

<div class="embed">
    <input type="hidden" name="id" disabled={is_disabled} value={document.original.id || ''} />

    <input 
        type="text" 
        placeholder="Document name"
        disabled={is_disabled}
        name="name"
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
            name="from_page"
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
            name="to_page"
            class:changed={document.changes.to_page != document.original.to_page} 
            min={document.changes.from_page}
            max={number_of_pages} 
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
                    <form method="POST" action="?/remove" use:enhance>
                        <input type="hidden" name="id" value={document.original.id} />
                        <button class="outline">Remove</button>
                    </form>
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
