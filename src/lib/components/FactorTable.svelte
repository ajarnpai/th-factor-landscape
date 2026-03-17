<script>
  import factors from '$lib/data/factors.json';
  import groups from '$lib/data/groups.json';
  import { fmt } from '$lib/utils/format.js';
  import FactorCard from './FactorCard.svelte';
  import { activeGroups } from '$lib/stores/filters.js';

  let sortCol = $state('tStat');
  let sortAsc = $state(false);
  let expandedRow = $state(null);

  // Color map
  const colorMap = {};
  for (const g of groups) {
    for (const f of g.factors) colorMap[f] = g.color;
  }

  let filtered = $derived(
    factors.filter(f => $activeGroups.has(f.group))
  );

  let sorted = $derived(
    [...filtered].sort((a, b) => {
      let va = a[sortCol], vb = b[sortCol];
      if (va == null) return 1;
      if (vb == null) return -1;
      if (typeof va === 'string') {
        return sortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
      }
      if (typeof va === 'boolean') {
        return sortAsc ? (va === vb ? 0 : va ? -1 : 1) : (va === vb ? 0 : va ? 1 : -1);
      }
      return sortAsc ? va - vb : vb - va;
    })
  );

  function toggleSort(col) {
    if (sortCol === col) {
      sortAsc = !sortAsc;
    } else {
      sortCol = col;
      sortAsc = col === 'label' || col === 'group';
    }
  }

  function toggleExpand(name) {
    expandedRow = expandedRow === name ? null : name;
  }

  const columns = [
    { key: 'label', header: 'Factor' },
    { key: 'group', header: 'Category' },
    { key: 'tStat', header: 't-stat' },
    { key: 'sharpe', header: 'Sharpe' },
    { key: 'hlzPass', header: '|t| > 3' },
  ];
</script>

<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        {#each columns as col}
          <th onclick={() => toggleSort(col.key)}
              class:sorted={sortCol === col.key}>
            {col.header}
            {#if sortCol === col.key}
              <span class="sort-arrow">{sortAsc ? '\u25B2' : '\u25BC'}</span>
            {/if}
          </th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each sorted as factor (factor.name)}
        <tr onclick={() => toggleExpand(factor.name)}
            class:expanded={expandedRow === factor.name}>
          <td>
            <span class="color-dot" style="background: {colorMap[factor.name]}"></span>
            {factor.label}
          </td>
          <td class="td-group">{factor.group}</td>
          <td class="td-num">{fmt(factor.tStat)}</td>
          <td class="td-num">{fmt(factor.sharpe)}</td>
          <td>
            {#if factor.hlzPass}
              <span class="badge pass">Pass</span>
            {:else}
              <span class="badge">{'\u2014'}</span>
            {/if}
          </td>
        </tr>
        {#if expandedRow === factor.name}
          <tr class="card-row">
            <td colspan="5">
              <FactorCard {factor} />
            </td>
          </tr>
        {/if}
      {/each}
    </tbody>
  </table>
</div>

<style>
  .table-wrapper {
    overflow-x: auto;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
  }
  th {
    text-align: left;
    padding: 0.6rem 0.75rem;
    border-bottom: 2px solid var(--color-border);
    cursor: pointer;
    white-space: nowrap;
    font-weight: 600;
    font-size: 0.8rem;
    color: var(--color-text-secondary);
    user-select: none;
  }
  th.sorted {
    color: var(--color-text);
  }
  .sort-arrow {
    font-size: 0.6rem;
    margin-left: 0.2rem;
  }
  td {
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid #f0f0f0;
  }
  tr {
    cursor: pointer;
    transition: background 0.15s;
  }
  tr:hover {
    background: var(--color-surface);
  }
  tr.expanded {
    background: var(--color-surface);
  }
  .card-row {
    cursor: default;
  }
  .card-row:hover {
    background: none;
  }
  .card-row td {
    padding: 0;
    border-bottom: 2px solid var(--color-border);
  }
  .td-num {
    font-variant-numeric: tabular-nums;
    text-align: right;
  }
  .td-group {
    font-size: 0.75rem;
    color: var(--color-text-muted);
  }
  .color-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 0.4rem;
    vertical-align: middle;
  }
  .badge {
    font-size: 0.7rem;
    padding: 0.15rem 0.4rem;
    border-radius: 3px;
    color: var(--color-text-muted);
  }
  .badge.pass {
    background: #e8f5e9;
    color: #2e7d32;
    font-weight: 600;
  }
</style>
