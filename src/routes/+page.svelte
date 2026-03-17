<script>
  import Part1 from '$lib/components/Part1.svelte';
  import Part2 from '$lib/components/Part2.svelte';
  import FilterPills from '$lib/components/FilterPills.svelte';
  import RiskReturnScatter from '$lib/components/RiskReturnScatter.svelte';
  import Part3 from '$lib/components/Part3.svelte';
</script>

<header class="site-header">
  <div class="header-content">
    <span class="header-title">Factor Investing in Thailand</span>
    <span class="header-credit">Kanis Saengchote &middot; Chulalongkorn Business School &middot; Co-created with Claude Code</span>
  </div>
</header>

<main>
  <Part1 />

  <div class="section-divider">
    <div class="divider-line"></div>
  </div>

  <Part2 />

  <section class="scatter-section">
    <div class="scatter-inner">
      <div class="scatter-header">
        <h2>Risk and Return</h2>
        <p class="section-subtitle">
          Annualized return vs. volatility for all 66 factors.
          Dot size reflects |t-statistic|. Dashed lines show constant Sharpe ratio contours.
        </p>
      </div>
      <FilterPills />
      <div class="scatter-container">
        <RiskReturnScatter />
      </div>
    </div>
  </section>

  <Part3 />
</main>

<footer>
  <div class="footer-content">
    <p class="footer-credit">Kanis Saengchote &middot; Chulalongkorn Business School</p>
    <p class="footer-sub">Co-created with Claude Code</p>
    <div class="footer-ctas">
      <a href="https://www.ajarnpai.com/" target="_blank" rel="noopener" class="footer-cta">
        Follow my work &rarr;
      </a>
      <a href="https://www.youtube.com/@ajarnpai" target="_blank" rel="noopener" class="footer-cta footer-cta-yt">
        My YouTube Channel &rarr;
      </a>
    </div>
  </div>
</footer>

<style>
  .site-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(250, 248, 244, 0.92);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--color-border);
    padding: 0.65rem 2rem;
  }
  .header-content {
    max-width: var(--max-width);
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header-title {
    font-family: var(--font-display);
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--color-text);
    letter-spacing: -0.01em;
  }
  .header-credit {
    font-size: 0.72rem;
    color: var(--color-text-muted);
    letter-spacing: 0.02em;
  }

  .section-divider {
    max-width: 120px;
    margin: 0 auto;
    padding: 1rem 0;
  }
  .divider-line {
    height: 1px;
    background: var(--color-border);
  }

  main {
    width: 100%;
  }

  .scatter-section {
    background: var(--color-surface);
    padding: 5rem 2rem;
  }
  .scatter-inner {
    max-width: var(--max-width);
    margin: 0 auto;
  }
  .scatter-header {
    margin-bottom: 2rem;
  }
  .scatter-header h2 {
    font-size: 2.2rem;
    color: var(--color-text);
    margin-bottom: 0.6rem;
  }
  .section-subtitle {
    color: var(--color-text-secondary);
    font-size: 0.95rem;
    max-width: 600px;
    line-height: 1.5;
  }
  .scatter-container {
    margin-top: 2rem;
  }

  footer {
    padding: 4rem 2rem;
    text-align: center;
    border-top: 1px solid var(--color-border);
  }
  .footer-content {
    max-width: var(--max-width);
    margin: 0 auto;
  }
  .footer-credit {
    font-family: var(--font-display);
    font-size: 1rem;
    color: var(--color-text);
    margin-bottom: 0.25rem;
  }
  .footer-sub {
    font-size: 0.78rem;
    color: var(--color-text-muted);
  }
  .footer-ctas {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 1.25rem;
  }
  .footer-cta {
    display: inline-block;
    padding: 0.6rem 1.5rem;
    font-family: var(--font-display);
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--color-accent);
    border: 1.5px solid var(--color-accent);
    border-radius: 4px;
    transition: background 0.2s, color 0.2s;
    letter-spacing: -0.01em;
  }
  .footer-cta:hover {
    background: var(--color-accent);
    color: #fff;
    border-bottom-color: var(--color-accent);
  }

  @media (max-width: 640px) {
    .site-header { padding: 0.5rem 1rem; }
    .header-content {
      flex-direction: column;
      gap: 0.15rem;
      text-align: center;
    }
    .scatter-section { padding: 3rem 1rem; }
  }
</style>
