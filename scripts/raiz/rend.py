import pyvista as pv, numpy as np
D='/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/teste_cantoneira_central/_posicao_montagem/'
P={k:pv.read(D+k+'.stl') for k in ['suporte','chapa_inf','chapa_sup','verde_sup','verde_inf']}
col={'suporte':'#2f2f2f','chapa_inf':'#4a4a4a','chapa_sup':'#4a4a4a','verde_sup':'#6f8a3a','verde_inf':'#6f8a3a'}
lab={'suporte':'Suporte central (preto)','chapa_inf':'Chapa da coluna de baixo\n(lingueta nova)','chapa_sup':'Chapa da coluna de cima\n(lingueta nova)','verde_sup':'Verde de cima','verde_inf':'Verde de baixo'}
c=np.array(P['suporte'].center)
def shot(fn, off, cam, title, labels=True, hide=()):
    p=pv.Plotter(off_screen=True, window_size=(1100,1100)); p.set_background('white')
    for k,m in P.items():
        if k in hide: continue
        mm=m.translate(off.get(k,(0,0,0)), inplace=False)
        p.add_mesh(mm, color=col[k], smooth_shading=False, specular=0.2, show_edges=False)
        if labels:
            pt=np.array(mm.center)
            p.add_point_labels([pt],[lab[k]], font_size=16, point_size=1, shape_color='white', text_color='black', always_visible=True, shape_opacity=0.8)
    p.camera_position=[tuple(c+np.array(cam)), tuple(c), (0,1,0)]
    p.add_text(title, font_size=14, color='black')
    p.enable_parallel_projection() if False else None
    p.screenshot(fn); p.close()
# exploded, seen from inside (-Z) and slightly from below/side to see the rebate
ex={'chapa_inf':(0,-35,0),'chapa_sup':(0,35,0),'verde_sup':(0,60,45),'verde_inf':(0,-60,45)}
shot('m1.png', {}, (-120,60,-170), 'Montado - visto por dentro', labels=False)
shot('m2.png', ex, (-170,40,-200), 'Explodido - visto por dentro (lado da camara)')
shot('m3.png', {}, (-150,40,200), 'Montado - visto por fora', labels=False)
# close-up of the lower joint from inside
p=pv.Plotter(off_screen=True, window_size=(1100,1000)); p.set_background('white')
for k in ['suporte','chapa_inf']:
    p.add_mesh(P[k].translate({'chapa_inf':(0,-18,0)}.get(k,(0,0,0)), inplace=False), color=col[k] if k=='suporte' else '#8a8a8a')
f=np.array([240,300,276.0])
p.camera_position=[tuple(f+np.array([-45,-35,-80])), tuple(f), (0,1,0)]
p.add_text('Detalhe: lingueta da chapa (cinza claro) entra no rebaixo do suporte', font_size=12, color='black')
p.screenshot('m4.png'); p.close()
