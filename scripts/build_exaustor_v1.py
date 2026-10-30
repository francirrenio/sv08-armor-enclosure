# EXAUSTOR_LATERAL (modelo 1): em cada janela de aletas do riser lateral (2 por lado), 2 sopradores 4020 deitados
# (entrada para baixo, puxando da camara), duto coletor que passa pela janela do suporte do trilho e despeja nas aletas,
# aletas moveis (pino nas pontas, bracinho na ponta de dentro), barra de ligacao e servo SG90 no vao entre suporte e riser.
# Construido na janela da frente do lado direito (Z 58-196) e espelhado em Z para a janela de tras.
import numpy as np, trimesh, json, pickle
exec(open('geo.py').read())
CT=pickle.load(open('CT.pkl','rb')); S3=pickle.load(open('SUP3.pkl','rb'))
Mz=np.diag([1,1,-1,1])
def mz(m):
    q=m.copy(); q.apply_transform(Mz)
    if q.volume<0: q.invert()
    return q
def big(m): return max(m.split(only_watertight=False),key=lambda q:q.volume)
CZ=lambda x,y,z0,z1,d: CYL([x,y,z0],[x,y,z1],d)
CY=lambda x,z,y0,y1,d: CYL([x,y0,z],[x,y1,z],d)
XP=281.1; YC=[582.0,596.0,610.0]                 # eixo das aletas
ZW0,ZW1=58.0,196.0; YW0,YW1=574.0,618.0          # janela do riser
R={}
# ---------- riser: janela atravessa (tirava a pelicula de 0,2 de tras) + rasgos em U dos pinos (abertos para dentro) ----------
rs=D(CT['riser47'],B(276.5,278.3,YW0,YW1,ZW0,ZW1),B(276.5,282.5,YW0-3.0,YW1+3.0,ZW0,ZW1))
for y in YC:
    for z0,z1 in ((56.0,58.1),(195.9,198.0)):
        rs=D(rs,CZ(XP,y,z0,z1,3.3),B(276.0,XP,y-1.65,y+1.65,z0,z1))
R['riser']=rs
# ---------- aletas moveis ----------
AL=[]
for c in CT['riser47_aletas'].split(only_watertight=False):
    y=min(YC,key=lambda v:abs(v-0.5*(c.bounds[0][1]+c.bounds[1][1])))
    a=U(c,CZ(XP,y,56.4,59.05,3.0),CZ(XP,y,193.95,197.6,3.0))                       # pinos das pontas
    arm=B(273.6,279.7,y-2.4,y+2.4,58.2,61.0)                                       # bracinho (dentro da janela, atras da aleta)
    arm=U(arm,CZ(275.1,y,58.2,61.0,4.8))
    a=D(U(a,arm),CZ(275.1,y,57.5,61.5,2.1))
    AL.append(a)
R['aletas']=U(*AL)
# ---------- barra de ligacao (Z 55,2-58,0) com extensao e rasgo para o pino do servo ----------
SX,SY=270.7,569.5; HR=5.0                            # eixo do servo e raio do braco
bar=U(B(273.6,276.6,577.0,614.0,55.2,58.0),B(263.4,276.6,564.6,577.0,55.2,58.0))
for y in YC: bar=U(bar,CZ(275.1,y,55.2,58.0,4.8))
for y in YC: bar=D(bar,CZ(275.1,y,54.6,58.6,2.1))
bar=D(bar,B(SX-HR-0.6,SX-HR+3.2,SY-1.15,SY+1.15,54.6,58.6))
R['barra']=bar
R['pinos']=U(*[CZ(275.1,y,55.4,60.9,2.0) for y in YC],CZ(SX-HR,SY,51.9,57.9,2.0))
# ---------- servo SG90 (eixo em +Z) ----------
sb=U(B(SX-6.1,SX+6.1,SY-5.9,SY+16.9,27.9,50.6),B(SX-6.1,SX+6.1,SY-10.65,SY+21.65,43.8,46.3),CZ(SX,SY,50.6,51.8,11.8),CZ(SX,SY,51.8,53.6,4.6))
horn=U(CZ(SX,SY,51.9,53.6,7.0),B(SX-HR,SX,SY-2.0,SY+2.0,51.9,53.6),CZ(SX-HR,SY,51.9,53.6,4.0))
R['servo']=U(sb,horn)
# ---------- sopradores 4020 (deitados, entrada para baixo) ----------
BXS=(199.0,239.0); BY=(563.3,583.3); BZ=[(84.0,124.0),(134.0,174.0)]
bl=[]
for z0,z1 in BZ:
    h=B(BXS[0],BXS[1],BY[0],BY[1],z0,z1)
    h=D(h,CY(219.0,0.5*(z0+z1),BY[0]-1,BY[0]+0.6,27.0))                  # boca de entrada
    h=U(h,B(BXS[1],241.9,564.8,579.8,z0+0.5,z0+18.5))                     # bocal de saida (entra no duto)
    for x,z in ((BXS[0]+3.0,z0+3.0),(BXS[1]-3.0,z1-3.0)): h=D(h,CY(x,z,BY[0]-1,BY[1]+1,3.4))
    bl.append(h)
