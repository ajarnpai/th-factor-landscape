<script>
  import StatCallout from './StatCallout.svelte';
</script>

<section class="part1">
  <div class="hero">
    <h1>Factor Investing<br/>in Thailand</h1>
    <p class="subtitle">
      A comprehensive replication of global factor strategies
      using Thai stock market data
    </p>
  </div>

  <div class="narrative">
    <p>
      Factor investing — building portfolios based on characteristics like
      value, profitability, or momentum — has transformed how investors
      think about returns. But most of the evidence comes from the
      United States and developed markets.
    </p>
    <p class="pull-quote">
      Does it work in Thailand?
    </p>
    <p>
      This project builds on
      <a href="https://doi.org/10.1016/j.pacfin.2021.101632"
         target="_blank" rel="noopener">
        "Digesting anomalies: A q-factor approach for the Thai market"
      </a>
      (Charoenwong, Nettayanun, Saengchote, 2021) and the CMDF-funded and SET-supported
      <a href="https://dashboard.factorlibrary.app/"
         target="_blank" rel="noopener">Factor Library</a>
      to present a broader replication: 81 well-known factors from the
      global asset pricing literature, tested on the Stock Exchange of Thailand.
    </p>
  </div>

  <div class="stats-row">
    <StatCallout value={81} label="factors tested" />
    <StatCallout value={370} label="months of data" suffix="+" />
    <StatCallout value={1100} label="securities" suffix="+" />
  </div>

  <div class="narrative">
    <p>
      The factors span 11 categories — from the Fama-French six to value,
      profitability, investment, quality, and beyond. Each was constructed
      using standard double-sort methodology on SET common stocks from
      July 2001 to December 2025.
    </p>
  </div>
</section>

<style>
  .part1 {
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 7rem 2rem 4rem;
  }
  .hero {
    text-align: center;
    margin-bottom: 4rem;
  }
  h1 {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1.25rem;
    letter-spacing: -0.03em;
    line-height: 1.05;
  }
  .subtitle {
    font-size: 1.1rem;
    color: var(--color-text-secondary);
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.6;
  }
  .narrative {
    max-width: 580px;
    margin: 0 auto 2.5rem;
    font-size: 1.05rem;
  }
  .narrative p {
    margin-bottom: 1.1rem;
  }
  .pull-quote {
    font-family: var(--font-display);
    font-style: italic;
    font-size: 1.5rem;
    color: var(--color-text);
    text-align: center;
    padding: 1.5rem 0;
    letter-spacing: -0.01em;
  }
  .stats-row {
    display: flex;
    justify-content: center;
    gap: 5rem;
    margin: 4rem 0;
  }
  @media (max-width: 640px) {
    h1 { font-size: 2.4rem; }
    .stats-row { gap: 2.5rem; flex-wrap: wrap; }
    .part1 { padding: 4rem 1.25rem 2rem; }
    .pull-quote { font-size: 1.25rem; }
  }
</style>
