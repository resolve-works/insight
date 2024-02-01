
<script>
    import Page from '$lib/Page.svelte';
    import Card from '$lib/Card.svelte'
</script>

<Page>
    <h2>Conversations</h2>

    <div class="message user">
        <aside>
            <h3>U</h3>
        </aside>

        <Card class="card">
            <h3>User</h3>

            <p>What advice is commonly provided by external parties like consultants?</p>
        </Card>
    </div>

    <div class="message bot">
        <aside>
            <h3>B</h3>
        </aside>

        <Card class="card">
            <h3>Bot</h3>

            <p>Consultants provide advice and expertise in various fields to help businesses or individuals solve specific problems or achieve specific goals. The advice given by consultants can vary depending on their area of expertise, but here are some common types of advice consultants may offer:</p>

            <ol>
                <li>Strategic advice: Consultants often help businesses develop long-term strategies for growth, market expansion, or organizational improvement.</li>
                <li>Operational advice: Consultants may provide recommendations on optimizing business processes, improving efficiency, or streamlining operations.</li>
                <li>Financial advice: Consultants with financial expertise may offer advice on budgeting, financial planning, investment strategies, or cost reduction.</li>
                <li>Marketing advice: Consultants can assist with developing marketing strategies, branding, market research, and customer targeting.</li>
                <li>Technology advice: Consultants may provide guidance on IT infrastructure, software implementation, cybersecurity, or digital transformation.</li>
                <li>Human resources advice: Consultants can advise on talent acquisition, employee training and development, performance management, or organizational culture.</li>
            </ol>

            <p>It's important to note that the specific advice given by consultants depends on the unique needs and goals of each client. If you're looking for more detailed information or specific advice, I recommend consulting with a professional consultant in the relevant field. </p>
        </Card>
    </div>
</Page>

<style>
    :root {
        --profile-size: 4rem;
        --profile-margin: 1rem;
        --triangle-size: 3rem;
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
</style>
