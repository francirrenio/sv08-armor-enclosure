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
dob=[];gai=[];hw=[]
for yc in (150,450):
    a,b,c=[trimesh.load('../hingeW/SV-30-05%s_D%d.stl'%(k,yc)) for k in 'abc']
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
