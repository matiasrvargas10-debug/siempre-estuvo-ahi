from rlib import head, TAIL, render, BASE
# Cielo de Mataró, domingo 8/11/2026 a las 7:00, mirando al mar (este-sureste). Posiciones calculadas con ephem.
S = 30  # px por grado
H = 1010  # horizonte
X = lambda az: 540 + (az - 116.5) * S
Y = lambda alt: H - alt * S
V, E, L = (118.96, 12.71), (117.74, 12.55), (115.91, 1.84)
css = '''.root{width:1080px;height:1350px;background:linear-gradient(#0c0f2a 0%%,#1d2150 38%%,#5a3f6e 62%%,#c9775a 80%%,#f2b36b 86%%)}
.sea{position:absolute;left:0;right:0;top:%dpx;bottom:0;background:linear-gradient(#2a3354,#0d1530)}
.st{position:absolute;border-radius:50%%;background:#fff}
.lb{position:absolute;font:600 34px Inter;color:#fff;white-space:nowrap}
.sm{font:400 26px Inter;opacity:.8}
.ln{position:absolute;height:2px;background:#ffffffaa;transform-origin:0 0}''' % H
import random; random.seed(8)
stars = ''.join(f'<div class="st" style="left:{random.randint(0,1080)}px;top:{random.randint(0,520)}px;width:{random.choice([2,2,3])}px;height:3px;opacity:{random.random()*.6+.2:.2f}"></div>' for _ in range(90))
vx, vy = X(V[0]), Y(V[1]); ex, ey = X(E[0]), Y(E[1]); lx, ly = X(L[0]), Y(L[1])
html = head('#0c0f2a', '#fff', css) + f'''{stars}
<div class="sea"></div>
<div style="position:absolute;left:0;right:0;top:{H}px;height:3px;background:#ffd59a88"></div>
<div class="st" style="left:{vx-11}px;top:{vy-11}px;width:22px;height:22px;box-shadow:0 0 40px 14px #fff6"></div>
<div class="st" style="left:{ex-5}px;top:{ey-5}px;width:10px;height:10px;background:#cfe0ff;box-shadow:0 0 18px 6px #9fc2ff88"></div>
<div style="position:absolute;left:{lx-16}px;top:{ly-16}px;width:32px;height:32px;border-radius:50%;box-shadow:inset 4px -4px 0 0 #ffe9c4cc"></div>
<div class="ln" style="left:{vx+18}px;top:{vy-10}px;width:120px;transform:rotate(-25deg)"></div>
<div class="lb" style="left:{vx+125}px;top:{vy-90}px">Venus<br><span class="sm">lo más brillante</span></div>
<div class="ln" style="left:{ex-14}px;top:{ey-6}px;width:120px;transform:rotate(-155deg)"></div>
<div class="lb" style="left:{ex-330}px;top:{ey-110}px;text-align:right;width:200px">Espiga<br><span class="sm">estrella</span></div>
<div class="lb" style="left:{lx-430}px;top:{ly-80}px;text-align:right;width:400px;font-size:28px">Luna, casi invisible<br><span class="sm">solo un 1 % iluminada</span></div>
<div style="position:absolute;left:110px;top:120px;right:110px">
 <p class="kick" style="color:#C9B8FF">MATARÓ · DOMINGO 8 · 7:00</p>
 <h1 style="font-size:72px;margin-top:20px">Mañana, antes del amanecer, mira al mar.</h1>
</div>
<div style="position:absolute;left:110px;right:110px;top:{H+60}px">
 <p class="p" style="font-size:40px">Venus y la Espiga, casi pegadas: a un dedo de distancia con el brazo estirado.</p>
 <p class="s" style="margin-top:22px">Bajas sobre el horizonte, hacia el este-sureste. Mejor de 6:45 a 7:15.</p>
</div>
<div style="position:absolute;right:30px;top:{H-34}px;font-size:22px;opacity:.6">Posiciones reales calculadas · ilustración</div>
''' + TAIL
render(html, BASE + '/para-revisar/16-mira-al-cielo-manana/placa_cielo_8nov', 0, 0, 1080, 1350)
