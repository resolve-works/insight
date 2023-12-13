
<script lang="ts">
    import { page } from '$app/stores';

    const href = $page.url.pathname;
    const title = href.slice(1).charAt(0).toUpperCase() + href.slice(2);
</script>

<ul>
    <li><a href="/">Home</a></li>
    {#if href !== '/' }
        <li><a {href}>{title}</a></li>
    {/if}
</ul>

<style>
    ul {
        margin: 0;
        padding: 1.5rem 0;
        list-style-type: none;
        display: flex;
    }

    li {
        margin-right: 1rem;
    }

    li:after {
        margin-left: 1rem;
        content: "›"
    }

    li:last-child a {
        text-decoration: none;
        color: var(--text-color-dark);
    }

    li:last-child:after {
        content: "";
    }
</style>
