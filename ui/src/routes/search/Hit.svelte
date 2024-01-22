
<script lang="ts">
    import Icon from '../Icon.svelte';
    import Card from '../Card.svelte';
    export let filename: string;
    export let pages: { index: number, url: URL, highlights: string[] }[];
</script>

<Card>
    <header>
        <h3>{filename}</h3>
    </header>

    {#each pages as page}
        <a href="{page.url}">
            <span>
                <Icon class="gg-file" />
                {page.index}
            </span>

            <ul>
                {#each page.highlights as highlight}
                    <li>{@html highlight}</li>
                {/each}
            </ul>
        </a>
    {/each}
</Card>

<style>
    span {
        display: grid;
        height: 2rem;
        grid-template-columns: 2rem auto;
        align-items: center;
    }

    a {
        display: grid;
        grid-template-columns: 3rem auto;
        align-items: top;
        line-height: 2rem;
        text-decoration: none;
        color: currentColor;
    }

    a:hover span {
        text-decoration: underline;
        color: var(--color-primary);
    }

    ul {
        list-style-type: none;
        margin: 0 0 1rem 0;
        padding: none;
    }

    li {
        border-top: 1px solid var(--color-page);
        padding: 0.5rem 0;
    }

    li:first-child {
        padding-top: 0;
        border-top: none;
    }

    li :global(em) {
        color: var(--color-primary);
        font-weight: bold;
    }
</style>
