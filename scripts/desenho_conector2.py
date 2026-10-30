import pickle,numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
exec(open('geo.py').read())
from shapely.geometry import Polygon, box as sbox, LineString
from shapely.ops import unary_union
CT=pickle.load(open('CT.pkl','rb')); RL=pickle.load(open('RL.pkl','rb'))
PG,PN=pickle.load(open('cv2d.pkl','rb'))
A=pickle.load(open('../as03/as03_contornos_D.pkl','rb'))
def sec(m,x=281.5):
    s=section_polys(m,'x',x); gs=s.geoms if hasattr(s,'geoms') else [s]; return max(gs,key=lambda g:g.area)
q=64
op=lambda p,r:p.buffer(-r,join_style=1,quad_segs=q).buffer(r,join_style=1,quad_segs=q)
cl=lambda p,r:p.buffer(r,join_style=1,quad_segs=q).buffer(-r,join_style=1,quad_segs=q)
v3=PN['verde_central']; fsup=PG['verde_lat_F_sup']
mold=sec(CT['E_moldura_conector'],283.0)
aro=A['aro']; fl=A['flange']
jan=aro.buffer(0.2,join_style=1)
# v3 estendida para baixo pelas diagonais (para a borda esquerda das propostas seguir a ponta da verde 3)
ZL=lambda y:72+(y-9.25)*15.28/26.5
v3x=unary_union([v3,Polygon([(0,37),(ZL(37),37),(ZL(-20),-20),(0,-20)])])
# ---- badge hexagonal (mini verde 3) em volta da tomada: mesmas diagonais da verde 3, cantos R6
K=15.28/26.5; ZC=135.5; YC=19.5; H=17.5; a=ZC-27.5; b=ZC+27.5
hexa=Polygon([(a,YC-H),(b,YC-H),(b+H*K,YC),(b,YC+H),(a,YC+H),(a-H*K,YC)])
hexa=op(hexa,6.0)
bra=PN['verde_braco_F']; inf=PG['verde_lat_F_inf']
def corta(g,f,r=3.0):
    g=op(g.difference(f.buffer(1.0,join_style=1,quad_segs=q)),r)
    return unary_union([p for p in (g.geoms if hasattr(g,'geoms') else [g]) if p.area>40])
# C: badge verde com a tomada; braco e verde de baixo voltam e encaixam nele com folga de 1
pa=hexa.difference(jan); ca=corta(bra,hexa); cb=corta(inf,hexa)
# D: mesma ideia, mas o hexagono e uma ilha preta (a placa aparece), sem verde em volta da tomada
pb=corta(bra,hexa); inf=corta(inf,hexa)
# ---- desenho
def pp(ax,g,fc,ec='#0b0c0d',lw=0.8,z=2,alpha=1):
    for p in (g.geoms if hasattr(g,'geoms') else [g]):
        if p.is_empty: continue
        verts=[];codes=[]
        for r in [p.exterior]+list(p.interiors):
            c=np.array(r.coords); verts+=c.tolist(); codes+=[Path.MOVETO]+[Path.LINETO]*(len(c)-2)+[Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts,codes),fc=fc,ec=ec,lw=lw,zorder=z,alpha=alpha))
def tomada(ax):
    pp(ax,fl,'#151617','#000',0.5,1)
    pp(ax,aro,'#1d1e20','#000',0.6,4)
    pp(ax,sbox(115.5,13,124.5,28),'#d23a2a','#5a0f08',0.6,5)       # chave
    pp(ax,sbox(129.5,10,135,31),'#2b2c2e','#000',0.5,5)             # fusivel
    pp(ax,Polygon([(139,9),(156,9),(156,27),(152,31),(143,31),(139,27)]),'#111','#000',0.5,5)   # C14
    for z,y in ((147.5,24),(143.5,15),(151.5,15)): pp(ax,Point(z,y).buffer(1.2),'#8a8f94','#000',0.3,6)
from shapely.geometry import Point
def base(ax,tit):
    pp(ax,sbox(-5,0,262,81),'#26292c','#000',0.8,0)
    pp(ax,sbox(262,0,292,81).union(sbox(250,0,262,30)),'#1c1e20','#000',0.8,0)
    pp(ax,v3,'#3aa857'); pp(ax,fsup,'#2f9449')
    ax.set_xlim(40,292); ax.set_ylim(-2,84); ax.set_aspect('equal'); ax.axis('off'); ax.set_title(tit,fontsize=12,loc='left',fontweight='bold')
fig,axs=plt.subplots(3,1,figsize=(13,11.5))
base(axs[0],'Hoje'); pp(axs[0],mold,'#3aa857'); tomada(axs[0])
axs[0].text(215,14,'vão preto vazio\n(sem braço e sem\na verde de baixo)',fontsize=9,color='#e8e8e8',ha='center',va='center')
base(axs[1],'C — mini verde 3 em volta da tomada; braço e verde de baixo voltam e encaixam nela')
pp(axs[1],ca,'#45b862'); pp(axs[1],cb,'#2f9449'); pp(axs[1],pa,'#3aa857'); tomada(axs[1])
axs[1].annotate('hexágono com as mesmas\ndiagonais da verde 3 (R6)',xy=(172,19.5),xytext=(218,8),fontsize=8.5,color='w',arrowprops=dict(arrowstyle='->',color='w',lw=0.8))
axs[1].annotate('folga de 1 mm igual\nàs outras emendas',xy=(100,22),xytext=(44,74),fontsize=8.5,color='w',arrowprops=dict(arrowstyle='->',color='w',lw=0.8))
base(axs[2],'D — mesmo desenho, mas o hexágono fica preto (só a tomada aparece na placa)')
pp(axs[2],pb,'#45b862'); pp(axs[2],inf,'#2f9449'); tomada(axs[2])
axs[2].annotate('ilha preta em hexágono',xy=(171,19.5),xytext=(218,8),fontsize=8.5,color='w',arrowprops=dict(arrowstyle='->',color='w',lw=0.8))
plt.tight_layout(); plt.savefig('desenho_conector2.png',dpi=130,facecolor='#e9ebe6')
for nm,g in (('hex',hexa),('ca',ca),('cb',cb)): print(nm,[round(b,1) for b in g.bounds],round(g.area,0))
