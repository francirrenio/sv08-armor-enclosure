import pickle,numpy as np
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
pts=np.array([[282.0,15.0,-150.0],[282.0,15.0,150.0],[282.0,15.0,-80.0]])
for D_,nm in ((RL,'RL'),(CT,'CT')):
  for k,m in D_.items():
    if hasattr(m,'contains') and hasattr(m,'bounds') and m.bounds is not None:
      try:
        c=m.contains(pts)
        if c.any(): print(nm,k,c)
      except Exception as e: pass
