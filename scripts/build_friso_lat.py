# FRISO_4_LADOS: o trilho de rasgos da frente (Y 540-554, 6 mm para fora, rasgos de 4 a cada 10, pontas 45 graus)
# continua nas bandas pretas das laterais (face X 283,8). Termina 10 mm antes do canto, como na frente; rasgo em Z 0 cobre a emenda.
import numpy as np, trimesh, json, pickle
exec(open('geo.py').read())
from shapely.geometry import Polygon
CT=pickle.load(open('CT.pkl','rb')); TC=pickle.load(open('TC.pkl','rb'))
XF=283.8; YR0,YR1=540.0,554.0; ZR=210.0
prof=Polygon([(XF-0.1,542.5),(XF+2.5,YR0),(XF+4.0,YR0),(XF+6.0,YR0+2.0),(XF+6.0,YR1-2.0),(XF+4.0,YR1),(XF+2.5,YR1),(XF-0.1,YR1-2.5)])
def prism_xy_z(poly,z0,z1):
    m=trimesh.creation.extrude_polygon(poly,z1-z0); m.apply_translation([0,0,z0])
    if m.volume<0: m.invert()
    return m
rail=prism_xy_z(prof,0.0,ZR)
w=Polygon([(XF-1,ZR),(XF+7.0,ZR),(XF+7.0,ZR-8.0)])                 # ponta 45 graus (x,z)
cut=trimesh.creation.extrude_polygon(w,YR1-YR0+2); cut.apply_transform(np.array([[1,0,0,0],[0,0,1,YR0-1],[0,1,0,0],[0,0,0,1]],float))
if cut.volume<0: cut.invert()
rail=D(rail,cut)
for z in np.arange(0.0,191.0,10.0): rail=D(rail,B(XF+3.5,XF+7,YR0-1,YR1+1,z-2.0,z+2.0))
bF=U(CT['bandaB'],rail)
bT=bF.copy(); bT.apply_transform(np.diag([1,1,-1,1]))
if bT.volume<0: bT.invert()
R={'banda_F':bF,'banda_T':bT}
P=pickle.load(open('parts.pkl','rb'))
chk={}
for k,m in R.items():
    for pid,lab,grp,pm in P:
        if grp not in ('prop','comum') or pid in ('bandaB','tcBanda'): continue
        try:
            if not (np.all(pm.bounds[0]<m.bounds[1]) and np.all(m.bounds[0]<pm.bounds[1])): continue
            x=I(m,pm).volume
        except Exception as e: x=str(e)[:20]
        if not isinstance(x,float) or x>0.01: chk[k+'_x_'+pid]=x
print(json.dumps({'chk':chk,'vol':{k:bool(v.is_volume) for k,v in R.items()},'b':{k:np.round(v.bounds,1).tolist() for k,v in R.items()},
  'dTC':round(float(abs(TC['banda'].volume-CT['bandaB'].volume)),2)},default=str))
pickle.dump(R,open('BR.pkl','wb'))
