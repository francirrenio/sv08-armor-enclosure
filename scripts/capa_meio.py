# CANTONEIRA DO MEIO (74_capa_central_D): 1 parafuso no centro de cada aba
#  - sai o furo da borda da lateral (Z 232), que caia em cima da cabeca do parafuso da espinha (Y 322,8 / Z 228)
#  - lateral: M3x16 cabeca abaulada no centro da face plana (Z 255,6), atravessa a verde 72 e aperta numa porca embutida na espinha (por dentro)
#  - frente: M3x16 cabeca abaulada no centro da face plana (X 261,55), atravessa a verde 72 e aperta num inserto M3 na espinha
#  Refeito limpo: a regiao dos furos antigos e preenchida com o perfil da propria peca (secao sem furo, extrudada em Y) e os furos novos sao cortados nela.
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
from shapely.geometry import Polygon
from shapely.ops import unary_union
CF=pickle.load(open('CF.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
YS=324.0; ZL=255.6; XF=261.55; YFX=322.8
def secy(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float))
    return unary_union([p for p in p2.polygons_full])
def ext_xz(poly,y0,y1):
    gs=poly.geoms if hasattr(poly,'geoms') else [poly]; ms=[]
    for g in gs:
        m=trimesh.creation.extrude_polygon(g,y1-y0)
        m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
        if m.volume<0: m.invert()
        ms.append(m)
    return U(*ms)
def preenche(m,yref,y0,y1,*caixas):
    pr=ext_xz(secy(m,yref),y0,y1)
    return U(m,*[I(pr,c) for c in caixas])
def hexX(x0,x1,y,z,s=5.5+0.3):
    r=s/np.sqrt(3); pts=[(y+r*np.cos(a),z+r*np.sin(a)) for a in np.radians([0,60,120,180,240,300])]
    m=trimesh.creation.extrude_polygon(Polygon(pts),x1-x0)          # (y,z) extrudado em X
    m.apply_transform(np.array([[0,0,1,x0],[1,0,0,0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m

# 1) cantoneira do meio
c=CF['capa_74']
c=preenche(c,310.0,319.0,329.5,B(283.9,293.6,319.0,329.5,220.5,265.0),B(240.0,251.0,319.0,329.5,286.0,295.6))
c=D(c,CYL([283.0,YS,ZL],[294.0,YS,ZL],3.4),CYL([290.9,YS,ZL],[294.0,YS,ZL],6.2),        # lateral: furo + rebaixo da cabeca
      CYL([XF,YS,285.0],[XF,YS,296.0],3.4),CYL([XF,YS,293.1],[XF,YS,296.0],6.2))        # frente
CF['capa_74']=max(c.split(only_watertight=False),key=lambda p:p.volume)
# 2) verde 72 (so ate Y 326)
v=CT['verde_72']
v=preenche(v,318.0,319.0,326.0,B(279.0,284.5,319.0,326.0,256.0,263.5))
v=D(v,CYL([278.0,YS,ZL],[285.0,YS,ZL],3.4),CYL([XF,YS,280.0],[XF,YS,287.0],3.4))
CT['verde_72']=max(v.split(only_watertight=False),key=lambda p:p.volume)
# 3) espinha: furo antigo da capa (Z 232), furo/porca antigos (Z 259,7) e a cabeca do parafuso da espinha refeitos
e=CT['espinha']
e=preenche(e,316.0,319.0,329.0,B(272.0,284.5,319.0,329.0,224.0,264.0))
e=D(e,CYL([270.0,YFX,228.0],[290.0,YFX,228.0],3.4),CYL([280.6,YFX,228.0],[290.0,YFX,228.0],6.2),   # parafuso da espinha no perfil (cabeca embutida)
      CYL([272.0,YS,ZL],[285.0,YS,ZL],3.4),hexX(272.0,278.5,YS,ZL),                                   # lateral: porca M3 embutida por dentro
      CYL([XF,YS,276.6],[XF,YS,283.0],4.2))                                                           # frente: inserto M3 (D 4,2)
CT['espinha']=max(e.split(only_watertight=False),key=lambda p:p.volume)
# 4) ferragens
def btn(p,axis,Lg):   # ISO7380 M3: cabeca D5,7 x 1,65
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*1.65,5.7),CYL(p,p-a*Lg,3.0))
hw=[btn([290.9,YS,ZL],[1,0,0],16.0),btn([XF,YS,293.1],[0,0,1],16.0),
    D(hexX(275.9,278.3,YS,ZL,5.5),CYL([275,YS,ZL],[279,YS,ZL],3.0)),
    D(CYL([XF,YS,277.8],[XF,YS,281.8],4.2),CYL([XF,YS,277],[XF,YS,282.6],3.0))]
CT['hw_capa74']=trimesh.util.concatenate(hw)
chk={}
pr=[('capa','esp',CF['capa_74'],CT['espinha']),('capa','v72',CF['capa_74'],CT['verde_72']),('v72','esp',CT['verde_72'],CT['espinha']),
    ('capa','vsup',CF['capa_74'],CT['verde_sup']),('fix','capa',CF['fix_espinha'],CF['capa_74']),('fix','v72',CF['fix_espinha'],CT['verde_72'])]
for a,b,ma,mb in pr: chk[a+'_x_'+b]=I(ma,mb).volume
for i,h in enumerate(hw[:2]):
    chk['para%d_x_capa'%i]=I(h,CF['capa_74']).volume; chk['para%d_x_v72'%i]=I(h,CT['verde_72']).volume; chk['para%d_x_esp'%i]=I(h,CT['espinha']).volume
chk['ok']=float(all(m.is_volume for m in (CF['capa_74'],CT['verde_72'],CT['espinha'])))
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}))
pickle.dump(CF,open('CF.pkl','wb')); pickle.dump(CT,open('CT.pkl','wb'))
