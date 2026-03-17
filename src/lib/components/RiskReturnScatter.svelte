<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import factors from '$lib/data/factors.json';
  import groups from '$lib/data/groups.json';
  import { fmt } from '$lib/utils/format.js';
  import { activeGroups } from '$lib/stores/filters.js';

  let container;
  let tooltip = $state({ visible: false, x: 0, y: 0, factor: null });
  let svg, gPlot, xScale, yScale, rScale, plotW, plotH;
  let hasTransitioned = false;

  // Build color map
  const colorMap = {};
  for (const g of groups) {
    for (const f of g.factors) colorMap[f] = g.color;
  }

  // All factors with valid stats, sorted same as DotPlot (group, then t-stat desc)
  const data = factors
    .filter(f => f.annRet != null && f.annVol != null)
    .sort((a, b) => {
      if (a.groupIndex !== b.groupIndex) return a.groupIndex - b.groupIndex;
      return (b.tStat ?? 0) - (a.tStat ?? 0);
    });

  const maxAbsT = d3.max(data, d => Math.abs(d.tStat ?? 0));

  // Starting positions: mimic the dot plot layout (t-stat on x, spread vertically)
  function dotPlotX(d) {
    // Map t-stat to the scatter's x range
    const tExtent = d3.extent(data, f => f.tStat ?? 0);
    const pad = Math.max(Math.abs(tExtent[0]), Math.abs(tExtent[1])) * 0.1;
    const tScale = d3.scaleLinear()
      .domain([Math.min(tExtent[0] - pad, -5), Math.max(tExtent[1] + pad, 5)])
      .range([0, plotW]);
    return tScale(d.tStat ?? 0);
  }

  function dotPlotY(d, i) {
    // Spread evenly across the plot height
    const spacing = plotH / (data.length + 1);
    return spacing * (i + 1);
  }

  // Final scatter positions
  function scatterX(d) { return xScale(d.annVol * 100); }
  function scatterY(d) { return yScale(d.annRet * 100); }

  onMount(() => {
    draw();
    const ro = new ResizeObserver(() => { hasTransitioned = false; draw(); });
    ro.observe(container);

    // Trigger transition when section scrolls into view
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasTransitioned) {
          hasTransitioned = true;
          transitionToScatter();
        }
      },
      { threshold: 0.3 }
    );
    observer.observe(container);

    return () => { ro.disconnect(); observer.disconnect(); };
  });

  function draw() {
    if (!container) return;
    const rect = container.getBoundingClientRect();
    const width = rect.width;
    const height = Math.min(width * 0.6, 550);
    const margin = { top: 30, right: 30, bottom: 50, left: 65 };

    d3.select(container).select('svg').remove();

    svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    gPlot = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    plotW = width - margin.left - margin.right;
    plotH = height - margin.top - margin.bottom;

    // Scatter scales (in percentage)
    const xVals = data.map(f => f.annVol * 100);
    const yVals = data.map(f => f.annRet * 100);

    xScale = d3.scaleLinear()
      .domain([0, d3.max(xVals) * 1.1])
      .range([0, plotW]);

    yScale = d3.scaleLinear()
      .domain([d3.min(yVals) * 1.2 - 1, d3.max(yVals) * 1.1 + 1])
      .range([plotH, 0]);

    rScale = d3.scaleSqrt()
      .domain([0, maxAbsT])
      .range([3, 14]);

    // Grid lines
    gPlot.append('g').attr('class', 'grid-lines')
      .selectAll('line')
      .data(yScale.ticks(8))
      .join('line')
      .attr('x1', 0).attr('x2', plotW)
      .attr('y1', d => yScale(d)).attr('y2', d => yScale(d))
      .attr('stroke', '#eee').attr('stroke-width', 1)
      .attr('opacity', 0);

    // Zero line
    gPlot.append('line').attr('class', 'zero-line')
      .attr('x1', 0).attr('x2', plotW)
      .attr('y1', yScale(0)).attr('y2', yScale(0))
      .attr('stroke', '#bbb').attr('stroke-width', 1)
      .attr('stroke-dasharray', '3,3')
      .attr('opacity', 0);

    // Sharpe ratio iso-curves
    for (const sr of [0.5, 1.0]) {
      const lineData = d3.range(0.1, d3.max(xVals) * 1.1, 0.5)
        .map(vol => ({ x: vol, y: sr * vol }))
        .filter(d => d.y <= d3.max(yVals) * 1.1 + 1);

      if (lineData.length > 1) {
        gPlot.append('path')
          .attr('class', 'sr-line')
          .datum(lineData)
          .attr('d', d3.line().x(d => xScale(d.x)).y(d => yScale(d.y)))
          .attr('fill', 'none')
          .attr('stroke', '#ddd')
          .attr('stroke-width', 1)
          .attr('stroke-dasharray', '6,4')
          .attr('opacity', 0);

        const last = lineData[lineData.length - 1];
        gPlot.append('text')
          .attr('class', 'sr-label')
          .attr('x', xScale(last.x) + 3)
          .attr('y', yScale(last.y))
          .attr('font-size', '9px')
          .attr('fill', '#bbb')
          .attr('dominant-baseline', 'middle')
          .attr('opacity', 0)
          .text(`SR=${sr}`);
      }
    }

    // Axes (hidden initially, fade in during transition)
    const xAxis = gPlot.append('g').attr('class', 'x-axis')
      .attr('transform', `translate(0,${plotH})`)
      .attr('opacity', 0)
      .call(d3.axisBottom(xScale).ticks(8).tickFormat(d => d + '%'));
    xAxis.selectAll('text').attr('font-size', '11px');

    const yAxis = gPlot.append('g').attr('class', 'y-axis')
      .attr('opacity', 0)
      .call(d3.axisLeft(yScale).ticks(8).tickFormat(d => d + '%'));
    yAxis.selectAll('text').attr('font-size', '11px');

    // Axis labels (hidden initially)
    gPlot.append('text').attr('class', 'x-label')
      .attr('x', plotW / 2).attr('y', plotH + 40)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('fill', 'var(--color-text-secondary)')
      .attr('opacity', 0)
      .text('Annualized Volatility');

    gPlot.append('text').attr('class', 'y-label')
      .attr('transform', 'rotate(-90)')
      .attr('x', -plotH / 2).attr('y', -50)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('fill', 'var(--color-text-secondary)')
      .attr('opacity', 0)
      .text('Annualized Return');

    // Dots — start in dot-plot arrangement
    gPlot.selectAll('.dot')
      .data(data)
      .join('circle')
      .attr('class', 'dot')
      .attr('cx', (d, i) => dotPlotX(d))
      .attr('cy', (d, i) => dotPlotY(d, i))
      .attr('r', d => rScale(Math.abs(d.tStat ?? 0)))
      .attr('fill', d => colorMap[d.name] || '#888')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .attr('opacity', 0.85)
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

    // Labels (hidden, appear after transition)
    const notable = data
      .filter(d => d.hlzPass || d.name === 'mkt')
      .slice(0, 10);

    gPlot.selectAll('.factor-label')
      .data(notable)
      .join('text')
      .attr('class', 'factor-label')
      .attr('x', d => scatterX(d) + rScale(Math.abs(d.tStat ?? 0)) + 3)
      .attr('y', d => scatterY(d) + 3)
      .attr('font-size', '9px')
      .attr('fill', 'var(--color-text-secondary)')
      .attr('opacity', 0)
      .text(d => d.label);

    // If already scrolled past, show final state immediately
    if (hasTransitioned) {
      showFinalState();
    }
  }

  function transitionToScatter() {
    if (!gPlot) return;
    const dur = 1200;

    // Fly dots to scatter positions
    gPlot.selectAll('.dot')
      .transition()
      .duration(dur)
      .ease(d3.easeCubicInOut)
      .attr('cx', d => scatterX(d))
      .attr('cy', d => scatterY(d));

    // Fade in scatter chrome
    gPlot.selectAll('.grid-lines line').transition().delay(dur * 0.3).duration(600).attr('opacity', 1);
    gPlot.select('.zero-line').transition().delay(dur * 0.3).duration(600).attr('opacity', 1);
    gPlot.selectAll('.sr-line').transition().delay(dur * 0.5).duration(600).attr('opacity', 1);
    gPlot.selectAll('.sr-label').transition().delay(dur * 0.5).duration(600).attr('opacity', 1);
    gPlot.select('.x-axis').transition().delay(dur * 0.4).duration(600).attr('opacity', 1);
    gPlot.select('.y-axis').transition().delay(dur * 0.4).duration(600).attr('opacity', 1);
    gPlot.select('.x-label').transition().delay(dur * 0.6).duration(600).attr('opacity', 1);
    gPlot.select('.y-label').transition().delay(dur * 0.6).duration(600).attr('opacity', 1);

    // Labels appear after dots land
    gPlot.selectAll('.factor-label')
      .transition()
      .delay(dur + 200)
      .duration(400)
      .attr('opacity', 1);
  }

  function showFinalState() {
    if (!gPlot) return;
    gPlot.selectAll('.dot')
      .attr('cx', d => scatterX(d))
      .attr('cy', d => scatterY(d));
    gPlot.selectAll('.grid-lines line').attr('opacity', 1);
    gPlot.select('.zero-line').attr('opacity', 1);
    gPlot.selectAll('.sr-line').attr('opacity', 1);
    gPlot.selectAll('.sr-label').attr('opacity', 1);
    gPlot.select('.x-axis').attr('opacity', 1);
    gPlot.select('.y-axis').attr('opacity', 1);
    gPlot.select('.x-label').attr('opacity', 1);
    gPlot.select('.y-label').attr('opacity', 1);
    gPlot.selectAll('.factor-label').attr('opacity', 1);
  }

  // React to filter changes
  $effect(() => {
    if (!gPlot) return;
    const current = $activeGroups;
    gPlot.selectAll('.dot')
      .transition()
      .duration(400)
      .attr('opacity', d => current.has(d.group) ? 0.85 : 0.08)
      .attr('r', d => {
        const base = rScale(Math.abs(d.tStat ?? 0));
        return current.has(d.group) ? base : base * 0.6;
      });

    gPlot.selectAll('.factor-label')
      .transition()
      .duration(400)
      .attr('opacity', d => current.has(d.group) ? 1 : 0);
  });
</script>

<div class="scatter-wrapper" bind:this={container}>
  {#if tooltip.visible && tooltip.factor}
    <div class="tooltip"
         style="left: {tooltip.x}px; top: {tooltip.y}px;">
      <strong>{tooltip.factor.label}</strong>
      <span class="tooltip-group">{tooltip.factor.group}</span>
      <div class="tooltip-stats">
        <span>Return: {(tooltip.factor.annRet * 100).toFixed(1)}%</span>
        <span>Volatility: {(tooltip.factor.annVol * 100).toFixed(1)}%</span>
        <span>t-stat: {fmt(tooltip.factor.tStat)}</span>
        <span>Sharpe: {fmt(tooltip.factor.sharpe)}</span>
      </div>
    </div>
  {/if}
</div>

<style>
  .scatter-wrapper {
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
</style>
