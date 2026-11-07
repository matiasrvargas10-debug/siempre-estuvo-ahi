# Reel diario del mar en Mataró — 9:16, 8 s. Los datos se cargan a mano (verificados) en DATOS.
import os, asyncio, subprocess, datetime as dt
from playwright.async_api import async_playwright

BASE = os.path.dirname(os.path.abspath(__file__)); F = BASE + '/fonts'
FPS, DUR = 30, 8.0
BG, AC, CARD, TXT, MUT = '#0B2E2E', '#7FD8C9', '#12403F', '#FFFFFF', '#A9C9C4'
DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

DATOS = dict(fecha=dt.date(2026, 11, 6), agua='21,5', normal='17', normal_n=17.0, agua_n=21.5,
             olas='0,7–0,9', fuente='Fuentes: temperaturadomar.pt · climate-data.org')

d = DATOS['fecha']
# barras: escala 10–25 °C
esc = lambda t: (t - 10) / 15 * 100
HTML = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;font-weight:400;src:url(file://{F}/fraunces-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:400;src:url(file://{F}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url(file://{F}/inter-latin-600-normal.woff2)}}
body{{margin:0}}
.root{{width:1080px;height:1920px;box-sizing:border-box;padding:250px 150px 0 110px;background:{BG};color:{TXT};font-family:Inter,sans-serif;display:flex;flex-direction:column;gap:54px}}
.kick{{margin:0;font-size:28px;font-weight:600;letter-spacing:6px;color:{AC}}}
h1{{margin:18px 0 0;font-family:Fraunces,serif;font-weight:400;font-size:100px;line-height:1.04}}
.card{{background:{CARD};border-radius:28px;padding:40px 40px 36px}}
.lab{{margin:0;font-size:30px;color:{MUT}}} .big{{margin:10px 0 0;font-family:Fraunces,serif;font-size:150px;line-height:1}}
.row{{display:flex;align-items:center;gap:20px;margin-top:26px}} .rl{{width:190px;font-size:28px;color:{MUT}}}
.bar{{flex:1;height:26px;background:#0B2E2E;border-radius:13px;overflow:hidden}}
.fill{{height:100%;border-radius:13px;width:0}} .rv{{width:110px;text-align:right;font-size:30px;font-weight:600}}
.w1{{background:{AC};animation:w1 1.4s cubic-bezier(.2,.8,.2,1) 2.2s forwards}} @keyframes w1{{to{{width:{esc(DATOS['agua_n']):.0f}%}}}}
.w2{{background:#5C8F89;animation:w2 1.4s cubic-bezier(.2,.8,.2,1) 2.5s forwards}} @keyframes w2{{to{{width:{esc(DATOS['normal_n']):.0f}%}}}}
.fr{{margin:0;font-size:44px;line-height:1.3}} .fr b{{color:{AC};font-weight:600}}
.mid{{font-size:96px}}
.src{{margin:0;font-size:22px;color:{MUT}}}
.a{{opacity:0;animation:in .7s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:none}}}}
.wave{{position:absolute;left:0;bottom:0;width:2160px;height:120px;animation:wv 6s linear infinite}} @keyframes wv{{to{{transform:translateX(-1080px)}}}}
</style></head><body><div class="root" style="position:relative;overflow:hidden">
<div><p class="kick a" style="animation-delay:.1s">MATARÓ · EL MAR HOY</p>
<h1 class="a" style="animation-delay:.3s">{DIAS[d.weekday()]} {d.day} de {MESES[d.month - 1]}</h1></div>
<div class="card a" style="animation-delay:1.1s"><p class="lab">Temperatura del agua</p><p class="big">{DATOS['agua']} °C</p>
<div class="row"><span class="rl">Hoy</span><div class="bar"><div class="fill w1"></div></div><span class="rv">{DATOS['agua']}°</span></div>
<div class="row"><span class="rl">Normal en {MESES[d.month - 1]}</span><div class="bar"><div class="fill w2"></div></div><span class="rv">{DATOS['normal']}°</span></div></div>
<div class="card a" style="animation-delay:3.6s"><p class="lab">Olas</p><p class="big mid">{DATOS['olas']} m</p></div>
<p class="fr a" style="animation-delay:4.6s">El agua está <b>unos 4 °C más caliente</b> de lo normal para esta época.</p>
<p class="src a" style="animation-delay:5.4s">{DATOS['fuente']}</p>
<svg class="wave" viewBox="0 0 2160 120" preserveAspectRatio="none"><path d="M0,60 Q135,20 270,60 T540,60 T810,60 T1080,60 T1350,60 T1620,60 T1890,60 T2160,60 V120 H0Z" fill="{CARD}"/></svg>
</div></body></html>'''

async def main():
    out = BASE + '/reels'; os.makedirs(out, exist_ok=True)
    fn = f'{out}/mar_mataro_{d.isoformat()}.mp4'
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        tmp = BASE + '/tmp_mar.html'; open(tmp, 'w').write(HTML)
        await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready')
        await pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', fn],
                              stdin=subprocess.PIPE)
        for f in range(int(FPS * DUR)):
            await pg.evaluate(f'document.getAnimations().forEach(a=>a.currentTime={f * 1000 / FPS})')
            ff.stdin.write(await pg.screenshot(type='jpeg', quality=95))
        ff.stdin.close(); ff.wait()
        await pg.screenshot(path=fn.replace('.mp4', '_portada.png'))
        await b.close()
    print('listo', fn)

asyncio.run(main())
