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
chk={'es_cap':I(es,cap).volume,'es_sup':I(es,sup).volume,'es_r47':I(es,r47).volume,'es_vs':I(es,vs).volume,'es_bd':I(es,CT['bandaB']).volume,'cap_r47':I(cap,r47).volume,'cap_sup':I(cap,sup).volume,'cap_vs':I(cap,CT['verde_sup']).volume}
for k,mm in (('es',es),('cap',cap),('r47',r47),('sup',sup),('vs',vs)):
    chk['hw_'+k]=sum(I(h,mm).volume for h in hw if h.is_volume)
for f in ('035','052','055','060','062','047'): chk['cap_'+f]=I(cap,trimesh.load('../ltop/'+f+'.stl')).volume
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}), es.is_volume, cap.is_volume, r47.is_volume, sup.is_volume)
CT['espinha']=es; CT['riser47']=r47; CT['verde_sup']=vs; CT['hw_topo']=HW; CT['supF']=sup
pickle.dump(CT,open('CT.pkl','wb'))
