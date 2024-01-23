
<script lang=ts>
    import Icon from '../Icon.svelte';
    import { Upload } from './Upload.svelte';
    import { uploads } from './stores.ts';

    let is_dragover = false;
    let input: HTMLInputElement;

    function upload(file: File) {
        uploads.update(uploads => [...uploads, new Upload(file)])
    }

    function drop(e: DragEvent) {
        is_dragover = false;
    
        if( ! e.dataTransfer) {
            return
        }

        for(const file of e.dataTransfer.files) {
            if(file.type != 'application/pdf') {
                alert(`Unsupported file type: ${file.type}`);
            }

            upload(file)
        }
    }

    function select() {
        if( ! input.files ) {
            return;
        }

        for(const file of input.files) {
            upload(file)
        }

        input.value = '';
    }
</script>

<input type="file" accept=".pdf" multiple bind:this={input} on:change={select} />

<button on:click={() => input.click()} on:drop|preventDefault={drop} on:dragover|preventDefault on:dragenter|preventDefault={() => is_dragover = true} on:dragexit|preventDefault={() => is_dragover = false} class:dragover={is_dragover}>
    <span>
        <Icon class="gg-software-upload" />
    </span>

    <h2><b>Choose PDF files</b> or drop them here</h2>
</button>

<style>
    input {
        display: none;
    }

    button {
        padding: 3rem 1.5rem;
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
        border-color: var(--color-primary);
        cursor: pointer;
    }

    h2 {
        font-weight: normal;
    }

    span {
        margin: 0.5rem 1rem 0 1rem;
    }

    span :global(.gg-software-upload) {
        --ggs: 1.8;
    }

</style>
