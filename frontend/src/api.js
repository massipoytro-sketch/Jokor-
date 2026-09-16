const API = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '');

export async function apiGet(path) {
  const response = await fetch(`${API}${path}`, { headers: { Accept: 'application/json' } });
  let body = null;
  try { body = await response.json(); } catch { body = null; }
  if (!response.ok) throw new Error(body?.message || `API request failed (${response.status})`);
  if (body && body.success === false) throw new Error(body.message || body.error || 'Request failed');
  return body;
}

export const endpoints = {
  meta: () => apiGet('/api/meta'),
  health: () => apiGet('/api/health'),
  regions: () => apiGet('/api/regions'),
  gameInfo: () => apiGet('/api/game-info'),
  player: (region, uid) => apiGet(`/api/player/${encodeURIComponent(region)}/${encodeURIComponent(uid)}`),
  stats: (region, uid, mode) => apiGet(`/api/player/${encodeURIComponent(region)}/${encodeURIComponent(uid)}/stats?mode=${encodeURIComponent(mode)}`),
  compare: (region, uid, otherUid) => apiGet(`/api/player/${encodeURIComponent(region)}/${encodeURIComponent(uid)}/compare/${encodeURIComponent(otherUid)}`),
  search: (region, keyword) => apiGet(`/api/search/${encodeURIComponent(region)}/${encodeURIComponent(keyword)}`),
  guild: (region, guildId) => apiGet(`/api/guild/${encodeURIComponent(region)}/${encodeURIComponent(guildId)}`),
};

export function apiBase() { return API || 'same-origin'; }
