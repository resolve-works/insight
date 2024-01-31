
<script lang="ts">
    import type { Document } from './stores.ts'
    import { documents } from './stores.ts'

    export let document: Document;
    let defaults = {
        from_page: 0,
        to_page: 1,
    }
    let data: Document = { ...defaults, ...document};

    export let index: number;

    function remove() {

    }

    function cancel() {
        documents.update(documents => {
            documents.splice(index, 1)
            return documents;
        })
    }
</script>

<div class="embed">
    <form>
        <input type="text" placeholder="Document name" bind:value={data.name} />

        <div class="row">
            <input type="number" bind:value={data.from_page} />
            <span>to</span>
            <input type="number" bind:value={data.to_page} />

            {#if document.id}
                <button class="outline" on:click={remove}>Remove</button>
            {:else}
                <button class="outline" on:click={cancel}>Cancel adding</button>
            {/if}
        </div>
    </form>
</div>

<style>
    .embed {
        margin-bottom: 1rem;
    }

    input {
        border-color: var(--color-subnavigation-darker);
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
