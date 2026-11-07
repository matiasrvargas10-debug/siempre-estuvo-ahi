from rlib import head, TAIL, sc, render, BASE
BG, AC, TX = '#F3EBDD', '#B5452F', '#2A1E17'
PATH = 'M70,470 C 300,380 520,230 790,60'
css = f'''
.map{{position:absolute;left:110px;top:660px;width:860px;height:520px}}
.trk{{fill:none;stroke:{TX};stroke-width:7;stroke-dasharray:1200;stroke-dashoffset:1200;animation:draw 3.6s linear 1.9s forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.train{{position:absolute;left:0;top:0;width:46px;height:46px;border-radius:50%;background:{AC};
 offset-path:path('{PATH}');offset-distance:0%;offset-rotate:0deg;opacity:0;
 animation:ride 3.6s linear 1.9s forwards, show .1s 1.9s forwards}}
@keyframes ride{{to{{offset-distance:100%}}}} @keyframes show{{to{{opacity:1}}}}
.smoke{{position:absolute;left:0;top:0;width:24px;height:24px;margin-top:-40px;border-radius:50%;background:#2A1E1733;
 offset-path:path('{PATH}');offset-rotate:0deg;opacity:0;animation:ride 3.6s linear 2.05s forwards, puff .6s ease-out 2.05s 6}}
@keyframes puff{{0%{{opacity:.8;transform:scale(.6)}}100%{{opacity:0;transform:scale(2) translateY(-30px)}}}}
.lab{{position:absolute;font-weight:600;font-size:38px}}
.chips{{position:absolute;left:110px;right:170px;top:1240px;display:grid;grid-template-columns:1fr 1fr;gap:26px 30px}}
.chip b{{display:block;font-family:Fraunces,serif;font-weight:400;font-size:76px;color:{AC};line-height:1}}
.chip span{{font-size:30px}}
'''
html = head(BG, TX, css) + f'''
<p class="kick abs" style="top:250px;color:{AC};{sc(.1)}">MATARÓ · 1848</p>
<h1 class="abs" style="top:310px;{sc(.3)}">El primer tren de la Península acabó en Mataró.</h1>
<div class="map" style="{sc(1.4, 7.0)}">
 <svg width="860" height="520" viewBox="0 0 860 520">
  <path d="M0,520 L0,505 C 260,430 560,260 860,90 L860,520 Z" fill="#C9D9D6"/>
  <text x="480" y="480" font-family="Inter" font-size="28" fill="#5d7f7a" letter-spacing="8">MEDITERRÁNEO</text>
  <path class="trk" d="{PATH}"/>
  <circle cx="70" cy="470" r="16" fill="{TX}"/><circle cx="790" cy="60" r="16" fill="{TX}"/>
 </svg>
 <div class="train"></div><div class="smoke"></div>
 <div class="lab" style="left:0;top:380px;{sc(1.6)}">Barcelona</div>
 <div class="lab" style="left:560px;top:-50px;font-size:52px;color:{AC};{sc(5.4, kind='pop')}">Mataró</div>
 <div style="position:absolute;left:0;top:540px;font-size:24px;opacity:.6">Recreación aproximada</div>
</div>
<div class="chips" style="{sc(2.3, 7.0)}">
 <div class="chip" style="{sc(2.4)}"><b>28·10·1848</b><span>inauguración</span></div>
 <div class="chip" style="{sc(3.3)}"><b>≈ 28 km</b><span>de recorrido</span></div>
 <div class="chip" style="{sc(4.2)}"><b>~35 min</b><span>el primer viaje</span></div>
 <div class="chip" style="{sc(5.1)}"><b>400</b><span>pasajeros a bordo</span></div>
</div>
<p class="p abs" style="top:720px;{sc(7.5)}">La idea fue de un mataronés: <b style="color:{AC}">Miquel Biada</b>.</p>
<p class="p abs" style="top:900px;{sc(8.8)}">No llegó a verlo. Murió en abril de 1848, medio año antes de la inauguración.</p>
<p class="p abs ser" style="top:1250px;font-size:56px;color:{AC};{sc(10.6)}">Mándaselo a alguien que coja la R1 cada día.</p>
''' + TAIL
render(html, BASE + '/para-revisar/01-tren-1848/reel_tren_1848', 13.5, 6.4)
