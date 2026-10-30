import trimesh, numpy as np, os, sys
from trimesh.graph import connected_components
D='/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/coluna_frontal_D/_mundo/'
R={'-Z':np.eye(3),'+Z':np.diag([1,-1,-1]),'-Y':np.array([[1,0,0],[0,0,-1],[0,1,0]]),'+Y':np.array([[1,0,0],[0,0,1],[0,-1,0]]),
   '-X':np.array([[0,0,-1],[0,1,0],[1,0,0]]),'+X':np.array([[0,0,1],[0,1,0],[-1,0,0]])}
for n in sys.argv[1:]:
    m=trimesh.load(D+n+'.stl'); print(n, 'vol',round(m.volume,1),'wt',m.is_watertight)
    for k,M in R.items():
        T=np.eye(4); T[:3,:3]=M; mm=m.copy(); mm.apply_transform(T)
        z0=mm.bounds[0][2]; nz=mm.face_normals[:,2]; c=mm.triangles_center[:,2]; a=mm.area_faces
        bed=a[(nz<-0.99)&(c<z0+0.05)].sum()
        sel=np.where((nz<-0.707)&(c>z0+0.4))[0]; big=[]
        if len(sel):
            adj=mm.face_adjacency; msk=np.isin(adj[:,0],sel)&np.isin(adj[:,1],sel)
            for cc in connected_components(adj[msk],nodes=sel):
                ar=a[cc].sum(); p=mm.triangles_center[cc][:,:2]; span=min(np.ptp(p[:,0]),np.ptp(p[:,1])) if len(cc)>1 else 0
                if ar>15: big.append((round(ar),round(span,1),round(float(c[cc].mean()-z0),1)))
        print('  ',k,'bed',round(bed),'h',round(mm.extents[2],1),'ov',sorted(big,reverse=True)[:5])
