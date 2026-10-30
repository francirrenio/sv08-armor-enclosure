import sys, trimesh, numpy as np
for f in sys.argv[1:]:
    m = trimesh.load(f)
    print('==', f, 'tris', len(m.faces), 'watertight', m.is_watertight)
    print(' bounds', np.round(m.bounds,2).tolist(), 'extents', np.round(m.extents,2).tolist())
    parts = m.split(only_watertight=False)
    print(' bodies', len(parts))
    for p in sorted(parts, key=lambda p:-p.volume)[:6]:
        print('   body ext', np.round(p.extents,2).tolist(), 'bounds', np.round(p.bounds,1).tolist(), 'vol cm3', round(abs(p.volume)/1000,2))
    # dominant planar face areas by normal
    n = np.round(m.face_normals,2); a = m.area_faces
    from collections import defaultdict
    d = defaultdict(float)
    for k,ar in zip(map(tuple,n),a): d[k]+=ar
    top = sorted(d.items(), key=lambda kv:-kv[1])[:8]
    print(' normals by area', [(k, round(v)) for k,v in top])
