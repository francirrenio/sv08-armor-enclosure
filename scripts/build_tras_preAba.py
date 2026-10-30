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
TAMPA=op(sbox(-26,580,26,612),2.0)                                     # ilha preta dentro do hexagono (enfeite: atras nao tem servo)
ladD=maior(op(sbox(0,YG0,300,YG1).difference(bf(hexT,GAPV)).difference(bf(caps,GAPV)),R))
ladD=Polygon(ladD.exterior.coords,[bf(JAN[1],2.0).exterior.coords]); ladE=M(ladD)
hexF=Polygon(hexT.exterior.coords,[bf(TAMPA,0.5).exterior.coords])
NG={'verde_tras_hex':hexF,'verde_tras_D':ladD,'verde_tras_E':ladE}
GS=[(-33.0,596.0),(33.0,596.0)]+[(s*x,y) for s in (1,-1) for x,y in ((214.0,572.0),(214.0,620.0),(127.0,567.5),(127.0,624.5))]
TS=[]
RS=[(x,y) for y in (538.0,553.0) for x in (-200.0,-100.0,-25.0,25.0,110.0,200.0)]   # insertos M3x4 por tras (estrutura escondida)
def verde(poly):
    m=D(prism_xy(poly,ZG0,ZF1+0.5),chamfer_cutter(poly,'z',ZF1+0.5,1.0))
    for x,y in [p for p in GS if poly.contains(Point(p))]: m=D(m,CYL([x,y,ZG0-1],[x,y,ZF1+1],3.4))
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
for k,p in NG.items(): F[k]=verde(p)
# (sem tampa: a ilha preta faz parte da parede)
REC=uu([bf(Polygon(p.exterior),0.5) for p in NG.values()])
_Ry=trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0])
_al=[]
for _k in ('riser47_aletas','riser35_aletas'):
    _q=CT[_k].copy(); _q.apply_transform(_Ry); _q.apply_transform(np.diag([1,1,-1,1])); _q.apply_translation([0,0,2.0])
    if _q.volume<0: _q.invert()
    _al.append(_q)
ALETAS=U(*_al)
ZI=ZF1-1.5
def prism_xz(poly,y0,y1):   # poligono (x,z) extrudado em Y
    m=trimesh.creation.extrude_polygon(poly,y1-y0); m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
YR0,YR1=540.0,554.0; XR=225.0
# ---------- trilho (perfil (z,y), extrudado em X) ----------
prof=Polygon([(285.9,542.5),(288.5,YR0),(290.0,YR0),(292.0,YR0+2.0),(292.0,YR1-2.0),(290.0,YR1),(288.5,YR1),(285.9,YR1-2.5)])
rail=prism_zy(prof,-XR,XR)
for s_ in (1,-1):   # pontas em 45 graus
    w=Polygon([(s_*XR,285.0),(s_*XR,293.0),(s_*(XR-8.0),293.0)]) if s_>0 else Polygon([(-XR,285.0),(-XR+8.0,293.0),(-XR,293.0)])
    w=Polygon([(s_*(XR+1),285.0),(s_*(XR+1),293.5),(s_*(XR-7.0),293.5),(s_*(XR-0.0),286.5)])
    rail=D(rail,prism_xz(w,YR0-1,YR1+1))
