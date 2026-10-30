# EXAUSTOR_LATERAL (modelo 1): em cada janela de aletas do riser lateral (2 por lado), 2 sopradores 4020 EM PE dentro da
# janela do suporte do trilho (entrada para a camara, no nivel do perfil), caixa que forma a camara de ar atras das aletas,
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
XP=281.1; YC=[574.0+44.0/6,596.0,618.0-44.0/6]   # eixo das aletas (passo 44/3)
ZW0,ZW1=58.0,196.0; YW0,YW1=574.0,618.0          # janela do riser
R={}
# ---------- riser: janela atravessa (tirava a pelicula de 0,2 de tras) + rasgos em U dos pinos (abertos para dentro) ----------
rs=D(CT['riser47'],B(276.5,284.5,571.0,621.0,ZW0,ZW1))
# BATENTES: a aleta de baixo e a de cima fecham numa meia-esquadria do proprio riser (mesma regra das aletas entre si)
lipB=U(B(278.0,284.0,571.0,572.95,ZW0,ZW1),B(281.15,284.0,571.0,574.95,ZW0,ZW1))
lipT=U(B(278.0,281.05,617.05,621.0,61.4,ZW1),B(281.05,284.0,619.05,621.0,ZW0,ZW1))   # metade de dentro some na faixa do bracinho (Z<61,4)
rs=U(rs,lipB,lipT)
rs=D(rs,B(276.8,280.7,563.0,621.0,54.8,58.0))                         # rebaixo por dentro para a barra de ligacao andar (ate 2,6 para fora)
for y in YC:
    for z0,z1 in ((56.0,58.1),(195.9,198.0)):
        rs=D(rs,CZ(XP,y,z0,z1,3.3),B(276.0,XP,y-1.65,y+1.65,z0,z1))
R['riser']=rs
# ---------- aletas moveis ----------
from shapely.geometry import Polygon as _Pg
AL=[]
T0,T1=279.9,282.3; LAP=1.0; GL=0.05                  # ALETAS_RETAS: placa reta de 2,4, meia-esquadria de 1 mm nas bordas que se tocam
YE=[574.0,574.0+44.0/3,574.0+88.0/3,618.0]          # todas as bordas em meia-esquadria (entre aletas e com os batentes)
ZA_0,ZA_1=58.2,195.8                                  # folga de 0,2 nas pontas da janela (58-196)
for k,y in enumerate(YC):
    top=[(T1,YE[k+1]+LAP-GL),(XP+GL,YE[k+1]+LAP-GL),(XP+GL,YE[k+1]-LAP-GL),(T0,YE[k+1]-LAP-GL)]
    bot=[(T0,YE[k]-LAP+GL),(XP-GL,YE[k]-LAP+GL),(XP-GL,YE[k]+LAP+GL),(T1,YE[k]+LAP+GL)]
    pg=_Pg(top+bot).buffer(0)
    c=trimesh.creation.extrude_polygon(pg,ZA_1-ZA_0); c.apply_translation([0,0,ZA_0])
    if c.volume<0: c.invert()
    if k==2:                                          # cantos de cima chanfrados 2,4: passam pelo raio 2 dos cantos da moldura ao abrir
        yt_=YE[3]+LAP-GL
        for tri in ([(ZA_0-1,yt_-3.4),(ZA_0-1,yt_+1),(ZA_0+3.4,yt_+1)],[(ZA_1+1,yt_-3.4),(ZA_1+1,yt_+1),(ZA_1-3.4,yt_+1)]):
            c=D(c,prism_zy(_Pg(tri),277.0,285.0))
    a=U(c,CZ(XP,y,56.4,ZA_0+0.05,3.0),CZ(XP,y,ZA_1-0.05,197.6,3.0))                       # pinos das pontas
    arm=B(273.6,280.5,y-2.4,y+2.4,58.2,61.0)                                       # bracinho (dentro da janela, atras da aleta)
    arm=U(arm,CZ(275.1,y,58.2,61.0,4.8))
    a=D(U(a,arm),CZ(275.1,y,57.5,61.5,2.1))
    AL.append(a)
