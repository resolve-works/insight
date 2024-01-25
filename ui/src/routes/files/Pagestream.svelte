
<script lang=ts>
    import Card from '$lib/Card.svelte';
    import Icon from '$lib/Icon.svelte';

    export let id: string;
    export let name: string;
    export let status: string;
    export let documents: { id: string, name: string }[] = []
</script>

<Card>
    <a href={`/pagestreams/${id}`}>
        <h3>
            {name}

            {#if status != 'idle'}
                <Icon class="gg-loadbar" />
            {:else}
                {#if documents.length > 1}
                    <Icon class="gg-box" />
                {/if}
            {/if}
        </h3>

        {#if documents.length > 1}
            <p>{documents.length} embedded document{documents.length == 1 ? '' : 's'}</p>
        {/if}
    </a>
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

