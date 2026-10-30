import numpy as np, trimesh, shapely
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union
from skimage import measure
def B(x0,x1,y0,y1,z0,z1):
    x0,x1=sorted((x0,x1)); y0,y1=sorted((y0,y1)); z0,z1=sorted((z0,z1))
    m=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); m.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return m
def CYL(p0,p1,d,sec=32):
    p0=np.array(p0,float); p1=np.array(p1,float)
    return trimesh.creation.cylinder(radius=d/2,segment=[p0,p1],sections=sec)
def U(*ms):
    ms=[m for m in ms if m is not None and len(m.faces)]
    return trimesh.boolean.union(ms,engine='manifold') if len(ms)>1 else ms[0]
def D(a,*bs):
    bs=[b for b in bs if b is not None and len(b.faces)]
    return trimesh.boolean.difference([a]+bs,engine='manifold') if bs else a
def I(a,b): return trimesh.boolean.intersection([a,b],engine='manifold')
def HS(p,n,size=2000):
    # meio-espaco (q-p).n <= 0 como caixa grande
    n=np.array(n,float); n/=np.linalg.norm(n)
    m=trimesh.creation.box(extents=[size,size,size])
    # alinhar eixo z da caixa com n
    T=trimesh.geometry.align_vectors([0,0,1],n)
    m.apply_transform(T); m.apply_translation(np.array(p)-n*size/2); return m
def grow(m,c):
    parts=[m]
    for v in ((c,0,0),(-c,0,0),(0,c,0),(0,-c,0),(0,0,c),(0,0,-c)):
        q=m.copy(); q.apply_translation(v); parts.append(q)
    return U(*parts)
def prism_xy(poly,z0,z1):
    # poligono no plano XY extrudado em Z
    m=trimesh.creation.extrude_polygon(poly,z1-z0); m.apply_translation([0,0,z0]); return m
def prism_zy(poly,x0,x1):
    # poligono com coords (z,y) extrudado em X de x0 a x1
    m=trimesh.creation.extrude_polygon(poly,x1-x0)   # coords (a=z,b=y), altura em c
    # mapear (a,b,c)->(x=x0+c, y=b, z=a)
    T=np.array([[0,0,1,x0],[0,1,0,0],[1,0,0,0],[0,0,0,1]],float)
    m.apply_transform(T)
    if m.volume<0: m.invert()
    return m
def pockets(H,a0,b0,step,lo,hi,minarea=40):
    mask=((H>lo)&(H<hi)).astype(float)
    mask=np.pad(mask,1)
    cs=measure.find_contours(mask,0.5)
    polys=[]
    for c in cs:
        pts=[(a0+(j-1)*step,b0+(i-1)*step) for i,j in c]
        if len(pts)<4: continue
        p=Polygon(pts)
        if not p.is_valid: p=p.buffer(0)
        if p.area>minarea: polys.append(p.simplify(0.3))
    return polys
from shapely.geometry import Polygon as _Poly, box as _box
from shapely.ops import unary_union as _uu
def section_polys(m,axis,val):
    if axis=='z':
        s=m.section(plane_origin=[0,0,val],plane_normal=[0,0,1]); 
        if s is None: return None
        p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,-val],[0,0,0,1]]))
    else:
        s=m.section(plane_origin=[val,0,0],plane_normal=[1,0,0])
        if s is None: return None
        # coords (z,y)
        p2,T=s.to_2D(to_2D=np.array([[0,0,1,0],[0,1,0,0],[1,0,0,-val],[0,0,0,1]]))
    return _uu([p for p in p2.polygons_full])
def chamfer_top(m,axis,ztop,c,n=5,pad=50):
    poly=section_polys(m,axis,ztop-0.05)
    if poly is None or poly.is_empty: return m
    bb=_box(*np.array(poly.bounds)+np.array([-pad,-pad,pad,pad]))
    cuts=[]
    for i in range(n):
        r=c*(1-(i+0.5)/n); z1=ztop-c*i/n+0.01; z0=ztop-c*(i+1)/n
        reg=bb.difference(poly.buffer(-r,join_style=2))
        if reg.is_empty: continue
        for g in (reg.geoms if hasattr(reg,'geoms') else [reg]):
            if g.area<0.01: continue
            cuts.append(prism_xy(g,z0,z1) if axis=='z' else prism_zy(g,z0,z1))
    return D(m,*cuts) if cuts else m
# ---- chanfro com face lisa (substitui a versao em degraus) ----
exec(open('/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/pe/geo_ch2.py').read())
chamfer_top_steps=chamfer_top
CH_FAIL=[]
def chamfer_top(m,axis,ztop,c,n=5,pad=50):
    poly=section_polys(m,axis,ztop-0.05)
    if poly is None or poly.is_empty: return m
    cut=chamfer_cutter(poly,axis,ztop,c)
    return D(m,cut) if cut is not None else m
def chamfer_solid(poly,h0,h1,c,axis='z',sign=1):
    m=prism_xy(poly,h0,h1) if axis=='z' else prism_zy(poly,h0,h1)
    return [chamfer_top(m,axis,h1,c)]
