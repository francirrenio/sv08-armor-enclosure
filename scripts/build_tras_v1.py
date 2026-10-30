# TRASEIRA DO TOP HAT (T2 aprovada): parede preta (Y 523-634, face Z -286) com 2 janelas de aletas iguais as da lateral
# (138 x 44, centro X +-127, Y 574-618), hexagono verde central (moldura) com a tampa preta do servo dentro, e verdes dos lados
# com a ponta para o centro abracando as aletas. Preto num nivel so, verdes 0,5 acima, friso 0,6. Construida como "frente"
# (face +286) e espelhada em Z no fim.
import numpy as np, trimesh, json, pickle
exec(open('load.py').read()); MESH=M; exec(open('geo.py').read()); exec(open('geo_ch2.py').read())
from shapely.geometry import box as sbox, Polygon, Point
from shapely.ops import unary_union as uu
_pxy=prism_xy
def prism_xy(poly,z0,z1):
    poly=poly.buffer(0); gs=[g for g in (poly.geoms if hasattr(poly,'geoms') else [poly]) if g.area>0.05]
    ms=[_pxy(g,z0,z1) for g in gs]; return ms[0] if len(ms)==1 else U(*ms)
_fv=open('frente_versoes.py').read(); exec(_fv.split('VERS=[')[0])          # hexa, op, bf, K, R, M, fit
CT=pickle.load(open('CT.pkl','rb')); F={}; LOG={}
TD_='/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/'
_c=trimesh.load(TD_+'054.stl'); _s=section_polys(_c,'z',-290.0); cap=max((_s.geoms if hasattr(_s,'geoms') else [_s]),key=lambda q:q.area); caps=uu([cap,M(cap)])
ZF1=286.0; ZFL=282.8; ZG0=283.0; ZP0=279.0; ZI=ZF1-1.5
XW=235.2; YW0=523.0; YW1=634.0; GAPV=4.0
YG0,YG1=563.0,629.0
JAN=[sbox(xc-69,574.0,xc+69,618.0) for xc in (-127.0,127.0)]           # aberturas das aletas (iguais as da lateral)
hexT=hexa(-40.0,40.0,YG0,YG1)
TAMPA=op(sbox(-26,580,26,612),2.0)                                     # tampa preta do servo (dentro do hexagono)
JS=op(sbox(-14,584,14,608),1.5)                                        # janela de acesso ao servo, atras da tampa
ladD=maior(op(sbox(0,YG0,300,YG1).difference(bf(hexT,GAPV)).difference(bf(caps,GAPV)),R))
ladD=Polygon(ladD.exterior.coords,[bf(JAN[1],2.0).exterior.coords]); ladE=M(ladD)
hexF=Polygon(hexT.exterior.coords,[bf(TAMPA,0.5).exterior.coords])
NG={'verde_tras_hex':hexF,'verde_tras_D':ladD,'verde_tras_E':ladE}
GS=[(-33.0,596.0),(33.0,596.0)]+[(s*x,y) for s in (1,-1) for x,y in ((214.0,572.0),(214.0,620.0),(127.0,567.5),(127.0,624.5))]
TS=[(-20.0,596.0),(20.0,596.0)]
def verde(poly):
    m=D(prism_xy(poly,ZG0,ZF1+0.5),chamfer_cutter(poly,'z',ZF1+0.5,1.0))
    for x,y in [p for p in GS if poly.contains(Point(p))]: m=D(m,CYL([x,y,ZG0-1],[x,y,ZF1+1],3.4))
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
for k,p in NG.items(): F[k]=verde(p)
tam=D(prism_xy(TAMPA,ZFL+0.2,ZF1),chamfer_cutter(TAMPA,'z',ZF1,0.8))
for x,y in TS: tam=D(tam,CYL([x,y,ZFL],[x,y,ZF1+1],3.4))
F['tampa_servo_tras']=tam
REC=uu([bf(Polygon(p.exterior),0.5) for p in NG.values()])
def tong(x,yc): return Polygon([(x+0.2,yc-3),(x+0.2,yc+3),(x-4.5,yc+4.5),(x-4.5,yc-4.5)])
TT=[tong(0.0,570.0),tong(0.0,621.0)]                                   # rabo de andorinha da emenda, escondido sob o hexagono
def parede(poly,dono):
    m=prism_xy(poly,ZP0,ZF1); m=chamfer_top(m,'z',ZF1,1.25)
    m=D(m,prism_xy(REC.intersection(poly.buffer(2)),ZFL,ZF1+5))
    c1=chamfer_cutter(poly.buffer(6).difference(REC),'z',ZF1,0.6)
    if c1 is not None: m=D(m,c1)
    for j in JAN: m=D(m,prism_xy(j,ZP0-1,ZF1+1))
    m=D(m,prism_xy(JS,ZP0-1,ZF1+1))
    if dono: m=U(m,*[prism_xy(t,ZP0,ZFL) for t in TT])
    else: m=D(m,*[prism_xy(t.buffer(0.2,join_style=2),ZP0-1,ZFL+0.01) for t in TT])
    for x,y in [p for p in GS+TS if poly.buffer(-1).contains(Point(p))]: m=D(m,CYL([x,y,ZP0+0.8],[x,y,ZF1+1],2.5))
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
F['parede_tras_E']=parede(sbox(-XW,YW0,-0.1,YW1),False)
F['parede_tras_D']=parede(sbox(0.1,YW0,XW,YW1),True)
def bolt(p,axis,L,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*L,d))
F['ferragens_tras']=U(*[bolt([x,y,ZF1+0.5],[0,0,1],6) for x,y in GS]+[bolt([x,y,ZF1],[0,0,1],6) for x,y in TS])
# aletas: as mesmas da lateral, giradas para a traseira (lateral D: face X 284 -> traseira face Z 286 antes do espelho)
Ry=trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0])           # (x,y,z)->(z,y,-x)
al=[]
for k in ('riser47_aletas','riser35_aletas'):
    q=CT[k].copy(); q.apply_transform(Ry); q.apply_translation([0,0,-2.0])
    if q.volume<0: q.invert()
    al.append(q)
