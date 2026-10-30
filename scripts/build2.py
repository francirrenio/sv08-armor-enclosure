import numpy as np, trimesh, json, pickle
exec(open('load.py').read()); exec(open('geo.py').read())
from shapely.geometry import box as sbox, Polygon
P=pickle.load(open('P.pkl','rb'))   # soleira, porta, batente da v1
Q={}; LOG={}
HF=np.load('frontZ.npy'); pf=pockets(HF,45.0,0.0,0.5,262.5,265.0)
HS_=np.load('sideX.npy'); ps=pockets(HS_,-15.0,0.0,0.5,257.5,260.0)
def keys_front(xr,yr,z0=263.8,z1=276.2,amin=25):
    out=[]; clip=sbox(xr[0],yr[0],xr[1],yr[1])
    for p in pf:
        q=p.buffer(-0.4).intersection(clip)
        for g in (q.geoms if hasattr(q,'geoms') else [q]):
            if not g.is_empty and g.area>=amin: out.append(prism_xy(g,z0,z1))
    return out
def pilot(m,pts,axis,d=2.5,a0=None,a1=None):
    for p in pts:
        if axis=='z': m=D(m,CYL([p[0],p[1],a0],[p[0],p[1],a1],d))
        if axis=='x': m=D(m,CYL([a0,p[0],p[1]],[a1,p[0],p[1]],d))
    return m
def plate_xy(x0,x1,y0,y1,z0,z1,c):
    m=B(x0,x1,y0,y1,z0,z1)
    for pp,n in (([x0,(y0+y1)/2,z1-c],(-1,0,1)),([x1,(y0+y1)/2,z1-c],(1,0,1)),([(x0+x1)/2,y0,z1-c],(0,-1,1)),([(x0+x1)/2,y1,z1-c],(0,1,1))):
        m=I(m,HS(pp,n))
    return m
# ================= FRENTE =================
ZC0,ZC1=276.0,280.0          # estrutura (preta, escondida): face Z 280 plana -> vai na mesa
SEAM=125.0
tongU=Polygon([(SEAM+0.2,56.0),(SEAM+0.2,62.0),(SEAM-4.5,63.5),(SEAM-4.5,54.5)])
tongL=Polygon([(SEAM+0.2,8.0),(SEAM+0.2,14.0),(SEAM-4.5,15.5),(SEAM-4.5,6.5)])
# estrutura direita
eD=B(SEAM+0.1,258.0,2.0,81.0,ZC0,ZC1)
eD=D(eD,B(SEAM,220.6,19.5,40.5,ZC0-1,ZC1+1))                      # janela do LED
kD=keys_front((127.5,194.0),(40.6,60.8))+keys_front((127.5,194.0),(4.4,19.1))
eD=U(eD,*kD,prism_xy(tongU,ZC0,ZC1),prism_xy(tongL,ZC0,ZC1))
LOG['chaves_estrutura_D']=len(kD)
# estruturas centrais (sup e inf)
eCs=B(-124.9,SEAM-0.1,40.5,81.0,ZC0,ZC1); eCi=B(-124.9,SEAM-0.1,2.0,19.5,ZC0,ZC1)
kCs=keys_front((66.0,122.0),(40.6,60.8)); kCi=keys_front((66.0,122.0),(4.4,19.1))
eCs=U(eCs,*kCs); eCi=U(eCi,*kCi)
eCs=D(eCs,prism_xy(tongU.buffer(0.2,join_style=2),262.0,285.0)); eCi=D(eCi,prism_xy(tongL.buffer(0.2,join_style=2),262.0,285.0))
LOG['chaves_centrais']=len(kCs)+len(kCi)
# placas de acabamento (seams desencontradas da emenda das estruturas: X 75 = 50 mm)
SX0,SX1=75.0,257.5
pG=plate_xy(SX0,SX1,64.0,80.8,ZC1,286.0,1.5)          # verde (no plano da moldura da porta)
pBs=plate_xy(SX0,SX1,41.0,63.5,ZC1,284.0,1.0)         # preta de cima
pBi=plate_xy(SX0,SX1,2.0,19.0,ZC1,284.0,1.0)          # preta de baixo
pCs=plate_xy(-SX0+0.5,SX0-0.5,41.0,63.5,ZC1,284.0,1.0); pCg=plate_xy(-SX0+0.5,SX0-0.5,64.0,80.8,ZC1,286.0,1.5); pCi=plate_xy(-SX0+0.5,SX0-0.5,2.0,19.0,ZC1,284.0,1.0)
# parafusos aparentes, simetricos em cada placa (centro X 166,25 -> +-58)
cx=(SX0+SX1)/2; XS=[round(cx-58,2),round(cx+58,2)]; XC=[-45.0,45.0]
SG=[(x,72.4) for x in XS]; SB=[(x,52.2) for x in XS]; SI=[(x,10.5) for x in XS]
SCg=[(x,72.4) for x in XC]; SCs=[(x,52.2) for x in XC]; SCi=[(x,10.5) for x in XC]
for nm,m,pts in (('pG',pG,SG),('pBs',pBs,SB),('pBi',pBi,SI),('pCg',pCg,SCg),('pCs',pCs,SCs),('pCi',pCi,SCi)):
    m=pilot(m,pts,'z',3.4,ZC1-1,290); globals()[nm]=m
