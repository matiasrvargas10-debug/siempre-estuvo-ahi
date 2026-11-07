from rlib import head, TAIL, sc, render, BASE
BG, AC, TX = '#0F1B2D', '#F4A63A', '#FFFFFF'
# minutero: 12:00 -> 12:34 = 204 grados ; horario: 0 -> 17 grados
css = f'''
.clock{{position:absolute;left:290px;top:640px;width:500px;height:500px;border-radius:50%;border:8px solid #ffffff33}}
.h,.m{{position:absolute;left:50%;bottom:50%;transform-origin:50% 100%;border-radius:8px;background:{TX}}}
.h{{width:16px;height:140px;margin-left:-8px;animation:hh 2.6s ease-in-out 1.4s forwards}}
.m{{width:10px;height:200px;margin-left:-5px;background:{AC};animation:mm 2.6s ease-in-out 1.4s forwards}}
@keyframes hh{{to{{transform:rotate(17deg)}}}} @keyframes mm{{to{{transform:rotate(204deg)}}}}
.sun{{position:absolute;left:480px;top:520px;width:120px;height:120px;border-radius:50%;background:{AC};box-shadow:0 0 80px 20px {AC}66;opacity:0;animation:pop .6s 4.0s forwards}}
.bar{{height:70px;border-radius:12px;background:#ffffff22;position:relative;margin:14px 0 40px}}
.fill{{position:absolute;left:0;top:0;bottom:0;border-radius:12px;background:{AC};width:0}}
.f1{{animation:f1 1s ease 6.6s forwards}} @keyframes f1{{to{{width:52%}}}}
.f2{{animation:f2 1s ease 7.6s forwards}} @keyframes f2{{to{{width:82%}}}}
.row{{font-size:40px;font-weight:600;display:flex;justify-content:space-between}}
'''
html = head(BG, TX, css) + f'''
<p class="kick abs" style="top:250px;color:{AC};{sc(.1)}">DATO INÚTIL DEL DÍA</p>
<h1 class="abs" style="top:310px;{sc(.3)}">En Mataró, el mediodía no es a las 12.</h1>
<div style="{sc(1.0, 5.8)}"><div class="clock"><div class="h"></div><div class="m"></div></div><div class="sun"></div>
 <p class="p abs" style="top:1200px;{sc(4.2)}">Estos días, el sol llega a lo más alto a las <b style="color:{AC}">12:34</b>.</p></div>
<div class="abs" style="top:660px;{sc(6.0)}">
 <p class="s" style="margin-bottom:30px">Mismo reloj, mismo día:</p>
 <div class="row"><span>Mataró</span><span style="color:{AC}">12:34</span></div><div class="bar"><div class="fill f1"></div></div>
 <div class="row"><span>A Coruña</span><span style="color:{AC}">13:17</span></div><div class="bar"><div class="fill f2"></div></div>
 <p class="p" style="{sc(9.0)}">En verano, en Mataró: <b style="color:{AC}">13:52</b>.</p>
 <p class="s" style="margin-top:30px;{sc(10.4)}">Culpa del huso horario: España usa la hora de Europa central.</p>
</div>
<p class="p abs ser" style="top:1400px;font-size:50px;color:{AC};{sc(12.0)}">¿Cambiarías la hora? Te leo.</p>
''' + TAIL
render(html, BASE + '/para-revisar/06-mediodia-1234/reel_mediodia', 14.5, 4.8)
