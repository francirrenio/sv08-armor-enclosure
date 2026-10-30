# topo da espinha FD aparafusado no suporte de canto do top hat; a cantoneira de cima fica com as faces de dentro planas
#  - espinha ganha uma capa em L de Y 558,4 a 622 ate as faces de fora (lateral X 283,8 / frente Z 286, mesma quina chanfrada da verde)
#  - lateral: os 2 ressaltos do suporte sao encurtados ate X 279,6 (rente a perna); M3x8 ISO7380 com a cabeca embutida na capa
#  - frente: a cantoneira prende com M3x16 atravessando a capa ate os ressaltos da frente do suporte
#  - lateral da cantoneira: M3x16 em Z 235,2 com porca embutida por dentro da espinha (passa pelo riser)
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
from shapely.geometry import Polygon
CT=pickle.load(open('CT.pkl','rb'))
sup0=trimesh.load('../ltop/050.stl')
YS=(563.5,614.0); ZS=259.5; ZF=235.2; XFR=246.0
YC=(542.6,614.0); YIN=542.6     # parafusos da cantoneira (simetricos na altura); embaixo na frente: inserto roscado M3 na espinha
sup=D(sup0,B(279.6,290,550,630,250,270))                                     # ressaltos da lateral encurtados (rentes a perna da espinha)
es=CT['espinha']; cap=CT['cant_top_F']; r47=CT['riser47']
# TOPO_LIMPO: de Y 558,4 a 622 a espinha e refeita como UM prisma limpo (sem sobras da espinha antiga):
#  lateral cheia ate a face de fora X 283,8 desde Z 220,1 (mesmo chanfro da aba de baixo); o riser termina reto em Z 219,9,
#  quina chanfrada igual a da verde, frente cheia de Z 276 a 286 desde a ponta X 235,4; faces de dentro planas X 273 / Z 276
sec=Polygon([(273.0,220.1),(282.4,220.1),(283.8,221.5),(283.8,276.83),(274.63,286.0),(235.4,286.0),(235.4,276.0),(273.0,276.0)])
m=trimesh.creation.extrude_polygon(sec,622.0-558.3); m.apply_transform(np.array([[1,0,0,0],[0,0,1,558.3],[0,1,0,0],[0,0,0,1]],float))
if m.volume<0: m.invert()
es=U(D(es,B(200,300,558.4,700,150,300)),m)
fr=Polygon([(235.4,281.8),(235.4,284.6),(236.8,286.0),(238.3,286.0),(239.55,284.75),(239.55,281.8)])   # friso da ponta da frente (ao lado da verde)
mf=trimesh.creation.extrude_polygon(fr,558.4-548.0); mf.apply_transform(np.array([[1,0,0,0],[0,0,1,548.0],[0,1,0,0],[0,0,0,1]],float))
if mf.volume<0: mf.invert()
es=U(es,mf)   # o friso continua ate o topo limpo (fechava o vao que sobrou do corte antigo da cantoneira)
# FAIXA_2MM: onde a verde e larga (em cima Y 461-558 e embaixo Y 81-133), a faixa azul fica 2 mm mais larga e a verde recua 2 mm
# (a borda entre as duas anda 2 mm para a frente, com os mesmos chanfros; na rampa encontra a borda normal: azul Z 233,25 / verde Z 234)
CF=pickle.load(open('CF.pkl','rb'))
vs=CT['verde_sup']; v72=CF['verde_72']
def _pzx(poly,y0,y1):
    mm=trimesh.creation.extrude_polygon(poly,y1-y0); mm.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if mm.volume<0: mm.invert()
    return mm
def _shift_green(g,y0,y1):
    # borda nova = a mais baixa entre (borda antiga + 2) e a borda normal da verde (Z 234 por dentro, chanfro 2 ate Z 236 por fora)
    zb=B(279.0,284.5,y0,y1,219.0,236.5)
    gt=g.copy(); gt.apply_translation([0,0,2.0])
    S=_pzx(Polygon([(270,234.0),(281.8,234.0),(290,242.2),(290,300),(270,300)]),y0,y1)
    return U(D(g,zb),I(I(g,zb),U(gt,S)))
