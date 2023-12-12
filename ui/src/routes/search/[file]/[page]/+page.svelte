
<script>
    import Layout from '../../../Layout.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    import { page } from '$app/stores';
    console.log($page.params)
</script>

<Layout>
    <header>
        <h2>Document</h2>
    </header>

    <PDFViewer url={'https://blog.mozilla.org/wp-content/uploads/2017/12/test.pdf'} />
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
