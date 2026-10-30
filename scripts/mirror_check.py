import pickle,numpy as np,trimesh
exec(open('geo.py').read())
P={pid:(lab,grp,m) for pid,lab,grp,m in pickle.load(open('parts.pkl','rb'))}
FRONT=['esp1','esp1s','espF','espFs','v72','vsup1','capa74','hwCapa','fbI','fbS','fixesp','hwcol','thCantF','thSupF','hwTopo','riser47','molAl47','bandaB','apB','acI','acS','acHW','cantF']
REAR_OLD=['colTD','thCantT','thSupT','colT1','molS1','mollat1','riser35','molAl35','bandaA','apA','cantT']
ENV=['base','perfT','apT','topImp','hw','pLA','eLT','v24','v15','trD','trE','trL','trH','trT','trA','trHW','dsF','fechos','fechosHW','hw1','hwRiser','apHW','acrL1']
def mz(m):
    q=m.copy(); q.apply_transform(np.diag([1,1,-1,1]))
    if q.is_volume and q.volume<0: q.invert()
    return q
MIR={k:mz(P[k][2]) for k in FRONT if k in P}
# so a metade de tras de pecas que atravessam o centro
for k in ('riser47','molAl47','bandaB','apB','acI','acS','acHW'):
    pass
print('pecas espelhadas:',list(MIR.keys()))
for k,m in MIR.items():
    for e in ENV:
        if e not in P: continue
        v=P[e][2]
        try:
            b=v.bounds
            if np.any(b[0]>m.bounds[1]) or np.any(b[1]<m.bounds[0]): continue
            x=I(m,v).volume
        except Exception as ex: x='ERR'
        if x=='ERR' or x>0.5: print(f'{k:8s} x {e:8s}',x if x=='ERR' else round(x,1))
# comparacao p01 x apT espelhado
p01=P['p01'][2]; apT=P['apT'][2]
print('p01 vs mirror(apT): vol',round(p01.volume),round(apT.volume),' xor~', round(p01.volume+apT.volume-2*I(p01,mz(apT)).volume,1))
print('perfil vs mirror(perfT):', round(P['perfil'][2].volume+P['perfT'][2].volume-2*I(P['perfil'][2],mz(P['perfT'][2])).volume,1))
