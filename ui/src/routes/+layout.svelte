<script>
    import Navigation from "./Navigation.svelte";
</script>

<div class="container">
    <nav>
        <Navigation />
    </nav>

    <header>
        <ul>
            <li><a href="/">Link</a></li>
            <li><a href="/">Link</a></li>
            <li><a href="/">Link</a></li>
            <li><a href="/">Link</a></li>
        </ul>
        
        <p>Username</p>
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

        grid-template-columns: 1fr 4fr;
        grid-template-rows: 8rem 1fr 8rem;

        height: 100vh;
    }

    header {
        grid-area: header;
        display: grid;
        grid-template-columns: 3fr 1fr;
        align-items: center;
    }
    header p {
        text-align: right;
    }

    nav {
        grid-area: nav;
        background: #494582;
        color: #F9FAFB;
        display: grid;
        grid-template-rows: subgrid;
        box-shadow: -1rem 0 1rem -1rem #38325D inset;
    }

    main {
        grid-area: content;
    }

    footer {
        grid-area: footer;
        display: grid;
        align-items: center;
    }
</style>
