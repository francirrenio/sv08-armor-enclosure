import pyvista as pv
D='/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/coluna_frontal_D/_mundo/'
col=pv.read(D+'58_coluna_inferior_lateral_frontal_D_interna.stl'); blk=pv.read(D+'58_bloco_dobradica_inferior_frontal_D.stl')
p=pv.Plotter(off_screen=True, window_size=(2400,1000), shape=(1,2)); p.set_background('white')
p.subplot(0,0); p.add_mesh(col,color='#5a5a5a',specular=.3,ambient=.3); p.add_mesh(blk.translate((0,0,14),inplace=False),color='#8a8a8a',specular=.3,ambient=.3)
p.view_vector((-1,0.15,0.9),viewup=(0,1,0)); p.reset_camera(); p.camera.zoom(1.2)
p.add_text('Coluna interna D inferior (face que encosta na impressora) + bloco da dobradica separado (cinza)',font_size=11,color='black')
p.subplot(0,1); p.add_mesh(col,color='#5a5a5a',specular=.3,ambient=.3); p.add_mesh(blk.translate((0,0,14),inplace=False),color='#8a8a8a',specular=.3,ambient=.3)
p.view_vector((1,0.3,0.8),viewup=(0,1,0)); p.reset_camera(); p.camera.zoom(1.2)
p.add_text('Lado de fora',font_size=11,color='black')
p.screenshot('col58.png'); p.close()
