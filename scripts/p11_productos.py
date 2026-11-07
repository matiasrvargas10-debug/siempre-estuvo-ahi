from rlib import head, TAIL, render, BASE
BG, AC, TX = '#F6F0E2', '#3E7C3A', '#2A1E17'
css = '''.root{width:1080px;height:1350px;padding:120px 110px;box-sizing:border-box}
.n{font-family:Fraunces,serif;font-size:220px;line-height:.9;color:%s;margin:0}
.t{font-family:Fraunces,serif;font-size:84px;line-height:1.05;margin:30px 0 40px}
.d{font-size:40px;line-height:1.4;margin:0 0 26px}
.f{position:absolute;left:110px;bottom:90px;font-size:26px;opacity:.6}''' % AC
D = [
 ('portada', None, 'Lo que el Maresme cultiva y casi nadie fuera conoce.', ['Ranking de 4 productos. Desliza →'], ''),
 ('1', '4', 'Mongeta del ganxet', ['Judía blanca con forma de gancho (de ahí el nombre).', 'Tiene Denominación de Origen Protegida, y el Maresme está dentro.'], 'DOP Mongeta del Ganxet'),
 ('2', '3', 'Maduixa del Maresme', ['Fresas de la zona de la Vallalta: Sant Cebrià, Sant Iscle, Sant Pol, Arenys de Munt y Canet.', 'Su mejor momento: primavera.'], 'Consell Comarcal del Maresme'),
 ('3', '2', "Cirera d'en Roca", ['Cerezas de Arenys de Munt.', 'Las trajeron los hermanos Roca desde el Empordà a finales del siglo XIX.'], 'Xarxa Productes de la Terra (Diputació de Barcelona)'),
 ('4', '1', 'Pèsol de Llavaneres', ['La “perla verde” del Maresme. Variedad garrofal.', 'Tiene marca de garantía y solo dura marzo y abril.'], 'Xarxa Productes de la Terra · Vilaweb'),
 ('5', None, '¿Cuál falta en la lista?', ['Dímelo en comentarios y hacemos la parte 2.'], ''),
]
for slug, n, t, ds, src in D:
    body = (f'<p class="n">{n}</p>' if n else '<p class="kick" style="color:%s;margin-bottom:40px">MARESME · PRODUCTOS DE LA TIERRA</p>' % AC)
    body += f'<p class="t">{t}</p>' + ''.join(f'<p class="d">{d}</p>' for d in ds)
    if src: body += f'<p class="f">Fuente: {src}</p>'
    render(head(BG, TX, css) + body + TAIL, BASE + f'/para-revisar/11-productos-maresme/placa_{slug}', 0, 0, 1080, 1350)
