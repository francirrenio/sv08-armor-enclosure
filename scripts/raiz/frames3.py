import json, numpy as np, trimesh
from shapely.ops import unary_union
E=json.load(open('aud/manifest.json'))
def mesh(i):
    x=E[i]; t=trimesh.load('aud/'+x['f'],process=True); t.merge_vertices(digits_vertex=4)
    T=np.array(x['T']).reshape(4,4); T[:3,3]*=10.0; t.apply_transform(T); return t
def sect(ids, axis, pos):
    n=[0,0,0]; n[axis]=1; o=[0,0,0]; o[axis]=pos
    keep=[a for a in range(3) if a!=axis]
    polys=[]
    for i in ids:
        s=mesh(i).section(plane_origin=o,plane_normal=n)
        if s is None: continue
        p2,M=s.to_2D()
        from shapely.geometry import Polygon
        def tr(c):
            c=np.asarray(c); h=np.c_[c,np.zeros(len(c)),np.ones(len(c))]@M.T
            return h[:,keep]
        for pf in p2.polygons_full:
            polys.append(Polygon(tr(pf.exterior.coords),[tr(r.coords) for r in pf.interiors]).buffer(0))
    return unary_union(polys) if polys else None
P=json.load(open('frames_panels.json')) if False else None
import re
def find(pat): return [i for i,x in enumerate(E) if re.search(pat,x['body']) and 'SV-30-99' not in x['occ']]
panels={
 'porta_inferior_D (padrao)': (find(r'^SV-30-01a moldura$'),2,285.0,find(r'^SV-30-01b acrilico')[0]),
 'lateral_D': (find(r'SV08_Moldura_Lateral_D_'),0,285.8,find(r'V2_Acrilico_Lateral_D_REF')[0]),
 'lateral_E': (find(r'SV08_Moldura_Lateral_E_'),0,-285.8,find(r'V2_Acrilico_Lateral_E_REF')[0]),
 'traseira': (find(r'SV08_Moldura_Traseira_'),2,-288.0,find(r'V2_Acrilico_Fundo_REF')[0]),
 'ext_porta_D': (find(r'SV08_Ext_Porta_D_Moldura_Black_V2'),2,288.0,find(r'SV08_Ext_Porta_D_Acrilico')[0]),
 'ext_porta_E': (find(r'SV08_Ext_Porta_E_Moldura_Black_V2'),2,288.0,find(r'SV08_Ext_Porta_E_Acrilico')[0]),
 'ext_janela_lat_D': (find(r'SV08_Ext_Janela_Lateral_D_(Moldura|Tira)'),0,268.4,find(r'SV08_Ext_Janela_Lateral_D_Acrilico')[0]),
 'ext_janela_tras': (find(r'SV08_Ext_Janela_Traseira_(Moldura|Tira)'),2,-273.9,find(r'SV08_Ext_Janela_Traseira_Acrilico')[0]),
}
res={}
for k,(ids,ax,pos,acr) in panels.items():
    g=sect(ids,ax,pos)
    a=E[acr]['bb']; keep=[q for q in range(3) if q!=ax]
    ab=[a[keep[0]],a[keep[1]],a[keep[0]+3],a[keep[1]+3]]
    geoms=list(g.geoms) if hasattr(g,'geoms') else [g]
    from shapely.geometry import box as sbox
    rest=sbox(*g.bounds).difference(g.buffer(0.3))
    rg=list(rest.geoms) if hasattr(rest,'geoms') else [rest]
    big=max(rg,key=lambda p:p.area)
    wins=[[round(v,1) for v in big.bounds]]
    for gg in []:
        for h in gg.interiors:
            from shapely.geometry import Polygon
            hp=Polygon(h)
            if hp.area>2000: wins.append([round(v,1) for v in hp.bounds])
    # border widths: window vs frame outer, window vs acrylic
    fb=[round(v,1) for v in g.bounds]
    res[k]={'ids':ids,'frame':fb,'windows':wins,'acrylic':ab,'thick_axis':ax}
    w=wins[0]; print(k,'frame',fb,'acr',ab,'window',w,'borders(min,max sides):',[round(w[0]-fb[0],1),round(fb[2]-w[2],1),round(w[1]-fb[1],1),round(fb[3]-w[3],1)],'lip over acr:',[round(w[0]-ab[0],1),round(ab[2]-w[2],1),round(w[1]-ab[1],1),round(ab[3]-w[3],1)])
json.dump(res,open('frames_res.json','w'))
