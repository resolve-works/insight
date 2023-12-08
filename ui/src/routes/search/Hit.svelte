
<script>
    export let hit;
</script>

<article>
    <header>
        <h3>{hit["_source"]["insight:filename"]}</h3>
    </header>

    {#each hit["inner_hits"]["insight:pages"]["hits"]["hits"] as page}
        <section>
            {page['_source']['index'] + 1}

            <ul>
                {#each page["highlight"]["insight:pages.contents"] as highlight}
                    <li>{@html highlight}</li>
                {/each}
            </ul>
        </section>
    {/each}
</article>

<style>
    article {
        background: var(--color-white);
        padding: var(--gap) var(--double-gap);
        margin: 0 var(--double-gap) 1rem;
    }
</style>
