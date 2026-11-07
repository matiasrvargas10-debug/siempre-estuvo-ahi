from rlib import head, TAIL, sc, render, BASE
BG, AC, TX = '#0E0E12', '#E5484D', '#FFFFFF'
SERIES = ['Días de Navidad', 'El cuerpo en llamas', 'Dos tumbas', 'Terra Alta', 'Merlí: Sapere Aude', 'Moebius']
css = f'''
.rain i{{position:absolute;width:3px;height:60px;background:#ffffff30;animation:rn .7s linear infinite}}
@keyframes rn{{from{{transform:translateY(-200px)}}to{{transform:translateY(2100px)}}}}
.it{{display:flex;align-items:center;gap:28px;font-size:46px;font-weight:600;margin:0 0 30px}}
.it span{{display:inline-block;width:62px;height:62px;border-radius:12px;background:{AC};color:#fff;font-size:34px;text-align:center;line-height:62px}}
'''
import random; random.seed(3)
rain = ''.join(f'<i style="left:{random.randint(0,1080)}px;animation-delay:-{random.random():.2f}s"></i>' for _ in range(40))
items = ''.join(f'<p class="it" style="{sc(2.2 + i * .9)}"><span>{i+1}</span>{s}</p>' for i, s in enumerate(SERIES))
html = head(BG, TX, css) + f'''
<div class="rain" style="position:absolute;inset:0">{rain}</div>
<p class="kick abs" style="top:250px;color:{AC};{sc(.1)}">DÍA DE SOFÁ</p>
<h1 class="abs" style="top:310px;font-size:84px;{sc(.3)}">¿Llueve? Series con escenas rodadas en Mataró.</h1>
<div class="abs" style="top:720px">{items}</div>
<p class="p abs ser" style="top:1430px;font-size:46px;color:{AC};{sc(8.4)}">¿Reconociste alguna calle? Te leo.</p>
''' + TAIL
render(html, BASE + '/para-revisar/12-dia-de-sofa-series/reel_series', 12, 8.0)
