import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP
from shapely.geometry import Polygon, box
from shapely import affinity
BLK='#1d2022'; GRN='#33a250'; LED='#f2b13c'; BG='#d9dcd6'; CTX='#b9bdb6'
C0=258.0; CW=36.0
def lat(z): return C0+CW+(273.4-z)      # u da lateral
def L(poly_zy): return Polygon([(lat(z),y) for z,y in poly_zy])
def draw(ax,g,col,ch=1.2,reveal=0.5,z=3):
    for p in (g.geoms if hasattr(g,'geoms') else [g]):
        q=p.buffer(-reveal/2,join_style=2)
        if q.is_empty: continue
        for qq in (q.geoms if hasattr(q,'geoms') else [q]):
            ax.add_patch(MP(np.array(qq.exterior.coords),closed=True,fc=col,ec='none',zorder=z))
            inn=qq.buffer(-ch,join_style=2)
            if not inn.is_empty:
                for ii in (inn.geoms if hasattr(inn,'geoms') else [inn]):
                    xy=np.array(ii.exterior.coords); ax.plot(xy[:,0],xy[:,1],color='white',lw=0.5,alpha=0.35,zorder=z+0.1)
def screw(ax,x,y):
    ax.add_patch(plt.Circle((x,y),2.85,fc='#3a3f42',ec='#8a9095',lw=0.6,zorder=6)); ax.plot([x-1.2,x+1.2],[y,y],color='#111',lw=0.8,zorder=7)
def base_ctx(ax):
    ax.add_patch(MP([(-20,82),(C0-23.5,82),(C0-23.5,110),(-20,110)],fc='#c9b9d6',ec='none',zorder=1)); ax.text(60,95,'porta (fundo em Y 82)',fontsize=7,color='#555')
    ax.add_patch(MP([(C0-22.6,81),(lat(220),81),(lat(220),110),(C0-22.6,110)],fc='#7c8da8',ec='none',zorder=1)); ax.text(C0+2,100,'coluna (espinha + verde)',fontsize=7,color='#223')
    ax.add_patch(MP([(lat(219.2),93),(lat(-12),93),(lat(-12),110),(lat(219.2),110)],fc='#a9b6cf',ec='none',zorder=1)); ax.text(lat(120),100,'painel lateral',fontsize=7,color='#223')
    ax.add_patch(MP([(-20,19.5),(C0,19.5),(C0,40.5),(-20,40.5)],fc=LED,ec='none',zorder=0.5))
    ax.axvline(C0,color='#666',lw=0.5,ls=':'); ax.axvline(C0+CW,color='#666',lw=0.5,ls=':')
    ax.text(C0+CW/2,-6,'canto',ha='center',fontsize=7,color='#444'); ax.text(120,-6,'frente (X)',ha='center',fontsize=7,color='#444'); ax.text(lat(130),-6,'lateral (Z)',ha='center',fontsize=7,color='#444')
# lateral existente (verdes do dono) + preta com janelas
faixa=L([(65.1,79.0),(239.6,79.0),(246.7,70.0),(239.6,62.0),(65.1,62.0)])
placa=L([(90.1,58.6),(90.1,7.0),(146,7),(154,3),(246.7,3.0),(246.7,58.0),(90.1,58.6)])
latB=box(lat(273.4),2,lat(-12),93).difference(faixa.buffer(0.5,join_style=2)).difference(placa.buffer(0.5,join_style=2))
def lateral(ax):
    draw(ax,latB,BLK); draw(ax,faixa,GRN); draw(ax,placa,GRN)
    for y,z in ((86,20),(86,255),(30,20),(30,255)): screw(ax,lat(z),y)
    for y,z in ((72,129.9),(72,181.9),(20,224),(47,224),(20,116),(47,116)): screw(ax,lat(z),y)
