_src=open('frente_versoes.py').read(); exec(_src.split('VERS=[')[0]); exec(_src[_src.index('def pp'):_src.index('fig,axs')])
import pickle
from shapely import affinity as af
from matplotlib.gridspec import GridSpec
LG=pickle.load(open('../logo/logo_poly.pkl','rb'))
def logo(h,xc,yc):
    g=af.scale(LG,1,-1,origin=(0,0)); b=g.bounds; s=h/(b[3]-b[1])
    g=af.scale(g,s,s,origin=(0,0)); b=g.bounds
    return af.translate(g,xc-0.5*(b[0]+b[2]),yc-0.5*(b[1]+b[3]))
y0,y1=4.0,72.0; yc=38.0
c=hexa(-100,100,y0,y1); L=logo(58,0,yc).buffer(-0.15,join_style=2)
xi=logo(58,0,yc).bounds[2]+9.0; fx=[hexa(xi,xi+52,yc-3.5,yc+3.5,1.5)]; fx.append(M(fx[0]))
luz=uu([L]+fx)
cav=op(bf(uu([L.convex_hull]+fx),5.0),3.0)                 # interior da caixa de luz
fita=[box(-92,yc-6,92,yc+6),box(-26,yc+12,26,yc+24),box(-26,yc-24,26,yc-12)]   # fita de 12 mm: linha do meio + 2 trechos atras da logo
fig=plt.figure(figsize=(13,9.5)); gs=GridSpec(2,2,height_ratios=[1.05,1],width_ratios=[1.25,1],figure=fig)
ax=fig.add_subplot(gs[0,:])
pp(ax,c.difference(bf(luz,0.2)),'#3aa857','#0b0c0d',0.8,2); pp(ax,luz,'#ffffff','#999',0.4,3)
for f in fita: pp(ax,f,'none','#d23a2a',1.0,6)
for f in fita:
    for x in np.arange(f.bounds[0]+3.5,f.bounds[2]-2,6.94): ax.add_patch(plt.Circle((x,0.5*(f.bounds[1]+f.bounds[3])),1.6,color='#ff4fd8',zorder=7))
pp(ax,cav,'none','#1f6fd6',1.2,6)
ax.annotate('fita ARGB 12 mm (144 LED/m): linha do meio de ponta a ponta',xy=(70,yc+6),xytext=(30,84),fontsize=9,color='#a01818',arrowprops=dict(arrowstyle='->',color='#a01818'))
ax.annotate('+ 2 trechos curtos atrás da logo (em cima e embaixo)',xy=(20,yc+24),xytext=(-100,84),fontsize=9,color='#a01818',arrowprops=dict(arrowstyle='->',color='#a01818'))
ax.annotate('contorno da caixa de luz (fechada, por dentro branca)',xy=(-95,yc),xytext=(-150,-6),fontsize=9,color='#1f4f9f',arrowprops=dict(arrowstyle='->',color='#1f4f9f'))
ax.set_xlim(-150,150); ax.set_ylim(-10,90); ax.set_aspect('equal'); ax.axis('off'); ax.set_title('Vista de frente, sem a verde: onde fica a fita atrás da logo e dos filetes',fontsize=11,loc='left',fontweight='bold')
# corte
ax=fig.add_subplot(gs[1,0])
def P(pts): return Polygon(pts)
Z=lambda z:z
parts=[('base da impressora','#cfc8b8',box(258,-2,263.5,80)),
       ('estrutura escondida','#565b60',uu([box(263.8,-2,279,4),box(263.8,72,279,80)])),
       ('placa preta','#26292c',uu([box(279,-2,286,4),box(279,72,286,80)])),
       ('caixa de luz (branca por dentro)','#e8e8e8',uu([box(270.5,6,272.0,70),box(270.5,6,279,8),box(270.5,68,279,70)])),
       ('verde central','#3aa857',uu([box(283,4,286,26),box(283,50,286,72)])),
       ('placa branca da logo','#ffffff',uu([box(281.8,10,283,66),box(283,26,286,50)]))]
for nm,col,g in parts: pp(ax,g,col,'#000',0.6,2)
for y in (32,44): ax.add_patch(plt.Rectangle((272.0,y-6),1.6,12,color='#ff4fd8',zorder=5))
ax.annotate('fita na base da caixa',xy=(273,38),xytext=(258.5,86),fontsize=8.5,arrowprops=dict(arrowstyle='->'))
ax.annotate('~9 mm de distância\naté a placa branca\n(espalha a luz)',xy=(277,38),xytext=(287.5,10),fontsize=8.5,arrowprops=dict(arrowstyle='->'))
ax.annotate('placa branca 1,2 mm atrás\n+ logo em relevo até a face',xy=(283.5,38),xytext=(287.5,62),fontsize=8.5,arrowprops=dict(arrowstyle='->'))
ax.set_xlim(256,300); ax.set_ylim(-4,92); ax.set_aspect('equal'); ax.axis('off'); ax.set_title('Corte pelo centro (lado = profundidade)',fontsize=11,loc='left',fontweight='bold')
ax=fig.add_subplot(gs[1,1]); ax.axis('off')
txt=('Como fica:\n'
'• a verde central tem a logo e os 2 filetes vazados\n'
'• atrás dela entra uma peça branca (PETG/PLA branco):\n'
'  placa de 1,2 mm com a logo e os filetes em relevo,\n'
'  que preenchem os vazados até a face da verde\n'
'• atrás, uma caixa de luz fechada, impressa em branco\n'
'  por dentro (reflete), com a fita ARGB no fundo,\n'
'  a ~9 mm da placa branca para a luz espalhar\n'
'• a caixa fica no lugar do vão da barra de LED atual,\n'
'  na estrutura escondida, longe dos ressaltos da base\n'
'• o cabo da fita sai por um furo no fundo da caixa\n'
'  para dentro da base (5 V, GND e dados)\n'
'• o olho do dragão vira um furo na logo branca:\n'
'  aparece mais fundo, como detalhe')
ax.text(0,1,txt,va='top',fontsize=9.5,family='DejaVu Sans')
plt.tight_layout(); plt.savefig('caixa_luz.png',dpi=110,facecolor='#e9ebe6')
print([round(v,1) for v in cav.bounds])
