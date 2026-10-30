# Topo da frente com BAIA do modulo de display (encaixe padronizado; o modulo de 7" e feito depois)
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
Y0,Y1,YS=531.5,634.0,558.5; XI=235.0; YC=596.0
def pp(ax,g,fc,ec='#0b0c0d',lw=0.8,z=2,ls='-',a=1):
    for p in [q for q in (g.geoms if hasattr(g,'geoms') else [g]) if not q.is_empty and q.area>0.3]:
        verts=[];codes=[]
        for r in [p.exterior]+list(p.interiors):
            c=np.array(r.coords); verts+=c.tolist(); codes+=[Path.MOVETO]+[Path.LINETO]*(len(c)-2)+[Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts,codes),fc=fc,ec=ec,lw=lw,zorder=z,ls=ls,alpha=a))
# layout comum (igual ao Fusion): verde lisa a esquerda, baia do display a direita (X 46-226)
BX0,BX1=46.0,226.0; XB=0.5*(BX0+BX1)
verdeE=hexa(-224.0,36.0,563,629,R,pl=False)              # ponta na diagonal apontando para a baia
def base(ax):
    pp(ax,box(-XI,YS,XI,Y1),'#26292c','#000',0.6,1); pp(ax,box(-XI,Y0,XI,YS),'#1f2124','#000',0.6,1)
    pp(ax,box(-61.6,Y0,-58.4,Y1),'#121314','#000',0.3,2)                     # emenda do riser num vinco (X -60, como no Fusion)
    pp(ax,caps,'#1b1d1f','#000',0.9,3)
    pp(ax,mold.intersection(box(-400,470,400,Y0)),'#c6a3df','#000',0.6,1)
    pp(ax,verdeE,'#3aa857','#0b0c0d',0.8,5)
    for x,y in [(-200,575),(-200,617),(15,575),(15,617)]: ax.add_patch(plt.Circle((x,y),2.6,fc='#c43b3b',ec='#000',lw=.4,zorder=7))
    ax.axhline(YS,color='#e0a020',lw=.6,ls='--',zorder=8)
OPC=[]
# A: bolso + 2 ganchos em cima + 1 parafuso embaixo (pendura e trava)
def A(ax,sx):
    fr=op(box(BX0,563,BX1,629),R); bol=op(box(BX0+10,567,BX1-10,625),2.0)
    pp(ax,fr.difference(bol),'#3aa857','#0b0c0d',0.8,5); pp(ax,bol,'#141516','#000',0.6,5)
    pp(ax,op(box(XB-55,580,XB+55,612),2.0),'#060607','#000',0.5,6)                 # janela do cabo
    for x in (XB-55,XB+55): pp(ax,box(x-8,616,x+8,620),'#000','#000',0.4,6)        # rasgos dos ganchos
    ax.add_patch(plt.Circle((XB,571.5),2.0,fc='#888',ec='#000',lw=.4,zorder=7))   # inserto M3
    # corte
    W0,W1=278.5,286.0
    sx.add_patch(plt.Rectangle((W0,558),W1-W0,76,fc='#26292c',ec='#000')); sx.add_patch(plt.Rectangle((W1,563),0.5,66,fc='#3aa857',ec='#000'))
    sx.add_patch(plt.Rectangle((W1-3,567),3.5,58,fc='#e9ebe6',ec='none'));                                  # bolso 3 mm
    sx.add_patch(plt.Rectangle((W0-0.1,580),W1-W0-2.9,32,fc='#e9ebe6',ec='none'))                          # janela
    sx.add_patch(plt.Rectangle((W0-0.1,616),W1-W0-2.9,4,fc='#e9ebe6',ec='none'))                           # rasgo gancho
    sx.add_patch(plt.Rectangle((W1-3,560),14,72,fc='#7d8a99',ec='#000',alpha=.55))                         # modulo (fantasma)
    sx.plot([W1-3,W0+1.5,W0+1.5],[618,618,614],color='#c43b3b',lw=2.2)                                     # gancho
    sx.plot([W1+11,W1-6],[571.5,571.5],color='#c43b3b',lw=1.6)                                            # parafuso
    return 'A — Pendura e trava','Bolso de 3 mm na verde (160 x 58). O módulo entra pelos 2 ganchos de cima (rasgos 16 x 4) e trava com 1 parafuso M3 embaixo, num inserto. Janela de 110 x 32 atrás para o cabo. Fácil de tirar: solta 1 parafuso e levanta.'
