<script lang="ts">
    import Search from '$lib/Search.svelte'
    import { page } from '$app/stores';
    const query = $page.url.searchParams.get('query')

    export let total: number;
</script>

<aside>
    <header>
        <Search value={query ? query : ''} />
    </header>

    <main>
        <h2>{total} file{total == 1 ? '' : 's'} found</h2>

        <h4>File type:</h4>
        <ul>
            <li>
                <label>
                    <input type="checkbox" checked={true}> 
                    Document
                </label>
            </li>
            <li>
                <label>
                    <input type="checkbox" checked={true}> 
                    Email
                </label>
            </li>
            <li>
                <label>
                    <input type="checkbox" checked={true}> 
                    Presentation
                </label>
            </li>
        </ul>

        <p>
        <br>
            <a class="button" href="/conversations">Start conversation about these files</a>
        </p>
    </main>

</aside>

<style>
    aside {
        display: grid;
        grid-template-rows: var(--header-height) auto var(--footer-height);
        position: sticky;
        top: 0;
        min-height: 100vh;
    }

    header {
        display: grid;
        align-items: center;
    }
    
    header :global(input[type=text]) {
        border-color: var(--color-subnavigation-darker);
    }

    ul {
        margin: 0 0 2rem 0;
        padding: 0;
        list-style-type: none;
    }

    a.button {
        background: #FECF49;
        color: var(--text-color-dark);
        display: block;
    }
</style>

