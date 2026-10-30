import pickle,numpy as np,trimesh
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb')); R=pickle.load(open('R4.pkl','rb'))
pt=np.array([283.8,33.8,-90.3])
for nm,Dd in (('RL',RL),('CT',CT),('R4',R)):
  for k,m in Dd.items():
    if isinstance(m,trimesh.Trimesh) and len(m.vertices):
      lo,hi=m.bounds
      if np.all(pt>lo-3) and np.all(pt<hi+3):
        d=np.linalg.norm(m.vertices-pt,axis=1); 
        print(nm,k,round(d.min(),2), np.round(m.vertices[d<3][:6],2).tolist() if (d<3).sum()<40 else (d<3).sum())
