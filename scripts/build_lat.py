import numpy as np, trimesh, json, pickle, time
exec(open('latload.py').read()); exec(open('geo.py').read())
from shapely.geometry import box as sbox, Polygon, Point
from shapely.ops import unary_union as uu
t0=time.time(); RL={}; LOG={}
_pzy=prism_zy
def prism_zy(poly,x0,x1):
    gs=[g for g in (poly.geoms if hasattr(poly,'geoms') else [poly]) if g.area>0.01]
    ms=[_pzy(g,x0,x1) for g in gs]
    return ms[0] if len(ms)==1 else trimesh.util.concatenate(ms)
YT=81.0                     # topo da lateral = topo da base da frente
XS0,XS1=273.0,276.8         # pele da estrutura escondida (face X 276,8 plana -> mesa)
XF=268.7                    # costas do quadro (base da impressora em X 268,5)
XP0,XP1=276.8,281.8         # placa preta (mesmo desenho da laranja), 5 mm
XFL=278.6                   # fundo dos rebaixos das verdes (verdes atuais X 278,8-281,8)
def filled(p): return uu([Polygon(g.exterior) for g in (p.geoms if hasattr(p,'geoms') else [p])])
def holes_x(m,pts,d,x0,x1):
    for y,z in pts: m=D(m,CYL([x0,y,z],[x1,y,z],d))
    return m
def sec_y(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    if s is None: return None
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float))
    return uu([p for p in p2.polygons_full])
def prism_xz(poly,y0,y1):
    m=trimesh.creation.extrude_polygon(poly,y1-y0)
    m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
GR=['22_lateral_placa_1_1_D','22_lateral_placa_2_1_D','22_lateral_placa_3_1_D','22_lateral_faixa_1_1_D','22_lateral_faixa_2_1_D','22_lateral_faixa_3_1_D']
gsec={k:section_polys(L[k],'x',280.3) for k in GR}
gfoot=uu([filled(p) for p in gsec.values()])
oval=max([Polygon(h) for h in gsec['22_lateral_placa_2_1_D'].interiors],key=lambda p:p.area)        # janela oval da verde central
LOG['oval']=[round(v,1) for v in oval.bounds]
clipY=sbox(-400,0,400,YT)
# ---------- placas pretas: contorno de fora da laranja (2 pecas, emenda em degrau ja existente) ----------
PLATES={}
sA=section_polys(L['21_lateral_chassis_1_D'],'x',280.3); sB=section_polys(L['21_lateral_chassis_2_D'],'x',280.3)
outline=filled(uu([sA,sB,gfoot.buffer(0.6)]).buffer(0.3).buffer(-0.3)).intersection(clipY)
regA=uu([sbox(-400,0,-12.05,62.0),sbox(-400,62.0,11.85,90)])           # emenda em degrau da laranja atual (Z -12 embaixo, Z +12 em cima)
regB=uu([sbox(-11.95,0,400,62.0),sbox(11.95,62.0,400,90)])
PLATES['A']=outline.intersection(regA); PLATES['B']=outline.intersection(regB)
LOG['sobreposicao_AB']=round(PLATES['A'].intersection(PLATES['B']).area,2)
cant=grow(L['37_cantoneira_traseira_D'],0.2)
POC=gfoot.buffer(0.5,join_style=2)          # linha de sombra 0,5 em volta das verdes
# parafusos
GS=[(20,-224),(47,-224),(20,-116),(47,-116),(35,-74),(35,74),(20,224),(47,224),(20,116),(47,116),
    (72,-178.025),(72,-126.025),(72,-26.0),(72,26.0),(72,129.875),(72,181.875)]               # das verdes (existentes)
