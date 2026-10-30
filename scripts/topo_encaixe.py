# ENCAIXE DO PAINEL LATERAL SOB A BANDA (sai o fecho de cima)
#  - o acrilico sobe 4 mm (topo Y 529,3 -> 533,3) e entra num rebaixo por baixo da banda do topo (X 277,0-280,9, Y ate 533,7)
#  - parede de fora do rebaixo = a propria banda (2,9 mm ate a face X 283,8); parede de dentro = apoios do acrilico (X 277,3)
#  - boca do rebaixo com chanfro de 0,8 na parede de fora para guiar o acrilico
#  - montagem: encaixar o topo do acrilico no rebaixo com o painel inclinado, empurrar a parte de baixo e fechar os 4 fechos
#    (para tirar: abrir os fechos, puxar a parte de baixo e baixar o painel)
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
from shapely.geometry import Polygon
CT=pickle.load(open('CT.pkl','rb')); TL=pickle.load(open('TL.pkl','rb'))
Y0,Y1,XI,XO=529.0,533.7,277.0,280.9
def prism_xy_z(poly,z0,z1):
    m=trimesh.creation.extrude_polygon(poly,z1-z0); m.apply_translation([0,0,z0])
    if m.volume<0: m.invert()
    return m
chf=Polygon([(XO-0.01,529.4),(XO+0.8,529.4),(XO+0.8,529.5),(XO,530.3),(XO-0.01,530.3)])
for k,(z0,z1) in (('bandaA',(-210.7,0.5)),('bandaB',(-0.5,220.5))):
    b=D(CT[k],B(XI,XO,Y0,Y1,z0,z1),prism_xy_z(chf,z0,z1))
    CT[k]=max(b.split(only_watertight=False),key=lambda p:p.volume)
# acrilico: o topo sobe 4 mm (mesmo contorno do topo atual)
a=TL['acrilico']
s=a.section(plane_origin=[0,529.0,0],plane_normal=[0,1,0])
p2,_=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-529.0],[0,0,0,1]],float))
ext=[]
for g in p2.polygons_full:
    m=trimesh.creation.extrude_polygon(g,533.3-529.0)
    m.apply_transform(np.array([[1,0,0,0],[0,0,1,529.0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    ext.append(m)
a2=U(I(a,B(200,300,0,529.1,-300,300)),*ext)
CT['acrilico_lat']=max(a2.split(only_watertight=False),key=lambda p:p.volume)
parts=pickle.load(open('parts.pkl','rb')); P={p[0]:p[3] for p in parts}
chk={}
for k in ('bandaA','bandaB'):
    chk[k+'_x_acr']=I(CT[k],CT['acrilico_lat']).volume
for k in ('apA','apB','fbS','esp1','acS','molS1','apHW','riser47','riser35'):
    m=P[k] if k in P else CT[k]
    if m.is_volume: chk['acr_x_'+k]=I(CT['acrilico_lat'],m).volume
chk['acr_bounds']=float(CT['acrilico_lat'].bounds[1][1]); chk['ok']=float(all(CT[k].is_volume for k in ('bandaA','bandaB','acrilico_lat')))
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}))
pickle.dump(CT,open('CT.pkl','wb'))
