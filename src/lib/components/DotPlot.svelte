<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import factors from '$lib/data/factors.json';
  import groups from '$lib/data/groups.json';
  import { fmt } from '$lib/utils/format.js';

  let { highlightGroup = null, startFaded = false } = $props();

  let container;
  let tooltip = $state({ visible: false, x: 0, y: 0, factor: null });

  // Build color map
  const colorMap = {};
  for (const g of groups) {
    for (const f of g.factors) {
      colorMap[f] = g.color;
    }
  }

  // Sort factors by group then by t-stat within group (descending)
  const sorted = [...factors].sort((a, b) => {
    if (a.groupIndex !== b.groupIndex) return a.groupIndex - b.groupIndex;
    return (b.tStat ?? 0) - (a.tStat ?? 0);
  });

  let svg;

  onMount(() => {
    draw();
    const ro = new ResizeObserver(() => draw());
    ro.observe(container);
    return () => ro.disconnect();
  });

  function draw() {
    if (!container) return;
    const rect = container.getBoundingClientRect();
    const width = rect.width;
    const margin = { top: 24, right: 30, bottom: 40, left: 90 };
    const height = Math.max(sorted.length * 18, 400);

    d3.select(container).select('svg').remove();

    svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height + margin.top + margin.bottom);

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const plotWidth = width - margin.left - margin.right;

    // Scales
    const tStats = sorted.map(f => f.tStat ?? 0);
    const extent = d3.extent(tStats);
    const pad = Math.max(Math.abs(extent[0]), Math.abs(extent[1])) * 0.1;

    const xScale = d3.scaleLinear()
      .domain([Math.min(extent[0] - pad, -5), Math.max(extent[1] + pad, 5)])
      .range([0, plotWidth]);

    const yScale = d3.scaleBand()
      .domain(sorted.map(f => f.name))
      .range([0, height])
      .padding(0.3);

    // Zero line
    g.append('line')
      .attr('x1', xScale(0)).attr('x2', xScale(0))
      .attr('y1', 0).attr('y2', height)
      .attr('stroke', '#ddd').attr('stroke-width', 1);

    // HLZ threshold lines
    for (const t of [-3, 3]) {
      g.append('line')
        .attr('x1', xScale(t)).attr('x2', xScale(t))
        .attr('y1', 0).attr('y2', height)
        .attr('stroke', 'var(--color-hlz)')
        .attr('stroke-width', 1)
        .attr('stroke-dasharray', '4,4')
        .attr('opacity', 0.7);
    }

    // HLZ label (only on positive side)
    g.append('text')
      .attr('x', xScale(3))
      .attr('y', -8)
      .attr('text-anchor', 'middle')
      .attr('font-size', '10px')
      .attr('fill', 'var(--color-hlz)')
      .text('|t| = 3.0');

    // X axis
    g.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale).ticks(10))
      .selectAll('text')
      .attr('font-size', '11px')
      .attr('fill', 'var(--color-text-secondary)');

    // Style axis lines for dark bg
    g.selectAll('.domain').attr('stroke', '#ddd');
    g.selectAll('.tick line').attr('stroke', '#ddd');

    // X axis label
    g.append('text')
      .attr('x', plotWidth / 2)
      .attr('y', height + 35)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('fill', '#8a8aa0')
      .text('t-statistic');

    // Y axis labels
    const yAxisG = g.append('g')
      .call(d3.axisLeft(yScale).tickSize(0));
    yAxisG.selectAll('text')
      .attr('font-size', '10px')
      .attr('fill', '#8a8aa0')
      .text(d => {
        const fac = sorted.find(f => f.name === d);
        return fac ? fac.label : d;
      });

    // Remove y-axis line
    yAxisG.select('.domain').remove();

    // Dots
    g.selectAll('.dot')
      .data(sorted)
      .join('circle')
      .attr('class', 'dot')
      .attr('cx', d => xScale(d.tStat ?? 0))
      .attr('cy', d => yScale(d.name) + yScale.bandwidth() / 2)
      .attr('r', 5)
      .attr('fill', d => startFaded ? '#c8c5be' : (colorMap[d.name] || '#888'))
      .attr('stroke', '#fff')
      .attr('stroke-width', 1)
      .attr('opacity', startFaded ? 0.5 : 1)
      .style('cursor', 'pointer')
      .on('mouseenter', (event, d) => {
        const r = container.getBoundingClientRect();
        tooltip = {
          visible: true,
          x: event.clientX - r.left,
          y: event.clientY - r.top - 10,
          factor: d,
        };
      })
      .on('mouseleave', () => {
        tooltip = { ...tooltip, visible: false };
      });
  }

  // Update dot opacity and color when highlightGroup changes
  $effect(() => {
    if (!svg) return;
    const group = highlightGroup;
    svg.selectAll('.dot')
      .transition()
      .duration(400)
      .attr('opacity', d => {
        if (group === null) return startFaded ? 0.5 : 1;
        return d.group === group ? 1 : 0.1;
      })
      .attr('fill', d => {
        if (group === null) return startFaded ? '#c8c5be' : (colorMap[d.name] || '#888');
        return d.group === group ? (colorMap[d.name] || '#888') : '#ddd8d0';
      })
      .attr('r', d => {
        if (group === null) return 5;
        return d.group === group ? 6 : 4;
      });
  });
</script>

<div class="dotplot-wrapper" bind:this={container}>
  {#if tooltip.visible && tooltip.factor}
    <div class="tooltip"
         style="left: {tooltip.x}px; top: {tooltip.y}px;">
      <strong>{tooltip.factor.label}</strong>
      <span class="tooltip-group">{tooltip.factor.group}</span>
      {#if tooltip.factor.description}
        <div class="tooltip-desc">{tooltip.factor.description}</div>
      {/if}
      <div class="tooltip-stats">
        <span>t-stat: {fmt(tooltip.factor.tStat)}</span>
        <span>Sharpe: {fmt(tooltip.factor.sharpe)}</span>
      </div>
    </div>
  {/if}
</div>

<style>
  .dotplot-wrapper {
    position: relative;
    width: 100%;
  }
  .tooltip {
    position: absolute;
    background: white;
    border: 1px solid var(--color-border);
    border-radius: 6px;
    padding: 0.75rem;
    font-size: 0.8rem;
    pointer-events: none;
    transform: translate(-50%, -100%);
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    z-index: 10;
    min-width: 180px;
  }
  .tooltip strong {
    display: block;
    font-size: 0.9rem;
  }
  .tooltip-group {
    display: block;
    color: var(--color-text-muted);
    font-size: 0.75rem;
    margin-bottom: 0.4rem;
  }
  .tooltip-stats {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }
  .tooltip-desc {
    font-size: 0.78rem;
    color: var(--color-text-secondary);
    line-height: 1.4;
    margin-bottom: 0.4rem;
    max-width: 260px;
  }
</style>
