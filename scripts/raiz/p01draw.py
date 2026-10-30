import pyvista as pv, trimesh, numpy as np
D='/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/coluna_frontal_D/_mundo/'
E=trimesh.load('/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/auditoria3/b0159.stl')
print(np.round(E.bounds,1).tolist())
P=E.copy(); P.apply_transform(np.diag([-1,1,1,1])); P.fix_normals()
def L(n): return trimesh.load(D+n+'.stl')
col=L('58_coluna_inferior_lateral_frontal_D_interna')
cut=trimesh.creation.box(bounds=[[268.3,81.05,231.7],[273.0,136.05,249.8]])
try:
    import manifold3d
    col2=col.difference(cut)
except Exception as e:
    print('bool fail',e); col2=col
ch=L('69_coluna_chapa_frontal_restaurada_D'); ca=L('54_cantoneira_base_D')
refs=[trimesh.load(D+f'REF_impressora_{i}.stl') for i in range(12)]
ref=trimesh.util.concatenate([r for r in refs])
ref=ref.slice_plane([0,180,0],[0,-1,0]) if True else ref
def cylZ(x,y,z0,z1,r=1.5): c=trimesh.creation.cylinder(r,abs(z1-z0)); c.apply_translation([x,y,(z0+z1)/2]); return c
def cylX(y,z,x0,x1,r=1.5): c=trimesh.creation.cylinder(r,abs(x1-x0)); c.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0])); c.apply_translation([(x0+x1)/2,y,z]); return c
scr_imp=[cylZ(234.5,60,262,281,2.6), cylX(60,240.5,262,286,2.6)]
scr_ch=[cylZ(245,110,268,284), cylZ(238,118,268,284)]
scr_ca=[cylZ(246,17,270,296), cylZ(246,64,270,296), cylX(17,259.7,268,294), cylX(64,259.7,268,294)]
def tm2pv(m): return pv.wrap(m)
def draw(fn, ex):
    off={'P':(0,0,0),'col':(45,0,0) if ex else (0,0,0),'ch':(0,0,55) if ex else (0,0,0),'ca':(0,-45,45) if ex else (0,0,0)}
    p=pv.Plotter(off_screen=True,window_size=(1500,1400)); p.set_background('white')
    p.add_mesh(tm2pv(ref),color='#b9c2c8',opacity=0.25)
    p.add_mesh(tm2pv(P),color='#d9822b',specular=.3,ambient=.3)
    p.add_mesh(tm2pv(col2).translate(off['col'],inplace=False),color='#4a5054',specular=.3,ambient=.3)
    p.add_mesh(tm2pv(cut).translate(off['col'],inplace=False),color='#e04040',opacity=0.45)
    p.add_mesh(tm2pv(ch).translate(off['ch'],inplace=False),color='#5b6266',opacity=0.95 if ex else 0.55,specular=.3,ambient=.3)
    p.add_mesh(tm2pv(ca).translate(off['ca'],inplace=False),color='#5b6266',opacity=0.95 if ex else 0.4,specular=.3,ambient=.3)
    for s in scr_imp: p.add_mesh(tm2pv(s),color='#1f6fd1')
    for s in scr_ch: p.add_mesh(tm2pv(s).translate(off['ch'],inplace=False),color='#2aa05a')
    for s in scr_ca: p.add_mesh(tm2pv(s).translate(off['ca'],inplace=False),color='#9b59b6')
    labs=[((249,70,276),'P01 (novo no lado D)'),((236,60,282),'2 parafusos da impressora (Y 60)'),
          ((240,114,286 + (55 if ex else 0)),'chapa 04 -> P01: 2x M3 (Y 110/118)'),
          ((270,108,245),'trecho da coluna 02 removido (vermelho)'),
          ((262,40 - (45 if ex else 0),296+(45 if ex else 0)),'cantoneira 01 -> P01: 4x M3x16 (Y 17/64)')]
    for pt,t in labs:
        q=np.array(pt,float)
        if 'removido' in t: q=q+np.array(off['col'])
        p.add_point_labels([q],[t],font_size=20,point_size=8,point_color='black',shape_color='#fff4c2',always_visible=True,shape_opacity=0.95)
    p.view_vector((1.0,0.35,1.25),viewup=(0,1,0)); p.reset_camera(); p.camera.focal_point=(250,80,255); p.camera.zoom(1.5)
    p.add_text('Canto inferior D - '+('explodido' if ex else 'montado'),font_size=16,color='black')
    p.screenshot(fn); p.close()
draw('p01_montado.png',False); draw('p01_explodido.png',True)
