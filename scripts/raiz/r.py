import trimesh, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
m = trimesh.load('/root/.claude/uploads/feeeb77d-0d0c-5101-9504-0705fb8bda2b/50ea2d4a-Teste_cantoneira_suporte_preto.stl')
print(m.bounds, m.is_watertight, m.volume)
v=m.vertices-m.bounds[0]
fig=plt.figure(figsize=(18,12))
views=[(20,30),(20,120),(20,210),(20,300),(-40,45),(-40,225),(85,0),(-85,0),(0,0)]
L=np.array([0.3,0.5,0.8]);L/=np.linalg.norm(L)
for i,(e,a) in enumerate(views):
    ax=fig.add_subplot(3,3,i+1,projection='3d')
    tri=v[m.faces]; n=m.face_normals
    sh=0.3+0.7*np.clip(np.abs(n@L),0,1)
    pc=Poly3DCollection(tri,facecolors=plt.cm.gray(sh),edgecolor='none')
    ax.add_collection3d(pc); mx=v.max()
    ax.set_xlim(0,mx);ax.set_ylim(0,mx);ax.set_zlim(0,mx); ax.view_init(e,a); ax.set_title(f'e{e} a{a}'); ax.set_xlabel('X');ax.set_ylabel('Y');ax.set_zlabel('Z')
plt.tight_layout(); plt.savefig('sup.png',dpi=70)
