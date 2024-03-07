<script>
    import { onMount, onDestroy } from "svelte";
    import { invalidate } from "$app/navigation";
    import Navigation from '$lib/Navigation.svelte';

    let ac = new AbortController();

    class StreamAbortedError extends Error {}

    async function getEvents() {
        try {
            // Fetch will error with AbortError when abort is called
            const response = await fetch("/events", { signal: ac.signal });
            const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
            while (true) {
                const { value, done } = await reader.read();
                const body = JSON.parse(value);

                const mapping = {
                    analyze_file: ['api:files'],
                    ingest_document: ['api:files'],
                    index_document: ['api:files'],
                    answer_prompt: ['api:conversations'],
                }

                if(body.message in mapping) {
                    // @ts-ignore
                    for(const key of mapping[body.message]) {
                        invalidate(key)
                    }
                }

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

<div class="container">
    <nav>
        <div class="sticky">
            <Navigation />
        </div>
    </nav>

    <slot />
</div>

<style>
    :root {
        --box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.5);
    }

    .container {
        display: grid;

        grid-template-areas:
            "nav content content content"
            "nav content content content"
            "nav content content content";
        grid-template-columns: 20rem 5fr 6fr 5fr;
        grid-template-rows: var(--header-height) 1fr var(--footer-height);

        height: 100vh;
    }

    nav {
        display: grid;
        grid-area: nav;
    }

    .sticky {
        height: 100vh;
        display: grid;
        grid-template-rows: var(--header-height) 1fr var(--footer-height);
        top: 0;
        position: sticky;
        z-index: 3;
        color: var(--text-color-light);
    }
</style>
