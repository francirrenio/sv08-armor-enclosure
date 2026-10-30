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

def base(ax):
    pp(ax,box(-XI,YS,XI,Y1),'#26292c','#000',0.6,1); pp(ax,box(-XI,Y0,XI,YS),'#1f2124','#000',0.6,1)
    pp(ax,caps,'#1b1d1f','#000',0.9,3); pp(ax,mold.intersection(box(-400,470,400,Y0)),'#c6a3df','#000',0.6,1)
def bolts(ax,P):
    for x,y in P: ax.add_patch(plt.Circle((x,y),2.4,fc='#c43b3b',ec='#000',lw=.4,zorder=7))
def tela(ax,g):
    pp(ax,g,'#060708','#000',0.7,7); x0,y0,x1,y1=g.bounds
    pp(ax,box(x0+3,y1-6,x0+(x1-x0)*0.45,y1-3),'#16191c','none',0,8)          # reflexo
def linha(ax,p,cor='#2a8a44'):   # rebaixo de 1 mm (linha de sombra) dentro da verde, igual ao painel do modelo antigo
    pp(ax,bf(p,-7.0),cor,'#0b0c0d',0.6,6)
def corte3(xa,xb,wide_left=True):
    m=hexa(xa,xb,G0,G1)                                    # peca do meio com as 2 pontas na diagonal
    e=fit(box(-300,G0,xa+30,G1),[m,caps]); d=fit(box(xb-30,G0,300,G1),[m,caps])
    return e,m,d
def janela(p,mx=10.0,my=8.0):
    _,y0,x1,y1=p.bounds; xm=p.intersection(box(-1e3,YC-0.01,1e3,YC+0.01)).bounds[0]   # fundo do V
    return op(box(xm+mx,y0+my,x1-17.0,y1-my),3.0)
def faixa3(ax,cuts=(-110.0,120.0)):
    xs=[-XI+6]+list(cuts)+[XI-6]; P=[]
    for a,b in zip(xs[:-1],xs[1:]):
        g=op(box(a+2,537,b-2,553),3.0); pp(ax,g,'#2f9449','#0b0c0d',0.7,5); P+=[(a+14,545),(b-14,545)]
    bolts(ax,P)
def D1(ax):
    base(ax); e,m,d=corte3(-30,44)
    pp(ax,e,'#3aa857','#0b0c0d',0.8,5); linha(ax,e); pp(ax,m,'#2f9449','#0b0c0d',0.8,5); pp(ax,d,'#3aa857','#0b0c0d',0.8,5); tela(ax,janela(d))
    bolts(ax,[(-215,570),(-215,622),(-50,570),(-50,622),(7,576),(7,616),(226,570),(226,622)])
    return 'D1 — Como o antigo, no estilo novo','Três divisões: painel largo à esquerda (com o rebaixo de 1 mm por dentro, como no antigo), uma peça estreita no meio com as duas pontas na diagonal e o display à direita, na própria verde. As emendas são em V, com vão de 4 mm.'
def D2(ax):
    base(ax); e,m,d=corte3(-78,78)
    for g,c in ((e,'#3aa857'),(m,'#2f9449'),(d,'#3aa857')): pp(ax,g,c,'#0b0c0d',0.8,5)
    linha(ax,e); tela(ax,janela(d,mx=11,my=8))
    bolts(ax,[(-215,570),(-215,622),(-100,570),(-100,622),(-45,570),(45,570),(-45,622),(45,622),(226,570),(226,622)])
    return 'D2 — Três partes iguais','Três divisões de tamanho parecido: esquerda com rebaixo, centro liso (hexágono como o da logo, mais curto) e o display à direita. Fica mais equilibrado que o antigo.'
def D3(ax):
    t=D1(ax); faixa3(ax)
    return 'D3 — D1 + faixa de baixo em 3','A D1 com a banda de baixo também em 3 verdes finas (como no antigo). As emendas da faixa ficam desencontradas das de cima (mais de 50 mm), uma travando a outra.'
def D4(ax):
    base(ax); e,m,d=corte3(-78,78)
    fil=[hexa(-52,-4,YC-3.5,YC+3.5,1.5)]; fil.append(M(fil[0]))
    pp(ax,e,'#3aa857','#0b0c0d',0.8,5); linha(ax,e)
    pp(ax,Polygon(m.exterior.coords,[f.exterior.coords for f in fil]),'#2f9449','#0b0c0d',0.8,5)
    for f in fil: pp(ax,f,'#ffffff','#0b0c0d',0.7,6)
    pp(ax,d,'#3aa857','#0b0c0d',0.8,5); tela(ax,janela(d)); faixa3(ax,(-140.0,140.0))
    bolts(ax,[(-215,570),(-215,622),(-100,570),(-100,622),(226,570),(226,622)])
    return 'D4 — D2 com filetes de luz + faixa em 3','A D2 com os dois filetes de luz da logo na peça do meio e a banda de baixo em 3 verdes finas, emendas desencontradas das de cima.'
fig,axs=plt.subplots(4,1,figsize=(13,15))
for ax,fn in zip(axs,(D1,D2,D3,D4)):
    t,n=fn(ax); ax.set_xlim(-300,300); ax.set_ylim(474,640); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(t,fontsize=12,loc='left',fontweight='bold'); ax.text(-298,468,n,fontsize=9,va='top',wrap=True)
plt.tight_layout(h_pad=3.0); plt.savefig('topo_frente_div3.png',dpi=100,facecolor='#e9ebe6'); print('ok')
