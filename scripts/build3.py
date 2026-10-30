import numpy as np, trimesh, json, pickle
exec(open('load.py').read()); exec(open('geo.py').read())
from shapely.geometry import box as sbox, Polygon
P=pickle.load(open('P.pkl','rb')); Q=pickle.load(open('Q.pkl','rb'))
R={}; LOG={}
HF=np.load('frontZ.npy'); pf=pockets(HF,45.0,0.0,0.5,262.5,265.0)
def keys_front(xr,yr,z0=263.8,z1=276.2,amin=25):
    out=[]; clip=sbox(xr[0],yr[0],xr[1],yr[1])
    for p in pf:
        q=p.buffer(-0.4).intersection(clip)
        for g in (q.geoms if hasattr(q,'geoms') else [q]):
            if not g.is_empty and g.area>=amin: out.append(prism_xy(g,z0,z1))
    return out
def holes_z(m,pts,d,z0,z1):
    for x,y in pts: m=D(m,CYL([x,y,z0],[x,y,z1],d))
    return m
def mirrorX(m):
    c=m.copy(); c.apply_transform(np.diag([-1,1,1,1]));
    if c.volume<0: c.invert()
    return c
ZS0,ZS1=276.0,279.0      # estrutura escondida; face Z 279 plana (vai na mesa)
S1=175.0                 # emenda das estruturas (50 mm da emenda das placas em X 125)
def tong(x,yc): return Polygon([(x+0.2,yc-3),(x+0.2,yc+3),(x-4.5,yc+4.5),(x-4.5,yc-4.5)])
tU,tL=tong(S1,59.0),tong(S1,11.0)
tU0,tL0=tong(0.0,59.0),tong(0.0,11.0)
# ---- estruturas da frente ----
eD=B(S1+0.1,258.0,2.0,81.0,ZS0,ZS1)
eD=D(eD,B(S1,220.6,19.5,40.5,ZS0-1,ZS1+1))
eD=U(eD,*keys_front((S1+1.5,194.0),(40.6,60.8)),*keys_front((S1+1.5,194.0),(4.4,19.1)),prism_xy(tU,ZS0,ZS1),prism_xy(tL,ZS0,ZS1))
eCs=B(0.1,S1-0.1,40.5,81.0,ZS0,ZS1); eCi=B(0.1,S1-0.1,2.0,19.5,ZS0,ZS1)
eCs=U(eCs,*keys_front((45.5,S1-1.5),(40.6,60.8))); eCi=U(eCi,*keys_front((45.5,S1-1.5),(4.4,19.1)))
eCs=D(eCs,prism_xy(tU.buffer(0.2,join_style=2),262,285)); eCi=D(eCi,prism_xy(tL.buffer(0.2,join_style=2),262,285))
eCsL=D(mirrorX(eCs),prism_xy(tU0.buffer(0.2,join_style=2),262,285)); eCiL=D(mirrorX(eCi),prism_xy(tL0.buffer(0.2,join_style=2),262,285))
eCs=U(eCs,prism_xy(tU0,ZS0,ZS1)); eCi=U(eCi,prism_xy(tL0,ZS0,ZS1))
# ---- placas pretas = camada externa das pecas atuais (mesmo desenho) ----
roxa=U(M['10_chassis_3_1'],B(125.1,258.0,55.0,81.0,276.0,284.0))       # parte de cima que subiu
pR=I(roxa,B(100,300,0,90,ZS1,290))
# detalhe verde na parte que subiu: linha esquerda no prolongamento da diagonal do rebaixo da roxa; ponta para o canto (como a seta da faixa lateral)
gpoly=Polygon([(168.1,62.0),(193.6,79.0),(248.0,79.0),(255.0,70.5),(248.0,62.0)])
pR=D(pR,prism_xy(gpoly.buffer(0.5,join_style=2),ZS1-1,290))
def chamfer_prism(poly,z0,z1,c):
    lo=prism_xy(poly,z0,z1-c); top=None
    m=prism_xy(poly,z0,z1)
    inner=poly.buffer(-c,join_style=2)
    # chanfro 45: interseccao de prismas escalonados (aprox. por 3 degraus finos -> usar loft simples)
    steps=6
    parts=[prism_xy(poly,z0,z1-c)]
    for i in range(steps):
        t0=z1-c+c*i/steps; t1=z1-c+c*(i+1)/steps; pp=poly.buffer(-c*(i+0.5)/steps,join_style=2)
        parts.append(prism_xy(pp,t0,t1))
    return U(*parts)
