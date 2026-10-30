# TRASEIRA DE BAIXO (faixa da base, Y 0-81, face Z -286), vista de tras: 4 versoes no estilo da frente e das laterais,
# com a tomada AS03 (janela 48,6 x 28 + 2 furos, a mesma da base original)
import pickle, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from shapely.geometry import Polygon, box
from shapely.ops import unary_union as uu
exec(open('geo.py').read())
_fv=open('frente_versoes.py').read(); exec(_fv.split('VERS=[')[0])
RL=pickle.load(open('RL.pkl','rb'))
s=section_polys(RL['cantoneira_T_L'],'z',-288.0); Lr2=max((s.geoms if hasattr(s,'geoms') else [s]),key=lambda q:q.area)
Lr=Lr2 if Lr2.centroid.x>0 else M(Lr2); cants=uu([Lr,M(Lr)])
def pp(ax,g,fc,ec='#0b0c0d',lw=0.8,z=2):
    for p in [q for q in (g.geoms if hasattr(g,'geoms') else [g]) if not q.is_empty and q.area>0.3]:
        verts=[];codes=[]
        for r in [p.exterior]+list(p.interiors):
            c=np.array(r.coords); verts+=c.tolist(); codes+=[Path.MOVETO]+[Path.LINETO]*(len(c)-2)+[Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts,codes),fc=fc,ec=ec,lw=lw,zorder=z))
def bolts(ax,P):
    for x,y in P: ax.add_patch(plt.Circle((x,y),2.3,fc='#c43b3b',ec='#000',lw=.4,zorder=9))
def as03(ax,xc,yc):
    j=box(xc-24.3,yc-14,xc+24.3,yc+14); pp(ax,j,'#0a0a0a','#000',0.6,8)
    pp(ax,box(xc-17,yc-9,xc+5,yc+9),'#2a2a2a','#555',0.5,9)                           # tomada
    pp(ax,box(xc+8,yc-8,xc+20,yc+8),'#b02020','#300',0.5,9)                           # chave
    for dx in (-32.0,32.0): ax.add_patch(plt.Circle((xc+dx,yc),2.0,fc='#0a0a0a',ec='#000',lw=.4,zorder=8))
def base(ax):
    pp(ax,box(-260,0,260,81),'#26292c','#000',0.6,1); pp(ax,cants,'#1b1d1f','#000',0.9,3)
def ilha(ax,b):
    il=bf(b,-0.5); pp(ax,il,'#1a1c1e','#000',0.6,4); pp(ax,grade(il),'#0a0b0c','#000',0.4,5)
def B1(ax):
    base(ax); c=hexa(-100,100,4,72); ls,il=lados(c)
    pp(ax,Polygon(c.exterior.coords,[box(-36,24,36,52).exterior.coords]),'#3aa857'); pp(ax,box(-36,24,36,52),'#121314','#000',0.6,4); as03(ax,0,38)
    for g in ls: pp(ax,g,'#2f9449' if g.centroid.y>42 else '#45b862')
    for i_ in il: pp(ax,i_,'#1a1c1e','#000',0.6,4); pp(ax,grade(i_),'#0a0b0c','#000',0.4,5)
    bolts(ax,[(-72,12),(72,12),(-72,62),(72,62)])
    return 'B1 — Igual à frente, com a tomada no hexágono','O mesmo desenho da frente de baixo: hexágono central (no lugar da logo, a tomada AS03 num rebaixo preto), faixa de cima e asas com bolsão nos 2 lados. As linhas da frente e da lateral dão a volta completa na impressora.'
def B2(ax):
    base(ax); c=hexa(-100,100,4,72); ls,il=lados(c)
    pp(ax,c,'#3aa857'); bolts(ax,[(-72,12),(72,12),(-72,62),(72,62)])
    for g in ls: pp(ax,g,'#2f9449' if g.centroid.y>42 else '#45b862')
    # tomada no bolsao da direita (vista de tras)
    for k,i_ in enumerate(il):
        if i_.centroid.x<0: pp(ax,i_,'#1a1c1e','#000',0.6,4); pp(ax,grade(i_),'#0a0b0c','#000',0.4,5)
        else: pp(ax,i_,'#1a1c1e','#000',0.6,4); as03(ax,i_.centroid.x,i_.centroid.y)
    return 'B2 — Hexágono liso, tomada no bolsão','Hexágono central liso. A tomada AS03 fica dentro do bolsão de uma das asas; o bolsão do outro lado mantém a grade. O centro fica limpo e a tomada perto do canto, onde chega o cabo.'
def B3(ax):
    base(ax)
    sup=fit(box(-300,43,300,66),[cants]); sup=[op(sup.intersection(box(-300,0,-2,100)),R),op(sup.intersection(box(2,0,300,100)),R)]
    inf=fit(box(-300,0,300,39),[cants]); inf=[op(inf.intersection(box(-300,-1,-2,100)),R),op(inf.intersection(box(2,-1,300,100)),R)]
    for g in sup: pp(ax,g,'#2f9449')
    for g in inf:
        b=hexa(g.centroid.x-60,g.centroid.x+60,7,33,5.0); pp(ax,Polygon(g.exterior.coords,[b.exterior.coords]),'#45b862'); ilha(ax,b)
    as03(ax,0,56)
    return 'B3 — Faixas corridas (sem hexágono)','Duas faixas verdes corridas (cima e baixo), cada uma em 2 metades, com bolsões de grade (ventilação da eletrônica da base). A tomada AS03 fica no centro, na faixa de cima. Visual mais técnico.'
def B4(ax):
    base(ax); c=hexa(-70,70,8,66); ls,il=lados(c)
    pp(ax,c,'#3aa857'); bolts(ax,[(-48,14),(48,14),(-48,60),(48,60)])
    for g in ls: pp(ax,g,'#2f9449' if g.centroid.y>42 else '#45b862')
    for i_ in il: pp(ax,i_,'#1a1c1e','#000',0.6,4); pp(ax,grade(i_),'#0a0b0c','#000',0.4,5)
    j=box(-24.3,24,24.3,52); pp(ax,Polygon(c.exterior.coords,[bf(j,3).exterior.coords]),'#3aa857'); as03(ax,0,38)
    return 'B4 — Igual à lateral (hexágono menor)','Hexágono central menor, do tamanho do da lateral, com a tomada AS03 no meio; faixa de cima e asas com bolsão como na lateral. Lateral e traseira ficam idênticas.'
fig,axs=plt.subplots(4,1,figsize=(13,13))
for ax,fn in zip(axs,(B1,B2,B3,B4)):
    t,n=fn(ax); ax.set_xlim(-300,300); ax.set_ylim(-2,100); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(t+'   (vista de trás)',fontsize=12,loc='left',fontweight='bold'); ax.text(-298,-8,n,fontsize=9,va='top',wrap=True)
plt.tight_layout(h_pad=3.5); plt.savefig('tras_base_versoes.png',dpi=100,facecolor='#e9ebe6'); print('ok')
