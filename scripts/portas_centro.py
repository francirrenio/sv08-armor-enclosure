# PORTAS_CENTRO: as 2 portas ficam mais perto no meio (vao de 3 para 1 mm: o montante do meio de cada porta cresce 1 mm, de X 1,5
# para 0,5) e o batente do meio (aba de 1,8 mm atras da porta E, na porta D) passa a ir de baixo ate em cima (antes so na moldura
# de baixo). A porta E ganha o rebaixo para essa aba (folga 0,2) em vez de bater nela.
import numpy as np, pickle, json
exec(open('geo.py').read())
CT=pickle.load(open('CT.pkl','rb'))
X0=0.5
def M_(m):
    q=m.copy(); q.apply_transform(np.diag([-1,1,1,1]))
    if q.volume<0: q.invert()
    return q
R={}
for k,(y0,y1) in (('mold1',(82.0,297.0)),('mold2',(297.0,531.5))):
    m=CT['porta_'+k]
    s=section_polys(m,'x',2.0); m=U(m,prism_zy(s,X0,2.01))            # montante do meio ate X 0,5
    lap=B(-8.0,X0+0.5,y0,y1,276.0,277.8)                                # aba do batente (porta D), de ponta a ponta
    D_=U(m,lap)
    E_src=D(I(m,B(X0,300,-10,700,-400,400)),M_(B(-8.2,-X0+0.01,y0-1,y1+1,275.9,278.0)))   # porta E (antes de espelhar): sem aba, com rebaixo
    R[k]=max(D_.split(only_watertight=False),key=lambda q:q.volume); R[k+'_Esrc']=max(E_src.split(only_watertight=False),key=lambda q:q.volume)
P={p[0]:p[3] for p in pickle.load(open('parts.pkl','rb'))}
chk={}
for k in ('mold1','mold2'):
    E=M_(R[k+'_Esrc'])
    for k2 in ('mold1','mold2'):
        x=I(R[k],M_(R[k2+'_Esrc'])).volume
        if x>0.01: chk[k+'_x_'+k2+'E']=round(x,2)
    for pid in ('acr1','acr1_E','ved1','ved1_E','pux','pux_E','dobr','sol1','sol1E','tfD','tfE','p21','tfEE','tfED'):
        if pid not in P: continue
        for nm,mm in ((k,R[k]),(k+'E',E)):
            x=I(mm,P[pid]).volume
            if x>0.05: chk[nm+'_x_'+pid]=round(x,2)
chk['vao']=round(float(R['mold2'].bounds[0][0]),2)
print(json.dumps({'chk':chk,'vol':{k:bool(v.is_volume) for k,v in R.items()},'b':{k:np.round(v.bounds,1).tolist() for k,v in R.items()}}))
pickle.dump(R,open('PC.pkl','wb'))
