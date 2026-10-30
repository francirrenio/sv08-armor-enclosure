# 4 versoes da faixa de baixo da FRENTE (vista de fora), no mesmo estilo das laterais: cantos R6, vao de 4 mm,
# diagonais de 30 graus, bolsoes com grade. Coordenadas (X, Y); a cantoneira da frente tem o mesmo perfil da lateral.
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union as uu
from shapely import affinity
_V={}; exec(open('esb/geom_lat_v2.py').read(),_V)
Lr=_V['Lr']; op=_V['op']; bf=_V['bf']; maior=_V['maior']; K=_V['K']; grade=_V['grade']
M=lambda g:affinity.scale(g,-1,1,origin=(0,0))
cants=uu([Lr,M(Lr)]); GAP=4.0; R=6.0
def hexa(x0,x1,y0,y1,r=R,pl=True,pr=True):
    ym=(y0+y1)/2; d=(y1-y0)/2*K
    pts=[(x0+(d if pl else 0),y0),(x1-(d if pr else 0),y0)]+([(x1,ym)] if pr else [])+[(x1-(d if pr else 0),y1),(x0+(d if pl else 0),y1)]+([(x0,ym)] if pl else [])
    return op(Polygon(pts),r)
def fit(g,viz,r=R):
    return maior(op(g.difference(uu([bf(v,GAP) for v in viz])),r))
def bolsao(asa,lb=55.0,hb=11.5):
    s=asa.bounds; yc=0.5*(s[1]+s[3]); seg=asa.intersection(box(-1e3,yc-0.01,1e3,yc+0.01)); xc=0.5*(seg.bounds[0]+seg.bounds[2])
    return hexa(xc-lb/2,xc+lb/2,yc-hb,yc+hb,5.0)
def com_furo(p,f): return Polygon(p.exterior.coords,[f.exterior.coords])
def lados(centro,ysup=(43.0,66.0),ywing=(0.0,66.0),bols=True):   # faixa de cima + asa dos 2 lados (igual a lateral)
    sup=fit(box(0,ysup[0],300,ysup[1]),[centro,Lr])
    _,y0c,_,y1c=centro.bounds; _pd=[]
    for t in (0.2,0.4):   # dois pontos na diagonal reta de baixo do lado direito
        yy=y0c+(y1c-y0c)*t; _pd.append((centro.intersection(box(-1e3,yy-1e-4,1e3,yy+1e-4)).bounds[2],yy))
    asa=maior(op(box(0,ywing[0],300,ywing[1]).difference(uu([bf(v,GAP) for v in [centro,sup,Lr]])).difference(_V['corta_diag'](_pd[0],_pd[1],GAP)),R))
    out=[sup,M(sup)]; ilhas=[]
    if bols:
        b=bolsao(asa); out+=[com_furo(asa,b),M(com_furo(asa,b))]; ilhas=[bf(b,-0.5),M(bf(b,-0.5))]
    else: out+=[asa,M(asa)]
    return out,ilhas
def V1():   # igual a lateral: hexagono central com a barra de LED no lugar do apoio de mao
    c=_V['hexv']; led=box(-60,27.5,60,46.5)
    ls,il=lados(c); return dict(verdes=[com_furo(c,bf(led,0.2))]+ls,led=led,ilhas=il,nota='Igual à lateral: a peça central é o mesmo hexágono da lateral e a barra de LED (120 x 19) fica no lugar do apoio de mão. Faixa de cima e asa com bolsão dos 2 lados, nas mesmas alturas da lateral: as linhas continuam em volta da impressora.')
def V2():   # hexagono central mais largo, LED maior
    c=hexa(-128,128,8,66); led=box(-90,27.5,90,46.5)
    ls,il=lados(c); return dict(verdes=[com_furo(c,bf(led,0.2))]+ls,led=led,ilhas=il,nota='Hexágono central mais largo (256 mm), com LED de 180 x 19. As asas ficam mais curtas, ainda com o bolsão.')
