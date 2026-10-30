import pickle,numpy as np,trimesh,sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
def render(m,views,fn,title=''):
    fig=plt.figure(figsize=(6*len(views),6))
    for i,(el,az) in enumerate(views):
        ax=fig.add_subplot(1,len(views),i+1,projection='3d')
        v=m.vertices[:,[2,0,1]]  # plot (z,x,y) so y is up
        tri=v[m.faces]; n=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]); n/=np.linalg.norm(n,axis=1)[:,None]+1e-12
        L=np.array([0.4,0.5,0.8]); L/=np.linalg.norm(L); s=0.35+0.65*np.clip(n@L,0,1)
        pc=Poly3DCollection(tri,facecolors=np.c_[s*0.55,s*0.6,s*0.65],edgecolors=(0,0,0,0.15),linewidths=0.2); ax.add_collection3d(pc)
        mn,mx=v.min(0),v.max(0); c=(mn+mx)/2; r=(mx-mn).max()/2
        ax.set_xlim(c[0]-r,c[0]+r); ax.set_ylim(c[1]-r,c[1]+r); ax.set_zlim(c[2]-r,c[2]+r)
        ax.view_init(el,az); ax.set_xlabel('Z'); ax.set_ylabel('X'); ax.set_zlabel('Y'); ax.set_title(f'{title} el{el} az{az}')
    plt.tight_layout(); plt.savefig(fn,dpi=80)
CT=pickle.load(open('CT.pkl','rb')); o=trimesh.load('../ltop/053_fix.stl')
render(CT['cant_top_F'],[(20,-30),(20,-150),(-25,-60)],'rc_new.png','nova')
render(o,[(20,-30),(20,-150),(-25,-60)],'rc_old.png','original')
