import trimesh, numpy as np, glob
D='/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/teste_cantoneira_central/'
for f in sorted(glob.glob(D+'Teste_cantoneira_*.stl')):
    m=trimesh.load(f); n=m.face_normals; c=m.triangles_center; a=m.area_faces
    z0=m.bounds[0][2]
    down=(n[:,2]<-0.71)&(c[:,2]>z0+0.3)   # >45deg overhang above bed
    flat=(n[:,2]<-0.99)&(c[:,2]>z0+0.3)
    bed=(n[:,2]<-0.99)&(c[:,2]<z0+0.05)
    print(f.split('/')[-1], 'faces',len(m.faces),'ext',np.round(m.extents,1),'vol',round(m.volume,1),'wt',m.is_watertight)
    print('   bed area %.0f  overhang>45 area %.1f  flat-down area %.1f' % (a[bed].sum(), a[down].sum(), a[flat].sum()))
    if down.any():
        cc=c[down]; print('   overhang z range', np.round(cc[:,2].min(),1), np.round(cc[:,2].max(),1), 'pts', np.round(cc[:6],1).tolist())
