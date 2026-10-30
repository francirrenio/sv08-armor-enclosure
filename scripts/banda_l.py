# banda do topo - frente: engrossa para dentro acima do acrilico (fecha o vao ate o apoio), folga 0,1
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
CT=pickle.load(open('CT.pkl','rb'))
P={pid:m for pid,lab,grp,m in pickle.load(open('parts.pkl','rb'))}
P['esp1']=CT['espinha']; P['thCantF']=CT['cant_top_F']; P['vsup1']=CT['verde_sup']
bd=CT['bandaB']
z0,z1=bd.bounds[0][2],bd.bounds[1][2]
L=B(277.4,280.8,529.4,558.25,z0,z1)
viz=[P[k] for k in ('esp1','vsup1','apB','apA','fbS','thCantF','topImp','acrL1','acHW','apHW','bandaA','acS','hwcol','fixesp') if k in P]
viz+= [trimesh.load('../ltop/'+f+'.stl') for f in ('035','047','050')]
cut=[]
for m in viz:
    if (m.bounds[0]<L.bounds[1]).all() and (m.bounds[1]>L.bounds[0]).all():
        try:
            if I(L,m).volume>1e-3: cut.append(grow(m,0.1))
        except Exception: cut.append(grow(m,0.1))
L2=D(L,*cut) if cut else L
bd2=U(bd,L2); parts=bd2.split(only_watertight=False)
bd2=max(parts,key=lambda p:p.volume)
chk={'parts':len(parts),'dv':bd2.volume-bd.volume}
for k in ('esp1','vsup1','apB','apA','fbS','thCantF','topImp','acrL1','bandaA','acS'):
    if k in P: chk[k]=I(bd2,P[k]).volume
for f in ('035','047','050'): chk[f]=I(bd2,trimesh.load('../ltop/'+f+'.stl')).volume
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}), bd2.is_volume, np.round(bd2.bounds,1).tolist(), [round(p.volume,1) for p in parts])
CT['bandaB']=bd2; pickle.dump(CT,open('CT.pkl','wb'))
