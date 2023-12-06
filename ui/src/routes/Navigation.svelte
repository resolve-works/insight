<script>
    import { page } from '$app/stores';

    const items = [
        { href: "/search", name: "Search", },
        { href: "/conversations", name: "Conversations", },
        { href: "/files", name: "Files", },
    ]
</script>

<header>
    <h1><a href="/">Insight</a></h1>
</header>

<ul>
    {#each items as item}
        <li class:active={$page.url.pathname == item.href}><a href={item.href}>{item.name}</a></li>
    {/each}
</ul>

<style>
    header {
        border-bottom: 1px solid var(--color-primary-darker);
        display: grid;
        align-items: center;
    }

    h1 {
        font-size: 1.5rem;
        color: inherit;
        padding: 0 var(--gap);
    }

    h1 a {
        color: inherit;
        text-decoration: none;
    }

    ul {
        padding: 0;
        margin: 0;
    }

    li a {
        display: block;
        color: inherit;
        border-top: 1px solid var(--color-primary-lighter);
        border-bottom: 1px solid var(--color-primary-darker);
        padding: 1.5rem var(--gap);
        text-decoration: none;
        font-weight: bold;
    }

    li.active a {
        background: var(--color-primary-darker);
        border-top: 1px solid #38325D;
        border-bottom: 1px solid var(--color-primary-darker);
        position: relative;
    }

    li.active a:after {
        content: "";
        position: absolute;
        top: 0;
        bottom: 0;
        right: -1rem;
        width: 1rem;
        background: var(--color-primary-darker);
    }
</style>
