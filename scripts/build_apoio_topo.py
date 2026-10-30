# APOIO_TOPO_LAT: apoio do acrilico no topo da lateral refeito inteiro (o espelho deixava um vao de 31 mm em Z 0).
# Perfil constante de Z -208 a 208 + espigas das pontas (iguais as da peca da frente), furo do parafuso original em Z 0,
# emenda em Z 60 (desencontrada 60 mm da emenda da banda em Z 0) com rabo de andorinha atravessando a espessura.
import numpy as np, trimesh, json, pickle
exec(open('geo.py').read())
from shapely.geometry import Polygon
TL=pickle.load(open('TL.pkl','rb')); A=TL['apoio_A']; Bp=TL['apoio_B']
Mz=np.diag([1,1,-1,1])
def mz(m):
    q=m.copy(); q.apply_transform(Mz)
    if q.volume<0: q.invert()
    return q
X0,X1=265.0,277.5; Y0,Y1=523.0,558.0
P=section_polys(Bp,'z',40.0)
def pz(poly,z0,z1):
    m=trimesh.creation.extrude_polygon(poly,z1-z0); m.apply_translation([0,0,z0])
    if m.volume<0: m.invert()
    return m
def zy(poly,x0,x1):            # poligono (z,y) extrudado em X
    m=trimesh.creation.extrude_polygon(poly,x1-x0); m.apply_transform(np.array([[0,0,1,x0],[0,1,0,0],[1,0,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
full=U(I(Bp,B(X0,X1,Y0,Y1,25.0,250.0)),I(mz(Bp),B(X0,X1,Y0,Y1,-250.0,-25.0)),pz(P,-25.0,25.0))
furo=D(pz(P,-3.5,3.5),I(A,B(X0,X1,Y0,Y1,-3.5,3.5)))        # furo do parafuso original em Z 0 (o mesmo da peca A)
full=D(full,furo)
ZS=60.0; yc=0.5*(P.bounds[1]+P.bounds[3])
tg=Polygon([(ZS+0.2,yc-3),(ZS+0.2,yc+3),(ZS-4.5,yc+4.5),(ZS-4.5,yc-4.5)])
tgc=Polygon([(ZS+0.2,yc-3.2),(ZS+0.2,yc+3.2),(ZS-4.7,yc+4.7),(ZS-4.7,yc-4.7)])
F=U(I(full,B(X0-1,X1+1,Y0-1,Y1+1,ZS,300)),I(full,zy(tg,X0-1,X1+1)))
T=D(I(full,B(X0-1,X1+1,Y0-1,Y1+1,-300,ZS)),zy(tgc,X0-1,X1+1))
big=lambda m:max(m.split(only_watertight=False),key=lambda q:q.volume)
R={'apoio_F':big(F),'apoio_T':big(T)}
Pp=pickle.load(open('parts.pkl','rb')); chk={}
for k,m in R.items():
    for pid,lab,grp,pm in Pp:
        if grp not in ('prop','comum') or pid in ('apB','tcApoio','apHW','tcHW'): continue
        try:
            if not (np.all(pm.bounds[0]<m.bounds[1]) and np.all(m.bounds[0]<pm.bounds[1])): continue
            x=I(m,pm).volume
        except Exception as e: x=str(e)[:20]
        if not isinstance(x,float) or x>0.01: chk[k+'_x_'+pid]=x
chk['F_x_T']=round(I(R['apoio_F'],R['apoio_T']).volume,3)
print(json.dumps({'chk':chk,'vol':{k:bool(v.is_volume) for k,v in R.items()},'b':{k:np.round(v.bounds,1).tolist() for k,v in R.items()},
  'vfull_vs_orig':[round(full.volume),round(Bp.volume+mz(Bp).volume)]},default=str))
pickle.dump(R,open('AP.pkl','wb'))
