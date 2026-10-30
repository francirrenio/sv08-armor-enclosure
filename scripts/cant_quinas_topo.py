# CANTONEIRA DE CIMA: o mesmo detalhe da cantoneira do meio (capa_quinas.py): as 4 quinas das pontas (lateral em Z 220 e
# frente em X 235,5; Y 523 e 633,6) cortadas a 45 graus em toda a espessura (6 mm) e o chanfro de fora acompanhando o corte.
# A de tras (TD) e o espelho em Z.
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read()); exec(open('geo_ch2.py').read())
from shapely.geometry import Polygon
CT=pickle.load(open('CT.pkl','rb'))
c=CT['cant_top_F']; Y0,Y1=523.0,633.6; K=6.0; CH=5.5
def cont(u0,u1): return Polygon([(u0,Y0+K),(u0+K,Y0),(u1,Y0),(u1,Y1),(u0+K,Y1),(u0,Y1-K)])
diag=lambda p,q: not (abs(p[0]-q[0])>0.5 and abs(p[1]-q[1])>0.5)     # so as arestas novas (diagonais)
cl=chamfer_cutter(cont(220.0,270.0),'x',293.3,CH,skip=diag)
cf=chamfer_cutter(cont(235.5,270.0),'z',295.5,CH,skip=diag)
tri=lambda u0,s: Polygon([(u0-1,Y0-1),(u0+K+1,Y0-1),(u0-1,Y0+K+1)]) if s<0 else Polygon([(u0-1,Y1+1),(u0+K+1,Y1+1),(u0-1,Y1-K-1)])
clips=[prism_zy(tri(220.0,s),282.0,295.0) for s in (-1,1)]+[prism_xy(tri(235.5,s),284.0,297.0) for s in (-1,1)]
c2=max(D(c,*[m for m in (cl,cf) if m is not None],*clips).split(only_watertight=False),key=lambda p:p.volume)
# CHANFRO_INTERNO: o canto de dentro do L ganha o mesmo reforco a 45 graus da cantoneira do meio e da de baixo,
# paralelo a quina chanfrada da verde da coluna (x+z=560,63) com folga de 0,2
_k=560.63+0.2*np.sqrt(2)
gus=trimesh.creation.extrude_polygon(Polygon([(284.25,286.25),(284.25,_k-284.25),(_k-286.25,286.25)]),Y1-Y0)
gus.apply_transform(np.array([[1,0,0,0],[0,0,1,Y0],[0,1,0,0],[0,0,0,1]],float))
if gus.volume<0: gus.invert()
c2=U(c2,gus)
t2=c2.copy(); t2.apply_transform(np.diag([1,1,-1,1]))
if t2.volume<0: t2.invert()
P={p[0]:p[3] for p in pickle.load(open('parts.pkl','rb'))}
chk={'dv':round(c.volume-c2.volume,1),'vol':bool(c2.is_volume)}
for k in ('tfD','riser47','vsup1','espFs','esp1s','hwTopo','thSupF','bandaB','exCamara','exCaixa'):
    x=I(c2,P[k]).volume
    if x>0.05: chk[k]=round(x,2)
print(json.dumps(chk))
pickle.dump({'thCantF':c2,'tcCant':t2},open('CQ.pkl','wb'))
