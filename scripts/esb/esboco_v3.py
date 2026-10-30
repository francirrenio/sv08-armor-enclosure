import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
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
AT=192.0; AH=10.0; GAPB=3.0                         # bracos: 14 mm de largura, ponta em Z +-192
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
sideR=box(0,YG0,ZE,YG1).difference(hexa.buffer(GAP,join_style=2)).difference(armR.buffer(GAPB,join_style=2)).difference(hexa.buffer(GAP,join_style=2)).difference(Lr.buffer(GAP+3.0,join_style=2))
sideR=max([g for g in (sideR.geoms if hasattr(sideR,'geoms') else [sideR])],key=lambda g:g.area)
sideL=affinity.scale(sideR,-1,1,origin=(0,0))
groove=[box(AT+2.0,YM-0.5,228.0,YM+0.5),box(-228.0,YM-0.5,-AT-2.0,YM+0.5)]
tri=lambda zc,yc,s: Polygon([(zc-s/2,yc-s*0.29),(zc+s/2,yc-s*0.29),(zc,yc+s*0.58)])
tris=[tri(229.0,17.0,14.0),tri(-229.0,17.0,14.0)]
SC={'central':[(z,y) for z in (-72,72) for y in (22,52)],'lateral':[(z,y) for z in (-140,140) for y in (16.0,58.0)],'braco':[(z,y) for z in (-118,118,-168,168) for y in (37,)],'cantoneira':[(z,y) for z in (-259.7,259.7) for y in (24.5,71.5)]}
holes=[box(109.5,17,127.5,34),box(132,11,149.5,29),box(155,19.5,172,29)]
# checagens
chk={'hexa_compr':round(hexc.bounds[2]-hexc.bounds[0],1),'braco_compr':round(armR.bounds[2]-armR.bounds[0],1),'lateral_compr':round(sideR.bounds[2]-sideR.bounds[0],1),
     'furos_cobertos_por_verde':[round(h.difference(sideR.buffer(0)).area,1) for h in holes]}
print(chk)
# ---------------- desenho ----------------
BLK='#1c1f21'; BLK2='#2c3034'; GRN='#3f9a4f'; GRN2='#357f43'; LINE='#0d0f10'
fig=plt.figure(figsize=(19,8.6)); ax=fig.add_axes([0.03,0.27,0.94,0.68])
def fill(p,fc,ec=LINE,lw=0.8,z=1,hatch=None,alpha=1):
    for g in (p.geoms if hasattr(p,'geoms') else [p]):
        x,y=g.exterior.xy; ax.fill(-np.array(x),y,fc=fc,ec=ec,lw=lw,zorder=z,hatch=hatch,alpha=alpha)
        for h in g.interiors:
            x,y=h.xy; ax.fill(-np.array(x),y,fc='#d8d2c2',ec=ec,lw=lw,zorder=z+0.1)
# painel lateral em cima (contexto)
fill(box(-219.2,81.2,219.2,100),'#c9d4ea',ec='#7d8db3',lw=0.6,z=0); ax.text(0,92,'painel lateral (assenta em Y 81)',ha='center',va='center',fontsize=9,color='#4b5a7d')
# placa preta
plate=box(-ZE,YB,ZE,YT)
fill(plate,BLK,z=1)
# rebaixos (linha de sombra) - fundo preto, mostrado pelo contorno das verdes
fill(oval,'#cfc7b3',z=5)
fill(hexc,GRN,z=3); fill(armR,GRN,z=3); fill(armL,GRN,z=3); fill(sideR,GRN2,z=3); fill(sideL,GRN2,z=3)
for g in groove: fill(g,'#24402b',ec='none',z=4)
fill(Lboth,BLK2,z=6,lw=1.0)
for t in tris: fill(t,'#121416',z=7)
for k,pts in SC.items():
    for z,y in pts:
        ax.add_patch(plt.Circle((-z,y),2.85,fc='#b23a32',ec='#3a0f0c',lw=0.8,zorder=8))
for h in holes:
    x,y=h.exterior.xy; ax.plot(-np.array(x),y,ls=(0,(3,2)),color='#f2b13c',lw=1.1,zorder=9)
ax.annotate('3 furos da placa antiga:\nfechados pela preta, verde por cima',xy=(-140.7,30),xytext=(-140,-56),fontsize=9.5,ha='center',va='center',color='#8a5a00',arrowprops=dict(arrowstyle='-',lw=0.7,color='#c48a1a'),zorder=11,bbox=dict(fc='#fff7e6',ec='#e0b866',lw=0.5,pad=2.5))
# chanfro indicado
ax.plot([-ZE,ZE],[YT-0.6,YT-0.6],color='#555',lw=0.6,zorder=2)
# cotas
def dimh(z0,z1,y,txt):
    ax.annotate('',xy=(-z0,y),xytext=(-z1,y),arrowprops=dict(arrowstyle='<->',lw=0.8,color='#333'),zorder=10)
    ax.text(-(z0+z1)/2,y-1.5,txt,ha='center',va='top',fontsize=9,color='#222',zorder=10,bbox=dict(fc='#f4f3ef',ec='none',pad=0.5))
