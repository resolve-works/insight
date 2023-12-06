<script>
    import Navigation from "./Navigation.svelte";
    import Breadcrumbs from "./Breadcrumbs.svelte";
    import Search from "./Search.svelte";
    import Profile from "./Profile.svelte";
</script>

<div class="container">
    <nav>
        <Navigation />
    </nav>

    <header>
        <Breadcrumbs />
        
        <Search />

        <Profile />
    </header>

    <main>
        <slot />
    </main>

    <footer>
        <h3>Footer</h3>
    </footer>
</div>


<style>
    .container {
        display: grid;

        grid-template-areas:
            "nav header"
            "nav content"
            "nav footer";

        grid-template-columns: 1fr 5fr;
        grid-template-rows: 6rem 1fr 6rem;

        height: 100vh;
    }

    header {
        grid-area: header;
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        align-items: center;
        padding: 0 var(--gap);
        background: #F9FAFB;
    }

    nav {
        grid-area: nav;
        background: var(--color-primary);
        color: var(--text-color-light);
        display: grid;
        grid-template-rows: subgrid;
        box-shadow: -1rem 0 1rem -1rem #38325D inset;
    }

    main {
        grid-area: content;
        padding: 0 var(--gap);
        box-shadow: 0 1rem 1rem -1rem #D0D5DC inset;
    }

    footer {
        grid-area: footer;
        display: grid;
        align-items: center;
        padding: 0 var(--gap);
    }
</style>
