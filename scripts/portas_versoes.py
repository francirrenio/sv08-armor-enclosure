# PORTAS: 3 versoes da moldura (vista de frente), no padrao preto estrutural + verde estetico (0,5 acima, vao 0,5-1,0, friso).
# Porta D: X 1,5-234,5, Y 82-531,5; janela do acrilico X 9,5-222,5, Y 94-519,5 com cantos de 25 mm (como no Fusion). A E e espelho.
import numpy as np, textwrap, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from shapely.geometry import Polygon, box
from shapely.ops import unary_union as uu
from shapely import affinity
M=lambda g:affinity.scale(g,-1,1,origin=(0,0))
def op(g,r): return g.buffer(-r,join_style=1).buffer(r,join_style=1) if r>0 else g
def bf(g,d): return g.buffer(d,join_style=2)
def octo(x0,y0,x1,y1,c): return Polygon([(x0+c,y0),(x1-c,y0),(x1,y0+c),(x1,y1-c),(x1-c,y1),(x0+c,y1),(x0,y1-c),(x0,y0+c)])
def pp(ax,g,fc,ec='#0b0c0d',lw=0.8,z=2):
    for p in [q for q in (g.geoms if hasattr(g,'geoms') else [g]) if not q.is_empty and q.area>0.3]:
        verts=[];codes=[]
        for r in [p.exterior]+list(p.interiors):
            c=np.array(r.coords); verts+=c.tolist(); codes+=[Path.MOVETO]+[Path.LINETO]*(len(c)-2)+[Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts,codes),fc=fc,ec=ec,lw=lw,zorder=z))
def bolts(ax,P):
    for x,y in P:
        for s in (1,-1): ax.add_patch(plt.Circle((s*x,y),2.3,fc='#c43b3b',ec='#000',lw=.4,zorder=9))
OUT=box(1.5,82,234.5,531.5); PRE='#1f2124'; V1c='#3aa857'; V2c='#2f9449'; ACR='#cfe8f3'
def contexto(ax):
    for s in (1,-1):
        pp(ax,box(min(s*235.5,s*286),81,max(s*235.5,s*286),532),'#2f9449','#000',0.6,1)
        pp(ax,box(min(s*268,s*286),81,max(s*268,s*286),532),'#2b5fd0','#000',0.4,1)
    pp(ax,box(-296,0,296,81),'#26292c','#000',0.6,1); pp(ax,box(-296,532,296,634),'#26292c','#000',0.6,1)
    pp(ax,box(-225,540,225,554),'#141516','#000',0.4,2)
def porta(ax,jan,verdes,furos,pux):
    for s in (1,-1):
        f=OUT.difference(jan); f=f if s>0 else M(f)
        pp(ax,f,PRE,'#000',0.8,3); pp(ax,jan if s>0 else M(jan),ACR,'#7aa',0.5,2)
        for g in verdes:
            c=V1c if g.area>1500 else V2c
            pp(ax,g if s>0 else M(g),c,'#0b0c0d',0.8,5)
        pp(ax,pux if s>0 else M(pux),'#141516','#000',0.7,6)
    bolts(ax,furos)
def D1(ax):
    jan=octo(9.5,94,222.5,519.5,25)
    cs=[]
    for (x0,y0,sx,sy) in ((1.5,82,1,1),(234.5,82,-1,1),(1.5,531.5,1,-1),(234.5,531.5,-1,-1)):
        L=box(min(x0,x0+sx*70),min(y0,y0+sy*70),max(x0,x0+sx*70),max(y0,y0+sy*70))
        cs.append(op(L.intersection(OUT).difference(bf(jan,1.0)).buffer(-1.0,join_style=2),1.5))
    pux=box(6,270,18,330)
    porta(ax,jan,cs,[(12,110),(222,110),(12,503),(222,503)],pux)
    return 'D1 — Moldura preta com cantos verdes','A moldura fica preta e fina, como no Fusion (janela grande, cantos de 25 mm). Os 4 cantos ganham uma peça verde em L que contorna o chanfro da janela, 0,5 mm acima do preto e com vão de 1 mm, presa por 1 parafuso. O puxador é preto, embutido na borda do meio.'
def D2(ax):
    jan=octo(20,106,212,508,30)
    fai=bf(jan,9.0).difference(bf(jan,1.0))
    cortes=uu([box(100,0,136,600),box(0,280,300,334)])
    vs=[g for g in (fai.difference(cortes).geoms) ]
    pux=box(4,280,16,324)
    porta(ax,jan,vs,[(116,99),(116,515),(10,307),(226,307)],pux)
    return 'D2 — Faixa verde em volta da janela','A moldura alarga (janela um pouco menor) e ganha uma faixa verde de 8 mm seguindo o contorno da janela, dividida em 4 peças com emendas no meio de cada lado. Os cantos chanfrados de 30 mm repetem o desenho das colunas. Puxador no meio da altura.'
def D3(ax):
    jan=octo(9.5,128,222.5,500,22)
    baixo=op(Polygon([(10,88),(226,88),(226,118),(200,122),(36,122),(10,118)]),3.0)
    cima=op(Polygon([(10,525),(226,525),(226,509),(36,506),(10,509)]),3.0)
    pux=box(3,262,15,338); vpx=op(box(1.5+1,250,22,350),2.0)
    porta(ax,jan,[baixo.difference(bf(jan,1.0)),cima.difference(bf(jan,1.0))],[(24,105),(212,105),(24,517),(212,517)],pux)
    return 'D3 — Trilhos largos em cima e embaixo','O trilho de baixo (40 mm) e o de cima (25 mm) ficam largos, com uma verde em cada um que continua a linha das faixas da base e do top hat; os lados ficam pretos e finos. A janela encolhe só na altura.'
fig,axs=plt.subplots(1,3,figsize=(21,10.5))
for ax,f in zip(axs,(D1,D2,D3)):
    contexto(ax); t,n=f(ax)
    ax.set_xlim(-300,300); ax.set_ylim(-5,640); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(t,fontsize=13,loc='left',fontweight='bold'); ax.text(-300,-25,textwrap.fill(n,92),fontsize=9,va='top')
plt.tight_layout(); plt.subplots_adjust(bottom=0.2); plt.savefig('portas_versoes.png',dpi=110)
