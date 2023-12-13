<script>
    import Filters from './Filters.svelte'
    import Hit from './Hit.svelte'
    import Layout from '../Layout.svelte'

    export let data
</script>

<Layout>
    <Filters {...data} slot="subnav" />

    {#each data.hits as hit }
        <Hit {...hit} />
    {/each}
</Layout>
