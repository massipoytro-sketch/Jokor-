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
  const [stats, setStats] = useState({ br: null, cs: null });
  const [compare, setCompare] = useState(null);
  const [guild, setGuild] = useState(null);
  const [system, setSystem] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('idle');
  const [error, setError] = useState('');

  const validUid = value => /^\d{5,15}$/.test(value.trim());
  const clear = () => { setError(''); setStatus('idle'); };

  async function scan(e) {
    e?.preventDefault();
    const target = uid.trim();
    if (!validUid(target)) { setError('أدخل UID صحيحًا من 5 إلى 15 رقمًا.'); return; }
    setLoading(true); setError(''); setStatus('detecting'); setPlayer(null); setStats({ br: null, cs: null });
    try {
      const profile = await endpoints.playerAuto(target);
      setPlayer(profile.data);
      setStatus('loading');
      const region = profile.metadata.region;
      const [br, cs] = await Promise.allSettled([
        endpoints.stats(region, target, 'br'),
        endpoints.stats(region, target, 'cs')
      ]);
      setStats({ br: br.status === 'fulfilled' ? br.value.data : null, cs: cs.status === 'fulfilled' ? cs.value.data : null });
      setStatus('ready');
      if (!br.value && !cs.value) setError('تم العثور على اللاعب، لكن الإحصائيات غير متاحة حاليًا.');
    } catch (x) {
      setPlayer(null); setStats({ br: null, cs: null }); setStatus('error');
      setError(x.message || 'تعذر جلب بيانات اللاعب.');
    } finally { setLoading(false); }
  }

  async function doCompare(e) {
    e?.preventDefault();
    if (!validUid(uid) || !validUid(otherUid)) { setError('أدخل UIDين صحيحين للمقارنة.'); return; }
    setLoading(true); setError('');
    try {
      const [a, b] = await Promise.all([endpoints.playerAuto(uid.trim()), endpoints.playerAuto(otherUid.trim())]);
      if (a.metadata.region !== b.metadata.region) throw new Error('اللاعبان على منطقتين مختلفتين؛ المقارنة المباشرة غير متاحة من هذا المصدر.');
      const result = await endpoints.compare(a.metadata.region, uid.trim(), otherUid.trim());
      setCompare(result.data ?? result); setView('compare');
    } catch (x) { setCompare(null); setError(x.message || 'تعذر إنشاء المقارنة.'); }
    finally { setLoading(false); }
  }

  async function doGuild(e) {
    e?.preventDefault();
    if (!/^[0-9]+$/.test(guildId.trim())) { setError('أدخل Guild ID رقميًا.'); return; }
    setLoading(true); setError(''); setGuild(null);
    try {
      if (!player?.region) throw new Error('افحص لاعبًا أولًا حتى يحدد Jokor المنطقة تلقائيًا.');
      const result = await endpoints.guild(player.region, guildId.trim());
      setGuild(result.data ?? result);
    } catch (x) { setError(x.message || 'تعذر جلب بيانات النقابة.'); }
    finally { setLoading(false); }
  }

  async function loadSystem() {
    setView('system'); setError(''); setSystem(null);
    const [health, meta] = await Promise.allSettled([endpoints.health(), endpoints.meta()]);
    setSystem({ health: health.status === 'fulfilled' ? health.value : null, meta: meta.status === 'fulfilled' ? meta.value : null });
  }

  const br = stats.br;
  const cs = stats.cs;
  const metrics = [
    ['LEVEL', player?.level], ['LIKES', player?.likes], ['BR RANK', br?.rank ?? player?.rank], ['BR POINTS', br?.ranking_points ?? br?.rankingPoints ?? player?.rank_points],
    ['BR K/D', br?.derived?.kd_ratio ?? br?.kd], ['BR WIN RATE', br?.derived?.win_rate_pct != null ? `${br.derived.win_rate_pct}%` : null],
    ['CS RANK', cs?.rank ?? cs?.cs_rank], ['CS K/D', cs?.derived?.kd_ratio ?? cs?.kd]
  ];

  return <div className="app">
    <div className="grid-bg" />
    <header className="topbar">
      <button className="brand" onClick={() => { setView('scan'); clear(); }}><span className="brand-mark">J</span><span><b>JOKOR</b><small>PLAYER INTELLIGENCE</small></span></button>
      <nav>{[['scan','SCAN'],['compare','COMPARE'],['guild','GUILD']].map(([id,label]) => <button key={id} className={view===id?'active':''} onClick={() => { setView(id); clear(); }}>{label}</button>)}</nav>
      <button className="system-link" onClick={loadSystem}><span className="pulse"/> SYSTEM</button>
    </header>

    <main>
      <section className="hero">
        <div className="hero-copy">
          <div className="eyebrow"><Zap size={14}/> AUTOMATIC PLAYER INTELLIGENCE</div>
          <h1>ENTER UID.<br/><em>WE DO THE REST.</em></h1>
          <p>اكتب UID فقط. Jokor يكتشف المنطقة تلقائيًا ويجمع المعلومات المتاحة من مصدر البيانات، بدون اختيار سيرفر وبدون بيانات وهمية.</p>
          <form className="uid-search" onSubmit={scan}>
            <div className="uid-input"><Search size={19}/><input value={uid} onChange={e=>setUid(e.target.value.replace(/\D/g,''))} inputMode="numeric" autoComplete="off" placeholder="PLAYER UID"/></div>
            <button disabled={loading}>{loading ? <Activity className="spin"/> : <Crosshair/>}<span>{status==='detecting'?'DETECTING…':'SCAN PLAYER'}</span></button>
          </form>
          <div className="trust"><span>●</span> NO PASSWORDS <span>●</span> PUBLIC DATA ONLY <span>●</span> LIVE SOURCE</div>
        </div>
        <div className="hero-visual" aria-hidden="true"><div className="halo h1"/><div className="halo h2"/><div className="halo h3"/><div className="core">J</div><div className="crosshair"><i/><i/></div></div>
      </section>

      {error && <div className="error"><Shield size={18}/><span>{error}</span></div>}

      {view==='scan' && <section className="result-area">
        {player ? <>
          <div className="player-head"><div className="avatar">{String(player.nickname || 'J')[0]}</div><div className="identity"><span className="label">PLAYER DETECTED · {player.region}</span><h2>{player.nickname || 'Unknown player'}</h2><p>UID {player.uid || uid}</p></div><div className="source"><span>DATA SOURCE</span><b>LIVE</b></div></div>
          <div className="stats-grid">{metrics.map(([label,value],i)=><div className="metric" key={label}>{[<Gauge/>,<Users/>,<Crown/>,<Zap/>,<Swords/>,<BarChart3/>,<Crown/>,<Crosshair/>][i]}<span>{label}</span><strong>{value ?? '—'}</strong></div>)}</div>
          <div className="detail-row"><div><span className="section-kicker">PROFILE</span><div className="profile-line"><b>LEVEL</b><span>{player.level ?? '—'}</span><b>LIKES</b><span>{player.likes ?? '—'}</span><b>GUILD</b><span>{player.guild_name || player.guild_id || '—'}</span></div></div><div className="availability"><span className="live-dot"/> DATA AVAILABLE</div></div>
        </> : <div className="empty-state"><div className="empty-icon"><Crosshair/></div><h2>READY TO SCAN</h2><p>أدخل UID في الأعلى. لا تحتاج إلى معرفة السيرفر أو نوع البيانات.</p></div>}
      </section>}

      {view==='compare' && <section className="panel"><div className="section-kicker">INTELLIGENCE TOOL</div><h2>COMPARE PLAYERS</h2><form className="tool-form" onSubmit={doCompare}><input value={uid} onChange={e=>setUid(e.target.value.replace(/\D/g,''))} inputMode="numeric" placeholder="FIRST UID"/><div className="vs">VS</div><input value={otherUid} onChange={e=>setOtherUid(e.target.value.replace(/\D/g,''))} inputMode="numeric" placeholder="SECOND UID"/><button disabled={loading}>{loading?'…':'COMPARE'}</button></form>{compare?<pre className="json">{JSON.stringify(compare,null,2)}</pre>:<Empty text="أدخل UIDين ثم ابدأ المقارنة."/>}</section>}

      {view==='guild' && <section className="panel"><div className="section-kicker">INTELLIGENCE TOOL</div><h2>GUILD LOOKUP</h2><p className="hint">يستخدم Jokor المنطقة التي اكتشفها من آخر لاعب تم فحصه.</p><form className="tool-form" onSubmit={doGuild}><input value={guildId} onChange={e=>setGuildId(e.target.value.replace(/\D/g,''))} inputMode="numeric" placeholder="GUILD ID"/><button disabled={loading}>{loading?'…':'SCAN GUILD'}</button></form>{guild?<pre className="json">{JSON.stringify(guild,null,2)}</pre>:<Empty text="لا توجد بيانات Guild محملة."/>}</section>}

      {view==='system' && <section className="panel"><div className="section-kicker">JOKOR TELEMETRY</div><h2>SYSTEM STATUS</h2><div className="system-cards"><Info icon={<Activity/>} label="API" value={system?.health?'ONLINE':'CHECKING'}/><Info icon={<Database/>} label="SOURCE" value="PUBLIC"/><Info icon={<Shield/>} label="SAFETY" value="NO CREDENTIALS"/></div>{system&&<pre className="json">{JSON.stringify(system,null,2)}</pre>}</section>}

      <section className="features"><div className="section-kicker">BUILT FOR SPEED</div><div className="feature-grid"><Feature icon={<Crosshair/>} title="UID FIRST" text="واجهة واحدة وبسيطة: UID فقط، والباقي يتكفل به Jokor."/><Feature icon={<Globe2Fallback/>} title="AUTO REGION" text="اكتشاف المنطقة من مصدر البيانات بدل إجبار المستخدم على اختيارها."/><Feature icon={<BarChart3/>} title="REAL DATA" text="لا نعرض أرقامًا تجريبية. عند غياب المصدر نخبرك بوضوح."/><Feature icon={<Shield/>} title="SAFE BY DESIGN" text="لا كلمات مرور، لا access tokens، ولا أدوات لتعديل الحساب."/></div></section>
    </main>
    <footer><b>JOKOR</b><span>PLAYER INTELLIGENCE · {new Date().getFullYear()}</span><code>{apiBase()}</code></footer>
  </div>;
}

function Empty({text}) { return <div className="empty-state small"><Database/><p>{text}</p></div>; }
function Info({icon,label,value}) { return <div className="info">{icon}<span>{label}</span><b>{value}</b></div>; }
function Feature({icon,title,text}) { return <article className="feature"><div>{icon}</div><h3>{title}</h3><p>{text}</p><ChevronRight/></article>; }
function Globe2Fallback(){ return <span className="globe-mark">◎</span>; }

createRoot(document.getElementById('root')).render(<App/>);
