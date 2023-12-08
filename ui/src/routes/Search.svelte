<script>
    import Icon from './Icon.svelte';
    import { page } from '$app/stores';
    const query = $page.url.searchParams.get('query')
</script>

<form method="get" action="/search">
    <input name="query" type="text" placeholder="Search files by keyword" value={query} />

    <button>
        <Icon class="gg-search" />
    </button>
</form>

<style>
    form {
        display: grid;
        grid-template-columns: 5fr 3rem;
    }

    input[type=text] {
        grid-column: 1 / 3;
        grid-row: 1;
    }

    button {
        grid-column: 2 / 3;
        grid-row: 1;
        background: none;
        padding: 0 0.5rem;
        color: var(--text-color-dark);
        border: none;
        cursor: pointer;
    }
</style>
