# PARAFUSOS DAS VERDES DA COLUNA: no lugar dos furos das verdes (centrados na parte visivel de cada verde)
#  - verde de baixo: visivel de Y 94 a 298 (centro 196) -> Y 126 e 266 (antes os parafusos e os pilotos da espinha estavam em 126 e 236)
#  - verde de cima:  visivel de Y 354 a 523 (centro 438,5) -> Y 383,5 e 493,5 (antes 384 e 494)
#  - lateral em Z 256,2 e frente em X 261,25; M3x8 cabeca abaulada com rosca no piloto de 2,5 da espinha
#  - pilotos antigos da espinha fechados com o perfil da propria peca
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
from shapely.ops import unary_union
CT=pickle.load(open('CT.pkl','rb'))
YV=(126.0,266.0,383.5,493.5); YANT=(236.0,384.0,494.0)
def secy(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,_=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float))
    return unary_union([p for p in p2.polygons_full])
def ext_xz(pg,y0,y1):
    ms=[]
    for g in (pg.geoms if hasattr(pg,'geoms') else [pg]):
        mm=trimesh.creation.extrude_polygon(g,y1-y0); mm.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
        if mm.volume<0: mm.invert()
        ms.append(mm)
    return U(*ms)
def fecha(m,y,caixa,yref):
    pr=ext_xz(secy(m,yref),y-2.5,y+2.5)
    return U(m,I(pr,caixa))
pick=lambda m:max(m.split(only_watertight=False),key=lambda q:q.volume)
for k in ('espinha_lat_inf','espinha_lat_sup'):
    m=CT[k]
    for y in YANT:
        if m.bounds[0][1]<y<m.bounds[1][1]: m=fecha(m,y,B(272.5,280.0,y-2.5,y+2.5,253.0,259.5),y+7.0)
    m=D(m,*[CYL([272.0,y,256.2],[285.0,y,256.2],2.5) for y in YV if m.bounds[0][1]+3<y<m.bounds[1][1]-3])
    CT[k]=pick(m)
for k in ('espinha_fre_inf','espinha_fre_sup'):
    m=CT[k]
    for y in YANT:
        if m.bounds[0][1]<y<m.bounds[1][1]: m=fecha(m,y,B(258.0,264.5,y-2.5,y+2.5,275.5,282.0),y+7.0)
    m=D(m,*[CYL([261.25,y,275.0],[261.25,y,287.0],2.5) for y in YV if m.bounds[0][1]+3<y<m.bounds[1][1]-3])
    CT[k]=pick(m)
def bolt(p,axis,Lg,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*Lg,d))
HW=[bolt([283.8,y,256.2],[1,0,0],8) for y in YV]+[bolt([261.25,y,286.0],[0,0,1],8) for y in YV]
HW+=[bolt([276.4,y,244.0],[1,0,0],8,hd=5.5,hh=3.0) for y in (110,126)]
CT['hw_verdes']=trimesh.util.concatenate(HW)
chk={}
for i,h in enumerate(HW[:8]):
    for k in ('verde_72','verde_sup','espinha_lat_inf','espinha_lat_sup','espinha_fre_inf','espinha_fre_sup'):
        v=I(h,CT[k]).volume
        if v>0.01: chk['p%d_%s'%(i,k)]=v
chk['ok']=float(all(CT[k].is_volume for k in ('espinha_lat_inf','espinha_lat_sup','espinha_fre_inf','espinha_fre_sup')))
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}))
pickle.dump(CT,open('CT.pkl','wb'))
