import numpy as np
from shapely.geometry import Polygon, box, Point, LineString
from shapely.ops import unary_union as uu
from shapely import affinity
T60=np.tan(np.radians(60))
GAP=1.0
# ---- coordenadas (Z, Y) da lateral direita; desenho visto de fora (frente a esquerda) ----
ZE=273.5; YB,YT=2.0,81.0
YG0,YG1=8.0,66.0; YM=37.0                 # verdes: de Y 8 a Y 66; linha do meio na altura do centro do apoio de mao
def stadium(zc,yc,hw,r):                  # apoio de mao (oval da base)
    return uu([box(zc-hw+r,yc-r,zc+hw-r,yc+r),Point(zc-hw+r,yc).buffer(r,64),Point(zc+hw-r,yc).buffer(r,64)])
oval=stadium(0,37,60.9,21.0)
WP=88.0; WT=WP-(YG1-YM)/T60
hexa=Polygon([(-WT,YG1),(WT,YG1),(WP,YM),(WT,YG0),(-WT,YG0),(-WP,YM)])
AT=211.0; AH=12.0; GAPB=3.0       # bracos: 24 mm de largura, ponta em Z +-211 (ponta paralela a perna da cantoneira)                         # bracos: 14 mm de largura, ponta em Z +-192
armR=Polygon([(WP-AH/T60,YM-AH),(AT-AH/T60,YM-AH),(AT,YM),(AT-AH/T60,YM+AH),(WP-AH/T60,YM+AH)])
armR=armR.difference(hexa.buffer(GAP,join_style=2))          # encaixe em V na ponta do hexagono (pecas separadas, limite 300 mm)
armL=affinity.scale(armR,-1,1,origin=(0,0))
hexc=hexa.difference(oval)
central=uu([hexc,armR,armL])
# cantoneira em L (preta, por cima da lateral): perna vertical existente (Z 247,7 a 273,5) + perna de baixo para dentro
ZL=247.7; YLb=34.0; ZLs=214.0
Lr=Polygon([(ZL,YB-2),(ZE+22,YB-2),(ZE+22,94.0),(ZL+3,94.0),(ZL,91.0),(ZL,YLb),(ZLs,YLb),(ZLs-(YLb-YB+2)/T60,YB-2)])
Ll=affinity.scale(Lr,-1,1,origin=(0,0))
Lboth=uu([Lr,Ll])
# placas verdes laterais: contornam a peca central e a cantoneira
sideR=box(0,YG0,ZE,YG1).difference(hexa.buffer(GAP,join_style=2)).difference(armR.buffer(GAPB,join_style=2)).difference(Lr.buffer(GAP+3.0,join_style=2))
sideR=sideR.difference(box(AT-14.0,31.0,ZE,43.0))          # placas 1 e 5: parte de cima e de baixo separadas por vao de 12 mm depois da ponta do braco
parts=sorted([g for g in (sideR.geoms if hasattr(sideR,'geoms') else [sideR]) if g.area>50],key=lambda g:-g.centroid.y)
sideR=uu(parts)
sideL=affinity.scale(sideR,-1,1,origin=(0,0))
groove=[]
tri=lambda zc,yc,s: Polygon([(zc-s/2,yc-s*0.29),(zc+s/2,yc-s*0.29),(zc,yc+s*0.58)])
tris=[tri(229.0,17.0,14.0),tri(-229.0,17.0,14.0)]
SC={'central':[(z,y) for z in (-72,72) for y in (22,52)],'lateral':[(z,y) for z in (-110,110,-170,170) for y in (15.0,59.0)],'braco':[(z,y) for z in (-140,140,-195,195) for y in (37,)],'cantoneira':[(z,y) for z in (-259.7,259.7) for y in (24.5,71.5)]}
# ---- cantos do contorno arredondados (R 2,5) ----
RR=2.5
def rc(p,r=RR): return p.buffer(-r,join_style=1,resolution=8).buffer(r,join_style=1,resolution=8)
def rr(p,r=RR): return rc(p,r).buffer(r,join_style=1,resolution=8).buffer(-r,join_style=1,resolution=8)
_armraw=Polygon([(WP-AH/T60-4,YM-AH),(AT-AH/T60,YM-AH),(AT,YM),(AT-AH/T60,YM+AH),(WP-AH/T60-4,YM+AH)])
hexa=rc(hexa)
armR=rc(rc(_armraw).difference(hexa.buffer(GAP,join_style=1,resolution=8)),1.5)
armL=affinity.scale(armR,-1,1,origin=(0,0))
hexc=hexa.difference(oval)
Lr=rr(Lr).buffer(12.0,join_style=1,resolution=16).buffer(-12.0,join_style=1,resolution=16)   # canto de dentro do L suave (R 12)
_s=box(0,YG0,ZE,YG1).difference(hexa.buffer(GAP,join_style=1,resolution=8)).difference(armR.buffer(GAPB,join_style=1,resolution=8)).difference(Lr.buffer(GAP+3.0,join_style=1,resolution=8))
_s=_s.difference(box(AT-14.0,31.0,ZE,43.0))
parts=sorted([rc(g) for g in (_s.geoms if hasattr(_s,'geoms') else [_s]) if g.area>50],key=lambda g:-g.centroid.y)
