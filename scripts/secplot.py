import pickle,numpy as np,trimesh,sys,matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
L=[(p[0],p[3]) for p in pickle.load(open('parts.pkl','rb')) if p[2]!='atual' and not p[0].endswith('0')]
def plot(y,box,fn,axes=(0,2)):
    x0,x1,z0,z1=box; fig,ax=plt.subplots(figsize=(14,8)); cm=plt.get_cmap('tab20'); i=0
    for k,m in L:
        b=m.bounds
        if not(b[0][1]<y<b[1][1] and b[0][axes[0]]<x1 and b[1][axes[0]]>x0 and b[0][axes[1]]<z1 and b[1][axes[1]]>z0): continue
        s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
        if s is None: continue
        c=cm(i%20); i+=1; lab=True
        for e in s.discrete:
            ax.plot(e[:,axes[0]],e[:,axes[1]],color=c,lw=1.2,label=k if lab else None); lab=False
    ax.set_xlim(x0,x1); ax.set_ylim(z0,z1); ax.set_aspect('equal'); ax.grid(alpha=.3); ax.legend(fontsize=7,loc='upper left',bbox_to_anchor=(1,1)); ax.set_title(f'Y={y}')
    fig.tight_layout(); fig.savefig(fn,dpi=110)
exec(sys.argv[1])
