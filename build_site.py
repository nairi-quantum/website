# -*- coding: utf-8 -*-
"""Build the Nairi Quantum website (index.html) with the real logo embedded + orbiting animation."""
import base64, io
import numpy as np
from PIL import Image

LOGO_SRC = r"C:\Users\MichelKulhandjian\OneDrive - Digital Global Systems\Desktop\Michel\Quantum\Nairi_Quantum_logo_03.png"

# --- make the light background transparent so the logo blends + orbits show through ---
im = Image.open(LOGO_SRC).convert("RGBA")
arr = np.array(im).astype(int)
rgb = arr[..., :3]
mx = rgb.max(axis=2); mn = rgb.min(axis=2)
sat = mx - mn; light = mx
newa = np.full(light.shape, 255, dtype=int)
graybg = sat <= 16                                   # only near-gray/white pixels
newa[graybg & (light >= 240)] = 0                    # white bg -> transparent
feather = graybg & (light >= 222) & (light < 240)    # soft edge
newa[feather] = ((240 - light[feather]) / 18.0 * 255).astype(int)
arr[..., 3] = np.minimum(arr[..., 3], newa)          # keep all colored content
im = Image.fromarray(arr.astype("uint8"), "RGBA")

# --- embed an optimized copy of the (now transparent) logo as a data URI ---
w, h = im.size
tw = 760
im2 = im.resize((tw, int(h * tw / w)))
buf = io.BytesIO(); im2.save(buf, format="PNG", optimize=True)
logo_uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