HID=[(33.0,-200.0),(33.0,-150.0),(70.5,-210.0),(70.5,-100.0),(11.5,-40.0)]
HID=HID+[(y,-z) for y,z in HID]                                                                  # escondidos sob as verdes (simetricos)
AP=[(52.0,-254.0),(52.0,254.0)]                                                                 # M3 lateral_apoio (existentes, aparentes)
CT=[(24.5,-259.7),(71.5,-259.7),(24.5,259.7),(71.5,259.7)]                                      # parafusos das cantoneiras
BF=[(18.0,-220.0),(18.0,220.0)]                                                                 # furo da lateral da base
for nm,poly in PLATES.items():
    m=prism_zy(poly,XP0,XP1)
    m=D(m,prism_zy(POC.intersection(poly.buffer(2)),XFL,XP1+5))
    m=D(m,prism_zy(oval,XP0-1,XP1+1))
    def mine(pts): return [p for p in pts if poly.buffer(-1).contains(Point(p[1],p[0]))]
    m=holes_x(m,mine(GS),3.4,XP0-1,XP1+1)
    m=holes_x(m,mine(HID),3.4,XP0-1,XP1+1); m=holes_x(m,mine(HID),6.2,XP0+0.3,XP1+1)
    m=holes_x(m,mine(AP),3.4,XP0-1,XP1+1); m=holes_x(m,mine(AP),6.2,278.0,XP1+1)
    m=holes_x(m,mine(CT),2.5,XP0-1,XP1+1)
    m=D(m,cant)
    m=chamfer_top(m,'x',XP1,1.25)
    RL['placa_'+nm]=m; LOG['placa_'+nm]={'bb':np.round(m.bounds,1).tolist(),'wt':bool(m.is_watertight),'hid':len(mine(HID))}
# ---------- estrutura escondida ----------
ZA,ZB=-273.5,273.4
pele=sbox(ZA,2.0,ZB,YT).difference(oval)
fr=[sbox(-229,2,229,6),sbox(-229,YT-4,229,YT),sbox(-229,2,-225,YT),sbox(225,2,229,YT),
    oval.buffer(3).difference(oval)]
for z in (-145.0,145.0): fr+= [sbox(z-3.1,2,z-0.1,YT),sbox(z+0.1,2,z+3.1,YT)]
fr=uu(fr).difference(oval)
BOSS=GS+HID+BF
bosses=uu([Point(z,y).buffer(4.5,16) for y,z in BOSS if abs(z)<229])
st=U(prism_zy(pele,XS0,XS1),prism_zy(fr.intersection(sbox(ZA,2,ZB,YT)),XF,XS0+0.05),prism_zy(bosses.intersection(sbox(ZA,2,ZB,YT)),XF,XS0+0.05))
# apoios finos nos bolsos da lateral da base (mesma regra da frente: so as tiras estreitas)
G=pickle.load(open('latG.pkl','rb'))
KEEPL={4,6,8,10,15,17,22,24,27,31,35,37,39,41}
keys=[prism_zy(g,258.8,XS0+0.2) for i,g in enumerate(G,1) if i in KEEPL]
st=U(st,*keys); LOG['apoios_lateral']=sorted(KEEPL)
# aba interna: fecha o vao entre a estrutura e a base (canal X 265-268,5 e degrau do piso Y 73); topo no maximo 2 mm acima do piso
YP=73.0
aba=D(B(263.0,XF+0.05,YP,YP+2.0,-229.0,229.0),grow(L['Corpo1@067.stl'],0.1))
parede=B(XF,270.6,YP,YT,-229.0,229.0)
st=U(st,aba,parede); LOG['aba']={'bb':np.round(aba.bounds,2).tolist(),'vol':round(aba.volume,1)}
# furos
GSb=[p for p in GS if p[0]<60]; GSt=[p for p in GS if p[0]>60]
st=holes_x(st,GSb,3.4,XF-1,XS1+1); st=holes_x(st,GSt,3.4,269.5,XS1+1)
for y,z in GSb:                                   # porca M3 presa por tras
    hx=trimesh.creation.cylinder(radius=6.1/np.sqrt(3),height=7.4,sections=6)
    hx.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0])); hx.apply_translation([XF-1+3.7,y,z]); st=D(st,hx)
for y,z in GSt:                                   # faixas: porca entra por baixo (a parede de tras fica fechada)
    hx=trimesh.creation.cylinder(radius=6.1/np.sqrt(3),height=2.6,sections=6)
    hx.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0])); hx.apply_translation([271.9,y,z])
    st=D(st,hx,B(270.6,273.2,y-8.0,y,z-2.8,z+2.8))