XS=[x for x in np.arange(-210.0,211.0,10.0)]                                   # rasgos de 4 mm a cada 10 mm (um deles em X 0, na emenda)
for x in XS: rail=D(rail,B(x-2.0,x+2.0,YR0-1,YR1+1,289.5,294.0))
def tong(x,yc): return Polygon([(x+0.2,yc-3),(x+0.2,yc+3),(x-4.5,yc+4.5),(x-4.5,yc-4.5)])
TT=[tong(0.0,570.0),tong(0.0,621.0)]                                   # rabo de andorinha da emenda, escondido sob o hexagono
def parede(poly,dono):
    m=prism_xy(poly,ZP0,ZF1); m=chamfer_top(m,'z',ZF1,1.25)
    m=D(m,prism_xy(REC.intersection(poly.buffer(2)),ZFL,ZF1+5))
    c1=chamfer_cutter(poly.buffer(6).difference(REC),'z',ZF1,0.6)
    if c1 is not None: m=D(m,c1)
    x0,_,x1,_=poly.bounds
    m=U(m,I(rail,B(x0,x1,YR0-2,YR1+2,284.0,295.0)))                      # FRISO_4_LADOS: mesmo trilho da frente
    for j in JAN: m=D(m,prism_xy(j,ZP0+1.5,ZF1+1))                       # aletas de enfeite: bolso de 5,5 com fundo de 1,5
    m=U(m,I(ALETAS,prism_xy(uu(JAN),ZP0,ZF1)))
    if poly.buffer(-1).intersects(TAMPA): m=U(m,D(prism_xy(TAMPA.intersection(poly),ZFL-0.01,ZI),chamfer_cutter(TAMPA,'z',ZI,0.6)))   # ilha 1,5 abaixo da face
    for x,y in [p for p in RS if poly.buffer(-1).contains(Point(p))]: m=D(m,CYL([x,y,ZP0-1],[x,y,ZP0+4.0],4.0))
    if dono: m=U(m,*[prism_xy(t,ZP0,ZFL) for t in TT])
    else: m=D(m,*[prism_xy(t.buffer(0.2,join_style=2),ZP0-1,ZFL+0.01) for t in TT])
    for x,y in [p for p in GS+TS if poly.buffer(-1).contains(Point(p))]: m=D(m,CYL([x,y,ZP0+0.8],[x,y,ZF1+1],2.5))
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
XWP=242.0                                                              # PAREDE_SOB_CANTONEIRA: a ponta da parede entra 6,5 mm por baixo da cantoneira (como o riser na lateral)
F['parede_tras_E']=parede(sbox(-XWP,YW0,-0.1,YW1),False)
F['parede_tras_D']=parede(sbox(0.1,YW0,XWP,YW1),True)
def bolt(p,axis,L,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*L,d))
# ---------- estrutura escondida (Z 276-279, face reta para a mesa), 2 metades com emenda em X 60 (desencontrada da parede) ----------
FS=pickle.load(open('FUS_SUP.pkl','rb')); TRAV=FS['travessa_topo_frente']; SUPA=FS['SV08_TopHat_Suporte_Trilho_Frente_A_Black']; SUPB=FS['SV08_TopHat_Suporte_Trilho_Frente_B_Black']
ZS0=276.0; XE=60.0; YB=588.7
BOSS=[]                                                    # SEM_TORRES: as 3 torres (Y 588,7) sairam; a estrutura prende nos suportes so pela nervura           # parafuso M3 por dentro do top hat, pelos furos dos suportes do trilho da frente
PADS=[-150.0,-60.0,65.0,155.0]
# ENCAIXE_BARRA: nervura na estrutura, encostada na barra de cima dos suportes do trilho (Y 612-623,4), 4 parafusos M3x16 por tras
YN0,YN1=613.0,622.5; XN=190.0; YNS=617.7
SN=[(-150.0,YNS),(-75.0,YNS),(-15.0,YNS),(15.0,YNS),(75.0,YNS),(150.0,YNS)]   # 6 parafusos na horizontal pela barra de cima                               # encostos na face da travessa (Z 273,5)
TE=[tong(XE,575.0),tong(XE,610.0)]
def estr(poly,dono):
    m=prism_xy(poly,ZS0,ZP0)
    x0,_,x1,_=poly.bounds
    a,b=max(x0,-220.0),min(x1,220.0)
    m=U(m,B(a,b,558.2,561.0,266.2,ZS0+0.05))                                      # aba: apoia em cima da travessa (Y 558)
    for x in PADS:
        if x0+9<x<x1-9: m=U(m,B(x-8,x+8,535.0,552.0,273.7,ZS0+0.05))
    na,nb=max(x0,-XN),min(x1,XN)
    if nb>na: m=U(m,B(na,nb,YN0,YN1,266.1,ZS0+0.05))                                 # nervura (encaixe na barra dos suportes)
    for x,y in SN:
        if x0+5<x<x1-5: m=D(m,CYL([x,y,266.0],[x,y,266.1+5.8],4.0),CYL([x,y,266.0],[x,y,ZP0-0.5],3.4))
    for x,zt in BOSS:
        if x0+5<x<x1-5:
            m=U(m,CYL([x,YB,ZS0+0.05],[x,YB,zt],9.0)); m=D(m,CYL([x,YB,zt-0.1],[x,YB,zt+5.8],4.0),CYL([x,YB,zt],[x,YB,ZP0+1],3.4))
    if dono: m=U(m,*[prism_xy(t,ZS0,ZP0) for t in TE])
    else: m=D(m,*[prism_xy(t.buffer(0.2,join_style=2),ZS0-1,ZP0+0.01) for t in TE])
    for x,y in [p for p in RS if poly.buffer(-1).contains(Point(p))]:
        m=D(m,CYL([x,y,ZS0-1],[x,y,ZP0+1],3.4),CONE([x,y,ZS0-0.01],[x,y,ZS0+1.7],6.4,3.0) if 'CONE' in globals() else CYL([x,y,ZS0-1],[x,y,ZS0+1.7],6.2))
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
F['estr_tras_E']=estr(sbox(-XW,YW0,XE-0.1,YW1),False)
F['estr_tras_D']=estr(sbox(XE+0.1,YW0,XW,YW1),True)
F['ferragens_tras']=U(*[bolt([x,y,ZF1+0.5],[0,0,1],6) for x,y in GS]+[bolt([x,y,ZS0+1.7],[0,0,-1],6,hd=6.0,hh=1.7) for x,y in RS]+[bolt([x,y,255.6],[0,0,-1],16) for x,y in SN])
S3=pickle.load(open('SUP3.pkl','rb'))
F['ref_travessa_tras']=TRAV.copy()
for k in ('f_E','f_C','f_D','hw_frente'): F['sup_tras_'+k]=S3[k].copy()            # suportes do trilho de tras = espelho dos da frente (mesmas medidas no Fusion)