R['sopradores']=U(*bl)
# ---------- duto coletor ----------
ZA0,ZA1=74.2,174.6                                    # passa entre os montantes do suporte (73,5) e o montante da ponta (174,8)
outA=B(241.0,261.2,563.3,611.2,ZA0,ZA1)
outB=U(B(261.2,276.8,563.3,620.5,58.6,197.6),B(276.8,277.8,568.2,620.5,58.6,197.6))
inA=B(242.6,262.0,564.9,609.6,ZA0+1.6,ZA1-1.6)
inB=U(B(261.0,279.0,564.9,618.9,60.2,194.4),B(272.2,279.0,564.9,618.9,50.0,194.4))   # ponta de dentro aberta na faixa do bracinho
duto=D(U(outA,outB),inA,inB)
duto=D(duto,B(272.2,279.0,560.0,625.0,50.0,61.3))                    # faixa livre para bracinhos e barra
for z0,z1 in BZ: duto=D(duto,B(240.0,243.5,564.5,580.1,z0+0.2,z0+18.8))   # bocas dos sopradores
# berco dos sopradores (furos de entrada) + nervuras para cima
cr=B(197.0,241.2,561.6,563.3,82.0,176.0)
for z0,z1 in BZ:
    cr=D(cr,CY(219.0,0.5*(z0+z1),560,564,30.0))
    for x,z in ((BXS[0]+3.0,z0+3.0),(BXS[1]-3.0,z1-3.0)): cr=D(cr,CY(x,z,560,564,2.6))
for z0,z1 in ((80.4,82.0),(125.0,133.0),(176.0,177.6)):
    rib=trimesh.creation.extrude_polygon(__import__('shapely.geometry',fromlist=['Polygon']).Polygon([(241.2,563.3),(241.2,583.0),(225.0,563.3)]),z1-z0)
    rib.apply_translation([0,0,z0]); cr=U(cr,rib)
duto=U(duto,cr)
# suporte do servo: chapa sob as abas + alma ligada a parede do duto
pl=D(B(263.4,276.8,558.6,592.0,41.3,43.8),B(SX-6.3,SX+6.3,SY-6.1,SY+17.1,40.0,44.5))
web=B(261.2,263.0,558.6,592.0,41.3,60.2)
duto=U(duto,pl,web)
duto=D(duto,grow(R['riser'],0.2))                                     # folga 0,2 para o riser (corte com a propria peca)
for x,y in ((SX,SY-8.3),(SX,SY+19.35)): duto=D(duto,CZ(x,y,40.5,44.5,1.8))
# fixacao no suporte do trilho: 2x M3 na barra de baixo (insertos)
FX=[(255.7,95.0),(255.7,165.0)]
for x,z in FX: duto=D(duto,CY(x,z,563.0,565.5,3.4))
R['duto']=big(duto)
lF=S3['l_F']
for x,z in FX: lF=D(lF,CY(x,z,558.0,563.2,4.0))
R['sup_lF']=lF
def bolt_y(x,z,y_top,L,hd=5.5,hh=1.6,d=3.0): return U(CY(x,z,y_top,y_top+hh,hd),CY(x,z,y_top-L,y_top,d))
hw=[bolt_y(x,z,564.9,6) for x,z in FX]
for z0,z1 in BZ:
    for x,z in ((BXS[0]+3.0,z0+3.0),(BXS[1]-3.0,z1-3.0)): hw.append(U(CY(x,z,583.3,584.9,5.5),CY(x,z,561.6,583.3,3.0)))
for x,y in ((SX,SY-8.3),(SX,SY+19.35)): hw.append(U(CZ(x,y,46.3,47.5,4.0),CZ(x,y,40.1,46.3,2.0)))
R['ferragens']=U(*hw)
# ---------- conferencias ----------
P=pickle.load(open('parts.pkl','rb')); chk={}
skip={'riser47','aletas1','thTrB','thTrA','tcRiser','dsS'}
for k in ('riser','aletas','barra','pinos','servo','sopradores','duto','sup_lF','ferragens'):
    m=R[k]
    for pid,lab,grp,pm in P:
        if grp not in ('prop','comum','ref') or pid in skip: continue
        try:
            if not (np.all(pm.bounds[0]<m.bounds[1]) and np.all(m.bounds[0]<pm.bounds[1])): continue
            x=I(m,pm).volume
        except Exception as e: x=str(e)[:20]
        if not isinstance(x,float) or x>0.05: chk[k+'_x_'+pid]=round(x,2) if isinstance(x,float) else x
ks=['riser','aletas','barra','servo','sopradores','duto','sup_lF']
for i,a in enumerate(ks):
    for b in ks[i+1:]:
        x=I(R[a],R[b]).volume
        if x>0.05: chk[a+'_x_'+b]=round(x,2)
# aletas giradas 60 graus (abertas) contra riser, duto, moldura
for ang in (35.0,60.0):
    rot=[]
    for a,y in zip(AL,YC):
        q=a.copy(); q.apply_transform(trimesh.transformations.rotation_matrix(np.radians(ang),[0,0,1],[XP,y,0])); rot.append(q)
    for b in ('riser','duto'):
        x=sum(I(q,R[b]).volume for q in rot)
        if x>0.05: chk['aberta%d_x_%s'%(ang,b)]=round(x,2)
    Pm={p[0]:p[3] for p in P}
    x=sum(I(q,Pm['molAl47']).volume for q in rot)
    if x>0.05: chk['aberta%d_x_molAl47'%ang]=round(x,2)
# espelho para a janela de tras
for k in list(R.keys()):
    if k in ('riser',): continue
    R[k+'_T']=mz(R[k])
rT=mz(R['riser']); R['riser_T']=rT
R['sup_lT']=D(S3['l_T'],*[CY(x,-z,558.0,563.2,4.0) for x,z in FX]); del R['sup_lF_T']
LOG={'chk':chk,'vol':{k:bool(v.is_volume) for k,v in R.items()},'tam':{k:round(float(max(v.extents)),1) for k,v in R.items() if k in ('duto','barra','riser')}}
print(json.dumps(LOG,default=str))
pickle.dump(R,open('EX.pkl','wb'))
