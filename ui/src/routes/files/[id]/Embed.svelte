
<script lang="ts">
    export let from_page: number;
    export let to_page: number;

    export let id: string;
    export let name: string;
</script>

<div>
    <h3>{name}</h3>

    <form>
        <input type="number" value={from_page + 1} />
        <span>to</span>
        <input type="number" value={to_page} />
    </form>
</div>

<style>
    div {
        overflow-x: hidden;
    }

    h3 {
        overflow-x: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }

    input[type=number] {
        width: 8rem;
    }
</style>
