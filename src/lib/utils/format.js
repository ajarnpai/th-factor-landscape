/** Format number to fixed decimals, handling null. */
export function fmt(val, decimals = 2) {
  if (val == null) return '\u2014';
  return val.toFixed(decimals);
}

/** Format as percentage. */
export function pct(val, decimals = 1) {
  if (val == null) return '\u2014';
  return (val * 100).toFixed(decimals) + '%';
}
