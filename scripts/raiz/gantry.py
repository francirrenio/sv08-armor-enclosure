import json, numpy as np, trimesh, manifold3d as mf
E=json.load(open('aud/manifest.json')); K=json.load(open('aud_kinds.json'))
def M(i):
    x=E[i]; t=trimesh.load('aud/'+x['f'],process=True); t.merge_vertices(digits_vertex=4)
    T=np.array(x['T']).reshape(4,4); T[:3,3]*=10.0; t.apply_transform(T)
    return mf.Manifold(mf.Mesh(vert_properties=np.asarray(t.vertices,np.float32),tri_verts=np.asarray(t.faces,np.uint32)))
tol=0.3
R1=mf.Manifold.cube([2*(226.5-tol),523.5-81.0-2*tol,2*(273.5-tol)]).translate([-(226.5-tol),81.0+tol,-(273.5-tol)])
R2=mf.Manifold.cube([2*(268.5-tol),523.5-81.0-2*tol,2*(225.5-tol)]).translate([-(268.5-tol),81.0+tol,-(225.5-tol)])
R=R1+R2
out=[]
for i,x in enumerate(E):
    if K[i]=='hw': continue
    b=x['bb']
    if b[3]<-268.5 or b[0]>268.5 or b[4]<81 or b[1]>523.5 or b[5]<-273.5 or b[2]>273.5: continue
    if 'SV-30-99' in x['occ']: continue
    m=M(i); I=m^R; v=I.volume()
    if v>0.5: out.append([round(v,1),x['body'][:45],x['occ'].split('+')[-1][:30],[round(t,1) for t in np.array(I.bounding_box()).ravel()]])
for o in sorted(out,key=lambda o:-o[0]): print(o)
json.dump(out,open('gantry_res.json','w'))
