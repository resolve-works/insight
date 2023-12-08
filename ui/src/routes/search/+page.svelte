<script>
    import Filters from './Filters.svelte'
    import Hit from './Hit.svelte'
    import Layout from '../Layout.svelte'

    export let data
</script>

<Layout>
    <Filters slot="subnav" />

    <header>
        <h2>{data.total} result{data.total > 1 ? 's' : ''} for "{data.query}"</h2>

        <button>Start conversation</button>
    </header>

    {#each data.hits as hit }
        <Hit hit={hit} />
    {/each}
</Layout>

<style>
    header {
        display: grid;
        grid-template-columns: auto auto;
        justify-content: space-between;
        align-items: center;
        padding: var(--gap) 0;
    }
</style>
