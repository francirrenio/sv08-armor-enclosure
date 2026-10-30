# LADO E - CONECTOR DE FORCA (coordenadas do lado D; a exportacao espelha)
#  O conector passa da base para a ESTRUTURA LATERAL (escondida), com o mesmo encaixe da base:
#   - a pele de fora da estrutura (X 273-276,8, 3,8 mm) e a parede do conector: janela 48,6 x 28 (cantos arredondados,
#     Z 111,2-159,8, Y 5-33) e os 2 furos D4 (Z 107,5 / 163,5, Y 19,5); atras, a janela continua pelas nervuras ate a base
#   - o rebaixo 73,4 x 32,8 (Z 99,1-172,4, Y 3,2-35,9) fica por fora, no vao da placa preta + moldura verde (10 mm, a base tem 9,7);
#     aberto embaixo (nao sobra tira fina na borda)
#   - a emenda das 2 estruturas (Z 140) passa pelo encaixe; os dentes pequenos dela no trecho do encaixe saem e entra
#     1 rabo de andorinha maior no meio do que sobra acima do encaixe (Y 42-62), na pele de fora (X 273-276,8), folga 0,2
#  Por fora, a placa preta e a moldura verde so deixam o vao (do tamanho do rebaixo):
#   - saem a verde de baixo da frente e o braco da frente nesse lado; os rebaixos deles na placa sao fechados
#   - moldura verde em U em volta do vao: borda de 9 mm, Y ate 43,9; quinas de cima a 45 graus (5 mm), chanfro de 1 mm;
#     presa por 2 M3x8 de cabeca abaulada nas quinas de cima
import numpy as np, pickle, trimesh, json
exec(open('load.py').read()); exec(open('geo.py').read()); exec(open('geo_ch2.py').read())
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
base=M['Corpo1@071.stl']
def ints(x,zr,ymax=40):
    s=section_polys(base,'x',x); gs=s.geoms if hasattr(s,'geoms') else [s]
    return [Polygon(i.coords) for g in gs for i in g.interiors if zr[0]<i.bounds[0] and i.bounds[2]<zr[1] and i.bounds[3]<ymax]
jan=ints(-256.0,(100.0,170.0)); janela=[p for p in jan if p.area>500][0]; furos=[p for p in jan if p.area<=500]
rebx=[p for p in ints(-262.0,(95.0,175.0)) if p.area>1000][0]               # rebaixo 73,4 x 32,8
reb_aberto=unary_union([rebx,sbox(rebx.bounds[0]+6,0.0,rebx.bounds[2]-6,rebx.bounds[1]+3)]) # aberto embaixo
reb_aberto=unary_union([rebx,Polygon([(rebx.bounds[0],0.0),(rebx.bounds[2],0.0),(rebx.bounds[2],10.0),(rebx.bounds[0],10.0)])])
pick=lambda m:max(m.split(only_watertight=False),key=lambda q:q.volume)
def mp(pg,a,b,f): return U(*[f(g,a,b) for g in (pg.geoms if hasattr(pg,'geoms') else [pg]) if g.area>0.05])
XF=276.8; XW1=XF-9.7; XW0=XW1-3.5                                            # parede do conector X 263,6-267,1
# --- estrutura: encaixe + andorinha maior na emenda
# CONTORNO_AS03: a estrutura contorna a tomada AS03 (STEP do fabricante) com folga de 0,2:
#  - janela = corpo da tomada (47 x 26,8) + 0,2 em volta, atravessando a pele e as nervuras
#  - em volta da flange (66,3 x 32,3, 2,75 de espessura) a estrutura sobe ate a face da flange (X 279,55), preenchendo o vao
#    da placa (com 0,2 de folga da placa), com o encaixe da flange + 0,2
_AS=pickle.load(open('../as03/as03_contornos_D.pkl','rb'))
FLT=2.75
cut_enc=[prism_zy(_AS['corpo'].buffer(0.2,join_style=1),250.0,XF+FLT+0.5)]+[prism_zy(p,270.0,XF+0.5) for p in furos]
_ressalto=reb_aberto.buffer(-0.2,join_style=2).intersection(sbox(0,2.0,400,100)).difference(_AS['flange'].buffer(0.2,join_style=1))
_ressalto=mp(_ressalto,XF-0.01,XF+FLT,prism_zy)
ZJ0,ZJ1=139.9,140.1; DVD=10.0
cauda=Polygon([(ZJ1+0.1,45.0),(ZJ1+0.1,59.0),(ZJ1-DVD,62.0),(ZJ1-DVD,42.0)])   # (z,y): pescoco 14 na emenda, 20 na ponta
espiga=prism_zy(cauda,273.2,XF)
FSm=[(94.6,39.9),(176.9,39.9)]                                                 # parafusos da moldura verde
def _ext_y(m,yref,y0,y1):   # perfil (x,z) da propria peca em yref, extrudado em Y
    sec=m.section(plane_origin=[0,yref,0],plane_normal=[0,1,0])
    p2,_=sec.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-yref],[0,0,0,1]],float))
    ms=[]
    for g in p2.polygons_full:
        mm=trimesh.creation.extrude_polygon(g,y1-y0); mm.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
        if mm.volume<0: mm.invert()
        ms.append(mm)
    return U(*ms)
