
<script lang=ts>
    import Card from '$lib/Card.svelte';
    import Icon from '$lib/Icon.svelte';

    export let name: string;
    export let status: string;
</script>

<Card>
    <h3>
        {name}
        {#if status != 'idle'}
            <span>
                {status}
                <Icon class="gg-spinner" />
            </span>
        {/if}
    </h3>
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
        font-weight: normal;
    }

    span :global(.gg-spinner) {
        --ggs: 1.4;
        margin: 0.2rem 0 0 2rem;
    }
</style>

