_src=open('frente_versoes.py').read(); exec(_src.split('VERS=[')[0]); exec(_src[_src.index('def pp'):_src.index('fig,axs')])
import pickle
from shapely import affinity as af
LG=pickle.load(open('../logo/logo_poly.pkl','rb'))
def logo(h,xc,yc):
    g=af.scale(LG,1,-1,origin=(0,0)); b=g.bounds; s=h/(b[3]-b[1])
    g=af.scale(g,s,s,origin=(0,0)); b=g.bounds
    return af.translate(g,xc-0.5*(b[0]+b[2]),yc-0.5*(b[1]+b[3])),s
c=_V['hexv']; ls,il=lados(c)
L1,s1=logo(50,0,37.5)
gap_mm=30*s1
fig,axs=plt.subplots(2,1,figsize=(13,7.4))
def base(ax):
    pp(ax,box(-300,0,300,81),'#26292c','#000',0.6,0); pp(ax,box(-300,81,300,97),'#c9a6e0','#000',0.5,0)
    pp(ax,cants,'#1b1d1f','#000',0.9,3)
    for g in ls:
        for q in (g.geoms if hasattr(g,'geoms') else [g]): pp(ax,q,'#2f9449' if q.centroid.y>42 else '#45b862')
    for i_ in il: pp(ax,i_,'#1a1c1e','#000',0.6,3); pp(ax,grade(i_),'#0a0b0c','#000',0.4,4)
    ax.set_xlim(-298,298); ax.set_ylim(-1,97); ax.set_aspect('equal'); ax.axis('off')
# 1: so a logo
base(axs[0]); pp(axs[0],c.difference(bf(L1,0.3)),'#3aa857'); pp(axs[0],bf(L1,0.6),'#fff8d8','#c9b98a',0.5,1); pp(axs[0],L1,'#ffffff','#bba',0.4,5)
axs[0].set_title('A + logo: a logo no centro, iluminada por trás (sem barra de LED aparente)',fontsize=12,loc='left',fontweight='bold')
# 2: logo + 2 frisos de luz
base(axs[1]); L2,_=logo(46,0,37.5)
luz=[af.rotate(box(-6,-1.6,6,1.6),0).buffer(0)]
fx=[hexa(x0,x1,35.0,40.0,1.5) for x0,x1 in ((-72,-32),(32,72))]
pp(axs[1],c.difference(bf(L2,0.3)).difference(uu(fx)),'#3aa857'); pp(axs[1],L2,'#ffffff','#bba',0.4,5)
for f in fx: pp(axs[1],f,'#fff4c0','#b9a35a',0.5,5)
axs[1].set_title('A + logo + 2 filetes de luz dos lados (a mesma luz de trás)',fontsize=12,loc='left',fontweight='bold')
plt.tight_layout(h_pad=2.5); plt.savefig('frente_logo.png',dpi=110,facecolor='#e9ebe6')
print('logo 50 mm de altura: largura',round(L1.bounds[2]-L1.bounds[0],1),'vao entre segmentos ~',round(gap_mm,2),'mm')
