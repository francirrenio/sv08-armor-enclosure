# FRENTE_V2: faixa de baixo da frente no mesmo desenho das laterais (versao A aprovada):
#  - verde central hexagonal (X +-100, Y 4-72) com a logo (58 mm) e 2 filetes de luz vazados
#  - faixa de cima e asa com bolsao dos 2 lados (mesmas alturas da lateral), vao de 4 mm, nervura com frisos
#  - placa branca (logo e filetes em relevo) e caixa de luz fechada com fita ARGB atras da verde central
#  - placas pretas: central (X +-125) e laterais (X 125-258); estruturas escondidas: centrais (2 metades) e D
# Coordenadas (X, Y), profundidade em Z (face de fora Z 286). Lado E da frente = espelho (exportacao), menos as pecas centrais.
import numpy as np, trimesh, json, pickle
exec(open('load.py').read()); MESH=M; exec(open('geo.py').read()); exec(open('geo_ch2.py').read())
from shapely.geometry import box as sbox, Polygon, Point
from shapely.ops import unary_union as uu
from shapely import affinity as af
R4=pickle.load(open('R4.pkl','rb'))
_pxy=prism_xy
def prism_xy(poly,z0,z1):
    poly=poly.buffer(0)
    gs=[g for g in (poly.geoms if hasattr(poly,'geoms') else [poly]) if g.area>0.05]
    ms=[_pxy(g,z0,z1) for g in gs]
    ms=[m if m.volume>0 else m.invert() or m for m in ms]
    return ms[0] if len(ms)==1 else U(*ms)
F={}; LOG={}
_fv=open('frente_versoes.py').read(); exec(_fv.split('VERS=[')[0])          # hexa, fit, lados, bolsao, grade, Lr, M, op, bf
# ---------- geometria 2D ----------
ZF1=286.0; ZFL=282.8; ZG0=283.0          # face, fundo do encaixe das verdes, costas das verdes
ZR=ZF1-0.5; ZI=ZF1-1.5; ZGR=ZI-1.0       # topo da nervura, ilha do bolsao, fundo da grade
ZP0=279.0; ZS0,ZS1=276.0,279.0           # placa preta de 279 a 286; estrutura escondida 276-279 (+ chaves ate 263,8)
ZW0,ZW1=281.7,282.9                      # placa branca (base de 1,2 mm)
ZB0,ZB1=270.5,272.0                      # fundo da caixa de luz (fita apoiada em Z 272)
YC=38.0
hexc=hexa(-100.0,100.0,4.0,72.0)
LG=pickle.load(open('../logo/logo_poly.pkl','rb'))
def _logo(h,xc,yc):
    g=af.scale(LG,1,-1,origin=(0,0)); b=g.bounds; s=h/(b[3]-b[1])
    g=af.scale(g,s,s,origin=(0,0)); b=g.bounds
    return af.translate(g,xc-0.5*(b[0]+b[2]),yc-0.5*(b[1]+b[3]))
logo0=_logo(58.0,0.0,YC)
segs=[p.buffer(-0.15,join_style=2) for p in logo0.geoms]                      # vazados da logo (vaos entre as partes alargados para ~1,2 mm ou mais)
xi=logo0.bounds[2]+9.0
fil=[hexa(xi,xi+52.0,YC-3.5,YC+3.5,1.5)]; fil.append(M(fil[0]))               # filetes de luz 52 x 7
jan=uu([Polygon(s.exterior) for s in segs]+fil)                               # janelas na verde (o olho do dragao fica dentro da janela)
cav=op(bf(uu([logo0.convex_hull]+fil),1.5),1.5).intersection(bf(hexc,-3.5))  # interior da caixa de luz = furo de luz na placa preta
sheet=bf(cav,1.5).intersection(bf(hexc,-2.0))                                # placa branca (base): fica toda escondida sob a verde
box_out=bf(cav,1.6); flange=bf(cav,5.6)
lados_v,ilhas=lados(hexc)                                                     # faixas de cima e asas (dir e esq), com bolsao
supF=[g for g in lados_v if g.centroid.x>0 and g.centroid.y>42][0]; asaF=[g for g in lados_v if g.centroid.x>0 and g.centroid.y<=42][0]
supE=M(supF); asaE=M(asaF)
ilF=[i for i in ilhas if i.centroid.x>0][0]; ilE=M(ilF)
NG={'verde_central':hexc,'sup_D':supF,'asa_D':asaF,'sup_E':supE,'asa_E':asaE}
# ---------- parafusos ----------
def _meio(p,y,xa,xb):
    s=p.intersection(sbox(xa,y-0.01,xb,y+0.01)); return 0.5*(s.bounds[0]+s.bounds[2])