for (y0,y1) in ((461.0,558.45),(81.0,133.5)):
    # faixa azul: a borda da frente anda 2 mm, limitada pela borda normal da aba (Z 233,25 por dentro, chanfro ate 232 por fora)
    lip=I(es,B(279.55,283.9,y0,y1,219.0,241.0)); lip.apply_translation([0,0,2.0])
    T=_pzx(Polygon([(270,200),(270,233.25),(282.55,233.25),(290,225.8),(290,200)]),y0,y1)
    es=U(es,I(lip,T),B(279.6,283.8,y0,y1,221.5,224.25))   # o miolo da aba fica cheio (sem o vinco entre os 2 chanfros)
vs=_shift_green(vs,461.0,558.45); v72=_shift_green(v72,80.0,133.5)
# FAIXA_2MM_FRENTE: o mesmo na face da frente (ponta da frente): onde a verde e larga (em cima Y 486-558, embaixo Y 81-121)
# a faixa azul fica 2 mm mais larga e a verde recua 2 mm (borda anda +2 em X), limitado pela borda normal (azul X 245,25 / verde X 246)
def _pxz_(poly,y0,y1):
    mm=trimesh.creation.extrude_polygon(poly,y1-y0); mm.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if mm.volume<0: mm.invert()
    return mm
def _shift_green_fr(g,y0,y1):
    zb=B(239.0,250.0,y0,y1,281.0,287.0)
    gt=g.copy(); gt.apply_translation([2.0,0,0])
    S=_pxz_(Polygon([(246.0,200),(300,200),(300,300),(262.0,300),(246.0,284.0)]),y0,y1)
    return U(D(g,zb),I(I(g,zb),U(gt,S)))
for (y0,y1) in ((486.0,558.45),(81.0,121.0)):
    st=I(es,B(235.3,246.0,y0,y1,281.7,286.1)); st.apply_translation([2.0,0,0])
    T=_pxz_(Polygon([(200,200),(245.25,200),(245.25,284.75),(239.0,291.0),(200,291.0)]),y0,y1)
    es=U(es,I(st,T),B(236.8,239.55,y0,y1,281.8,286.0))
vs=_shift_green_fr(vs,486.0,558.45); v72=_shift_green_fr(v72,80.0,121.0)
# CHANFRO_BASE: na base (encontro com a placa preta em Y 81) a verde e a faixa azul levam chanfro de 1,2 nas arestas de fora,
# igual ao da moldura do painel (que tambem termina em Y 81,2 com chanfro 1,2)
def _chanfro_base(m,y0,c=1.2):
    s=section_polys(m,'y',y0) if False else None
    sec=m.section(plane_origin=[0,y0+0.05,0],plane_normal=[0,1,0])
    from shapely.ops import unary_union as _u
    p2,T=sec.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-(y0+0.05)],[0,0,0,1]],float))
    poly=_u([p for p in p2.polygons_full]); out=m
    for g in (poly.geoms if hasattr(poly,'geoms') else [poly]):
        g=g.simplify(0.01)
        fora=lambda a,b: all((q[0]>=281.5 or q[1]>=284.0) for q in (a,b))
        out=D(out,chamfer_cutter(Polygon(g.exterior),'y-',-y0,c,skip=lambda a,b: not fora(a,b)))
    return out
