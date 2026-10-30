# CHAVES_RETAS: as chaves (apoios finos que entram nos bolsos da base) viram tiras retas de largura constante,
# com as pontas cortadas 4 mm: nas pontas soltas e nos encontros (fundo do V / centro do X), para encaixar mais facil
import numpy as np, pickle
from shapely.geometry import Polygon, box, LineString
from shapely.ops import unary_union
TRIM=4.0
def _pca(p):
    pts=np.array(p.exterior.coords); c=pts.mean(0); u=np.linalg.svd(pts-c)[2][0]
    if u[1]<0: u=-u
    return c,u
def _strip(p,trim_a=TRIM,trim_b=TRIM):
    c,u=_pca(p); n=np.array([-u[1],u[0]])
    pts=np.array(p.exterior.coords); t=(pts-c)@u; t0,t1=t.min(),t.max()
    T0,T1=t0,t1
    band=Polygon([c+u*(t0+trim_a)-n*30,c+u*(t1-trim_b)-n*30,c+u*(t1-trim_b)+n*30,c+u*(t0+trim_a)+n*30])
    p0=p; p=max(((p.intersection(band)).geoms if hasattr(p.intersection(band),'geoms') else [p.intersection(band)]),key=lambda q:q.area)
    pts=np.array(p.exterior.coords); t=(pts-c)@u; t0,t1=t.min(),t.max()
    mids=[]; ws=[]
    for _ in range(2):                              # eixo pelos pontos medios das secoes do meio (2 passadas)
        mids=[]; ws=[]
        for tt in np.linspace(t0+0.2*(t1-t0),t1-0.2*(t1-t0),25):
            L=LineString([c+u*tt-n*20,c+u*tt+n*20]).intersection(p)
            if L.is_empty: continue
            seg=max((L.geoms if hasattr(L,'geoms') else [L]),key=lambda q:q.length)
            q=np.array(seg.coords); mids.append(q.mean(0)); ws.append(seg.length)
        M=np.array(mids); c=M.mean(0); u=np.linalg.svd(M-c)[2][0]
        if u[1]<0: u=-u
        n=np.array([-u[1],u[0]]); t=(pts-c)@u; t0,t1=t.min(),t.max()
    w=min(ws)-0.1
    a=c+u*t0; b=c+u*t1
    st=Polygon([a-n*w/2,b-n*w/2,b+n*w/2,a+n*w/2])
    fora=st.difference(p0.buffer(0.02)).area
    while fora>0.05 and w>2.0:                       # se ainda sair da tira antiga, afina um pouco
        w-=0.1; st=Polygon([a-n*w/2,b-n*w/2,b+n*w/2,a+n*w/2]); fora=st.difference(p0.buffer(0.02)).area
    return st,round(w,2)
def chaves(G,keep):
    out=[]; log=[]
    for i,g in enumerate(G,1):
        if i not in keep: continue
        mr=g.minimum_rotated_rectangle; e=np.array(mr.exterior.coords)
        if g.area/mr.area>0.6:                      # tira simples
            s,w=_strip(g); out.append(s); log.append((i,'tira',round(w,2)))
        else:                                       # V: separa os 2 bracos no meio
            zc=0.5*(g.bounds[0]+g.bounds[2])
            for half in (g.intersection(box(-1e3,-1e3,zc,1e3)),g.intersection(box(zc,-1e3,1e3,1e3))):
                h=max((half.geoms if hasattr(half,'geoms') else [half]),key=lambda q:q.area)
                pj=np.array(h.exterior.coords); yj=pj[np.abs(pj[:,0]-zc)<1.0][:,1].mean()   # altura do encontro
                emb=yj<h.centroid.y                                                       # encontro embaixo (V) ou em cima
                for ex in np.arange(0,12.1,1.0):                                           # se o braco curva perto do encontro, corta mais
                    s,w=_strip(h,TRIM+(ex if emb else 0),TRIM+(0 if emb else ex))
                    if w>=3.2: break
                out.append(s); log.append((i,'braco',round(w,2),'corte extra',ex))
    return out,log
if __name__=='__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    G=pickle.load(open('latG.pkl','rb')); KEEPL={4,6,8,10,15,17,22,24,27,31,35,37,39,41}
    S,log=chaves(G,KEEPL); print(log)
    orig=unary_union([g for i,g in enumerate(G,1) if i in KEEPL])
    print('fora da antiga (mm2):',round(unary_union(S).difference(orig.buffer(0.02)).area,3))
    fig,ax=plt.subplots(figsize=(18,4))
    for g in [g for i,g in enumerate(G,1) if i in KEEPL]:
        a=np.array(g.exterior.coords); ax.plot(a[:,0],a[:,1],'0.6',lw=0.7)
    for s in S:
        a=np.array(s.exterior.coords); ax.plot(a[:,0],a[:,1],'r',lw=1)
    ax.set_aspect('equal'); plt.savefig('keys_retas.png',dpi=100,bbox_inches='tight')