# espelho em Z -> traseira
Mz=np.diag([1,1,-1,1])
for k in list(F.keys()):
    q=F[k].copy()
    q.apply_transform(Mz)
    if q.volume<0: q.invert()
    F[k]=q
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
for a in ('parede_tras_E','parede_tras_D','verde_tras_hex','verde_tras_D','verde_tras_E','estr_tras_E','estr_tras_D'):
    for b,v in viz.items():
        if v is None: continue
        try: x=I(F[a],v).volume
        except Exception as e: x=str(e)[:20]
        if not isinstance(x,float) or x>0.01: chk[a+'_x_'+b]=x
for a in ('verde_tras_hex','verde_tras_D','verde_tras_E'):
    for b in ('parede_tras_E','parede_tras_D'):
        x=I(F[a],F[b]).volume
        if x>0.01: chk[a+'_x_'+b]=round(x,2)
for a in ('estr_tras_E','estr_tras_D'):
    for b in ('parede_tras_E','parede_tras_D','ref_travessa_tras','sup_tras_f_E','sup_tras_f_C','sup_tras_f_D','verde_tras_hex','verde_tras_D','verde_tras_E'):
        x=I(F[a],F[b]).volume
        if x>0.01: chk[a+'_x_'+b]=round(x,2)
chk['eE_x_eD']=round(I(F['estr_tras_E'],F['estr_tras_D']).volume,3)
LOG['chk']=chk; LOG['vol']={k:bool(v.is_volume) for k,v in F.items()}; LOG['tam']={k:round(float(max(v.extents)),1) for k,v in F.items()}
LOG['b']={k:np.round(v.bounds,1).tolist() for k,v in F.items()}
pickle.dump(F,open('TR.pkl','wb')); print(json.dumps(LOG,default=str))
