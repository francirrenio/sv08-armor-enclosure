import pickle,numpy as np,json,re
L=pickle.load(open('parts.pkl','rb'))
exec(open('bom.py').read().split("HW=[p for p in L if isHW(p)]")[0].split("isHW=lambda")[0].split("L=pickle.load")[0]) if False else None
HWIDS={'tcHW','tbHW','trHW','tnT','exHW','pfFchHW','pfHW','u_hwCapa','u_fixesp','fixesp','u_hwcol','u_acHW','u_fechosHW','u_tcHW','u_pfHW','u_pfFchHW','u_dobrHW','u_portaHW','u_portaIns','u_portaHWcD','u_portaHWcE','u_hw2020','tnF','tnL','tfHW','hwCapa','hwRiser','hwTopo','bandaPin','apHW','acHW','hwcol','portaHW','portaIns','portaHWcD','portaHWcE','dobrHW','fechosHW','hw1'}
base=lambda k: k[:-2] if k.endswith('_E') else k
P={p[0]:p for p in L if p[2]=='prop'}
rows=[]
for k,p in P.items():
    if k.endswith('_E') or base(k) in HWIDS: continue
    m=p[3]; comps=[c for c in m.split(only_watertight=False) if abs(c.volume)>150]
    sizes=sorted([np.round(sorted(c.extents)[::-1],0).astype(int).tolist() for c in comps],reverse=True)
    rows.append(dict(id=k,label=p[1],n=len(comps),E=(k+'_E') in P,sizes=sizes,vol=round(sum(abs(c.volume) for c in comps)/1000,1)))
json.dump(rows,open('bom_parts.json','w'),ensure_ascii=False,indent=0)
for r in rows: print(r['id'],'|',r['n'],'| E' if r['E'] else '|  ','|',r['sizes'][:6],'|',r['label'][:70])
