import numpy as np, trimesh, json, pickle
exec(open('load.py').read()); exec(open('geo.py').read())
from shapely.geometry import box as sbox
P={}   # propostas
LOG={}
# ---------- bolsos da base (frente e lateral) ----------
HF=np.load('frontZ.npy')   # Y 0..81 (0.5) x X 45..270
pf=pockets(HF,45.0,0.0,0.5,262.5,265.0)
HS_=np.load('sideX.npy')   # Y 0..82 x Z -15..276
ps=pockets(HS_,-15.0,0.0,0.5,257.5,260.0)
LOG['bolsos_frente']=len(pf); LOG['bolsos_lado']=len(ps)
def keys_front(xr,yr,z0=263.8,z1=276.2):
    out=[]
    clip=sbox(xr[0],yr[0],xr[1],yr[1])
    for p in pf:
        q=p.buffer(-0.4).intersection(clip)
        if q.is_empty or q.area<25: continue
        for g in (q.geoms if hasattr(q,'geoms') else [q]):
            if g.area<25: continue
            out.append(prism_xy(g,z0,z1))
    return out
# ---------- A. roxa (10_chassis_3_1) ----------
roxa=M['10_chassis_3_1']
roxa=U(roxa,B(125.1,258.0,55.0,81.0,276.0,284.0))                  # sobe ate Y 81 em toda a largura (porta encurtada)
kR=keys_front((127.5,194.0),(40.6,60.8)); LOG['chaves_roxa']=len(kR)
roxa=U(roxa,*kR)
# rabo de andorinha na emenda X 125 com a 10_chassis_2_1 (desliza em Z junto com as chaves)
from shapely.geometry import Polygon
tong=Polygon([(125.3,56.0),(125.3,62.0),(120.6,63.5),(120.6,54.5)])
lin=prism_xy(tong,276.0,284.0)
roxa=U(roxa,lin)
# rebaixo para o friso verde + furos dos parafusos que prendem verde+roxa na soleira
roxa=D(roxa,B(131.0,252.0,63.0,77.0,282.0,290.0))
SCR=[(161.5,70.0),(221.5,70.0)]
for x,y in SCR: roxa=D(roxa,CYL([x,y,270],[x,y,290],3.4))
P['10_chassis_3_1 (proposta)']=roxa
# friso verde
from shapely.geometry import Polygon as Pg
g=B(131.2,251.8,63.2,76.8,282.0,286.0)
# chanfro 45 x 1.5 nas arestas externas (4 lados)
for p,n in ((( 131.2,0,286-1.5),(-1,0,1)),((251.8,0,286-1.5),(1,0,1)),((0,63.2,286-1.5),(0,-1,1)),((0,76.8,286-1.5),(0,1,1))):
    pp=list(p)
    if n[0]==-1: pp=[131.2+0,70,284.5]
    if n[0]==1: pp=[251.8,70,284.5]
    if n[1]==-1: pp=[190,63.2,284.5]
    if n[1]==1: pp=[190,76.8,284.5]
    nn=np.array(n,float)/np.sqrt(2)
    # remove o que esta alem do plano pela aresta: pontos com (q-pp).nn > 0
    g=D(g,HS(np.array(pp),-nn) if False else None)
def chamfer_box(x0,x1,y0,y1,z0,z1,c):
    m=B(x0,x1,y0,y1,z0,z1)
    for pp,n in (([x0,0,z1-c],(-1,0,1)),([x1,0,z1-c],(1,0,1)),([0,y0,z1-c],(0,-1,1)),([0,y1,z1-c],(0,1,1))):
        pp=np.array(pp,float)
        if n[0]==0: pp[0]=(x0+x1)/2
        else: pp[1]=(y0+y1)/2
        m=I(m,HS(pp,n))
    return m
verde=chamfer_box(131.2,251.8,63.2,76.8,282.0,286.0,1.5)
for x,y in SCR: verde=D(verde,CYL([x,y,280],[x,y,290],3.4))
P['SV08_Friso_Base_FD_Green (novo)']=verde
# ---------- B. central 10_chassis_2_1 ----------
c21=M['10_chassis_2_1']
kC=keys_front((66.0,122.5),(40.6,60.8)); LOG['chaves_central']=len(kC)
c21=U(c21,*kC)
c21=D(c21,prism_xy(tong.buffer(0.2,join_style=2),262.0,285.0))
P['10_chassis_2_1 (proposta)']=c21
# ---------- C. soleira (degrau) mais alta + aba de fixacao no deck ----------
sol=M['SV-30-03c soleira (degrau) (2 de 2)']
alta=B(53.0,226.4,80.0,96.0,263.0,275.0)
alta=I(alta,HS([140,93.0,263.0],(0,1,-1)))     # chanfro 3 mm na aresta de tras do topo
sol=U(sol,alta)
aba=B(176.0,220.0,81.0,85.0,236.0,263.5)
sol=U(sol,aba)
for x in (185.5,210.5):
    sol=D(sol,CYL([x,78,240.5],[x,90,240.5],3.4),CYL([x,83.4,240.5],[x,90,240.5],6.2))
