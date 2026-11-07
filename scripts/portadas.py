# Portadas 9:16 con todo dentro de la zona central 3:4 (la que muestra el perfil)
import asyncio, os
from playwright.async_api import async_playwright
F=os.path.abspath('fonts')
def html(bg,ac,txt,kick,title,num,sub):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;src:url(file://{F}/fraunces-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url(file://{F}/inter-latin-600-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:400;src:url(file://{F}/inter-latin-400-normal.woff2)}}
body{{margin:0}}.r{{width:1080px;height:1920px;background:{bg};color:{txt};font-family:Inter;display:flex;flex-direction:column;justify-content:center;padding:0 120px;box-sizing:border-box;gap:40px}}
.k{{margin:0;font-size:34px;font-weight:600;letter-spacing:6px;color:{ac}}}
h1{{margin:0;font-family:Fraunces;font-weight:400;font-size:120px;line-height:1.05}}
.n{{margin:0;font-family:Fraunces;font-size:190px;line-height:1;color:{ac}}}
.s{{margin:0;font-size:48px;opacity:.85}}</style></head><body><div class="r">
<p class="k">{kick}</p><h1>{title}</h1><p class="n">{num}</p><p class="s">{sub}</p></div></body></html>'''
P={'luna_mataro_2026-11-06_portada.png':('#15112B','#C9B8FF','#F2EEFF','MATARÓ · LA LUNA','Esta noche no está','6 %','iluminada · vuelve a salir a las 05:36')}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        for fn,a in P.items():
            open('tmp_p.html','w').write(html(*a)); await pg.goto('file://'+os.path.abspath('tmp_p.html')); await pg.evaluate('document.fonts.ready')
            await pg.screenshot(path='reels/'+fn)
        await b.close()
asyncio.run(main())
