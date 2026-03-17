import { writable } from 'svelte/store';
import groups from '$lib/data/groups.json';

export const activeGroups = writable(new Set(groups.map(g => g.name)));
