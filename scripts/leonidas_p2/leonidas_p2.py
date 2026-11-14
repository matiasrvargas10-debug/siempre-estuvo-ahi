# Leónidas parte 2 — reel 9:16 animado en canvas (Chromium) + voz + música
# Uso: python3 leonidas_p2.py [--nubes "texto AEMET"]
import json, os, sys, asyncio, subprocess
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__)); FPS=30
NUBES = sys.argv[sys.argv.index('--nubes')+1] if '--nubes' in sys.argv else '[ hueco: previsión AEMET del martes ]'
VO=0.3                                   # retardo de la voz
words=json.load(open(D+'/words_c.json')); sky=json.load(open(D+'/sky.json'))
DUR=round(words[-1][1]+VO+1.3,2)
F=D+'/fonts'; I=D+'/fonts'
html=f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;font-weight:400;src:url(file://{F}/fraunces-latin-400-normal.woff2)}}
@font-face{{font-family:Fraunces;font-weight:600;src:url(file://{F}/fraunces-latin-600-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:400;src:url(file://{I}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url(file://{I}/inter-latin-600-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:800;src:url(file://{I}/inter-latin-800-normal.woff2)}}
body{{margin:0;background:#000}}</style></head><body><canvas id=c width=1080 height=1920></canvas>
<script>
const SKY={json.dumps(sky)}, W={json.dumps(words)}, VO={VO}, NUBES={json.dumps(NUBES)};
const OR='#F4A63A', BG='#0F1B2D', HZ=1200, K=9.5;
const c=document.getElementById('c'), x=c.getContext('2d');
// ---------- utilidades
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)), lerp=(a,b,f)=>a+(b-a)*f;
const ease=f=>f<.5?4*f*f*f:1-Math.pow(-2*f+2,3)/2;
const win=(t,a,b,fi=.45,fo=.4)=>cl((t-a)/fi)*cl((b-t)/fo);
function rnd(s){{return()=>{{s=(s*16807)%2147483647;return (s-1)/2147483646}}}}
function txt(s,X,Y,font,col,al='left',alpha=1){{x.save();x.globalAlpha*=alpha;x.font=font;x.fillStyle=col;x.textAlign=al;x.textBaseline='alphabetic';x.fillText(s,X,Y);x.restore()}}
function wrap(s,maxw){{const ws=s.split(' ');let L=[],cur='';for(const w of ws){{const t=cur?cur+' '+w:w;if(x.measureText(t).width>maxw&&cur){{L.push(cur);cur=w}}else cur=t}}L.push(cur);return L}}
// ---------- cielo
function idxAt(t){{ // índice temporal (0=00:45, cada 15 min)
  const a=10.2+VO,b=13.9+VO; if(t<a) return 0; const f=ease(cl((t-a)/(b-a))); return f*12; }}
function sample(arr,f){{const i=Math.min(Math.floor(f),arr.length-2),r=f-i;return [lerp(arr[i][0],arr[i+1][0],r),lerp(arr[i][1],arr[i+1][1],r)]}}
function proj(az,alt,caz){{let d=az-caz; if(d>180)d-=360; if(d<-180)d+=360; return [540+d*K, HZ-alt*K]}}
const M=[]; {{const r=rnd(12345); let tt=0.05; while(tt<32){{ const big=r()<.12;
  M.push({{t:tt,a:r()*Math.PI*2,r0:60+r()*260,len:big?520:180+r()*300,d:big?.9:.45+r()*.35,b:big?1:.55+r()*.4,w:big?5:2.2+r()*1.6}}); tt+=0.35+r()*0.75 }} }}
const CLOUD=[]; {{const r=rnd(99); for(let i=0;i<14;i++) CLOUD.push({{x:r()*1400-200,y:300+r()*800,s:180+r()*260,v:40+r()*60}}) }}
function drawSky(t,f,starBoost,glow){{
  const caz=sample(SKY.rad,f)[0];
  let g=x.createLinearGradient(0,0,0,HZ); g.addColorStop(0,'#060B16'); g.addColorStop(.75,BG); g.addColorStop(1,'#1A2B44');
  x.fillStyle=g; x.fillRect(0,0,1080,HZ);
  // estrellas de fondo
  for(let j=0;j<SKY.bg.length;j++){{ const p=sample(SKY.bg[j],f); if(p[1]<0.5) continue; const [X,Y]=proj(p[0],p[1],caz);
    if(X<-10||X>1090) continue; const m=SKY.bgm[j]; const lim=0.55+0.45*starBoost; if(m>lim) continue;
    const tw=.75+.25*Math.sin(t*3+j); x.globalAlpha=cl((0.35+0.65*(1-m))*tw*(.6+.4*starBoost)*cl(p[1]/6)); x.fillStyle='#fff';
    x.beginPath(); x.arc(X,Y,m<.08?2.2:1.3,0,7); x.fill(); }}
  x.globalAlpha=1;
  // contaminación lumínica (costa)
  if(glow>0){{ let gg=x.createRadialGradient(80,HZ,10,80,HZ,700); gg.addColorStop(0,`rgba(244,166,58,${{.38*glow}})`); gg.addColorStop(1,'rgba(244,166,58,0)'); x.fillStyle=gg; x.fillRect(0,0,1080,HZ);
    gg=x.createRadialGradient(1000,HZ,10,1000,HZ,420); gg.addColorStop(0,`rgba(244,166,58,${{.22*glow}})`); gg.addColorStop(1,'rgba(244,166,58,0)'); x.fillStyle=gg; x.fillRect(0,0,1080,HZ); }}
  return caz;
}}
function leoPts(f,caz){{const P={{}}; for(const n in SKY.leo){{const p=sample(SKY.leo[n],f); P[n]=proj(p[0],p[1],caz)}} return P}}
function drawLeo(P,lineF,labelA){{
  if(lineF>0){{ x.strokeStyle=OR; x.lineWidth=3; x.globalAlpha=.85; const L=SKY.lines;
    for(let i=0;i<L.length;i++){{ const ff=cl(lineF*L.length-i); if(ff<=0) break; const [a,b]=[P[L[i][0]],P[L[i][1]]];
      x.beginPath(); x.moveTo(a[0],a[1]); x.lineTo(lerp(a[0],b[0],ff),lerp(a[1],b[1],ff)); x.stroke(); }} x.globalAlpha=1; }}
  for(const n in P){{ const [X,Y]=P[n]; if(Y>HZ) continue; const r=5.5-SKY.mag[n]; let g=x.createRadialGradient(X,Y,0,X,Y,r*5); g.addColorStop(0,'rgba(255,240,215,.9)'); g.addColorStop(1,'rgba(255,240,215,0)');
    x.fillStyle=g; x.beginPath(); x.arc(X,Y,r*5,0,7); x.fill(); x.fillStyle='#fff'; x.beginPath(); x.arc(X,Y,r*.9,0,7); x.fill(); }}
  if(labelA>0){{ const R=P['Rasalas']; txt('LEO',R[0]+30,R[1]-26,'800 46px Inter',OR,'left',labelA) }}
}}
function drawMeteors(t,rad,cut){{
  for(const m of M){{ const u=(t-m.t)/m.d; if(u<0||u>1.25) continue;
    const head=m.r0+m.len*cl(u), tail=m.r0+m.len*cl(u-.45); const ca=Math.cos(m.a), sa=Math.sin(m.a);
    const hx=rad[0]+ca*head, hy=rad[1]+sa*head, tx=rad[0]+ca*tail, ty=rad[1]+sa*tail;
    if(hy>HZ&&ty>HZ) continue; const al=m.b*cl((1.25-u)/.35)*cut;
    x.save(); x.beginPath(); x.rect(0,0,1080,HZ); x.clip();
    let g=x.createLinearGradient(tx,ty,hx,hy); g.addColorStop(0,'rgba(255,255,255,0)'); g.addColorStop(.7,`rgba(200,225,255,${{.6*al}})`); g.addColorStop(1,`rgba(255,255,255,${{al}})`);
    x.strokeStyle=g; x.lineWidth=m.w; x.lineCap='round'; x.beginPath(); x.moveTo(tx,ty); x.lineTo(hx,hy); x.stroke();
    if(u<=1){{ x.fillStyle=`rgba(255,250,235,${{al}})`; x.beginPath(); x.arc(hx,hy,m.w*.9,0,7); x.fill() }} x.restore(); }}
}}
function drawSea(t,caz,moonX,moonA){{
  let g=x.createLinearGradient(0,HZ,0,1920); g.addColorStop(0,'#13233A'); g.addColorStop(.25,'#0A1424'); g.addColorStop(1,'#03070E');
  x.fillStyle=g; x.fillRect(0,HZ,1080,720);
  x.globalAlpha=.10; x.strokeStyle='#9fb6d6'; x.lineWidth=2;
  for(let i=0;i<26;i++){{ const y=HZ+8+i*i*1.1; const off=Math.sin(t*.8+i)*30; x.beginPath(); x.moveTo(0,y); for(let X=0;X<=1080;X+=40) x.lineTo(X,y+Math.sin(X/90+t*1.2+i)*2.5+off*0); x.stroke() }}
  x.globalAlpha=1; x.fillStyle='rgba(255,255,255,.35)'; x.fillRect(0,HZ,1080,1.5);
  // cardinales en el horizonte
  for(const [az,n] of [[0,'N'],[45,'NE'],[90,'E'],[135,'SE'],[180,'S']]){{ const [X]=proj(az,0,caz); if(X<30||X>1050) continue;
    x.fillStyle='rgba(255,255,255,.5)'; x.fillRect(X-1,HZ,2,14); txt(n,X,HZ+46,'600 28px Inter',n=='E'?OR:'rgba(255,255,255,.6)','center') }}
  if(moonA>0){{ let gg=x.createLinearGradient(0,HZ,0,1500); gg.addColorStop(0,`rgba(255,236,200,${{.35*moonA}})`); gg.addColorStop(1,'rgba(255,236,200,0)');
    x.fillStyle=gg; for(let i=0;i<14;i++){{ const w=40+Math.sin(t*2+i)*25+i*6; x.fillRect(moonX-w/2+Math.sin(t*1.5+i*1.7)*12,HZ+8+i*20,w,4) }} }}
}}
function chip(X,Y,s,font,col,a){{ if(a<=0) return; x.save(); x.globalAlpha=a; x.font=font; const w=x.measureText(s).width;
  x.fillStyle='rgba(6,11,22,.62)'; x.beginPath(); x.roundRect(X-22,Y-50,w+44,70,35); x.fill(); txt(s,X,Y,font,col); x.restore(); }}
function panel(X,Y,w,h,a){{ x.save(); x.globalAlpha=a*.9; x.fillStyle='rgba(6,11,22,.68)'; x.beginPath(); x.roundRect(X,Y,w,h,28); x.fill(); x.restore() }}
// ---------- subtítulos
const CH=[]; {{let cur=[]; for(const w of W){{ cur.push(w); const p=/[.,:?]$/.test(w[2]); if(p||cur.length>=5){{CH.push(cur);cur=[]}} }} if(cur.length) CH.push(cur) }}
function subs(t){{ const tv=t-VO; let k=-1; for(let i=0;i<CH.length;i++) if(tv>=CH[i][0][0]-.05) k=i; if(k<0) return;
  const ch=CH[k], end=(k+1<CH.length?CH[k+1][0][0]-.05:ch[ch.length-1][1]+.6); if(tv>end) return;
  x.font='800 68px Inter'; const parts=ch.map(w=>w[2]); let line=parts.join(' '); let lines=wrap(line,780);
  let y0=1440-(lines.length-1)*42; let wi=0;
  for(const L of lines){{ const lw=x.measureText(L).width; let X=520-lw/2; for(const w of L.split(' ')){{ const on=tv>=ch[wi][0];
      x.lineWidth=12; x.strokeStyle='rgba(3,7,14,.85)'; x.lineJoin='round'; x.strokeText(w,X,y0); x.fillStyle=on?(ch[wi][2].match(/Leo|este|setenta|kilómetros|segundo|quince|superluna|cuarto|una|menos|tarde|mejor/)?OR:'#fff'):'rgba(255,255,255,.45)';
      x.fillText(w,X,y0); X+=x.measureText(w+' ').width; wi++; }} y0+=84; }}
}}
// ---------- frame
window.R=function(t){{
  x.clearRect(0,0,1080,1920);
  const f=idxAt(t), s6=cl((t-(20.1+VO))/2.2), starBoost=s6, glow=1-.8*s6;
  const caz=drawSky(t,f,starBoost,glow);
  const rad=proj(...sample(SKY.rad,f),caz), P=leoPts(f,caz);
  const T8=25.8+VO, moonA=cl((t-T8)/1.2), cloudA=win(t,23.9+VO,T8+.6,.7,.9);
  const leoLine=cl((t-(7.0+VO))/2.2), leoLbl=cl((t-(8.9+VO))/.4);
  drawLeo(P,leoLine*(1-moonA),leoLbl*(1-moonA));
  drawMeteors(t,rad,1-moonA*.85);
  // luna llena (cierre)
  let mx=540,my=lerp(HZ+170,800,ease(cl((t-T8)/2.4)));
  if(moonA>0){{ x.save(); x.globalAlpha=moonA*.9; x.fillStyle='rgba(3,6,12,.55)'; x.fillRect(0,0,1080,HZ); x.restore();
    x.save(); x.beginPath(); x.rect(0,0,1080,HZ); x.clip();
    let g=x.createRadialGradient(mx,my,140,mx,my,420); g.addColorStop(0,`rgba(255,236,200,${{.45*moonA}})`); g.addColorStop(1,'rgba(255,236,200,0)'); x.fillStyle=g; x.fillRect(0,0,1080,HZ);
    g=x.createRadialGradient(mx-40,my-40,20,mx,my,160); g.addColorStop(0,'#FFF8E8'); g.addColorStop(1,'#E9D9B8'); x.fillStyle=g; x.globalAlpha=moonA; x.beginPath(); x.arc(mx,my,160,0,7); x.fill();
    x.fillStyle='rgba(150,135,110,.28)'; for(const [a,b,r] of [[-50,-30,38],[30,20,30],[-10,60,22],[55,-55,20],[-70,40,16]]){{x.beginPath();x.arc(mx+a,my+b,r,0,7);x.fill()}}
    x.restore(); }}
  // nubes
  if(cloudA>0){{ for(const cdat of CLOUD){{ const X=cdat.x+(t-23.9-VO)*cdat.v; const g=x.createRadialGradient(X,cdat.y,0,X,cdat.y,cdat.s);
     g.addColorStop(0,`rgba(120,132,152,${{.55*cloudA}})`); g.addColorStop(1,'rgba(120,132,152,0)'); x.fillStyle=g; x.fillRect(X-cdat.s,cdat.y-cdat.s,cdat.s*2,cdat.s*2) }} }}
  drawSea(t,caz,mx,moonA);
  txt('Simulación · lluvia acelerada',110,1610,'400 22px Inter','rgba(255,255,255,.4)');
  // cabecera
  txt('MATARÓ · MARTES 17 NOV',110,190,'600 30px Inter',OR);
  txt('Leónidas · parte 2',110,270,'400 66px Fraunces','#fff');
  // S2 reloj -> 00:45
  {{ const a=win(t,3.5+VO,6.9+VO); if(a>0){{ const p=ease(cl((t-3.7-VO)/2.0)); const mins=21*60+p*(3*60+45); const hh=Math.floor(mins/60)%24, mm=Math.floor(mins%60);
    panel(90,340,820,330,a); x.save(); x.globalAlpha=a;
    txt(String(hh).padStart(2,'0')+':'+String(mm).padStart(2,'0'),130,500,'600 128px Fraunces',OR);
    txt('máximo · noche del 17 al 18',134,570,'400 32px Inter','#fff'); txt('(hora de Mataró)',134,620,'400 28px Inter','rgba(255,255,255,.6)');
    const cx=770,cy=505,R=118; x.strokeStyle='rgba(255,255,255,.85)'; x.lineWidth=5; x.beginPath(); x.arc(cx,cy,R,0,7); x.stroke();
    for(let i=0;i<12;i++){{const an=i/12*Math.PI*2; x.lineWidth=i%3?3:6; x.beginPath(); x.moveTo(cx+Math.sin(an)*(R-18),cy-Math.cos(an)*(R-18)); x.lineTo(cx+Math.sin(an)*(R-6),cy-Math.cos(an)*(R-6)); x.stroke()}}
    const ha=(mins/60%12)/12*Math.PI*2, ma=(mins%60)/60*Math.PI*2; x.lineCap='round';
    x.lineWidth=9; x.strokeStyle='#fff'; x.beginPath(); x.moveTo(cx,cy); x.lineTo(cx+Math.sin(ha)*62,cy-Math.cos(ha)*62); x.stroke();
    x.lineWidth=6; x.strokeStyle=OR; x.beginPath(); x.moveTo(cx,cy); x.lineTo(cx+Math.sin(ma)*96,cy-Math.cos(ma)*96); x.stroke();
    x.fillStyle=OR; x.beginPath(); x.arc(cx,cy,9,0,7); x.fill(); x.restore(); }} }}
  // S3 brújula + flecha a Leo
  {{ const a=win(t,6.8+VO,10.4+VO); if(a>0){{ x.save(); x.globalAlpha=a; const cx=210,cy=1300,R=62;
    x.strokeStyle='rgba(255,255,255,.8)'; x.lineWidth=3; x.beginPath(); x.arc(cx,cy,R,0,7); x.stroke();
    for(const [an,n] of [[0,'N'],[90,'E'],[180,'S'],[270,'O']]){{ const r=an*Math.PI/180; txt(n,cx+Math.sin(r)*(R+24),cy-Math.cos(r)*(R+24)+10,'600 26px Inter',n=='E'?OR:'#fff','center') }}
    const sp=ease(cl((t-6.9-VO)/1.0)); const an=lerp(-60,90,sp)*Math.PI/180; x.fillStyle=OR; x.beginPath();
    x.moveTo(cx+Math.sin(an)*(R-8),cy-Math.cos(an)*(R-8)); x.lineTo(cx+Math.sin(an+2.7)*20,cy-Math.cos(an+2.7)*20); x.lineTo(cx+Math.sin(an-2.7)*20,cy-Math.cos(an-2.7)*20); x.fill();
    txt('ESTE · sobre el mar',320,1312,'600 38px Inter','#fff');
    const R0=P['Regulus']; const ah=cl((t-7.6-VO)/.8); if(ah>0){{ x.strokeStyle=OR; x.lineWidth=4; x.setLineDash([12,10]); x.beginPath(); x.moveTo(R0[0]+40,HZ-6); x.lineTo(R0[0]+40,lerp(HZ-6,R0[1]-120,ah)); x.stroke(); x.setLineDash([]) }}
    x.restore(); }} }}
  // S4 timelapse
  {{ const a=win(t,10.2+VO,14.3+VO); if(a>0){{ const fi=Math.min(Math.round(f),17); const p=sample(SKY.rad,f);
    panel(90,340,820,300,a); x.save(); x.globalAlpha=a;
    txt(SKY.t_local[fi],130,490,'600 120px Fraunces',OR); txt('Leo a '+Math.round(p[1])+'° de altura',470,445,'600 40px Inter','#fff');
    txt('más alto = más estrellas fugaces',470,495,'400 28px Inter','rgba(255,255,255,.7)');
    txt('La luna se pone a las 00:36 → cielo oscuro',130,595,'400 32px Inter','#fff'); x.restore(); }} }}
  // S5 15/h y 71 km/s
  {{ const a=win(t,14.2+VO,15.9+VO); if(a>0){{ panel(90,340,820,300,a); x.save(); x.globalAlpha=a;
     txt('15',130,540,'600 190px Fraunces',OR); txt('por hora, como máximo',400,450,'600 40px Inter','#fff'); txt('con cielo oscuro y Leo alto',400,505,'400 30px Inter','rgba(255,255,255,.7)'); x.restore() }} }}
  {{ const a=win(t,15.9+VO,20.3+VO); if(a>0){{ panel(90,340,820,320,a); x.save(); x.globalAlpha=a; const rows=[['Sonido','0,34 km/s',.34],['Estación Espacial','7,7 km/s',7.7],['Leónidas','71 km/s',71]];
     rows.forEach((r,i)=>{{ const y=405+i*90, g=ease(cl((t-16.1-VO-i*.55)/1.0)); txt(r[0],130,y,'600 34px Inter',i==2?OR:'#fff'); txt(r[1],870,y,'600 34px Inter',i==2?OR:'#fff','right');
       x.fillStyle='rgba(255,255,255,.15)'; x.fillRect(130,y+20,740,22); x.fillStyle=i==2?OR:'#fff'; x.fillRect(130,y+20,Math.max(4,740*r[2]/71*g),22) }});
     x.restore() }} }}
  // S6 consejos
  {{ const a=win(t,20.1+VO,23.9+VO); if(a>0){{ panel(90,340,820,300,a); x.save(); x.globalAlpha=a;
     txt('Lejos de las luces',130,430,'600 52px Fraunces','#fff'); txt('y sin mirar el móvil',130,485,'400 32px Inter','rgba(255,255,255,.75)');
     const p=cl((t-21.2-VO)/2.4); const cx=760,cy=500; x.lineWidth=12; x.strokeStyle='rgba(255,255,255,.15)'; x.beginPath(); x.arc(cx,cy,90,0,7); x.stroke();
     x.strokeStyle=OR; x.lineCap='round'; x.beginPath(); x.arc(cx,cy,90,-Math.PI/2,-Math.PI/2+p*Math.PI*2); x.stroke();
     txt('~30',cx,cy+14,'600 56px Fraunces','#fff','center'); txt('min',cx,cy+50,'400 24px Inter','rgba(255,255,255,.7)','center');
     txt('para que tus ojos se acostumbren',130,590,'400 32px Inter','#fff'); x.restore() }} }}
  // S7 nubes / AEMET
  {{ const a=win(t,23.9+VO,25.9+VO); if(a>0){{ panel(90,340,820,240,a); x.save(); x.globalAlpha=a;
     txt('¿Y SI HAY NUBES?',130,420,'600 30px Inter',OR); txt('Previsión AEMET · martes 17',130,480,'600 40px Inter','#fff');
     x.font='400 34px Inter'; wrap(NUBES,740).slice(0,2).forEach((L,i)=>txt(L,130,535+i*44,'400 34px Inter','rgba(255,255,255,.85)')); x.restore() }} }}
  // S8 superluna
  {{ const a=win(t,25.8+VO,28.3+VO); if(a>0){{ x.save(); x.globalAlpha=a; txt('24 NOV',540,450,'600 44px Inter',OR,'center'); txt('Superluna',540,560,'400 110px Fraunces','#fff','center');
     txt('luna llena a 360.765 km',540,620,'400 32px Inter','rgba(255,255,255,.75)','center'); x.restore() }} }}
  // S9 pregunta
  {{ const a=cl((t-28.2-VO)/.5); if(a>0){{ x.save(); x.globalAlpha=a; txt('¿Vas a salir a verlas?',540,440,'400 76px Fraunces','#fff','center');
     txt('SÍ o NO',540,580,'600 130px Fraunces',OR,'center'); txt('Síguenos · @siempre.estuvo.ahi',540,650,'400 32px Inter','rgba(255,255,255,.75)','center'); x.restore() }} }}
  subs(t);
}};
</script></body></html>'''
async def main(out):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        tmp=out+'.html'; open(tmp,'w').write(html); await pg.goto('file://'+tmp)
        for fnt in ['400 40px Fraunces','600 40px Fraunces','400 40px Inter','600 40px Inter','800 40px Inter']: await pg.evaluate(f"document.fonts.load('{fnt}')")
        await pg.evaluate('document.fonts.ready')
        if '--frames' in sys.argv:
            for tt in [float(v) for v in sys.argv[sys.argv.index('--frames')+1].split(',')]:
                await pg.evaluate(f'window.R({tt})'); await pg.locator('canvas').screenshot(path=f'{out}_f{tt:05.1f}.png')
            await b.close(); return
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out+'_mudo.mp4'],stdin=subprocess.PIPE)
        for k in range(int(FPS*DUR)):
            await pg.evaluate(f'window.R({k/FPS})'); ff.stdin.write(await pg.locator('canvas').screenshot(type='jpeg',quality=92))
        ff.stdin.close(); ff.wait()
        await pg.evaluate('window.R(9.6)'); await pg.locator('canvas').screenshot(path=out+'_portada.png')
        await b.close()
out=os.path.abspath(D+'/../../para-revisar/leonidas-parte2/reel_leonidas_parte2')
asyncio.run(main(out))
if '--frames' not in sys.argv:
    # voz (retardo VO) + música al ~18 % por debajo
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',out+'_mudo.mp4','-i',D+'/voz_c.wav','-i',D+'/musica.wav','-filter_complex',
     f'[1:a]adelay={int(VO*1000)}|{int(VO*1000)},aformat=channel_layouts=stereo,loudnorm=I=-16:TP=-1.5[v];[2:a]atrim=0:{DUR},volume=0.18[m];[v][m]amix=inputs=2:duration=first:normalize=0,apad,atrim=0:{DUR}[a]',
     '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart','-t',str(DUR),out+'.mp4'],check=True)
    os.remove(out+'_mudo.mp4'); print('listo',out+'.mp4',DUR)
