# TOPO_FRENTE (T3 ajustado, aprovado no desenho): parede preta acima da porta (Y 532,5-634) com trilho de acessorios
# (perfil rabo de andorinha, rasgos a cada 10 mm) logo acima da porta, hexagono verde central e verdes laterais (vao 7 mm,
# 10 mm de preto no topo). Preto num nivel so (face Z 286), verdes 0,5 acima, friso 0,6 em volta dos rebaixos.
# Parede em 2 metades (emenda em X 0, dentro de um rasgo do trilho e sob o hexagono; rabo de andorinha escondido).
import numpy as np, trimesh, json, pickle
exec(open('load.py').read()); MESH=M; exec(open('geo.py').read()); exec(open('geo_ch2.py').read())
from shapely.geometry import box as sbox, Polygon, Point
from shapely.ops import unary_union as uu
_pxy=prism_xy
def prism_xy(poly,z0,z1):
    poly=poly.buffer(0); gs=[g for g in (poly.geoms if hasattr(poly,'geoms') else [poly]) if g.area>0.05]
    ms=[_pxy(g,z0,z1) for g in gs]; return ms[0] if len(ms)==1 else U(*ms)
def prism_xz(poly,y0,y1):   # poligono (x,z) extrudado em Y
    m=trimesh.creation.extrude_polygon(poly,y1-y0); m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
_fv=open('frente_versoes.py').read(); exec(_fv.split('VERS=[')[0])          # hexa, op, bf, K, R, M
CT=pickle.load(open('CT.pkl','rb')); F={}; LOG={}
_s=section_polys(CT['cant_top_F'],'z',290.0); cap=max((_s.geoms if hasattr(_s,'geoms') else [_s]),key=lambda q:q.area); caps=uu([cap,M(cap)])
ZF1=286.0; ZFL=282.8; ZG0=283.0; ZP0=279.0
XW=235.2; YW0=532.5; YW1=634.0; GV=7.0
YR0,YR1=540.0,554.0; XR=225.0
YG0,YG1=YR1+GV,YW1-10.0
# ---------- verdes ----------
hexT=hexa(-112.0,112.0,YG0,YG1)
ladD=maior(op(sbox(0,YG0,300,YG1).difference(bf(hexT,GV)).difference(bf(caps,GV)),R)); ladE=M(ladD)
NG={'verde_topo_centro':hexT,'verde_topo_D':ladD,'verde_topo_E':ladE}
GS=[(-80.0,YG0+8),(80.0,YG0+8),(-80.0,YG1-8),(80.0,YG1-8),(155.0,YG0+9),(205.0,YG1-9),(-155.0,YG0+9),(-205.0,YG1-9)]
GS=[p for p in GS if any(g.buffer(-4.5).contains(Point(p)) for g in NG.values())]
def verde(poly):
    m=D(prism_xy(poly,ZG0,ZF1+0.5),chamfer_cutter(poly,'z',ZF1+0.5,1.0))
    for x,y in [p for p in GS if poly.contains(Point(p))]: m=D(m,CYL([x,y,ZG0-1],[x,y,ZF1+1],3.4))
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
for k,p in NG.items(): F[k]=verde(p)
# ---------- trilho (perfil (z,y), extrudado em X) ----------
prof=Polygon([(285.9,542.5),(288.5,YR0),(290.0,YR0),(292.0,YR0+2.0),(292.0,YR1-2.0),(290.0,YR1),(288.5,YR1),(285.9,YR1-2.5)])
rail=prism_zy(prof,-XR,XR)
for s_ in (1,-1):   # pontas em 45 graus
    w=Polygon([(s_*XR,285.0),(s_*XR,293.0),(s_*(XR-8.0),293.0)]) if s_>0 else Polygon([(-XR,285.0),(-XR+8.0,293.0),(-XR,293.0)])
    w=Polygon([(s_*(XR+1),285.0),(s_*(XR+1),293.5),(s_*(XR-7.0),293.5),(s_*(XR-0.0),286.5)])
    rail=D(rail,prism_xz(w,YR0-1,YR1+1))
