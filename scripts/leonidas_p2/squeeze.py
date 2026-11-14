import json, numpy as np, wave
w=json.load(open('words.json'))
r=wave.open('voz.wav'); sr=r.getframerate(); ch=r.getnchannels(); x=np.frombuffer(r.readframes(r.getnframes()),np.int16).reshape(-1,ch)
MAXG=0.5; segs=[]; shift=0; cur=0.0; out=[]
for i in range(len(w)):
    out.append([w[i][0]-shift,w[i][1]-shift,w[i][2]])
    if i+1<len(w):
        g=w[i+1][0]-w[i][1]
        if g>MAXG:
            a=w[i][1]+0.25; b=w[i+1][0]-(MAXG-0.25)  # cut [a,b)
            segs.append((cur,a)); cur=b; shift+=b-a
segs.append((cur,len(x)/sr))
y=np.concatenate([x[int(a*sr):int(b*sr)] for a,b in segs])
o=wave.open('voz_c.wav','wb'); o.setnchannels(ch); o.setsampwidth(2); o.setframerate(sr); o.writeframes(y.tobytes()); o.close()
json.dump(out,open('words_c.json','w')); print(len(y)/sr)
