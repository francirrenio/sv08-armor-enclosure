_src=open('frente_versoes.py').read(); exec(_src.split('VERS=[')[0]); exec(_src[_src.index('def pp'):_src.index('fig,axs')])
import pickle
from shapely import affinity as af
LG=pickle.load(open('../logo/logo_poly.pkl','rb'))
def logo(h,xc,yc):
    g=af.scale(LG,1,-1,origin=(0,0)); b=g.bounds; s=h/(b[3]-b[1])
    g=af.scale(g,s,s,origin=(0,0)); b=g.bounds
    return af.translate(g,xc-0.5*(b[0]+b[2]),yc-0.5*(b[1]+b[3]))
OPC=[('Centro de Y 4 a 72 (68 mm): logo de 58 mm e filetes de 52 x 7',4.0,72.0,58.0,7.0,52.0),
     ('Centro de Y 2 a 77 (75 mm): logo de 64 mm e filetes de 52 x 8',2.0,77.0,64.0,8.0,52.0)]
fig,axs=plt.subplots(2,1,figsize=(13,7.6))
for ax,(t,y0,y1,h,fh,fl) in zip(axs,OPC):
    c=hexa(-100.0,100.0,y0,y1); ls,il=lados(c); yc=0.5*(y0+y1)
    L=logo(h,0,yc)
    xi=L.bounds[2]+9.0                       # filete comeca 9 mm depois da logo
    fx=[hexa(xi,xi+fl,yc-fh/2,yc+fh/2,1.5)]; fx.append(M(fx[0]))
    pp(ax,box(-300,0,300,81),'#26292c','#000',0.6,0); pp(ax,box(-300,81,300,97),'#c9a6e0','#000',0.5,0)
    pp(ax,cants,'#1b1d1f','#000',0.9,3)
    for g in ls:
        for q in (g.geoms if hasattr(g,'geoms') else [g]): pp(ax,q,'#2f9449' if q.centroid.y>42 else '#45b862')
    for i_ in il: pp(ax,i_,'#1a1c1e','#000',0.6,3); pp(ax,grade(i_),'#0a0b0c','#000',0.4,4)
    pp(ax,c.difference(bf(L,0.3)).difference(uu(fx)),'#3aa857'); pp(ax,L,'#ffffff','#bba',0.4,5)
    for f in fx: pp(ax,f,'#fff4c0','#b9a35a',0.5,5)
    ax.set_xlim(-298,298); ax.set_ylim(-1,97); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(t,fontsize=12,loc='left',fontweight='bold')
    print(t,'filete X',round(xi,1),round(xi+fl,1),'borda do hexagono na altura do filete',round(c.intersection(box(0,yc-0.1,300,yc+0.1)).bounds[2],1))
plt.tight_layout(h_pad=2.5); plt.savefig('frente_logo3.png',dpi=110,facecolor='#e9ebe6')
