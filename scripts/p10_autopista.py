from rlib import head, TAIL, sc, render, BASE
BG, AC, TX = '#1E1F22', '#F2C230', '#FFFFFF'
css = f'''
.road{{position:absolute;left:390px;width:300px;top:0;bottom:0;background:#2c2d31;overflow:hidden}}
.dash{{position:absolute;left:142px;width:16px;height:2400px;top:-480px;
 background:repeating-linear-gradient(#fff 0 120px,transparent 120px 240px);animation:mv .8s linear infinite}}
@keyframes mv{{to{{transform:translateY(240px)}}}}
.slot{{position:absolute;left:250px;top:620px;width:580px;height:24px;background:#000;border-radius:12px}}
.ticket{{position:absolute;left:290px;top:632px;width:500px;height:0;overflow:hidden;background:#F7F3E6;color:#1E1F22;border-radius:0 0 10px 10px;
 font-family:monospace;animation:print 2.4s steps(24) 2.0s forwards}}
@keyframes print{{to{{height:620px}}}}
.tk{{padding:40px 44px;font-size:34px;line-height:1.5}}
'''
html = head(BG, TX, css) + f'''
<div class="road" style="opacity:.35"><div class="dash"></div></div>
<p class="kick abs" style="top:250px;color:{AC};{sc(.1)}">MARESME · 1969</p>
<h1 class="abs" style="top:310px;font-size:76px;{sc(.3)}">La primera autopista de peaje de España llegaba a Mataró.</h1>
<div style="{sc(1.4, 8.6)}"><div class="slot"></div>
 <div class="ticket"><div class="tk">AUTOPISTA DE PEAJE<br>──────────────<br>ENTRADA: MONTGAT<br>SALIDA:&nbsp; MATARÓ<br>──────────────<br>FECHA: 02-07-1969<br>Nº 000001<br><br><span style="font-size:22px">TICKET RECREADO · NO REAL</span></div></div></div>
<div class="abs" style="top:700px;{sc(8.9)}">
 <p class="p">Se inauguró el <b style="color:{AC}">2 de julio de 1969</b>, entre Montgat y Mataró.</p>
 <p class="p" style="margin-top:44px;{sc(10.2)}">Fue la primera de peaje de todo el país. Hoy es parte de la <b style="color:{AC}">C-32</b>.</p>
</div>
<p class="p abs ser" style="top:1340px;font-size:50px;color:{AC};{sc(11.8)}">¿Cuántas veces la has hecho? Te leo.</p>
''' + TAIL
render(html, BASE + '/para-revisar/10-autopista-1969/reel_autopista', 14, 5.0)
