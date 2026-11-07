# Reel de la luna en Mataró — 9:16, 8 s, 30 fps. Datos con ephem.
# Uso: python3 reel_luna.py "2026-11-05 20:30"
import ephem, datetime as dt, os, sys, asyncio, subprocess, math
from zoneinfo import ZoneInfo
from playwright.async_api import async_playwright

BASE = os.path.dirname(os.path.abspath(__file__)); F = BASE + '/fonts'
FPS, DUR = 30, 8.0
TZ = ZoneInfo('Europe/Madrid')
BG, AC, CARD, TXT, MUT = '#15112B', '#C9B8FF', '#221C42', '#F2EEFF', '#A79FC7'
DS = ['lun', 'mar', 'mié', 'jue', 'vie', 'sáb', 'dom']
AHORA = dt.datetime.fromisoformat(sys.argv[1]).replace(tzinfo=TZ) if len(sys.argv) > 1 else dt.datetime.now(TZ)

o = ephem.Observer(); o.lat, o.lon, o.elevation = '41.5381', '2.4447', 0
loc = lambda d: ephem.Date(d).datetime().replace(tzinfo=dt.timezone.utc).astimezone(TZ)
utc = AHORA.astimezone(dt.timezone.utc)
o.date = utc; m = ephem.Moon(o)
ilum = round(m.phase); visible = m.alt > 0
creciente = ephem.next_new_moon(utc) > ephem.next_full_moon(utc)  # la próxima es la llena -> está creciendo
o.date = utc; sale = loc(o.next_rising(ephem.Moon())); o.date = utc; pone = loc(o.next_setting(ephem.Moon()))
o.date = utc; puso = loc(o.previous_setting(ephem.Moon()))
fases = sorted([(loc(f(utc)), n, k) for f, n, k in [
    (ephem.next_new_moon, 'Nueva', 0), (ephem.next_first_quarter_moon, 'Creciente', 1),
    (ephem.next_full_moon, 'Llena', 2), (ephem.next_last_quarter_moon, 'Menguante', 3)]])
nueva = [f for f in fases if f[2] == 0][0][0]
llena = [f for f in fases if f[2] == 2][0][0]

def nombre_fase(i, crec):
    if i < 3: return 'Luna nueva'
    if i > 97: return 'Luna llena'
    if 45 <= i <= 55: return 'Cuarto creciente' if crec else 'Cuarto menguante'
    if i < 50: return 'Creciente' if crec else 'Menguante'
    return 'Gibosa creciente' if crec else 'Gibosa menguante'

def luna_svg(frac, crec, R=150, cx=160, cy=160):
    # Hemisferio norte: creciente iluminada a la derecha, menguante a la izquierda
    s = 1 if crec else 0
    rx = abs(1 - 2 * frac) * R
    bulge = 1 if frac < .5 else 0  # el terminador se curva hacia el lado iluminado si es creciente
    if crec: d = f'M{cx},{cy-R} A{R},{R} 0 0 1 {cx},{cy+R} A{rx:.1f},{R} 0 0 {0 if frac < .5 else 1} {cx},{cy-R}Z'
    else:    d = f'M{cx},{cy-R} A{R},{R} 0 0 0 {cx},{cy+R} A{rx:.1f},{R} 0 0 {1 if frac < .5 else 0} {cx},{cy-R}Z'
    return f'''<svg width="320" height="320" viewBox="0 0 320 320"><circle cx="{cx}" cy="{cy}" r="{R}" fill="#2E2752"/><path d="{d}" fill="{TXT}"/></svg>'''

def mini(k):
    cx, R = 30, 24
    if k == 0: return f'<circle cx="{cx}" cy="{cx}" r="{R}" fill="#2E2752" stroke="#4A4178" stroke-width="2"/>'
    if k == 2: return f'<circle cx="{cx}" cy="{cx}" r="{R}" fill="{TXT}"/>'
    lado = 1 if k == 1 else 0
    return f'<circle cx="{cx}" cy="{cx}" r="{R}" fill="#2E2752"/><path d="M{cx},{cx-R} A{R},{R} 0 0 {lado} {cx},{cx+R}Z" fill="{TXT}"/>'

hoy = AHORA.date()
dia = lambda t: 'hoy' if t.date() == hoy else 'mañana' if t.date() == hoy + dt.timedelta(1) else f'{DS[t.weekday()]} {t.day:02d}/{t.month:02d}'
if visible:
    titulo = 'Mirá para arriba.<br>Está ahí.'
    c1, c2 = ('Salió', f'{sale.strftime("%H:%M")}'), ('Se pone', pone.strftime('%H:%M'))
    c1 = ('Se pone', pone.strftime('%H:%M')); c2 = ('Sale de nuevo', '')