HTML = r"""<title>Nairi Quantum</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="The first direct quantum-communication laboratory in Armenia and the region.">
<style>
  :root{
    --bg:#F8F9FC; --surface:#FFFFFF; --line:#E3E8F3; --ink:#14213F; --muted:#5A6588;
    --blue:#2050D0; --orange:#F08010; --red:#D01010; --navy:#0A1B4A;
    --sans:system-ui,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; --maxw:1080px;
  }
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}
  a{color:inherit;text-decoration:none}
  .wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}

  nav{position:sticky;top:0;z-index:20;background:rgba(248,249,252,.85);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
  .nav-in{display:flex;align-items:center;gap:20px;height:64px}
  .brand{font-weight:800;letter-spacing:.14em;font-size:15px;color:var(--navy)}
  .brand b{color:var(--blue)}
  .nav-links{margin-left:auto;display:flex;gap:26px;align-items:center}
  .nav-links a{font-size:13.5px;color:var(--muted);transition:color .2s}
  .nav-links a:hover{color:var(--blue)}
  .btn{display:inline-block;padding:11px 20px;border-radius:999px;font-size:13.5px;font-weight:700;letter-spacing:.02em;background:var(--red);color:#fff;border:0;cursor:pointer;transition:transform .2s,box-shadow .2s}
  .btn:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(208,16,16,.22)}
  .btn.ghost{background:transparent;color:var(--blue);border:1.5px solid var(--blue)}
  .btn.ghost:hover{background:rgba(32,80,208,.06);box-shadow:none}
  @media(max-width:720px){.nav-links a:not(.btn){display:none}}

  .hero{position:relative;min-height:94vh;display:flex;align-items:center;overflow:hidden;
    background:radial-gradient(900px 500px at 78% -8%,rgba(240,128,16,.12),transparent 60%),
               radial-gradient(900px 520px at 12% 108%,rgba(32,80,208,.10),transparent 60%),var(--bg)}
  #orb{position:absolute;inset:0;width:100%;height:100%;display:block}
  .hero-in{position:relative;z-index:2;padding:56px 0;text-align:center;width:100%}
  .hero img.logo{width:min(440px,80vw);height:auto;margin:0 auto 6px;display:block;filter:drop-shadow(0 8px 30px rgba(20,33,63,.10))}
  .hero h1{font-size:clamp(28px,4.6vw,46px);line-height:1.08;margin:14px auto 0;letter-spacing:-.02em;font-weight:800;max-width:18ch;text-wrap:balance}
  .hero h1 .g{color:var(--red)}
  .hero .lede{font-size:clamp(16px,2vw,20px);color:var(--muted);max-width:60ch;margin:16px auto 30px}
  .cta-row{display:flex;gap:14px;flex-wrap:wrap;justify-content:center}

  section.block{padding:clamp(60px,9vw,108px) 0;border-top:1px solid var(--line)}
  .kicker{font-size:12.5px;letter-spacing:.28em;text-transform:uppercase;color:var(--orange);font-weight:700;margin:0 0 14px}
  h2{font-size:clamp(26px,4vw,40px);line-height:1.1;margin:0 0 18px;letter-spacing:-.01em;font-weight:700;text-wrap:balance}
  .lead{font-size:clamp(15px,1.7vw,18px);color:var(--muted);max-width:64ch}

  .grid{display:grid;gap:20px;margin-top:40px}
  .cols-3{grid-template-columns:repeat(3,1fr)}
  @media(max-width:820px){.cols-3{grid-template-columns:1fr}}
  .card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:26px 24px;box-shadow:0 1px 3px rgba(20,33,63,.04);transition:transform .25s,border-color .25s,box-shadow .25s}
  .card:hover{transform:translateY(-4px);border-color:var(--blue);box-shadow:0 14px 34px rgba(20,33,63,.10)}
  .card h3{margin:0 0 8px;font-size:18px}
  .card p{margin:0;color:var(--muted);font-size:14.5px}
  .card .ic{font-size:22px;margin-bottom:12px;display:block}

  .road{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:40px}
  @media(max-width:820px){.road{grid-template-columns:1fr 1fr}}
  .stage{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:20px 18px}
  .stage .n{font-size:12px;color:var(--blue);font-weight:700;letter-spacing:.1em}
  .stage h4{margin:8px 0 4px;font-size:15.5px}
  .stage p{margin:0;color:var(--muted);font-size:13px}
  .stage:last-child{border-color:var(--orange)}
  .stage:last-child .n{color:var(--orange)}

  .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:36px}
  @media(max-width:720px){.stats{grid-template-columns:1fr 1fr}}
  .stat .num{font-size:clamp(30px,5vw,46px);font-weight:800;letter-spacing:-.02em;line-height:1;color:var(--blue)}
  .stat .num .g{color:var(--red)}
  .stat .lbl{color:var(--muted);font-size:13.5px;margin-top:8px}

  .support-wrap{background:linear-gradient(160deg,#fff,#EEF2FB);border:1px solid var(--line);border-radius:20px;padding:clamp(28px,5vw,52px);margin-top:8px;box-shadow:0 8px 30px rgba(20,33,63,.06)}
  .tiers{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px}
  @media(max-width:820px){.tiers{grid-template-columns:1fr}}
  .tier{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:22px;border-top:3px solid var(--orange)}
  .tier:nth-child(2){border-top-color:var(--blue)}
  .tier:nth-child(3){border-top-color:var(--red)}
  .tier h4{margin:0 0 6px;color:var(--ink)}
  .tier p{margin:0;color:var(--muted);font-size:14px}

  .partners{display:flex;gap:16px;flex-wrap:wrap;margin-top:28px}
  .partner{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 22px;color:var(--muted);font-size:14.5px}
  .partner b{color:var(--ink);font-weight:600}
  .contact-row{display:flex;gap:16px;flex-wrap:wrap;margin-top:28px;align-items:center}
  footer{border-top:1px solid var(--line);padding:34px 0;color:var(--muted);font-size:13px}
  .foot-in{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center}

  .quote-sec{background:linear-gradient(160deg,#fff,#EEF2FB)}
  .quote-sec blockquote{margin:0 auto;max-width:780px;text-align:center}
  .quote-sec .mark{font-size:56px;line-height:.6;color:var(--orange);font-weight:800}
  .quote-sec .q{font-size:clamp(22px,3.2vw,34px);line-height:1.3;font-weight:700;letter-spacing:-.01em;color:var(--navy);margin:6px 0 0}
  .quote-sec cite{display:block;margin-top:22px;font-style:normal;font-size:15px;color:var(--muted);letter-spacing:.04em}
  .plink{transition:transform .2s,border-color .2s,box-shadow .2s}
  .plink:hover{transform:translateY(-3px);border-color:var(--blue);box-shadow:0 12px 30px rgba(20,33,63,.10);color:var(--blue)}
  .reveal{opacity:0;transform:translateY(20px);transition:opacity .7s ease,transform .7s cubic-bezier(.2,.7,.2,1)}
  .reveal.in{opacity:1;transform:none}
  @media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}}
</style>

<nav><div class="wrap nav-in">
  <a class="brand" href="#top">NAIRI <b>QUANTUM</b></a>
  <div class="nav-links">
    <a href="#mission">Mission</a><a href="#roadmap">Roadmap</a><a href="#support">Support</a>
    <a class="btn" href="#contact">Get in touch</a>
  </div>
</div></nav>

<header class="hero" id="top">
  <canvas id="orb" aria-hidden="true"></canvas>
  <div class="wrap hero-in">
    <img class="logo" src="%%LOGO%%" alt="Nairi Quantum">
    <h1>The region's first <span class="g">quantum communication</span> laboratory.</h1>
    <p class="lede">We build Quantum Secure Direct Communication — and we train the next generation of
    Armenian scientists to build it, at home.</p>
    <div class="cta-row">
      <a class="btn" href="#support">Support a scientist</a>
      <a class="btn ghost" href="#mission">What we do</a>
    </div>
  </div>
</header>

<section class="block" id="mission"><div class="wrap">
  <p class="kicker reveal">Our mission</p>
  <h2 class="reveal">Securing tomorrow's communication — and keeping Armenian talent home.</h2>
  <p class="lead reveal">Quantum computers will one day break today's encryption, and adversaries already
  harvest encrypted data to decrypt later. Quantum Secure Direct Communication (QSDC) answers this by
  sending the message itself through a quantum channel, protected by the laws of physics. Nairi Quantum
  is the first laboratory in Armenia and the region to pursue it — founded by Dr.&nbsp;Michel Kulhandjian
  and giving a dozen young Armenian scientists a reason to build advanced careers in Yerevan rather than abroad.</p>
  <div class="grid cols-3">
    <div class="card reveal"><span class="ic">&#128272;</span><h3>Beyond key distribution</h3><p>QSDC transmits the message directly over the quantum channel — no key to steal, no ciphertext to harvest.</p></div>
    <div class="card reveal"><span class="ic">&#128225;</span><h3>From SDR to photons</h3><p>We start in software-defined radio, where our team is strongest, and advance toward true photonic quantum links.</p></div>
    <div class="card reveal"><span class="ic">&#127462;&#127474;</span><h3>Talent, kept home</h3><p>A dozen young Armenians, trained at the frontier of quantum technology — the reverse of brain drain.</p></div>
  </div>
</div></section>

<section class="block" id="roadmap"><div class="wrap">
  <p class="kicker reveal">The roadmap</p>
  <h2 class="reveal">Classical to quantum, one stage at a time.</h2>
  <p class="lead reveal">Each stage produces real, publishable results — building toward the region's first photonic quantum-secure link.</p>
  <div class="road">
    <div class="stage reveal"><div class="n">01</div><h4>Classical</h4><p>Communications theory &amp; coding.</p></div>
    <div class="stage reveal"><div class="n">02</div><h4>SDR</h4><p>GNU Radio &amp; USRP; physical-layer security.</p></div>
    <div class="stage reveal"><div class="n">03</div><h4>Quantum-inspired</h4><p>Emulated QSDC on software-defined radio.</p></div>
    <div class="stage reveal"><div class="n">04</div><h4>Photonic QSDC</h4><p>Single-photon hardware, with partner labs.</p></div>
  </div>
</div></section>

<section class="block"><div class="wrap"><div class="stats">
  <div class="stat reveal"><div class="num">12</div><div class="lbl">young researchers</div></div>
  <div class="stat reveal"><div class="num">3</div><div class="lbl">research tracks</div></div>
  <div class="stat reveal"><div class="num"><span class="g">1</span>st</div><div class="lbl">QSDC lab in the region</div></div>
  <div class="stat reveal"><div class="num">&#8734;</div><div class="lbl">ambition for Armenia</div></div>
</div></div></section>

<section class="block quote-sec"><div class="wrap"><blockquote class="reveal">
  <div class="mark">&#8220;</div>
  <p class="q">Armenia does not need to wait for the quantum age to be handed to it. We are building it here &mdash;
  training our own scientists, on our own soil, to secure the communication of the future.</p>
  <cite>Dr. Michel Kulhandjian &middot; Founder</cite>
</blockquote></div></section>

<section class="block" id="support"><div class="wrap">
  <p class="kicker reveal">Become a patron</p>
  <h2 class="reveal">Sponsor a scientist. Keep a mind in Armenia.</h2>
  <div class="support-wrap reveal">
    <p class="lead">Our researchers are talented and committed. What they need to stay fully dedicated is
    modest — support for their transportation and a small stipend. We invite patrons to sponsor one member
    of the team, and we recognize that support with pride.</p>
    <div class="tiers">
      <div class="tier"><h4>Patron</h4><p>Sponsor one scientist for a year. Recognized on this site, in our research acknowledgments, and at our events.</p></div>
      <div class="tier"><h4>Named Fellow</h4><p>Your name carried by the position — "The [Your Name] Fellow" — for the duration of your support.</p></div>
      <div class="tier"><h4>Founding Supporter</h4><p>An early champion of the region's first quantum lab, with a standing invitation to visit and follow our progress.</p></div>
    </div>
    <div class="cta-row" style="margin-top:28px;justify-content:flex-start"><a class="btn" href="#contact">Talk to us about sponsoring</a></div>
  </div>
</div></section>

<section class="block"><div class="wrap">
  <p class="kicker reveal">Supported by</p>
  <h2 class="reveal">Built with generous partners.</h2>
  <div class="partners reveal">
    <div class="partner"><b>Engineering City</b> &middot; laboratory space, Yerevan</div>
    <div class="partner"><b>NI&nbsp;Armenia</b> &middot; software-defined radios &amp; support</div>
  </div>
</div></section>

<section class="block"><div class="wrap">
  <p class="kicker reveal">Press</p>
  <h2 class="reveal">As featured in.</h2>
  <p class="lead reveal">Our launch and mission were profiled in the Engineering City journal.</p>
  <div class="partners reveal">
    <a class="partner plink" href="EC_journal.pdf" target="_blank" rel="noopener"><b>Engineering City Journal</b> &middot; read the article (PDF) &rarr;</a>
  </div>
</div></section>

<section class="block" id="contact"><div class="wrap">
  <p class="kicker reveal">Get in touch</p>
  <h2 class="reveal">Support the lab, collaborate, or just say hello.</h2>
  <p class="lead reveal">Whether you'd like to sponsor a young scientist, explore a collaboration, or learn
  more about our work, we'd be glad to hear from you.</p>
  <div class="contact-row reveal">
    <a class="btn" href="mailto:info@nairiquantum.org">info@nairiquantum.org</a>
    <span class="partner">Engineering City &middot; Yerevan, Armenia</span>
  </div>
</div></section>

<footer><div class="wrap foot-in">
  <div class="brand">NAIRI <b style="color:var(--blue)">QUANTUM</b></div>
  <div>&copy; 2026 Nairi Quantum &middot; Engineering City, Yerevan</div>
</div></footer>

<script>
  const io=new IntersectionObserver((es)=>{for(const e of es){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}}},{threshold:.14});
  document.querySelectorAll('.reveal').forEach((el,i)=>{el.style.transitionDelay=(Math.min(i%3,2)*70)+'ms';io.observe(el);});

  // orbiting photons behind the hero (echoes the logo's orbits)
  const c=document.getElementById('orb'), ctx=c.getContext('2d');
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const orbits=[
    {rx:.60,ry:.22,rot:-0.35,sp:0.30,ph:0.0,col:'32,80,208'},   // blue
    {rx:.44,ry:.40,rot:0.62,sp:-0.26,ph:2.0,col:'240,128,16'},  // orange
    {rx:.64,ry:.30,rot:0.14,sp:0.24,ph:4.1,col:'208,16,16'},    // red
    {rx:.52,ry:.52,rot:0.90,sp:-0.20,ph:1.0,col:'32,80,208'},   // blue (wide ring)
  ];
  let W,H,dpr,cx,cy,base;
  function size(){dpr=Math.min(devicePixelRatio||1,2);W=c.width=c.offsetWidth*dpr;H=c.height=c.offsetHeight*dpr;cx=W*0.5;cy=H*0.44;base=Math.min(W,H)*1.02;}
  function draw(t){
    ctx.clearRect(0,0,W,H);
    for(const o of orbits){
      const rx=o.rx*base, ry=o.ry*base, R=o.rot;
      // faint orbit path
      ctx.save();ctx.translate(cx,cy);ctx.rotate(R);
      ctx.strokeStyle='rgba('+o.col+',0.14)';ctx.lineWidth=1*dpr;
      ctx.beginPath();ctx.ellipse(0,0,rx,ry,0,0,Math.PI*2);ctx.stroke();ctx.restore();
      // orbiting photon
      const a=t*o.sp+o.ph, x=rx*Math.cos(a), y=ry*Math.sin(a);
      const X=cx+x*Math.cos(R)-y*Math.sin(R), Y=cy+x*Math.sin(R)+y*Math.cos(R);
      const g=ctx.createRadialGradient(X,Y,0,X,Y,7*dpr);
      g.addColorStop(0,'rgba('+o.col+',0.95)');g.addColorStop(1,'rgba('+o.col+',0)');
      ctx.fillStyle=g;ctx.beginPath();ctx.arc(X,Y,7*dpr,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='rgba('+o.col+',1)';ctx.beginPath();ctx.arc(X,Y,2.4*dpr,0,Math.PI*2);ctx.fill();
    }
  }
  let raf;
  function loop(){draw(performance.now()/1000);raf=requestAnimationFrame(loop);}
  size();
  if(reduce){draw(0);}
  else{loop();
    addEventListener('resize',()=>{size();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(raf);}else{loop();}});
  }
</script>
"""

HTML = HTML.replace("%%LOGO%%", logo_uri)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print("Saved index.html  (logo embedded:", round(len(logo_uri)/1024), "KB base64 )")