st=holes_x(st,HID,2.5,XF-1,XS1+1)
st=holes_x(st,AP,3.4,XF-1,XS1+1)
st=holes_x(st,CT,2.5,XF-1,XS1+1)
st=holes_x(st,BF,3.4,XF-1,XS1+1); st=holes_x(st,BF,6.2,XS1-1.9,XS1+1)
# divide em 3 (emendas Z -145 e +145, rabo de andorinha escondido na pele)
def tongue(zs,yc,s):   # s=+1: lingueta da peca de Z>zs entrando em Z<zs
    return Polygon([(zs+0.2*s,yc-3),(zs+0.2*s,yc+3),(zs-4.5*s,yc+4.5),(zs-4.5*s,yc-4.5)])
TT=[tongue(-145.0,y,-1) for y in (12.0,72.0)]+[tongue(145.0,y,1) for y in (12.0,72.0)]
eT=I(st,B(XF-20,XS1+1,0,90,ZA-1,-145.1)); eM=I(st,B(XF-20,XS1+1,0,90,-144.9,144.9)); eF=I(st,B(XF-20,XS1+1,0,90,145.1,ZB+1))
eT=U(eT,*[prism_zy(t,XS0,XS1) for t in TT[:2]]); eF=U(eF,*[prism_zy(t,XS0,XS1) for t in TT[2:]])
eM=D(eM,*[prism_zy(t.buffer(0.2,join_style=2),XS0-0.5,XS1+0.5) for t in TT])
RL['est_tras']=eT; RL['est_meio']=eM; RL['est_frente']=eF
for k in ('est_tras','est_meio','est_frente'):
    b=RL[k].bounds; LOG[k]={'compr':round(b[1][2]-b[0][2],1),'wt':bool(RL[k].is_watertight)}
# ---------- o que fica acima (Y 81-93) desce ate o topo novo ----------
def desce(m,yref,ylo,xmin=None,cut=None):
    p=sec_y(m,yref)
    if xmin is not None: p=p.intersection(sbox(xmin,-400,400,400))
    gs=[g for g in (p.geoms if hasattr(p,'geoms') else [p]) if g.area>0.5]
    ext=[prism_xz(g,ylo,yref+0.01) for g in gs]
    if cut is not None: ext=[D(e,cut) for e in ext]
    try: return U(m,*ext)
    except Exception as e:
        LOG.setdefault('desce_concat',[]).append(str(e)[:40]); return trimesh.util.concatenate([m]+ext)
cant=grow(L['37_cantoneira_traseira_D'],0.2)
def stretch(m,ycut,dy):
    c=m.copy(); v=c.vertices.copy(); v[v[:,1]<ycut,1]+=dy; c.vertices=v; return c
# painel lateral desce 12 mm (montantes e acrilico 12 mm mais longos); assenta no topo da lateral em Y 81
RL['moldura_lat_c']=stretch(L['SV-40-01c inf +u'],200,-12.0)
RL['moldura_lat_d']=stretch(L['SV-40-01d inf -u'],200,-12.0)
RL['acrilico_lat']=stretch(L['SV-40-01e acrilico 3mm 420x411'],300,-12.0)
RL['coluna_TD_ext']=desce(L['58_coluna_inferior_lateral_traseiro_D_externa'],95.0,YT,cut=cant)
RL['espinha']=desce(L['SV08_Espinha_L_FD_Black'],94.0,YT,xmin=272.9)
# interferencias
chk={}
for a in ('placa_A','placa_B'):
    for b in ('est_tras','est_meio','est_frente'): chk[a+'x'+b]=round(I(RL[a],RL[b]).volume,2)
for a in ('est_tras','est_meio','est_frente'):
    chk[a+'xbase']=round(I(RL[a],L['Corpo1@067.stl'] if 'Corpo1@067.stl' in L else L['Corpo1']).volume,2)
    for s in ('65_suporte_P01_D','20_apoio_traseiro_D'): chk[a+'x'+s[:6]]=round(I(RL[a],L[s]).volume,2)
for g in GR:
    for a in ('placa_A','placa_B'): chk[g[13:]+'x'+a]=round(I(L[g],RL[a]).volume,2)
LOG['interf']=chk
# ---------- ferragens novas ----------
def bolt(p,axis,Lg,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*Lg,d))
HW=[bolt([XP0+0.35,y,z],[1,0,0],6) for y,z in HID]+[bolt([XS1-1.85,y,z],[1,0,0],16) for y,z in BF]
RL['ferragens']=U(*HW)
pickle.dump(RL,open('RL.pkl','wb')); LOG['t']=round(time.time()-t0)
print(json.dumps(LOG,indent=0))