else:
    titulo = 'Ahora no está<br>en el cielo.'
    c1, c2 = (f'Se puso {dia(puso)}', puso.strftime('%H:%M')), (f'Vuelve a salir {dia(sale)}', sale.strftime('%H:%M'))
dn = (nueva.date() - hoy).days; dl = (llena.date() - hoy).days
frase = (f'Faltan <b>{dn} días</b> para la luna nueva.' if dn < dl else f'Faltan <b>{dl} días</b> para la luna llena.')

fases_html = ''.join(f'''<div class="ph a" style="animation-delay:{4.2 + i * .25:.2f}s"><svg width="60" height="60">{mini(k)}</svg><p class="pn">{n}</p><p class="pd">{DS[t.weekday()]} {t.day:02d}/{t.month:02d}</p></div>''' for i, (t, n, k) in enumerate(fases))

HTML = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;font-weight:400;src:url(file://{F}/fraunces-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:400;src:url(file://{F}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url(file://{F}/inter-latin-600-normal.woff2)}}
body{{margin:0}}
.root{{width:1080px;height:1920px;box-sizing:border-box;padding:250px 150px 0 110px;background:{BG};color:{TXT};font-family:Inter,sans-serif;display:flex;flex-direction:column;gap:56px}}
.kick{{margin:0;font-size:28px;font-weight:600;letter-spacing:6px;color:{AC}}}
h1{{margin:18px 0 0;font-family:Fraunces,serif;font-weight:400;font-size:100px;line-height:1.04}}
.moon{{display:flex;align-items:center;gap:44px}}
.ft{{margin:0;font-family:Fraunces,serif;font-size:64px}} .il{{margin:8px 0 0;font-size:34px;color:{AC};font-weight:600}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:28px}}
.card{{background:{CARD};border-radius:26px;padding:34px 34px 30px}}
.lab{{margin:0;font-size:28px;color:{MUT}}} .big{{margin:10px 0 0;font-family:Fraunces,serif;font-size:104px;line-height:1}}
.fr{{margin:0;font-size:42px}} .fr b{{color:{AC};font-weight:600}}
.phs{{background:{CARD};border-radius:26px;padding:26px 20px;display:grid;grid-template-columns:repeat(4,1fr);text-align:center}}
.ph svg{{display:block;margin:0 auto 10px}} .pn{{margin:0;font-size:26px;font-weight:600}} .pd{{margin:4px 0 0;font-size:24px;color:{MUT}}}
.pt{{margin:0 0 14px;font-size:26px;color:{MUT}}}
.a{{opacity:0;animation:in .7s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:none}}}}
.glow{{opacity:0;animation:gl 1.6s ease-out 1s forwards}} @keyframes gl{{from{{opacity:0;transform:scale(.85) rotate(-8deg)}}to{{opacity:1;transform:none}}}}
</style></head><body><div class="root">
<div><p class="kick a" style="animation-delay:.1s">MATARÓ · LA LUNA DE HOY</p>
<h1 class="a" style="animation-delay:.3s">{titulo}</h1></div>
<div class="moon"><div class="glow">{luna_svg(m.phase / 100, creciente)}</div>
<div class="a" style="animation-delay:1.6s"><p class="ft">{nombre_fase(ilum, creciente)}</p><p class="il">{ilum}% iluminada</p></div></div>
<div class="grid"><div class="card a" style="animation-delay:2.4s"><p class="lab">{c1[0]}</p><p class="big">{c1[1]}</p></div>
<div class="card a" style="animation-delay:2.7s"><p class="lab">{c2[0]}</p><p class="big">{c2[1]}</p></div></div>
<p class="fr a" style="animation-delay:3.4s">{frase}</p>
<div><p class="pt a" style="animation-delay:4s">Próximas fases</p><div class="phs">{fases_html}</div></div>
</div></body></html>'''

async def main():
    out = BASE + '/reels'; os.makedirs(out, exist_ok=True)
    fn = f'{out}/luna_mataro_{hoy.isoformat()}.mp4'
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        tmp = BASE + '/tmp_luna.html'; open(tmp, 'w').write(HTML)
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
    print('listo', fn, '| ilum', ilum, '| visible', visible, '| puso', puso, '| sale', sale, '|', [(t.strftime('%d/%m %H:%M'), n) for t, n, _ in fases])

asyncio.run(main())
