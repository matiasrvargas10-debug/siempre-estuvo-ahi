# Reel "¿Cómo va a estar el día en Mataró?" — 9:16, 9 s. Datos cargados a mano desde la fuente.
import os, asyncio, subprocess
from playwright.async_api import async_playwright
BASE = os.path.dirname(os.path.abspath(__file__)); F = BASE + '/fonts'
FPS, DUR = 30, 9.0
BG, INK, AC, MUT, CARD = '#EAF1F8', '#14243A', '#2F6FB5', '#5B6B80', '#FFFFFF'

sun = '<circle cx="24" cy="24" r="9" fill="#F4A63A"/><g stroke="#F4A63A" stroke-width="3" stroke-linecap="round"><path d="M24 4v6M24 38v6M4 24h6M38 24h6M10 10l4 4M34 34l4 4M10 38l4-4M34 14l4-4"/></g>'
cloud_sun = '<circle cx="18" cy="18" r="8" fill="#F4A63A"/><path d="M14 38h22a8 8 0 0 0 0-16 11 11 0 0 0-21 3 7 7 0 0 0-1 13z" fill="#9FB3CC"/>'
rain = '<path d="M12 28h24a8 8 0 0 0 0-16 11 11 0 0 0-21 3 7 7 0 0 0-3 13z" fill="#7F93AE"/><g stroke="#2F6FB5" stroke-width="3" stroke-linecap="round"><path d="M16 34l-2 6M25 34l-2 6M34 34l-2 6"/></g>'
sunset = '<path d="M8 32a16 16 0 0 1 32 0z" fill="#F4A63A"/><path d="M4 36h40" stroke="#14243A" stroke-width="3" stroke-linecap="round"/><path d="M24 8v8M21 13l3 3 3-3" stroke="#F4A63A" stroke-width="3" fill="none" stroke-linecap="round"/>'
fog = '<g stroke="#7F93AE" stroke-width="4" stroke-linecap="round"><path d="M6 16h30M12 24h30M6 32h30M14 40h24"/></g>'

FILAS = [
    (cloud_sun, '11 – 13 h', '17–18 °C · parcialmente nuboso', 'Lo mejor del día para caminar.'),
    (rain, '13 – 15 h', 'Lluvia débil, poca cosa', 'Buen momento para comer a cubierto.'),
    (sunset, '17:37', 'Atardecer con pocas nubes', 'Vale la pena mirar al cielo.'),
    (fog, 'Desde 21 h', 'Baja a 10 °C y niebla', 'Ahí sí, chaqueta.'),
]
filas = ''.join(f'''<div class="row a" style="animation-delay:{1.3 + i * 1.0:.1f}s"><svg width="64" height="64" viewBox="0 0 48 48">{ic}</svg>
<div><p class="h">{h} <span>{t}</span></p><p class="c">{c}</p></div></div>''' for i, (ic, h, t, c) in enumerate(FILAS))

HTML = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;font-weight:400;src:url(file://{F}/fraunces-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:400;src:url(file://{F}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url(file://{F}/inter-latin-600-normal.woff2)}}
body{{margin:0}}
.root{{width:1080px;height:1920px;box-sizing:border-box;padding:250px 150px 0 110px;background:{BG};color:{INK};font-family:Inter,sans-serif;display:flex;flex-direction:column;gap:40px}}
.kick{{margin:0;font-size:30px;font-weight:600;letter-spacing:6px;color:{AC}}}
h1{{margin:18px 0 0;font-family:Fraunces,serif;font-weight:400;font-size:104px;line-height:1.02}}
.top{{display:flex;align-items:baseline;gap:24px;margin-top:10px}} .mx{{font-family:Fraunces,serif;font-size:150px;line-height:1;color:{AC}}} .mxl{{font-size:34px;color:{MUT}}}
.row{{background:{CARD};border-radius:26px;padding:26px 30px;display:flex;gap:26px;align-items:center;box-shadow:0 4px 18px rgba(20,36,58,.06)}}
.h{{margin:0;font-size:38px;font-weight:600}} .h span{{font-weight:400;color:{MUT};font-size:32px}} .c{{margin:6px 0 0;font-size:34px}}
.src{{margin:0;font-size:22px;color:{MUT}}}
.a{{opacity:0;animation:in .6s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(30px)}}to{{opacity:1;transform:none}}}}
</style></head><body><div class="root">
<div><p class="kick">MATARÓ · SÁBADO 7 DE NOVIEMBRE</p><h1>¿Chaqueta hoy?<br>Sí, pero ligera.</h1>
<div class="top"><span class="mx">18°</span><span class="mxl">máxima, entre las 12 y las 14 h</span></div></div>
{filas}
<p class="src a" style="animation-delay:5.6s">Previsión: meteosat.com · Datos que siempre estuvieron ahí. Síguenos.</p>
</div></body></html>'''

async def main():
    out = BASE + '/reels'; os.makedirs(out, exist_ok=True); fn = out + '/tiempo_mataro_2026-11-07.mp4'
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        tmp = BASE + '/tmp_tiempo.html'; open(tmp, 'w').write(HTML)
        await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready')
        await pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', fn], stdin=subprocess.PIPE)
        for f in range(int(FPS * DUR)):
            await pg.evaluate(f'document.getAnimations().forEach(a=>a.currentTime={f * 1000 / FPS})')
            ff.stdin.write(await pg.screenshot(type='jpeg', quality=92))
        ff.stdin.close(); ff.wait()
        await pg.screenshot(path='/tmp/tiempo_last.png')
    print('listo', fn)
asyncio.run(main())
