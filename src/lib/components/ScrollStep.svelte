<script>
  let { children } = $props();
</script>

<div class="scroll-step">
  {@render children()}
</div>

<style>
  .scroll-step {
    min-height: 60vh;
    display: flex;
    align-items: center;
    padding: 2rem 1.5rem;
  }
  .scroll-step :global(h3) {
    font-size: 1.3rem;
    margin-bottom: 0.75rem;
  }
  .scroll-step :global(p) {
    font-size: 1rem;
    color: var(--color-text-secondary);
    line-height: 1.6;
    max-width: 360px;
  }
</style>