R['aletas']=U(*AL)
for _i,_a in enumerate(AL): R['al%d'%(_i+1)]=_a                       # pecas separadas (animacao)
# ---------- barra de ligacao (Z 55,2-58,0) com extensao e rasgo para o pino do servo ----------
SX,SY=270.7,569.5; HR=5.0                            # eixo do servo e raio do braco
bar=U(B(273.6,276.6,577.0,614.0,55.2,58.0),B(263.4,276.6,564.6,577.0,55.2,58.0))
for y in YC: bar=U(bar,CZ(275.1,y,55.2,58.0,4.8))
for y in YC: bar=D(bar,CZ(275.1,y,54.6,58.6,2.1))
bar=D(bar,B(SX-HR-1.3,SX-HR+3.0,SY-1.15,SY+1.15,54.6,58.6))   # rasgo: o pino do braco anda ate 1,5 para fora em relacao a barra
R['barra']=bar
R['pinos']=U(*[CZ(275.1,y,55.4,60.9,2.0) for y in YC],CZ(SX-HR,SY,51.9,57.9,2.0))
# ---------- servo SG90 (eixo em +Z) ----------
sb=D(U(B(SX-6.1,SX+6.1,SY-5.9,SY+16.9,27.9,50.6),B(SX-6.1,SX+6.1,SY-10.65,SY+21.65,43.8,46.3),CZ(SX,SY,50.6,51.8,11.8),CZ(SX,SY,51.8,53.6,4.6)),*[CZ(SX,y,43.0,47.0,2.2) for y in (SY-8.3,SY+19.35)])
horn=U(CZ(SX,SY,51.9,53.6,7.0),B(SX-HR,SX,SY-2.0,SY+2.0,51.9,53.6),CZ(SX-HR,SY,51.9,53.6,4.0))
R['servo']=U(sb,D(horn,CZ(SX,SY,51.0,53.7,4.6)))
R['servo_corpo']=sb; R['horn']=D(U(horn,CZ(SX-HR,SY,51.9,57.9,2.0)),CZ(SX,SY,51.0,53.7,4.6))
R['barra_mov']=U(bar,*[CZ(275.1,y,55.4,60.9,2.0) for y in YC])
# ---------- sopradores 4020 EM PE na janela do suporte (entrada virada para a camara, no nivel do perfil) ----------
# a face de entrada fica em X 252,4 (1,9 mm para fora da face de dentro do perfil, X 250,5): nada entra no espaco do umbilical
BX=(252.4,272.4); BYY=(567.3,607.3); BZ=[(78.0,118.0),(128.0,168.0)]
IYC=0.5*(BYY[0]+BYY[1])
bl=[]
for z0,z1 in BZ:
    zc=0.5*(z0+z1)
    h=B(BX[0],BX[1],BYY[0],BYY[1],z0,z1)
    h=D(h,CYL([BX[0]-1,IYC,zc],[BX[0]+0.6,IYC,zc],27.0))                 # boca de entrada (virada para a camara)
    h=D(h,B(256.0,271.0,BYY[1]-1.5,BYY[1]+1,z0+2.0,z0+21.0))            # boca de saida (para cima, para a camara de ar atras das aletas)
    for y,z in ((BYY[0]+3.0,z0+3.0),(BYY[1]-3.0,z1-3.0)): h=D(h,CYL([BX[0]-1,y,z],[BX[1]+1,y,z],3.4))
    bl.append(h)
R['sopradores']=U(*bl)
# ---------- DUTO_2_PECAS: (A) caixa dos sopradores, na janela do suporte; (B) camara de ar entre o suporte e o riser ----------
# A imprime com a placa dos furos na mesa; B imprime com a parede de dentro (X 261,2) na mesa. Sem suporte nas duas.
# As duas sao presas no suporte do trilho (A: 2 M3 na barra de baixo; B: 4 M3 de lado nas barras) e se alinham por um ressalto de 1 mm.
ZA0,ZA1=74.2,174.6                                    # dentro da janela do suporte: entre o montante da emenda (73,5) e o da ponta (174,8)
XJ=261.2                                              # plano da junta (face de fora do suporte em 260,9)
# (A) caixa
A=D(B(250.8,XJ-0.2,563.3,611.2,ZA0,ZA1),B(252.4,XJ,564.9,609.6,ZA0+1.6,ZA1-1.6))
A=U(A,D(B(XJ-0.3,XJ+1.4,564.9,609.6,ZA0+1.6,ZA1-1.6),B(XJ-1,XJ+2,565.9,608.6,ZA0+2.6,ZA1-2.6)))   # ressalto de 1 mm que entra na janela da B
for z0,z1 in BZ:
    A=D(A,CYL([249.0,IYC,0.5*(z0+z1)],[253.0,IYC,0.5*(z0+z1)],30.0))      # entrada de ar
    A=U(A,B(252.4,XJ-0.2,564.9,BYY[0]-0.2,z0,z1))                          # calco embaixo do soprador
    for zz in (z0-1.8,z1+0.2):                                            # guias dos lados do soprador (bolso de 0,2)
        if ZA0+1.6<zz<ZA1-3.2: A=U(A,B(252.4,XJ-0.2,564.9,609.6,zz,zz+1.6))
    for y,z in ((BYY[0]+3.0,z0+3.0),(BYY[1]-3.0,z1-3.0)): A=D(A,CYL([250.0,y,z],[253.0,y,z],2.6))   # rosca direta na placa