XS=[x for x in np.arange(-210.0,211.0,10.0)]                                   # rasgos de 4 mm a cada 10 mm (um deles em X 0, na emenda)
for x in XS: rail=D(rail,B(x-2.0,x+2.0,YR0-1,YR1+1,289.5,294.0))
# ---------- parede preta (2 metades) ----------
REC=uu([bf(p,0.5) for p in NG.values()])
def tong(x,yc): return Polygon([(x+0.2,yc-3),(x+0.2,yc+3),(x-4.5,yc+4.5),(x-4.5,yc-4.5)])
TT=[tong(0.0,575.0),tong(0.0,610.0)]
# FIXACAO: parafusos por tras (estrutura escondida -> insertos na parede), nas faixas pretas cheias (trilho e topo)
RS=[(x,y) for y in (547.0,629.0) for x in (-200.0,-100.0,-25.0,25.0,110.0,200.0)]
def parede(poly,dono):
    m=prism_xy(poly,ZP0,ZF1); m=chamfer_top(m,'z',ZF1,1.25)
    m=D(m,prism_xy(REC.intersection(poly.buffer(2)),ZFL,ZF1+5))
    c1=chamfer_cutter(poly.buffer(6).difference(REC),'z',ZF1,0.6)
    if c1 is not None: m=D(m,c1)
    x0,_,x1,_=poly.bounds
    m=U(m,I(rail,B(x0,x1,YR0-2,YR1+2,284.0,295.0)))
    if dono: m=U(m,*[prism_xy(t,ZP0,ZFL) for t in TT])
    else: m=D(m,*[prism_xy(t.buffer(0.2,join_style=2),ZP0-1,ZFL+0.01) for t in TT])
    for x,y in [p for p in GS if poly.buffer(-1).contains(Point(p))]: m=D(m,CYL([x,y,ZP0+0.8],[x,y,ZF1+1],2.5))
    for x,y in [p for p in RS if poly.buffer(-1).contains(Point(p))]: m=D(m,CYL([x,y,ZP0-1],[x,y,ZP0+4.0],4.0))      # inserto M3x4 por tras
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
F['parede_topo_E']=parede(sbox(-XW,YW0,-0.1,YW1),False)
F['parede_topo_D']=parede(sbox(0.1,YW0,XW,YW1),True)
# ---------- ferragens ----------
def bolt(p,axis,L,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*L,d))
# ---------- estrutura escondida (Z 276-279, face reta para a mesa), 2 metades com emenda em X 60 (desencontrada da parede) ----------
FS=pickle.load(open('FUS_SUP.pkl','rb')); TRAV=FS['travessa_topo_frente']; SUPA=FS['SV08_TopHat_Suporte_Trilho_Frente_A_Black']; SUPB=FS['SV08_TopHat_Suporte_Trilho_Frente_B_Black']
ZS0=276.0; XE=60.0; YB=588.7
BOSS=[(-188.9,266.1),(16.1,266.1),(188.9,266.1)]           # parafuso M3 por dentro do top hat, pelos furos dos suportes do trilho da frente
PADS=[-150.0,-60.0,65.0,155.0]                               # encostos na face da travessa (Z 273,5)
TE=[tong(XE,575.0),tong(XE,610.0)]
def estr(poly,dono):
    m=prism_xy(poly,ZS0,ZP0)
    x0,_,x1,_=poly.bounds
    a,b=max(x0,-220.0),min(x1,220.0)
    m=U(m,B(a,b,558.2,561.0,266.2,ZS0+0.05))                                      # aba: apoia em cima da travessa (Y 558)
    for x in PADS:
        if x0+9<x<x1-9: m=U(m,B(x-8,x+8,535.0,552.0,273.7,ZS0+0.05))
    for x,zt in BOSS:
        if x0+5<x<x1-5:
            m=U(m,CYL([x,YB,ZS0+0.05],[x,YB,zt],9.0)); m=D(m,CYL([x,YB,zt-0.1],[x,YB,zt+5.8],4.0),CYL([x,YB,zt],[x,YB,ZP0+1],3.4))
    if dono: m=U(m,*[prism_xy(t,ZS0,ZP0) for t in TE])
    else: m=D(m,*[prism_xy(t.buffer(0.2,join_style=2),ZS0-1,ZP0+0.01) for t in TE])
    for x,y in [p for p in RS if poly.buffer(-1).contains(Point(p))]:
        m=D(m,CYL([x,y,ZS0-1],[x,y,ZP0+1],3.4),CONE([x,y,ZS0-0.01],[x,y,ZS0+1.7],6.4,3.0) if 'CONE' in globals() else CYL([x,y,ZS0-1],[x,y,ZS0+1.7],6.2))
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
F['estr_topo_E']=estr(sbox(-XW,YW0,XE-0.1,YW1),False)
F['estr_topo_D']=estr(sbox(XE+0.1,YW0,XW,YW1),True)
F['ferragens_topo']=U(*[bolt([x,y,ZF1+0.5],[0,0,1],6) for x,y in GS]+[bolt([x,y,ZS0+1.7],[0,0,-1],6,hd=6.0,hh=1.7) for x,y in RS]+
                      [bolt([x,YB,255.6],[0,0,-1],16) for x,_ in BOSS])
