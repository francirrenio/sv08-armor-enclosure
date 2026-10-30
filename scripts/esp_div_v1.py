# ESPINHA EM 2 PECAS: sai a quina (canto X > 268 e Z > 271, a altura toda) e abre um canal de cabos no canto da coluna
#  - lateral: X 273-283,8, Z 220,1-271 (presa no perfil pelos 2 parafusos de fabrica da aba lateral e nos ressaltos do top hat)
#  - frente:  X 235,4-268, Z 276-286 (em cima presa no suporte do top hat pelos parafusos da cantoneira do topo; no resto,
#             pelas verdes e pelas cantoneiras, que sao aparafusadas nas 2 pecas)  -> fixacao propria a decidir
#  - canal de cabos: entre o perfil (canto chanfrado) e as verdes, ~12 x 12 mm + o vao atras da perna lateral, de Y 81 ate o topo
import numpy as np, pickle, trimesh, json
exec(open('load.py').read()); exec(open('geo.py').read())
CT=pickle.load(open('CT.pkl','rb'))
e=CT['espinha']; V0=e.volume
lat=I(e,B(272.5,295.0,0.0,700.0,200.0,271.0))
fre=I(e,B(220.0,268.0,0.0,700.0,271.5,300.0))
canto=I(e,D(B(200,300,0,700,200,300),B(272.5,295.0,0.0,700.0,200.0,271.0),B(220.0,268.0,0.0,700.0,271.5,300.0)))
hw=None
lat=max(lat.split(only_watertight=False),key=lambda p:p.volume); fre=max(fre.split(only_watertight=False),key=lambda p:p.volume)
chk={'v0':V0,'lat':lat.volume,'fre':fre.volume,'canto':canto.volume,'lat_len':float(np.ptp(lat.bounds[:,1])),'fre_len':float(np.ptp(fre.bounds[:,1]))}
pf=M['Corpo1@072.stl']; p01=M['65_suporte_P01_D']
for nm,m in (('perfil',pf),('p01',p01),('v72',CT['verde_72']),('vsup',CT['verde_sup']),('capa',pickle.load(open('CF.pkl','rb'))['capa_74']),('cantTop',CT['cant_top_F']),('sup',CT['supF'])):
    for pn,pm in (('lat',lat),('fre',fre)):
        try:
            mm=m if m.is_volume else m.convex_hull
            v=I(pm,mm).volume
        except Exception as ex: v=-1
        if v!=0: chk[pn+'_x_'+nm]=v
chk['ok']=float(lat.is_volume and fre.is_volume)
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}))
CT['espinha_lat']=lat; CT['espinha_fre']=fre; 
pickle.dump(CT,open('CT.pkl','wb'))
