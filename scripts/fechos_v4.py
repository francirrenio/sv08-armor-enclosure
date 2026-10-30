# FECHOS DO PAINEL LATERAL + DOBRADICAS DA PORTA DIREITA (na pagina)
#  - fechos snap latch (SV-40-05) do painel lateral: frente Y 190 / 430 (nos encaixes ja feitos na verde/espinha) e tras Y 190 / 430 (espelho)
#  - dobradicas K1 270 graus (SV-30-05) em Y 150 e 450: folha fixa na face lateral da coluna, folha da porta na frente da moldura da porta
#  - parafusos das dobradicas com porca sextavada embutida (no lugar dos furos-piloto de autoatarraxante):
#      folha fixa: M3x20 cabeca cilindrica, porca embutida por dentro da espinha (X 273,2-275,6)
#      folha da porta: M3x18 cabeca cilindrica, porca embutida por tras da moldura da porta (Z 276,3-278,7)
#  - o fecho de cima (centro da banda) fica de fora ate decidir: ele cruza o trilho de cima da moldura e o acrilico
import numpy as np, pickle, trimesh, json
exec(open('load.py').read()); exec(open('geo.py').read())
from shapely.geometry import Polygon
CT=pickle.load(open('CT.pkl','rb')); P=pickle.load(open('P.pkl','rb'))
T='../ltop/'
YH={150:(141.0,159.0),450:(441.0,459.0)}; ZB=266.0; XA=231.0
def hexA(axis,a0,a1,c1,c2,s=5.5+0.3):
    r=s/np.sqrt(3); pts=[(c1+r*np.cos(t),c2+r*np.sin(t)) for t in np.radians([0,60,120,180,240,300])]
    m=trimesh.creation.extrude_polygon(Polygon(pts),a1-a0)
    if axis=='x': M_=np.array([[0,0,1,a0],[1,0,0,0],[0,1,0,0],[0,0,0,1]],float)   # (y,z) -> extrudado em X
    else:         M_=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,a0],[0,0,0,1]],float)   # (x,y) -> extrudado em Z
    m.apply_transform(M_)
    if m.volume<0: m.invert()
    return m
def cap(p,axis,Lg,hd=5.5,hh=3.0):   # DIN912 M3
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*Lg,3.0))
def nut(axis,a0,c1,c2):
    return D(hexA(axis,a0,a0+2.4,c1,c2,5.5),CYL(*(([a0-1,c1,c2],[a0+3.4,c1,c2]) if axis=='x' else ([c1,c2,a0-1],[c1,c2,a0+3.4])),3.0))

# 1) espinha: piloto 2,4 -> furo 3,4 + bolsa da porca por dentro
e=CT['espinha']; cuts=[]
for yy in YH.values():
    for y in yy: cuts+=[CYL([271.0,y,ZB],[284.0,y,ZB],3.4),hexA('x',272.0,275.6,y,ZB)]
