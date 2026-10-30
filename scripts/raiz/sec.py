import pickle,trimesh,json
exec(open('geo.py').read())
CT=pickle.load(open('CT.pkl','rb'))
for n in ('riser47','riser35'):
    r=CT[n]; print(n,r.bounds.round(1).tolist())
    for z in (100.0,-100.0,30.0,-30.0,200.0,-200.0):
        s=section_polys(r,'z',z)
        if s is None or s.is_empty: continue
        gs=s.geoms if hasattr(s,'geoms') else [s]
        print(' z',z,[ (list(map(lambda v:round(v,1),g.bounds)), len(g.interiors)) for g in gs])
for f in ('036','048','043','052','055'):
    try:
        m=trimesh.load('../ltop/'+f+'.stl'); print(f,m.bounds.round(1).tolist())
    except Exception as e: print(f,e)
print([k for k in CT.keys()])
