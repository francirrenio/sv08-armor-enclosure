# TRASEIRA DE BAIXO (B2a aprovada, hexagono do meio menor): faixa da base atras (Y 0-81, face Z -286), no mesmo padrao da frente:
# placas pretas (Z 279-286 no quadro local) + estruturas escondidas (276-279) com apoios nos bolsos da parte de tras da base,
# hexagono verde central liso (140 x 68), faixas de cima e asas; asa da direita (vista de tras = lado E da impressora, X<0)
# sem bolsao: a tomada AS03 (C14 + fusivel + chave) numa moldura preta 1,5 acima da verde. Construida no quadro da frente e
# espelhada em Z no fim.
import numpy as np, trimesh, json, pickle
exec(open('load.py').read()); MESH=M; exec(open('geo.py').read()); exec(open('geo_ch2.py').read())
from shapely.geometry import box as sbox, Polygon, Point
from shapely.ops import unary_union as uu
_pxy=prism_xy
def prism_xy(poly,z0,z1):
    poly=poly.buffer(0); gs=[g for g in (poly.geoms if hasattr(poly,'geoms') else [poly]) if g.area>0.05]
    ms=[_pxy(g,z0,z1) for g in gs]; return ms[0] if len(ms)==1 else U(*ms)
_fv=open('frente_versoes.py').read(); exec(_fv.split('VERS=[')[0])          # hexa, fit, lados, bolsao, grade, Lr, M, op, bf
F={}; LOG={}
ZF1=286.0; ZFL=282.8; ZG0=283.0; ZI=ZF1-1.5; ZGR=ZI-2.0; ZP0=279.0; ZS0,ZS1=276.0,279.0
RL=pickle.load(open('RL.pkl','rb'))
_s=section_polys(RL['cantoneira_T_L'],'z',-286.35); Lr=max([Polygon(g.exterior) for g in (_s.geoms if hasattr(_s,'geoms') else [_s])],key=lambda q:q.area)
if Lr.centroid.x<0: Lr=M(Lr)
hexc=hexa(-70.0,70.0,4.0,72.0)
lados_v,ilhas=lados(hexc)
supD=[g for g in lados_v if g.centroid.x>0 and g.centroid.y>42][0]; asaD=[g for g in lados_v if g.centroid.x>0 and g.centroid.y<=42][0]
supE=M(supD); asaE0=M(Polygon(asaD.exterior)); ilD=[i for i in ilhas if i.centroid.x>0][0]
# tomada AS03 na asa E: janela 48,5 x 28 e 2 furos a +-28 (a mesma da base original)
xa=asaE0.centroid.x; ya=asaE0.centroid.y
MOL=op(sbox(xa-41,ya-16,xa+41,ya+16),4.0); JAN=op(sbox(xa-24.25,ya-14,xa+24.25,ya+14),0.8)
FT=[(xa-28.0,ya),(xa+28.0,ya)]
asaE=Polygon(asaE0.exterior.coords,[bf(MOL,0.5).exterior.coords])
NG={'verde_central':hexc,'sup_D':supD,'asa_D':asaD,'sup_E':supE,'asa_E':asaE}
LOG['asaE_margem']=[round(MOL.bounds[1]-asaE0.bounds[1],2),round(asaE0.bounds[3]-MOL.bounds[3],2)]
# parafusos aparentes das verdes
def _meio(p,y,xa_,xb_):
    s=p.intersection(sbox(xa_,y-0.01,xb_,y+0.01)); return 0.5*(s.bounds[0]+s.bounds[2])