def prep(m,lado):
    cs=[m] if m.is_volume else m.split(only_watertight=False); out=[]
    for c in cs:
        if c.is_volume and not (np.any(c.bounds[0]>np.array([300,70,185])) or np.any(c.bounds[1]<np.array([255,0,85]))):
            # dentes pequenos da emenda no trecho do encaixe e do pino (Y < 41): emenda reta ali
            if lado=='meio': c=D(c,B(255,280,0,41.0,ZJ0,150.0)); c=U(c,I(_ext_y(c,45.0,2.0,41.0),B(255,280,2.0,41.0,130.0,ZJ0)))
            else:            c=D(c,B(255,280,0,41.0,125.0,ZJ1)); c=U(c,I(_ext_y(c,45.0,2.0,41.0),B(255,280,2.0,41.0,ZJ1,150.0)))
            zr=(80.0,ZJ0) if lado=='meio' else (ZJ1,190.0)   # pele lisa no vao (fecha furos de parafusos que sairam), depois janela e furos
            c=U(c,I(mp(reb_aberto,273.0,XF,prism_zy),B(255,280,2.0,36.0,*zr)))
            c=U(c,I(_ressalto,B(255,285,0.0,40.0,*zr)))
            c=D(c,*cut_enc,*[CYL([268.0,y,z],[278.0,y,z],2.5) for z,y in FSm])
            if lado=='meio': c=D(c,prism_zy(cauda.buffer(0.2,join_style=2),272.9,XF+0.5))
            else:            c=U(c,espiga)
            c=pick(c)
        out.append(c)
    return out[0] if len(out)==1 else trimesh.util.concatenate(out)
