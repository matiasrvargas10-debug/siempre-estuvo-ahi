# Librería común para renderizar reels 9:16 (y placas) con Chromium + ffmpeg.
import os, asyncio, subprocess
from playwright.async_api import async_playwright

BASE = os.path.dirname(os.path.abspath(__file__)); F = BASE + '/fonts'
FPS = 30

def head(bg, fg, extra=''):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;font-weight:400;src:url(file://{F}/fraunces-latin-400-normal.woff2)}}
@font-face{{font-family:Fraunces;font-weight:600;src:url(file://{F}/fraunces-latin-600-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:400;src:url(file://{F}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url(file://{F}/inter-latin-600-normal.woff2)}}
body{{margin:0}}
.root{{width:1080px;height:1920px;box-sizing:border-box;background:{bg};color:{fg};font-family:Inter,sans-serif;position:relative;overflow:hidden}}
.abs{{position:absolute;left:110px;right:170px}}
.kick{{margin:0;font-size:28px;font-weight:600;letter-spacing:6px}}
h1{{margin:0;font-family:Fraunces,serif;font-weight:400;font-size:92px;line-height:1.05}}
.ser{{font-family:Fraunces,serif}}
.p{{font-size:48px;line-height:1.3;margin:0}}
.s{{font-size:30px;line-height:1.35;margin:0;opacity:.75}}
.op{{opacity:0}}
@keyframes in{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:none}}}}
@keyframes out{{from{{opacity:1}}to{{opacity:0;transform:translateY(-30px)}}}}
@keyframes pop{{0%{{opacity:0;transform:scale(.6)}}70%{{opacity:1;transform:scale(1.08)}}100%{{opacity:1;transform:scale(1)}}}}
{extra}
</style></head><body><div class="root">'''

TAIL = '</div></body></html>'

def sc(t_in, t_out=None, kind='in'):
    """estilo de aparición (y salida opcional) en segundos"""
    s = f'opacity:0;animation:{kind} .6s cubic-bezier(.2,.8,.2,1) {t_in}s forwards'
    if t_out is not None:
        s += f', out .45s ease {t_out}s forwards'
    return s

async def _render(html, fn, dur, cover_t, w, h, js=False):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': w, 'height': h})
        tmp = fn + '.html'; open(tmp, 'w').write(html)
        await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready')
        await pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
        if dur:
            ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                                   '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                                   '-movflags', '+faststart', fn + '.mp4'], stdin=subprocess.PIPE)
            for f in range(int(FPS * dur)):
                await pg.evaluate(f'document.getAnimations().forEach(a=>a.currentTime={f * 1000 / FPS})')
                if js: await pg.evaluate(f'window.R({f / FPS})')
                ff.stdin.write(await pg.screenshot(type='jpeg', quality=92))
            ff.stdin.close(); ff.wait()
        await pg.evaluate(f'document.getAnimations().forEach(a=>a.currentTime={cover_t * 1000})')
        if js: await pg.evaluate(f'window.R({cover_t})')
        await pg.screenshot(path=fn + ('_portada.png' if dur else '.png'))
        await b.close()
    os.remove(tmp)

def render(html, fn, dur, cover_t, w=1080, h=1920, js=False):
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    asyncio.run(_render(html, fn, dur, cover_t, w, h, js))
    print('listo', fn)
