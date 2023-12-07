<script>
    import { page } from '$app/stores';
    import Icon from './Icon.svelte';

    const items = [
        { href: "/search", name: "Search", class: "gg-search" },
        { href: "/conversations", name: "Conversations", class: "gg-comment" },
        { href: "/files", name: "Files", class: "gg-file-document"},
    ]
</script>

<a class="logo" href="/">
    <h1>
        Insight
    </h1>
    <Icon class="gg-menu" />
</a>

<ul>
    {#each items as item}
        <li class:active={$page.url.pathname == item.href}>
            <a href={item.href}>
                {item.name}
                <Icon class={item.class} />
            </a>
        </li>
    {/each}
</ul>

<style>
    a.logo {
        border-bottom: 1px solid var(--color-navigation-darker);
        display: grid;
        grid-template-columns: auto 1.5rem;
        align-items: center;
        color: inherit;
        text-decoration: none;
        color: inherit;
        padding: 0 var(--gap);
    }
    a.logo h1 {
        font-size: 1.5rem;
    }

    ul {
        padding: 0;
        margin: 0;
    }

    li a {
        display: grid;
        grid-template-columns: auto 1.5rem;
        align-items: end;
        color: inherit;
        border-top: 1px solid var(--color-navigation-lighter);
        border-bottom: 1px solid #303943;
        padding: 1.5rem var(--gap);
        text-decoration: none;
        font-weight: bold;
    }

    li.active a {
        background: var(--color-subnavigation);
        border-top: 1px solid transparent;
        border-bottom: 1px solid var(--color-navigation-darker);
        position: relative;
    }

    li.active a:after {
        content: "";
        position: absolute;
        top: 0;
        bottom: 0;
        right: -1rem;
        width: 1rem;
        background: var(--color-subnavigation);
    }
</style>
