# Música ambiental propia (sin derechos), generada con numpy
import numpy as np, wave
SR=44100; D=32.5; t=np.arange(int(SR*D))/SR
def note(m): return 440*2**((m-69)/12)
def pad(freqs,start,dur,amp=.18):
    y=np.zeros_like(t); i0=int(start*SR); n=int(dur*SR); tt=np.arange(n)/SR
    env=np.minimum(1,tt/2.0)*np.minimum(1,(dur-tt)/2.2); env=np.clip(env,0,1)
    s=np.zeros(n)
    for f in freqs:
        for det in (-0.25,0.25):
            ff=f*2**(det/1200*8)
            s+=np.sin(2*np.pi*ff*tt+0.3*np.sin(2*np.pi*0.2*tt))+0.25*np.sin(4*np.pi*ff*tt)
    s*=env*amp/len(freqs); y[i0:i0+n]+=s[:len(y)-i0]; return y
# Dm9 - Bbmaj7 - Gm9 - A(sus) ... lento, misterioso
ch=[[50,57,62,64,65],[46,53,57,62,65],[43,50,58,62,65],[45,52,57,62,64]]
y=np.zeros_like(t); L=8.0
for k in range(5):
    y+=pad([note(m) for m in ch[k%4]],k*L-0.8 if k else 0,L+2.2)
# grave
y+=0.10*np.sin(2*np.pi*note(38)*t)*np.minimum(1,t/3)
# campanitas suaves (destellos)
rng=np.random.default_rng(3); scale=[74,77,79,81,84,86]
for s0 in np.arange(1.0,D-2,1.7):
    s0+=rng.uniform(-.3,.3); f=note(rng.choice(scale)); n=int(2.5*SR); tt=np.arange(n)/SR
    b=0.05*np.sin(2*np.pi*f*tt)*np.exp(-tt*1.8); i=int(s0*SR); y[i:i+n]+=b[:len(y)-i]
# reverb simple
ir_n=int(2.2*SR); ir=rng.standard_normal(ir_n)*np.exp(-np.arange(ir_n)/SR*2.8); ir/=np.abs(ir).sum()/6
from numpy.fft import rfft, irfft
N=1<<int(np.ceil(np.log2(len(y)+ir_n))); wet=irfft(rfft(y,N)*rfft(ir,N),N)[:len(y)]
y=0.7*y+0.3*wet
fade=np.minimum(1,(D-t)/2.5); y*=np.clip(fade,0,1)
y/=np.abs(y).max()*1.12
st=np.stack([y,np.roll(y,600)],1)
w=wave.open('musica.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes()); w.close(); print('ok')
