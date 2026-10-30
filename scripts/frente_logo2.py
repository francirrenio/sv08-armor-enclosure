_src=open('frente_versoes.py').read(); exec(_src.split('VERS=[')[0]); exec(_src[_src.index('def pp'):_src.index('fig,axs')])
import pickle
from shapely import affinity as af
LG=pickle.load(open('../logo/logo_poly.pkl','rb'))
def logo(h,xc,yc):
    g=af.scale(LG,1,-1,origin=(0,0)); b=g.bounds; s=h/(b[3]-b[1])
    g=af.scale(g,s,s,origin=(0,0)); b=g.bounds
    return af.translate(g,xc-0.5*(b[0]+b[2]),yc-0.5*(b[1]+b[3]))
OPC=[('Hoje: centro de Y 8 a 66 (58 mm), logo de 50 mm',8.0,66.0,50.0),
     ('Centro de Y 4 a 72 (68 mm), logo de 58 mm',4.0,72.0,58.0),
     ('Centro de Y 2 a 77 (75 mm), logo de 64 mm',2.0,77.0,64.0)]
fig,axs=plt.subplots(3,1,figsize=(13,11))
for ax,(t,y0,y1,h) in zip(axs,OPC):
    c=hexa(-100.0,100.0,y0,y1) if y0<8 else _V['hexv']
    ls,il=lados(c)
    L=logo(h,0,0.5*(y0+y1))
    pp(ax,box(-300,0,300,81),'#26292c','#000',0.6,0); pp(ax,box(-300,81,300,97),'#c9a6e0','#000',0.5,0)
    pp(ax,cants,'#1b1d1f','#000',0.9,3)
    for g in ls:
        for q in (g.geoms if hasattr(g,'geoms') else [g]): pp(ax,q,'#2f9449' if q.centroid.y>42 else '#45b862')
    for i_ in il: pp(ax,i_,'#1a1c1e','#000',0.6,3); pp(ax,grade(i_),'#0a0b0c','#000',0.4,4)
    pp(ax,c.difference(bf(L,0.3)),'#3aa857'); pp(ax,L,'#ffffff','#bba',0.4,5)
    ax.set_xlim(-298,298); ax.set_ylim(-1,97); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(t,fontsize=12,loc='left',fontweight='bold')
    print(t,[round(v,1) for v in c.bounds])
plt.tight_layout(h_pad=2.5); plt.savefig('frente_logo2.png',dpi=110,facecolor='#e9ebe6')
