<form method="get">
    <input name="query" type="text" placeholder="Kwartiermaker" value="Kwartiermaker" />

    <input type="submit" value="🔍">
</form>

<style>
    form {
        display: grid;
        grid-template-columns: 5fr 4em;
    }

    input[type=text] {
        grid-column: 1 / 3;
        grid-row: 1;
    }

    input[type=submit] {
        grid-column: 2 / 3;
        grid-row: 1;
        background: none;
        border: none;
        cursor: pointer;
    }
</style>
