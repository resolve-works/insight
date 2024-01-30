
<script lang="ts">
    export let from_page: number;
    export let to_page: number;

    export let id: string;
    export let name: string;
</script>

<h3>{name}</h3>

<form>
    from: <input type="number" value={from_page + 1} />
    to:<input type="number" value={to_page} />
</form>

<style>
    h3 {
        overflow-x: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }
</style>
