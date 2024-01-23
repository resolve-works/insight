
<script lang=ts>
    import Icon from '../Icon.svelte';

    let is_dragover = false;

    let input: HTMLInputElement;
    let files: File[];
    $: files = [];

    function drop(e: DragEvent) {
        if( ! e.dataTransfer) {
            return
        }

        for(const file of e.dataTransfer.files) {
            input.files.push(file)
        }
    }

    function upload() {
        if( ! input.files ) {
            return;
        }

        for(const file of input.files) {
            files = [...files, file]
            // TODO - Create pagestream in DB
            // TODO - Get signed write url
            // TODO - POST actual file to S3 signed url
        }

        input.value = '';
    }
</script>

<input type="file" accept=".pdf" multiple bind:this={input} on:change={upload} />

<button on:click={() => input.click()} on:drop|preventDefault={drop} on:dragover|preventDefault on:dragenter|preventDefault={() => is_dragover = true} on:dragexit|preventDefault={() => is_dragover = false} class:dragover={is_dragover}>
    <span>
        <Icon class="gg-software-upload" />
    </span>

    <h2>Drop files here to upload</h2>
</button>


{#each files as file}
    <div>{file.name}</div>
{/each}

<style>
    input {
        display: none;
    }

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

    button.dragover,
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
