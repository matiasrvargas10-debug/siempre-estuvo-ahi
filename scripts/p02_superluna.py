from rlib import head, TAIL, sc, render, BASE
BG, AC, TX = '#15112B', '#C9B8FF', '#FFFFFF'
css = f'''
.moon{{position:absolute;border-radius:50%;background:radial-gradient(circle at 38% 35%,#fffbe8,#e8dcc0 60%,#bfb39a)}}
.grow{{animation:grow 2.4s ease-in-out 2.2s forwards}} @keyframes grow{{to{{transform:scale(1.065)}}}}
.glow{{animation:glow 2.4s ease-in-out 2.2s forwards}} @keyframes glow{{to{{box-shadow:0 0 120px 30px #fff6d655}}}}
.sky{{position:absolute;left:0;right:0;top:640px;height:620px;background:linear-gradient(#2a2350,#7a4f7a 70%,#e59a6b)}}
.sea{{position:absolute;left:0;right:0;top:1180px;height:80px;background:#1d2b4a}}
.rise{{animation:rise 3s ease-out 7.4s forwards}} @keyframes rise{{to{{transform:translateY(-260px)}}}}
.set{{animation:set 3s ease-in 7.4s forwards}} @keyframes set{{to{{transform:translateY(200px)}}}}
.t{{position:absolute;font-size:34px;font-weight:600}}
'''
html = head(BG, TX, css) + f'''
<p class="kick abs" style="top:250px;color:{AC};{sc(.1)}">24 DE NOVIEMBRE · MATARÓ</p>
<h1 class="abs" style="top:310px;{sc(.3)}">Vas a ver el sol y la superluna a la vez.</h1>

<div style="{sc(1.2, 6.6)}">
 <div class="moon" style="left:150px;top:760px;width:330px;height:330px"></div>
 <div class="moon grow glow" style="left:560px;top:760px;width:330px;height:330px"></div>
 <p class="s abs" style="top:1130px;left:150px">Luna llena media</p>
 <p class="abs" style="top:1130px;left:560px;font-size:30px;font-weight:600;color:{AC};margin:0">Superluna</p>
 <p class="p abs" style="top:1240px;{sc(3.2)}"><b style="color:{AC}">+6,5 %</b> más grande<br><b style="color:{AC}">+13,5 %</b> más brillante</p>
</div>

<div style="{sc(6.9)}">
 <div class="sky"></div><div class="sea"></div>
 <div class="moon rise" style="left:170px;top:1150px;width:120px;height:120px;box-shadow:0 0 60px 10px #fff6d655"></div>
 <div class="set" style="position:absolute;left:760px;top:900px;width:120px;height:120px;border-radius:50%;background:#ffb25c;box-shadow:0 0 80px 20px #ffb25c88"></div>
 <div class="t" style="left:110px;top:680px;{sc(7.8)}">16:56<br><span style="font-weight:400;font-size:28px">sale la luna (noreste)</span></div>
 <div class="t" style="left:640px;top:680px;text-align:right;width:260px;{sc(8.6)}">17:23<br><span style="font-weight:400;font-size:28px">se pone el sol</span></div>
 <p class="p abs" style="top:1300px;{sc(10.2)}">Casi media hora con los dos en el cielo.</p>
 <p class="s abs" style="top:1420px;{sc(11.4)}">Mejor desde la playa, mirando hacia Arenys.</p>
</div>
''' + TAIL
render(html, BASE + '/para-revisar/02-superluna/reel_superluna', 14, 5.2)
