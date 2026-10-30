import pickle,numpy as np,trimesh,glob,os
exec(open('geo.py').read())
S=pickle.load(open('SUPT.pkl','rb')); DS=pickle.load(open('DS.pkl','rb'))
F=DS['frame2020']
# rasgo: pontos no eixo do parafuso dentro do perfil devem estar fora do solido
for x,z in [(-165,255),(40,255),(250,-150),(250,150)]:
    ys=np.arange(623.6,632,0.5); print('rasgo',x,z,''.join('#' if c else '.' for c in F.contains(np.array([[x,y,z] for y in ys]))))
exec(open('chk_ds.py').read().split("for part in ('frame2020','slider'):")[0].split("DS=pickle.load")[0])
