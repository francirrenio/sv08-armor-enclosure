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
def bolt(x,z):
    return U(CYL([x,YCB-5.0,z],[x,YCB,z],8.5),CYL([x,YCB,z],[x,YCB+10,z],5.0),B(x-5,x+5,625.3,628.4,z-5,z+5))
HWf=[bolt(x,ZF) for x in FX]
HWl=[U(CYL([XL,YCB-5,z],[XL,YCB,z],8.5),CYL([XL,YCB,z],[XL,YCB+10,z],5.0),B(XL-5,XL+5,625.3,628.4,z-5,z+5)) for z in LZ52+LZ55]
S['hw_frente']=U(*HWf); S['hw_lat']=U(*HWl)
LOG={k:[bool(v.is_volume),np.round(v.bounds,1).tolist()] for k,v in S.items()}
pickle.dump(S,open('SUPT.pkl','wb')); print(json.dumps(LOG))
