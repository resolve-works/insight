<script lang="ts">
    export let name: string
    export let documents: { id: string, name: string, from_page: int, to_page: int }[] = []
</script>

<header>
    <p>{name}</p>
</header>

<main>
    <h2>{documents.length} embedded document{documents.length == 1 ? '' : 's'}</h2>

    <ul>
        {#each documents as document, index}
            <li>#{index} - From page {document.from_page} to page {document.to_page}</li>
        {/each}
    </ul>
</main>

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
    }
</style>
