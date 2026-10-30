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
# ---- R1: trilho de acessorios (tipo picatinny) de ponta a ponta ----
YR0,YR1=589.0,603.0
def R1(ax,disp=None):
    base(ax)
    rail=box(-XI+8,YR0,XI-8,YR1); pp(ax,rail,'#141516','#000',0.7,5)
    for x in np.arange(-XI+16,XI-12,10.0): pp(ax,box(x,YR0+1.5,x+4,YR1-1.5),'#060606','#000',0.2,6)
    for s_ in (1,-1):
        for e in (box(XI-16,YR0-2,XI-4,YR1+2),): pp(ax,e if s_>0 else M(e),'#2f9449','#0b0c0d',0.6,7)   # ponteiras verdes
    up=fit(box(-XI,YR1+4,XI,G1),[caps]); lo=fit(box(-XI,G0,XI,YR0-4),[caps])
    for g,cut in ((up,40.0),(lo,-40.0)):
        for h in (g.intersection(box(-400,0,cut-2,700)),g.intersection(box(cut+2,0,400,700))): pp(ax,op(h,4.0),'#3aa857','#0b0c0d',0.7,5)
    bolts(ax,[(-200,618),(-60,618),(80,618),(200,618),(-200,574),(-80,574),(60,574),(200,574)])
    if disp is not None: case7(ax,disp,YC+8)
def R1n(): return 'R1 — Trilho de acessórios (off-road)','Um trilho preto com rasgos (tipo picatinny) de ponta a ponta no meio do topo, com ponteiras verdes. Em cima e embaixo, faixas verdes finas. Sem display, o trilho é a linha de estilo. O display (ou uma câmera, uma luz) prende no trilho com uma trava rápida, em qualquer posição: centro ou direita.'
# ---- R2: tres medalhoes iguais com tampa ----
def R2(ax,disp=None):
    base(ax); cs=[-150.0,0.0,150.0]; meds=[hexa(c-58,c+58,G0,G1) for c in cs]
    band=op(box(-XI,G0+16,XI,G1-16).difference(uu([bf(v,GAP) for v in [caps]+meds])),3.0)
    for g in (band.geoms if hasattr(band,'geoms') else [band]): pp(ax,g,'#2f9449','#0b0c0d',0.6,4)
    for c,m in zip(cs,meds):
        t=bf(m,-7.0); pp(ax,m,'#3aa857','#0b0c0d',0.8,5); pp(ax,t,'#141516','#000',0.6,6); pp(ax,grade(bf(t,-1.0),n=5,w=2.6),'#050506','#000',0.3,7)
        bolts(ax,[(c-40,G0+5.5),(c+40,G0+5.5),(c-40,G1-5.5),(c+40,G1-5.5)],2.0)
    if disp is not None: case7(ax,disp,YC+8)
def R2n(): return 'R2 — Três medalhões com tampa','Três hexágonos verdes iguais (esquerda, centro, direita), ligados por uma faixa verde. Cada um tem uma tampa preta com a grade em relevo, presa por 4 parafusos. Para usar o display, troca a tampa do centro ou da direita pela base da case, nos mesmos 4 insertos. Sem display, fica simétrico e acabado.'
# ---- R3: viseira no topo ----
def R3(ax,disp=None):
    base(ax)
    vis=box(-XI,G1-2,XI,Y1); pp(ax,vis,'#141516','#000',0.7,6); pp(ax,box(-XI,G1-2,XI,G1-0.5),'#000','none',0,7)
    for x in (-150.0,0.0,150.0): pp(ax,box(x-14,G1+0.5,x+14,Y1-1.5),'#3aa857','#0b0c0d',0.5,8)
    c=hexa(-112,112,G0,G1-6); a=fit(box(0,G0,300,G1-6),[c,caps])
    for g,cl in ((c,'#3aa857'),(a,'#2f9449'),(M(a),'#2f9449')): pp(ax,g,cl,'#0b0c0d',0.8,5)
    bolts(ax,[(-80,G0+8),(80,G0+8),(150,G0+10),(-150,G0+10)])
    if disp is not None: case7(ax,disp,YC+8)
def R3n(): return 'R3 — Viseira no topo','O topo vira uma viseira preta saliente (8 mm) com um encaixe por baixo, de ponta a ponta. A case do display engancha nela por cima e encosta na verde, em qualquer posição. Sem display, a viseira faz uma sombra forte sobre as verdes, com 3 marcas verdes por cima.'
fig=plt.figure(figsize=(15,12)); gs=fig.add_gridspec(3,2,hspace=.55,wspace=.04)
for i,(fn,nf) in enumerate(((R1,R1n),(R2,R2n),(R3,R3n))):
    for j,disp in enumerate((None,150.0 if i==1 else 120.0)):
        ax=fig.add_subplot(gs[i,j]); fn(ax,disp); ax.set_xlim(-300,300); ax.set_ylim(474,662); ax.set_aspect('equal'); ax.axis('off')
        t,n=nf()
        ax.set_title((t if j==0 else '')+('   ·   sem display' if j==0 else 'com o display (case por fora)'),fontsize=11,loc='left',fontweight='bold' if j==0 else 'normal')
        if j==0: ax.text(-298,466,n,fontsize=8.6,va='top',wrap=True)
plt.savefig('topo_frente_trilho.png',dpi=100,facecolor='#e9ebe6',bbox_inches='tight'); print('ok')
