import pickle,numpy as np
exec(open('geo.py').read())
RL=pickle.load(open('RL.pkl','rb'))
p=RL['placa_A']
for z in (-150,-90,-200):
  for x in (281.0,282.5,283.0,283.5,283.75):
    ys=np.arange(18,26,0.05); c=p.contains(np.c_[np.full_like(ys,x),ys,np.full_like(ys,z)])
    runs=np.flatnonzero(np.diff(c.astype(int)))
    print(z,x,[round(ys[i],2) for i in runs])
# junction region between v3 and arm: Z from -95 to -80 at Y=30, x 282.5
zs=np.arange(-95,-78,0.05)
for x in (282.5,283.7):
    c=p.contains(np.c_[np.full_like(zs,x),np.full_like(zs,30.0),zs]); print('Y30',x,[round(zs[i],2) for i in np.flatnonzero(np.diff(c.astype(int)))])
