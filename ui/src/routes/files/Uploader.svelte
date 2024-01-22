
<script lang=ts>
    import Icon from '../Icon.svelte';

    let input: HTMLInputElement;

    function upload(e: Event) {
        for(const pagestream of e.target.files) {
            console.log(pagestream)
            // TODO - POST pagestream
            // TODO - Get signed write url
            // TODO - POST actual file to S3 signed url
        }
    }
</script>

<input type="file" accept=".pdf" multiple bind:this={input} on:change={upload} />

<button on:click={() => input.click()}>
    <span>
        <Icon class="gg-software-upload" />
    </span>

    <h2>Drop files here to upload</h2>
</button>

<style>
    button {
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 3px dashed var(--color-page-border);
        display: grid;
        grid-template-columns: auto auto;
        color: var(--text-color-page);
        align-items: center;
        justify-content: center;
        background: transparent;
        width: 100%;
    }

    button:hover {
        color: var(--color-primary);
        cursor: pointer;
    }

    span {
        margin: 0.5rem 1rem 0 1rem;
    }

    span :global(.gg-software-upload) {
        --ggs: 1.8;
    }
</style>
