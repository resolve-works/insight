
<script lang=ts>
    import Card from '$lib/Card.svelte';
    import Icon from '$lib/Icon.svelte';

    export let id: string;
    export let name: string;
    export let status: string;
    export let documents: { id: string, name: string }[]

    const is_archive = documents && documents.length > 1;
    const url = is_archive ? `/pagestreams/${id}` : `/documents/${documents[0].id}`
</script>

<Card>
    <a href={url}>
        <h3>
            {name}

            {#if status != 'idle'}
                <Icon class="gg-loadbar" />
            {:else}
                {#if is_archive}
                    <Icon class="gg-box" />
                {/if}
            {/if}
        </h3>
    </a>

    {#if is_archive}
        {#each documents as document}
            {document.name}
        {/each}
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
</style>