eLM=prep(RL['est_meio'],'meio'); eLF=prep(RL['est_frente'],'frente')
# --- moldura verde em volta do vao
K=5.0; BD=9.0
Z0,Z1,Y0,Y1=rebx.bounds[0]-BD,rebx.bounds[2]+BD,2.0,rebx.bounds[3]+8.0
fora=Polygon([(Z0,Y0),(Z1,Y0),(Z1,Y1-K),(Z1-K,Y1),(Z0+K,Y1),(Z0,Y1-K)])
# MOLDURA_LARGA: as bordas entram no vao (ficam em balanco sobre ele) ate perto da janela e dos parafusos do conector:
# abertura Z 104-167 (antes 99,1-172,4), topo em Y 33,5 (antes 35,9, a janela vai ate 33); quinas de dentro arredondadas R4
RQ=4.0; ZA,ZB,YT=104.0,167.0,33.5
abert=unary_union([sbox(ZA+RQ,-5.0,ZB-RQ,YT-RQ).buffer(RQ,resolution=16),sbox(ZA,-5.0,ZB,YT-RQ)])
# MOLDURA_CONTORNO: a abertura da moldura segue a flange da tomada AS03 + 0,2 (mesmo contorno da estrutura);
# embaixo fica aberta na largura do lado reto de baixo da flange, para nao sobrar tira fina na borda
_ASm=pickle.load(open('../as03/as03_contornos_D.pkl','rb'))
_fb=_ASm['flange'].bounds; _zc=0.5*(_fb[0]+_fb[2])
abert=unary_union([_ASm['flange'].buffer(0.2,join_style=1),sbox(_zc-22.17,-5.0,_zc+22.17,_fb[1]+0.6)])
mold_pg=fora.difference(abert)
mold=mp(mold_pg,280.8,283.8,prism_zy)
ch=chamfer_cutter(mold_pg,'x',283.8,1.0,skip=lambda a,b: a[1]<Y0+0.01 and b[1]<Y0+0.01)
mold=pick(D(mold,ch,*[CYL([279.0,y,z],[285.0,y,z],3.4) for z,y in FSm]))
# --- placa preta: fecha os rebaixos das verdes que saem e abre o vao
pl=RL['placa_B']
perf=mp(section_polys(pl,'z',225.0),70.0,215.0,prism_xy)
_rm=unary_union([Polygon(g.exterior) for k in ('verde_lat_F_inf','verde_braco_F') for g in [section_polys(RL[k],'x',282.5)]]).buffer(2.0,join_style=2)
_enc=U(mp(_rm,280.0,284.5,prism_zy),CYL([276.0,37.0,195.0],[282.0,37.0,195.0],3.2))
pl2=U(pl,I(perf,_enc))
topo=RL['verde_lat_F_sup']
rt=prism_zy(Polygon(section_polys(topo,'x',282.5).buffer(0.5,join_style=2).exterior),280.8,284.5)
_r3=prism_zy(Polygon(section_polys(RL['verde_central'],'x',282.5).buffer(0.5,join_style=2).exterior),280.8,284.5)
reb_m=prism_zy(fora.buffer(0.5,join_style=2),280.8,284.5)
pl2=D(pl2,I(rt,B(270,290,30,70,60,220)),I(_r3,B(270,290,0,80,60,100)),reb_m,mp(reb_aberto,270.0,285.0,prism_zy),
      *[CYL([272.0,y,z],[281.0,y,z],2.5) for z,y in FSm])
pl2=pick(pl2)
def btn(p,axis,Lg,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*Lg,3.0))
hwm=trimesh.util.concatenate([btn([283.8,y,z],[1,0,0],8.0) for z,y in FSm])
def vol_ok(m): return float(m.is_volume) if m.is_volume else float(all(c.is_volume for c in m.split(only_watertight=False)))
def iv(a,b):
    A=[a] if a.is_volume else [c for c in a.split(only_watertight=False) if c.is_volume]
    Bs=[b] if b.is_volume else [c for c in b.split(only_watertight=False) if c.is_volume]
    return sum(I(x,y).volume for x in A for y in Bs)
chk={'mold_ok':float(mold.is_volume),'pl_ok':float(pl2.is_volume),'mold_x_pl':I(mold,pl2).volume,'mold_x_topo':I(mold,topo).volume,
     'meio_x_frente':iv(eLM,eLF),'pl_x_meio':iv(pl2,eLM),'pl_x_frente':iv(pl2,eLF),'hw_x_mold':I(hwm,mold).volume,
     'est_x_base':iv(eLM,base)+iv(eLF,base),'rebx':[round(v,1) for v in rebx.bounds],'Y1':Y1,'Z0Z1':(Z0,Z1)}
print(json.dumps({k:(round(float(v),2) if isinstance(v,(int,float)) else v) for k,v in chk.items()}))
CT['E_placa_B']=pl2; CT['E_moldura_conector']=mold; CT['E_hw_moldura']=hwm; CT['E_est_meio']=eLM; CT['E_est_frente']=eLF
pickle.dump(CT,open('CT.pkl','wb'))
