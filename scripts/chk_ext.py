import pickle,numpy as np,json
exec(open('geo.py').read())
P=[p for p in pickle.load(open('parts.pkl','rb')) if p[2] in ('prop','comum','ref')]
U_=[p for p in P if p[0].startswith('u_') and not p[0].endswith('_E')]
res={}
def vols(m): return [c for c in m.split(only_watertight=False) if c.is_volume] if not m.is_volume else [m]
for pid,lab,grp,m in U_:
    ma=vols(m)
    for qid,lab2,g2,q in P:
        if qid==pid: continue
        if qid.startswith('u_') and qid<pid and not qid.endswith('_E'): continue
        b=q.bounds
        if not(np.all(b[0]<m.bounds[1]) and np.all(m.bounds[0]<b[1])): continue
        qa=vols(q); x=0.0
        for a in ma:
            for c in qa:
                if np.all(c.bounds[0]<a.bounds[1]) and np.all(a.bounds[0]<c.bounds[1]):
                    try: x+=I(a,c).volume
                    except Exception: pass
        if x>0.3: res[pid+' x '+qid]=round(x,1)
print(json.dumps(res,indent=0))
