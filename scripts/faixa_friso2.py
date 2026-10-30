exec(open('faixa_versoes.py').read().split('# ---------------- versoes')[0])
src=open('faixa_versoes.py').read()
exec(src[src.index('def V2'):src.index('def V3')])
exec(src[src.index('# ---------------- desenho'):src.index('def painel')])
fit.__defaults__=(6.0,4.0); D=V2()
from matplotlib.gridspec import GridSpec
verdes=unary_union([p for g in D['verdes'] for p in parts(g)])
rebaixo=bf(verdes,0.5)
friso=bf(verdes,2.0)
fig=plt.figure(figsize=(13,9.6)); gs=GridSpec(2,2,height_ratios=[1.35,1],figure=fig)
ax=fig.add_subplot(gs[0,:])
pp(ax,sbox(-300,0,300,81),'#26292c','#000',0.6,0)
pp(ax,cants,'#1b1d1f','#000',0.9,3)
pp(ax,rebaixo,'#121314','#000',0.5,1)
PS=parts(verdes)
for i,p in enumerate(PS):
    ln=bf(p,1.1).exterior.difference(unary_union([bf(o,0.45) for j,o in enumerate(PS) if j!=i]))
    for l in (ln.geoms if hasattr(ln,'geoms') else [ln]):
        if l.is_empty: continue
        c=np.array(l.coords); ax.plot(c[:,0],c[:,1],color='#7a8086',lw=1.3,zorder=1.5)
for p in parts(verdes):
    e3=p.equals(v3); pp(ax,p,'#3aa857' if e3 else ('#2f9449' if p.centroid.y>40 else '#45b862'),'#0b0c0d',0.8,2)
pp(ax,oval,'#b7b2a6','#000',0.8,4)
pp(ax,D['bolF'],'#1a1c1e','#000',0.6,3); tomada(ax,1)
ax.set_xlim(55,252); ax.set_ylim(-1,70); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Vista de fora (lateral esquerda, lado da frente)',fontsize=11,loc='left',fontweight='bold')
ax.annotate('nervura preta 0,5 abaixo da face,\ncom chanfro de 0,6 nas 2 bordas',xy=(171.5,41.5),xytext=(185,60),fontsize=9,color='w',arrowprops=dict(arrowstyle='->',color='w',lw=0.8))
from shapely.ops import nearest_points
_w=[p for p in PS if p.bounds[0]>60 and p.centroid.y<40][0]; _pt=nearest_points(_w.exterior,Point(70,12))[0]
ax.annotate('folga 0,5 entre a verde\ne o encaixe na preta',xy=(_pt.x-0.25,_pt.y),xytext=(58,4),fontsize=9,color='w',arrowprops=dict(arrowstyle='->',color='w',lw=0.8))
# corte
def corte(ax):
    F=283.8; FU=280.6; T=F-0.5; C=0.6
    pl=Polygon([(-8,276.8),(13,276.8),(13,FU),(4.5,FU),(4.5,T-C),(4.5-C,T),(0.5+C,T),(0.5,T-C),(0.5,FU),(-8,FU)])
    gE=Polygon([(-8,280.8),(0,280.8),(0,F-1.0),(-1.0,F),(-8,F)]); gD=affinity.scale(gE,-1,1,origin=(2.5,0))
    pp(ax,pl,'#2a2d30','#000',0.8,1); pp(ax,gE,'#45b862','#0b0c0d',0.8,2); pp(ax,gD,'#3aa857','#0b0c0d',0.8,2)
    ax.set_xlim(-8,13); ax.set_ylim(277.8,285.6); ax.set_aspect('equal'); ax.axis('off')
    ax.plot([-8,13],[F,F],':',color='#888',lw=0.6)
    kw=dict(fontsize=8,color='#222')
    ax.annotate('',xy=(0,284.9),xytext=(5,284.9),arrowprops=dict(arrowstyle='<->',lw=0.7)); ax.text(2.5,285.1,'vão 4,0',ha='center',**kw)
    ax.annotate('',xy=(6.2,F),xytext=(6.2,T),arrowprops=dict(arrowstyle='<->',lw=0.6)); ax.text(6.5,T+0.1,'0,5 abaixo da face verde',fontsize=8,color='#222',va='bottom')
    ax.text(2.5,T-1.2,'topo reto',ha='center',fontsize=8,color='#ddd')
    ax.annotate('chanfro 0,6 x 45°',xy=(0.8,T-0.3),xytext=(-6.5,284.9),fontsize=8,color='#222',arrowprops=dict(arrowstyle='->',lw=0.6))
    ax.annotate('',xy=(4.2,T-0.3),xytext=(-1.5,285.0),arrowprops=dict(arrowstyle='->',lw=0.6))
    for z0 in (0,4.5):
        ax.annotate('',xy=(z0,280.2),xytext=(z0+0.5,280.2),arrowprops=dict(arrowstyle='<->',lw=0.6,color='#ddd')); ax.text(z0+0.25,279.5,'0,5',ha='center',fontsize=8,color='#ddd')
    ax.text(-4.5,282.2,'verde\n3 mm',ha='center',fontsize=8,color='#0b2a12'); ax.text(9.5,282.2,'verde',ha='center',fontsize=8,color='#0b2a12')
    ax.text(2.5,278.6,'placa preta',ha='center',fontsize=8,color='#ddd')
    ax.set_title('Corte A — nervura entre as verdes',fontsize=10.5,loc='left',fontweight='bold')
corte(fig.add_subplot(gs[1,:]))
fig.text(0.02,0.01,'Nervura preta de 3 mm entre as verdes, topo reto 0,5 abaixo da face verde e chanfro de 0,6 nas 2 bordas. Folga de 0,5 até a verde; o fundo do encaixe fica 0,2 atrás dela.',fontsize=9)
plt.tight_layout(rect=(0,0.03,1,1)); plt.savefig('faixa_friso2.png',dpi=120,facecolor='#e9ebe6')
