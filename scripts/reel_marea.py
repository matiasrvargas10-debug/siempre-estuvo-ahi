# Reel "¿Sabías que…?" — la marea en Mataró. 9:16, 12 s, 30 fps.
# Uso: python3 reel_marea.py   (necesita fonts/ al lado y ffmpeg)
import os, asyncio, subprocess
from playwright.async_api import async_playwright

BASE = os.path.dirname(os.path.abspath(__file__)); F = BASE + '/fonts'
FPS, DUR = 30, 12.0
BG, AC, CARD, TXT, MUT = '#0B2E2E', '#7FD8C9', '#12403F', '#FFFFFF', '#A9C9C4'

# Escala: 14 m = 440 px de agua  ->  20 cm = 6 px
HTML = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;font-weight:400;src:url(file://{F}/fraunces-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:400;src:url(file://{F}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url(file://{F}/inter-latin-600-normal.woff2)}}
body{{margin:0}}
.root{{width:1080px;height:1920px;box-sizing:border-box;padding:250px 110px 0;background:{BG};color:{TXT};font-family:Inter,sans-serif;position:relative;overflow:hidden}}
.kick{{margin:0;font-size:28px;font-weight:600;letter-spacing:6px;color:{AC}}}
h1{{margin:20px 0 0;font-family:Fraunces,serif;font-weight:400;font-size:100px;line-height:1.04}}
.a{{opacity:0;animation:in .7s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:none}}}}
.out{{animation:out .5s ease forwards}} @keyframes out{{to{{opacity:0;transform:translateY(-30px)}}}}
.cmp{{position:absolute;left:110px;right:110px;top:720px;display:grid;grid-template-columns:1fr 1fr;gap:40px}}
.col{{display:flex;flex-direction:column;gap:18px}}
.tank{{height:520px;background:{CARD};border-radius:28px;position:relative;overflow:hidden}}
.water{{position:absolute;left:0;right:0;bottom:0;background:{AC}}}
.big{{margin:0;font-family:Fraunces,serif;font-size:100px;line-height:1;color:{AC}}}
.lab{{margin:0;font-size:34px;font-weight:600}} .sub{{margin:0;font-size:28px;color:{MUT}}}
.msm{{animation:msm 3s ease-in-out infinite alternate}} @keyframes msm{{from{{height:40px}}to{{height:480px}}}}
.mat{{animation:mat 3s ease-in-out infinite alternate}} @keyframes mat{{from{{height:40px}}to{{height:46px}}}}
.txt{{position:absolute;left:110px;right:110px;top:720px;font-size:50px;line-height:1.35}}
.txt b{{color:{AC};font-weight:600}}
.note{{margin-top:50px;font-size:38px;line-height:1.4;color:{MUT}}}
</style></head><body><div class="root">
<p class="kick a" style="animation-delay:.1s">MATARÓ · ¿SABÍAS QUE…?</p>
<h1 class="a" style="animation-delay:.3s">En Mataró, la marea casi no existe.</h1>

<div class="cmp" style="opacity:0;animation:in .7s cubic-bezier(.2,.8,.2,1) 1.2s forwards, out .5s ease 6.6s forwards">
 <div class="col"><p class="big">14 m</p><div class="tank"><div class="water msm"></div></div>
  <p class="lab">Mont Saint-Michel</p><p class="sub">Francia · océano Atlántico</p></div>
 <div class="col"><p class="big">20 cm</p><div class="tank"><div class="water mat"></div></div>
  <p class="lab">Mataró</p><p class="sub">Mediterráneo · misma escala</p></div>
</div>

<div class="txt a" style="animation-delay:7.2s">¿Por qué? El Mediterráneo se conecta con el océano solo por el <b>estrecho de Gibraltar</b>, de unos 14&nbsp;km. La marea del Atlántico entra muy debilitada.
<p class="note a" style="animation-delay:9.2s">Acá el mar lo mueven más el viento y la presión: con 1 hPa menos de presión, el agua sube ~1&nbsp;cm.</p></div>
</div></body></html>'''

async def main():
    out = BASE + '/reels'; os.makedirs(out, exist_ok=True)
    fn = out + '/mar_marea_mataro.mp4'
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        tmp = BASE + '/tmp_marea.html'; open(tmp, 'w').write(HTML)
        await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready')
        await pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', fn],
                              stdin=subprocess.PIPE)
        for f in range(int(FPS * DUR)):
            await pg.evaluate(f'document.getAnimations().forEach(a=>a.currentTime={f * 1000 / FPS})')
            ff.stdin.write(await pg.screenshot(type='jpeg', quality=95))
        ff.stdin.close(); ff.wait()
        await pg.evaluate('document.getAnimations().forEach(a=>a.currentTime=5000)')
        await pg.screenshot(path=out + '/mar_marea_mataro_portada.png')
        await b.close()
    print('listo', fn)

asyncio.run(main())
