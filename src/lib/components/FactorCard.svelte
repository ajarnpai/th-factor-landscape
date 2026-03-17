<script>
  import { fmt } from '$lib/utils/format.js';
  let { factor } = $props();
</script>

<div class="factor-card">
  <div class="card-grid">
    <div class="card-stat">
      <span class="card-label">t-statistic</span>
      <span class="card-value">{fmt(factor.tStat)}</span>
    </div>
    <div class="card-stat">
      <span class="card-label">Sharpe</span>
      <span class="card-value">{fmt(factor.sharpe)}</span>
    </div>
    <div class="card-stat">
      <span class="card-label">Max Drawdown</span>
      <span class="card-value">{fmt(factor.maxDrawdown)}</span>
    </div>
    {#if factor.reference}
      <div class="card-stat">
        <span class="card-label">Reference</span>
        <span class="card-value card-ref-value">{factor.reference}</span>
      </div>
    {/if}
  </div>
  {#if factor.description}
    <div class="card-desc">
      <span>{factor.description}</span>
    </div>
  {/if}
</div>

<style>
  .factor-card {
    padding: 1rem 1.5rem;
    background: var(--color-surface);
    border-top: 1px solid var(--color-border);
  }
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }
  .card-stat {
    display: flex;
    flex-direction: column;
  }
  .card-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--color-text-muted);
    margin-bottom: 0.15rem;
  }
  .card-value {
    font-size: 0.95rem;
    font-weight: 600;
  }
  .card-ref-value {
    font-weight: 500;
    font-size: 0.8rem;
  }
  .card-desc {
    font-size: 0.85rem;
    color: var(--color-text-secondary);
    line-height: 1.5;
  }
</style>
