# TNUT_2020: pontos para aparafusar os perfis 2020 de baixo do DragonSlider nos suportes do trilho, por baixo, com porca T M5
# (o rasgo do perfil fica no centro: frente Z 255, laterais X 250; os suportes ganham uma aba ate o rasgo)
import numpy as np, trimesh, pickle, json
exec(open('geo.py').read())
TF=pickle.load(open('TF.pkl','rb'))
TD_='/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/'
L52=trimesh.load(TD_+'052.stl'); L55=trimesh.load(TD_+'055.stl')
YB0,YB1=612.0,623.4          # barra de cima dos suportes
YCB=617.0                    # fundo do rebaixo da cabeca (M5 DIN 912: cabeca 8,5 x 5)
FX=[-165.0,-40.0,40.0,165.0]; ZF=255.0           # frente: perfil Z 245-265
LZ52=[-150.0,-60.0,40.0]; LZ55=[150.0]; XL=250.0  # lateral: perfil X 240-260
def furo(m,p,axis_pts):
    x,z=p
    return D(m,CYL([x,YB0-1,z],[x,YB1+1,z],5.5),CYL([x,YB0-1,z],[x,YCB,z],9.5))
def frente(m,xs):
    for x in xs: m=U(m,B(x-9,x+9,YB0,YB1,248.5,256.3))
    for x in xs: m=furo(m,(x,ZF),None)
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
def lateral(m,zs):
    for z in zs: m=U(m,B(243.5,250.9,YB0,YB1,z-9,z+9))
    for z in zs: m=furo(m,(XL,z),None)
    return max(m.split(only_watertight=False),key=lambda q:q.volume)
S={}
S['supA']=frente(TF['ref_supA'],[x for x in FX if x<12]); S['supB']=frente(TF['ref_supB'],[x for x in FX if x>20])
S['lat52']=lateral(L52,LZ52); S['lat55']=lateral(L55,LZ55)
# EMENDA_DE_LADO: parafuso M3x20 atravessando os 2 montantes da emenda, na horizontal (cabeca rebaixada no B, porca sextavada no A)
EY=[572.0,605.0]
def hexpocket(c,axis,depth):
    n=trimesh.creation.cylinder(radius=3.3,height=depth,sections=6)
    if axis=='x': n.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
    n.apply_translation(c); return n
def axial(a,b,d): return CYL(a,b,d)
# frente: montantes A X 8,05-19,85 e B X 20,15-31,95; eixo em X, Z 260,75
ZE=260.75
for y in EY:
    S['supA']=D(S['supA'],axial([6.0,y,ZE],[21.0,y,ZE],3.4),hexpocket([8.05+1.2-0.01,y,ZE],'x',2.4))
    S['supB']=D(S['supB'],axial([19.0,y,ZE],[34.0,y,ZE],3.4),axial([28.95,y,ZE],[34.0,y,ZE],6.2))
# laterais: montantes A Z 88,05-99,85 e B Z 100,15-111,95; eixo em Z, X 255,75
XE=255.75
for y in EY:
    S['lat52']=D(S['lat52'],axial([XE,y,86.0],[XE,y,101.0],3.4),hexpocket([XE,y,88.05+1.2-0.01],'z',2.4))
    S['lat55']=D(S['lat55'],axial([XE,y,99.0],[XE,y,114.0],3.4),axial([XE,y,108.95],[XE,y,114.0],6.2))
def bolt(x,z):
    return U(CYL([x,YCB-5.0,z],[x,YCB,z],8.5),CYL([x,YCB,z],[x,YCB+10,z],5.0),B(x-5,x+5,625.3,628.4,z-2.8,z+2.8))
HWf=[bolt(x,ZF) for x in FX]
HWl=[U(CYL([XL,YCB-5,z],[XL,YCB,z],8.5),CYL([XL,YCB,z],[XL,YCB+10,z],5.0),B(XL-2.8,XL+2.8,625.3,628.4,z-5,z+5)) for z in LZ52+LZ55]
def emb(p0,ax):
    p0=np.array(p0,float); a=np.array(ax,float)
    return U(CYL(p0,p0+a*3.0,5.5),CYL(p0,p0-a*20.0,3.0))
for y in EY:
    HWf.append(emb([28.95,y,ZE],[1,0,0])); HWf.append(hexpocket([8.05+1.2,y,ZE],'x',2.2))
    HWl.append(emb([XE,y,108.95],[0,0,1])); HWl.append(hexpocket([XE,y,88.05+1.2],'z',2.2))
S['hw_frente']=U(*HWf); S['hw_lat']=U(*HWl)
LOG={k:[bool(v.is_volume),np.round(v.bounds,1).tolist()] for k,v in S.items()}
pickle.dump(S,open('SUPT.pkl','wb')); print(json.dumps(LOG))
