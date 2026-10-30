import pyvista as pv
col={'a_folha_porta':'#4f4f4f','b_folha_fixa':'#4f4f4f','c_gaiola':'#8a8a8a'}
p=pv.Plotter(off_screen=True, window_size=(2400,1300), shape=(2,2)); p.set_background('white')
for r,(d,t) in enumerate((('k1old','Atual'),('k1new','Novo: cantos 5 mm + chanfro da face 1,0 x 3,5'))):
    P={k:pv.read(f'{d}/local_D_{k}.stl') for k in col}
    for i,(v,f) in enumerate([((-0.55,0.45,1.0),(240,0,292)),((1.0,0.45,-0.45),(296,0,262))]):
        p.subplot(r,i)
        for k,m in P.items(): p.add_mesh(m,color=col[k],specular=0.4,ambient=0.3)
        p.view_vector(v, viewup=(0,1,0)); p.reset_camera(); p.camera.focal_point=f; p.camera.zoom(1.6 if i==0 else 1.8)
        if i==0: p.add_text(t, font_size=14, color='black')
p.screenshot('k1_cmp3.png'); p.close()