# ---------- conferencias ----------
P=pickle.load(open('P.pkl','rb'))
viz={'travessa':TRAV,'supA':SUPA,'supB':SUPB,'porta_mold2':CT['porta_mold2'],'porta_mold1':CT['porta_mold1'],'cant_top_F':CT['cant_top_F'],'espinha_fre_sup':CT['espinha_fre_sup'],'supF':CT['supF'],
     'dobradicas':CT['dobradicas'],'acr_porta':P['SV-30-01b acrilico (proposta)'],'riser47':CT['riser47'],'bandaB':CT['bandaB'],'perfil':MESH['Corpo1@072.stl']}
chk={}
for a in ('parede_topo_E','parede_topo_D','estr_topo_E','estr_topo_D','verde_topo_centro','verde_topo_D','verde_topo_E'):
    for b,v in viz.items():
        for vv in (v,):
            for mir in (False,True):
                w=vv
                if mir: w=vv.copy(); w.apply_transform(np.diag([-1,1,1,1])); w.invert() if w.volume<0 else None
                try: x=I(F[a],w).volume
                except Exception as e: x=str(e)[:30]
                if not isinstance(x,float) or x>0.01: chk[a+'_x_'+b+('_E' if mir else '')]=x
for a in ('verde_topo_centro','verde_topo_D','verde_topo_E'):
    for b in ('parede_topo_E','parede_topo_D'):
        x=I(F[a],F[b]).volume
        if x>0.01: chk[a+'_x_'+b]=round(x,2)
chk['E_x_D']=round(I(F['parede_topo_E'],F['parede_topo_D']).volume,3); chk['eE_x_eD']=round(I(F['estr_topo_E'],F['estr_topo_D']).volume,3)
for a in ('estr_topo_E','estr_topo_D'):
    for b in ('parede_topo_E','parede_topo_D','verde_topo_centro','verde_topo_D','verde_topo_E'):
        x=I(F[a],F[b]).volume
        if x>0.01: chk[a+'_x_'+b]=round(x,2)
F['ref_travessa']=TRAV; F['ref_supA']=SUPA; F['ref_supB']=SUPB
LOG['chk']=chk; LOG['vol']={k:bool(v.is_volume) for k,v in F.items()}
LOG['tam']={k:round(float(max(v.extents)),1) for k,v in F.items()}; LOG['GS']=len(GS)
pickle.dump(F,open('TF.pkl','wb')); print(json.dumps(LOG,default=str))