ys=0.5*(43.0+66.0); bol=Polygon(asaD.interiors[0])
SCc=[(x,y) for x in (-42.0,42.0) for y in (12.0,62.0)]
SCd=[(supD.bounds[0]+26.0,ys),(supD.bounds[2]-30.0,ys),(_meio(asaD,asaD.centroid.y,0,bol.bounds[0]),asaD.centroid.y),(_meio(asaD,asaD.centroid.y,bol.bounds[2],300),asaD.centroid.y)]
SCe=[(-x,y) for x,y in SCd[:2]]+[(_meio(asaE,ya,-300,MOL.bounds[0]-0.5),ya),(_meio(asaE,ya,MOL.bounds[2]+0.5,0),ya)]
GS=SCc+SCd+SCe
_bc=0.5*(bol.bounds[0]+bol.bounds[2]); _ya=asaD.bounds[1]
HIDd=[(40.0,9.0),(40.0,58.0),(_bc-14.0,_ya+3.5),(_bc+14.0,_ya+3.5),(230.0,55.0),(248.0,52.0),(248.0,10.5)]
HIDe=[(-40.0,9.0),(-40.0,58.0),(-230.0,55.0),(-248.0,52.0),(-248.0,10.5)]
HID=HIDd+HIDe
# ---------- verdes ----------
def verde(poly):
    m=D(prism_xy(poly,ZG0,ZF1+0.5),chamfer_cutter(poly,'z',ZF1+0.5,1.0))
    for x,y in [p for p in GS if poly.contains(Point(p))]: m=D(m,CYL([x,y,ZG0-1],[x,y,ZF1+1],3.4))
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
for k,p in NG.items(): F['verde_'+k if not k.startswith('verde') else k]=verde(p)
# ---------- moldura preta da tomada (1,5 acima da verde) ----------
mol=D(prism_xy(MOL,ZFL+0.2,ZF1+2.0),chamfer_cutter(MOL,'z',ZF1+2.0,1.0),prism_xy(JAN,ZFL-1,ZF1+3))
for x,y in FT: mol=D(mol,CYL([x,y,ZFL-1],[x,y,ZF1+3],3.4))
F['moldura_tomada']=max(mol.split(only_watertight=False),key=lambda q:q.volume)
# ---------- placas pretas ----------
REC=uu([bf(Polygon(g.exterior),0.5) for g in NG.values()]+[bf(MOL,0.5)])
PL={'central':sbox(-125.0,0.0,125.0,81.0),'lado_D':sbox(125.0,0.0,258.0,81.0),'lado_E':sbox(-258.0,0.0,-125.0,81.0)}
def placa(poly):
    m=prism_xy(poly,ZP0,ZF1); m=chamfer_top(m,'z',ZF1,1.25)
    m=D(m,prism_xy(REC.intersection(poly.buffer(2)),ZFL,ZF1+5))
    c1=chamfer_cutter(poly.buffer(6).difference(REC),'z',ZF1,0.6)
    if c1 is not None: m=D(m,c1)
    if poly.buffer(-1).intersects(ilD):
        il=bf(ilD,-0.0); il=[i for i in ilhas if i.centroid.x>0][0]
        m=D(m,prism_xy(il,ZI,ZF1+5),chamfer_cutter(il,'z',ZI,0.6),prism_xy(grade(il),ZGR,ZF1+5))
    if poly.intersects(JAN): m=D(m,prism_xy(JAN,ZP0-1,ZF1+5))
    mine=lambda pts:[p for p in pts if poly.buffer(-1).contains(Point(p))]
    for x,y in mine(GS+FT): m=D(m,CYL([x,y,ZP0-1],[x,y,ZF1+1],3.4))
    for x,y in mine(HID): m=D(m,CYL([x,y,ZP0-1],[x,y,ZF1+1],3.4),CYL([x,y,ZP0+0.3],[x,y,ZF1+1],6.2))
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
for k,p in PL.items(): F['placa_'+k]=placa(p)
# ---------- estruturas escondidas (apoios nos bolsos de tras da base) ----------
HR=np.load('rearZ.npy'); pr=pockets(HR,-270.0,0.0,0.5,262.5,265.0)
S1=175.0
def tong(x,yc,s=1): return Polygon([(x+0.2*s,yc-3),(x+0.2*s,yc+3),(x-4.5*s,yc+4.5),(x-4.5*s,yc-4.5)])
def apoios(xr,yr,n=2):
    clip=sbox(xr[0],yr[0],xr[1],yr[1]); out=[]
    for p in pr:
        q=p.buffer(-0.4).intersection(clip)
        for g in (q.geoms if hasattr(q,'geoms') else [q]):
            if not g.is_empty and g.area>=25: out.append(g)
    out=sorted(out,key=lambda g:-g.area)[:n]
    return [prism_xy(g,263.8,ZS0+0.2) for g in out]
def est(x0,x1,zonas):
    m=B(x0,x1,0.0,81.0,ZS0,ZS1)
    for xr in zonas: m=U(m,*apoios(xr,(40.6,60.8)),*apoios(xr,(4.4,19.1)))
    return m
