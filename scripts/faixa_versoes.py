# 4 versoes da faixa de baixo das laterais (vista de fora): esquerda com a tomada AS03, direita espelhada
import pickle,numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
exec(open('geo.py').read())
from shapely.geometry import Polygon, Point, box as sbox, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity
PG,PN=pickle.load(open('cv2d.pkl','rb')); A=pickle.load(open('../as03/as03_contornos_D.pkl','rb'))
RL=pickle.load(open('RL.pkl','rb'))
q=64; K=15.28/26.5; G=1.0
op=lambda p,r:p.buffer(-r,join_style=1,quad_segs=q).buffer(r,join_style=1,quad_segs=q)
cl=lambda p,r:p.buffer(r,join_style=1,quad_segs=q).buffer(-r,join_style=1,quad_segs=q)
bf=lambda p,r:p.buffer(r,join_style=1,quad_segs=q)
def parts(g): return [p for p in (g.geoms if hasattr(g,'geoms') else [g]) if not p.is_empty and p.area>20]
mz=lambda g:affinity.scale(g,-1,1,origin=(0,0))
# referencias fixas
v3=PN['verde_central']
s=section_polys(RL['verde_central'],'x',282.0); oval=[Polygon(r) for g in parts(s) for r in g.interiors if Polygon(r).area>100][0]
cT=Polygon([(-238.0,34.2),(-243.3,36.7),(-245.7,39.3),(-247.2,42.5),(-247.7,88.5),(-253.2,94.0),(-287.1,94.0),(-294.8,88.5),(-294.8,7.5),(-287.1,2.0),(-196.3,2.0),(-196.6,3.9),(-214.0,33.5),(-238.0,34.2)])
cF=mz(cT); cants=unary_union([cT,cF])
aro=A['aro']; fl=A['flange']; jan=bf(aro,0.2)
TZ0,TZ1=111.1,159.9
def hexa(z0,z1,y0,y1,pl=True,pr=True,r=6.0):   # barra com pontas de seta (120 graus, inclinacao da verde 3)
    ym=(y0+y1)/2; d=(y1-y0)/2*K
    pts=[(z0+(d if pl else 0),y0),(z1-(d if pr else 0),y0)]+([(z1,ym)] if pr else [])+[(z1-(d if pr else 0),y1),(z0+(d if pl else 0),y1)]+([(z0,ym)] if pl else [])
    return op(Polygon(pts),r)
def fit(g,viz,r=6.0,gap=G):  # tira os vizinhos com folga e arredonda (R6 por fora, entalhes acompanham)
    g=g.difference(unary_union([bf(v,gap) for v in viz])) if viz else g
    g=op(g,r)
    return unary_union(parts(g))
zona_cant=bf(cants,3.0)
def slots(z0,z1,y0,y1,n=6,w=2.6):   # grade de ventilacao (rasgos inclinados na mesma diagonal)
    out=[]; step=(z1-z0)/n
    for i in range(n):
        zc=z0+step*(i+0.5); d=(y1-y0)/2*K
        out.append(op(Polygon([(zc-w/2-d,y0),(zc+w/2-d,y0),(zc+w/2+d,y1),(zc-w/2+d,y1)]).buffer(0),0.0))
    return unary_union(out)
def screws(p,n=2):
    i=p.buffer(-4.5)
    if i.is_empty: return []
    z0,y0,z1,y1=i.bounds; out=[]
    for f in ([0.5] if n==1 else np.linspace(0.18,0.82,n)):
        pt=Point(z0+(z1-z0)*f,(y0+y1)/2)
        from shapely.ops import nearest_points
        pt=pt if i.contains(pt) else nearest_points(i,pt)[0]
        out.append(pt)
    return out
# ---------------- versoes (lado esquerdo, Z+ = frente; a direita e o espelho com a tomada trocada por tampa)
def V1():   # modulos hexagonais nas pontas, iguais na frente e atras
    sup=[fit(sbox(0,43,250,66),[v3,cF],3.0),fit(sbox(-250,43,0,66),[v3,cT],3.0)]
    mF=hexa(99,172,2,37); mT=mz(mF)
    lig=[fit(sbox(70,8,110,37),[v3,mF]+sup,3.0),fit(sbox(-110,8,-70,37),[v3,mT]+sup,3.0)]
    pon=[fit(sbox(160,8,240,37),[mF,cF]+sup,3.0),fit(sbox(-240,8,-160,37),[mT,cT]+sup,3.0)]
    return dict(verdes=[v3]+sup+lig+pon, modF=mF, modT=mT, nota='Módulos hexagonais nas duas pontas de cada lateral. Na esquerda, o da frente leva a tomada. Os outros 3 levam grade de ventilação.')
