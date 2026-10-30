import json, numpy as np, trimesh
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union, polygonize
E=json.load(open('aud/manifest.json'))
def mesh(i):
    x=E[i]; t=trimesh.load('aud/'+x['f'],process=True); t.merge_vertices(digits_vertex=4)
    T=np.array(x['T']).reshape(4,4); T[:3,3]*=10.0; t.apply_transform(T); return t
def sect(ids, axis, pos):
    n=[0,0,0]; n[axis]=1; o=[0,0,0]; o[axis]=pos
    polys=[]
    keep=[a for a in range(3) if a!=axis]
    for i in ids:
        sg=trimesh.intersections.mesh_plane(mesh(i),n,o)
        if len(sg)==0: continue
        lines=[ [tuple(np.round(s[0][keep],4)),tuple(np.round(s[1][keep],4))] for s in sg]
        from shapely.geometry import MultiLineString
        ps=list(polygonize(MultiLineString(lines)))
        # even-odd: union of polygons minus holes via symmetric difference
        g=None
        for p in sorted(ps,key=lambda p:-p.area):
            g=p if g is None else g.symmetric_difference(p)
        if g is not None: polys.append(g)
    return unary_union(polys) if polys else None
panels={
 'lateral_D': ([494,495,496,497],0,285.8,574),
 'traseira': ([126,127,128,129],2,-288.0,292),
 'ext_porta_D': ([158],2,288.0,159),
 'ext_janela_lat_D': ([832,833,818,819],0,268.4,817),
 'ext_janela_tras': ([866,867,852,853],2,-273.9,851),
 'porta_inferior_D_ref': ([None],2,284.0,417),
}
res={}
for k,(ids,ax,pos,acr) in panels.items():
    if ids==[None]:
        import re
        ids=[i for i,x in enumerate(E) if x['body']=='SV-30-01a moldura' and 'SV-30-01 Porta' in x['occ']]
    g=sect(ids,ax,pos)
    a=E[acr]['bb']; keep=[q for q in range(3) if q!=ax]
    ab=[a[keep[0]],a[keep[1]],a[keep[0]+3],a[keep[1]+3]]
    holes=[]
    geoms=g.geoms if hasattr(g,'geoms') else [g]
    for gg in geoms:
        for h in gg.interiors: holes.append(Polygon(h).bounds)
    res[k]={'frame_bounds':[round(v,1) for v in g.bounds],'windows':[[round(v,1) for v in h] for h in holes],'acrylic':ab,'area':round(g.area)}
    print(k,res[k])
json.dump(res,open('frames_res.json','w'))
