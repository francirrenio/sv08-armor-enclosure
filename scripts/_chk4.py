import pickle,numpy as np
CT=pickle.load(open('CT.pkl','rb'))
for p in CT['verde_sup'].split(only_watertight=False): print(round(p.volume,2),np.round(p.bounds,1).tolist())
