# Precalcula alt/az (ephem) de Leo, radiante y estrellas de fondo desde Mataró
import ephem, math, json, random
o=ephem.Observer(); o.lat='41.5381'; o.lon='2.4447'; o.elevation=10; o.pressure=0
LEO={'Regulus':('10:08:22','11:58'),'Eta':('10:07:20','16:46'),'Algieba':('10:19:58','19:50'),'Adhafera':('10:16:41','23:25'),
 'Rasalas':('9:52:46','26:00'),'Epsilon':('9:45:51','23:46'),'Zosma':('11:14:06','20:31'),'Chertan':('11:14:14','15:26'),'Denebola':('11:49:04','14:34')}
MAG={'Regulus':1.4,'Eta':3.5,'Algieba':2.0,'Adhafera':3.4,'Rasalas':3.9,'Epsilon':3.0,'Zosma':2.6,'Chertan':3.3,'Denebola':2.1}
LINES=[('Regulus','Eta'),('Eta','Algieba'),('Algieba','Adhafera'),('Adhafera','Rasalas'),('Rasalas','Epsilon'),
 ('Algieba','Zosma'),('Zosma','Denebola'),('Denebola','Chertan'),('Chertan','Regulus'),('Zosma','Chertan')]
random.seed(7)
bg=[]
for i in range(900):
    ra=random.uniform(0,24); dec=math.degrees(math.asin(random.uniform(-1,1)))
    bg.append((ephem.hours(ra*math.pi/12), ephem.degrees(math.radians(dec)), random.random()))
def body(ra,dec):
    b=ephem.FixedBody(); b._ra=ephem.hours(ra) if isinstance(ra,str) else ra; b._dec=ephem.degrees(dec) if isinstance(dec,str) else dec; b._epoch=ephem.J2000; return b
# horas locales: 00:45 -> 05:00 (UT = local-1)
times=[]; T0=ephem.Date('2026/11/17 23:45')
for k in range(18): times.append(ephem.Date(T0+k*15*ephem.minute))
out={'t_local':[],'leo':{n:[] for n in LEO},'rad':[],'bg':[[] for _ in bg],'lines':LINES,'mag':MAG}
for t in times:
    o.date=t
    lt=ephem.Date(t+ephem.hour).datetime(); out['t_local'].append(lt.strftime('%H:%M'))
    for n,(ra,dec) in LEO.items():
        b=body(ra,dec); b.compute(o); out['leo'][n].append([round(math.degrees(b.az),2),round(math.degrees(b.alt),2)])
    b=body('10:08','22'); b.compute(o); out['rad'].append([round(math.degrees(b.az),2),round(math.degrees(b.alt),2)])
    for j,(ra,dec,m) in enumerate(bg):
        b=body(ra,dec); b.compute(o); out['bg'][j].append([round(math.degrees(b.az),2),round(math.degrees(b.alt),2)])
out['bgm']=[round(m,3) for _,_,m in bg]
json.dump(out,open('sky.json','w'))
print(out['t_local'][0],out['rad'][0],out['t_local'][-1],out['rad'][-1])
