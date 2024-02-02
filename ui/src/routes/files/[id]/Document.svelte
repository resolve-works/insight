
<script lang="ts">
    import { documents } from './stores.ts'
    export let max: number;
    export let index: number;

    $: is_changed = JSON.stringify($documents[index].original) != JSON.stringify($documents[index].changes)

    function remove() {

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
    <form>
        <input type="text" placeholder="Document name" bind:value={$documents[index].changes.name} class:changed={$documents[index].changes.name != $documents[index].original.name} />

        <div class="row">
            <input type="number" 
                   bind:value={$documents[index].changes.from_page} 
                   class:changed={$documents[index].changes.from_page != $documents[index].original.from_page} 
                   min="1" 
                   {max} />
            <span>to</span>
            <input type="number" 
                   bind:value={$documents[index].changes.to_page} 
                   class:changed={$documents[index].changes.to_page != $documents[index].original.to_page} 
                   min="1" 
                   {max} />

            {#if $documents[index].original.id}
                {#if is_changed}
                    <button class="outline" on:click={cancel_changes}>Cancel changes</button>
                {:else}
                    <button class="outline" on:click={remove}>Remove</button>
                {/if}
            {:else}
                <button class="outline" on:click={cancel_adding}>Cancel adding</button>
            {/if}
        </div>
    </form>
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