for x,y in SCR: sol=D(sol,CYL([x,y,262],[x,y,276],2.5))
P['SV-30-03c soleira (degrau) (proposta)']=sol
# ---------- D. porta direita mais baixa (fundo em Y 82) ----------
DY=19.5
def encurta(m,ysplit=101.0):
    a=I(m,B(-50,300,ysplit,700,200,300)); b=I(m,B(-50,300,0,ysplit,200,300)); b.apply_translation([0,DY,0])
    return U(a,b)
P['SV-30-01a moldura (proposta)']=encurta(M['SV-30-01a moldura (1 de 2)'])
P['SV-30-01c vedacao EPDM (proposta)']=encurta(M['SV-30-01c vedacao EPDM 8x2'])
P['SV-30-01b acrilico (proposta)']=I(M['SV-30-01b acrilico 225x453'],B(-50,300,70.5+DY,600,200,300))
P['SV-30-03a batente lateral D (proposta)']=I(M['SV-30-03a batente lateral D (1 de 3)'],B(200,260,81.0,300,200,300))
# ---------- E. laranja (21_lateral_chassis_2_D) refeita: em pe na mesa (base Y 2 plana) ----------
Z0,Z1=-11.95,273.4
pele=B(275.8,281.8,2.0,93.0,Z0,Z1)
quadro=[B(268.7,275.9,2.0,6.0,Z0,229.0),B(268.7,275.9,89.0,93.0,Z0,229.0),          # fundo e topo
        B(273.0,275.9,2.0,93.0,229.0,Z1),B(273.0,281.8,89.0,93.0,229.0,Z1),         # zona do P01 (por fora dele)
        B(268.7,275.9,2.0,93.0,Z0,Z0+4.0),B(268.7,275.9,2.0,93.0,225.0,229.0)]     # cabeceiras
for z in (60.0,190.0): quadro.append(B(268.7,275.9,2.0,93.0,z-1.5,z+1.5))
lar=U(pele,*quadro)
# chaves nos bolsos em V da lateral da base (fileira de cima, ponta para baixo -> imprime sem suporte)
kL=[]
clipL=sbox(-8.0,36.0,224.0,72.0)
for p in ps:
    q=p.buffer(-0.4).intersection(clipL)
    if q.is_empty or q.area<30: continue
    for gg in (q.geoms if hasattr(q,'geoms') else [q]):
        if gg.area<30: continue
        c=gg.centroid
        # so V (ponta para baixo): vertice mais baixo isolado
        x0,y0,x1,y1=gg.bounds
        wb=gg.intersection(sbox(x0-1,y0+0.2*(y1-y0),x1+1,y0+0.3*(y1-y0))).area
        wt=gg.intersection(sbox(x0-1,y1-0.3*(y1-y0),x1+1,y1-0.2*(y1-y0))).area
        if not (wt>1.6*wb and y1-y0>15): continue
        kL.append(prism_zy(gg,258.8,276.0))
LOG['chaves_laranja']=len(kL)
lar=U(lar,*kL)
# placas verdes 22 assentadas em rebaixo (folga 0,2) + bossas com porca das placas
for k in ('22_lateral_placa_3_1_D','22_lateral_faixa_3_1_D'): lar=D(lar,grow(M[k],0.2))
NUT=[(20.0,224.0),(47.0,224.0),(20.0,116.0),(47.0,116.0),(72.0,129.875),(72.0,181.875)]
for y,z in NUT:
    lar=U(lar,CYL([268.7,y,z],[276.0,y,z],9.0))
for y,z in NUT:
    lar=D(lar,CYL([260,y,z],[290,y,z],3.4))
    hexa=trimesh.creation.cylinder(radius=6.0/np.sqrt(3),height=4.0,sections=6); hexa.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0])); hexa.apply_translation([270.6,y,z])
    lar=D(lar,hexa)
# fixacoes: M3 no furo da lateral da base (Y18 Z220) e M3 no P01 (Y52 Z254, ja existente)
for y,z in ((18.0,220.0),(52.0,254.0)):
    lar=D(lar,CYL([260,y,z],[290,y,z],3.4),CYL([278.8,y,z],[290,y,z],6.2))
# folgas: perfil e P01
LOG['lar_x_P01']=round(I(lar,M['65_suporte_P01_D']).volume,3); LOG['lar_x_perfil']=round(I(lar,M['Corpo1@072.stl']).volume,3)
P['21_lateral_chassis_2_D (proposta)']=lar
# ---------- ferragens novas ----------
HW=[]
def bolt(p,axis,L,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float)
    return U(CYL(p,p+a*hh,hd),CYL(p+a*hh*0,p-a*L,d))
for x,y in SCR: HW.append(bolt([x,y,286.0],[0,0,1],12))
for x in (185.5,210.5): HW.append(bolt([x,85.0,240.5],[0,1,0],10))
HW.append(bolt([281.8-3.0,18.0,220.0],[1,0,0],16))
P['M3 novos (proposta)']=U(*HW)
LOG['vol']={k:round(v.volume,1) for k,v in P.items()}
LOG['watertight']={k:bool(v.is_watertight) for k,v in P.items()}
pickle.dump(P,open('P.pkl','wb'))
print(json.dumps(LOG,indent=1))
