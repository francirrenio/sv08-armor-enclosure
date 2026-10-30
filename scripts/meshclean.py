import numpy as np, trimesh, manifold3d as m3
def clean(m,tol=1e-3):
    if not m.is_volume: return m
    mm=m3.Manifold(m3.Mesh(vert_properties=np.asarray(m.vertices,np.float32),tri_verts=np.asarray(m.faces,np.uint32)))
    mm=mm.simplify(tol)
    o=mm.to_mesh(); r=trimesh.Trimesh(np.asarray(o.vert_properties)[:,:3],np.asarray(o.tri_verts),process=True)
    return r