# B: 4 rasgos de snap + janela (encaixa de frente, sem ferramenta)
def B(ax,sx):
    fr=op(box(BX0,563,BX1,629),R); pp(ax,fr,'#3aa857','#0b0c0d',0.8,5)
    pp(ax,op(box(XB-55,580,XB+55,612),2.0),'#060607','#000',0.5,6)
    for x in (BX0+16,BX1-16):
        for y in (568,624): pp(ax,box(x-6,y-1.75,x+6,y+1.75),'#000','#000',0.4,6)
    W0,W1=278.5,286.0
    sx.add_patch(plt.Rectangle((W0,558),W1-W0,76,fc='#26292c',ec='#000')); sx.add_patch(plt.Rectangle((W1,563),0.5,66,fc='#3aa857',ec='#000'))
    sx.add_patch(plt.Rectangle((W0-0.1,580),W1-W0+0.7,32,fc='#e9ebe6',ec='none'))
    for y in (568,624): sx.add_patch(plt.Rectangle((W0-0.1,y-1.75),W1-W0+0.7,3.5,fc='#e9ebe6',ec='none'))
    sx.add_patch(plt.Rectangle((W1+0.5,560),12,72,fc='#7d8a99',ec='#000',alpha=.55))
    for y,s_ in ((568,-1),(624,1)): sx.plot([W1+0.5,W0-1,W0-1],[y,y,y+2.2*s_],color='#c43b3b',lw=2.2)
    return 'B — Encaixe de pressão (4 ganchos)','A verde fica lisa por fora, só com 4 rasgos (12 x 3,5) e a janela do cabo. O módulo empurra de frente e 4 ganchos travam por trás da parede. Sem parafuso aparente. Para tirar, aperta os ganchos por dentro do top hat.'
# C: trilho rabo de andorinha horizontal (desliza do centro para a direita)
def C(ax,sx):
    fr=op(box(BX0,563,BX1,629),R); pp(ax,fr,'#3aa857','#0b0c0d',0.8,5)
    tr=box(BX0+8,571,BX1-4,621); pp(ax,tr,'#141516','#000',0.6,5)
    for y in (573,619): pp(ax,box(BX0+8,y-1.2,BX1-4,y+1.2),'#000','#000',0.3,6)
    pp(ax,op(box(XB-55,582,XB+55,610),2.0),'#060607','#000',0.5,6)
    ax.annotate('',xy=(BX1-8,596),xytext=(BX0+14,596),arrowprops=dict(arrowstyle='->',color='#e0a020',lw=1.5),zorder=9)
    ax.add_patch(plt.Circle((BX0+4,596),2.0,fc='#888',ec='#000',lw=.4,zorder=7))
    W0,W1=278.5,286.0
    sx.add_patch(plt.Rectangle((W0,558),W1-W0,76,fc='#26292c',ec='#000')); sx.add_patch(plt.Rectangle((W1,563),0.5,66,fc='#3aa857',ec='#000'))
    sx.add_patch(PathPatch(Path([(W1+0.6,571),(W1-3.5,569),(W1-3.5,623),(W1+0.6,621),(W1+0.6,571)]),fc='#e9ebe6',ec='none',zorder=3))
    sx.add_patch(PathPatch(Path([(W1+0.6,571),(W1-3.5,569),(W1-3.5,623),(W1+0.6,621),(W1+14,621),(W1+14,571),(W1+0.6,571)]),fc='#7d8a99',ec='#000',alpha=.55,zorder=4))
    sx.add_patch(plt.Rectangle((W0-0.1,582),W1-W0-3.4,28,fc='#e9ebe6',ec='none',zorder=3))
    return 'C — Trilho rabo de andorinha','Bolso em rabo de andorinha (trilho em cima e embaixo, 3,5 mm). O módulo entra pelo lado do centro e desliza até o fim; 1 parafuso na ponta esquerda impede que volte. Muito firme, sem folga, e o módulo pode ter qualquer largura até 172 mm.'
fig=plt.figure(figsize=(14,15)); gs=fig.add_gridspec(3,2,width_ratios=[5.2,1],hspace=.55,wspace=.05)
for i,fn in enumerate((A,B,C)):
    ax=fig.add_subplot(gs[i,0]); sx=fig.add_subplot(gs[i,1]); base(ax); t,n=fn(ax,sx)
    ax.set_xlim(-300,300); ax.set_ylim(470,640); ax.set_aspect('equal'); ax.axis('off'); ax.set_title(t,fontsize=12,loc='left',fontweight='bold')
    ax.text(-298,462,n,fontsize=9,va='top',wrap=True)
    sx.set_xlim(272,302); sx.set_ylim(552,640); sx.set_aspect('equal'); sx.set_xticks([]); sx.set_yticks([]); sx.set_title('corte (de lado)',fontsize=8)
    sx.text(273,554,'dentro',fontsize=7); sx.text(301,554,'fora',fontsize=7,ha='right')
plt.savefig('topo_display_encaixe.png',dpi=100,facecolor='#e9ebe6',bbox_inches='tight')
print('ok')
