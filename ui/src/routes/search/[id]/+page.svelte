
<script>
    import Page from '$lib/Page.svelte';
    import PDFViewer from '$lib/PDFViewer.svelte';
    import { page } from '$app/stores';
    export let data;
</script>

<Page>
    <PDFViewer url={data.url} index={parseInt($page.url.searchParams.get('page') ?? '1')} />
</Page>

