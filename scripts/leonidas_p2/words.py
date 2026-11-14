import json;a=json.load(open('align.json'));c=a['characters'];s=a['character_start_times_seconds'];e=a['character_end_times_seconds']
w='';st=None;out=[];en=0
for ch,t0,t1 in zip(c,s,e):
  if ch==' ':
    if w: out.append([round(st,2),round(en,2),w])
    w='';continue
  if not w: st=t0
  w+=ch; en=t1
out.append([round(st,2),round(en,2),w]);json.dump(out,open('words.json','w'));print([(x[0],x[2]) for x in out])