def V3():   # LED numa seta central; faixas finas em cima e embaixo (2 metades) e uma peca em V de cada lado
    c=hexa(-145,145,23,51); led=box(-100,27.5,100,46.5)
    sup=fit(box(-300,55.0,300,66.0),[Lr,M(Lr)],5.0); sup=[op(sup.intersection(box(-300,0,-2,100)),5.0),op(sup.intersection(box(2,0,300,100)),5.0)]
    inf=fit(box(-300,0,300,19.0),[Lr,M(Lr)]); inf=[op(inf.intersection(box(-300,-1,-2,100)),R),op(inf.intersection(box(2,-1,300,100)),R)]
    lado=fit(box(0,23,300,51),[c,Lr]+sup+inf)
    return dict(verdes=[com_furo(c,bf(led,0.2))]+sup+inf+[lado,M(lado)],led=led,ilhas=[],nota='Seta central (290 mm) com LED de 200 x 19. Em cima e embaixo, faixas finas de ponta a ponta (2 metades cada). Dos lados, uma peça na altura da seta, com o encaixe em V na ponta dela.')
def V4():   # LED curto no centro, faixa de cima corrida (2 metades) e asas com bolsao
    c=hexa(-72,72,8,40); led=box(-45,14.5,45,33.5)
    sup=fit(box(-300,44.0,300,66.0),[Lr,M(Lr)]); sup=[op(sup.intersection(box(-300,0,-2,100)),R),op(sup.intersection(box(2,0,300,100)),R)]
    asa=fit(box(0,0,300,40.0),[c,Lr]+sup); b=bolsao(asa)
    return dict(verdes=[com_furo(c,bf(led,0.2))]+sup+[com_furo(asa,b),M(com_furo(asa,b))],led=led,ilhas=[bf(b,-0.5),M(bf(b,-0.5))],
                nota='LED curto (90 x 19) num hexágono pequeno embaixo, no centro. Em cima, uma faixa corrida de ponta a ponta (2 metades emendadas no centro). Asas com bolsão dos lados do LED.')
VERS=[('A — Igual à lateral (LED 120 mm)',V1),('B — Hexágono largo (LED 180 mm)',V2),('C — Seta central (LED 200 mm)',V3),('D — Faixa de cima corrida (LED 90 mm)',V4)]
def pp(ax,g,fc,ec='#0b0c0d',lw=0.8,z=2):
    for p in [q for q in (g.geoms if hasattr(g,'geoms') else [g]) if not q.is_empty and q.area>1]:
        verts=[];codes=[]
        for r in [p.exterior]+list(p.interiors):
            c=np.array(r.coords); verts+=c.tolist(); codes+=[Path.MOVETO]+[Path.LINETO]*(len(c)-2)+[Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts,codes),fc=fc,ec=ec,lw=lw,zorder=z))
fig,axs=plt.subplots(4,1,figsize=(13,13))
for ax,(t,fn) in zip(axs,VERS):
    D=fn(); D['verdes']=[g for g in D['verdes'] if not g.is_empty and g.area>20]
    pp(ax,box(-300,0,300,81),'#26292c','#000',0.6,0); pp(ax,box(-300,81,300,97),'#c9a6e0','#000',0.5,0)
    pp(ax,cants,'#1b1d1f','#000',0.9,3)
    for g in D['verdes']:
        for q in (g.geoms if hasattr(g,'geoms') else [g]):
            pp(ax,q,'#3aa857' if q.contains(D['led'].centroid) else ('#2f9449' if q.centroid.y>42 else '#45b862'))
    pp(ax,D['led'],'#ffc23d','#3a2a00',0.8,4)
    for il in D['ilhas']:
        pp(ax,il,'#1a1c1e','#000',0.6,3); pp(ax,grade(il),'#0a0b0c','#000',0.4,4)
    big=max(max(q.bounds[2]-q.bounds[0],q.bounds[3]-q.bounds[1]) for g in D['verdes'] for q in (g.geoms if hasattr(g,'geoms') else [g]))
    ax.set_xlim(-298,298); ax.set_ylim(-1,97); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(t,fontsize=12,loc='left',fontweight='bold')
    ax.text(-296,-9,D['nota'],fontsize=9,va='top',wrap=True)
    n=sum(len(g.geoms) if hasattr(g,'geoms') else 1 for g in D['verdes']); print(t,'verdes',n,'maior',round(big,1))
plt.tight_layout(h_pad=3.5); plt.savefig('frente_versoes.png',dpi=110,facecolor='#e9ebe6')
