import { readable } from 'svelte/store';

function getWidth() {
  return typeof window !== 'undefined' ? window.innerWidth : 1200;
}

export const viewportWidth = readable(getWidth(), (set) => {
  if (typeof window === 'undefined') return;
  const handler = () => set(window.innerWidth);
  window.addEventListener('resize', handler);
  return () => window.removeEventListener('resize', handler);
});

export const isMobile = {
  subscribe(fn) {
    return viewportWidth.subscribe(w => fn(w < 768));
  }
};
