# chanfro com face lisa (loft entre o contorno e o contorno deslocado), no lugar da aproximacao em degraus
import numpy as np, trimesh
from shapely.geometry import Polygon, Point, LinearRing
from shapely.geometry.polygon import orient
from shapely.ops import unary_union as _uu, nearest_points
def _ring_offset(ring_pts, target_ring, d):
    # para cada vertice: ponto de esquadria deslocado d (para dentro do material), projetado no contorno alvo
    P=np.array(ring_pts)[:-1]; n=len(P); out=[]
    tr=LinearRing(target_ring)
    for i in range(n):
        a,b,c=P[i-1],P[i],P[(i+1)%n]
        e1=b-a; e2=c-b
        l1=np.linalg.norm(e1); l2=np.linalg.norm(e2)
        if l1<1e-9 or l2<1e-9: q=b
        else:
            n1=np.array([-e1[1],e1[0]])/l1; n2=np.array([-e2[1],e2[0]])/l2   # normal a esquerda (anel CCW -> para dentro)
            s=1.0+float(n1@n2)
            q=b+d*(n1+n2)/s if s>0.2 else b+d*(n1+n2)/max(np.linalg.norm(n1+n2),1e-6)
        out.append(tr.project(Point(q)))
    L=tr.length; t=np.array(out,float)
    for i in range(1,n):                       # desenrola e forca a ordem (sem voltar no contorno)
        while t[i]-t[i-1]<-L/2: t[i]+=L
        while t[i]-t[i-1]>L/2: t[i]-=L
    t=np.maximum.accumulate(t)
    if t[-1]-t[0]>L: t=np.minimum(t,t[0]+L-1e-6)
    pts=[tr.interpolate(x%L) for x in t]
    return [(p.x,p.y) for p in pts]
import mapbox_earcut as _ec
def _cap(pg):
    rings=[np.array(pg.exterior.coords)[:-1]]+[np.array(r.coords)[:-1] for r in pg.interiors]
    v=np.vstack(rings); ends=np.cumsum([len(r) for r in rings]).astype(np.uint32)
    t=np.array(_ec.triangulate_float64(v,ends)).reshape(-1,3)
    # orientar triangulos para +normal
    a,b,c=v[t[:,0]],v[t[:,1]],v[t[:,2]]
    cr=(b[:,0]-a[:,0])*(c[:,1]-a[:,1])-(b[:,1]-a[:,1])*(c[:,0]-a[:,0])
    t[cr<0]=t[cr<0][:,::-1]
    return v,t
def _clean(pg):
    def dd(r):
        r=np.array(r)[:-1]; keep=[0]
        for i in range(1,len(r)):
            if np.linalg.norm(r[i]-r[keep[-1]])>1e-4: keep.append(i)
        r=r[keep]
        if np.linalg.norm(r[0]-r[-1])<1e-4: r=r[:-1]
        return r
    return Polygon(dd(pg.exterior.coords),[dd(i.coords) for i in pg.interiors])
def _poly_mesh(poly,h0,h1,c,sign=1):
    """prisma de poly de h0 a h1; borda de cima com chanfro c (sign=+1 chanfro para dentro; -1 abre para fora)."""
    poly=orient(_clean(poly),1.0)
    top=poly.buffer(-sign*c,join_style=2,mitre_limit=10)
    if top.is_empty or top.geom_type!='Polygon': raise ValueError('topo')
    top=orient(_clean(top),1.0)
    rings_b=[list(poly.exterior.coords)]+[list(r.coords) for r in poly.interiors]
    if len(top.interiors)!=len(poly.interiors): raise ValueError('furos')
    # casar furos por proximidade
    tint=list(top.interiors); rings_t=[list(top.exterior.coords)]
    for r in poly.interiors:
        cen=Polygon(r).centroid; j=int(np.argmin([Polygon(t).centroid.distance(cen) for t in tint])); rings_t.append(list(tint.pop(j).coords))
    V=[]; F=[]
    def add(p): V.append(p); return len(V)-1
    top_rings=[]
    for rb,rt in zip(rings_b,rings_t):
        q=_ring_offset(rb,rt,sign*c)
        P=np.array(rb)[:-1]; n=len(P)
        ib=[add((x,y,h0)) for x,y in P]; im=[add((x,y,h1-c)) for x,y in P]; it=[add((x,y,h1)) for x,y in q]
        for i in range(n):
            j=(i+1)%n
            F+= [[ib[i],ib[j],im[j]],[ib[i],im[j],im[i]],[im[i],im[j],it[j]],[im[i],it[j],it[i]]]
        top_rings.append(q)
    def dedup(r):
        o=[r[0]]
        for p in r[1:]:
            if abs(p[0]-o[-1][0])>1e-6 or abs(p[1]-o[-1][1])>1e-6: o.append(p)
        if abs(o[0][0]-o[-1][0])<1e-6 and abs(o[0][1]-o[-1][1])<1e-6: o=o[:-1]
        return o
    tp=Polygon(dedup(top_rings[0]),[dedup(r) for r in top_rings[1:]])
    if not tp.is_valid: raise ValueError('topo invalido')
    vt,ft=_cap(tp)
    vb,fb=_cap(poly)
    o=len(V); V+= [(x,y,h1) for x,y in vt]; F+= (np.array(ft)+o).tolist()
    o=len(V); V+= [(x,y,h0) for x,y in vb]; F+= (np.array(fb)[:,::-1]+o).tolist()
    m=trimesh.Trimesh(np.array(V,float),np.array(F),process=True)
    m.merge_vertices(digits_vertex=5); m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices()
    trimesh.repair.fix_normals(m)
    if not m.is_watertight: raise ValueError('nao fechado')
    if m.volume<0: m.invert()
    return m
def _place(m,axis,a0):
    if axis=='z': return m
    # coords (a=z, b=y), altura -> x
    T=np.array([[0,0,1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]],float); m=m.copy(); m.apply_transform(T)
    if m.volume<0: m.invert()
    return m
def chamfer_solid(poly,h0,h1,c,axis='z',sign=1):
    gs=[g for g in (poly.geoms if hasattr(poly,'geoms') else [poly]) if g.area>0.3]
    ms=[]
    for g in gs:
        try: ms.append(_place(_poly_mesh(g.buffer(0),h0,h1,c,sign),axis,h0))
        except Exception as e:
            CH_FAIL.append(str(e)); ms.append(None)
    return ms
CH_FAIL=[]
