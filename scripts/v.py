import numpy as np, pyvista as pv, trimesh, sys
pv.global_theme.allow_empty_mesh=True
from PIL import Image, ImageDraw, ImageFont
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',15); Fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
exec(open('load.py').read())
COL={'Corpo1@071.stl':'#d9d4c7','Corpo1@072.stl':'#c9ced4','10_chassis_3_1':'#963cc8','10_chassis_2_1':'#5a5a5a','10_chassis_2_2':'#3d3d3d','LED_REFERENCIA':'#f5b041','Regua_baixo_central_mod':'#6b8e23','SV-30-03c soleira (degrau) (2 de 2)':'#e0e0e0','SV-30-03c soleira (degrau) (1 de 2)':'#e0e0e0','65_suporte_P01_D':'#888888','21_lateral_chassis_2_D':'#f08c14','22_lateral_placa_3_1_D':'#556b2f','22_lateral_faixa_3_1_D':'#556b2f','SV08_Espinha_L_FD_Black':'#1e6ee6','SV-30-03a batente lateral D (1 de 3)':'#bbbbbb','SV-40-01c inf +u':'#8fa6d9','SV-30-01a moldura (1 de 2)':'#c8a2e0'}
def shot(keys,cam,foc,sc,title,fn,clip=None,W=1100,H=700,op={}):
    pl=pv.Plotter(off_screen=True,window_size=(W,H)); pl.set_background('white'); leg=[]
    for k in keys:
        m=M[k]
        if clip:
            lo,hi=clip
            for ax in range(3):
                n=[0,0,0]; n[ax]=1; m=m.slice_plane(lo,n,cap=True)
                n=[0,0,0]; n[ax]=-1; m=m.slice_plane(hi,n,cap=True)
            if len(m.faces)==0: continue
        pm=pv.wrap(m); c=COL.get(k,'#999999')
        pl.add_mesh(pm,color=c,opacity=op.get(k,1.0),smooth_shading=False)
        pl.add_mesh(pm.extract_feature_edges(feature_angle=30,boundary_edges=False,non_manifold_edges=False,manifold_edges=False),color='black',line_width=1)
        leg.append((c,k))
    up=(0,0,-1) if abs(cam[1]-foc[1])>500 else (0,1,0); pl.camera_position=[cam,foc,up]; pl.enable_parallel_projection(); pl.camera.parallel_scale=sc
    pl.screenshot(fn); pl.close()
    im=Image.open(fn).convert('RGB'); O=Image.new('RGB',(W+330,H),'white'); O.paste(im,(0,0)); d=ImageDraw.Draw(O); d.text((8,6),title,fill=(0,0,0),font=F)
    for i,(c,n) in enumerate(leg): d.rectangle([W+5,10+i*18,W+18,23+i*18],fill=c,outline='black'); d.text((W+22,9+i*18),n[:40],fill=(0,0,0),font=Fs)
    O.save(fn)
K=['Corpo1@071.stl','Corpo1@072.stl','10_chassis_3_1','10_chassis_2_1','10_chassis_2_2','LED_REFERENCIA','Regua_baixo_central_mod','SV-30-03c soleira (degrau) (2 de 2)','65_suporte_P01_D','21_lateral_chassis_2_D','22_lateral_placa_3_1_D','SV-30-03a batente lateral D (1 de 3)','SV-40-01c inf +u','SV08_Espinha_L_FD_Black']
clip=(np.array([0,-5,150]),np.array([300,140,300]))
shot(K,np.array([150,60,900]),np.array([150,60,270]),90,'Frente (sem porta e sem cantoneira)','f1.png',clip)
shot(K,np.array([150,60,270])+np.array([500,350,600]),np.array([180,60,250]),110,'Iso frente-direita, de cima','f2.png',clip)
shot(K,np.array([150,60,270])+np.array([300,150,-700]),np.array([200,60,250]),110,'Por dentro (de tras)','f3.png',clip)