CT['espinha']=max(D(e,*cuts).split(only_watertight=False),key=lambda p:p.volume)
# 2) molduras da porta direita: bolsa da porca por tras (Z 276 a 278,7)
m1=P['SV-30-01a moldura (proposta)']; m2=trimesh.load('../aud3/b0364.stl')
def bolsas(m,ys): return max(D(m,*[hexA('z',275.0,278.7,XA,y) for y in ys]).split(only_watertight=False),key=lambda p:p.volume)
CT['porta_mold1']=bolsas(m1,YH[150]); CT['porta_mold2']=bolsas(m2,YH[450])
CT['porta_pux']=trimesh.load('../aud3/b0358.stl')
# 3) dobradicas
# CHANFRO_DOBRADICA: chanfro de 45 graus em volta da face de fora das 2 folhas (em cima, embaixo e na ponta livre),
# com cantos em meia-esquadria, no padrao das cantoneiras; 2,5 mm para nao entrar nos rebaixos dos parafusos (Y +-9)
CD=2.5; _e=2.0
def _pz(poly,z0,z1): return prism_xy(poly,z0,z1)
def chanfra(m,yc):
    yt,yb=yc+13.7,yc-15.2
    cutA=[prism_zy(Polygon([(297.0+_e,yt-CD-_e),(297.0+_e,yt+_e),(297.0-CD-_e,yt+_e)]),221.0,279.0),        # folha da porta: face Z 297
          prism_zy(Polygon([(297.0+_e,yb+CD+_e),(297.0+_e,yb-_e),(297.0-CD-_e,yb-_e)]),221.0,279.0),
          prism_xz_(Polygon([(222.0+CD+_e,297.0+_e),(222.0-_e,297.0+_e),(222.0-_e,297.0-CD-_e)]),yb-1,yt+1)]
    cutB=[_pz(Polygon([(296.0+_e,yt-CD-_e),(296.0+_e,yt+_e),(296.0-CD-_e,yt+_e)]),254.0,282.2),               # folha fixa: face X 296
          _pz(Polygon([(296.0+_e,yb+CD+_e),(296.0+_e,yb-_e),(296.0-CD-_e,yb-_e)]),254.0,282.2),
          prism_xz_(Polygon([(296.0+_e,255.0+CD+_e),(296.0+_e,255.0-_e),(296.0-CD-_e,255.0-_e)]),yb-1,yt+1)]
    return cutA,cutB
def prism_xz_(poly,y0,y1):   # poligono (x,z) extrudado em Y
    m=trimesh.creation.extrude_polygon(poly,y1-y0)
    m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
def corta(m,cuts):
    out=[]
    for p in m.split(only_watertight=False):
        if p.is_volume and np.any([not (np.any(p.bounds[0]>c.bounds[1]) or np.any(p.bounds[1]<c.bounds[0])) for c in cuts]):
            p=D(p,*cuts)
        out.append(p)
    return trimesh.util.concatenate(out)
# a placa de cada folha (fora da regiao das engrenagens) e refeita limpa: contorno com as quinas da ponta livre cortadas a 45 graus
# (5 mm, como nas cantoneiras) e chanfro de 45 graus de 1,5 mm em volta da face de fora, acompanhando tambem as quinas cortadas.
# 1,5 mm: os rebaixos dos parafusos de cima ficam a 1,6 mm da borda (a folha nao e simetrica em relacao aos parafusos)
exec(open('geo_ch2.py').read())
CD=1.5; KQ=5.0
def _contorno(u0,u1,v0,v1):   # u: ponta livre em u0, lado das engrenagens em u1; v: altura (Y)
    return Polygon([(u0,v0+KQ),(u0+KQ,v0),(u1,v0),(u1,v1),(u0+KQ,v1),(u0,v1-KQ)])
def refaz(m,lado,yc,cuts=None):
    yt,yb=yc+13.7,yc-15.2
    if lado=='A':   # folha da porta: face Z 297, contorno em (x,y)
        zona=B(221.0,271.6,yb-1,yt+1,285.0,298.0)
        placa=U(prism_xy(_contorno(222.0,271.6,yb,yt),286.6,297.0),prism_xy(I_poly(_contorno(222.0,271.6,yb,yt),(221.0,233.0)),286.0,286.7))
        corte=chamfer_cutter(_contorno(222.0,279.0,yb,yt),'z',297.0,CD,skip=lambda p,q: p[0]>278.9 and q[0]>278.9)
        cl=[prism_xy(Polygon([(221.0,yb-1),(222.0+KQ,yb-1),(221.0,yb+KQ+1)]),284.0,299.0),prism_xy(Polygon([(221.0,yt+1),(222.0+KQ,yt+1),(221.0,yt-KQ-1)]),284.0,299.0)]
        furos=[CYL([231.0,yc+d,284.0],[231.0,yc+d,299.0],3.4) for d in (-9,9)]+[CYL([231.0,yc+d,293.8],[231.0,yc+d,299.0],6.2) for d in (-9,9)]
    else:           # folha fixa: face X 296, contorno em (z,y)
        zona=B(283.0,297.0,yb-1,yt+1,254.0,277.3)
        placa=prism_zy(_contorno(255.0,277.3,yb,yt),283.8,296.0)
        corte=chamfer_cutter(_contorno(255.0,282.2,yb,yt),'x',296.0,CD,skip=lambda p,q: p[0]>282.1 and q[0]>282.1)
        cl=[prism_zy(Polygon([(254.0,yb-1),(255.0+KQ,yb-1),(254.0,yb+KQ+1)]),282.0,298.0),prism_zy(Polygon([(254.0,yt+1),(255.0+KQ,yt+1),(254.0,yt-KQ-1)]),282.0,298.0)]
        furos=[CYL([282.0,yc+d,266.0],[298.0,yc+d,266.0],3.4) for d in (-9,9)]+[CYL([292.8,yc+d,266.0],[298.0,yc+d,266.0],6.2) for d in (-9,9)]
    out=[]
    for p in m.split(only_watertight=False):
        toca=not (np.any(p.bounds[0]>zona.bounds[1]) or np.any(p.bounds[1]<zona.bounds[0]))
        if p.is_volume and toca:
            p=D(U(D(p,zona),placa),*cl,*furos,corte)
            p=max(p.split(only_watertight=False),key=lambda q:q.volume)
        out.append(p)
    return trimesh.util.concatenate(out)
