# Reel del sol v2 — el sol sale del mar y se pone. 9:16, 7 s, 30 fps.
# Uso: python3 reel_sol2.py 2026-11-07
import datetime as dt, os, sys, asyncio, subprocess
from zoneinfo import ZoneInfo
from astral import LocationInfo
from astral.sun import sun, elevation
from playwright.async_api import async_playwright

BASE = os.path.dirname(os.path.abspath(__file__)); F = BASE + '/fonts'
FPS, DUR = 30, 8.0
TZ = ZoneInfo('Europe/Madrid'); LOC = LocationInfo('Mataro', 'ES', 'Europe/Madrid', 41.5381, 2.4447)
D = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today() + dt.timedelta(1)
import json
# Tiempo del día (verificado a mano): json con w1, w2, w3, plan, nubes (0-1 de nubosidad a la tarde)
W = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}

def datos(d):
    s = sun(LOC.observer, date=d, tzinfo=TZ)
    return s['sunrise'].strftime('%H:%M'), s['sunset'].strftime('%H:%M'), round((s['sunset'] - s['sunrise']).total_seconds() / 60), (s['sunset'] - s['sunrise']).total_seconds()
sal, pue, m, secs = datos(D); _s = sun(LOC.observer, date=D, tzinfo=TZ); noon = _s['noon']; alt = round(elevation(LOC.observer, noon)); mid = (noon + dt.timedelta(seconds=30)).strftime('%H:%M'); dif = round((secs - datos(D - dt.timedelta(1))[3]) / 60)
# próximo día más corto (medio de los empates)
lst = [(D + dt.timedelta(i), datos(D + dt.timedelta(i))[2]) for i in range(366)]
mn = min(x[1] for x in lst); ds = [x[0] for x in lst if x[1] == mn]; falta = (ds[len(ds) // 2] - D).days
cambio = f'{abs(dif)} min {"menos" if dif < 0 else "más"} que ayer' if dif else 'igual que ayer'
cola = f'Faltan {falta} días para el día más corto.' if falta < 200 else 'Los días ya se alargan.'

NUB = W.get('nubes', 0)
HTML = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;font-weight:400;src:url(file://{F}/fraunces-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:400;src:url(file://{F}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url(file://{F}/inter-latin-600-normal.woff2)}}
body{{margin:0}}
.root{{width:1080px;height:1920px;position:relative;overflow:hidden;background:#0F1B2D;font-family:Inter,sans-serif;color:#FFF7EC}}
.sky{{position:absolute;inset:0}}
.night{{background:linear-gradient(#0F1B2D 0%,#1B2A44 60%,#3A3A55 75%)}}
.dawn{{background:linear-gradient(#22335A 0%,#7A5A7A 45%,#F4A63A 72%);opacity:0;animation:dawn 8s linear forwards}}
@keyframes dawn{{0%{{opacity:.15}}20%{{opacity:1}}38%{{opacity:.3}}60%{{opacity:.3}}80%{{opacity:1}}100%{{opacity:.25}}}}
.sun{{position:absolute;width:190px;height:190px;border-radius:50%;background:radial-gradient(#FFE3A3,#F4A63A 70%);
 box-shadow:0 0 120px 40px rgba(244,166,58,.45);left:445px;top:1180px;animation:arc 8s cubic-bezier(.45,0,.55,1) forwards}}
@keyframes arc{{0%{{transform:translate(-260px,40px)}}22%{{transform:translate(-200px,-260px)}}45%{{transform:translate(0,-420px)}}
 68%{{transform:translate(200px,-260px)}}84%{{transform:translate(270px,60px)}}100%{{transform:translate(270px,60px)}}}}
.sea{{position:absolute;left:0;right:0;top:1270px;bottom:0;background:linear-gradient(#16304D,#0B1626)}}
.glint{{position:absolute;left:0;right:0;top:1270px;height:300px;background:radial-gradient(ellipse 260px 60px at 50% 0,rgba(244,166,58,.55),transparent);animation:gl 8s linear forwards}}
@keyframes gl{{0%{{opacity:.6}}22%{{opacity:1}}45%{{opacity:.2}}78%{{opacity:.9}}100%{{opacity:.3}}}}
.txt{{position:absolute;left:110px;right:150px;top:250px}}
.kick{{margin:0;font-size:30px;font-weight:600;letter-spacing:6px;color:#F4A63A}}
.lab{{margin:26px 0 0;font-size:56px}}
.big{{margin:6px 0 0;font-family:Fraunces,serif;font-size:250px;line-height:.95;font-variant-numeric:tabular-nums}}
.p1{{animation:o1 8s linear forwards}} @keyframes o1{{0%,27%{{opacity:1}}31%,100%{{opacity:0}}}}
.pm{{position:absolute;top:0;left:0;right:0;opacity:0;animation:om 8s linear forwards}} @keyframes om{{0%,31%{{opacity:0}}35%,57%{{opacity:1}}61%,100%{{opacity:0}}}}
.p2{{position:absolute;top:0;left:0;right:0;opacity:0;animation:o2 8s linear forwards}} @keyframes o2{{0%,61%{{opacity:0}}65%,100%{{opacity:1}}}}
.w{{margin:14px 0 0;font-size:42px;color:#FFE3A3}}
.clouds{{position:absolute;left:-200px;right:-200px;top:300px;height:900px;opacity:0;animation:cl 8s linear forwards;background:radial-gradient(ellipse 380px 120px at 30% 55%,rgba(200,210,225,.85),transparent 70%),radial-gradient(ellipse 420px 130px at 75% 62%,rgba(190,200,215,.9),transparent 70%),radial-gradient(ellipse 300px 100px at 55% 45%,rgba(210,218,230,.8),transparent 70%),radial-gradient(ellipse 360px 140px at 76% 96%,rgba(185,195,212,.97),transparent 72%)}}
@keyframes cl{{0%,40%{{opacity:0;transform:translateX(-60px)}}75%,100%{{opacity:{NUB};transform:translateX(40px)}}}}
.info{{position:absolute;left:110px;right:150px;top:1330px;font-size:40px;line-height:1.4;opacity:0;animation:fi .6s ease 6.2s forwards}}
.info b{{color:#F4A63A;font-weight:600}} .info span{{color:#C9D3E0;font-size:34px}}
@keyframes fi{{to{{opacity:1}}}}
</style></head><body><div class="root">
<div class="sky night"></div><div class="sky dawn"></div>
<div class="sun"></div><div class="clouds"></div><div class="sea"></div><div class="glint"></div>
<div class="txt"><div class="p1"><p class="kick">MATARÓ · HOY</p><p class="lab">El sol sale del mar a las</p><p class="big">{sal}</p><p class="w">{W.get("w1","")}</p></div>
<div class="pm"><p class="kick">MATARÓ · HOY</p><p class="lab">llega a lo más alto a las</p><p class="big">{mid}</p><p class="w">{W.get("w2", f"a {alt}° sobre el horizonte")}</p></div>
<div class="p2"><p class="kick">MATARÓ · HOY</p><p class="lab">y se esconde a las</p><p class="big">{pue}</p><p class="w">{W.get("w3","")}</p></div></div>
<div class="info">{W.get("plan","")}<br><b>{m // 60} h {m % 60:02d} min</b> de luz · {cambio}.<br><span>{cola}</span></div>
</div></body></html>'''

async def main():
    out = BASE + '/reels'; os.makedirs(out, exist_ok=True); fn = f'{out}/sol2_mataro_{D.isoformat()}.mp4'
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        tmp = BASE + '/tmp_sol2.html'; open(tmp, 'w').write(HTML)
        await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready')
        await pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', fn], stdin=subprocess.PIPE)
        for f in range(int(FPS * DUR)):
            await pg.evaluate(f'document.getAnimations().forEach(a=>a.currentTime={f * 1000 / FPS})')
            ff.stdin.write(await pg.screenshot(type='jpeg', quality=92))
        ff.stdin.close(); ff.wait()
    print('listo', fn, sal, mid, alt, pue, m, dif, falta)

asyncio.run(main())
