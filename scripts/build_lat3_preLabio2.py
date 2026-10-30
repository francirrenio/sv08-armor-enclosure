import numpy as np, trimesh, json, pickle, time
exec(open('latload.py').read()); exec(open('geo.py').read()); exec(open('geo_ch2.py').read())
from shapely.geometry import box as sbox, box, Polygon, Point
from shapely.ops import unary_union as uu
t0=time.time(); RL={}; LOG={}
_pzy=prism_zy
def prism_zy(poly,x0,x1):
    poly=poly.buffer(0).simplify(0.02)
    gs=[g for g in (poly.geoms if hasattr(poly,'geoms') else [poly]) if g.area>0.3]
    ms=[_pzy(g,x0,x1) for g in gs]
    ms=[m for m in ms if m.is_volume] or ms
    return ms[0] if len(ms)==1 else U(*ms)
YT=81.0                     # topo da lateral = topo da base da frente
XS0,XS1=273.0,276.8         # pele da estrutura escondida (face X 276,8 plana -> mesa)
XF=268.7                    # costas do quadro (base da impressora em X 268,5)
XP0,XP1=276.8,283.8         # placa preta: face de fora no plano da coluna e do painel (X 283,8)
XFL=280.6                   # fundo dos rebaixos das verdes (verdes X 280,8-283,8)
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
# EMENDA_NO_VINCO: as 2 placas emendam reto em Z 0, no fundo do vinco do meio (os vincos Z -6/0/+6 da moldura descem pela placa)
regA=sbox(-400,0,-0.1,90); regB=sbox(0.1,0,400,90)
# BASE_Y0: tudo desce ate o fundo da base (Y 0); CANTO_CABOS: a lateral para em |Z| 261 (vao para os cabos sob a cantoneira)
YB0=0.0; ZCAB=261.0
_fb=outline.intersection(sbox(-400,2.0,400,2.6)).bounds
outline=uu([outline,sbox(_fb[0],YB0,_fb[2],2.6)]).intersection(sbox(-ZCAB,YB0,ZCAB,YT))
PLATES['A']=outline.intersection(regA); PLATES['B']=outline.intersection(regB)
LOG['sobreposicao_AB']=round(PLATES['A'].intersection(PLATES['B']).area,2)
cant=grow(L['37_cantoneira_traseira_D'],0.2)
_G={}; exec(open('esb/geom_lat.py').read(),_G)
from shapely import affinity as _af
_V={}; exec(open('esb/geom_lat_v2.py').read(),_V)        # FAIXA_V2: asas com bolsao, vao de 4 mm
NG=_V['NG']
nfoot=uu(list(NG.values()))
POC=nfoot.buffer(0.5,join_style=2)          # linha de sombra 0,5 em volta das verdes novas
# parafusos
GS=[(y,z) for z,y in _V['SC']]                                                     # parafusos aparentes das verdes (simetricos)
HID=_V['HID']                                                                    # escondidos sob as verdes (simetricos)                                                                  # escondidos sob as verdes (simetricos)
AP=[(52.0,-254.0),(52.0,254.0)]                                                                 # M3 lateral_apoio (existentes, aparentes)
CT=[(24.5,-256.0),(71.5,-256.0),(24.5,256.0),(71.5,256.0)]                                      # parafusos das cantoneiras
BF=[(18.0,-220.0),(18.0,220.0)]                                                                 # furo da lateral da base
REC=uu([Polygon(g.exterior.coords,[r.coords for r in g.interiors]).buffer(0.5,join_style=1,quad_segs=32) for g in NG.values()])   # encaixe: folga 0,5
_cl=REC.buffer(6.0,join_style=1,quad_segs=32).buffer(-6.0,join_style=1,quad_segs=32)   # fecha tambem o centro dos encontros em T (sem ilha)
RIB=_cl.difference(REC).buffer(-0.15,join_style=1).buffer(0.15,join_style=1)   # nervura = vaos estreitos entre as verdes (fecha so o que tem < 5,2)
RIB=uu([g for g in (RIB.geoms if hasattr(RIB,'geoms') else [RIB]) if g.area>5])
XR=XP1-0.5; XI=XP1-1.5; XG=XI-2.0                              # topo da nervura, topo da ilha do bolsao, fundo da grade
def _perto(pg,tol=0.08):
    bd=pg.boundary
    def f(a,b): return bd.distance(Point(0.5*(a[0]+b[0]),0.5*(a[1]+b[1])))<tol
    return f
