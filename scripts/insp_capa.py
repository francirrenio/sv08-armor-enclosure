import pickle,numpy as np
P=pickle.load(open('parts.pkl','rb'))
def g(k):
    v=P[k]; return v
import trimesh
for kc in ('u_capa74','u_tcCapa','u_capa74_E','u_tcCapa_E'):
    if kc not in P: print('no',kc); continue
    m=P[kc]; m=m if isinstance(m,trimesh.Trimesh) else m
    print(kc, np.round(m.bounds,1).tolist() if hasattr(m,'bounds') else type(m))
