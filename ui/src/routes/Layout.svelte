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
        --box-shadow: 0 0 1rem 0 rgba(56, 50, 93, 0.8);
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
        background: var(--color-primary);
        color: var(--text-color-light);
        display: grid;
        grid-template-rows: subgrid;
        box-shadow: var(--box-shadow);
        z-index: 2;
    }

    .subnav {
        grid-area: subnav;
        background: #494582;
        padding: 0 var(--gap);
        color: var(--text-color-light);
        display: grid;
        grid-template-rows: subgrid;
    }

    .page {
        display: grid;
        grid-area: content;
        grid-template-rows: subgrid;
        box-shadow: var(--box-shadow);
        background: var(--color-background);
        z-index: 3;
    }

    header {
        display: grid;
        grid-template-columns: 1fr 1fr;
        align-items: center;
        padding: 0 var(--gap);
        background: #F9FAFB;
        border-bottom: 1px solid #D0D5DC;
    }

    main {
        border-top: 1px solid #F9FAFB;
        padding: 0 var(--gap);
    }

    footer {
        display: grid;
        align-items: center;
        padding: 0 var(--gap);
    }
</style>
