# 4 versoes do TOPO DA FRENTE (acima da porta, Y 531,5-634), vista de fora; mesmo estilo da lateral e da frente de baixo
import pickle, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from shapely.geometry import Polygon, box
from shapely.ops import unary_union as uu
from shapely import affinity
exec(open('geo.py').read())
_fv=open('frente_versoes.py').read(); exec(_fv.split('VERS=[')[0])     # hexa, op, bf, K, grade, R, GAP
CT=pickle.load(open('CT.pkl','rb'))
s=section_polys(CT['cant_top_F'],'z',290.0); cap=max((s.geoms if hasattr(s,'geoms') else [s]),key=lambda q:q.area)
caps=uu([cap,M(cap)])
mold=section_polys(CT['porta_mold2'],'z',285.5); mold=uu([mold,M(mold)])
Y0,Y1,YS=531.5,634.0,558.5          # topo da porta, topo do top hat, emenda banda/riser (mesma linha da lateral)
XI=235.5-0.5                        # encosta na cantoneira de cima
def janela(xc,w=160.0,h=66.0,yc=596.0):   # moldura verde das aletas igual a da lateral (160 x 66, abertura 138 x 44)
    fr=op(box(xc-w/2,yc-h/2,xc+w/2,yc+h/2),3.0); ab=op(box(xc-w/2+11,yc-h/2+11,xc+w/2-11,yc+h/2-11),2.0)
    al=[box(xc-w/2+11,y,xc+w/2-11,y+3.0) for y in np.arange(yc-h/2+14,yc+h/2-13,8.0)]
    pf=[(xc-w/2+5.5,yc-h/2+5.5),(xc+w/2-5.5,yc-h/2+5.5),(xc-w/2+5.5,yc+h/2-5.5),(xc+w/2-5.5,yc+h/2-5.5)]
    return fr.difference(ab),ab,uu(al),pf
def V_A():
    G=[];A=[];L=[];P=[]
    for xc in (-115.0,115.0):
        f,a,l,p=janela(xc); G.append(f);A.append(a);L.append(l);P+=p
    return dict(verdes=G,aber=A,aletas=L,paraf=P,luz=[],vinco=[0.0],nota='Igual à lateral: banda preta lisa e duas janelas de aletas com a mesma moldura verde da lateral (160 x 66). As linhas da lateral continuam na frente. Emenda do riser no centro, escondida num vinco.')
def V_B():
    c=hexa(-100,100,563,629); fil=hexa(-80,80,592.5,599.5,1.5)
    G=[Polygon(c.exterior.coords,[fil.exterior.coords])]
    return dict(verdes=G,aber=[],aletas=[],paraf=[(-72,575),(72,575),(-72,617),(72,617)],luz=[fil],vinco=[-160.0,160.0],nota='Hexágono verde no centro (200 x 66), igual ao de baixo, com um filete de luz branco (fita ARGB atrás). Lados pretos lisos com um vinco. Sem aletas na frente.')
def V_C():
    d=V_A()
    ys0,ys1=536.0,553.0; s=fit(box(-XI,ys0,XI,ys1),[caps])
    meia=[op(s.intersection(box(-400,0,-2,700)),R).intersection(box(-400,0,-2,700)),op(s.intersection(box(2,0,400,700)),R)]
    meia=[hexa(-XI+8,-2,ys0,ys1,4.0,pr=False),hexa(2,XI-8,ys0,ys1,4.0,pl=False)]
    d['verdes']+=meia; d['nota']='Como a A, mais uma faixa verde fina corrida na banda (17 mm), de canto a canto em 2 metades, com as pontas na mesma diagonal das outras verdes. Cria uma linha contínua acima da porta.'
    return d
def V_D():
    f,a,l,p=janela(0.0,w=280.0)
    G=[f]
    for s_ in (1,-1):
        g=hexa(150,XI-6,566,626,R,pr=False) if s_>0 else M(hexa(150,XI-6,566,626,R,pr=False))
        G.append(g)
    return dict(verdes=G,aber=[a],aletas=[l],paraf=p,luz=[],vinco=[],nota='Uma janela de aletas larga no centro (280 x 66) para a exaustão, com moldura verde. Dos lados, duas verdes com a ponta na diagonal, apontando para o centro.')
VERS=[('A — Igual à lateral (2 janelas de aletas)',V_A),('B — Hexágono central com filete de luz',V_B),('C — A + faixa verde corrida na banda',V_C),('D — Janela larga no centro + verdes laterais',V_D)]
def pp(ax,g,fc,ec='#0b0c0d',lw=0.8,z=2,ls='-'):
    for p in [q for q in (g.geoms if hasattr(g,'geoms') else [g]) if not q.is_empty and q.area>0.5]:
        verts=[];codes=[]
        for r in [p.exterior]+list(p.interiors):
            c=np.array(r.coords); verts+=c.tolist(); codes+=[Path.MOVETO]+[Path.LINETO]*(len(c)-2)+[Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts,codes),fc=fc,ec=ec,lw=lw,zorder=z,ls=ls))
fig,axs=plt.subplots(4,1,figsize=(13,15))
for ax,(t,fn) in zip(axs,VERS):
    D=fn()
    pp(ax,box(-XI,YS,XI,Y1),'#26292c','#000',0.6,1)            # riser preto
    pp(ax,box(-XI,Y0,XI,YS),'#1f2124','#000',0.6,1)            # banda preta
    for xv in D['vinco']: pp(ax,box(xv-1.6,Y0,xv+1.6,Y1),'#121314','#000',0.3,2)
    pp(ax,caps,'#1b1d1f','#000',0.9,3)
    pp(ax,mold.intersection(box(-400,440,400,Y0)),'#c6a3df','#000',0.6,1); pp(ax,box(-226.5,440,226.5,Y0-8).difference(mold),'#d6eef7','#7aa',0.4,0)
    for a in D['aber']: pp(ax,a,'#0d0e0f','#000',0.5,3)
    for l in D['aletas']: pp(ax,l,'#5a5e63','#000',0.4,4)
    for g in D['verdes']: pp(ax,g,'#3aa857','#0b0c0d',0.8,5)
    for l in D['luz']: pp(ax,l,'#ffffff','#0b0c0d',0.8,6)
    for x,y in D['paraf']: ax.add_patch(plt.Circle((x,y),2.6,fc='#c43b3b',ec='#000',lw=.4,zorder=7))
    ax.axhline(YS,color='#e0a020',lw=.6,ls='--',zorder=8); ax.text(298,YS+1,'linha da lateral',fontsize=7,color='#a0700a',ha='right')
    ax.set_xlim(-300,300); ax.set_ylim(452,640); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(t,fontsize=12,loc='left',fontweight='bold'); ax.text(-298,446,D['nota'],fontsize=9,va='top',wrap=True)
plt.tight_layout(h_pad=3.0); plt.savefig('topo_frente_versoes.png',dpi=105,facecolor='#e9ebe6')
print('ok')
