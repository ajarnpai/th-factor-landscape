<script>
  import DotPlot from './DotPlot.svelte';
  import groups from '$lib/data/groups.json';

  let highlightGroup = $state(null);

  const groupInfo = {
    "Fama-French Six": "The foundational six factors: market, size, value, profitability, investment, and momentum.",
    "q-Factors (HXZ)": "Hou, Xue, and Zhang's q-factor model: size, investment, and profitability.",
    "Behavioral": "Daniel, Hirshleifer, and Sun (2020) short- and long-horizon behavioral factors: post-earnings announcement drift and composite financing.",
    "QMJ": "Asness, Frazzini, and Pedersen's quality-minus-junk composite and its components.",
    "Low-Risk": "Betting-against-beta, volatility, idiosyncratic volatility, and lottery demand.",
    "Momentum": "Six-month momentum and one-month short-term reversal.",
    "Value": "Nine measures of cheapness: earnings, cash flow, sales, dividends, and book value ratios.",
    "Profitability": "Thirteen measures spanning margins, turnover, and return on assets or equity.",
    "Investment": "Ten measures of asset growth, issuance, and capital allocation.",
    "Quality": "Ten measures including accruals, leverage, distress scores, and growth stability.",
    "Trading / Liquidity": "Turnover, short-term reversal, and illiquidity.",
  };

  function selectGroup(name) {
    highlightGroup = highlightGroup === name ? null : name;
  }
</script>

<section class="part2">
  <div class="part2-header">
    <h2>Results by Category</h2>
    <p class="section-subtitle">
      All 66 factors by t-statistic. Click a category to highlight.
      The dashed line marks the multiple-testing threshold (|t| > 3.0).
    </p>
  </div>

  <div class="part2-content">
    <div class="sidebar">
      <div class="legend">
        {#each groups as g}
          <button
            class="legend-item"
            class:active={highlightGroup === g.name}
            style="--dot-color: {g.color}"
            onclick={() => selectGroup(g.name)}
          >
            <span class="legend-dot"></span>
            <span class="legend-label">{g.name}</span>
            <span class="legend-count">{g.factors.length}</span>
          </button>
        {/each}
      </div>

      <div class="group-card">
        {#if highlightGroup}
          <h3 style="color: {groups.find(g => g.name === highlightGroup)?.color}">{highlightGroup}</h3>
          <p>{groupInfo[highlightGroup]}</p>
        {:else}
          <p class="muted">Click a category to explore.</p>
        {/if}
      </div>
    </div>

    <div class="chart">
      <DotPlot {highlightGroup} startFaded={true} />
    </div>
  </div>
</section>

<style>
  .part2 {
    background: var(--color-surface);
    padding: 5rem 2rem;
  }
  .part2-header {
    text-align: center;
    max-width: var(--max-width);
    margin: 0 auto 3rem;
  }
  h2 {
    font-size: 2.2rem;
    color: var(--color-text);
    margin-bottom: 0.6rem;
  }
  .section-subtitle {
    color: var(--color-text-secondary);
    font-size: 0.95rem;
    max-width: 560px;
    margin: 0 auto;
  }
  .part2-content {
    max-width: var(--max-width);
    margin: 0 auto;
    display: flex;
    gap: 2rem;
  }
  .sidebar {
    flex: 0 0 200px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  .legend {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0.65rem;
    border: none;
    background: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.15s;
    text-align: left;
  }
  .legend-item:hover {
    background: var(--color-bg);
  }
  .legend-item.active {
    background: var(--color-bg);
    box-shadow: inset 2px 0 0 var(--dot-color);
  }
  .legend-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--dot-color);
    flex-shrink: 0;
  }
  .legend-label {
    font-size: 0.78rem;
    color: var(--color-text);
    flex: 1;
  }
  .legend-count {
    font-size: 0.68rem;
    color: var(--color-text-muted);
    font-variant-numeric: tabular-nums;
  }
  .group-card {
    padding: 1rem;
    background: var(--color-bg);
    border-radius: 8px;
    border: 1px solid var(--color-border);
    min-height: 80px;
  }
  .group-card h3 {
    font-family: var(--font-display);
    font-size: 0.95rem;
    margin-bottom: 0.4rem;
    font-weight: 600;
  }
  .group-card p {
    font-size: 0.82rem;
    color: var(--color-text-secondary);
    line-height: 1.5;
  }
  .group-card .muted {
    font-style: italic;
    color: var(--color-text-muted);
  }
  .chart {
    flex: 1;
    min-width: 0;
  }

  @media (max-width: 768px) {
    .part2 { padding: 3rem 1rem; }
    .part2-content { flex-direction: column; }
    .sidebar {
      flex: none;
      flex-direction: row;
      flex-wrap: wrap;
      gap: 0.5rem;
    }
    .legend {
      flex-direction: row;
      flex-wrap: wrap;
      gap: 0.25rem;
    }
    .legend-count { display: none; }
    .group-card { order: 1; }
  }
</style>
