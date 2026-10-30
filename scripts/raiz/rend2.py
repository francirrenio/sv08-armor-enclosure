import pyvista as pv, numpy as np
D='/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/teste_cantoneira_central/_posicao_montagem/'
P={k:pv.read(D+k+'.stl') for k in ['suporte','chapa_inf','chapa_sup','verde_sup','verde_inf']}
col={'suporte':'#5a5a5a','chapa_inf':'#9a9a9a','chapa_sup':'#9a9a9a','verde_sup':'#7fa043','verde_inf':'#7fa043'}
lab={'suporte':'1. Suporte central (preto)','chapa_inf':'2. Chapa coluna de baixo','chapa_sup':'3. Chapa coluna de cima','verde_sup':'5. Verde de cima','verde_inf':'4. Verde de baixo'}
def panel(p, off, vec, title, labels, hide=(), zoom=1.0, foc=None):
    for k,m in P.items():
        if k in hide: continue
        mm=m.translate(off.get(k,(0,0,0)), inplace=False)
        p.add_mesh(mm, color=col[k], specular=0.3, ambient=0.25, diffuse=0.8)
        if labels and k in labels:
            p.add_point_labels([np.array(mm.center)+np.array(labels[k])],[lab[k]], font_size=15, point_size=1, shape_color='white', text_color='black', always_visible=True, shape_opacity=0.85)
    p.view_vector(vec, viewup=(0,1,0)); p.reset_camera()
    if foc is not None:
        p.camera.focal_point=foc; p.camera.position=tuple(np.array(foc)+np.array(vec)/np.linalg.norm(vec)*120)
    p.camera.zoom(zoom)
    p.add_text(title, font_size=13, color='black', position='upper_left')
ex={'chapa_inf':(0,-30,0),'chapa_sup':(0,30,0),'verde_sup':(0,55,40),'verde_inf':(0,-55,40)}
p=pv.Plotter(off_screen=True, window_size=(2200,1100), shape=(1,2)); p.set_background('white')
p.subplot(0,0); panel(p, ex, (-0.8,0.25,-1.0), 'Vista explodida - por dentro (lado da camara)', {k:(0,0,0) for k in P}, zoom=1.15)
p.subplot(0,1); panel(p, ex, (-0.7,0.3,1.0), 'Vista explodida - por fora', {k:(0,0,0) for k in P}, zoom=1.15)
p.screenshot('expl.png'); p.close()
# detail lower joint, assembled vs separated
p=pv.Plotter(off_screen=True, window_size=(2200,1000), shape=(1,2)); p.set_background('white')
foc=(240,296,277)
p.subplot(0,0); panel(p, {'chapa_inf':(0,-22,0)}, (-0.9,-0.4,-1.0), 'Detalhe: lingueta da chapa (cinza claro) e rebaixo do suporte', {}, hide=('verde_sup','verde_inf','chapa_sup'), zoom=1.0, foc=foc)
p.subplot(0,1); panel(p, {}, (-0.9,-0.4,-1.0), 'Encaixado', {}, hide=('verde_sup','verde_inf','chapa_sup'), zoom=1.0, foc=foc)
p.screenshot('det.png'); p.close()
