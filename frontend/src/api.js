const API = (import.meta.env.VITE_API_URL || 'https://jokor.onrender.com').replace(/\/$/, '');

export async function apiGet(path) {
  const response = await fetch(`${API}${path}`, { headers: { Accept: 'application/json' } });
  let body = null;
  try { body = await response.json(); } catch { body = null; }
  if (!response.ok) throw new Error(body?.message || `API request failed (${response.status})`);
  if (body?.success === false) throw new Error(body.message || body.error || 'Request failed');
  return body;
}

export const endpoints = {
  meta: () => apiGet('/api/meta'),
  health: () => apiGet('/api/health'),
  gameInfo: () => apiGet('/api/game-info'),
  playerAuto: (uid) => apiGet(`/api/player/auto/${encodeURIComponent(uid)}`),
  stats: (region, uid, mode) => apiGet(`/api/player/${encodeURIComponent(region)}/${encodeURIComponent(uid)}/stats?mode=${encodeURIComponent(mode)}`),
  compare: (region, uid, otherUid) => apiGet(`/api/player/${encodeURIComponent(region)}/${encodeURIComponent(uid)}/compare/${encodeURIComponent(otherUid)}`),
  guild: (region, guildId) => apiGet(`/api/guild/${encodeURIComponent(region)}/${encodeURIComponent(guildId)}`),
};

export function apiBase() { return API; }