FX=[(255.7,95.0),(255.7,145.0)]
for x,z in FX: A=D(A,CY(x,z,563.0,565.5,3.4),CY(x,z,564.8,566.8,6.2))   # furo + alojamento da cabeca no calco
# (B) camara: parede de dentro inteira (com a janela da A), paredes de cima/baixo/pontas, aba de baixo sobre a barra, suporte do servo
Bo=U(B(XJ,276.8,563.3,620.5,58.6,197.6),B(276.8,277.8,568.2,620.5,58.6,197.6),B(XJ,XJ+1.6,558.6,563.3,58.6,197.6))
Bi=U(B(XJ+1.6,279.0,564.9,618.9,60.2,196.0),B(272.2,279.0,564.9,618.9,50.0,196.0))
Bm=D(Bo,Bi,B(XJ-1,XJ+2,564.7,609.8,ZA0+1.4,ZA1-1.4))                 # janela da parede de dentro = ressalto da A + 0,2
Bm=D(Bm,B(272.2,279.0,560.0,625.0,50.0,61.3))                         # faixa livre para bracinhos e barra
pl=D(B(XJ,276.8,558.6,592.0,41.3,43.8),B(SX-6.3,SX+6.3,SY-6.1,SY+17.1,40.0,44.5))
web=B(XJ,263.0,558.6,592.0,41.3,60.2)
Bm=U(Bm,pl,web)
Bm=D(Bm,grow(R['riser'],0.2))
for x,y in ((SX,SY-8.3),(SX,SY+19.35)): Bm=D(Bm,CZ(x,y,40.5,44.5,1.8))
FB=[(616.0,90.0),(616.0,130.0),(560.8,85.0),(560.8,165.0)]               # 4 M3x8 de lado, insertos nas barras do suporte
for y,z in FB: Bm=D(Bm,CYL([XJ-0.5,y,z],[XJ+2.0,y,z],3.4),CYL([XJ+1.6,y,z],[XJ+4.0,y,z],6.0))
R['duto_A']=big(A); R['duto_B']=big(Bm); R['duto']=U(R['duto_A'],R['duto_B'])
lF=S3['l_F']
for x,z in FX: lF=D(lF,CY(x,z,558.0,563.2,4.0))
for y,z in FB: lF=D(lF,CYL([254.5,y,z],[261.0,y,z],4.0))
R['sup_lF']=lF
def bolt_y(x,z,y_top,L,hd=5.5,hh=1.6,d=3.0): return U(CY(x,z,y_top,y_top+hh,hd),CY(x,z,y_top-L,y_top,d))
hw=[bolt_y(x,z,564.9,6) for x,z in FX]+[U(CYL([XJ+1.6,y,z],[XJ+3.2,y,z],5.5),CYL([XJ+1.6,y,z],[XJ-6.4,y,z],3.0)) for y,z in FB]
for z0,z1 in BZ:                                                      # M3x22 cabeca abaulada, por fora do soprador, rosca na parede
    for y,z in ((BYY[0]+3.0,z0+3.0),(BYY[1]-3.0,z1-3.0)): hw.append(U(CYL([BX[1],y,z],[BX[1]+1.6,y,z],5.5),CYL([250.9,y,z],[BX[1],y,z],3.0)))
for x,y in ((SX,SY-8.3),(SX,SY+19.35)): hw.append(U(CZ(x,y,46.3,47.5,4.0),CZ(x,y,40.1,46.3,2.0)))
R['ferragens']=U(*hw)
xx=I(R['sopradores'],B(-400,250.5,0,1000,-400,400)).volume+I(R['duto'],B(-400,250.5,0,1000,-400,400)).volume+I(R['ferragens'],B(-400,250.5,0,1000,-400,400)).volume
# ---------- conferencias ----------
P=pickle.load(open('parts.pkl','rb')); chk={}
skip={'riser47','aletas1','thTrB','thTrA','tcRiser','dsS','exDuto','exSopr','exServo','exBarra','exHW','exBarF','exBarT','exHornF','exHornT','alF1','alF2','alF3','alT1','alT2','alT3'}
for k in ('riser','aletas','barra','pinos','servo','sopradores','duto_A','duto_B','sup_lF','ferragens'):
    m=R[k]
    for pid,lab,grp,pm in P:
        if grp not in ('prop','comum','ref') or pid in skip: continue
        try:
            if not (np.all(pm.bounds[0]<m.bounds[1]) and np.all(m.bounds[0]<pm.bounds[1])): continue
            x=I(m,pm).volume
        except Exception as e: x=str(e)[:20]
        if not isinstance(x,float) or x>0.05: chk[k+'_x_'+pid]=round(x,2) if isinstance(x,float) else x