def V2():   # asas: uma peca grande de cada lado da verde 3, com um bolsao hexagonal preto
    sup=[fit(sbox(0,43,250,66),[v3,cF],3.0),fit(sbox(-250,43,0,66),[v3,cT],3.0)]
    wF=fit(sbox(70,2,250,40),[v3,cF]+sup,6.0); wT=mz(wF)
    bol=bf(hexa(103,168,5,35,r=5.0),0)
    return dict(verdes=[v3]+sup+[wF.difference(bol),wT.difference(mz(bol))], bolF=bol, bolT=mz(bol), nota='Uma asa verde grande de cada lado da verde 3, com um bolsão hexagonal preto. Na esquerda, o bolsão da frente leva a tomada. Os outros têm grade.')
def V3():   # setas grandes: verde 3 vira o centro de uma seta dupla; faixas sobem em diagonal
    sup=[fit(Polygon([(60,66),(250,66),(250,50),(150,50),(140,43),(60,43)]),[v3,cF],3.0),
         fit(Polygon([(-60,66),(-250,66),(-250,50),(-150,50),(-140,43),(-60,43)]),[v3,cT],3.0)]
    mF=hexa(99,172,2,37); mT=mz(mF)
    bF=fit(Polygon([(70,8),(110,8),(110,47),(70,47)]),[v3,mF]+sup,3.0)
    tipF=fit(Polygon([(172,2),(250,2),(250,47),(172,47)]),[mF,cF]+sup,6.0)
    return dict(verdes=[v3]+sup+[bF,mz(bF),tipF,mz(tipF)], modF=mF, modT=mT, nota='Faixa de cima com degrau, módulo hexagonal colado na verde 3 por um elo curto, e uma ponta grande até a cantoneira.')
def V4():   # protetor (skid): faixa de baixo preta exposta com a tomada, verdes so em cima
    up=[fit(hexa(72,236,40,66,pl=True,pr=True),[v3,cF],6.0),fit(hexa(-236,-72,40,66),[v3,cT],6.0)]
    trilhoF=[fit(hexa(90,106,8,32,r=3.0),[v3],3.0),fit(hexa(165,181,8,32,r=3.0),[cF],3.0)]
    return dict(verdes=[v3]+up+trilhoF+[mz(t) for t in trilhoF], skid=True, nota='Faixa de baixo preta exposta, como um protetor de carro off-road. As verdes ficam só em cima. A tomada fica no preto, entre 2 trilhos verdes curtos.')
VERS=[('1 — Módulos nas pontas',V1),('2 — Asas com bolsão',V2),('3 — Degrau e pontas grandes',V3),('4 — Protetor preto embaixo',V4)]
# ---------------- desenho
def pp(ax,g,fc,ec='#0b0c0d',lw=0.8,z=2):
    for p in parts(g) if not isinstance(g,Polygon) else [g]:
        if p.is_empty: continue
        verts=[];codes=[]
        for r in [p.exterior]+list(p.interiors):
            c=np.array(r.coords); verts+=c.tolist(); codes+=[Path.MOVETO]+[Path.LINETO]*(len(c)-2)+[Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts,codes),fc=fc,ec=ec,lw=lw,zorder=z))
def tomada(ax,sg):
    T=(lambda g:g) if sg>0 else mz
    pp(ax,T(aro),'#1d1e20','#000',0.6,6)
    pp(ax,T(sbox(115.5,13,124.5,28)),'#d23a2a','#5a0f08',0.6,7)
    pp(ax,T(sbox(129.5,10,135,31)),'#2b2c2e','#000',0.5,7)
    pp(ax,T(Polygon([(139,9),(156,9),(156,27),(152,31),(143,31),(139,27)])),'#111','#000',0.5,7)
    for z,y in ((147.5,24),(143.5,15),(151.5,15)): pp(ax,T(Point(z,y).buffer(1.2)),'#8a8f94','#000',0.3,8)
