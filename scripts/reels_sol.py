# Reels del sol en Mataró — 9:16 (1080x1920), 8 s, 30 fps
# Uso: python3 reels_sol.py [AAAA-MM-DD] [cantidad_de_días]
# Ej.: python3 reels_sol.py 2026-11-05 7   -> 7 reels desde el 5/11
# Necesita al lado: carpeta fonts/ con fraunces e inter (.woff2), y ffmpeg instalado.
import datetime as dt, os, sys, asyncio, subprocess, zipfile
from zoneinfo import ZoneInfo
from astral import LocationInfo
from astral.sun import sun
from playwright.async_api import async_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
F = BASE + '/fonts'
INICIO = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today() + dt.timedelta(1)
CANT = int(sys.argv[2]) if len(sys.argv) > 2 else 1
FPS, DUR = 30, 8.0
TZ = ZoneInfo('Europe/Madrid')
LOC = LocationInfo('Mataro', 'ES', 'Europe/Madrid', 41.5381, 2.4447)
AC, BG, CARD, MUTED, TXT = '#F4A63A', '#0F1B2D', '#1A2A42', '#AEBBCC', '#EEF2F7'
DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
INI = ['E', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']

def datos(d):
    s = sun(LOC.observer, date=d, tzinfo=TZ)
    m = round((s['sunset'] - s['sunrise']).total_seconds() / 60)
    return s['sunrise'].strftime('%H:%M'), s['sunset'].strftime('%H:%M'), m

def curva_anio(y):
    """Horas de luz de todo el año calendario (para el gráfico)."""
    d0 = dt.date(y, 1, 1); n = (dt.date(y + 1, 1, 1) - d0).days
    return [(d0 + dt.timedelta(i), datos(d0 + dt.timedelta(i))[2]) for i in range(n)]

def proximo_minimo(d):
    """Día más corto que viene (mira 366 días hacia adelante)."""
    lst = [(d + dt.timedelta(i), datos(d + dt.timedelta(i))[2]) for i in range(366)]
    mn = min(t[1] for t in lst); ds = [t[0] for t in lst if t[1] == mn]
    return ds[len(ds) // 2]  # varios días empatan al minuto: tomo el del medio (solsticio)

def html(d):
    sal, pue, m = datos(d)
    m_ayer = datos(d - dt.timedelta(1))[2]
    dif = m - m_ayer
    cambio = (f'{abs(dif)} min menos que ayer' if dif < 0 else f'{dif} min más que ayer' if dif > 0 else 'igual que ayer')
    dmin = proximo_minimo(d); falta = (dmin - d).days
    frase = (f'Faltan <b>{falta} días</b> para el día más corto del año.' if falta > 1 else
             'Mañana es el día más corto del año.' if falta == 1 else 'Hoy es el día más corto del año.')
    if falta > 0 and falta > 200:  # ya pasó el solsticio de invierno
        frase = 'Los días ya se están alargando.'

    año = curva_anio(d.year)
    W, H, lo, hi = 820, 260, 8.5, 15.5
    n = len(año)
    P = [(i * W / (n - 1), H - (mm / 60 - lo) / (hi - lo) * H) for i, (_, mm) in enumerate(año)]
    path = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in P)
    area = path + f' L{W},{H} L0,{H} Z'
    ih = (d - dt.date(d.year, 1, 1)).days; hx, hy = P[ih]
    medio = lambda val: (lambda ix: ix[len(ix) // 2])([i for i in range(n) if año[i][1] == val])
    imax = medio(max(x[1] for x in año)); imin = medio(min(x[1] for x in año))
    fh = lambda mm: f'{mm // 60} h {mm % 60:02d}'
    meses = ''.join(f'<text x="{(dt.date(d.year, k + 1, 15) - dt.date(d.year, 1, 1)).days * W / (n - 1):.0f}" y="{H + 44}" font-size="24" fill="{MUTED}" text-anchor="middle" font-family="Inter">{INI[k]}</text>' for k in range(12))

    up = '<path d="M12 3v5M9 6l3-3 3 3"/><path d="M5 18a7 7 0 0 1 14 0"/><path d="M2 21h20"/>'
    dn = '<path d="M12 8V3M9 5l3 3 3-3"/><path d="M5 18a7 7 0 0 1 14 0"/><path d="M2 21h20"/>'
    card = lambda ic, lab, val, dl: f'''<div class="card a" style="animation-delay:{dl}s"><svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="{AC}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ic}</svg><p class="lab">{lab}</p><p class="big">{val}</p></div>'''
    L = 2400  # largo aprox. de la curva para el efecto de "dibujarse"
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;font-weight:400;src:url(file://{F}/fraunces-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:400;src:url(file://{F}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url(file://{F}/inter-latin-600-normal.woff2)}}
body{{margin:0}}
.root{{width:1080px;height:1920px;box-sizing:border-box;padding:250px 150px 0 110px;background:{BG};color:{TXT};font-family:Inter,sans-serif;display:flex;flex-direction:column;gap:60px}}
.kick{{margin:0;font-size:28px;font-weight:600;letter-spacing:6px;color:{AC}}}
h1{{margin:0;font-family:Fraunces,serif;font-weight:400;font-size:112px;line-height:1.02}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:32px}}
.card{{background:{CARD};border-radius:28px;padding:44px 40px 40px;display:flex;flex-direction:column;gap:14px}}
.lab{{margin:0;font-size:32px;color:{MUTED}}}
.big{{margin:0;font-family:Fraunces,serif;font-size:136px;line-height:1;font-variant-numeric:tabular-nums}}
.luz{{margin:0;font-size:46px;line-height:1.3}} .luz b{{color:{AC};font-weight:600}}
.sub{{margin:10px 0 0;font-size:34px;color:{MUTED}}}
.gt{{margin:0 0 18px;font-size:28px;color:{MUTED}}}
.a{{opacity:0;animation:in .7s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:none}}}}
.f{{opacity:0;animation:fa .6s ease forwards}} @keyframes fa{{to{{opacity:1}}}}
.draw{{stroke-dasharray:{L};stroke-dashoffset:{L};animation:dr 2s ease-in-out 3.2s forwards}} @keyframes dr{{to{{stroke-dashoffset:0}}}}
.pop{{transform-box:fill-box;transform-origin:center;transform:scale(0);animation:pp .5s cubic-bezier(.3,1.6,.5,1) 5.3s forwards}} @keyframes pp{{to{{transform:scale(1)}}}}
.pulse{{transform-box:fill-box;transform-origin:center;opacity:0;animation:pu 1.4s ease-out 5.8s 2}} @keyframes pu{{0%{{opacity:.7;transform:scale(1)}}100%{{opacity:0;transform:scale(3)}}}}
</style></head><body><div class="root">
<div style="display:flex;flex-direction:column;gap:20px">
<p class="kick a" style="animation-delay:.1s">MATARÓ · SALIDA Y PUESTA DEL SOL</p>
<h1 class="a" style="animation-delay:.3s">{DIAS[d.weekday()]} {d.day} de {MESES[d.month - 1]}</h1></div>
<div class="grid">{card(up, 'Sale el sol', sal, 1.0)}{card(dn, 'Se pone', pue, 1.3)}</div>
<div class="a" style="animation-delay:2.1s"><p class="luz"><b>{m // 60} h {m % 60} min</b> de luz. {frase}</p>
<p class="sub">{cambio}.</p></div>
<div class="f" style="animation-delay:2.9s"><p class="gt">Horas de luz en Mataró, {d.year}</p>
<svg width="820" height="340" viewBox="-10 -40 840 360" style="overflow:visible">
<path d="{area}" fill="{CARD}" class="f" style="animation-delay:4.6s"/>
<line x1="0" y1="{H}" x2="{W}" y2="{H}" stroke="#3A4C66" stroke-width="2"/>
{meses}
<path d="{path}" fill="none" stroke="{AC}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" class="draw"/>
<g class="f" style="animation-delay:5.0s">
<circle cx="{P[imax][0]:.1f}" cy="{P[imax][1]:.1f}" r="8" fill="{AC}"/>
<text x="{P[imax][0]:.1f}" y="{P[imax][1] - 22:.1f}" font-size="24" fill="{MUTED}" text-anchor="middle" font-family="Inter">{año[imax][0].strftime('%d/%m')} · {fh(año[imax][1])}</text>
<circle cx="{P[imin][0]:.1f}" cy="{P[imin][1]:.1f}" r="8" fill="{AC}"/>
<text x="{W}" y="{H + 92}" font-size="24" fill="{MUTED}" text-anchor="end" font-family="Inter">Día más corto: {año[imin][0].strftime('%d/%m')} · {fh(año[imin][1])}</text></g>
<circle cx="{hx:.1f}" cy="{hy:.1f}" r="12" fill="{TXT}" class="pulse"/>
<circle cx="{hx:.1f}" cy="{hy:.1f}" r="13" fill="{TXT}" class="pop"/>
<text x="{hx:.1f}" y="{hy - 30:.1f}" font-size="28" fill="{TXT}" font-family="Inter" font-weight="600" text-anchor="middle" class="f" style="animation-delay:5.5s">Hoy</text>
</svg></div></div></body></html>'''

async def main():
    out = BASE + '/reels'; os.makedirs(out, exist_ok=True); hechos = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for k in range(CANT):
            d = INICIO + dt.timedelta(k)
            tmp = BASE + '/tmp_reel.html'; open(tmp, 'w').write(html(d))
            await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready')
            await pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
            fn = f'{out}/sol_mataro_{d.isoformat()}.mp4'
            ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                                   '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                                   '-movflags', '+faststart', fn], stdin=subprocess.PIPE)
            for f in range(int(FPS * DUR)):
                await pg.evaluate(f'document.getAnimations().forEach(a=>a.currentTime={f * 1000 / FPS})')
                ff.stdin.write(await pg.screenshot(type='jpeg', quality=95))
            ff.stdin.close(); ff.wait()
            await pg.screenshot(path=fn.replace('.mp4', '_portada.png'))
            hechos += [fn, fn.replace('.mp4', '_portada.png')]; print('listo', fn)
        await b.close()
    if CANT > 1:
        with zipfile.ZipFile(BASE + '/reels_sol.zip', 'w') as z:
            for f in hechos: z.write(f, os.path.basename(f))

asyncio.run(main())
