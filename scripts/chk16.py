import pickle,numpy as np
from shapely.geometry.polygon import orient
RL=pickle.load(open('RL.pkl','rb'))
PG,PN=pickle.load(open('cv2d.pkl','rb'))
for k,pg in PG.items():
    r=orient(pg,1.0).exterior; L=r.length; res=[]
    for s in np.arange(0,L,1.5):
        a=np.array(r.interpolate(s).coords[0]); b=np.array(r.interpolate(s+0.3).coords[0]); t=(b-a)/np.linalg.norm(b-a)
        n=np.array([t[1],-t[0]])   # fora (CCW -> direita e fora)
        ds=np.arange(0.05,1.6,0.01); P=a+np.outer(ds,n)
        for p in (RL['placa_A'],RL['placa_B']):
            c=p.contains(np.c_[np.full(len(ds),282.0),P[:,1],P[:,0]])
            if c.any(): res.append(ds[np.argmax(c)]); break
    res=np.array(res); print(k,len(res),np.round(np.percentile(res,[10,50,90]),3) if len(res) else None)
