# chanfro de face lisa por cunhas ao longo de cada aresta do contorno (robusto para paredes finas e furos)
import numpy as np, trimesh
from shapely.geometry.polygon import orient as _orient
def _map(axis,p,h):
    # 'z': (x,y) plano, altura z; 'x': (z,y) plano, altura x; 'y': (x,z) plano, altura y; 'y-': (x,z), altura -y (chanfro embaixo)
    if axis=='z': return (p[0],p[1],h)
    if axis=='x': return (h,p[1],p[0])
    if axis=='y': return (p[0],h,p[1])
    return (p[0],-h,p[1])
def _rings(poly):
    out=[]
    for g in (poly.geoms if hasattr(poly,'geoms') else [poly]):
        if g.area<0.05: continue
        g=_orient(g,1.0)
        out.append(np.array(g.exterior.coords)[:-1])
        for r in g.interiors: out.append(np.array(r.coords)[:-1])
    return out
def chamfer_cutter(poly,axis,ztop,c,skip=None):
    hulls=[]
    for R in _rings(poly):
        n=len(R)
        if n<3: continue
        # convexidade de cada vertice (material a esquerda)
        conv=[]; turn=[]
        for i in range(n):
            a,b,cc=R[i-1],R[i],R[(i+1)%n]
            cr=(b[0]-a[0])*(cc[1]-b[1])-(b[1]-a[1])*(cc[0]-b[0])
            conv.append(cr>1e-9)
            d1=b-a; d2=cc-b
            ang=abs(np.arctan2(d1[0]*d2[1]-d1[1]*d2[0], d1@d2)); turn.append(ang)
        for i in range(n):
            a=R[i]; b=R[(i+1)%n]; d=b-a; L=np.linalg.norm(d)
            if L<1e-6: continue
            if skip is not None and skip(a,b): continue
            t=d/L; nn=np.array([-t[1],t[0]])
            def ext(k):   # canto para dentro com curva suave: estende so o necessario para fechar a fresta
                if conv[k] or turn[k]>np.radians(20): return 0.0
                return (c+1.0)*np.tan(turn[k]/2)+0.02
            ea=ext(i); eb=ext((i+1)%n)
            if skip is not None:   # vizinho sem chanfro (face de dentro): o chanfro atravessa ate o fim, sem deixar parede na quina
                if skip(R[i-1],R[i]): ea=c+1.0
                if skip(R[(i+1)%n],R[(i+2)%n]): eb=c+1.0
            pts=[]
            for u in (-ea,L+eb):
                base=a+t*u
                for s,h in ((-0.5,ztop-c-0.5),(-0.5,ztop+1.0),(c+1.0,ztop+1.0)):
                    p2=base+nn*s
                    pts.append(_map(axis,p2,h))
            try: hulls.append(trimesh.convex.convex_hull(np.array(pts)))
            except Exception: pass
        for i in range(n):
            if conv[i] or turn[i]<=np.radians(20): continue
            if skip is not None and (skip(R[i-1],R[i]) or skip(R[i],R[(i+1)%n])): continue
            v=R[i]; ang=np.linspace(0,2*np.pi,65)[:-1]; rr=c+1.0
            pts=[_map(axis,v,ztop-c)]+[_map(axis,(v[0]+rr*np.cos(a),v[1]+rr*np.sin(a)),ztop+1.0) for a in ang]
            try: hulls.append(trimesh.convex.convex_hull(np.array(pts)))
            except Exception: pass
    if not hulls: return None
    return trimesh.boolean.union(hulls,engine='manifold')
