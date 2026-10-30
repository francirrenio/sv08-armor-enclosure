# CANTOS_VERDES: cantos marcados das verdes da base da lateral com o arredondamento R6 (o mesmo da moldura do conector)
#  - verde central (3): os 6 cantos (4 quinas + 2 pontas) com R6
#  - bracos (2 e 4): ponta de fora e as 2 quinas dela com R6; o entalhe onde entra a ponta da verde 3 passa a ser a
#    copia da ponta nova da verde 3 afastada 1,0 (folga constante, R7 no fundo). As pontinhas do entalhe ficam como estao.
#  - placas pretas: so na zona dos cantos mudados, o rebaixo e refeito seguindo o contorno novo (folga 0,5, fundo no
#    mesmo nivel e chanfro de boca 1,25 igual ao resto). Fora dessa zona nada muda.
#  - chanfro de 1,0 da face das verdes refeito no contorno novo. Lado E = espelho (usa E_placa_B do lado_e).
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read()); exec(open('geo_ch2.py').read())
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
R=6.0; GAP=1.0; FOLGA=0.5; CHV=1.0; CHB=1.25; ZONA=2.5
pick=lambda m:max(m.split(only_watertight=False),key=lambda q:q.volume)
def geoms(pg): return [g for g in (pg.geoms if hasattr(pg,'geoms') else [pg]) if g.area>0.02]
def mp(pg,a,b):
    ms=[]
    for g in geoms(pg):
        g=Polygon(g.exterior.coords,[r.coords for r in g.interiors if Polygon(r).area>0.2]).simplify(0.003)
        if g.area<0.2: continue
        q=prism_zy(g,a,b)
        if not q.is_volume: q=prism_zy(g.buffer(0.005,join_style=2),a,b)
        if q.is_volume: ms.append(q)
        else: print('prisma ruim',round(g.area,2))
    return U(*ms)
def contorno(m,x=281.5):
    s=section_polys(m,'x',x); return max([Polygon(g.exterior) for g in geoms(s)],key=lambda p:p.area)
def opening(p,r): return p.buffer(-r,join_style=1,quad_segs=64).buffer(r,join_style=1,quad_segs=64)
def closing(p,r): return p.buffer(r,join_style=1,quad_segs=64).buffer(-r,join_style=1,quad_segs=64)
VER=('verde_central','verde_braco_T','verde_braco_F','verde_lat_T_inf','verde_lat_F_inf','verde_lat_T_sup','verde_lat_F_sup')
PG={k:contorno(RL[k]) for k in VER}; PN=dict(PG)
PN['verde_central']=opening(PG['verde_central'],R)
for k,sg in (('verde_braco_T',-1),('verde_braco_F',1)):
    fora=sbox(-1e3,-1e3,1e3,1e3).difference(sbox(sg*110 if sg<0 else -1e3,-1e3,1e3 if sg<0 else 110,1e3))  # lado da ponta de fora
    ent=sbox(-1e3,-1e3,1e3,1e3).difference(fora)                                                          # lado do entalhe
    a=opening(PG[k],R).intersection(fora).union(closing(PG[k],R+GAP).intersection(ent))
    PN[k]=max(geoms(a.difference(PN["verde_central"].buffer(GAP,join_style=1,quad_segs=64))),key=lambda p:p.area)
MUD=('verde_central','verde_braco_T','verde_braco_F')
out={}
# verdes
for k in MUD:   # peca refeita inteira: prisma do contorno novo com a janela (chanfro de 1 na face, por fora e na janela) e os furos
    m=RL[k]; pn=PN[k]; x0,x1=float(m.bounds[0][0]),float(m.bounds[1][0])
    s=section_polys(m,'x',(x0+x1)/2); ints=[Polygon(r) for g in geoms(s) for r in g.interiors]
    jan=[p for p in ints if p.area>100]; fur=[p for p in ints if 1<p.area<=100]
    P=Polygon(pn.exterior.coords,[p.exterior.coords for p in jan])
    g=D(mp(P,x0,x1),chamfer_cutter(P,'x',x1,CHV))
    if fur: g=D(g,mp(unary_union(fur),x0-1.0,x1+1.0))
    out[k]=pick(g)
