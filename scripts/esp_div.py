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
# EMENDA_MEIO: as 2 pecas azuis divididas em Y 345 (escondido sob a cantoneira do meio, Y 298-354), com rabo de andorinha
#  - a peca de cima tem a espiga (desce 10 mm: largura 10 na emenda, 14 na ponta); a de baixo, o encaixe com folga de 0,2
#  - a espiga atravessa a espessura da perna: monta deslizando a peca de cima de lado (lateral: em X; frente: em Z)
#  - fica entre os parafusos da cantoneira do meio (Y 324) e a emenda; tudo coberto pela cantoneira
from shapely.geometry import Polygon as _Pg
YS=345.0; DV=10.0
def _cauda(c): return _Pg([(c-5.0,YS),(c+5.0,YS),(c+7.0,YS-DV),(c-7.0,YS-DV)])
def _emenda(p,cauda,ext):
    sup=U(I(p,B(0,400,YS,800,-400,400)),I(p,ext(cauda)))
    inf=D(I(p,B(0,400,0,YS,-400,400)),ext(cauda.buffer(0.2,join_style=2)))
    pick=lambda m:max(m.split(only_watertight=False),key=lambda q:q.volume)
    return pick(inf),pick(sup)
li,ls=_emenda(lat,_cauda(247.0),lambda pg:prism_zy(pg,272.0,281.0))
fi,fs=_emenda(fre,_cauda(254.0),lambda pg:prism_xy(pg,275.0,283.0) if prism_xy(pg,275.0,283.0).volume>0 else prism_xy(pg,275.0,283.0))
c2={'li':li.volume,'ls':ls.volume,'fi':fi.volume,'fs':fs.volume,'soma_lat':li.volume+ls.volume-lat.volume,'soma_fre':fi.volume+fs.volume-fre.volume,
    'li_x_ls':I(li,ls).volume,'fi_x_fs':I(fi,fs).volume,'len':[float(np.ptp(m.bounds[:,1])) for m in (li,ls,fi,fs)],'ok':all(m.is_volume for m in (li,ls,fi,fs))}
print(json.dumps({k:(round(float(v),2) if not isinstance(v,(list,bool)) else v) for k,v in c2.items()}))
CT['espinha_lat_inf'],CT['espinha_lat_sup'],CT['espinha_fre_inf'],CT['espinha_fre_sup']=li,ls,fi,fs
pickle.dump(CT,open('CT.pkl','wb'))
