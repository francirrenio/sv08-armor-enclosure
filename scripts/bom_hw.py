import pickle,numpy as np,trimesh,json,sys
L=pickle.load(open('parts.pkl','rb'))
HWK=[p for p in L if p[2]=='prop' and any(w in p[1].lower() for w in ('parafus','porca','inserto','pinos')) and not p[0].endswith('_E')]
out={}
for pid,lab,g,m in HWK:
    comps=[c for c in m.split(only_watertight=False)]
    rows=[]
    for c in comps:
        if len(c.faces)<8: continue
        # principal axis via inertia of vertices
        v=c.vertices; ctr=v.mean(0); u,s,vt=np.linalg.svd(v-ctr,full_matrices=False)
        ax=vt[0]
        # snap axis to nearest global axis if close
        k=np.argmax(np.abs(ax)); 
        if abs(ax[k])>0.98: ax=np.eye(3)[k]*np.sign(ax[k])
        t=(v-ctr)@ax; L_=t.max()-t.min()
        r=np.linalg.norm((v-ctr)-np.outer(t,ax),axis=1)
        # radius profile along axis
        bins=np.linspace(t.min(),t.max(),21); prof=[]
        for i in range(20):
            sel=(t>=bins[i])&(t<=bins[i+1])
            prof.append(round(float(r[sel].max())*2,2) if sel.any() else 0)
        rows.append(dict(L=round(float(L_),2),ext=np.round(sorted(c.extents)[::-1],2).tolist(),dmax=round(float(r.max()*2),2),prof=prof,ctr=np.round(c.bounds.mean(0),1).tolist(),ax=np.round(ax,2).tolist(),vol=round(float(abs(c.volume)),1)))
    out[pid]=dict(label=lab,n=len(rows),rows=rows)
pickle.dump(out,open('bom_hw.pkl','wb'))
for pid,d in out.items():
    print(pid,d['n'],d['label'][:90])