# placas
def refaz_placa(p,verdes,extra=None):
    dif=[PG[k].symmetric_difference(PN[k]).buffer(-0.05).buffer(0.05) for k in MUD if k in verdes]   # sem as lascas ao longo das retas
    zona=unary_union([d.buffer(ZONA) for d in dif]+([extra] if extra is not None else []))
    fundo=280.6
    lo,hi=p.bounds
    S=I(p,B(lo[0]-1,fundo-0.15,lo[1]-1,hi[1]+1,lo[2]-1,hi[2]+1))
    S2=S.copy(); S2.apply_translation([3.4,0,0]); base=U(S,S2)                  # o proprio contorno da placa levado ate a face
    ench=I(mp(zona.intersection(unary_union([PG[k] for k in verdes]).buffer(FOLGA+CHB+0.3)),fundo-0.05,283.8),base)
    p=U(p,ench)
    cav=unary_union([PN[k].buffer(FOLGA,join_style=1,quad_segs=64) for k in verdes])
    big=sbox(-400,-50,400,150)
    cut=U(mp(cav,fundo,284.5),chamfer_cutter(big.difference(cav),'x',283.8,CHB))
    p=D(p,I(cut,mp(zona,279.0,285.0)))
    return pick(p),zona
VA=VER; VE=('verde_central','verde_braco_T','verde_lat_T_inf','verde_lat_T_sup','verde_lat_F_sup')   # lado E: sem braco_F e F_inf (moldura do conector)
out['placa_A'],zA=refaz_placa(RL['placa_A'],VA)
out['placa_B'],zB=refaz_placa(RL['placa_B'],VA)
# lado E: sem o braco e a verde de baixo da frente, a parede do rebaixo da verde 3 ficou exposta sem chanfro de boca;
# o rebaixo inteiro da verde 3 ganha o mesmo chanfro de 1,25 (assim nao fica emenda de chanfro so nos cantos)
anel=PN['verde_central'].buffer(FOLGA+ZONA).difference(PN['verde_central'].buffer(-ZONA))
out['E_placa_B'],zE=refaz_placa(CT['E_placa_B'],tuple(k for k in VE if k!='verde_braco_T'),extra=anel)
chk={}
src={'placa_A':RL['placa_A'],'placa_B':RL['placa_B'],'E_placa_B':CT['E_placa_B']}
for kp in src:
    chk[kp+'_ganhou']=D(out[kp],src[kp]).volume; chk[kp+'_perdeu']=D(src[kp],out[kp]).volume
    for k in MUD:
        if kp=='E_placa_B' and k=='verde_braco_F': continue
        chk[k[6:]+'_x_'+kp]=I(out[k],out[kp]).volume
for k in MUD: chk[k[6:]+'_perdeu']=D(RL[k],out[k]).volume; chk[k[6:]+'_ganhou']=D(out[k],RL[k]).volume
chk['v3_x_bT']=I(out['verde_central'],out['verde_braco_T']).volume; chk['v3_x_bF']=I(out['verde_central'],out['verde_braco_F']).volume
chk['folga_min_entalhe']=PN['verde_central'].distance(PN['verde_braco_T'])
chk['ok']=float(all(m.is_volume for m in out.values()))
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}))
exec(open('meshclean.py').read())
for k,v in out.items():
    c=clean(v,0.003); CT['R_'+k]=c if (c.is_volume and abs(c.volume-v.volume)<1.0) else v
pickle.dump(CT,open('CT.pkl','wb'))
pickle.dump((PG,PN),open('cv2d.pkl','wb'))