fig,axs=plt.subplots(3,1,figsize=(17,15))
# ---------- A: Lamina verde que continua a faixa da lateral ----------
ax=axs[0]; base_ctx(ax); lateral(ax)
canto=Polygon([(C0-0.5,2),(C0+CW,2),(C0+CW,93),(C0-0.5,81)])       # peca de canto preta (cobre o P01)
gA=Polygon([(C0+CW,79),(C0+6,79),(C0-6,70.5),(150,70.5),(150,62),(C0+6,62),(C0+CW,62)])
gA=Polygon([(C0+10,79),(150,79),(132,62),(C0+10,62),(C0+18,70.5)])        # cauda em V recebendo a seta da lateral
bA_top=Polygon([(-20,81),(C0-0.5,81),(C0-0.5,79.5),(150.2,79.5),(132.2,61.5),(60,61.5),(60,41),( -20,41)])
bA_top2=Polygon([(60,61.5),(132.2,61.5),(133,62.3),(C0-0.5,62.3),(C0-0.5,41),(60,41)])
bA_bot=Polygon([(-20,2),(95,2),(95,19.0),(-20,19.0)]); bA_bot2=Polygon([(95,2),(C0-0.5,2),(C0-0.5,19),(95,19)])
gA2=Polygon([(196.6,19),(C0-0.5,13.6),(C0-0.5,19)])
for g in (bA_top,bA_top2,bA_bot,bA_bot2): draw(ax,g,BLK)
draw(ax,canto,BLK); draw(ax,gA,GRN)
for x,y in ((26,51),(110,51),(205,51),(37,10.5),(150,10.5),(230,7.5)): screw(ax,x,y)
for x,y in ((172,70.5),(232,70.5)): screw(ax,x,y)
ax.set_title('A · Lâmina: a faixa verde da lateral passa pelo canto e corre pela frente, terminando numa diagonal; as pretas contornam o verde; emendas em X 60 (cima), X 95 (baixo) e no fim da lâmina',fontsize=10,loc='left')
# ---------- B: Painel rebaixado (linguagem da roxa) ----------
ax=axs[1]; base_ctx(ax); lateral(ax)
frame=box(-20,2,C0-0.5,81)
win=Polygon([(125.5,42.8),(131.4,42.8),(151.9,56.5),(238.3,56.5),(238.3,4.2),(140.1,4.2),(140.1,19.0),(125.5,19.0)])
win2=Polygon([(-20,42.8),(110,42.8),(110,56.5),(-20,56.5)])
fr=frame.difference(win.buffer(0.5,join_style=2)).difference(box(-20,19.5,C0,40.5))
draw(ax,fr.intersection(box(-20,0,70,90)),BLK); draw(ax,fr.intersection(box(70,0,C0,90)),BLK)
draw(ax,win.difference(box(-20,19.5,C0,40.5)),GRN)
draw(ax,canto,BLK)
for x,y in ((40,70),(160,70),(245,70),(40,10.5),(105,10.5),(248,10.5)): screw(ax,x,y)
ax.set_title('B · Painel rebaixado: moldura preta com a janela no desenho da sua roxa (diagonal no canto de cima); o verde fica 2 mm mais fundo, atrás da moldura; emenda da moldura em X 70',fontsize=10,loc='left')
# ---------- C: Escamas sobrepostas ----------
ax=axs[2]; base_ctx(ax); lateral(ax)
gC=box(-20,41,C0-0.5,81)
draw(ax,gC,GRN,z=2)
s1=Polygon([(-20,81),(40,81),(62,59),(-20,59)]); s2=Polygon([(48,81),(150,81),(172,59),(70,59)]); s3=Polygon([(158,81),(C0-0.5,81),(C0-0.5,59),(180,59)])
s4=Polygon([(-20,41),(85,41),(63,56.5),(-20,56.5)]); s5=Polygon([(93,41),(200,41),(178,56.5),(71,56.5)]); s6=Polygon([(208,41),(C0-0.5,41),(C0-0.5,56.5),(186,56.5)])
for s in (s1,s2,s3,s4,s5,s6): draw(ax,s,BLK,z=4)
bC=[Polygon([(-20,2),(110,2),(125,19),(-20,19)]),Polygon([(118,2),(C0-0.5,2),(C0-0.5,19),(133,19)])]
for b in bC: draw(ax,b,BLK)
draw(ax,canto,BLK)
for x,y in ((15,70),(110,70),(215,70),(20,48.5),(130,48.5),(230,48.5),(50,10.5),(190,10.5)): screw(ax,x,y)
ax.set_title('C · Escamas: placa verde de fundo e pretas por cima com pontas em diagonal, sobrepostas; o verde aparece em "V" entre elas; emendas inclinadas e desencontradas',fontsize=10,loc='left')
for ax in axs:
    ax.set_xlim(-22,lat(-14)); ax.set_ylim(-10,112); ax.set_aspect('equal'); ax.set_facecolor(BG); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
fig.suptitle('Base FD vista "desdobrada": frente + canto + lateral numa linha só (mm reais). Verde = acabamento; preto = placas; amarelo = faixa de LED',fontsize=12)
plt.tight_layout(rect=[0,0,1,0.97]); plt.savefig('conceitos.png',dpi=105,facecolor='white')
