<script>
    import Hit from './Hit.svelte'
    import Search from '$lib/Search.svelte'
    import Page from '$lib/Page.svelte';
    import { page } from '$app/stores';
    const query = $page.url.searchParams.get('query')

    export let data
</script>

<aside>
    <header>
        <Search value={query ? query : ''} />
    </header>

    <nav>
        <h2>{data.total} document{data.total == 1 ? '' : 's'} found</h2>

        <h4>Document type:</h4>
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

        <br>

        <p>
            <a class="button secondary" href="/conversations">Start conversation about these documents</a>
        </p>
    </nav>
</aside>

<Page class="with-sidebar-left">
    {#each data.hits as hit }
        <Hit {...hit} />
    {/each}
</Page>

<style>
    aside {
        padding: 0 var(--padding-x);
        background: var(--color-subnavigation);
        color: var(--text-color-light);
        box-shadow: var(--box-shadow);
        display: grid;
        grid-template-rows: subgrid;
        grid-column: 2 / 3;
        grid-row: 1 / 4;
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
        display: block;
    }
</style>