SE=205.0                                                                       # lado da tomada: emenda da estrutura fora da janela (e 80 mm da emenda da placa)
eD=est(S1+0.1,258.0,[(S1+1.5,200.0)]); eE=est(-258.0,-SE-0.1,[(-240.0,-SE-1.5)])
eC=est(0.1,S1-0.1,[(10.0,S1-1.5)]); eCL=est(-SE+0.1,-0.1,[(-SE+1.5,-10.0)])
tD=[tong(S1,59.0),tong(S1,11.0)]; tE=[tong(-SE,59.0,-1),tong(-SE,11.0,-1)]; t0=[tong(0.0,59.0),tong(0.0,11.0)]
eD=U(eD,*[prism_xy(t,ZS0,ZS1) for t in tD]); eC=D(eC,*[prism_xy(t.buffer(0.2,join_style=2),262,285) for t in tD])
eE=U(eE,*[prism_xy(t,ZS0,ZS1) for t in tE]); eCL=D(eCL,*[prism_xy(t.buffer(0.2,join_style=2),262,285) for t in tE])
eC=U(eC,*[prism_xy(t,ZS0,ZS1) for t in t0]); eCL=D(eCL,*[prism_xy(t.buffer(0.2,join_style=2),262,285) for t in t0])
def pil(m):
    for x,y in GS+HID: m=D(m,CYL([x,y,ZS0-1],[x,y,ZS1+1],2.5))
    for x,y in FT: m=D(m,CYL([x,y,ZS0-1],[x,y,ZS1+1],3.4))
    return D(m,prism_xy(bf(JAN,1.0),262.0,ZS1+1))                                # janela da tomada livre (sem apoio embaixo)
big=lambda m:max(m.split(only_watertight=False),key=lambda q:q.volume)
F['est_D']=big(pil(eD)); F['est_E']=big(pil(eE)); F['est_C']=big(pil(eC)); F['est_CL']=big(pil(eCL))
# ---------- ferragens + tomada (referencia) ----------
def bolt(p,axis,L,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*L,d))
HW=[bolt([x,y,ZF1+0.5],[0,0,1],10) for x,y in GS]+[bolt([x,y,ZP0+0.35],[0,0,1],6) for x,y in HID]+[bolt([x,y,ZF1+2.0+2.0],[0,0,1],16) for x,y in FT]
F['ferragens']=U(*HW)
tom=U(B(xa-31,xa+31,ya-15.5,ya+15.5,ZF1+2.0,ZF1+4.0),B(xa-23.5,xa+23.5,ya-13.75,ya+13.75,ZF1+4.0-33.0,ZF1+2.0))
tom=D(tom,B(xa-17,xa+5,ya-9,ya+9,ZF1+1.0,ZF1+4.1)); tom=U(tom,B(xa+8,xa+20,ya-8,ya+8,ZF1+4.0,ZF1+6.0))
for x,y in FT: tom=D(tom,CYL([x,y,ZF1+1],[x,y,ZF1+5],3.4))
F['tomada_AS03']=tom
# ---------- conferencias (antes do espelho) ----------
base=MESH['Corpo1@071.stl']; Rz=np.diag([1,1,-1,1])
bq=base.copy(); bq.apply_transform(Rz); bq.invert() if bq.volume<0 else None       # base espelhada para o quadro local
chk={}
for k in ('est_D','est_E','est_C','est_CL','placa_central','placa_lado_D','placa_lado_E','tomada_AS03'):
    chk[k+'_x_base']=round(I(F[k],bq).volume,2)
ks=list(F.keys())
for i,a in enumerate(ks):
    for b in ks[i+1:]:
        if a in ('ferragens',) or b in ('ferragens',): continue
        x=I(F[a],F[b]).volume
        if x>0.01: chk[a+'_x_'+b]=round(x,2)
LOG['chk']=chk; LOG['vol']={k:bool(v.is_volume) for k,v in F.items()}; LOG['tam']={k:round(float(max(v.extents[0],v.extents[1])),1) for k,v in F.items()}
# espelho -> traseira
T={}
for k,v in F.items():
    q=v.copy(); q.apply_transform(Rz)
    if q.volume<0: q.invert()
    T[k]=q
pickle.dump(T,open('TB.pkl','wb')); print(json.dumps(LOG))
