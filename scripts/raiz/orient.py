import trimesh, numpy as np, glob, os, json
D='/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/coluna_frontal_D/_mundo/'
R={'-Z':np.eye(3),'+Z':np.diag([1,-1,-1]),'-Y':np.array([[1,0,0],[0,0,-1],[0,1,0]]),'+Y':np.array([[1,0,0],[0,0,1],[0,-1,0]]),
   '-X':np.array([[0,0,-1],[0,1,0],[1,0,0]]),'+X':np.array([[0,0,1],[0,1,0],[-1,0,0]])}
# R[k] maps world so that world direction k points down (-Z)
res={}
for f in sorted(glob.glob(D+'*.stl')):
    m=trimesh.load(f); n=os.path.basename(f)[:-4]
    rows=[]
    for k,M in R.items():
        T=np.eye(4); T[:3,:3]=M; mm=m.copy(); mm.apply_transform(T)
        # sanity: k direction must map to -Z
        z0=mm.bounds[0][2]; nz=mm.face_normals[:,2]; c=mm.triangles_center[:,2]; a=mm.area_faces
        bed=a[(nz<-0.99)&(c<z0+0.05)].sum()
        ov=a[(nz<-0.707)&(c>z0+0.4)].sum()
        rows.append((k,round(ov,1),round(bed,1),np.round(mm.extents,1).tolist()))
    res[n]=rows
    best=sorted(rows,key=lambda r:(r[1]-0.02*r[2]))
    print(n, 'vol',round(m.volume/1000,1),'cm3 ext',np.round(m.extents,1).tolist())
    for r in sorted(rows,key=lambda r:r[1]): print('   ',r)
json.dump(res,open('orient.json','w'))
