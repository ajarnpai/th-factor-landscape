<script>
  let { value, label, suffix = '' } = $props();
  let visible = $state(false);
  let displayed = $state(0);
  let el;

  $effect(() => {
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !visible) {
          visible = true;
          animateCount();
        }
      },
      { threshold: 0.5 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  });

  function animateCount() {
    const duration = 1200;
    const start = performance.now();
    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      displayed = Math.round(eased * value);
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
</script>

<div class="stat-callout" bind:this={el} class:visible>
  <span class="stat-number">{displayed.toLocaleString()}{suffix}</span>
  <span class="stat-label">{label}</span>
</div>

<style>
  .stat-callout {
    text-align: center;
    opacity: 0;
    transform: translateY(16px);
    transition: opacity 0.7s ease, transform 0.7s ease;
  }
  .stat-callout.visible {
    opacity: 1;
    transform: translateY(0);
  }
  .stat-number {
    display: block;
    font-family: var(--font-display);
    font-size: 3.2rem;
    font-weight: 700;
    color: var(--color-text);
    line-height: 1;
    letter-spacing: -0.03em;
  }
  .stat-label {
    display: block;
    font-size: 0.85rem;
    color: var(--color-text-muted);
    margin-top: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
  }
</style>
