<script lang="ts">
    export let name: string
    export let documents: { id: string, name: string, from_page: number, to_page: number }[] = []
</script>

<header>
    <h2>{documents.length} embedded document{documents.length == 1 ? '' : 's'}</h2>
</header>

<ul>
    {#each documents as document, index}
        <li>#{index} - From page {document.from_page} to page {document.to_page}</li>
    {/each}
</ul>

<style>
    header {
        display: grid;
        align-items: center;
    }

    p {
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }
    
    ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
</style>
