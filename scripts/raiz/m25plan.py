import sys; sys.path.insert(0,'rev2')
RR=float(__import__("os").environ.get("RR","4.0"))
from load2 import *
import numpy as np, json, re
K=json.load(open('an2.json'))['E']
kind=[k['kind'] for k in K]
ids=[i for i,e in enumerate(E) if re.search(r'M25',e['body']+e['occ'].split('+')[-1])]
print(len(ids))
def ray_hits(o,d,cands):
    out=[]
    for j,src in cands:
        t=em(j)[0] if src=='E' else pm(j)[0]
        locs,ri,ti=t.ray.intersects_location([o],[d])
        if len(locs)==0: continue
        s=sorted(float(np.dot(l-o,d)) for l in locs)
        # pair entries/exits
        for k in range(0,len(s)-1,2): out.append((s[k],s[k+1],src,j))
    return sorted(out)
res=[]
for i in ids:
    t=em(i)[0]; b=t.bounds; ext=b[1]-b[0]; ax=int(np.argmax(ext)); c=(b[0]+b[1])/2
    # head side: compare cross-section extent near each end
    def width(at):
        o=[0,0,0]; o[ax]=1
        s=t.section(plane_origin=[*(c if True else 0)][:0] or [c[0] if ax!=0 else at, c[1] if ax!=1 else at, c[2] if ax!=2 else at],plane_normal=o)
        if s is None: return 0
        v=np.vstack([e for e in s.discrete]); oth=[k for k in range(3) if k!=ax]
        return np.ptp(v[:,oth[0]])
    w0=width(b[0][ax]+0.3); w1=width(b[1][ax]-0.3)
    head_hi = w1>w0
    d=np.zeros(3); d[ax]= -1.0 if head_hi else 1.0
    o=c.copy(); o[ax]= (b[1][ax]+30) if head_hi else (b[0][ax]-30)
    cands=[]
    for j in range(len(E)):
        if kind[j] not in ('black','green') : continue
        bb=EB[j]
        if all(bb[k]-1<=o[k]<=bb[k+3]+1 for k in range(3) if k!=ax): cands.append((j,'E'))
    for j in range(len(P)):
        bb=pm(j)[0].bounds.ravel()
        if all(bb[k]-1<=o[k]<=bb[k+3]+1 for k in range(3) if k!=ax): cands.append((j,'P'))
    oth=[k for k in range(3) if k!=ax]
    allh=[]
    for (da,db) in ((RR,0),(-RR,0),(0,RR),(0,-RR)):
        oo=o.copy(); oo[oth[0]]+=da; oo[oth[1]]+=db
        allh.append(ray_hits(oo,d,cands))
    # keep layers seen by at least 2 of 4 rays (merge by body)
    import collections
    agg=collections.defaultdict(list)
    for h in allh:
        for a,bq,s_,j in h: agg[(s_,j,round(a))].append((a,bq))
    hits=sorted([(min(x[0] for x in v),max(x[1] for x in v),k[0],k[1]) for k,v in agg.items() if len(v)>=2])
    layers=[(round(a-30,2),round(bq-30,2),E[j]['body'] if s=='E' else 'PRN',kind[j] if s=='E' else 'prn', E[j]['occ'] if s=='E' else P[j]['occ']) for a,bq,s,j in hits]
    # contiguous printed stack from the head
    stack=[]; end=None
    for l in layers:
        if l[3]=='prn': break
        if end is None or l[0]<=end+0.6:
            stack.append(l); end=max(end or 0,l[1])
        else: break
    inner=end
    lastb=[l for l in stack if l[3]=='black']
    lastb=lastb[-1] if lastb else None
    # free space test beyond the inner face: cylinder r5.5 x 3.2
    oth=[k for k in range(3) if k!=ax]
    he=float(b[1][ax] if head_hi else b[0][ax])
    p0=c.copy(); p0[ax]=he+d[ax]*inner
    cyl=mf.Manifold.cylinder(3.2,5.5,5.5,48)
    if ax==0: cyl=cyl.rotate([0,90,0])
    elif ax==1: cyl=cyl.rotate([-90,0,0])
    # cylinder extends along +axis from origin; orient by d
    if d[ax]<0: cyl=cyl.translate([-3.2 if ax==0 else 0,-3.2 if ax==1 else 0,-3.2 if ax==2 else 0])
    cyl=cyl.translate(p0.tolist())
    occ=0.0
    for j in range(len(E)):
        if j==i or kind[j] in ('hinge',): continue
        bb=EB[j]; cb=cyl.bounding_box()
        if bb[0]>cb[3] or bb[3]<cb[0] or bb[1]>cb[4] or bb[4]<cb[1] or bb[2]>cb[5] or bb[5]<cb[2]: continue
        M=em(j)[1]
        if M is None: continue
        occ+= (cyl^M).volume()
    for j in range(len(P)):
        M=pm(j)[1]
        if M is None: continue
        occ+= (cyl^M).volume()
    mode='nut' if occ<0.5 else 'pilot'
    res.append({'i':i,'name':E[i]['body'],'occ':E[i]['occ'],'axis':ax,'dir':d.tolist(),'head_hi':bool(head_hi),'center':c.round(3).tolist(),
                'head_end':he,'layers':layers,'stack':stack,'inner':inner,'lastb':lastb,'mode':mode,'occ_beyond':round(occ,2)})
json.dump(res,open('m25plan.json','w'),indent=0)
for r in res:
    print(r['name'][:34], r['occ'].split('+')[-1][:30], r['mode'], r['occ_beyond'], 'inner',r['inner'], [(l[0],l[1],l[2][:22],l[3]) for l in r['stack']])
