import numpy as np, trimesh, pickle, json
exec(open('load.py').read()); exec(open('latload.py').read()); exec(open('geo.py').read())
from shapely.geometry import Polygon, box
from shapely.ops import unary_union as uu
from shapely import affinity as _af
_G={}; exec(open('esb/geom_lat.py').read(),_G)
RL=pickle.load(open('RL.pkl','rb')); R=pickle.load(open('R4.pkl','rb'))
CF={}; LOG={}
def sec_y(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float))
    return uu([p for p in p2.polygons_full])
def prism_xz(poly,y0,y1):
    m=trimesh.creation.extrude_polygon(poly,y1-y0)
    m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
_pzy=prism_zy
def pzy(poly,x0,x1):
    poly=poly.buffer(0); gs=[g for g in (poly.geoms if hasattr(poly,'geoms') else [poly]) if g.area>0.3]
    ms=[_pzy(g,x0,x1) for g in gs]; return ms[0] if len(ms)==1 else U(*ms)
# 1) cantoneira da frente real (54), na posicao certa (a ocorrencia esta deslocada no Fusion), com a perna em L integrada
c54=L['54_cantoneira_base_D'].copy(); c54.apply_translation([3.159,5.023,6.726])
XP1,XC=281.8,293.3
p=_G['Lr'].intersection(box(190.0,2.0,275.0,120.0))
leg=pzy(p,XP1,XC); leg=chamfer_top(leg,'x',XC,5.5); leg=I(leg,B(XP1-1,XC+1,0,88.0,-268.0,268.0))
t=_G['rc'](Polygon([(229-7,17-4.06),(229+7,17-4.06),(229,17+8.12)]),1.0)
leg=D(leg,pzy(t,XC-1.5,XC+1))
CF['cantoneira_F_L']=U(c54,leg)
# 2) espinha: perna lateral desce ate Y 81 (topo novo da lateral); assentos planos sob a cantoneira
sp=M['SV08_Espinha_L_FD_Black']
pp=sec_y(sp,94.0).intersection(box(272.9,-400,400,400))
pp=pp.difference(box(281.6,247.5,400,400))                     # sob a aba da cantoneira: face plana X 281,6
pp=pp.difference(box(279.6,224.8,400,247.7))                    # atras da verde, que agora desce ate Y 81
ext=[prism_xz(g,81.0,94.01) for g in (pp.geoms if hasattr(pp,'geoms') else [pp]) if g.area>0.5]
sp2=U(sp,*ext)
sp2=D(sp2,B(237.3,300,80,98.9,283.95,300))                    # ponta da aba da frente: faces planas X 237,3 / Z 283,95
CF['espinha']=sp2
# 3) verdes da coluna na posicao (a 72 esta deslocada no Fusion)
v72=M['72_verde_inferior_D_encaixe'].copy(); v72.apply_translation([-95.73,-87.79,35.19])
v72=D(v72,I(grow(c54,0.2),B(270,300,80,100,240,300)))          # aba da cantoneira abraca a verde (acompanha as faces planas da aba)
gp=sec_y(v72,95.0).intersection(box(270.0,224.0,290.0,247.5))  # verde desce ate Y 81,2 no lado da lateral (mesmo comprimento da espinha)
v72=U(v72,*[prism_xz(g,81.2,95.01) for g in (gp.geoms if hasattr(gp,'geoms') else [gp]) if g.area>0.5])
CF['verde_72']=v72
vs=M['SV08_Verde_Superior_FD_Green']                       # E03: quina de dentro chanfrada igual a da 72 (X+Z >= 556, folga 0,2 da espinha)
vs=D(vs,I(B(265,279.79,320,560,265,281.99),HS([278.0,300,278.0],(1,0,1))))
CF['verde_sup']=vs; CF['capa_74']=M['74_capa_central_D_interior_continuo']
# 4) ferragens (E05): tampa em Y 126/236/384/494 (lado e frente) e M3x8 DIN912 embutidos em Y110/126
def bolt(p,axis,Lg,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*Lg,d))
HW=[bolt([283.8,y,256.2],[1,0,0],8) for y in (126,236,384,494)]+[bolt([261.25,y,286.0],[0,0,1],8) for y in (126,236,384,494)]
HW+=[bolt([276.4,y,244.0],[1,0,0],8,hd=5.5,hh=3.0) for y in (110,126)]
CF['ferragens']=U(*HW)
# interferencias
chk={}
pares=[('espinha','cantoneira_F_L'),('verde_72','cantoneira_F_L'),('verde_72','espinha'),('verde_sup','espinha'),('verde_sup','verde_72'),('capa_74','espinha')]
for a,b in pares: chk[a+' x '+b]=round(I(CF[a],CF[b]).volume,2)
for a in ('espinha','verde_72','cantoneira_F_L'):
    for k in ('placa_A','placa_B','est_frente','moldura_lat_c','acrilico_lat'): chk[a+' x '+k]=round(I(CF[a],RL[k]).volume,2)
    for k in ('placa_roxa','verde_topo','moldura_led','est_D'): chk[a+' x '+k]=round(I(CF[a],R[k]).volume,2)
    chk[a+' x P01']=round(I(CF[a],M['65_suporte_P01_D']).volume,2)
LOG['interf']={k:v for k,v in chk.items() if abs(v)>0.01}; LOG['n_pares']=len(chk)
LOG['bb']={k:np.round(v.bounds,1).tolist() for k,v in CF.items()}
pickle.dump(CF,open('CF.pkl','wb')); print(json.dumps(LOG,indent=0))
print('CH_FAIL',CH_FAIL)
