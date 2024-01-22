
<script>
    import Icon from '../Icon.svelte';
</script>

<div>
    <span>
        <Icon class="gg-software-upload" />
    </span>

    <h2>Drop files here to upload</h2>
</div>

<style>
    div {
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 3px dashed var(--color-page-border);
        display: grid;
        grid-template-columns: auto auto;
        color: var(--text-color-page);
        align-items: center;
        justify-content: center;
    }

    span {
        margin: 0.5rem 1rem 0 1rem;
    }

    span :global(.gg-software-upload) {
        --ggs: 2;
    }
</style>
