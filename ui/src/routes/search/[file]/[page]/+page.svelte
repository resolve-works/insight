
<script>
    import Layout from '../../../Layout.svelte'

    export let data
</script>

<Layout>
    <header>
        <h2>Document</h2>
    </header>
</Layout>

<style>
    header {
        display: grid;
        grid-template-columns: auto auto;
        justify-content: space-between;
        align-items: center;
        padding-bottom: var(--gap);
    }
</style>
