# cantoneira limpa: perfil em L com faces de dentro planas (assentam por cima das faces alinhadas), chanfros lisos e perna em L
import numpy as np
from shapely.geometry import Polygon, box
from shapely.ops import unary_union as uu
def _sec_y(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float))
    return uu([p for p in p2.polygons_full])
def _prism_xzy(poly,y0,y1):
    m=trimesh.creation.extrude_polygon(poly,y1-y0)
    m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
def make_cap(orig,side,xin=284.0,zin=None,ytop=94.0,ybot=2.0,c=5.5,leg_poly=None,xleg=283.8,holes=(),bevel=None):
    """side=+1 frente (Z+), -1 tras (Z-). zin: plano de dentro da aba da frente/tras."""
    P=_sec_y(orig,60.0); H=P.convex_hull
    lat=box(xin,-1000,1000,1000)
    face=box(-1000,zin,1000,1000) if side>0 else box(-1000,-1000,1000,zin)
    prof=H.intersection(uu([lat,face]))
    prof=Polygon(prof.exterior) if prof.geom_type=='Polygon' else max(prof.geoms,key=lambda g:g.area)
    tip=Polygon([(xin,247.7),(290.0,247.7),(295.5,253.2),(295.5,262.0),(xin,262.0)])     # ponta da aba lateral sempre em |Z| 247,7 (igual frente e tras)
    if side<0: tip=Polygon([(x,-z) for x,z in tip.exterior.coords])
    prof=uu([prof,tip]); prof=Polygon(prof.exterior)
    kb=None
    if bevel is not None:   # quina de dentro chanfrada, paralela ao chanfro da quina da verde da coluna (folga 0,2): tampa o vao
        kb=bevel+0.2*np.sqrt(2)
        if side>0: tri=Polygon([(xin,zin),(xin,kb-xin),(kb-zin,zin)])
        else: tri=Polygon([(xin,zin),(xin,xin-kb),(kb+zin,zin)])
        prof=Polygon(uu([prof,tri]).exterior)
    m=_prism_xzy(prof,ybot,ytop)
    def inner(a,b):   # arestas nas faces de dentro nao levam chanfro
        if abs(a[0]-xin)<1e-3 and abs(b[0]-xin)<1e-3: return True
        if abs(a[1]-zin)<1e-3 and abs(b[1]-zin)<1e-3: return True
        if kb is not None:
            f=(lambda q:q[0]+q[1]) if side>0 else (lambda q:q[0]-q[1])
            if abs(f(a)-kb)<1e-3 and abs(f(b)-kb)<1e-3: return True
        return False
    cut=chamfer_cutter(prof,'y',ytop,c,skip=inner)
    # embaixo: espelha Y (altura -y), mesmo contorno
    cutb=chamfer_cutter(prof,'y-',-ybot,c,skip=inner)
    m=D(m,cut,cutb)
    if leg_poly is not None:
        lp=leg_poly if side>0 else leg_poly
        xo=m.bounds[1][0]
        leg=prism_zy(lp,xleg,xo); leg=chamfer_top(leg,'x',xo,c)
        leg=I(leg,B(xleg-1,xo+1,0,52.0,-262.0,262.0))       # bordas cortadas ficam dentro da aba (sem sulco)
        zc=229.0*side; t=Polygon([(zc-7,17-4.06),(zc+7,17-4.06),(zc,17+8.12)]).buffer(-1.0).buffer(1.0)
        leg=D(leg,prism_zy(t,m.bounds[1][0]-1.5,m.bounds[1][0]+1))
        m=U(m,leg)
    for y,z in holes: m=D(m,CYL([270,y,z],[310,y,z],3.4))
    return m
