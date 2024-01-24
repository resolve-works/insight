
<script lang=ts>
    import Card from '$lib/Card.svelte';

    export let name: string;
    export let id: string;
    export let files: [];
</script>

<Card>
    <h3>{name}</h3>
</Card>

