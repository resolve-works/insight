
<script lang=ts>
    import Card from '$lib/Card.svelte';
    import Icon from '$lib/Icon.svelte';

    export let name: string;
    export let status: string;
    export let file: { id: string, name: string }[]
</script>

<Card>
    <h3>
        <span>
            <Icon class="gg-box" />
            {name}
        </span>

        {#if status != 'idle'}
            <span class="status">
                {status}
                <Icon class="gg-spinner" />
            </span>
        {/if}
    </h3>

    {#if file}
        {#each file as f}
            {f.name}
        {/each}
    {/if}
</Card>

<style>
    h3 {
        display: grid;
        grid-template-columns: auto auto;
        justify-content: space-between;
    }

    span {
        display: grid;
        grid-template-columns: auto auto;
        align-items: center;
        gap: 1rem;
    }

    .status {
        font-weight: normal;
    }

    .status :global(.gg-spinner) {
        --ggs: 1.4;
    }
</style>

