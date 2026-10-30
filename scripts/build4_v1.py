import numpy as np, trimesh, json, pickle
exec(open('load.py').read()); exec(open('geo.py').read())
from shapely.geometry import box as sbox, Polygon
P=pickle.load(open('P.pkl','rb')); Q=pickle.load(open('Q.pkl','rb'))
R={}; LOG={}
HF=np.load('frontZ.npy'); pf=pockets(HF,45.0,0.0,0.5,262.5,265.0)
def keys_front(xr,yr,z0=264.0,z1=276.2,amin=25,w=12.0,t=3.0,cl=0.3):
    # apoio fino: lingueta retangular w x t que assenta no fundo de cada bolso (em V fica travada nas duas diagonais)
    out=[]; clip=sbox(xr[0],yr[0],xr[1],yr[1])
    for p in pf:
        if not p.intersects(clip): continue
        pin=p.buffer(-cl,join_style=2)
        x0,y0,x1,y1=pin.bounds
        y=y0; ok=None
        while y<y1-t:
            ch=pin.intersection(sbox(x0-1,y,x1+1,y+t))
            if not ch.is_empty and ch.geom_type=='Polygon':
                cx0,_,cx1,_=ch.bounds
                if cx1-cx0>=w and ch.area>=w*t*0.99*(1 if False else 0)+0.0:
                    cx=(cx0+cx1)/2; r=sbox(cx-w/2,y,cx+w/2,y+t)
                    if pin.contains(r) and clip.contains(r): ok=r; break
            y+=0.25
        if ok is not None: out.append(prism_xy(ok,z0,z1))
    return out
def keys_front_old(xr,yr,z0=263.8,z1=276.2,amin=25):
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

# apoios escolhidos pelo dono (numeracao de apoios_numerados.png): ficam 1,6,7,9,10,16,17,19,20
KEEP={1,6,7,9,10,16,17,19,20}
_ZON=[((S1+1.5,194.0),(40.6,60.8)),((S1+1.5,194.0),(4.4,19.1)),((45.5,S1-1.5),(40.6,60.8)),((45.5,S1-1.5),(4.4,19.1))]
_ALL=[]
for zi,(xr,yr) in enumerate(_ZON):
    clip=sbox(xr[0],yr[0],xr[1],yr[1])
    for p in pf:
        q=p.buffer(-0.4).intersection(clip)
        for g in (q.geoms if hasattr(q,'geoms') else [q]):
            if not g.is_empty and g.area>=25: _ALL.append((zi,g))
def keys_sel(zi): return [prism_xy(g,263.8,276.2) for i,(z,g) in enumerate(_ALL,1) if z==zi and i in KEEP]
# ---- estruturas da frente ----
eD=B(S1+0.1,258.0,2.0,81.0,ZS0,ZS1)
eD=D(eD,B(S1,220.6,19.5,40.5,ZS0-1,ZS1+1))
eD=U(eD,*keys_sel(0),*keys_sel(1),prism_xy(tU,ZS0,ZS1),prism_xy(tL,ZS0,ZS1))
eCs=B(0.1,S1-0.1,40.5,81.0,ZS0,ZS1); eCi=B(0.1,S1-0.1,2.0,19.5,ZS0,ZS1)
eCs=U(eCs,*keys_sel(2)); eCi=U(eCi,*keys_sel(3))
eCs=D(eCs,prism_xy(tU.buffer(0.2,join_style=2),262,285)); eCi=D(eCi,prism_xy(tL.buffer(0.2,join_style=2),262,285))
eCsL=D(mirrorX(eCs),prism_xy(tU0.buffer(0.2,join_style=2),262,285)); eCiL=D(mirrorX(eCi),prism_xy(tL0.buffer(0.2,join_style=2),262,285))
eCs=U(eCs,prism_xy(tU0,ZS0,ZS1)); eCi=U(eCi,prism_xy(tL0,ZS0,ZS1))
# ---- placas pretas = camada externa das pecas atuais (mesmo desenho) ----
roxa=U(M['10_chassis_3_1'],B(125.1,258.0,55.0,81.0,276.0,284.0))       # parte de cima que subiu
pR=I(roxa,B(100,300,0,90,ZS1,290))
# detalhe verde na parte que subiu: linha esquerda no prolongamento da diagonal do rebaixo da roxa; ponta para o canto (como a seta da faixa lateral)
gpoly=Polygon([(168.1,62.0),(193.6,79.0),(248.0,79.0),(255.0,70.5),(248.0,62.0)])
ZF=281.0
cband=Polygon([(-110.0,62.0),(110.0,62.0),(135.5,79.0),(-135.5,79.0)])     # faixa verde central (mesma altura da faixa lateral)
pR=D(pR,prism_xy(gpoly.buffer(0.5,join_style=2),ZF,290),prism_xy(cband.buffer(0.5,join_style=2),ZF,290))
def chamfer_prism(poly,z0,z1,c):
    r=chamfer_solid(poly,z0,z1,c,'z')
    return r[0] if r[0] is not None else chamfer_top_steps(prism_xy(poly,z0,z1),'z',z1,c,n=30)
