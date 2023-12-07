<script>
    import Search from '../Search.svelte'
</script>

<header>
    <Search />

</header>

<main>
    <h4>File type:</h4>
    <ul>
        <li>
            <label>
                <input type="checkbox"> 
                Document
            </label>
        </li>
        <li>
            <label>
                <input type="checkbox"> 
                Email
            </label>
        </li>
        <li>
            <label>
                <input type="checkbox"> 
                Presentation
            </label>
        </li>
    </ul>

    <h4>File type:</h4>
    <ul>
        <li>
            <label>
                <input type="checkbox"> 
                Document
            </label>
        </li>
        <li>
            <label>
                <input type="checkbox"> 
                Email
            </label>
        </li>
        <li>
            <label>
                <input type="checkbox"> 
                Presentation
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
        margin: 0 0 2rem 0;
        padding: 0;
        list-style-type: none;
    }
</style>

