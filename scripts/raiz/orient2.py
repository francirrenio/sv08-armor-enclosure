import trimesh, numpy as np, glob, os, json
from trimesh.graph import connected_components
D='/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/coluna_frontal_D/_mundo/'
R={'-Z':np.eye(3),'+Z':np.diag([1,-1,-1]),'-Y':np.array([[1,0,0],[0,0,-1],[0,1,0]]),'+Y':np.array([[1,0,0],[0,0,1],[0,-1,0]]),
   '-X':np.array([[0,0,-1],[0,1,0],[1,0,0]]),'+X':np.array([[0,0,1],[0,1,0],[-1,0,0]])}
out={}
for f in sorted(glob.glob(D+'*.stl')):
    m=trimesh.load(f); n=os.path.basename(f)[:-4]; rows=[]
    for k,M in R.items():
        T=np.eye(4); T[:3,:3]=M; mm=m.copy(); mm.apply_transform(T)
        z0=mm.bounds[0][2]; nz=mm.face_normals[:,2]; c=mm.triangles_center[:,2]; a=mm.area_faces
        bed=a[(nz<-0.99)&(c<z0+0.05)].sum()
        sel=np.where((nz<-0.707)&(c>z0+0.4))[0]
        sig=0; big=[]
        if len(sel):
            adj=mm.face_adjacency; msk=np.isin(adj[:,0],sel)&np.isin(adj[:,1],sel)
            comps=connected_components(adj[msk],nodes=sel)
            for cc in comps:
                ar=a[cc].sum()
                # bridge-like (flat ceilings) vs real: measure span = min of footprint dims
                p=mm.triangles_center[cc][:,:2]; span=min(np.ptp(p[:,0]),np.ptp(p[:,1])) if len(cc)>1 else 0
                if ar>30 and span>4: sig+=ar; big.append((round(ar),round(span,1),round(float(c[cc].mean()-z0),1)))
        ext=mm.extents; h=ext[2]; fp=min(ext[0],ext[1])
        rows.append(dict(k=k,sig=round(sig),bed=round(bed),h=round(h,1),hr=round(h/max(fp,1),1),big=sorted(big,reverse=True)[:4]))
    out[n]=rows
    print(n)
    for r in sorted(rows,key=lambda r:r['sig']): print('   ',r)
json.dump(out,open('orient2.json','w'))