_nrec=_perto(REC); _nrib=_perto(RIB)
for nm,poly in PLATES.items():
    m=prism_zy(poly,XP0,XP1)
    m=chamfer_top(m,'x',XP1,1.25)                               # borda de fora da placa (como antes)
    m=D(m,prism_zy(REC.intersection(poly.buffer(2)),XFL,XP1+5))
    m=D(m,prism_zy(_G['oval'],XP0-1,XP1+1))
    # VERDES_SALTADAS: o preto fica todo num nivel so (face X 283,8, inclusive entre as verdes) e as verdes ficam 0,5 acima;
    # friso de 0,6 na boca do encaixe em volta de todas as verdes
    c1=chamfer_cutter(poly.buffer(6).difference(REC),'x',XP1,0.6)
    if c1 is not None: m=D(m,c1)
    for il,gr in zip(_V['ILHAS'],_V['GRADES']):                  # bolsao: ilha preta 1,5 abaixo da face, grade com rasgos de 2 mm
        if not poly.buffer(-1).intersects(il): continue
        m=D(m,prism_zy(il,XI,XP1+5),chamfer_cutter(il,'x',XI,0.6),prism_zy(gr,XG,XP1+5))
    def mine(pts): return [p for p in pts if poly.buffer(-1).contains(Point(p[1],p[0]))]
    m=holes_x(m,mine(GS),3.4,XP0-1,XP1+1)
    m=holes_x(m,mine(HID),3.4,XP0-1,XP1+1); m=holes_x(m,mine(HID),6.2,XP0+0.3,XP1+1)
    m=holes_x(m,mine(AP),3.4,XP0-1,XP1+1); m=holes_x(m,mine(AP),6.2,280.0,XP1+1)
    m=holes_x(m,mine(CT),2.5,XP0-1,XP1+1)
    for zv in (-6.0,0.0,6.0):                                    # vincos: V de 3,2 x 1,0 (os mesmos da moldura), placa inteira de alto a baixo
        vv=trimesh.creation.extrude_polygon(Polygon([(zv-1.6,XP1+0.6),(zv+1.6,XP1+0.6),(zv,XP1-1.0)]),YT+10)
        vv.apply_transform(np.array([[0,1,0,0],[0,0,1,-5.0],[1,0,0,0],[0,0,0,1]],float))
        if vv.volume<0: vv.invert()
        m=D(m,vv)
    # ENCAIXE_EMENDA: 2 rabos de andorinha escondidos sob a verde central (abaixo do fundo do encaixe dela), da placa B entrando na A
    for yc in (14.5,59.5):
        cauda=Polygon([(0.5,yc-3.0),(0.5,yc+3.0),(-5.0,yc+4.5),(-5.0,yc-4.5)])
        if nm=='B': m=U(m,prism_zy(cauda,XP0,XFL))
        else:       m=D(m,prism_zy(cauda.buffer(0.2,join_style=2),XP0-1,XFL+0.01))
    m=max(m.split(only_watertight=False),key=lambda q:q.volume)
    RL['placa_'+nm]=m; LOG['placa_'+nm]={'bb':np.round(m.bounds,1).tolist(),'wt':bool(m.is_watertight),'vol':bool(m.is_volume),'hid':len(mine(HID))}
# ---------- estrutura escondida ----------
ZA,ZB=-ZCAB,ZCAB
pele=sbox(ZA,YB0,ZB,YT).difference(oval)
fr=[sbox(-229,YB0,229,6),sbox(-229,YT-4,229,YT),sbox(-229,YB0,-225,YT),sbox(225,YB0,229,YT),
    oval.buffer(3).difference(oval)]
