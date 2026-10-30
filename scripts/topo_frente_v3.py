# Topo da frente v2: display montado (visto pronto). Encaixe por tras (o modulo entra por dentro do top hat): a frente fica limpa.
import pickle, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from shapely.geometry import Polygon, box
from shapely.ops import unary_union as uu
exec(open('geo.py').read())
_fv=open('frente_versoes.py').read(); exec(_fv.split('VERS=[')[0])
CT=pickle.load(open('CT.pkl','rb'))
s=section_polys(CT['cant_top_F'],'z',290.0); cap=max((s.geoms if hasattr(s,'geoms') else [s]),key=lambda q:q.area); caps=uu([cap,M(cap)])
mold=section_polys(CT['porta_mold2'],'z',285.5); mold=uu([mold,M(mold)])
Y0,Y1,YS=531.5,634.0,558.5; XI=235.0; YC=596.0; G0,G1=562.0,630.0
def pp(ax,g,fc,ec='#0b0c0d',lw=0.8,z=2,a=1):
    for p in [q for q in (g.geoms if hasattr(g,'geoms') else [g]) if not q.is_empty and q.area>0.2]:
        verts=[];codes=[]
        for r in [p.exterior]+list(p.interiors):
            c=np.array(r.coords); verts+=c.tolist(); codes+=[Path.MOVETO]+[Path.LINETO]*(len(c)-2)+[Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts,codes),fc=fc,ec=ec,lw=lw,zorder=z,alpha=a))
def tela(ax,x0,x1,y0,y1):   # display ligado (so ilustracao)
    w=x1-x0; h=y1-y0
    pp(ax,op(box(x0,y0,x1,y1),2.5),'#07090b','#000',0.6,8)
    pp(ax,box(x0+4,y1-9,x0+4+w*0.35,y1-5),'#e8f5ec','none',0,9)
    pp(ax,box(x0+4,y0+5,x1-4,y0+8),'#1d3326','none',0,9); pp(ax,box(x0+4,y0+5,x0+4+(w-8)*0.62,y0+8),'#45d06b','none',0,9)
    for i,(t,c) in enumerate((('245°','#ff9b3d'),('100°','#3fb6ff'),('62°','#e8f5ec'))):
        ax.text(x0+6+i*w/3.2,y0+h*0.48,t,color=c,fontsize=9,fontweight='bold',va='center',zorder=10)
    ax.text(x1-5,y1-7,'62%',color='#9fdcb0',fontsize=6.5,ha='right',va='center',zorder=10)
def base(ax):
    pp(ax,box(-XI,YS,XI,Y1),'#26292c','#000',0.6,1); pp(ax,box(-XI,Y0,XI,YS),'#1f2124','#000',0.6,1)
    pp(ax,caps,'#1b1d1f','#000',0.9,3); pp(ax,mold.intersection(box(-400,470,400,Y0)),'#c6a3df','#000',0.6,1)
def bolts(ax,P):
    for x,y in P: ax.add_patch(plt.Circle((x,y),2.4,fc='#c43b3b',ec='#000',lw=.4,zorder=7))
def asas(cx):   # verdes dos lados ate a cantoneira, ponta na diagonal apontando para o centro (como a frente de baixo)
    d=fit(box(0,G0,300,G1),[cx,caps]); return [d,M(d)]

def lados_grade(ax,c):
    for s_ in (1,-1):
        a=fit(box(0,G0,300,G1),[c,caps]); b=hexa(150,205,YC-12,YC+12,4.0); ilha=bf(b,-0.5); A=Polygon(a.exterior.coords,[b.exterior.coords])
        for g,fc in ((A,'#2f9449'),(ilha,'#141516')): pp(ax,g if s_>0 else M(g),fc,'#0b0c0d',0.7,5)
        gr=grade(ilha); pp(ax,gr if s_>0 else M(gr),'#050506','#000',0.3,6)
def F1(ax):
    base(ax); c=hexa(-112,112,G0,G1); pp(ax,c,'#3aa857','#0b0c0d',0.8,5)
    for g in asas(c): pp(ax,g,'#2f9449','#0b0c0d',0.8,5)
    bolts(ax,[(-80,G0+8),(80,G0+8),(-80,G1-8),(80,G1-8),(150,G0+10),(-150,G0+10),(205,G1-10),(-205,G1-10)])
    return 'F1 — Hexágono central liso','Hexágono verde no centro, do mesmo tamanho e forma do da logo embaixo, sem nada dentro. Dos lados, verdes com a ponta na diagonal apontando para o centro. É o mais limpo.'
def F2(ax):
    base(ax); c=hexa(-112,112,G0,G1); fil=[hexa(-86,-6,YC-3.5,YC+3.5,1.5)]; fil.append(M(fil[0]))
    pp(ax,Polygon(c.exterior.coords,[f.exterior.coords for f in fil]),'#3aa857','#0b0c0d',0.8,5)
    for f in fil: pp(ax,f,'#ffffff','#0b0c0d',0.7,6)
    for g in asas(c): pp(ax,g,'#2f9449','#0b0c0d',0.8,5)
    bolts(ax,[(-80,G0+8),(80,G0+8),(-80,G1-8),(80,G1-8),(150,G0+10),(-150,G0+10),(205,G1-10),(-205,G1-10)])
    return 'F2 — Hexágono central com filetes de luz','Igual à F1, com os mesmos dois filetes de luz brancos da logo de baixo (fita ARGB atrás). À noite, a frente acende em cima e embaixo com o mesmo desenho.'
def F3(ax):
    base(ax); c=hexa(-112,112,G0,G1); pp(ax,c,'#3aa857','#0b0c0d',0.8,5); lados_grade(ax,c)
    bolts(ax,[(-80,G0+8),(80,G0+8),(-80,G1-8),(80,G1-8)])
    return 'F3 — Hexágono central + bolsões com grade','Hexágono liso no centro e, nas verdes dos lados, o mesmo bolsão com grade das asas de baixo e da lateral. Repete no topo as peças da base.'
def F4(ax):
    base(ax); c=hexa(-112,112,G0,G1); ab=op(box(-80,571,80,621),2.5)
    pp(ax,Polygon(c.exterior.coords,[ab.exterior.coords]),'#3aa857','#0b0c0d',0.8,5); pp(ax,ab,'#0d0e0f','#000',0.5,5)
    for y in np.arange(574,618,8.0): pp(ax,box(-80,y,80,y+3.0),'#5a5e63','#000',0.4,6)
    for g in asas(c): pp(ax,g,'#2f9449','#0b0c0d',0.8,5)
    bolts(ax,[(-95,G0+8),(95,G0+8),(-95,G1-8),(95,G1-8),(150,G0+10),(-150,G0+10),(205,G1-10),(-205,G1-10)])
    return 'F4 — Hexágono central com aletas','O hexágono do centro vira a moldura de uma janela de aletas (160 x 50), igual às da lateral e da traseira. A exaustão fica também na frente, centralizada.'
fig,axs=plt.subplots(4,1,figsize=(13,15))
for ax,fn in zip(axs,(F1,F2,F3,F4)):
    t,n=fn(ax); ax.set_xlim(-300,300); ax.set_ylim(474,640); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(t,fontsize=12,loc='left',fontweight='bold'); ax.text(-298,468,n,fontsize=9,va='top',wrap=True)
plt.tight_layout(h_pad=3.0); plt.savefig('topo_frente_v3.png',dpi=100,facecolor='#e9ebe6'); print('ok')
