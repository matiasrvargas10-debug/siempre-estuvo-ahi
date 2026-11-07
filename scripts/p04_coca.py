from rlib import head, TAIL, sc, render, BASE
BG, AC, TX = '#10202E', '#E8B66A', '#F5EFE4'
PATH = 'M120,560 C 40,380 420,300 300,40'
css = f'''
.map{{position:absolute;left:220px;top:740px;width:640px;height:620px}}
.rt{{fill:none;stroke:{AC};stroke-width:6;stroke-dasharray:14 14}}
.mask{{fill:none;stroke:{BG};stroke-width:12;stroke-dasharray:1100;stroke-dashoffset:0;animation:rev 3.2s linear 1.6s forwards}}
@keyframes rev{{to{{stroke-dashoffset:-1100}}}}
.ship{{position:absolute;left:0;top:0;offset-path:path('{PATH}');offset-distance:0%;offset-rotate:0deg;animation:sail 3.2s linear 1.6s forwards;opacity:0}}
@keyframes sail{{0%{{opacity:1;offset-distance:0%}}100%{{opacity:1;offset-distance:100%}}}}
.lab{{position:absolute;font-weight:600;font-size:40px}}
.fact{{display:flex;gap:26px;align-items:baseline;margin:0 0 34px}}
.fact b{{font-family:Fraunces,serif;font-weight:400;font-size:64px;color:{AC};min-width:230px}}
.fact span{{font-size:36px;line-height:1.3}}
'''
SHIP = f'''<svg width="90" height="90" viewBox="-45 -60 90 90" style="transform:translate(-45px,-60px)">
<path d="M-38,10 L38,10 L26,28 L-26,28 Z" fill="{TX}"/><rect x="-2" y="-55" width="4" height="65" fill="{TX}"/>
<path d="M4,-50 L34,0 L4,0 Z" fill="{AC}"/><path d="M-4,-40 L-28,0 L-4,0 Z" fill="{AC}" opacity=".7"/></svg>'''
html = head(BG, TX, css) + f'''
<p class="kick abs" style="top:250px;color:{AC};{sc(.1)}">MATARÓ · SIGLO XV</p>
<h1 class="abs" style="top:310px;font-size:80px;{sc(.3)}">La maqueta de barco más famosa de Mataró no está en Mataró.</h1>
<div class="map" style="{sc(1.2, 6.4)}">
 <svg width="640" height="620" viewBox="0 0 640 620"><path class="rt" d="{PATH}"/><path class="mask" d="{PATH}" style="stroke-dashoffset:0"/>
 <circle cx="120" cy="560" r="14" fill="{TX}"/><circle cx="300" cy="40" r="14" fill="{AC}"/></svg>
 <div class="ship">{SHIP}</div>
 <div class="lab" style="left:160px;top:540px">Mataró</div>
 <div class="lab" style="left:340px;top:10px;color:{AC};font-size:56px;{sc(4.8, kind='pop')}">Rotterdam</div>
 <div style="position:absolute;left:0;top:600px;font-size:24px;opacity:.55">Esquema, no es la ruta real</div>
</div>
<div class="abs" style="top:720px;{sc(6.8)}">
 <p class="fact"><b>s. XV</b><span>Barco votivo conocido como la <i>Coca de Mataró</i>.</span></p>
 <p class="fact" style="{sc(8.0)}"><b>Sant Simó</b><span>Según la tradición, colgaba en la ermita de Sant Simó.</span></p>
 <p class="fact" style="{sc(9.2)}"><b>1929</b><span>Llega al museo marítimo de Rotterdam. Sigue allí.</span></p>
 <p class="fact" style="{sc(10.4)}"><b>Rareza</b><span>Considerada de las maquetas de barco más antiguas de Europa.</span></p>
</div>
<p class="p abs ser" style="top:1470px;font-size:48px;color:{AC};{sc(11.8)}">¿Debería volver? Te leo.</p>
''' + TAIL
render(html, BASE + '/para-revisar/04-coca-de-mataro/reel_coca', 14.5, 5.6)