xx=I(AL[0],AL[1]).volume+I(AL[1],AL[2]).volume
if xx>0.001: chk['fechada_aleta_x_aleta']=round(xx,3)
xx=I(R['barra'],R['pinos']).volume
if xx>0.05: chk['barra_x_pinos']=round(xx,2)
ks=['riser','aletas','barra','servo','sopradores','duto_A','duto_B','sup_lF','ferragens']
for i,a in enumerate(ks):
    for b in ks[i+1:]:
        x=I(R[a],R[b]).volume
        if x>0.05: chk[a+'_x_'+b]=round(x,2)
# aletas giradas 60 graus (abertas) contra riser, duto, moldura
for ang in (-35.0,-45.0):
    rot=[]
    for a,y in zip(AL,YC):
        q=a.copy(); q.apply_transform(trimesh.transformations.rotation_matrix(np.radians(ang),[0,0,1],[XP,y,0])); rot.append(q)
    for b in ('riser','duto'):
        x=sum(I(q,R[b]).volume for q in rot)
        if x>0.05: chk['aberta%d_x_%s'%(-ang,b)]=round(x,2)
    x=I(rot[0],rot[1]).volume+I(rot[1],rot[2]).volume
    if x>0.01: chk['aberta%d_aleta_x_aleta'%(-ang)]=round(x,3)
    Pm={p[0]:p[3] for p in P}
    x=sum(I(q,Pm['molAl47']).volume for q in rot)
    if x>0.05: chk['aberta%d_x_molAl47'%(-ang)]=round(x,2)
# ciclo completo: aletas giram ate -55, barra translada (raio 6), braco do servo gira asin(1,2 sen)
def Rz(a,px,py): return trimesh.transformations.rotation_matrix(np.radians(a),[0,0,1],[px,py,0])
for th in (-15.0,-30.0,-45.0):
    ph=np.degrees(np.arcsin(max(-1,1.2*np.sin(np.radians(th)))))
    als=[]
    for i,y in enumerate(YC):
        q=R['al%d'%(i+1)].copy(); q.apply_transform(Rz(th,XP,y)); als.append(q)
    bm=R['barra_mov'].copy(); bm.apply_translation([6-6*np.cos(np.radians(th)),-6*np.sin(np.radians(th)),0])
    hn=R['horn'].copy(); hn.apply_transform(Rz(ph,SX,SY))
    movs={'aletas':U(*als),'barra':bm,'braco':hn}
    for a_,m_ in movs.items():
        for b_ in ('riser','duto','servo_corpo','sup_lF','sopradores','ferragens'):
            x=I(m_,R[b_]).volume
            if x>0.05: chk['ciclo%d_%s_x_%s'%(-th,a_,b_)]=round(x,2)
    x=I(movs['braco'],D(bm,CZ(SX-HR+0,SY,0,0.01,0.1)) if False else bm).volume
    if x>0.05: chk['ciclo%d_braco_x_barra'%(-th)]=round(x,2)
    x=I(U(*als),bm).volume
    if x>0.05: chk['ciclo%d_aletas_x_barra'%(-th)]=round(x,2)
LOG_ANG={'ph55':round(float(np.degrees(np.arcsin(1.2*np.sin(np.radians(-55))))),1)}
# espelho para a janela de tras
for k in list(R.keys()):
    if k in ('riser',): continue
    R[k+'_T']=mz(R[k])
rT=mz(R['riser']); R['riser_T']=rT
R['sup_lT']=D(S3['l_T'],*[CY(x,-z,558.0,563.2,4.0) for x,z in FX],*[CYL([254.5,y,-z],[261.0,y,-z],4.0) for y,z in FB]); del R['sup_lF_T']
chk['para_dentro_do_perfil']=round(xx,3)
LOG={'chk':chk,'vol':{k:bool(v.is_volume) for k,v in R.items()},'tam':{k:round(float(max(v.extents)),1) for k,v in R.items() if k in ('duto','barra','riser')}}
print(json.dumps(LOG,default=str))
pickle.dump(R,open('EX.pkl','wb'))
