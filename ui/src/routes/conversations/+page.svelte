
<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import Page from '$lib/Page.svelte'
    import Card from '$lib/Card.svelte'
    import Icon from '$lib/Icon.svelte'
    import { enhance } from '$app/forms';

    export let data;

    let ac = new AbortController();

    class StreamAbortedError extends Error {}

    async function getEvents() {
        try {
            // Fetch will error with AbortError when abort is called
            const response = await fetch("/events", { signal: ac.signal });
            const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
            while (true) {
                const { value, done } = await reader.read();
                console.log(value);
                if (done) {
                    break;
                }
            }
        } catch(error) {
            if( ! (error instanceof StreamAbortedError)) {
                throw error;
            }
        }
    }

    onMount(() => {
        getEvents();
    })

    onDestroy(() => {
        ac.abort(new StreamAbortedError());
    });
</script>

<Page>
    <div class="chat">
        <div class="messages">
            {#each data.prompts as prompt}
                <div class="message human">
                    <aside>
                        <h3>H</h3>
                    </aside>

                    <Card class="card">
                        <h3>Human</h3>

                        <p>{ prompt.query }</p>
                    </Card>
                </div>

                <div class="message machine">
                    <aside>
                        <h3>M</h3>
                    </aside>

                    <Card class="card">
                        <h3>Machine</h3>

                        {#if prompt.response}
                            <p>{ prompt.response }</p>

                            {#each prompt.sources as source}
                                <a href="/search/{source.id}?page={source.index - source.from_page + 1}">
                                    <span>
                                        <Icon class="gg-file" />
                                        {source.index - source.from_page + 1}
                                    </span>
                                    {source.name}
                                </a>
                            {/each}
                        {:else}
                            <Icon class="gg-loadbar" />
                        {/if}
                    </Card>
                </div>
            {/each}
        </div>

        <form method="POST" use:enhance>
            <input type="text" name="query" placeholder="What's your question?">
            <input type="number" name="similarity_top_k" placeholder="Pages (default: 3)" min="0">
            <input type="submit" value="Prompt" class="primary">
        </form>
    </div>
</Page>

<style>
    :root {
        --profile-size: 4rem;
        --profile-margin: 1rem;
        --triangle-size: 3rem;
    }

    .chat {
        display: grid;
        grid-template-rows: auto min-content;
        min-height: 100%;
        justify-content: space-between;
    }

    .message {
        display: flex;
        gap: 2rem;
        margin-bottom: 1rem;
    }

    .message.human {
        flex-direction: row-reverse;
    }

    aside {
        display: grid;
        align-items: center;
        width: var(--profile-size);
        height: var(--profile-size);
        background: var(--color-primary);
        text-align: center;
        border-radius: 50%;
        color: var(--text-color-light);
        margin-top: var(--profile-margin);
    }

    .message.machine aside {
        background: #6167C9;
    }

    :global(.card) {
        max-width: 60%;
        position: relative;
    }

    :global(.card:before ) {
        content: "";
        width: var(--triangle-size);
        height: var(--triangle-size);
        position: absolute;
        top: calc(var(--profile-margin) + (var(--profile-size) - var(--triangle-size)) / 2);
        border: calc(var(--triangle-size) / 2) solid transparent;
    }

    .message.machine :global(.card:before) {
        left: calc(var(--triangle-size) * -1);
        border-right-color: var(--color-white);
    }
    .message.human :global(.card:before) {
        right: calc(var(--triangle-size) * -1);
        border-left-color: var(--color-white);
    }

    form {
        display: grid;
        grid-template-columns: 4fr 1fr 1fr;
        align-items: center;
        gap: 0.5rem;
    }

    a {
        display: grid;
        align-items: center;
        grid-template-columns: 6rem auto;
    }

    span {
        display: grid;
        height: 2rem;
        grid-template-columns: 2rem auto;
        align-items: center;
        margin-right: 1rem;
    }
</style>
