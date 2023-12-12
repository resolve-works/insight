
<script lang="ts">
    import { page } from '$app/stores';
    import Icon from '../Icon.svelte';
    export let filename: string;
    export let pages: { index: number, url: URL, highlights: string[] }[];
</script>

<article>
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

    li :global(em) {
        color: var(--color-primary);
        font-weight: bold;
    }
</style>
