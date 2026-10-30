# CANTONEIRA DO MEIO: quinas das pontas no padrao das dobradicas
#  - as 4 quinas das pontas (lateral em Z 220 e frente em X 235,5; Y 298 e 354) cortadas a 45 graus em toda a espessura (6 mm)
#  - chanfro de 45 graus de 6 mm na face de fora acompanhando tambem as quinas cortadas (sem ponta viva)
#  - a ponta da frente passa a ter o mesmo chanfro de 6 mm da lateral e de cima/baixo (antes 4,5)
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read()); exec(open('geo_ch2.py').read())
from shapely.geometry import Polygon
CF=pickle.load(open('CF.pkl','rb'))
c=CF['capa_74']; Y0,Y1=298.0,354.0; K=6.0; CH=6.0
def cont(u0,u1):   # contorno da face com as quinas da ponta (u0) cortadas
    return Polygon([(u0,Y0+K),(u0+K,Y0),(u1,Y0),(u1,Y1),(u0+K,Y1),(u0,Y1-K)])
# lateral: face X 293,3, contorno em (z,y); a borda do lado da quina grande (Z 270) nao entra
cl=chamfer_cutter(cont(220.0,270.0),'x',293.3,CH,skip=lambda p,q: p[0]>269.9 and q[0]>269.9)
# frente: face Z 295,5, contorno em (x,y)
cf=chamfer_cutter(cont(235.5,270.0),'z',295.5,CH,skip=lambda p,q: p[0]>269.9 and q[0]>269.9)
tri=lambda u0,s: Polygon([(u0-1,Y0-1),(u0+K+1,Y0-1),(u0-1,Y0+K+1)]) if s<0 else Polygon([(u0-1,Y1+1),(u0+K+1,Y1+1),(u0-1,Y1-K-1)])
clips=[prism_zy(tri(220.0,s),282.0,295.0) for s in (-1,1)]+[prism_xy(tri(235.5,s),284.0,297.0) for s in (-1,1)]
c2=D(c,cl,cf,*clips)
c2=max(c2.split(only_watertight=False),key=lambda p:p.volume)
CT=pickle.load(open('CT.pkl','rb'))
chk={'dv':c.volume-c2.volume,'ok':float(c2.is_volume)}
for k in ('verde_72','verde_sup','espinha_lat_inf','espinha_fre_inf','espinha_lat_sup','espinha_fre_sup'):
    if k in CT: chk[k]=I(c2,CT[k]).volume
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}))
CF['capa_74']=c2; pickle.dump(CF,open('CF.pkl','wb'))
