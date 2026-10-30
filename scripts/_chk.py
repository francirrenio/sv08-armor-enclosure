import pickle,numpy as np
exec(open('geo.py').read())
CT=pickle.load(open('CT.pkl','rb'));CF=pickle.load(open('CF.pkl','rb'))
c=CT['cant_top_F']
for k in ('espinha','verde_sup'):
    m=CF[k]; print(k,np.round(m.bounds,1).tolist()); i=I(c,m); print(' inter',np.round(i.bounds,1).tolist())
print([k for k in CF])