es=_chanfro_base(es,81.0); v72=_chanfro_base(v72,81.2)
vs=max(vs.split(only_watertight=False),key=lambda p:p.volume); v72=max(v72.split(only_watertight=False),key=lambda p:p.volume)
CT['verde_sup']=vs; CT['verde_72']=v72
es=D(es,I(grow(sup,0.2),B(230,284.5,550,630,240,287)))                         # alojamento dos ressaltos (folga 0,2)
es=D(es,*[CYL([279.0,y,ZS],[285.0,y,ZS],3.4) for y in YS],*[CYL([282.0,y,ZS],[285.0,y,ZS],6.2) for y in YS])   # lateral: passante + cabeca embutida
es=D(es,CYL([XFR,614.0,280.0],[XFR,614.0,287.0],3.4))                       # frente em cima: passante ate o ressalto
es=D(es,CYL([XFR,YIN,277.3],[XFR,YIN,287.0],4.2))                            # frente embaixo: furo do inserto M3 (4,2 x 4,5) por fora, coberto pela verde
es=D(es,*[CYL([268.0,y,ZF],[285.0,y,ZF],3.4) for y in YC],*[CYL([272.0,y,ZF],[275.6,y,ZF],2*3.406,sec=6) for y in YC])   # lateral da cantoneira: passante + porca
es=max(es.split(only_watertight=False),key=lambda p:p.volume)
r47=D(r47,B(270,290,500,700,219.9,300))    # ponta do riser reta em Z 219,9 ...
_s=section_polys(r47,'z',219.5); _s=max((_s.geoms if hasattr(_s,'geoms') else [_s]),key=lambda g:g.area)
r_enc=prism_xy(Polygon(_s.exterior),219.5,229.9)                              # ... e entra 10 mm na espinha (encaixe), com a mesma secao da ponta
r47=U(r47,r_enc)
es=D(es,grow(r_enc,0.2)); es=max(es.split(only_watertight=False),key=lambda p:p.volume)   # rebaixo de 10 mm na espinha para a ponta do riser (folga 0,2)

vs=D(CT['verde_sup'],CYL([278.0,YIN,ZF],[285.0,YIN,ZF],3.4),CYL([XFR,YIN,280.0],[XFR,YIN,287.0],3.4)); vs=max(vs.split(only_watertight=False),key=lambda p:p.volume)   # verde: passantes dos 2 parafusos de baixo
r47=max(r47.split(only_watertight=False),key=lambda p:p.volume)
hw=[]
for y in YS:
    hw+=[CYL([282.0,y,ZS],[283.65,y,ZS],5.7),CYL([274.0,y,ZS],[282.0,y,ZS],3.0)]                                   # espinha -> ressalto lateral: M3x8
for y in YC:
    hw+=[CYL([287.5,y,ZF],[289.15,y,ZF],5.7),CYL([271.5,y,ZF],[287.5,y,ZF],3.0),CYL([273.2,y,ZF],[275.6,y,ZF],2*3.175,sec=6)]   # cantoneira lateral -> espinha: M3x16 + porca
hw+=[CYL([XFR,614.0,289.7],[XFR,614.0,291.35],5.7),CYL([XFR,614.0,273.7],[XFR,614.0,289.7],3.0)]                # frente em cima -> ressalto: M3x16
hw+=[CYL([XFR,YIN,289.7],[XFR,YIN,291.35],5.7),CYL([XFR,YIN,278.7],[XFR,YIN,289.7],3.0),CYL([XFR,YIN,277.5],[XFR,YIN,281.8],4.4)]   # frente embaixo -> inserto: M3x12
HW=trimesh.util.concatenate(hw)
chk={'es_cap':I(es,cap).volume,'es_sup':I(es,sup).volume,'es_r47':I(es,r47).volume,'es_vs':I(es,vs).volume,'es_v72':I(es,CT['verde_72']).volume,'es_bd':I(es,CT['bandaB']).volume,'cap_r47':I(cap,r47).volume,'cap_sup':I(cap,sup).volume,'cap_vs':I(cap,CT['verde_sup']).volume}
for k,mm in (('es',es),('cap',cap),('r47',r47),('sup',sup),('vs',vs)):
    chk['hw_'+k]=sum(I(h,mm).volume for h in hw if h.is_volume)
for f in ('035','052','055','060','062','047'): chk['cap_'+f]=I(cap,trimesh.load('../ltop/'+f+'.stl')).volume
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}), es.is_volume, cap.is_volume, r47.is_volume, sup.is_volume)
CT['espinha']=es; CT['riser47']=r47; CT['verde_sup']=vs; CT['hw_topo']=HW; CT['supF']=sup
pickle.dump(CT,open('CT.pkl','wb'))