ys=0.5*(43.0+66.0); bol=[b for b in [Polygon(i) for i in asaF.interiors]][0]
SCc=[(x,y) for x in (-72.0,72.0) for y in (12.0,62.0)]
SCd=[(supF.bounds[0]+26.0,ys),(supF.bounds[2]-30.0,ys),(_meio(asaF,YC,0,bol.bounds[0]),YC-17.0+17.0),(_meio(asaF,YC,bol.bounds[2],300),YC)]
_ya=asaF.bounds[1]; _bc=0.5*(bol.bounds[0]+bol.bounds[2])
SCd[2]=(_meio(asaF,asaF.centroid.y,0,bol.bounds[0]),asaF.centroid.y); SCd[3]=(_meio(asaF,asaF.centroid.y,bol.bounds[2],300),asaF.centroid.y)
GS=SCc+SCd+[(-x,y) for x,y in SCd]                                            # aparentes (M3 cabeca abaulada)
HIDd=[(50.0,9.0),(50.0,58.0),(_bc-14.0,_ya+3.5),(_bc+14.0,_ya+3.5),(230.0,55.0),(248.0,52.0),(248.0,10.5)]
HID=HIDd+[(-x,y) for x,y in HIDd]                                             # escondidos sob as verdes / sob a cantoneira
# ---------- verdes ----------
def verde(poly,furos=()):
    m=D(prism_xy(poly,ZG0,ZF1),chamfer_cutter(poly,'z',ZF1,1.0))
    for x,y in [p for p in GS if poly.contains(Point(p))]: m=D(m,CYL([x,y,ZG0-1],[x,y,ZF1+1],3.4))
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
vc=verde(hexc)
vc=D(vc,prism_xy(jan,ZG0-1,ZF1+1)); vc=max(vc.split(only_watertight=False),key=lambda q:q.volume)
F['verde_central']=vc
for k in ('sup_D','asa_D','sup_E','asa_E'): F['verde_'+k]=verde(NG[k])
# ---------- placa branca (logo e filetes em relevo) ----------
rel=uu([s.buffer(-0.15,join_style=2) for s in segs]+[bf(f,-0.15) for f in fil])  # relevo com 0,15 de folga nos vazados (olho = furo)
wb=U(prism_xy(sheet,ZW0,ZW1),prism_xy(rel,ZW1-0.01,ZF1))
F['placa_branca']=wb
# ---------- caixa de luz ----------
cx=U(prism_xy(box_out,ZB0,ZB1),prism_xy(box_out.difference(cav),ZB1-0.01,ZP0),prism_xy(flange.difference(cav),ZP0-1.5,ZP0))
xc0=fil[1].bounds[0]+4.0
cx=D(cx,CYL([xc0,YC,ZB0-1],[xc0,YC,ZB1+1],7.0))                                # furo do cabo (5 V, GND, dados)
fita=[sbox(-92.0,YC-6.0,92.0,YC+6.0),sbox(-26.0,YC+12.0,26.0,YC+24.0),sbox(-26.0,YC-24.0,26.0,YC-12.0)]
guias=uu([bf(f,1.4).difference(bf(f,0.2)) for f in fita]).intersection(bf(cav,-0.5))   # guias de 0,8 mm em volta de cada trecho da fita
cx=U(cx,prism_xy(guias,ZB1-0.01,ZB1+0.8))
F['caixa_luz']=max(cx.split(only_watertight=False),key=lambda q:q.volume)
F['fita_led']=U(*[prism_xy(f.buffer(-0.2),ZB1,ZB1+1.6) for f in fita])
# ---------- placas pretas ----------
REC=uu([Polygon(g.exterior.coords,[r.coords for r in g.interiors]).buffer(0.5,join_style=1,quad_segs=32) for g in NG.values()])
REC=uu([REC.difference(bf(Polygon(hexc.exterior),0.5)),bf(Polygon(hexc.exterior),0.5)])   # a verde central nao tem furo na placa (a luz passa pelo furo proprio)
_cl=REC.buffer(2.6,join_style=1,quad_segs=32).buffer(-2.6,join_style=1,quad_segs=32)
RIB=_cl.difference(REC).buffer(-0.15,join_style=1).buffer(0.15,join_style=1)
RIB=uu([g for g in (RIB.geoms if hasattr(RIB,'geoms') else [RIB]) if g.area>5])
PL={'central':sbox(-125.0,0.0,125.0,81.0),'lado':sbox(125.0,0.0,258.0,81.0)}
def placa(poly):
    m=prism_xy(poly,ZP0,ZF1); m=chamfer_top(m,'z',ZF1,1.25)
    m=D(m,prism_xy(REC.intersection(poly.buffer(2)),ZFL,ZF1+5))
    rib=RIB.intersection(poly.buffer(2))
    if not rib.is_empty: m=D(m,prism_xy(rib,ZR,ZF1+5))
    Fp=poly.buffer(6).difference(REC)
    c1=chamfer_cutter(Fp,'z',ZF1,0.6); c3=chamfer_cutter(Fp,'z',ZR,0.6)
    if c1 is not None: m=D(m,I(c1,prism_xy(poly.buffer(6).difference(RIB),ZFL,ZF1+5)))
    if c3 is not None: m=D(m,I(c3,prism_xy(RIB.union(REC).buffer(0.01).intersection(poly.buffer(6)),ZFL,ZF1+5)))
    for il in (ilF,ilE):
        if poly.buffer(-1).intersects(il): m=D(m,prism_xy(il,ZI,ZF1+5),chamfer_cutter(il,'z',ZI,0.6),prism_xy(grade(il),ZGR,ZF1+5))
    if poly.intersects(cav):
        m=D(m,prism_xy(cav,ZP0-1,ZF1+5),prism_xy(sheet,ZW0,ZF1+5))              # furo de luz + encaixe da placa branca
    mine=lambda pts:[p for p in pts if poly.buffer(-1).contains(Point(p))]
    for x,y in mine(GS): m=D(m,CYL([x,y,ZP0-1],[x,y,ZF1+1],3.4))
    for x,y in mine(HID): m=D(m,CYL([x,y,ZP0-1],[x,y,ZF1+1],3.4),CYL([x,y,ZP0+0.3],[x,y,ZF1+1],6.2))
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
F['placa_central']=placa(PL['central']); F['placa_lado']=placa(PL['lado'])
# ---------- estruturas escondidas ----------
HF=np.load('frontZ.npy'); pf=pockets(HF,45.0,0.0,0.5,262.5,265.0)
S1=175.0
def tong(x,yc): return Polygon([(x+0.2,yc-3),(x+0.2,yc+3),(x-4.5,yc+4.5),(x-4.5,yc-4.5)])
tU,tL=tong(S1,59.0),tong(S1,11.0); tU0,tL0=tong(0.0,59.0),tong(0.0,11.0)
KEEP={1,6,7,9,10,16,17,19,20}
_ZON=[((S1+1.5,194.0),(40.6,60.8)),((S1+1.5,194.0),(4.4,19.1)),((45.5,S1-1.5),(40.6,60.8)),((45.5,S1-1.5),(4.4,19.1))]
_ALL=[]
for zi,(xr,yr) in enumerate(_ZON):
    clip=sbox(xr[0],yr[0],xr[1],yr[1])
    for p in pf:
        q=p.buffer(-0.4).intersection(clip)
        for g in (q.geoms if hasattr(q,'geoms') else [q]):
            if not g.is_empty and g.area>=25: _ALL.append((zi,g))
