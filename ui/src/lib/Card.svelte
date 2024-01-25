
<div {...$$props}>
    <slot />
</div>

<style>
    div {
        background: var(--color-white);
        padding: 1rem calc(var(--padding-x) * 1.5);
        margin-bottom: 1rem;
        border-bottom: var(--border-size) solid var(--color-page-darker);
    }
</style>
