<script>
    import Filters from './Filters.svelte'
    import Hit from './Hit.svelte'
    import Layout from '../Layout.svelte'

    import { page } from '$app/stores';

    export let data
    const total = data['hits']['total']['value']
    const hits = data.hits.hits
    const query = $page.url.searchParams.get('query')
</script>

<Layout>
    <Filters slot="subnav" />

    <header>
        <h2>{total} result{total > 1 ? 's' : ''} for "{query}"</h2>

        <button>Start conversation</button>
    </header>

    {#each hits as hit }
        <Hit hit={hit} />
    {/each}
</Layout>

<style>
    header {
        display: grid;
        grid-template-columns: auto auto;
        justify-content: space-between;
        align-items: center;
        padding: var(--gap) var(--double-gap);
        margin: 0 var(--double-gap);
    }
</style>