def keys_sel(zi): return [prism_xy(g,263.8,276.2) for i,(z,g) in enumerate(_ALL,1) if z==zi and i in KEEP]
furo_cx=prism_xy(bf(box_out,0.2),262.0,ZS1+1); bolso_fl=prism_xy(bf(flange,0.2),ZP0-1.7,ZS1+1)
eD=B(S1+0.1,258.0,0.0,81.0,ZS0,ZS1)                                           # sem o vao da barra de LED antiga
eD=U(eD,*keys_sel(0),*keys_sel(1),prism_xy(tU,ZS0,ZS1),prism_xy(tL,ZS0,ZS1))
eC=B(0.1,S1-0.1,0.0,81.0,ZS0,ZS1)
eC=U(eC,*keys_sel(2),*keys_sel(3))
eC=D(eC,prism_xy(tU.buffer(0.2,join_style=2),262,285),prism_xy(tL.buffer(0.2,join_style=2),262,285))
def _mx(m):
    c=m.copy(); c.apply_transform(np.diag([-1,1,1,1]))
    if c.volume<0: c.invert()
    return c
eCL=D(_mx(eC),prism_xy(tU0.buffer(0.2,join_style=2),262,285),prism_xy(tL0.buffer(0.2,join_style=2),262,285))
eC=U(eC,prism_xy(tU0,ZS0,ZS1),prism_xy(tL0,ZS0,ZS1))
allS=GS+HID
def pil(m):
    for x,y in allS: m=D(m,CYL([x,y,ZS0-1],[x,y,ZS1+1],2.5))
    return m
