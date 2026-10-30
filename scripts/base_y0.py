# BASE_Y0 (frente): as pecas da frente que paravam em Y 2 descem ate o fundo da base (Y 0), com o proprio perfil;
# a cantoneira da frente e refeita com o fundo em Y 0 e os parafusos da aba lateral em Z 256 (CANTO_CABOS)
import numpy as np, trimesh, pickle, json
exec(open('load.py').read()); exec(open('latload.py').read()); exec(open('geo.py').read())
from shapely.geometry import Polygon, box
from shapely.ops import unary_union as uu
R=pickle.load(open('R4_preY0.pkl','rb')); CF=pickle.load(open('CF.pkl','rb'))
base=M['Corpo1@071.stl']; gb=grow(base,0.2)
def sec_y(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float))
    return uu([p for p in p2.polygons_full])
def prism_xz(poly,y0,y1):
    ms=[]
    for g in (poly.geoms if hasattr(poly,'geoms') else [poly]):
        if g.area<0.3: continue
        m=trimesh.creation.extrude_polygon(g,y1-y0); m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
        if m.volume<0: m.invert()
        ms.append(m)
    return U(*ms)
LOG={}
for k in ('est_D','est_Ci','est_CiL','placa_roxa','placa_22'):
    m=R[k]
    if m.bounds[0][1]<1.0: continue
    ext=prism_xz(sec_y(m,2.3),0.0,2.31)
    ext=D(ext,gb)
    m2=U(m,ext)
    R[k]=max(m2.split(only_watertight=False),key=lambda q:q.volume)
    LOG[k]={'y0':round(float(R[k].bounds[0][1]),2),'vol':bool(R[k].is_volume),'xbase':round(I(R[k],base).volume,2),'ganho':round(R[k].volume-m.volume,1)}
_G={}; exec(open('esb/geom_lat.py').read(),_G)
c54=L['54_cantoneira_base_D'].copy(); c54.apply_translation([3.159+2.2,5.023,6.726+2.2])
exec(open('cap.py').read())
_lp=_G['Lr'].intersection(box(190.0,0.0,270.0,60.0))
CF['cantoneira_F_L']=make_cap(c54,+1,xin=284.0,zin=286.2,ybot=0.0,leg_poly=_lp,xleg=283.8,holes=[(24.5,256.0),(71.5,256.0)],bevel=560.627)
LOG['cantF']={'bb':np.round(CF['cantoneira_F_L'].bounds,1).tolist(),'vol':bool(CF['cantoneira_F_L'].is_volume),'xbase':round(I(CF['cantoneira_F_L'],base).volume,2)}
pickle.dump(R,open('R4.pkl','wb')); pickle.dump(CF,open('CF.pkl','wb'))
print(json.dumps(LOG))
