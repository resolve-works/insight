
<script lang="ts">
    import type { Document } from './+page.svelte'

    export let document: Document;

    export let index: number;
    export let is_editing: false;
</script>

<div class="embed">
    {#if is_editing}
        <input type="text" value={document.name} />
    {:else}
        <h3>{document.name}</h3>
    {/if}

    <form>
        <div>
            <input disabled type="number" value={document.from_page + 1} />
            <span>to</span>
            <input disabled type="number" value={document.to_page} />
        </div>

        <button>Edit</button>
    </form>
</div>

<style>
    .embed {
        overflow-x: hidden;
    }

    h3 {
        overflow-x: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }

    input[type=number] {
        width: 6rem;
        border-color: var(--color-subnavigation-darker);
    }

    form {
        display: grid;
        grid-template-columns: auto auto;
        align-items: center;
    }
</style>
