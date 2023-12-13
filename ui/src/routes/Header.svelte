<script>
    import Breadcrumbs from "./Breadcrumbs.svelte";
    import Profile from "./Profile.svelte";
</script>

<header>
    <Breadcrumbs />
    
    <Profile />
</header>

<style>
    header {
        display: grid;
        grid-template-columns: 1fr 1fr;
        align-items: center;
        padding: 0 var(--padding-x);
        background: #F9FAFB;
    }
</style>
