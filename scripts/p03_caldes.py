from rlib import head, TAIL, sc, render, BASE
BG, AC, TX = '#0B2E2E', '#7FD8C9', '#FFFFFF'
css = f'''
.card{{position:absolute;left:110px;right:170px;top:560px;background:#12403F;border-radius:36px;padding:60px 56px 70px}}
.btns{{position:absolute;left:110px;right:170px;top:1150px;display:grid;grid-template-columns:1fr 1fr;gap:30px}}
.b{{border:4px solid #ffffff55;border-radius:999px;text-align:center;font-weight:600;font-size:44px;padding:26px 0}}
.ok{{animation:ok .4s ease 3.4s forwards}} @keyframes ok{{to{{background:{AC};border-color:{AC};color:#0B2E2E;transform:scale(1.06)}}}}
.no{{animation:dim .4s ease 3.4s forwards}} @keyframes dim{{to{{opacity:.25}}}}
.tick{{animation:tick 2.4s ease 1.6s forwards}} @keyframes tick{{0%{{width:100%}}100%{{width:0%}}}}
.big{{font-family:Fraunces,serif;font-size:150px;line-height:1;color:{AC};margin:0}}
.steam span{{position:absolute;width:16px;height:120px;border-radius:8px;background:#ffffff40;animation:st 1.6s ease-in-out infinite}}
@keyframes st{{0%{{opacity:0;transform:translateY(40px) scaleY(.6)}}50%{{opacity:1}}100%{{opacity:0;transform:translateY(-60px)}}}}
'''
html = head(BG, TX, css) + f'''
<p class="kick abs" style="top:250px;color:{AC};{sc(.1)}">¿MITO O VERDAD?</p>
<h1 class="abs" style="top:310px;font-size:70px;{sc(.2)}">Tú decides antes de que acabe la barra.</h1>
<div style="{sc(.5, 5.6)}">
 <div class="card"><p class="p" style="font-size:58px;line-height:1.25">A 10 minutos de Mataró sale agua del suelo a casi <b style="color:{AC}">40 °C</b>.</p>
  <div style="height:10px;background:#ffffff22;border-radius:5px;margin-top:50px;overflow:hidden"><div class="tick" style="height:100%;background:{AC};width:100%"></div></div></div>
 <div class="btns"><div class="b no">MITO</div><div class="b ok">VERDAD</div></div>
</div>
<div style="{sc(5.9)}">
 <p class="big abs" style="top:760px">38,5 °C</p>
 <p class="p abs" style="top:930px">Es el agua termal de <b>Caldes d'Estrac</b>.</p>
 <p class="p abs" style="top:1080px;{sc(7.6)}">Brotan unos <b style="color:{AC}">232.000 litros</b> al día.</p>
 <p class="p abs" style="top:1230px;{sc(9.2)}">Y el nombre ya te avisaba: <i class="ser">Caldes</i> = aguas calientes.</p>
 <p class="s abs" style="top:1420px;opacity:0;animation:in .6s 10.8s forwards">¿Te has bañado alguna vez? Te leo en comentarios.</p>
</div>
''' + TAIL
render(html, BASE + '/para-revisar/03-caldes-mito-verdad/reel_caldes', 13, 1.0)
