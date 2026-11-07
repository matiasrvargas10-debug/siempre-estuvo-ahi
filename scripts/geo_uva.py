# Reel uva Mataro: globo real (Natural Earth) que viaja de Mataró a Barossa y hace zoom.
import json
from rlib import head, TAIL, sc, render, BASE
G = BASE + '/geo/node_modules/'
# datos reales en un .js para cargarlos sin fetch
w = json.load(open(G + 'world-atlas/countries-10m.json'))
au = json.load(open(G + '@highcharts/map-collection/countries/au/au-all.topo.json'))
open(BASE + '/geo/data_uva.js', 'w').write('var W=' + json.dumps(w) + ';var AU=' + json.dumps(au) + ';')

BG, AC, TX = '#0D2A3F', '#E9C46A', '#FFFFFF'
css = f'''
svg{{position:absolute;inset:0}}
.top{{position:absolute;left:0;right:0;top:0;height:760px;background:linear-gradient(#0D2A3Fee 55%,#0D2A3F00)}}
.k{{position:absolute;left:110px;top:250px;color:{AC}}}
.txt{{position:absolute;left:110px;right:170px;top:310px}}
.pin{{font:600 40px Inter;fill:#fff;paint-order:stroke;stroke:#0D2A3F;stroke-width:10px}}
'''
html = head(BG, TX, css) + f'''
<svg id="m" width="1080" height="1920"></svg>
<div class="top"></div>
<p class="kick k" style="{sc(.1)}">MATARÓ → AUSTRALIA</p>
<h1 class="txt" style="font-size:84px;{sc(.3, 5.6)}">Hay una uva que se llama “Mataro”.</h1>
<h1 class="txt" style="font-size:84px;{sc(5.9, 9.4)}">Está a 16.000 km de aquí.</h1>
<div class="txt" style="{sc(9.7)}"><h1 style="font-size:76px">Barossa Valley, Australia del Sur.</h1>
 <p class="p" style="margin-top:30px;{sc(11.0)}">Allí llaman <b style="color:{AC}">Mataro</b> a nuestra Monastrell. Y tienen cepas de <b style="color:{AC}">1853</b>.</p></div>
<p class="p ser" style="position:absolute;left:110px;right:170px;top:1430px;font-size:46px;color:{AC};text-shadow:0 2px 12px #000;{sc(13.2)}">Mándaselo a quien sepa de vino.</p>
<script src="file://{G}d3-array/dist/d3-array.min.js"></script>
<script src="file://{G}d3-geo/dist/d3-geo.min.js"></script>
<script src="file://{G}topojson-client/dist/topojson-client.min.js"></script>
<script src="file://{BASE}/geo/data_uva.js"></script>
<script>
const NS='http://www.w3.org/2000/svg', svg=document.getElementById('m');
const land={{type:'FeatureCollection',features:topojson.feature(W,W.objects.countries).features.filter(f=>f.id!=='010'&&d3.geoArea(f)<2*Math.PI)}}, borders=topojson.mesh(W,W.objects.countries,(a,b)=>a!==b);
const states=topojson.feature(AU,Object.values(AU.objects)[0]).features, SA=states.find(f=>f.properties.name==='South Australia');
const sMesh=topojson.mesh(AU,Object.values(AU.objects)[0],(a,b)=>a!==b);
const MAT=[2.4447,41.5381], BAR=[138.95,-34.53], ip=d3.geoInterpolate(MAT,BAR), grat=d3.geoGraticule10();
const ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2, cl=x=>Math.max(0,Math.min(1,x));
function el(t,a){{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);svg.appendChild(e);return e}}
window.R=function(t){{
  // centro y escala por tramos
  let c, s;
  const tv=ease(cl((t-2.2)/4.2));            // viaje 2.2–6.4 s
  c = tv<=0?MAT: tv>=1?BAR: ip(tv);
  s = 1300 - 800*Math.sin(Math.PI*tv);        // se aleja en medio del viaje
  const tz=ease(cl((t-6.6)/3.0));            // zoom 6.6–9.6 s
  s = s*Math.pow(5,tz);
  const p=d3.geoOrthographic().rotate([-c[0],-c[1]]).scale(s).translate([540,1150]).clipAngle(90);
  const g=d3.geoPath(p);
  svg.innerHTML='';
  el('path',{{d:g({{type:'Sphere'}}),fill:'#123B57'}});
  el('path',{{d:g(grat),fill:'none',stroke:'#ffffff14','stroke-width':1}});
  land.features.forEach(f=>el('path',{{d:g(f),fill:'#E9DFC8'}}));
  el('path',{{d:g(borders),fill:'none',stroke:'#b9ab8c','stroke-width':1.5}});
  if(t>6.6){{const o=cl((t-7.5)/1.2);
    el('path',{{d:g(SA),fill:'{AC}','fill-opacity':.55*o}});
    el('path',{{d:g(sMesh),fill:'none',stroke:'#9c8e6e','stroke-width':2,'stroke-opacity':o}});}}
  // arco del viaje
  if(t>2.2){{const n=60,k=Math.round(n*Math.min(tv,1)),pts=[];for(let i=0;i<=k;i++)pts.push(ip(i/n));
    if(pts.length>1)el('path',{{d:g({{type:'LineString',coordinates:pts}}),fill:'none',stroke:'{AC}','stroke-width':6,'stroke-dasharray':'14 10'}});}}
  const pin=(ll,txt,r)=>{{const xy=p(ll);if(!xy||d3.geoDistance(ll,c)>1.5)return;
    el('circle',{{cx:xy[0],cy:xy[1],r:r,fill:'{AC}',stroke:'#fff','stroke-width':4}});
    const tx=el('text',{{x:xy[0]+28,y:xy[1]+14,class:'pin'}});tx.textContent=txt;}};
  pin(MAT,'Mataró',14);
  if(t>8.8)pin(BAR,'Barossa Valley',18);
  el('text',{{x:110,y:1500,fill:'#ffffff88','font-size':22,'font-family':'Inter'}}).textContent='Mapa: Natural Earth';
}};
</script>''' + TAIL
render(html, BASE + '/para-revisar/05-uva-mataro-australia/reel_uva_mapa', 15.5, 11.5, js=True)
