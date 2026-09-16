import React, {useState} from 'react';
import {createRoot} from 'react-dom/client';
import {Search, Zap, Shield, BarChart3, Users, Swords, Activity, Crown} from 'lucide-react';
import './style.css';

const API = import.meta.env.VITE_API_URL || '';

function App(){
  const [uid,setUid]=useState(''); const [region,setRegion]=useState('ME'); const [player,setPlayer]=useState(null); const [loading,setLoading]=useState(false); const [error,setError]=useState('');
  async function lookup(e){e.preventDefault(); if(!/^\d+$/.test(uid)){setError('أدخل UID رقمي صحيح');return} setLoading(true);setError('');setPlayer(null); try{const r=await fetch(`${API}/api/player/${region}/${uid}`); const d=await r.json(); if(!d.success) throw new Error(d.message||'لم يتم العثور على البيانات'); setPlayer(d.data)}catch(x){setError(x.message)}finally{setLoading(false)}}
  return <div className="app">
    <div className="noise"/><header><div className="brand"><div className="logo">J</div><div><b>JOKOR</b><span>FREE FIRE INTELLIGENCE</span></div></div><nav><a href="#search">PLAYER</a><a href="#features">TOOLS</a><a href="#about">SYSTEM</a></nav><div className="status"><i/> SYSTEM ONLINE</div></header>
    <main>
      <section className="hero" id="search"><div className="hero-copy"><div className="eyebrow"><Zap size={15}/> NEXT-GEN PLAYER INTELLIGENCE</div><h1>KNOW THE<br/><em>PLAYER.</em></h1><p>ابحث عن لاعب Free Fire وحوّل الـUID إلى ملف مليء بالإحصائيات والتحليل.</p>
      <form onSubmit={lookup} className="search"><select value={region} onChange={e=>setRegion(e.target.value)}><option>ME</option><option>IND</option><option>BR</option><option>SG</option><option>EU</option><option>US</option></select><input value={uid} onChange={e=>setUid(e.target.value)} placeholder="ENTER PLAYER UID"/><button>{loading?<Activity className="spin"/>:<Search/>}<span>SCAN PLAYER</span></button></form>{error&&<div className="error">{error}</div>}
      </div><div className="orb"><div className="ring r1"/><div className="ring r2"/><div className="core">J</div><div className="scanline"/></div></section>
      {player&&<section className="result"><div className="section-label">PLAYER DETECTED</div><div className="profile"><div className="avatar">{String(player.nickname||'J')[0]}</div><div><h2>{player.nickname||'Unknown Player'}</h2><small>UID {player.uid||uid} · {player.region||region}</small></div><div className="rank"><Crown size={17}/> {player.rank||'UNRANKED'}</div></div><div className="stats"><Stat icon={<Swords/>} name="LEVEL" value={player.level??'—'}/><Stat icon={<Users/>} name="LIKES" value={player.likes??'—'}/><Stat icon={<BarChart3/>} name="K/D" value={player.kd_ratio??'—'}/><Stat icon={<Activity/>} name="WIN RATE" value={player.win_rate_pct!=null?`${player.win_rate_pct}%`:'—'}/></div></section>}
      <section className="features" id="features"><div className="section-label">JOKOR CORE</div><h2>BUILT TO <span>HUNT DATA.</span></h2><div className="grid"><Card icon={<Search/>} title="PLAYER SCAN" text="ملف لاعب منظم مع هوية، مستوى، رتبة، إعجابات وبيانات الأداء المتاحة."/><Card icon={<BarChart3/>} title="DEEP STATS" text="Win Rate و K/D و Headshot Rate ومؤشرات مشتقة قابلة للتحليل."/><Card icon={<Swords/>} title="BR / CS" text="افصل أداء Battle Royale عن Clash Squad عندما يقدمه مصدر البيانات."/><Card icon={<Shield/>} title="SMART FALLBACK" text="طبقة مزودين مع cache وhealth checks للحفاظ على استقرار النظام."/></div></section>
      <section className="terminal" id="about"><div><span className="dot"/> JOKOR API</div><code>PLAYER_INTELLIGENCE // READY<br/><b>STATUS:</b> AWAITING TARGET<br/><b>ENGINE:</b> PROVIDER HUB + ANALYTICS</code></section>
    </main><footer><b>JOKOR</b><span>PLAYER INTELLIGENCE SYSTEM · 2026</span></footer>
  </div>
}
function Stat({icon,name,value}){return <div className="stat">{icon}<small>{name}</small><strong>{value}</strong></div>}
function Card({icon,title,text}){return <article><div className="card-icon">{icon}</div><h3>{title}</h3><p>{text}</p><span className="arrow">↗</span></article>}

createRoot(document.getElementById('root')).render(<App/>);