for z in (-140.0,140.0): fr+= [sbox(z-3.1,YB0,z-0.1,YT),sbox(z+0.1,YB0,z+3.1,YT)]
fr=uu(fr).difference(oval)
BOSS=GS+HID+BF
bosses=uu([Point(z,y).buffer(4.5,16) for y,z in BOSS if abs(z)<229])
st=U(prism_zy(pele,XS0,XS1),prism_zy(fr.intersection(sbox(ZA,YB0,ZB,YT)),XF,XS0+0.05),prism_zy(bosses.intersection(sbox(ZA,YB0,ZB,YT)),XF,XS0+0.05))
# apoios finos nos bolsos da lateral da base (mesma regra da frente: so as tiras estreitas)
G=pickle.load(open('latG.pkl','rb'))
KEEPL={4,6,8,10,15,17,22,24,27,31,35,37,39,41}
exec(open('keys_retas.py').read().split("if __name__")[0])     # CHAVES_RETAS: tiras retas, pontas cortadas 4 mm
_KS,_KL=chaves(G,KEEPL); LOG['chaves']=_KL
keys=[prism_zy(g,258.8,XS0+0.2) for g in _KS]
st=U(st,*keys); LOG['apoios_lateral']=sorted(KEEPL)
# tunel liso da abertura menor ate a borda da base (X 265,3): as bordas e os dentes do apoio de mao ficam cobertos
OV=_G['oval']
tun=prism_zy(OV.buffer(2.5,join_style=1,resolution=16).difference(OV),265.3,XS0+0.05)
st=U(st,D(tun,grow(L['Corpo1@067.stl'],0.1)))
# OVAL_UNIFICADO: o vao entre o furo grande da pele (oval antigo) e o tunel do oval menor fica fechado (X 268,7-276,8):
# o tunel deixa de ser uma peca solta e vira parte da estrutura
_fech=Polygon(oval.exterior).difference(OV)
st=U(st,D(prism_zy(_fech,XF,XS1),grow(L['Corpo1@067.stl'],0.1)))
# aba interna: fecha o vao entre a estrutura e a base (canal X 265-268,5 e degrau do piso Y 73); topo no maximo 2 mm acima do piso
YP=73.0
aba=D(B(263.0,XF+0.05,YP,YP+2.0,-229.0,229.0),grow(L['Corpo1@067.stl'],0.1))
parede=B(XF,270.6,YP,YT,-229.0,229.0)
st=U(st,aba,parede); LOG['aba']={'bb':np.round(aba.bounds,2).tolist(),'vol':round(aba.volume,1)}
# furos
GSb=[p for p in GS if p[0]<66]; GSt=[p for p in GS if p[0]>=66]
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
st=I(st,B(200,300,-5,100,ZA,ZB))                 # CANTO_CABOS: nada passa de |Z| 261
# divide em 3 (emendas Z -145 e +145, rabo de andorinha escondido na pele)
def tongue(zs,yc,s):   # s=+1: lingueta da peca de Z>zs entrando em Z<zs
    return Polygon([(zs+0.2*s,yc-3),(zs+0.2*s,yc+3),(zs-4.5*s,yc+4.5),(zs-4.5*s,yc-4.5)])
TT=[tongue(-140.0,y,-1) for y in (12.0,72.0)]+[tongue(140.0,y,1) for y in (12.0,72.0)]
eT=I(st,B(XF-20,XS1+1,0,90,ZA-1,-140.1)); eM=I(st,B(XF-20,XS1+1,0,90,-139.9,139.9)); eF=I(st,B(XF-20,XS1+1,0,90,140.1,ZB+1))
eT=U(eT,*[prism_zy(t,XS0,XS1) for t in TT[:2]]); eF=U(eF,*[prism_zy(t,XS0,XS1) for t in TT[2:]])
eM=D(eM,*[prism_zy(t.buffer(0.2,join_style=2),XS0-0.5,XS1+0.5) for t in TT])
# LABIO_ACRILICO: a estrutura do meio sobe 5 mm por dentro do acrilico (apoio e vedacao da borda de baixo), folga 0,2 ate a face de dentro (X 277,5)
_lab=Polygon([(XF,YT-0.05),(XS1,YT-0.05),(XS1,YT),(277.3,YT),(277.3,YT+4.4),(276.7,YT+5.0),(XF+1.0,YT+5.0),(XF,YT+4.0)])
eM=U(eM,prism_xy(_lab,-139.9,139.9))
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
_c37=L['37_cantoneira_traseira_D'].copy(); _c37.apply_translation([2.2,0,0]); cant=grow(_c37,0.2)
def stretch(m,ycut,dy):
    c=m.copy(); v=c.vertices.copy(); v[v[:,1]<ycut,1]+=dy; c.vertices=v; return c