F['aletas_tras_pre']=U(*al)
# espelho em Z -> traseira
Mz=np.diag([1,1,-1,1])
for k in list(F.keys()):
    q=F[k].copy()
    if k!='aletas_tras_pre':
        q.apply_transform(Mz)
        if q.volume<0: q.invert()
    F[k.replace('_pre','')]=q
del F['aletas_tras_pre']
# conferencias
TL=pickle.load(open('TL.pkl','rb'))
viz={'cant54':_c,'cant54E':None,'sup51':trimesh.load(TD_+'051.stl'),'riser35':CT['riser35'],'bandaA':CT['bandaA'],'colTD':CT.get('coluna_TD_ext') if 'coluna_TD_ext' in CT else None}
def esp(m):
    q=m.copy(); q.apply_transform(np.diag([-1,1,1,1]));
    if q.volume<0: q.invert()
    return q
viz['cant54E']=esp(_c); viz['sup51E']=esp(viz['sup51']); viz['riser35E']=esp(CT['riser35'])
DS=pickle.load(open('DS.pkl','rb')); viz['frame']=DS['frame2020']
chk={}
for a in ('parede_tras_E','parede_tras_D','verde_tras_hex','verde_tras_D','verde_tras_E','tampa_servo_tras','aletas_tras'):
    for b,v in viz.items():
        if v is None: continue
        try: x=I(F[a],v).volume
        except Exception as e: x=str(e)[:20]
        if not isinstance(x,float) or x>0.01: chk[a+'_x_'+b]=x
for a in ('verde_tras_hex','verde_tras_D','verde_tras_E','tampa_servo_tras','aletas_tras'):
    for b in ('parede_tras_E','parede_tras_D'):
        x=I(F[a],F[b]).volume
        if x>0.01: chk[a+'_x_'+b]=round(x,2)
LOG['chk']=chk; LOG['vol']={k:bool(v.is_volume) for k,v in F.items()}; LOG['tam']={k:round(float(max(v.extents)),1) for k,v in F.items()}
LOG['b']={k:np.round(v.bounds,1).tolist() for k,v in F.items()}
pickle.dump(F,open('TR.pkl','wb')); print(json.dumps(LOG,default=str))