def I_poly(pg,xr):
    from shapely.geometry import box as _bx
    return pg.intersection(_bx(xr[0],-1e4,xr[1],1e4))
dob=[];gai=[];hw=[]
for yc in (150,450):
    a,b,c=[trimesh.load('../hingeW/SV-30-05%s_D%d.stl'%(k,yc)) for k in 'abc']
    a=refaz(a,'A',yc); b=refaz(b,'B',yc)
    dob+=[a,b]; gai.append(c)
    for y in YH[yc]:
        hw+=[cap([292.8,y,ZB],[1,0,0],20.0),nut('x',273.2,y,ZB),
             cap([XA,y,293.8],[0,0,1],18.0),nut('z',276.3,XA,y)]
CT['dobradicas']=trimesh.util.concatenate(dob); CT['dobr_gaiola']=trimesh.util.concatenate(gai); CT['dobr_hw']=trimesh.util.concatenate(hw)
# 4) fechos do painel lateral (frente do Fusion; tras = espelho em Z, como no Fusion)
def mz(m):
    q=m.copy(); q.apply_transform(np.diag([1,1,-1,1]))
    if q.volume<0: q.invert()
    return q
F190={k.split('Y190 ')[1]:M[k] for k in M if 'fecho D frente Y190' in k}
F430={n:trimesh.load(T+'%03d.stl'%i) for i,n in zip(range(11,19),['corpo','meio','alavanca','M3x16','porca','pino longo','pino curto 1','pino curto 2'])}
corpo=[];fhw=[]
for g in (F190,F430):
    for n,m in g.items():
        (fhw if n in ('M3x16','porca') else corpo).extend([m,mz(m)])
CT['fechos_lat']=trimesh.util.concatenate(corpo); CT['fechos_hw']=trimesh.util.concatenate(fhw)
# conferencias
chk={}
viz={'esp':CT['espinha'],'v72':CT['verde_72'],'vsup':CT['verde_sup'],'m1':CT['porta_mold1'],'m2':CT['porta_mold2'],'capa':pickle.load(open('CF.pkl','rb'))['capa_74']}
for i,h in enumerate(hw):
    for k,m in viz.items():
        v=I(h,m).volume
        if v>0.01: chk['hw%d_%s'%(i,k)]=v
for i,d in enumerate(dob+gai):
    for k,m in viz.items():
        dd=d if d.is_volume else d.convex_hull
        v=I(dd,m).volume if d.is_volume else -1
        if v!=0: chk['dob%d_%s'%(i,k)]=v
chk['ok']=float(all(m.is_volume for m in (CT['espinha'],CT['porta_mold1'],CT['porta_mold2'])))
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}))
pickle.dump(CT,open('CT.pkl','wb'))
