from rlib import head, TAIL, sc, render, BASE
BG, AC, TX = '#2B0B14', '#E9C46A', '#F7EEDF'
css = f'''
.bottle{{position:absolute;left:330px;top:560px;width:300px;height:720px}}
.label{{position:absolute;left:30px;right:30px;top:360px;height:260px;background:#F3EBDD;color:#2B0B14;border-radius:10px;text-align:center;
 display:flex;flex-direction:column;justify-content:center;transform-origin:50% 0;animation:lab 1s cubic-bezier(.2,.8,.2,1) 1.4s backwards}}
@keyframes lab{{from{{transform:scaleY(0)}}}}
.spin{{animation:sw 1.2s ease-in-out 5.6s forwards}} @keyframes sw{{to{{transform:translateX(-230px) scale(.8)}}}}
'''
html = head(BG, TX, css) + f'''
<p class="kick abs" style="top:250px;color:{AC};{sc(.1)}">MATARÓ · AUSTRALIA</p>
<h1 class="abs" style="top:310px;font-size:84px;{sc(.3)}">En Australia, “Mataro” es una uva.</h1>
<div style="{sc(.9)}"><div class="bottle spin">
 <svg width="300" height="720" viewBox="0 0 300 720"><path d="M120,0 h60 v170 c0,40 90,60 90,140 v390 c0,12 -8,20 -20,20 h-200 c-12,0 -20,-8 -20,-20 v-390 c0,-80 90,-100 90,-140 z" fill="#140409" stroke="{AC}" stroke-width="3"/></svg>
 <div class="label"><div style="font-size:20px;letter-spacing:5px">SOUTH AUSTRALIA</div>
  <div class="ser" style="font-size:50px;line-height:1.1;margin:8px 0">MATARO</div><div style="font-size:20px;letter-spacing:3px">RED WINE · ETIQUETA INVENTADA</div></div>
</div></div>
<div class="abs" style="left:520px;right:140px;top:640px">
 <p class="p" style="font-size:42px;{sc(6.6)}">Es la <b style="color:{AC}">Monastrell</b>. En Francia, Mourvèdre.</p>
 <p class="p" style="font-size:42px;margin-top:40px;{sc(8.0)}">Llegó a Australia hacia <b style="color:{AC}">1830</b> y allí se quedó con el nombre de nuestra ciudad.</p>
 <p class="p" style="font-size:42px;margin-top:40px;{sc(9.6)}">En Barossa hay cepas de <b style="color:{AC}">1853</b>.</p>
</div>
<p class="p abs ser" style="top:1400px;font-size:50px;color:{AC};{sc(11.4)}">Mándaselo a quien sepa de vino.</p>
''' + TAIL
render(html, BASE + '/para-revisar/05-uva-mataro-australia/reel_uva', 14, 4.5)