eD=pilot(eD,[p for p in SG+SB+SI if p[0]>SEAM],'z',2.5,ZC0-1,ZC1+1)
eD=pilot(eD,[p for p in SG if p[0]>SEAM],'z',3.4,ZC0-1,ZC1+1)   # verde: atravessa ate a soleira
eCs=pilot(eCs,[p for p in SG+SB if p[0]<SEAM]+SCg+SCs,'z',2.5,ZC0-1,ZC1+1)
eCi=pilot(eCi,[p for p in SI if p[0]<SEAM]+SCi,'z',2.5,ZC0-1,ZC1+1)
# soleira (da v1) com pilotos nas posicoes novas dos parafusos do verde
sol=M['SV-30-03c soleira (degrau) (2 de 2)']
alta=I(B(53.0,226.4,80.0,96.0,263.0,275.0),HS([140,93.0,263.0],(0,1,-1)))
sol=U(sol,alta,B(176.0,220.0,81.0,85.0,236.0,263.5))
for x in (185.5,210.5): sol=D(sol,CYL([x,78,240.5],[x,90,240.5],3.4),CYL([x,83.4,240.5],[x,90,240.5],6.2))
sol=pilot(sol,[p for p in SG if 55<p[0]<225],'z',2.5,262.0,276.0)
Q['frente_estrutura_D']=eD; Q['frente_estrutura_central_sup']=eCs; Q['frente_estrutura_central_inf']=eCi
Q['frente_placa_verde_D']=pG; Q['frente_placa_preta_sup_D']=pBs; Q['frente_placa_preta_inf_D']=pBi
Q['frente_placa_verde_C']=pCg; Q['frente_placa_preta_sup_C']=pCs; Q['frente_placa_preta_inf_C']=pCi
Q['soleira']=sol
# ================= LATERAL (laranja) =================
Z0,Z1=-11.95,273.4; XP=278.8   # face plana da estrutura (vai na mesa); placas por cima ate 281,8
pele=B(275.8,XP,2.0,93.0,Z0,Z1)
quadro=[B(268.7,275.9,2.0,6.0,Z0,229.0),B(268.7,275.9,89.0,93.0,Z0,229.0),B(273.0,275.9,2.0,93.0,229.0,Z1),
        B(268.7,275.9,2.0,93.0,Z0,Z0+4.0),B(268.7,275.9,2.0,93.0,225.0,229.0)]
for z in (60.0,190.0): quadro.append(B(268.7,275.9,2.0,93.0,z-1.5,z+1.5))
est=U(pele,*quadro)
# topo plano em Y 93 ate a face externa (assento da espinha) e chaves em todos os bolsos uteis (impressao com a face externa na mesa)
kL=[]; clipL=sbox(-8.0,4.0,224.0,72.0)
for p in ps:
    q=p.buffer(-0.4).intersection(clipL)
    for gg in (q.geoms if hasattr(q,'geoms') else [q]):
        if not gg.is_empty and gg.area>=60: kL.append(prism_zy(gg,258.8,276.0))
est=U(est,*kL); LOG['chaves_lateral']=len(kL)
NUT=[(20.0,224.0),(47.0,224.0),(20.0,116.0),(47.0,116.0),(72.0,129.875),(72.0,181.875)]
for y,z in NUT: est=U(est,CYL([268.7,y,z],[276.0,y,z],9.0))
for y,z in NUT:
    est=D(est,CYL([260,y,z],[290,y,z],3.4))
    hexa=trimesh.creation.cylinder(radius=6.0/np.sqrt(3),height=4.0,sections=6); hexa.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0])); hexa.apply_translation([270.6,y,z]); est=D(est,hexa)
LS=[(86.0,20.0),(86.0,255.0),(30.0,20.0),(30.0,255.0)]           # parafusos da placa preta (simetricos)
est=pilot(est,LS,'x',2.5,268.0,XP+0.1)
for y,z in ((18.0,220.0),(52.0,254.0)): est=D(est,CYL([260,y,z],[290,y,z],3.4),CYL([276.9,y,z],[279.0,y,z],6.2))
# placa preta lateral: moldura com janelas para as verdes (folga 0,5 = linha de sombra)
pl=B(XP,281.8,2.0,93.0,Z0,Z1)
for pp,n in (([XP,47,Z0],( 0,0,-1)),):
    pass
for k in ('22_lateral_placa_3_1_D','22_lateral_faixa_3_1_D'): pl=D(pl,grow(M[k],0.5))
pl=pilot(pl,LS,'x',3.4,XP-1,290)
Q['lateral_estrutura_D']=est; Q['lateral_placa_preta_D']=pl
# ================= ferragens novas =================
def bolt(p,axis,L,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*L,d))
HW=[bolt([x,y,286.0 if y>60 else 284.0],[0,0,1],12) for x,y in SG+SB+SI+SCg+SCs+SCi]
HW+=[bolt([x,85.0,240.5],[0,1,0],10) for x in (185.5,210.5)]
HW+=[bolt([281.8,y,z],[1,0,0],10) for y,z in LS]
HW.append(bolt([XP,18.0,220.0],[1,0,0],16))
Q['ferragens']=U(*HW)
LOG['watertight']={k:bool(v.is_watertight) for k,v in Q.items()}
pickle.dump(Q,open('Q.pkl','wb')); print(json.dumps(LOG,indent=1))
