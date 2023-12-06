<script>
    import Navigation from './Navigation.svelte';
    import Breadcrumbs from "./Breadcrumbs.svelte";
    import Profile from "./Profile.svelte";
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
            
            <Profile />
        </header>

        <main>
            <slot />
        </main>

        <footer>
            <h3>Footer</h3>
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
        grid-template-columns: 2fr 11fr;
        grid-template-rows: 6rem 1fr 6rem;

        height: 100vh;
    }

    .container.with-subnav {
        grid-template-areas:
            "nav subnav content"
            "nav subnav content"
            "nav subnav content";
        grid-template-columns: 2fr 3fr 8fr;
    }

    .mainnav {
        grid-area: nav;
        background: #4C4C4C;
        color: var(--text-color-light);
        display: grid;
        grid-template-rows: subgrid;
    }

    .subnav {
        grid-area: subnav;
        padding: 0 var(--gap);
        background: var(--color-subnavigation);
        color: var(--text-color-light);
        display: grid;
        box-shadow: var(--box-shadow);
        grid-template-rows: subgrid;
    }

    .page {
        display: grid;
        grid-area: content;
        grid-template-rows: subgrid;
        box-shadow: var(--box-shadow);
        background: #ECEEF1;
        z-index: 3;
    }

    header {
        display: grid;
        grid-template-columns: 1fr 1fr;
        align-items: center;
        padding: 0 var(--gap);
        background: #F9FAFB;
        border-bottom: var(--border-size) solid #D0D5DC;
    }

    main {
        border-top: var(--border-size) solid #F9FAFB;
        padding: 0 var(--gap);
    }

    footer {
        display: grid;
        align-items: center;
        padding: 0 var(--gap);
    }
</style>
