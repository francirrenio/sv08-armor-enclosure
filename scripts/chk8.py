import pickle,numpy as np
exec(open('geo.py').read())
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
for nm,p in (('old',RL['placa_A']),('new',CT['R_placa_A'])):
  for x in (281.0,282.0,282.5,283.0,283.4,283.7):
    ys=np.arange(45,54,0.05); pts=np.c_[np.full_like(ys,x),ys,np.full_like(ys,-140)]
    c=p.contains(pts); 
    print(nm,x,'top recess edge Y=',round(ys[np.argmax(c)],2))
for nm,p in (('old',RL['verde_braco_T']),('new',CT['R_verde_braco_T'])):
  for x in (281.0,283.0,283.4,283.7):
    ys=np.arange(45,54,0.05); pts=np.c_[np.full_like(ys,x),ys,np.full_like(ys,-140)]
    c=p.contains(pts); print(nm,'arm',x,round(ys[len(c)-1-np.argmax(c[::-1])],2))