# painel lateral desce 12 mm (montantes e acrilico 12 mm mais longos); assenta no topo da lateral em Y 81
RL['moldura_lat_c']=stretch(L['SV-40-01c inf +u'],120,-12.0)
RL['moldura_lat_d']=stretch(L['SV-40-01d inf -u'],120,-12.0)
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
T60=np.tan(np.radians(60))
for k,poly in NG.items():   # verdes: prisma do contorno (com janela/bolsao), chanfro de 1,0 por fora e por dentro, furos M3
    m=D(prism_zy(poly,XFL+0.2,XP1+0.5),chamfer_cutter(poly,'x',XP1+0.5,1.0))     # verde 0,5 acima da face preta
    m=holes_x(m,[p for p in GS if poly.contains(Point(p[1],p[0]))],3.4,XFL,XP1+1)
    RL[k]=max(m.split(only_watertight=False),key=lambda q:q.volume)
    for a in ('placa_A','placa_B'): chk[k+'x'+a]=round(I(RL[k],RL[a]).volume,2)
# cantoneira em L como peca unica: a aba lateral da cantoneira (X 281,8-293,3) desce e entra na lateral com a mesma face e o mesmo chanfro da ponta (5,5 x 45)
XC=295.5          # cantoneiras ficam por cima das faces alinhadas (afastadas 2,2 mm para fora)
def perna(s_):
    p=_G['Lr'].intersection(box(190.0,2.0,275.0,120.0))
    if s_<0: p=_af.scale(p,-1,1,origin=(0,0))
    m=prism_zy(p,XP1,XC); m=chamfer_top(m,'x',XC,5.5); m=I(m,B(XP1-1,XC+1,0,88.0,-268.0,268.0))
    zc=229.0*s_; t=_G['rc'](Polygon([(zc-7,17-4.06),(zc+7,17-4.06),(zc,17+8.12)]),1.0)
    return D(m,prism_zy(t,XC-1.5,XC+1))
c37=L['37_cantoneira_traseira_D'].copy(); c37.apply_translation([2.2,0,0])
cF=c37.copy(); cF.apply_transform(np.diag([1,1,-1,1]));
if cF.volume<0: cF.invert()
exec(open('cap.py').read())
_lp=_G['Lr'].intersection(box(190.0,YB0,270.0,60.0)); _lpT=_af.scale(_lp,1,1,origin=(0,0)); _lpT=Polygon([(-z,y) for z,y in _lp.exterior.coords])
RL['cantoneira_T_L']=make_cap(c37,-1,xin=284.0,zin=-284.0,ybot=YB0,leg_poly=_lpT,xleg=283.8,holes=[(24.5,-256.0),(71.5,-256.0)],bevel=561.936)
RL['cantoneira_F_L']=RL['cantoneira_T_L']
for k in ('cantoneira_T_L','cantoneira_F_L'):
    for a in ('placa_A','placa_B'): chk[k+'x'+a]=round(I(RL[k],RL[a]).volume,2)
LOG['interf']=chk
# ---------- ferragens novas ----------
def bolt(p,axis,Lg,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*Lg,d))
HW=[bolt([XP0+0.35,y,z],[1,0,0],6) for y,z in HID]+[bolt([XP1+0.5,y,z],[1,0,0],10) for y,z in GS]+[bolt([XS1-1.85,y,z],[1,0,0],16) for y,z in BF]
RL['ferragens']=U(*HW)
pickle.dump(RL,open('RL.pkl','wb')); LOG['t']=round(time.time()-t0)
print(json.dumps(LOG,indent=0))
print('CH_FAIL',CH_FAIL)