eC=D(pil(eC),furo_cx,bolso_fl); eCL=D(pil(eCL),furo_cx,bolso_fl); eD=pil(eD)
F['est_C']=max(eC.split(only_watertight=False),key=lambda q:q.volume); F['est_CL']=max(eCL.split(only_watertight=False),key=lambda q:q.volume); F['est_D']=eD
F['soleira']=MESH['SV-30-03c soleira (degrau) (2 de 2)']
# SOLEIRA_E: a soleira e em 2 pecas; a de 1/2 (X -226,4 a 60) passa pelo centro, por cima da caixa de luz:
# ganha um rebaixo com 0,3 de folga em volta da caixa (so na parte de baixo da frente dela)
_s1=MESH['SV-30-03c soleira (degrau) (1 de 2)']
F['soleira_E']=max(D(_s1,prism_xy(bf(flange,0.3),262.0,ZS1+1)).split(only_watertight=False),key=lambda q:q.volume)
# ---------- ferragens ----------
def bolt(p,axis,L,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*L,d))
HW=[bolt([x,y,ZF1],[0,0,1],10) for x,y in GS]+[bolt([x,y,ZP0+0.35],[0,0,1],6) for x,y in HID]
F['ferragens']=U(*HW)
# ---------- conferencias ----------
base=MESH['Corpo1@071.stl']; chk={}
for k in ('caixa_luz','est_C','est_CL','est_D','placa_central','placa_lado'): chk[k+'_x_base']=round(I(F[k],base).volume,2)
for a in ('verde_central','placa_branca','caixa_luz','verde_sup_D','verde_asa_D'):
    for b in ('placa_central','placa_lado','est_C','est_CL'): chk[a+'_x_'+b]=round(I(F[a],F[b]).volume,2)
chk['branca_x_verde']=round(I(F['placa_branca'],F['verde_central']).volume,2)
chk['caixa_x_branca']=round(I(F['caixa_luz'],F['placa_branca']).volume,2)
chk['caixa_x_soleira']=round(I(F['caixa_luz'],F['soleira']).volume,2); chk['caixa_x_soleiraE']=round(I(F['caixa_luz'],F['soleira_E']).volume,2); chk['hw_x_soleiraE']=round(I(F['ferragens'],F['soleira_E']).volume,2); chk['hw_x_soleira']=round(I(F['ferragens'],F['soleira']).volume,2)
chk['vol']={k:bool(v.is_volume) for k,v in F.items()}
chk['tam']={k:round(float(max(v.extents[0],v.extents[1])),1) for k,v in F.items()}
LOG['chk']=chk; LOG['GS']=len(GS); LOG['HID']=len(HID)
pickle.dump(F,open('R5.pkl','wb')); print(json.dumps(LOG))
