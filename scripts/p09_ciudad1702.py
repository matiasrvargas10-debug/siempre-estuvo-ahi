from rlib import head, TAIL, sc, render, BASE
BG, AC, TX = '#2A1E17', '#B5452F', '#2A1E17'
css = f'''
.paper{{position:absolute;left:90px;right:150px;top:300px;height:1180px;background:#F3EBDD;border-radius:6px;padding:50px 56px;box-sizing:border-box;color:#2A1E17;
 box-shadow:0 30px 80px #0008;transform:rotate(-2deg);animation:drop .9s cubic-bezier(.2,.8,.2,1) .2s backwards}}
@keyframes drop{{from{{transform:translateY(-1500px) rotate(-14deg)}}}}
@keyframes zm{{from{{transform:rotate(-2deg) scale(1)}}to{{transform:rotate(-2deg) scale(1.04)}}}}
.mast{{text-align:center;border-bottom:4px double {TX};padding-bottom:18px}}
.mast .t{{font-family:Fraunces,serif;font-size:66px}}
.mast .d{{font-size:22px;letter-spacing:4px;margin-top:6px}}
.hl{{font-family:Fraunces,serif;font-weight:600;font-size:84px;line-height:1;margin:40px 0 24px;text-transform:uppercase}}
.col{{font-family:Fraunces,serif;font-size:36px;line-height:1.4;columns:1}}
.stamp{{position:absolute;right:40px;top:1000px;border:8px solid {AC};color:{AC};font-family:Fraunces,serif;font-size:56px;padding:14px 30px;
 transform:rotate(-12deg);opacity:0;animation:stamp .35s ease-out 3.2s forwards}}
@keyframes stamp{{0%{{opacity:0;transform:rotate(-12deg) scale(2.2)}}100%{{opacity:.9;transform:rotate(-12deg) scale(1)}}}}
.end{{position:absolute;left:110px;right:170px;top:600px;color:#F3EBDD}}
'''
html = head(BG, '#F3EBDD', css) + f'''
<div class="paper" style="animation:zm 5s linear forwards, out .5s ease 5.0s forwards">
 <div class="mast"><div class="t">Noticias del Maresme</div><div class="d">20 DE MARZO DE 1702 · RECREACIÓN</div></div>
 <div class="hl">Mataró compra su título de ciudad</div>
 <div class="col" style="{sc(.6)}">El rey Felipe V concede a la villa de Mataró el título de <b>Ciudad</b>.<br><br>
 Precio pagado: <b style="color:{AC}">3.500 doblas de oro</b>.</div>
 <div class="col" style="margin-top:40px;font-size:30px;opacity:0;animation:in .6s 2.2s forwards">La noticia se anota en Mataró el 15 de abril: “obtingué la vila de Mataró la gràcia de ésser Ciutat”.</div>
 <div class="stamp">CIUDAD</div>
</div>
<div class="end">
 <p class="p ser" style="font-size:72px;line-height:1.1;{sc(5.3)}">324 años siendo ciudad.</p>
 <p class="p" style="margin-top:50px;{sc(6.0)}">¿Tú qué dices: Mataró es ciudad o pueblo grande? Te leo.</p>
</div>
''' + TAIL
render(html, BASE + '/para-revisar/09-ciudad-1702/reel_ciudad_1702', 8.5, 3.8)
