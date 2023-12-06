<script>
    import Search from '../Search.svelte'
</script>

<header>
    <Search />

</header>

<main>
    <h3>Filters</h3>

    <h4>Document type</h4>
    <ul>
        <li>
            <label>
                <input type="checkbox"> Email
            </label>
        </li>
        <li>
            <label>
                <input type="checkbox"> Presentatie
            </label>
        </li>
    </ul>
</main>

<style>
    header {
        display: grid;
        align-items: center;
    }

    ul {
        margin: 0;
        list-style-type: none;
    }
</style>

