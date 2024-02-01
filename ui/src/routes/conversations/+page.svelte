
<script lang="ts">
    import Page from '$lib/Page.svelte'
    import Card from '$lib/Card.svelte'
    import Icon from '$lib/Icon.svelte'
    import { invalidate } from '$app/navigation';

    let query_input: HTMLInputElement;

    export let data;
    const { access_token } = data;
    let is_disabled = false

    async function create_prompt(e: SubmitEvent) {
        let form_data = new FormData(e.target);
        // Strip empty keys
        let data = Object.fromEntries(Array.from(form_data).filter(([key, value]) => !!value))
        // Clear form
        is_disabled = true;
        
        const prompt_response = await fetch('/api/v1/prompts', { 
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,
                'Prefer': 'return=representation',
            },
            body: JSON.stringify(data),
        })
        if(prompt_response.status != 201) {
            throw new Error('Could not create prompt')
        }

        e.target.reset()

        await invalidate(url => url.pathname == '/api/v1/prompts')

        const prompts = await prompt_response.json();
        const prompt = prompts[0];

        const answer_response = await fetch('/api/v1/rpc/answer_prompt', { 
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,
            },
            body: JSON.stringify({ id: prompt.id })
        })
        if(answer_response.status != 204) {
            throw new Error('Could not trigger answering of prompt')
        }

        await invalidate(url => url.pathname == '/api/v1/prompts')
        is_disabled = false
        query_input.focus()
    }
</script>

<Page>
    <div class="chat">
        <div class="messages">
            {#each data.prompts as prompt}
                <div class="message user">
                    <aside>
                        <h3>U</h3>
                    </aside>

                    <Card class="card">
                        <h3>User</h3>

                        <p>{ prompt.query }</p>
                    </Card>
                </div>

                <div class="message bot">
                    <aside>
                        <h3>B</h3>
                    </aside>

                    <Card class="card">
                        <h3>Bot</h3>

                        {#if prompt.response}
                            <p>{ prompt.response }</p>
                            <ul>
                                {#each prompt.sources as source}
                                    <li>{JSON.stringify(source)}</li>
                                {/each}
                            </ul>
                        {:else}
                            <Icon class="gg-loadbar" />
                        {/if}
                    </Card>
                </div>
            {/each}
        </div>

        <form on:submit|preventDefault={create_prompt}>
            <input type="text" bind:this={query_input} disabled={is_disabled} name="query" placeholder="What's your question?">
            <input type="number" disabled={is_disabled} name="similarity_top_k" placeholder="Pages (default: 3)" min="0">
            <input type="submit" disabled={is_disabled} value="Prompt" class="primary">
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

    .message.user {
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

    .message.bot aside {
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

    .message.bot :global(.card:before) {
        left: calc(var(--triangle-size) * -1);
        border-right-color: var(--color-white);
    }
    .message.user :global(.card:before) {
        right: calc(var(--triangle-size) * -1);
        border-left-color: var(--color-white);
    }

    form {
        display: grid;
        grid-template-columns: 4fr 1fr 1fr;
        align-items: center;
        gap: 0.5rem;
    }
</style>
