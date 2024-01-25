
<script lang=ts>
    import Card from '$lib/Card.svelte';
    import Icon from '$lib/Icon.svelte';

    export let name: string;
    export let status: string;
    export let file: { id: string, name: string }[]
</script>

<Card>
    <h3>
        {name}

        {#if status != 'idle'}
            <Icon class="gg-loadbar" />
        {:else}
            <Icon class="gg-box" />
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
        align-items: center;
        justify-content: space-between;
    }
</style>

