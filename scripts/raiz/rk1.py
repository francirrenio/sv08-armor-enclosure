import pyvista as pv, numpy as np, sys
d=sys.argv[1]; out=sys.argv[2]
P={k:pv.read(f'{d}/local_D_{k}.stl') for k in ['a_folha_porta','b_folha_fixa','c_gaiola']}
col={'a_folha_porta':'#555555','b_folha_fixa':'#555555','c_gaiola':'#8a8a8a'}
p=pv.Plotter(off_screen=True, window_size=(2400,900), shape=(1,3)); p.set_background('white')
for i,v in enumerate([(1,0.5,1.2),(1.2,-0.4,-0.3),(0.2,1,0.3)]):
    p.subplot(0,i)
    for k,m in P.items(): p.add_mesh(m,color=col[k],specular=0.3,ambient=0.25)
    p.view_vector(v, viewup=(0,1,0) if i<2 else (0,0,1)); p.reset_camera(); p.camera.zoom(1.3)
p.screenshot(out); p.close()
