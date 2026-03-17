<script>
  import groups from '$lib/data/groups.json';
  import { activeGroups } from '$lib/stores/filters.js';

  function toggleGroup(name) {
    activeGroups.update(current => {
      const next = new Set(current);
      if (next.has(name)) next.delete(name);
      else next.add(name);
      return next;
    });
  }
</script>

<div class="filter-pills">
  {#each groups as g}
    <button
      class="pill"
      class:active={$activeGroups.has(g.name)}
      style="--pill-color: {g.color}"
      onclick={() => toggleGroup(g.name)}
    >
      {g.name}
    </button>
  {/each}
</div>

<style>
  .filter-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }
  .pill {
    border: 1px solid var(--pill-color);
    background: white;
    color: var(--pill-color);
    padding: 0.3rem 0.7rem;
    border-radius: 20px;
    font-size: 0.75rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  .pill.active {
    background: var(--pill-color);
    color: white;
  }
</style>
