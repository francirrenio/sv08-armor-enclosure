import pickle,numpy as np,trimesh
exec(open('load.py').read()); exec(open('geo.py').read()); exec(open('latload.py').read())
RL=pickle.load(open('RL.pkl','rb')); FB=pickle.load(open('FB.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
e=RL['est_meio']; print('est_meio',np.round(e.bounds,2).tolist(),e.is_watertight)
O={'acril_CT':CT['acrilico_lat'],'base':M['Corpo1@071.stl'],'perfil':M['Corpo1@072.stl'],'perfT':L['Corpo1@069.stl']}
for k,v in FB.items(): O['FB_'+k]=v
for k,v in RL.items():
    if k!='est_meio': O['RL_'+k]=v
for k,v in O.items():
    try: vol=I(e,v).volume
    except Exception as ex: vol=str(ex)[:40]
    if not isinstance(vol,float) or vol>0.01: print(k,vol)
print('ok')