def dimv(z,y0,y1,txt,side='right'):
    ax.annotate('',xy=(-z,y0),xytext=(-z,y1),arrowprops=dict(arrowstyle='<->',lw=0.8,color='#333'),zorder=10)
    ax.text(-z+(3 if side=='right' else -3),(y0+y1)/2,txt,ha='left' if side=='right' else 'right',va='center',fontsize=9,color='#222',zorder=10)
dimh(-WP,WP,-6,'176 — central'); dimh(WP-4,AT,-6,'108 — braço'); dimh(-AT,-WP+4,-6,'108 — braço')
dimh(-ZE,ZE,-20,'547 — lateral da base (Z −273,5 a +273,5)')
dimh(-ZL,ZL,108,'495 entre as cantoneiras')
dimv(-ZE-20,YB,YT,'79\n(Y 2→81)'); dimv(-ZE-20,YT,94,'13 (cantoneira)')
dimv(ZE+20,YG0,YG1,'58 verdes\n(Y 8→66)','left')
ax.text(-0,37,'apoio de mão\n122 × 42',ha='center',va='center',fontsize=9,color='#444',zorder=9)
def call(pt,txt,tp):          # pt e tp em (Z,Y); desenha com X = -Z
    ax.annotate(txt,xy=(-pt[0],pt[1]),xytext=(-tp[0],tp[1]),fontsize=9.5,ha='center',va='center',
                arrowprops=dict(arrowstyle='-',lw=0.7,color='#333',shrinkA=0,shrinkB=2),zorder=11,bbox=dict(fc='white',ec='#bbb',lw=0.5,pad=2.5))
call((0,64),'Peça central verde: contorna o apoio de mão;\nbraços de 20 mm saem para as laterais até Z ±192',(0,127))
call((150,62),'Placas verdes laterais: faixas de 16 mm; vão de 3 mm\npara o braço e 1,0 para a central e a cantoneira',(165,127))
call((-185,37),'Friso de 1 mm continua a linha do meio',(-165,127))
call((260,10),'Cantoneira em L: perna vertical (atual)\n+ perna de baixo entrando na lateral',(205,-38))
call((-229,18),'Triângulo rebaixado\nna perna de baixo',(-235,-40))
ax.text(150,73.5,'faixa preta de cima, 15 mm (apoio do painel)',ha='center',va='center',fontsize=8.5,color='#d9dcde',zorder=9)
ax.text(-150,73.5,'faixa preta de cima, 15 mm (apoio do painel)',ha='center',va='center',fontsize=8.5,color='#d9dcde',zorder=9)
call((-110,4.5),'Faixa preta de baixo (6 mm)',(-80,-38))
ax.set_xlim(-330,330); ax.set_ylim(-65,138); ax.set_aspect('equal'); ax.axis('off')
ax.text(-325,132,'FRENTE  ←',fontsize=10,fontweight='bold',color='#555'); ax.text(325,132,'→  FUNDO',fontsize=10,fontweight='bold',color='#555',ha='right')
fig.text(0.03,0.965,'Esboço — lateral direita da base vista de fora (medidas reais, mm)',fontsize=15,fontweight='bold')
# notas
notes=['• Todas as diagonais a 60°, iguais às nervuras da base (os V dos bolsos).',
 '• Topo e base das verdes (Y 66 e Y 8) são uma linha contínua de ponta a ponta; a linha do meio (Y 37) passa no centro do apoio de mão.',
 '• Parafusos aparentes simétricos: 4 na central, 2 em cada braço, 2 em cada lateral (acima/abaixo do braço), 2 em cada cantoneira (os atuais).',
 '• Preta de baixo continua inteira por trás das verdes (rebaixo de 3,2 mm): os 3 furos da base ficam fechados.',
 '• Emendas: preta no centro (escondida sob a verde central); verdes em ±72–89 (diagonal) e ±195–248 (contorno da cantoneira); estrutura escondida em Z ±140.',
 '• Braços (2 e 4): 20 mm de largura e ponta em Z ±192. Vão entre braço e placa lateral: 3 mm. Placas 1 e 5: faixas de 16 mm (antes 21).',
 '• Central + braços dariam 384 mm (> 300): os braços são peças próprias, encaixadas em V na ponta da central (sombra 1,0). Maior verde: 176 mm.']
for i,t in enumerate(notes): fig.text(0.035,0.235-i*0.031,t,fontsize=10.5,color='#222')
plt.savefig('esboco_lateral.png',dpi=110,facecolor='#f4f3ef')