gV=chamfer_prism(gpoly,ZF+0.2,284.0,1.0)
gC=chamfer_prism(cband,ZF+0.2,284.0,1.0)
SG=[(202.0,72.0),(234.0,72.0)]
gV=holes_z(gV,SG,3.4,ZS1-1,290)
SCB=[(-60.0,72.0),(60.0,72.0)]; S21=[(-90.0,72.0),(90.0,72.0)]
gC=holes_z(gC,SCB,3.4,ZS1-1,290)
SR=[(150.0,48.0),(228.0,48.0),(150.0,10.0),(228.0,10.0)]        # escondidos sob a moldura verde do LED
pR=holes_z(pR,SR,6.2,279.3,290); pR=holes_z(pR,SR+SG+[(146.0,72.0),(248.0,52.0),(248.0,10.5)],3.4,ZS1-1,290)
p21=I(M['10_chassis_2_1'],B(-200,200,0,90,ZS1,290)); p21=D(p21,prism_xy(cband.buffer(0.5,join_style=2),ZF,290)); p21=holes_z(p21,S21+SCB,3.4,ZS1-1,290); p21=holes_z(p21,S21,6.2,279.3,290)
p22=I(M['10_chassis_2_2'],B(-200,200,0,90,ZS1,290)); S22=[(-100.0,11.5),(100.0,11.5)]; p22=holes_z(p22,S22,3.4,ZS1-1,290); p22=holes_z(p22,S22,6.2,279.3,290)   # sob a regua verde (cabeca embutida)
# pilotos nas estruturas
allS=SR+SG+[(146.0,72.0),(248.0,52.0),(248.0,10.5)]+S21+S22+SCB
def pil(m):
    return holes_z(m,[(x,y) for x,y in allS],2.5,ZS0-1,ZS1+1)
eD=pil(eD); eCs=pil(eCs); eCi=pil(eCi); eCsL=pil(eCsL); eCiL=pil(eCiL)
sol=M['SV-30-03c soleira (degrau) (2 de 2)']   # rente a base da impressora (sem aba e sem a parte alta)
sol=holes_z(sol,[p for p in SG if p[0]<225],2.5,262,276)
# chanfros 45 x 1,25 em todas as arestas de cima das pretas (inclusive onde encontram as verdes)
pR=chamfer_top(pR,'z',284.0,1.25); p21=chamfer_top(p21,'z',284.0,1.25); p22=chamfer_top(p22,'z',281.0,1.0)
R.update({'verde_central':gC,'est_D':eD,'est_Cs':eCs,'est_Ci':eCi,'est_CsL':eCsL,'est_CiL':eCiL,'placa_roxa':pR,'placa_21':p21,'placa_22':p22,'verde_topo':gV,'soleira':sol})
# ---- lateral: placa = camada externa da laranja atual (mesmo desenho) ----
XP=278.8
pL=I(M['21_lateral_chassis_2_D'],B(XP,290,0,100,-30,290))
LS=[(86.0,20.0),(86.0,255.0),(30.0,20.0),(30.0,255.0)]
for k in ('22_lateral_placa_3_1_D','22_lateral_faixa_3_1_D'): pL=D(pL,grow(M[k],0.5))
for y,z in LS: pL=D(pL,CYL([XP-1,y,z],[290,y,z],3.4))
pL=chamfer_top(pL,'x',281.8,1.25)
R['placa_lateral']=pL; R['est_lateral']=Q['lateral_estrutura_D']
# ---- ferragens ----
def bolt(p,axis,L,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*L,d))
HW=[bolt([x,y,284.0],[0,0,1],12) for x,y in SG+SCB]+[bolt([x,y,284.0],[0,0,1],8) for x,y in [(146.0,72.0),(248.0,52.0),(248.0,10.5)]]+[bolt([x,y,279.35],[0,0,1],6) for x,y in S21]
HW+=[bolt([x,y,279.35],[0,0,1],7) for x,y in SR]+[bolt([x,y,279.35],[0,0,1],6) for x,y in S22]
HW+=[bolt([281.8,y,z],[1,0,0],10) for y,z in LS]+[bolt([XP,18.0,220.0],[1,0,0],16)]
R['ferragens']=U(*HW)
LOG['wt']={k:bool(v.is_watertight) for k,v in R.items()}
LOG['n_apoios']={z:len(keys_sel(z)) for z in range(4)}; LOG['n_total']=len(_ALL)
mol=M['Moldura_LED_D_mod'].copy(); mol.apply_translation([0,0,-1.0]); R['moldura_led']=mol      # topo em Z 284
reg=M['Regua_baixo_central_mod'].copy(); reg.apply_translation([0,0,-0.1]); R['regua']=reg           # topo em Z 284
pickle.dump(R,open('R4.pkl','wb')); print(json.dumps(LOG))
