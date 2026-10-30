# RISER: abertura das aletas mais baixa e mais larga (138 x 44: Z 58-196, Y 574-618) + moldura verde embutida em volta
#  - moldura verde POR FORA da face do riser (placa de 3 mm, Z 50,5-203,5, Y 566-626), presa com 4 parafusos M3x8 escareados
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
    # o vao antigo (com o chanfro de 0,7 da borda) vira parede inteira e a abertura nova e cortada nela: face do riser lisa
    r=U(r,prism_zy(zy(rect(57.5,192.5,565.5,626.5),s),278.0,284.0))
    r=D(r,prism_zy(zy(rect(ZO[0],ZO[1],YO[0],YO[1]),s),278.2,284.5))                 # abertura nova (parede do fundo ate X 278,2, como na original)
    # moldura verde POR FORA: placa de 4 mm sobre a face do riser (X 284-288), quinas R5 por fora e R2 por dentro, chanfro 0,8 por fora e por dentro,
    # 4 parafusos M3x8 de cabeca escareada nos cantos (rosca no riser, furo 2,5)
    PZ,PY=(50.5,203.5),(566.0,626.0)
    scr=[(z,y) for z in (54.5,199.5) for y in (570.5,621.5)]
    ring=zy(rect(PZ[0],PZ[1],PY[0],PY[1],5.0),s).difference(zy(rect(ZO[0],ZO[1],YO[0],YO[1],2.0),s))   # quinas arredondadas: R5 por fora, R2 por dentro
    bz=prism_zy(ring,284.0,288.0)                                   # placa de 4 mm
    bz=D(bz,chamfer_cutter(ring,'x',288.0,0.8))
    for z,y in scr:
        bz=D(bz,CYL([283.5,y,s*z],[288.5,y,s*z],3.4))
        cs=trimesh.creation.cone(radius=3.3,height=3.3,sections=32); cs.apply_transform(trimesh.geometry.align_vectors([0,0,1],[-1,0,0])); cs.apply_translation([288.2,y,s*z])
        bz=D(bz,cs)
    r=D(r,*[CYL([278.6,y,s*z],[284.5,y,s*z],2.5) for z,y in scr])
    r=max(r.split(only_watertight=False),key=lambda p:p.volume)
    hwm=[]
    for z,y in scr:
        h=trimesh.creation.cone(radius=2.85,height=2.85,sections=24); h.apply_transform(trimesh.geometry.align_vectors([0,0,1],[-1,0,0])); h.apply_translation([288.0,y,s*z])
        hwm+=[I(h,B(285.0,288.0,y-4,y+4,s*z-4,s*z+4)),CYL([280.0,y,s*z],[285.2,y,s*z],3.0)]
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
    out[nome]=r; out[nome+'_mold']=bz; out[nome+'_aletas']=trimesh.util.concatenate(al); out[nome+'_hw']=trimesh.util.concatenate(hwm)
CT.update(out); pickle.dump(CT,open('CT.pkl','wb'))
