import React, { useState } from 'react';
import { Activity, BarChart3, ChevronRight, Crown, Crosshair, Database, Gauge, Search, Shield, Swords, Users, Zap } from 'lucide-react';
import { createRoot } from 'react-dom/client';
import { endpoints, apiBase } from './api';
import './style.css';

function App() {
  const [view, setView] = useState('scan');
  const [uid, setUid] = useState('');
  const [otherUid, setOtherUid] = useState('');
  const [guildId, setGuildId] = useState('');
  const [player, setPlayer] = useState(null);
  const [stats, setStats] = useState({ br: null });
  const [compare, setCompare] = useState(null);
  const [guild, setGuild] = useState(null);
  const [system, setSystem] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('idle');
  const [error, setError] = useState('');

  const validUid = value => /^\d{5,15}$/.test(value.trim());
  const clear = () => setError('');

  async function scan(e) {
    e?.preventDefault();
    const target = uid.trim();
    if (!validUid(target)) { setError('أدخل UID صحيحًا من 5 إلى 15 رقمًا.'); return; }
    setLoading(true); setError(''); setStatus('detecting'); setPlayer(null); setStats({ br: null });
    try {
      const profile = await endpoints.playerAuto(target);
      setPlayer(profile.data);
      setStatus('loading');
      try {
        const br = await endpoints.stats(profile.metadata.region, target, 'br');
        setStats({ br: br.data });
      } catch { setStats({ br: null }); }
      setStatus('ready');
    } catch (x) {
      setPlayer(null); setStats({ br: null }); setStatus('error');
      setError(x.message || 'تعذر جلب بيانات اللاعب.');
    } finally { setLoading(false); }
  }

  async function doCompare(e) {
    e?.preventDefault();
    if (!validUid(uid) || !validUid(otherUid)) { setError('أدخل UIDين صحيحين للمقارنة.'); return; }
    setLoading(true); setError(''); setCompare(null);
    try {
      const [a, b] = await Promise.all([endpoints.playerAuto(uid.trim()), endpoints.playerAuto(otherUid.trim())]);
      if (a.metadata.region !== b.metadata.region) throw new Error('اللاعبان على منطقتين مختلفتين؛ المقارنة تحتاج مصدرًا مشتركًا لنفس المنطقة.');
      setCompare(await endpoints.compare(a.metadata.region, uid.trim(), otherUid.trim()));
      setView('compare');
    } catch (x) { setError(x.message || 'تعذر إنشاء المقارنة.'); }
    finally { setLoading(false); }
  }

  async function doGuild(e) {
    e?.preventDefault();
    const id = guildId.trim() || String(player?.guild_id || '');
    if (!/^\d+$/.test(id)) { setError('أدخل Guild ID رقميًا.'); return; }
    if (!player?.region) { setError('افحص لاعبًا أولًا حتى يحدد Jokor المنطقة تلقائيًا.'); return; }
    setLoading(true); setError(''); setGuild(null);
    try { const result = await endpoints.guild(player.region, id); setGuild(result.data ?? result); }
    catch (x) { setError(x.message || 'تعذر جلب بيانات النقابة.'); }
    finally { setLoading(false); }
  }

  async function loadSystem() {
    setView('system'); setError(''); setSystem(null);
    const [health, meta] = await Promise.allSettled([endpoints.health(), endpoints.meta()]);
    setSystem({ health: health.status === 'fulfilled' ? health.value : null, meta: meta.status === 'fulfilled' ? meta.value : null });
  }

  const br = stats.br;
  const metrics = [
    ['LEVEL', player?.level, Gauge], ['LIKES', player?.likes, Users], ['BR RANK', br?.rank ?? player?.rank, Crown],
    ['BR POINTS', br?.ranking_points ?? player?.rank_points, Zap],
    ['BR K/D', br?.derived?.kd_ratio ?? br?.kd, Swords],
    ['BR WIN RATE', br?.derived?.win_rate_pct != null ? `${br.derived.win_rate_pct}%` : (br?.win_rate != null ? `${br.win_rate}%` : '—'), BarChart3],
    ['CS RANK', player?.cs_rank, Crown], ['CS POINTS', player?.cs_rank_points, Crosshair]
  ];

  return <div className="app">
    <div className="grid-bg" />
    <header className="topbar"><button className="brand" onClick={() => { setView('scan'); clear(); }}><span className="brand-mark">J</span><span><b>JOKOR</b><small>PLAYER INTELLIGENCE</small></span></button><nav>{[['scan','SCAN'],['compare','COMPARE'],['guild','GUILD']].map(([id,label]) => <button key={id} className={view===id?'active':''} onClick={() => { setView(id); clear(); }}>{label}</button>)}</nav><button className="system-link" onClick={loadSystem}><span className="pulse"/> SYSTEM</button></header>
    <main>
      <section className="hero"><div className="hero-copy"><div className="eyebrow"><Zap size={14}/> AUTOMATIC PLAYER INTELLIGENCE</div><h1>ENTER UID.<br/><em>WE DO THE REST.</em></h1><p>اكتب UID فقط. Jokor يكتشف المنطقة تلقائيًا ويعرض البيانات التي يوفرها المصدر الحقيقي، بدون اختيار سيرفر وبدون أرقام وهمية.</p><form className="uid-search" onSubmit={scan}><div className="uid-input"><Search size={19}/><input value={uid} onChange={e=>setUid(e.target.value.replace(/\D/g,''))} inputMode="numeric" autoComplete="off" placeholder="PLAYER UID"/></div><button disabled={loading}>{loading?<Activity className="spin"/>:<Crosshair/>}<span>{status==='detecting'?'DETECTING…':status==='loading'?'LOADING…':'SCAN PLAYER'}</span></button></form><div className="trust"><span>●</span> NO PASSWORDS <span>●</span> REAL PUBLIC DATA <span>●</span> AUTO REGION</div></div><div className="hero-visual" aria-hidden="true"><div className="halo h1"/><div className="halo h2"/><div className="halo h3"/><div className="core">J</div><div className="crosshair"/></div></section>
      {error && <div className="error"><Shield size={18}/><span>{error}</span></div>}
      {view==='scan' && <section className="result-area">{player ? <><div className="player-head"><div className="avatar">{String(player.nickname || 'J')[0]}</div><div className="identity"><span className="label">PLAYER DETECTED · {player.region}</span><h2>{player.nickname || 'Unknown player'}</h2><p>UID {player.uid || uid}</p></div><div className="source"><span>DATA SOURCE</span><b>LIVE</b></div></div><div className="stats-grid">{metrics.map(([label,value,Icon])=><div className="metric" key={label}><Icon/><span>{label}</span><strong>{value ?? '—'}</strong></div>)}</div><div className="detail-row"><div><span className="section-kicker">PROFILE</span><div className="profile-line"><b>LEVEL</b><span>{player.level ?? '—'}</span><b>LIKES</b><span>{player.likes ?? '—'}</span><b>GUILD</b><span>{player.guild_name || player.guild_id || '—'}</span></div></div><div className="availability"><span className="live-dot"/> {br ? 'DATA AVAILABLE' : 'PROFILE ONLY'}</div></div></> : <div className="empty-state"><div className="empty-icon"><Crosshair/></div><h2>READY TO SCAN</h2><p>أدخل UID في الأعلى. لا تحتاج إلى معرفة السيرفر أو اختيار المنطقة.</p></div>}</section>}
      {view==='compare' && <section className="panel"><div className="section-kicker">INTELLIGENCE TOOL</div><h2>COMPARE PLAYERS</h2><form className="tool-form" onSubmit={doCompare}><input value={uid} onChange={e=>setUid(e.target.value.replace(/\D/g,''))} inputMode="numeric" placeholder="FIRST UID"/><div className="vs">VS</div><input value={otherUid} onChange={e=>setOtherUid(e.target.value.replace(/\D/g,''))} inputMode="numeric" placeholder="SECOND UID"/><button disabled={loading}>{loading?'…':'COMPARE'}</button></form>{compare?<CompareResult result={compare}/>:<Empty text="أدخل UIDين ثم ابدأ المقارنة."/>}</section>}
      {view==='guild' && <section className="panel"><div className="section-kicker">INTELLIGENCE TOOL</div><h2>GUILD LOOKUP</h2><p className="hint">المنطقة تُؤخذ تلقائيًا من آخر لاعب تم فحصه: <b>{player?.region || '—'}</b></p><form className="tool-form" onSubmit={doGuild}><input value={guildId} onChange={e=>setGuildId(e.target.value.replace(/\D/g,''))} inputMode="numeric" placeholder={player?.guild_id ? `AUTO · ${player.guild_id}` : 'GUILD ID'}/><button disabled={loading}>{loading?'…':'SCAN GUILD'}</button></form>{guild?<GuildResult data={guild}/>:<Empty text="أدخل Guild ID أو استخدم Guild ID الموجود في ملف اللاعب."/>}</section>}
      {view==='system' && <section className="panel"><div className="section-kicker">JOKOR TELEMETRY</div><h2>SYSTEM STATUS</h2><div className="system-cards"><Info icon={<Activity/>} label="API" value={system?.health?.status || (system ? 'UNAVAILABLE' : 'CHECKING')}/><Info icon={<Database/>} label="SOURCE" value={system?.meta?.features ? 'CONNECTED' : (system ? 'UNAVAILABLE' : 'CHECKING')}/><Info icon={<Shield/>} label="CREDENTIALS" value="NONE"/></div>{system&&<pre className="json">{JSON.stringify(system,null,2)}</pre>}</section>}
      <section className="features"><div className="section-kicker">BUILT FOR SPEED</div><div className="feature-grid"><Feature icon={<Crosshair/>} title="UID FIRST" text="واجهة واحدة وبسيطة: UID فقط، والباقي يتكفل به Jokor."/><Feature icon={<Globe2Fallback/>} title="AUTO REGION" text="يختبر المناطق المدعومة ويتأكد من UID قبل قبول النتيجة."/><Feature icon={<BarChart3/>} title="REAL DATA" text="لا نكرر بيانات BR على CS. البيانات غير المتاحة تظهر بوضوح."/><Feature icon={<Shield/>} title="SAFE BY DESIGN" text="لا كلمات مرور ولا access tokens ولا أدوات لتعديل الحساب."/></div></section>
    </main>
    <nav className="bottom-nav" aria-label="التنقل الرئيسي"><button className={view==='scan'?'active':''} onClick={()=>{setView('scan');clear();}}><Crosshair/><span>Scan</span></button><button className={view==='compare'?'active':''} onClick={()=>{setView('compare');clear();}}><Swords/><span>Compare</span></button><button className={view==='guild'?'active':''} onClick={()=>{setView('guild');clear();}}><Users/><span>Guild</span></button><button className={view==='system'?'active':''} onClick={loadSystem}><Activity/><span>System</span></button></nav>
    <footer><b>JOKOR</b><span>PLAYER INTELLIGENCE · {new Date().getFullYear()}</span><code>{apiBase()}</code></footer>
  </div>;
}
function CompareResult({result}) { const br=result?.comparison?.br||{}; const rows=['matches','wins','kills','deaths','headshots','ranking_points','win_rate']; const labels={matches:'MATCHES',wins:'WINS',kills:'KILLS',deaths:'DEATHS',headshots:'HEADSHOTS',ranking_points:'RANK POINTS',win_rate:'WIN RATE'}; return <div className="compare-result"><div className="compare-note"><span className="live-dot"/> LIVE BR COMPARISON · CS STATS NOT PROVIDED BY SOURCE</div>{rows.map(key=>{const m=br[key]||{};return <div className="compare-row" key={key}><span>{labels[key]}</span><b>{fmt(m.a)}</b><i>{fmt(m.b)}</i><em>{m.delta_a_minus_b==null?'—':fmt(m.delta_a_minus_b)}</em></div>})}</div>; }
function GuildResult({data}) { return <div className="guild-card"><div><span>GUILD</span><h3>{data?.clanName||'Unknown guild'}</h3></div><div className="guild-grid"><InfoMini label="LEVEL" value={data?.clanLevel}/><InfoMini label="MEMBERS" value={data?.memberNum}/><InfoMini label="CAPACITY" value={data?.capacity}/><InfoMini label="REGION" value={data?.region}/><InfoMini label="CAPTAIN" value={data?.captainId}/><InfoMini label="ID" value={data?.clanId}/></div></div>; }
function InfoMini({label,value}) { return <div><span>{label}</span><b>{value??'—'}</b></div>; }
function fmt(value) { return value==null?'—':Number.isInteger(value)?value:Number(value).toFixed(2); }
function Empty({text}) { return <div className="empty-state small"><Database/><p>{text}</p></div>; }
function Info({icon,label,value}) { return <div className="info">{icon}<span>{label}</span><b>{value}</b></div>; }
function Feature({icon,title,text}) { return <article className="feature"><div>{icon}</div><h3>{title}</h3><p>{text}</p><ChevronRight/></article>; }
function Globe2Fallback(){ return <span className="globe-mark">◎</span>; }
createRoot(document.getElementById('root')).render(<App/>);
