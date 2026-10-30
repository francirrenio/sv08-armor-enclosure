# TOPO DE TRAS (top hat), vista de tras: 4 versoes. Mesma altura e linhas da lateral (banda Y 529,5-558,5; riser 558,5-634),
# aletas nas posicoes do Fusion (aberturas X +-61,5 a +-188,5) e tampa do servo no centro.
import pickle, numpy as np, trimesh, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from shapely.geometry import Polygon, box
from shapely.ops import unary_union as uu
exec(open('geo.py').read())
_fv=open('frente_versoes.py').read(); exec(_fv.split('VERS=[')[0])     # hexa, op, bf, K, R, M, fit
TD_='/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/'
s=section_polys(trimesh.load(TD_+'054.stl'),'z',-290.0); cap=max((s.geoms if hasattr(s,'geoms') else [s]),key=lambda q:q.area)
caps=uu([cap,M(cap)])
Y0,YS,Y1=529.5,558.5,634.0; XI=234.0; YC=596.0
def pp(ax,g,fc,ec='#0b0c0d',lw=0.8,z=2):
    for p in [q for q in (g.geoms if hasattr(g,'geoms') else [g]) if not q.is_empty and q.area>0.3]:
        verts=[];codes=[]
        for r in [p.exterior]+list(p.interiors):
            c=np.array(r.coords); verts+=c.tolist(); codes+=[Path.MOVETO]+[Path.LINETO]*(len(c)-2)+[Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts,codes),fc=fc,ec=ec,lw=lw,zorder=z))
def bolts(ax,P):
    for x,y in P: ax.add_patch(plt.Circle((x,y),2.3,fc='#c43b3b',ec='#000',lw=.4,zorder=9))
def aletas(ax,xc,w=127.0,y0=569.0,y1=623.8):
    a=box(xc-w/2,y0,xc+w/2,y1); pp(ax,a,'#0d0e0f','#000',0.5,4)
    for y in np.arange(y0+3,y1-2,13.7): pp(ax,box(xc-w/2,y,xc+w/2,y+8),'#5a5e63','#000',0.4,5)
    return a
def base(ax):
    pp(ax,box(-XI,YS,XI,Y1),'#26292c','#000',0.6,1); pp(ax,box(-XI,Y0,XI,YS),'#1f2124','#000',0.6,1)
    pp(ax,caps,'#1b1d1f','#000',0.9,3); ax.axhline(YS,color='#e0a020',lw=.6,ls='--',zorder=8)
    ax.text(298,YS+1.5,'linha da lateral',fontsize=7,color='#a0700a',ha='right')
XS=(-125.0,125.0)
def T1(ax):
    base(ax)
    for xc in XS:
        fr=op(box(xc-80,563,xc+80,629),3.0); ab=aletas(ax,xc); pp(ax,fr.difference(ab),'#3aa857','#0b0c0d',0.8,6)
        bolts(ax,[(xc-74,569),(xc+74,569),(xc-74,623),(xc+74,623)])
    pp(ax,op(box(-42,574,42,618),3.0),'#141516','#000',0.7,6); bolts(ax,[(-34,580),(34,580),(-34,612),(34,612)])
    return 'T1 — Igual à lateral','As mesmas 2 janelas de aletas da lateral, com a moldura verde de 160 x 66, e a tampa do servo preta no centro. A banda de baixo é lisa, na mesma linha da lateral, e as 4 faces do top hat ficam iguais.'
def T2(ax):
    base(ax)
    c=hexa(-48,48,563,629); pp(ax,c,'#3aa857','#0b0c0d',0.8,6); pp(ax,op(box(-30,580,30,612),2.0),'#141516','#000',0.5,7)
    for s_ in (1,-1):
        g=fit(box(0,563,300,629),[c,caps]); g=g if s_>0 else M(g); ab=aletas(ax,s_*125.0)
        pp(ax,g.difference(bf(ab,2.0)),'#2f9449','#0b0c0d',0.8,6)
    bolts(ax,[(-30,570),(30,570),(-30,622),(30,622),(-200,575),(200,575),(-200,617),(200,617)])
    return 'T2 — Hexágono do servo (linguagem da frente)','A tampa do servo vira um hexágono verde, como o da frente, com um rebaixo preto. Dos lados, verdes com a ponta voltada para o centro, abraçando as janelas das aletas. A traseira repete o desenho do topo da frente.'
def T3(ax):
    base(ax)
    for s_ in (1,-1):
        g=hexa(50,XI-6,563,629,R,pr=False); g=g if s_>0 else M(g); ab=aletas(ax,s_*125.0)
        pp(ax,g.difference(bf(ab,2.0)),'#3aa857','#0b0c0d',0.8,6)
    pp(ax,op(box(-42,574,42,618),3.0),'#141516','#000',0.6,7); bolts(ax,[(-34,580),(34,580),(-34,612),(34,612)])
    bolts(ax,[(-210,575),(210,575),(-210,617),(210,617),(-55,575),(55,575),(-55,617),(55,617)])
    return 'T3 — Duas verdes grandes','Duas verdes grandes (2 metades, menos de 230 mm cada), com as janelas das aletas e a ponta em V no centro, onde fica a tampa do servo. Visual mais limpo, com menos peças aparentes.'
def T4(ax):
    base(ax)
    for xc in XS:
        ab=aletas(ax,xc); fr=op(box(xc-70,566,xc+70,627),2.0); pp(ax,fr.difference(ab),'#1a1b1d','#000',0.8,6)
    pp(ax,hexa(-36,36,578,614,4.0),'#3aa857','#0b0c0d',0.8,7)
    pp(ax,box(-200,537,200,551),'#2f9449','#0b0c0d',0.6,6)
    bolts(ax,[(-34,596),(34,596)])
    return 'T4 — Preto tático com detalhes verdes','Janelas das aletas com moldura preta chanfrada, a tampa do servo com um hexágono verde pequeno e uma faixa verde fina na banda de baixo. Mais discreto, o verde só marca o centro e a linha de baixo.'
fig,axs=plt.subplots(4,1,figsize=(13,15))
for ax,fn in zip(axs,(T1,T2,T3,T4)):
    t,n=fn(ax); ax.set_xlim(-300,300); ax.set_ylim(500,640); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(t+'   (vista de trás)',fontsize=12,loc='left',fontweight='bold'); ax.text(-298,496,n,fontsize=9,va='top',wrap=True)
plt.tight_layout(h_pad=3.0); plt.savefig('tras_versoes.png',dpi=100,facecolor='#e9ebe6'); print('ok')
