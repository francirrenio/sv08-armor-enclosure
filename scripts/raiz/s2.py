import trimesh, numpy as np
m = trimesh.load('/root/.claude/uploads/feeeb77d-0d0c-5101-9504-0705fb8bda2b/50ea2d4a-Teste_cantoneira_suporte_preto.stl')
def sec(axis,val):
    o=[0,0,0];o[axis]=val;n=[0,0,0];n[axis]=1
    s=m.section(plane_origin=o,plane_normal=n)
    print('---',"XYZ"[axis],val)
    for e in s.discrete:
        pts=np.round(e[:-1],2)
        # dedupe
        print(len(pts), [tuple(p[[i for i in range(3) if i!=axis]]) for p in pts][:40])
sec(1,300); sec(1,320); sec(2,255); sec(0,250)
