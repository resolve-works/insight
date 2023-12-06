<form>
    <input type="text" placeholder="Kwartiermaker" value="Kwartiermaker" />

    <input type="submit" value="Search">
</form>

<style>
    form {
        display: grid;
        grid-template-columns: 3fr 1fr;
    }

    input[type=text] {
        border-right: none;
        border-radius: var(--input-border-radius) 0 0 var(--input-border-radius);
    }

    input[type=submit] {
        border-left: none;
        border-radius: 0 var(--input-border-radius) var(--input-border-radius) 0;
    }
</style>
