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
def bolts(ax,P,r=2.4):
    for x,y in P: ax.add_patch(plt.Circle((x,y),r,fc='#c43b3b',ec='#000',lw=.4,zorder=7))
def case7(ax,xc,yc,w=184.0,h=116.0):   # case externa do display 7" (so ilustracao)
    c=op(box(xc-w/2,yc-h/2,xc+w/2,yc+h/2),8.0); pp(ax,c,'#1b1d20','#000',0.9,20)
    pp(ax,Polygon(c.exterior.coords,[bf(c,-2.0).exterior.coords]),'#3aa857','#0b0c0d',0.5,21)
    scr=op(box(xc-77,yc-43+4,xc+77,yc+43+4),2.0); pp(ax,scr,'#07090b','#000',0.6,22)
    pp(ax,box(xc-70,yc+30,xc-10,yc+36),'#e8f5ec','none',0,23); pp(ax,box(xc-70,yc-34,xc+70,yc-30),'#1d3326','none',0,23); pp(ax,box(xc-70,yc-34,xc+20,yc-30),'#45d06b','none',0,23)
    for i,(t,cl) in enumerate((('245°','#ff9b3d'),('100°','#3fb6ff'),('62°','#e8f5ec'))): ax.text(xc-66+i*48,yc+4,t,color=cl,fontsize=10,fontweight='bold',va='center',zorder=24)

YB=Y0+4.0; YT_=Y1-4.0
def base(ax):
    pp(ax,box(-XI,Y0,XI,Y1),'#26292c','#000',0.6,1); pp(ax,caps,'#1b1d1f','#000',0.9,3); pp(ax,mold.intersection(box(-400,470,400,Y0)),'#c6a3df','#000',0.6,1)
def trilho(ax,y0,y1):
    pp(ax,box(-XI+8,y0,XI-8,y1),'#141516','#000',0.7,5)
    for x in np.arange(-XI+16,XI-12,10.0): pp(ax,box(x,y0+1.5,x+4,y1-1.5),'#060606','#000',0.2,6)
    for e in (box(XI-16,y0-2,XI-4,y1+2),box(-XI+4,y0-2,-XI+16,y1+2)): pp(ax,e,'#2f9449','#0b0c0d',0.6,7)
def faixa(ax,y0,y1,cut,cor='#3aa857',bol=None):
    g=fit(box(-XI,y0,XI,y1),[caps]); P=[]
    for h in (g.intersection(box(-400,0,cut-2,700)),g.intersection(box(cut+2,0,400,700))):
        h=op(h,4.0)
        if bol is not None:
            for b in bol:
                if h.contains(b): h=Polygon(h.exterior.coords,[b.exterior.coords])
        pp(ax,h,cor,'#0b0c0d',0.7,5); x0,_,x1,_=h.bounds; P+=[(x0+14,(y0+y1)/2),(x1-14,(y0+y1)/2)]
    return P
def bolsoes(ax,yc,hb=12.0):
    B=[]
    for s_ in (1,-1):
        b=hexa(150,206,yc-hb,yc+hb,4.0); b=b if s_>0 else M(b); il=bf(b,-0.5)
        pp(ax,bf(b,-0.01),'#26292c','none',0,6); pp(ax,il,'#141516','#000',0.6,7); pp(ax,grade(il),'#050506','#000',0.3,8); B.append(b)
    return B
def T1(ax,disp=None):
    base(ax); yr0,yr1=576.0,590.0; trilho(ax,yr0,yr1)
    P=faixa(ax,YB,yr0-4,-40.0)+faixa(ax,yr1+4,YT_,40.0)
    bolts(ax,P)
    if disp is not None: case7(ax,disp,583.0)
    return 'T1 — Trilho no meio, verdes iguais','Toda a frente vira verde: uma faixa embaixo (Y 535-572) e outra em cima (Y 594-630), com o trilho no meio. Cada faixa em 2 peças; a emenda de cima e a de baixo ficam 80 mm desencontradas.'
def T2(ax,disp=None):
    base(ax); yr0,yr1=608.0,622.0; trilho(ax,yr0,yr1)
    P=faixa(ax,YB,yr0-4,0.0)+faixa(ax,yr1+4,YT_,-60.0,'#2f9449'); B=bolsoes(ax,569.0,13.0)
    bolts(ax,[p for p in P if abs(p[1]-569)>1]+[(-120,550),(120,550),(-120,590),(120,590)])
    if disp is not None: case7(ax,disp,583.0)
    return 'T2 — Trilho em cima (rack de teto) + bolsões','O trilho sobe para perto do topo, como um rack de teto. Embaixo, uma verde grande (Y 535-604) com os bolsões de grade da base e da lateral dos lados. A case fica no meio da altura, presa no trilho por cima.'
def T3(ax,disp=None):
    base(ax); yr0,yr1=540.0,554.0; trilho(ax,yr0,yr1)
    c=hexa(-112,112,yr1+4,YT_); a=fit(box(0,yr1+4,300,YT_),[c,caps])
    for g,cl in ((c,'#3aa857'),(a,'#2f9449'),(M(a),'#2f9449')): pp(ax,g,cl,'#0b0c0d',0.8,5)
    bolts(ax,[(-80,566),(80,566),(-80,622),(80,622),(150,566),(-150,566),(205,622),(-205,622)])
    if disp is not None: case7(ax,disp,590.0)
    return 'T3 — Trilho embaixo (para-choque) + hexágono','O trilho desce para logo acima da porta, como um para-choque. Em cima, o hexágono verde central (como o da logo) e as verdes dos lados com a ponta para o centro. A case apoia no trilho e cobre parte da verde.'
fig=plt.figure(figsize=(15,12)); gs=fig.add_gridspec(3,2,hspace=.55,wspace=.04)
for i,fn in enumerate((T1,T2,T3)):
    for j,disp in enumerate((None,0.0,128.0)[0:1]+((128.0,) if i!=1 else (0.0,))):
        ax=fig.add_subplot(gs[i,j]); t,n=fn(ax,disp); ax.set_xlim(-300,300); ax.set_ylim(474,662); ax.set_aspect('equal'); ax.axis('off')
        ax.set_title((t+'   ·   sem display') if j==0 else 'com o display (case por fora)',fontsize=11,loc='left',fontweight='bold' if j==0 else 'normal')
        if j==0: ax.text(-298,466,n,fontsize=8.6,va='top',wrap=True)
plt.savefig('topo_frente_trilho2.png',dpi=100,facecolor='#e9ebe6',bbox_inches='tight'); print('ok')
