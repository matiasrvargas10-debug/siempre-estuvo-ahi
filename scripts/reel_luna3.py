# Reel de la luna v3 — cielo de noche, la luna sale del mar y se esconde, y cierra con el mes en 2 segundos.
# Uso: python3 reel_luna3.py "2026-11-07 20:00"
import ephem, datetime as dt, os, sys, asyncio, subprocess, math, json
from zoneinfo import ZoneInfo
from playwright.async_api import async_playwright

BASE = os.path.dirname(os.path.abspath(__file__)); F = BASE + '/fonts'
FPS, DUR = 30, 11.0
TZ = ZoneInfo('Europe/Madrid')
AC, TXT, MUT = '#C9B8FF', '#F2EEFF', '#B9B0DA'
DS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
AHORA = dt.datetime.fromisoformat(sys.argv[1]).replace(tzinfo=TZ)
o = ephem.Observer(); o.lat, o.lon, o.elevation = '41.5381', '2.4447', 0
loc = lambda d: ephem.Date(d).datetime().replace(tzinfo=dt.timezone.utc).astimezone(TZ)
utc = AHORA.astimezone(dt.timezone.utc)
o.date = utc; m = ephem.Moon(o); frac = m.phase / 100; arriba = m.alt > 0
creciente = ephem.next_new_moon(utc) > ephem.next_full_moon(utc)
o.date = utc; sale = loc(o.next_rising(ephem.Moon()))
o.date = ephem.Date(sale.astimezone(dt.timezone.utc)); pone = loc(o.next_setting(ephem.Moon()))
o.date = ephem.Date(sale.astimezone(dt.timezone.utc)); sol_sale = loc(o.next_rising(ephem.Sun()))
o.date = ephem.Date(sale.astimezone(dt.timezone.utc)); sol_pone = loc(o.next_setting(ephem.Sun()))
nueva = loc(ephem.next_new_moon(utc)); llena = loc(ephem.next_full_moon(utc))
hoy = AHORA.date()
DSC = ['lun', 'mar', 'mié', 'jue', 'vie', 'sáb', 'dom']
fases = sorted([(loc(f(utc)), n, k) for f, n, k in [(ephem.next_new_moon, 'Nueva', 0), (ephem.next_first_quarter_moon, 'Creciente', 1),
    (ephem.next_full_moon, 'Llena', 2), (ephem.next_last_quarter_moon, 'Menguante', 3)]])
def mini(k):
    c, R = 26, 21
    if k == 0: return f'<circle cx="{c}" cy="{c}" r="{R}" fill="#2E2752" stroke="#6A5FA0" stroke-width="2"/>'
    if k == 2: return f'<circle cx="{c}" cy="{c}" r="{R}" fill="#F2EEFF"/>'
    return f'<circle cx="{c}" cy="{c}" r="{R}" fill="#2E2752"/><path d="M{c},{c-R} A{R},{R} 0 0 {1 if k == 1 else 0} {c},{c+R}Z" fill="#F2EEFF"/>'
FH = ''.join(f'<div class="ph"><svg width="52" height="52">{mini(k)}</svg><p class="pn">{n}</p><p class="pd">{DSC[t.weekday()]} {t.day:02d}/{t.month:02d}</p></div>' for t, n, k in fases)
cuando = lambda t: 'hoy' if t.date() == hoy else 'mañana' if t.date() == hoy + dt.timedelta(1) else f'el {DS[t.weekday()]}'
de_noche = sale < sol_sale or sale > sol_pone
de_dia_pone = sol_sale < pone < sol_pone
dn = (nueva.date() - hoy).days; dl = (llena.date() - hoy).days
nota = (f'Luna nueva {cuando(nueva) if dn <= 6 else f"en {dn} días"}.' if dn <= dl else f'Luna llena {cuando(llena) if dl <= 6 else f"en {dl} días"}.')
theta_hoy = math.acos(1 - 2 * frac); theta_hoy = 2 * math.pi - theta_hoy if not creciente else theta_hoy
assert not arriba, 'esta versión es para cuando la luna no está arriba a la hora de publicar'

