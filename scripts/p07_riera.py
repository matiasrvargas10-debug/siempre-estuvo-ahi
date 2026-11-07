from rlib import head, TAIL, sc, render, BASE
BG, AC, TX = '#F3EBDD', '#2F7FB5', '#2A1E17'
OLD = 'M250,0 C 260,150 240,300 260,620'
NEW = 'M250,0 C 300,90 420,120 560,200 C 640,260 650,420 660,620'
css = f'''
.map{{position:absolute;left:110px;top:640px;width:800px;height:640px}}
.w{{fill:none;stroke-linecap:round;stroke-width:22;stroke-dasharray:900;stroke-dashoffset:900}}
.old{{stroke:{AC};animation:dr 2s ease-in 1.4s forwards, fade 1s ease 6.4s forwards}}
.new{{stroke:{AC};animation:dr 2.4s ease-in 6.8s forwards}}
@keyframes dr{{to{{stroke-dashoffset:0}}}} @keyframes fade{{to{{stroke:#B5452F;opacity:.35}}}}
.blk{{fill:#e2d6c2}}
.lab{{position:absolute;font-weight:600;font-size:34px}}
'''
blocks = ''.join(f'<rect class="blk" x="{x}" y="{y}" width="150" height="90" rx="8"/>'
                 for x in (40, 300, 430) for y in (120, 250, 380))
html = head(BG, TX, css) + f'''
<p class="kick abs" style="top:250px;color:#B5452F;{sc(.1)}">MATARÓ · ¿SABÍAS QUE…?</p>
<h1 class="abs" style="top:310px;font-size:84px;{sc(.3)}">Por La Riera bajaba agua de verdad.</h1>
<div class="map" style="{sc(1.0)}">
 <svg width="800" height="640" viewBox="0 0 800 640">{blocks}
  <rect x="0" y="600" width="800" height="40" fill="#C9D9D6"/>
  <path class="w old" d="{OLD}"/><path class="w new" d="{NEW}"/></svg>
 <div class="lab" style="left:20px;top:0;{sc(1.6)}">Riera de Cirera</div>
 <div class="lab" style="left:280px;top:520px;color:#B5452F;{sc(3.4)}">La Riera</div>
 <div class="lab" style="left:520px;top:100px;color:{AC};{sc(8.6)}">hacia Sant Simó</div>
 <div style="position:absolute;left:600px;top:606px;font-size:24px;opacity:.6">Esquema aproximado</div>
</div>
<p class="p abs" style="top:1330px;font-size:42px;{sc(3.8, 6.4)}">La riera de Cirera cruzaba la ciudad por el centro.</p>
<p class="p abs" style="top:1330px;font-size:42px;{sc(6.8, 10.6)}">A principios del siglo XX la desviaron hacia la riera de Sant Simó.</p>
<p class="p abs" style="top:1330px;font-size:42px;{sc(11.0)}">Hoy es la calle del <b>Ayuntamiento</b>. ¿Lo sabías?</p>
''' + TAIL
render(html, BASE + '/para-revisar/07-la-riera/reel_riera', 14, 4.5)
