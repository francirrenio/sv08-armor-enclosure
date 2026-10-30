import pickle,numpy as np,trimesh
exec(open('geo.py').read())
from shapely.geometry import Polygon
pts=[[288.14, 633.6], [281.8, 633.6], [281.8, 551.0], [283.1, 551.0], [283.8, 550.3], [283.8, 541.6], [284.0, 541.6], [284.0, 523.0], [288.14, 523.0], [293.3, 533.32], [293.3, 623.28], [288.14, 633.6]]
poly=Polygon(pts)
m=prism_xy(poly,205.0,254.0)
parts=pickle.load(open('parts.pkl','rb'))
for pid,lab,grp,mm in parts:
    p={'id':pid,'mode':grp}
    if p['id'] in ('thCantF','thCantF0'): continue

    if not (mm.bounds[0]<m.bounds[1]).all() or not (mm.bounds[1]>m.bounds[0]).all(): continue
    try: v=I(m,mm).volume
    except Exception as e: v=str(e)[:40]
    i=I(m,mm) if isinstance(v,float) and v>0.01 else None
    print(p['id'],p['mode'],v, np.round(i.bounds,1).tolist() if i is not None else '')