HTML = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;font-weight:400;src:url(file://{F}/fraunces-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:400;src:url(file://{F}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url(file://{F}/inter-latin-600-normal.woff2)}}
body{{margin:0}}
.root{{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Inter,sans-serif;color:{TXT};background:#0D0A1F}}
.sky{{position:absolute;inset:0}}
.night{{background:linear-gradient(#0D0A1F,#15112B 55%,#2A2350 72%)}}
.day{{background:linear-gradient(#3B4F8C,#6F86C2 60%,#A9B8E0 72%);opacity:0;animation:day 11s linear forwards}}
@keyframes day{{0%,44%{{opacity:0}}54%,70%{{opacity:1}}82%,100%{{opacity:.15}}}}
.stars{{animation:st 11s linear forwards}} @keyframes st{{0%,42%{{opacity:1}}52%,72%{{opacity:0}}84%,100%{{opacity:.7}}}}
.tw{{animation:tw 1.6s ease-in-out infinite alternate}} @keyframes tw{{from{{opacity:.25}}to{{opacity:1}}}}
.cloud{{position:absolute;height:70px;border-radius:40px;background:rgba(201,184,255,.10);filter:blur(6px)}}
.c1{{width:420px;top:820px;left:-450px;animation:cl 11s linear forwards}} .c2{{width:300px;top:980px;left:-320px;animation:cl 11s linear -4s forwards}}
@keyframes cl{{to{{transform:translateX(1700px)}}}}
.moon{{position:absolute;left:0;top:0;width:260px;height:260px;animation:mv 11s linear forwards}}
@keyframes mv{{0%,20%{{transform:translate(140px,1230px)}}32%{{transform:translate(170px,910px)}}48%{{transform:translate(410px,580px)}}
 62%{{transform:translate(640px,720px)}}76%{{transform:translate(740px,1230px)}}100%{{transform:translate(740px,1230px)}}}}
.sea{{position:absolute;left:0;right:0;top:1200px;bottom:0;background:linear-gradient(#1C1840,#0D0A1F)}}
.arrow{{position:absolute;left:245px;top:1210px;font-size:70px;color:{AC};animation:ar 11s linear forwards}}
@keyframes ar{{0%{{opacity:0}}5%,18%{{opacity:1}}21%,100%{{opacity:0}}}}
.ghost{{position:absolute;left:140px;top:1290px;width:260px;height:260px;border:3px dashed rgba(201,184,255,.55);border-radius:50%;box-sizing:border-box;animation:ar 11s linear forwards}}
.txt{{position:absolute;left:110px;right:150px;top:250px}}
.blk{{position:absolute;top:0;left:0;right:0;opacity:0}}
.kick{{margin:0;font-size:30px;font-weight:600;letter-spacing:6px;color:{AC}}}
.q{{margin:22px 0 0;font-family:Fraunces,serif;font-size:110px;line-height:1.02}}
.lab{{margin:24px 0 0;font-size:54px}} .sub{{margin:10px 0 0;font-size:40px;color:{MUT}}}
.big{{margin:4px 0 0;font-family:Fraunces,serif;font-size:240px;line-height:.95}}
.b0{{animation:b0 11s linear forwards}} @keyframes b0{{0%,19%{{opacity:1}}22%,100%{{opacity:0}}}}
.b1{{animation:b1 11s linear forwards}} @keyframes b1{{0%,22%{{opacity:0}}25%,48%{{opacity:1}}51%,100%{{opacity:0}}}}
.b2{{animation:b2 11s linear forwards}} @keyframes b2{{0%,51%{{opacity:0}}54%,100%{{opacity:1}}}}
.endX{{position:absolute;inset:0;background:#15112B;opacity:0;animation:en 11s linear forwards;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;text-align:center}}
@keyframes en{{0%,64%{{opacity:0}}68%,100%{{opacity:1}}}}
.end .t{{margin:0;font-size:40px;color:{MUT}}} .end .h{{margin:0;font-family:Fraunces,serif;font-size:100px}} .end .h b{{color:{AC};font-weight:400}}
.end .n{{margin:0;font-size:44px}} .cta{{margin:30px 0 0;font-size:34px;color:{MUT}}}
.dat{{position:absolute;left:110px;right:150px;top:1240px}}
.phs{{margin-top:26px;background:rgba(34,28,66,.85);border-radius:24px;padding:20px 14px;display:grid;grid-template-columns:repeat(4,1fr);text-align:center;opacity:0;animation:d1 11s linear forwards}}
.ph svg{{display:block;margin:0 auto 8px}} .pn{{margin:0;font-size:24px;font-weight:600}} .pd{{margin:2px 0 0;font-size:22px;color:{MUT}}}
.d1{{margin:0;font-size:44px;opacity:0;animation:d1 11s linear forwards}} .d1 b{{color:{AC};font-weight:600}} @keyframes d1{{0%,28%{{opacity:0}}32%,100%{{opacity:1}}}}
.d2{{margin:24px 0 0;font-size:32px;color:{MUT};opacity:0;animation:d2 11s linear forwards}} @keyframes d2{{0%,80%{{opacity:0}}84%,100%{{opacity:1}}}}
.late{{opacity:0;animation:la 11s linear forwards}} @keyframes la{{0%,86%{{opacity:0}}90%,100%{{opacity:1}}}}
</style></head><body><div class="root">
<div class="sky night"></div><div class="sky day"></div>
<svg class="sky stars" width="1080" height="1200">{''.join(f'<circle class="tw" style="animation-delay:-{(i*37)%16/10}s" cx="{(i*397)%1080}" cy="{(i*211)%1170}" r="{1.5+(i%3)}" fill="#fff"/>' for i in range(70))}</svg>
<div class="cloud c1"></div><div class="cloud c2"></div>
<svg class="moon" viewBox="0 0 200 200" id="m1"></svg>
<div class="sea"></div>
<div class="ghost"></div><div class="arrow">↓</div>
<div class="txt">
<div class="blk b0"><p class="kick">MATARÓ · ESTA NOCHE</p><p class="q">¿Dónde está la luna?</p><p class="sub" style="margin-top:30px">Debajo del horizonte. Esta noche no la vas a ver.</p></div>
<div class="blk b1"><p class="kick">MATARÓ · LA LUNA</p><p class="lab">Sale del mar {cuando(sale)} a las</p><p class="big">{sale.strftime('%H:%M')}</p><p class="sub">{'todavía de noche' if de_noche else 'ya de día'}</p></div>
<div class="blk b2"><p class="kick">MATARÓ · LA LUNA</p><p class="lab">y se esconde a las</p><p class="big">{pone.strftime('%H:%M')}</p><p class="sub">{'a plena luz del día' if de_dia_pone else 'ya de noche'}</p></div>
</div>
<div class="dat"><p class="d1"><b>{round(frac*100)} %</b> iluminada · {nota}</p><div class="phs">{FH}</div><p class="d2">Cada noche, un dato que siempre estuvo ahí. Síguenos.</p></div><svg id="m2" style="display:none"></svg>
</div>
<script>
const TH={theta_hoy};
function path(th,R=90,c=100){{const k=(1-Math.cos(th))/2,crec=th<Math.PI,rx=Math.abs(1-2*k)*R;
 if(crec)return `M${{c}},${{c-R}} A${{R}},${{R}} 0 0 1 ${{c}},${{c+R}} A${{rx}},${{R}} 0 0 ${{k<.5?0:1}} ${{c}},${{c-R}}Z`;
 return `M${{c}},${{c-R}} A${{R}},${{R}} 0 0 0 ${{c}},${{c+R}} A${{rx}},${{R}} 0 0 ${{k<.5?1:0}} ${{c}},${{c-R}}Z`;}}
function moon(id,th,glow){{document.getElementById(id).innerHTML=`<circle cx="100" cy="100" r="90" fill="#2E2752" stroke="rgba(201,184,255,.5)" stroke-width="2"/><path d="${{path(th)}}" fill="{TXT}" ${{glow?'style="filter:drop-shadow(0 0 12px #C9B8FF)"':''}}/>`;}}
window.R=function(t){{moon('m1',TH,true);
 const a=6.9,b=8.7; let p=Math.min(1,Math.max(0,(t-a)/(b-a))); p=1-Math.pow(1-p,3);
 moon('m2',TH-2*Math.PI*(1-p),false);}}
R(0);
</script></body></html>'''

async def main():
    out = BASE + '/reels'; os.makedirs(out, exist_ok=True); fn = f'{out}/luna3_mataro_{hoy.isoformat()}.mp4'
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        tmp = BASE + '/tmp_luna3.html'; open(tmp, 'w').write(HTML)
        await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready')
        await pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', fn], stdin=subprocess.PIPE)
        for f in range(int(FPS * DUR)):
            t = f / FPS
            await pg.evaluate(f'document.getAnimations().forEach(a=>a.currentTime={t * 1000});R({t})')
            ff.stdin.write(await pg.screenshot(type='jpeg', quality=92))
        ff.stdin.close(); ff.wait()
    print('listo', fn, '| sale', sale, '| pone', pone, '| sol', sol_sale.strftime('%H:%M'), sol_pone.strftime('%H:%M'), '| ilum', round(frac * 100), nota)

asyncio.run(main())
