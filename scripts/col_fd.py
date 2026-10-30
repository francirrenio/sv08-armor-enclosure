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
c54=L['54_cantoneira_base_D'].copy(); c54.apply_translation([3.159+2.2,5.023,6.726+2.2])   # posicao certa + 2,2 para fora: fica por cima das faces alinhadas
exec(open('cap.py').read())
_lp=_G['Lr'].intersection(box(190.0,2.0,270.0,60.0))
CF['cantoneira_F_L']=make_cap(c54,+1,xin=284.0,zin=286.2,leg_poly=_lp,xleg=283.8,holes=[(24.5,259.7),(71.5,259.7)],bevel=560.627)
# 2) espinha: perna lateral desce ate Y 81 (topo novo da lateral); assentos planos sob a cantoneira
sp=M['SV08_Espinha_L_FD_Black']
pp=sec_y(sp,94.0).intersection(box(272.9,-400,400,400))
pp=pp.difference(box(279.6,224.8,400,400))                     # atras da verde, que agora desce ate Y 81 em toda a lateral
ext=[prism_xz(g,81.0,94.01) for g in (pp.geoms if hasattr(pp,'geoms') else [pp]) if g.area>0.5]
sp2=U(sp,*ext)
CF['espinha']=sp2
# 3) verdes da coluna na posicao (a 72 esta deslocada no Fusion)
v72=M['72_verde_inferior_D_encaixe'].copy(); v72.apply_translation([-95.73,-87.79,35.19])
gp=sec_y(v72,100.0)                                             # verde desce ate Y 81,2 na lateral e na frente, ate encostar na preta (cantoneira apoia nela)
gext=[prism_xz(g,81.2,100.01) for g in (gp.geoms if hasattr(gp,'geoms') else [gp]) if g.area>0.5]
v72=U(v72,*gext)
CF['espinha']=D(CF['espinha'],*[prism_xz(g.buffer(0.2,join_style=2),80.0,100.0) for g in (gp.geoms if hasattr(gp,'geoms') else [gp]) if g.area>0.5])
CF['verde_72']=v72
vs=M['SV08_Verde_Superior_FD_Green']                       # E03: quina de dentro chanfrada igual a da 72 (X+Z >= 556, folga 0,2 da espinha)
vs=D(vs,I(B(265,279.79,320,560,265,281.99),HS([278.0,300,278.0],(1,0,1))))
CF['verde_sup']=vs
# capa central: sem a saliencia que entrava no rebaixo da espinha; assenta por cima (face de dentro X 284,0 na lateral)
cp=M['74_capa_central_D_interior_continuo']
cp=D(cp,B(200,284.0,290,360,200,276.0))
CF['capa_74']=cp
# espinha: sem o rebaixo da capa (faixa lateral cheia ate X 283,8 em Y 297,8-354,2)
_band=sec_y(sp,290.0).intersection(box(280.0,215.0,290.0,240.0))
_fill=[prism_xz(g,297.0,355.0) for g in (_band.geoms if hasattr(_band,'geoms') else [_band]) if g.area>0.5]
_e=U(CF['espinha'],*_fill)
_e=D(_e,CYL([270,322.8,228.0],[290,322.8,228.0],3.4),CYL([280.6,322.8,228.0],[290,322.8,228.0],6.2))   # parafuso original: cabeca embutida na faixa
_e=D(_e,CYL([279.0,324.0,232.0],[290,324.0,232.0],2.5))                                                  # piloto do parafuso da capa
# fixacao na estrutura da impressora: 2 furos da aba do perfil (Z 228, Y 137,8 / 322,8), M3x18 cabeca cilindrica embutida
# (o de Y 507,8 saiu: em cima a espinha e presa nos 2 ressaltos do suporte de canto do top hat)
_FX={137.8:(280.6,18),322.8:(280.6,18),507.8:(276.4,16)}     # Y: (assento da cabeca, comprimento); em Y 507,8 a cabeca fica sob a verde de cima
for _y in (137.8,):
    _e=D(_e,CYL([270,_y,228.0],[290,_y,228.0],3.4),CYL([_FX[_y][0],_y,228.0],[290,_y,228.0],6.2))
CF['espinha']=_e
# TOPO_ESP: espinha sobe dentro da cantoneira do top hat ate Y 622 e se encaixa nos ressaltos do suporte de canto FD
_T='/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/'
_sup=trimesh.load(_T+'050.stl'); _cth=trimesh.load(_T+'053.stl'); _trv=trimesh.load(_T+'062.stl'); _prf=trimesh.load(_T+'058.stl'); _bm=trimesh.load(_T+'060.stl')
_top=sec_y(CF['espinha'],550.0)
_top=Polygon(max((_top.geoms if hasattr(_top,'geoms') else [_top]),key=lambda g:g.area).exterior)
_ext=prism_xz(_top,553.0,622.0)
_cl=[]
for _y in np.arange(553.0,622.0,1.0):     # a cantoneira do top hat nao e um solido fechado: folga por fatias de 1 mm
    try:
        _s=_cth.section(plane_origin=[0,_y+0.5,0],plane_normal=[0,1,0])
        _p2,_=_s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-(_y+0.5)],[0,0,0,1]],float))
        _pp=uu([q for q in _p2.polygons_full]).buffer(0.2,join_style=2)
        for _g in (_pp.geoms if hasattr(_pp,'geoms') else [_pp]):
            if _g.area>0.5: _cl.append(prism_xz(_g,_y-0.01,_y+1.01))
    except Exception: pass
_ext=D(_ext,*_cl)
_ext=D(_ext,grow(_trv,0.2),grow(_prf,0.2),grow(_bm,0.2))
_ext=D(_ext,*[CYL([266,y,259.7],[290,y,259.7],8.2) for y in (564.5,614.5)],*[CYL([246.0,y,266],[246.0,y,295],8.2) for y in (564.5,614.5)])   # furos para os ressaltos do suporte (folga 0,2)
_ext=D(_ext,grow(_sup,0.2))
CF['espinha']=U(CF['espinha'],_ext)
_CHK={'esp x sup':round(I(CF['espinha'],_sup).volume,2),'esp x cant_th(pts)':int(_cth.contains(CF['espinha'].sample(4000)).sum()) if False else 'fatias','esp x trav':round(I(CF['espinha'],_trv).volume,2),'esp x perfil':round(I(CF['espinha'],_prf).volume,2),'bb':np.round(CF['espinha'].bounds,1).tolist()}
def _bolt(p,axis,Lg,d=3.0,hd=5.5,hh=3.0):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*Lg,d))
CF['fix_espinha']=U(*[_bolt([_FX[_y][0],_y,228.0],[1,0,0],_FX[_y][1]) for _y in (137.8,322.8)])
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
print('TOPO',_CHK)
pickle.dump(CF,open('CF.pkl','wb')); print(json.dumps(LOG,indent=0))
print('CH_FAIL',CH_FAIL)
