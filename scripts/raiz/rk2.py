import pyvista as pv
col={'a_folha_porta':'#4f4f4f','b_folha_fixa':'#4f4f4f','c_gaiola':'#8a8a8a'}
p=pv.Plotter(off_screen=True, window_size=(2400,1500), shape=(2,3)); p.set_background('white')
for r,(d,t) in enumerate((('k1old','Atual (chanfro 1,0)'),('k1new','Novo (cantos 5 mm a 45 graus + chanfro 1,5)'))):
    P={k:pv.read(f'{d}/local_D_{k}.stl') for k in col}
    for i,v in enumerate([(0.35,0.25,1.0),(1.0,0.3,-0.25),(0.6,0.9,0.5)]):
        p.subplot(r,i)
        for k,m in P.items(): p.add_mesh(m,color=col[k],specular=0.35,ambient=0.3)
        p.view_vector(v, viewup=(0,1,0)); p.reset_camera(); p.camera.zoom(1.35)
        if i==0: p.add_text(t, font_size=14, color='black')
p.screenshot('k1_cmp.png'); p.close()
