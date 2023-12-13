<script>
    import Navigation from './Navigation.svelte';
    import Breadcrumbs from "./Breadcrumbs.svelte";
</script>

<div class="container" class:with-subnav={$$slots.subnav}>
    <nav class="mainnav">
        <Navigation />
    </nav>

	{#if $$slots.subnav}
        <nav class="subnav">
            <slot name="subnav" />
        </nav>
    {/if}

    <div class="page">
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
    </div>
</div>


<style>
    :root {
        --box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.5);
    }

    .container {
        display: grid;

        grid-template-areas:
            "nav content"
            "nav content"
            "nav content";
        grid-template-columns: auto 22fr;
        grid-template-rows: var(--header-height) 1fr var(--footer-height);

        height: 100vh;
    }

    .container.with-subnav {
        grid-template-areas:
            "nav subnav content"
            "nav subnav content"
            "nav subnav content";
        grid-template-columns: auto 2fr 4fr;
    }

    .mainnav {
        grid-area: nav;
        background: #4C4C4C;
        color: var(--text-color-light);
    }

    .subnav {
        grid-area: subnav;
        padding: 0 var(--padding-x);
        background: var(--color-subnavigation);
        color: var(--text-color-light);
        box-shadow: var(--box-shadow);
    }

    .page {
        display: grid;
        grid-area: content;
        grid-template-rows: subgrid;
        box-shadow: var(--box-shadow);
        background: var(--color-page);
        z-index: 3;
        padding: 0 calc(var(--padding-x) * 1.5);
    }

    header {
        display: grid;
        align-items: center;
    }

    main {
        padding: 0 calc(var(--padding-x) * 1.5);
    }

    footer {
        display: grid;
        align-items: center;
        color: #BDBDBD;
        grid-template-columns: auto auto;
        justify-content: space-between;
    }
</style>
