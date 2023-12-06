<div class="container">
    <header>
        <input type="text" placeholder="search">
        
        <p>Username</p>
    </header>

    <nav>
        <header>
            <h1>Insight</h1>
        </header>

        <section>
            <ul>
                <li><a href="/">Link</a></li>
                <li><a href="/">Link</a></li>
                <li><a href="/">Link</a></li>
                <li><a href="/">Link</a></li>
            </ul>
        </section>
    </nav>

    <main>
        <slot />
    </main>

    <aside>
        <h2>Chat</h2>
    </aside>

    <footer>
        <h3>Footer</h3>
    </footer>
</div>


<style>
    :root {
        --header-height: 5rem;
        --gap: 2.5rem;
        --half-gap: 1.25rem;
    }
    .container {
        display: grid;

        grid-template-areas:
            "nav header header"
            "nav content side"
            "nav footer footer";

        grid-template-columns: 1fr 3fr 2fr;
        grid-template-rows: auto 1fr auto;
        gap: var(--gap);

        height: 100vh;
    }

    header {
        padding-right: var(--gap);
        grid-area: header;
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        height: var(--header-height);
        align-items: center;
    }
    header p {
        grid-column: 3 / 4;
        text-align: right;
    }

    nav {
        grid-area: nav;
        background: #494582;
        color: #F9FAFB;
    }

    nav header {
        height: var(--header-height);
        border-bottom: 1px solid #38325D;
        display: grid;
        align-items: center;
    }

    nav header h1 {
        font-size: 1.5rem;
        padding: 0 var(--half-gap);
    }

    nav section {
        border-top: 1px solid #5756A6;
    }

    nav section ul {
        padding: 1rem 0;
    }

    nav section ul a {
        display: block;
        padding: 0.5rem var(--half-gap);
        color: inherit;
    }

    main {
        grid-area: content;
    }

    aside {
        grid-area: side;
    }

    footer {
        grid-area: footer;
    }

</style>
