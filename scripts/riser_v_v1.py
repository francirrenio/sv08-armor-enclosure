# RISER: abertura das aletas mais baixa e mais larga (138 x 44: Z 58-196, Y 574-618) + moldura verde embutida em volta
#  - rebaixo de 2 mm na face de fora em volta da abertura (Z 52-202, Y 568-624); moldura verde X 282,2-284,0 com folga 0,5 (linha de sombra)
#    e 0,2 no fundo, chanfro 0,6 na face; presa por 4 pinos de 2,5 em furos de 2,8 no fundo do rebaixo
#  - as 3 aletas ficam 8 mm mais compridas (esticadas no meio) e redistribuidas na altura nova
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
from shapely.geometry import Polygon, box
CT=pickle.load(open('CT.pkl','rb'))
T='../ltop/'
def zy(poly,s):   # espelha Z para o lado de tras
    return poly if s>0 else Polygon([(-z,y) for z,y in poly.exterior.coords])
def rect(z0,z1,y0,y1,r=0.0):
    b=box(z0,y0,z1,y1)
    return b.buffer(-r).buffer(r,resolution=6) if r>0 else b
ZO,YO=(58.0,196.0),(574.0,618.0); ZP,YP=(52.0,202.0),(568.0,624.0)
out={}
for nome,base,s,slats in (('riser47',CT['riser47'],+1,('040','041','042')),('riser35',trimesh.load(T+'035.stl'),-1,('037','038','039'))):
    r=base
    r=U(r,prism_zy(zy(rect(59.9,190.1,567.9,624.1),s),278.0,284.0))                 # o vao antigo vira parede (o riser e refeito em volta da abertura nova)
    r=D(r,prism_zy(zy(rect(ZO[0],ZO[1],YO[0],YO[1]),s),278.2,284.5))                 # abertura nova (parede do fundo ate X 278,2, como na original)
    r=D(r,prism_zy(zy(rect(ZP[0],ZP[1],YP[0],YP[1],1.5),s),282.0,284.5))             # rebaixo da moldura
    pins=[(z,y) for z in (55.25,198.75) for y in (571.0,621.0)]
    r=D(r,*[CYL([279.4,y,s*z],[282.1,y,s*z],2.8) for z,y in pins])
    r=max(r.split(only_watertight=False),key=lambda p:p.volume)
    # moldura verde
    ring=zy(rect(ZP[0]+0.5,ZP[1]-0.5,YP[0]+0.5,YP[1]-0.5,1.0),s).difference(zy(rect(ZO[0],ZO[1],YO[0],YO[1]),s))
    bz=prism_zy(ring,282.2,284.0)
    bz=D(bz,chamfer_cutter(ring,'x',284.0,0.6))
    bz=U(bz,*[CYL([279.7,y,s*z],[282.3,y,s*z],2.5) for z,y in pins])
    # aletas: esticadas 8 mm no meio (as pontas ficam iguais) e reposicionadas na altura
    al=[]
    for k,f in enumerate(slats):
        a=trimesh.load(T+f+'.stl'); zc=s*125.0
        lo=I(a,B(270,290,500,700,-300,zc)); hi=I(a,B(270,290,500,700,zc,300))
        sec=section_polys(a,'z',zc)
        mid=prism_xy(Polygon(max((sec.geoms if hasattr(sec,'geoms') else [sec]),key=lambda g:g.area).exterior),0,8.0)
        if s>0: hi.apply_translation([0,0,8.0]); mid.apply_translation([0,0,zc])
        else: lo.apply_translation([0,0,-8.0]); mid.apply_translation([0,0,zc-8.0])
        a2=U(lo,hi,mid)
        a2.apply_translation([0,0,-s*2.5])                       # centra na abertura nova (Z 58-196)
        y0=a.bounds[0][1]; ynew=575.2+k*14.0
        a2.apply_translation([0,ynew-y0,0])
        al.append(a2)
    chk={'r_bz':I(r,bz).volume,'r_al':sum(I(r,x).volume for x in al),'bz_al':sum(I(bz,x).volume for x in al),'r_cap':I(r,CT['cant_top_F']).volume,'r_es':I(r,CT['espinha']).volume}
    print(nome,json.dumps({k:round(float(v),2) for k,v in chk.items()}), r.is_volume, bz.is_volume, [np.round(x.bounds,1).tolist() for x in al][:1])
    out[nome]=r; out[nome+'_mold']=bz; out[nome+'_aletas']=trimesh.util.concatenate(al)
CT.update(out); pickle.dump(CT,open('CT.pkl','wb'))
