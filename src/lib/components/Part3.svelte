<script>
  import FactorTable from './FactorTable.svelte';
</script>

<section class="part3">
  <div class="part3-inner">
    <h2>Full Results</h2>
    <p class="section-subtitle">
      Click any row to see full details. Use the filters to focus on specific groups.
      Sort by any column.
    </p>

    <FactorTable />

    <div class="methodology">
      <h3>Methodology</h3>
      <ul>
        <li><strong>Sample:</strong> SET common stocks, July 2001 &ndash; December 2025 (370 months)</li>
        <li><strong>Construction:</strong> 2&times;3 double-sort (size &times; signal), 30/70 breakpoints (20/80 for PEAD/FIN), value-weighted portfolios (except BAB)</li>
        <li><strong>Size breakpoint:</strong> 90th percentile cumulative market capitalization</li>
        <li><strong>Data source:</strong> SETSMART database</li>
        <li><strong>t-statistics:</strong> mean / standard error (unadjusted); threshold |t| &gt; 3.0</li>
      </ul>
    </div>
  </div>
</section>

<style>
  .part3 {
    padding: 4rem 1.5rem;
    background: var(--color-surface);
  }
  .part3-inner {
    max-width: var(--max-width);
    margin: 0 auto;
  }
  h2 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }
  .section-subtitle {
    color: var(--color-text-secondary);
    margin-bottom: 2rem;
  }
  .methodology {
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid var(--color-border);
  }
  .methodology h3 {
    font-size: 1.1rem;
    margin-bottom: 0.75rem;
  }
  .methodology ul {
    list-style: none;
    padding: 0;
  }
  .methodology li {
    font-size: 0.9rem;
    color: var(--color-text-secondary);
    margin-bottom: 0.4rem;
  }
</style>
