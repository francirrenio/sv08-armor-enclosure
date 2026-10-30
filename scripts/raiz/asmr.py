import pyvista as pv, trimesh, numpy as np, glob, os
sc=trimesh.load('/mnt/user-data/outputs/coluna_FD/MONTAGEM_coluna_frontal_D.glb')
COL={'preto':'#3a3a3a','verde':'#6f8a3a','gaiola':'#8a8a8a','metal':'#c8c8c8','ref':'#c9ced8'}
import pickle; cols=pickle.load(open('asm_cols.pkl','rb'))
def off(n):
    p=n.split('_')[0]
    T={'01':(0,-45,0),'02':(0,0,0),'08':(0,0,0),'03':(45,0,0),'09':(45,0,0),'04':(0,0,40),'10':(0,0,40),'06':(25,0,60),
       '05':(70,0,85),'11':(70,0,85),'07':(95,0,110),'12':(0,45,30),'13':(0,45,0),'14':(45,55,45),'15':(-35,0,25),'16':(-35,0,25),
       '02b':(75,0,0),'08b':(75,0,0),'17':(115,0,40)}
    if n.startswith('fecho'): return (90,0,-50)
    if n.startswith('REF'): return (0,0,0)
    return T.get(p,(0,0,0))
def draw(fn, explode, view, title, labels):
    p=pv.Plotter(off_screen=True, window_size=(1600,2200)); p.set_background('white')
    for n,g in sc.geometry.items():
        m=pv.wrap(trimesh.Trimesh(g.vertices,g.faces))
        o=off(n) if explode else (0,0,0)
        m=m.translate(o,inplace=False)
        c=cols.get(n,'preto')
        p.add_mesh(m,color=COL[c],opacity=0.35 if c=='ref' else 1.0,specular=0.25,ambient=0.3)
        if labels and not n.startswith(('REF','fecho')) and ('folha_fixa' in n or not n.startswith('17')):
            tag=n.split('_')[0] if not n.startswith('17') else '17'
            if n.startswith('17') and 'Y150' not in n: continue
            p.add_point_labels([np.array(m.center)],[tag],font_size=26,point_size=1,shape_color='#ffe680',text_color='black',always_visible=True,shape_opacity=0.95)
    if labels:
        fc=[n for n in sc.geometry if n.startswith('fecho') and 'Y190_corpo' in n][0]
        g=sc.geometry[fc]; p.add_point_labels([np.array(g.centroid)+np.array(off(fc) if explode else (0,0,0))],['fecho'],font_size=22,point_size=1,shape_color='#cceeff',always_visible=True)
    p.view_vector(view, viewup=(0,1,0)); p.reset_camera(); p.camera.zoom(1.15)
    p.add_text(title,font_size=16,color='black')
    p.screenshot(fn); p.close()
draw('asm_montado.png',False,(1.0,0.25,1.1),'Coluna frontal D montada (impressora em cinza claro)',False)
draw('asm_explodido.png',True,(1.0,0.2,1.2),'Vista explodida - numeros = arquivos da pasta coluna_frontal_D',True)
