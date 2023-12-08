
<script>
    import Icon from '../Icon.svelte';
    export let hit;
</script>

<article>
    <header>
        <h3>{hit["_source"]["insight:filename"]}</h3>
    </header>

    {#each hit["inner_hits"]["insight:pages"]["hits"]["hits"] as page}
        <section>
            <span>
                <Icon class="gg-file" />
                {page['_source']['index'] + 1}
            </span>

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
        padding: calc(var(--gap)) calc(var(--gap) * 1.5);
        margin: 0 calc(var(--gap) * -1.5);
        margin-bottom: 1rem;
        border-bottom: var(--border-size) solid #D0D5DC;
    }

    span {
        display: grid;
        height: 2rem;
        grid-template-columns: 2rem auto;
        align-items: center;
    }

    section {
        display: grid;
        grid-template-columns: 3rem auto;
        align-items: top;
        line-height: 2rem;
    }

    ul {
        list-style-type: none;
        margin: 0 0 1rem 0;
        padding: none;
    }

    li :global(em) {
        color: var(--color-primary);
        font-weight: bold;
    }
</style>
