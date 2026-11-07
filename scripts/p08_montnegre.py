from rlib import head, TAIL, sc, render, BASE
BG, AC, TX = '#13261B', '#9BD27A', '#F2F5EE'
css = f'''
@property --n{{syntax:'<integer>';inherits:false;initial-value:0}}
.cnt{{--n:0;counter-reset:n var(--n);animation:cn 2.2s ease-out 1.2s forwards}}
.cnt::after{{content:counter(n)}}
@keyframes cn{{to{{--n:15010}}}}
.grid{{position:absolute;left:110px;top:900px;display:grid;grid-template-columns:repeat(4,150px);gap:18px}}
.sq{{width:150px;height:150px;border-radius:14px;background:{AC};opacity:0;animation:pop .4s ease forwards}}
.mt{{background:#F4A63A}}
'''
sqs = '<div class="sq mt" style="animation-delay:4.2s"></div>' + ''.join(
    f'<div class="sq" style="animation-delay:{4.6 + i * .25}s"></div>' for i in range(6)) + \
    '<div class="sq" style="width:100px;animation-delay:6.1s"></div>'
html = head(BG, TX, css) + f'''
<p class="kick abs" style="top:250px;color:{AC};{sc(.1)}">EL BOSQUE DE AL LADO</p>
<h1 class="abs" style="top:310px;font-size:84px;{sc(.3)}">Detrás de Mataró hay un bosque casi 7 veces más grande que la ciudad.</h1>
<div style="{sc(1.0, 8.0)}">
 <p class="abs ser" style="top:700px;font-size:120px;margin:0;color:{AC}"><span class="cnt"></span></p>
 <p class="s abs" style="top:850px">hectáreas · Parc del Montnegre i el Corredor</p>
 <div class="grid">{sqs}</div>
 <p class="p abs" style="top:1270px;font-size:38px;{sc(4.4)}"><b style="color:#F4A63A">■</b> Mataró &nbsp; <b style="color:{AC}">■</b> el parque</p>
</div>
<div class="abs" style="top:740px;{sc(8.4)}">
 <p class="p"><b class="ser" style="color:{AC};font-size:80px;font-weight:400">773 m</b><br>Turó Gros, el techo del Montnegre</p>
 <p class="p" style="margin-top:40px;{sc(9.6)}"><b class="ser" style="color:{AC};font-size:80px;font-weight:400">657 m</b><br>el santuario del Corredor</p>
 <p class="p" style="margin-top:40px;{sc(10.8)}"><b class="ser" style="color:{AC};font-size:80px;font-weight:400">+200</b><br>masías repartidas por el parque</p>
</div>
<p class="p abs ser" style="top:1420px;font-size:46px;color:{AC};{sc(12.2)}">¿Cuál es tu ruta? Te leo.</p>
''' + TAIL
render(html, BASE + '/para-revisar/08-montnegre-corredor/reel_montnegre', 14.5, 6.8)