def painel(ax,D,lado):
    # lado 'E': Z+ para a direita, tomada na frente; lado 'D': espelho (Z+ para a esquerda), sem tomada
    T=(lambda g:g) if lado=='E' else mz
    pp(ax,sbox(-300,0,300,81),'#26292c','#000',0.8,0)
    pp(ax,sbox(-300,81,300,96),'#5b7fa6','#000',0.5,0)
    pp(ax,T(cants),'#1b1d1f','#000',0.9,3)
    cores=['#3aa857','#2f9449','#45b862']
    for i,g in enumerate(D['verdes']):
        g=T(g)
        if lado=='E' and ('modF' in D or 'bolF' in D): pass
        for p in parts(g):
            e3=p.equals(T(v3)); c='#3aa857' if e3 else ('#2f9449' if p.centroid.y>40 else '#45b862')
            pp(ax,p,c)
            pts=[Point(z,y) for z in (-72,72) for y in (22,52)] if e3 else screws(p,1 if p.area<900 else 2)
            for s_ in pts: pp(ax,s_.buffer(1.6),'#c0392b','#5a0f08',0.4,9)
    pp(ax,T(oval),'#b7b2a6','#000',0.8,4)
    for key in ('modF','modT'):
        if key in D:
            m=T(D[key]); tem_tom=(lado=='E' and key=='modF')
            sl=slots(108,163,9,30); sl=sl if key=='modF' else mz(sl)
            pp(ax,m.difference(T(jan)) if tem_tom else m.difference(T(sl)),'#3aa857')
            for s_ in [Point(m.bounds[0]+7,m.centroid.y),Point(m.bounds[2]-7,m.centroid.y)]: pp(ax,s_.buffer(1.6),'#c0392b','#5a0f08',0.4,9)
            if tem_tom: tomada(ax,1 if lado=='E' else -1)
    for key in ('bolF','bolT'):
        if key in D:
            b=T(D[key]); tem_tom=(lado=='E' and key=='bolF')
            pp(ax,b,'#1a1c1e','#000',0.6,3)
            if tem_tom: tomada(ax,1)
            else: pp(ax,T((slots(110,161,10,30) if key=='bolF' else mz(slots(110,161,10,30)))).intersection(b.buffer(-2.5)),'#0a0b0c','#000',0.4,4)
    if D.get('skid'):
        base=sbox(-247,2,247,37).difference(bf(cants,0))
        for zc in (-135.5,135.5):
            if lado=='E' and zc>0: tomada(ax,1)
            else:
                g=T(slots(110,161,10,30)) if zc>0 else T(mz(slots(110,161,10,30)))
                pp(ax,g,'#0a0b0c','#000',0.4,4)
    ax.set_xlim(-298,298); ax.set_ylim(-1,97); ax.set_aspect('equal'); ax.axis('off')
    ax.text(-296,-0.5,('Esquerda (tomada)' if lado=='E' else 'Direita (espelho)'),fontsize=8,color='#d8d8d8',va='bottom')
    ax.text(296 if lado=='E' else -296,90,'frente',fontsize=8,color='#e8e8e8',ha='right' if lado=='E' else 'left')
for i,(tit,fn) in enumerate(VERS):
    D=fn()
    fig,axs=plt.subplots(2,1,figsize=(13,5.6))
    painel(axs[0],D,'E'); painel(axs[1],D,'D')
    fig.suptitle('Versão '+tit,fontsize=13,fontweight='bold',x=0.02,ha='left')
    fig.text(0.02,0.005,D['nota'],fontsize=9.5,ha='left',va='bottom',wrap=True)
    plt.tight_layout(rect=(0,0.04,1,0.96)); plt.savefig('faixa_v%d.png'%(i+1),dpi=120,facecolor='#e9ebe6'); plt.close(fig)
    n=sum(len(parts(g)) for g in D['verdes'])+sum(1 for k in ('modF','modT') if k in D)
    big=max(max(p.bounds[2]-p.bounds[0],p.bounds[3]-p.bounds[1]) for g in D['verdes'] for p in parts(g))
    print(tit,'pecas verdes por lado',n,'maior',round(big,1))
