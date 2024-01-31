<script>
    import Navigation from '$lib/Navigation.svelte';
</script>

<div class="container">
    <nav>
        <div class="sticky">
            <Navigation />
        </div>
    </nav>

    <slot />
</div>

<style>
    :root {
        --box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.5);
    }

    .container {
        display: grid;

        grid-template-areas:
            "nav content content content"
            "nav content content content"
            "nav content content content";
        grid-template-columns: 20rem 5fr 6fr 5fr;
        grid-template-rows: var(--header-height) 1fr var(--footer-height);

        height: 100vh;
    }

    nav {
        display: grid;
        grid-area: nav;
    }

    .sticky {
        height: 100vh;
        display: grid;
        grid-template-rows: var(--header-height) 1fr var(--footer-height);
        top: 0;
        position: sticky;
        z-index: 3;
        color: var(--text-color-light);
    }
</style>
