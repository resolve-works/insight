
<script lang="ts">
    import Breadcrumbs from "./Breadcrumbs.svelte"; 
</script>

<article {...$$props}>
    <header>
        <Breadcrumbs />
    </header>

    <main>
        <slot />
    </main>

    <footer>
        <p>Thank you for using Insight.</p> 
        <p>Do you want to <a href="https://www.discourse.org/">ask for help</a> or <a href="https://github.com/followthemoney/insight/">report a problem</a>?</p>
    </footer>
</article>

<style>
    article {
        position: relative;
        display: grid;
        grid-template-rows: subgrid;
        grid-column: 2 / 5;
        grid-row: 1 / 4;
        padding: 0 calc(var(--padding-x) * 1.5);
        background: var(--color-page);
        box-shadow: var(--box-shadow);
    }

    article.with-sidebar-left {
        grid-column-start: 3;
    }

    article.with-sidebar-right {
        grid-column-end: 4;
    }

    header {
        display: grid;
        align-items: center;
    }

    footer {
        display: grid;
        align-items: center;
        color: var(--text-color-page);
        grid-template-columns: auto auto;
        justify-content: space-between;
    }
</style>
