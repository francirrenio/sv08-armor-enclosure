import pickle,numpy as np
exec(open('geo.py').read())
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
a=RL['placa_A']; b=CT['R_placa_A']
pts=np.array([[x,15,-150] for x in np.arange(277,284,0.25)])
print(a.contains(pts).astype(int)); print(b.contains(pts).astype(int))
for x in (281.5,282.0,282.5,283.0):
    print(x, round(section_polys(a,'x',x).area,1), round(section_polys(b,'x',x).area,1))
