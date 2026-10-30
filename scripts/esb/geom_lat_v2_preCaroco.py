# FAIXA DE BAIXO DAS LATERAIS - VERSAO 2 (asas com bolsao), coordenadas (Z, Y) da lateral direita, Z+ = frente
#  - verde central (apoio de mao) igual, cantos R6
#  - de cada lado: faixa de cima (Y 43-66) e asa (Y 0-39, ate o fundo da base) com bolsao hexagonal preto (grade em relevo na placa)
#  - vao de 4 mm entre as verdes e ate a cantoneira; cantos de fora R6
import numpy as np
from shapely.geometry import Polygon, box, Point
from shapely.ops import unary_union as uu
from shapely import affinity
_g={}; exec(open('esb/geom_lat.py').read(),_g)
oval=_g['oval']; Lr=_g['Lr']; ZE=_g['ZE']; T60=_g['T60']
K=1.0/T60                      # inclinacao das diagonais (mesma da verde central)
Q=64
GAPV=4.0                       # vao entre as verdes
RV=6.0                         # cantos de fora
op=lambda p,r:p.buffer(-r,join_style=1,quad_segs=Q).buffer(r,join_style=1,quad_segs=Q)
bf=lambda p,r:p.buffer(r,join_style=1,quad_segs=Q)
def maior(g): return max([p for p in (g.geoms if hasattr(g,'geoms') else [g])],key=lambda p:p.area)
hexv=op(_g['hexa'],RV)                                   # contorno da verde central (o oval e furo dela)
YS0,YS1=43.0,66.0                                        # faixa de cima
supF=maior(op(box(0,YS0,ZE,YS1).difference(bf(hexv,GAPV)).difference(bf(Lr,GAPV)),RV))
asaF0=maior(op(box(0,0.0,ZE,YS1).difference(bf(hexv,GAPV)).difference(bf(supF,GAPV)).difference(bf(Lr,GAPV)),RV))
# bolsao: hexagono com pontas a 120 graus (mesma diagonal), no meio da asa
_ya,_yb=asaF0.bounds[1],asaF0.bounds[3]; YC=0.5*(_ya+_yb); HB=11.5; LB=55.0
_d=HB*K
def _zfaixa(p,y):   # trecho da asa na altura y
    s=p.intersection(box(-1e3,y-0.01,1e3,y+0.01)); return s.bounds[0],s.bounds[2]
_z0,_z1=_zfaixa(asaF0,YC); ZC=0.5*(_z0+_z1)
bolF=op(Polygon([(ZC-LB/2+_d,YC-HB),(ZC+LB/2-_d,YC-HB),(ZC+LB/2,YC),(ZC+LB/2-_d,YC+HB),(ZC-LB/2+_d,YC+HB),(ZC-LB/2,YC)]),5.0)
asaF=Polygon(asaF0.exterior.coords,[bolF.exterior.coords])
ilhaF=bf(bolF,-0.5)                                      # placa preta dentro do bolsao (0,5 de folga ate a verde)
def grade(ilha,n=6,w=2.6):                               # rasgos inclinados na mesma diagonal, dentro da ilha
    z0,y0,z1,y1=ilha.bounds; dz=(z1-z0-2*HB*K)/n; out=[]
    for i in range(n):
        zc=z0+HB*K+dz*(i+0.5); h=(y1-y0)/2; d=h*K
        out.append(Polygon([(zc-w/2-d,y0-1),(zc+w/2-d,y0-1),(zc+w/2+d,y1+1),(zc-w/2+d,y1+1)]))
    return op(uu(out).intersection(bf(ilha,-2.2)),0.6)
gradeF=grade(ilhaF)
M=lambda g:affinity.scale(g,-1,1,origin=(0,0))
NG={'verde_central':hexv.difference(oval),'verde_sup_F':supF,'verde_asa_F':asaF,'verde_sup_T':M(supF),'verde_asa_T':M(asaF)}
ILHAS=[ilhaF,M(ilhaF)]; GRADES=[gradeF,M(gradeF)]
# parafusos aparentes (M3 cabeca abaulada) - simetricos frente/tras
def _meio(p,y,za,zb):   # centro do trecho da peca entre za e zb na altura y
    s=p.intersection(box(za,y-0.01,zb,y+0.01)); return 0.5*(s.bounds[0]+s.bounds[2])
_ys=0.5*(YS0+YS1); _sz0,_sz1=supF.bounds[0],supF.bounds[2]
SC_F=[(-72.0,22.0),(-72.0,52.0),(72.0,22.0),(72.0,52.0)]                                   # verde central (furos atuais)
SC_S=[(_sz0+26.0,_ys),(_sz1-30.0,_ys)]                                                       # faixa de cima
SC_A=[(_meio(asaF,YC,0,bolF.bounds[0]),YC),(_meio(asaF,YC,bolF.bounds[2],ZE),YC)]            # asa: um de cada lado do bolsao
SC=SC_F+SC_S+SC_A+[(-z,y) for z,y in SC_S+SC_A]
# parafusos escondidos da placa (sob as verdes): (y,z)
HID=[(12.0,40.0),(62.0,40.0),(_ya+3.5,ZC-14.0),(_ya+3.5,ZC+14.0),(55.0,230.0)]
HID=HID+[(y,-z) for y,z in HID]
