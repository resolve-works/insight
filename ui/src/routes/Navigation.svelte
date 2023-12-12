<script>
    import { page } from '$app/stores';
    import Icon from './Icon.svelte';

    export let collapsed = false;

    const items = [
        { href: "/search?query=*", name: "Search", class: "gg-search" },
        { href: "/conversations", name: "Conversations", class: "gg-comment" },
        { href: "/files", name: "Files", class: "gg-file-document"},
    ]
</script>

<div class="container" class:collapsed={collapsed}>
    <a class="logo" href="/">
        <h1>Insight</h1>
        <Icon class="gg-menu" />
    </a>

    <ul>
        {#each items as item}
            <li class:active={$page.url.pathname == new URL(item.href, $page.url.origin).pathname}>
                <a href={item.href}>
                    <span>{item.name}</span>
                    <Icon class={item.class} />
                </a>
            </li>
        {/each}
    </ul>
</div>

<style>
    .container {
        display: grid;
        grid-template-rows: subgrid;
        grid-row: 1 / 4;
        min-width: 20rem;
    }

    .container.collapsed {
        min-width: 0;
    }

    .container.collapsed h1,
    .container.collapsed span {
        display: none;
    }

    a.logo {
        border-bottom: 1px solid var(--color-navigation-darker);
        display: grid;
        grid-template-columns: auto auto;
        justify-content: space-between;
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
        grid-template-columns: auto auto;
        justify-content: space-between;
        align-items: center;
        color: inherit;
        border-top: 1px solid var(--color-navigation-lighter);
        border-bottom: 1px solid #303943;
        padding: 1.5rem var(--gap);
        text-decoration: none;
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
        right: 0;
        width: 1rem;
        background: var(--color-subnavigation);
    }
</style>
