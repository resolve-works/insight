
<script lang=ts>
    import { getContext } from 'svelte';
    import { invalidate } from '$app/navigation';
    import type { Insight } from '$lib/insight.ts'; 
    import Card from '$lib/Card.svelte';
    import Icon from '$lib/Icon.svelte';

    export let id: string;
    export let name: string;
    export let status: string;
    export let documents: { id: string, name: string, status: string }[] = []

    const insight: Insight = getContext('insight');

    $: is_idle = status == 'idle' && documents.every(document => document.status == 'idle');

    async function remove() {
        await insight.delete('/files', id)
        invalidate(url => url.pathname == '/api/v1/files')
    }
</script>

<Card>
    <h3>
        <a href={`/files/${id}`}>
            {name}
        </a>

        {#if ! is_idle}
            <Icon class="gg-loadbar" />
        {:else}
            <button on:click={remove}>
                <Icon class="gg-trash" />
            </button>
        {/if}
    </h3>

    {#if documents.length > 1}
        <p>{documents.length} embedded document{documents.length == 1 ? '' : 's'}</p>
    {/if}
</Card>

<style>
    a {
        text-decoration: none;
        color: var(--text-color-dark);
    }

    a:hover {
        text-decoration: underline;
        color: var(--color-primary);
    }

    h3 {
        display: grid;
        grid-template-columns: auto auto;
        align-items: center;
        justify-content: space-between;
    }

    p {
        display: flex;
        gap: 0.5rem;
    }

    button {
        padding: 1rem;
        margin: -1rem;
        border: none;
    }

    button:hover {
        color: var(--color-primary);
    }
</style>

