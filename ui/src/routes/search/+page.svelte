<script>
    import Filters from './Filters.svelte'
    import Hit from './Hit.svelte'
    import Layout from '$lib/Layout.svelte'

    export let data
</script>

<Layout>
    <Filters total={data.total} slot="subnav" />

    {#each data.hits as hit }
        <Hit {...hit} />
    {/each}
</Layout>