gV=chamfer_prism(gpoly,ZS1,285.0,1.0)
SG=[(202.0,72.0),(234.0,72.0)]
gV=holes_z(gV,SG,3.4,ZS1-1,290)
SR=[(150.0,48.0),(228.0,48.0),(150.0,10.0),(228.0,10.0)]        # escondidos sob a moldura verde do LED
pR=holes_z(pR,SR,6.2,280.2,290); pR=holes_z(pR,SR+SG+[(146.0,72.0),(248.0,52.0),(248.0,10.5)],3.4,ZS1-1,290)
p21=I(M['10_chassis_2_1'],B(-200,200,0,90,ZS1,290)); S21=[(-90.0,72.0),(90.0,72.0)]; p21=holes_z(p21,S21,3.4,ZS1-1,290)
p22=I(M['10_chassis_2_2'],B(-200,200,0,90,ZS1,290)); S22=[(-100.0,11.5),(100.0,11.5)]; p22=holes_z(p22,S22,3.4,ZS1-1,290); p22=holes_z(p22,S22,6.2,279.3,290)   # sob a regua verde (cabeca embutida)
# pilotos nas estruturas
allS=SR+SG+[(146.0,72.0),(248.0,52.0),(248.0,10.5)]+S21+S22
def pil(m):
    return holes_z(m,[(x,y) for x,y in allS],2.5,ZS0-1,ZS1+1)
eD=pil(eD); eCs=pil(eCs); eCi=pil(eCi); eCsL=pil(eCsL); eCiL=pil(eCiL)
sol=Q['soleira']
sol=holes_z(sol,[p for p in SG if p[0]<225],2.5,262,276)
R.update({'est_D':eD,'est_Cs':eCs,'est_Ci':eCi,'est_CsL':eCsL,'est_CiL':eCiL,'placa_roxa':pR,'placa_21':p21,'placa_22':p22,'verde_topo':gV,'soleira':sol})
# ---- lateral: placa = camada externa da laranja atual (mesmo desenho) ----
XP=278.8
pL=I(M['21_lateral_chassis_2_D'],B(XP,290,0,100,-30,290))
LS=[(86.0,20.0),(86.0,255.0),(30.0,20.0),(30.0,255.0)]
for k in ('22_lateral_placa_3_1_D','22_lateral_faixa_3_1_D'): pL=D(pL,grow(M[k],0.5))
for y,z in LS: pL=D(pL,CYL([XP-1,y,z],[290,y,z],3.4))
R['placa_lateral']=pL; R['est_lateral']=Q['lateral_estrutura_D']
# ---- ferragens ----
def bolt(p,axis,L,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*L,d))
HW=[bolt([x,y,285.0],[0,0,1],12) for x,y in SG]+[bolt([x,y,284.0],[0,0,1],8) for x,y in [(146.0,72.0),(248.0,52.0),(248.0,10.5)]+S21]
HW+=[bolt([x,y,280.3],[0,0,1],7) for x,y in SR]+[bolt([x,y,279.35],[0,0,1],6) for x,y in S22]
HW+=[bolt([x,85.0,240.5],[0,1,0],10) for x in (185.5,210.5)]+[bolt([281.8,y,z],[1,0,0],10) for y,z in LS]+[bolt([XP,18.0,220.0],[1,0,0],16)]
R['ferragens']=U(*HW)
LOG['wt']={k:bool(v.is_watertight) for k,v in R.items()}
pickle.dump(R,open('R.pkl','wb')); print(json.dumps(LOG))
