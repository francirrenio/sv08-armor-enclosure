import pickle,numpy as np,trimesh,sys,matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
R=pickle.load(open(sys.argv[1],'rb'))
def plot(keys,o,n,box,ax_,fn):
    fig,ax=plt.subplots(figsize=(14,8)); cm=plt.get_cmap('tab10')
    for i,k in enumerate(keys):
        s=R[k].section(plane_origin=o,plane_normal=n)
        if s is None: continue
        for j,e in enumerate(s.discrete): ax.plot(e[:,ax_[0]],e[:,ax_[1]],color=cm(i%10),lw=1.2,label=k if j==0 else None)
    ax.set_xlim(box[0],box[1]); ax.set_ylim(box[2],box[3]); ax.set_aspect('equal'); ax.grid(alpha=.3); ax.legend(fontsize=7,loc='upper left',bbox_to_anchor=(1,1)); fig.tight_layout(); fig.savefig(fn,dpi=100)
exec(sys.argv[2])
