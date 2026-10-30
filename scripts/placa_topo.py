# PLACA_TOPO: a travessa de cima da frente da impressora tem um rebaixo (aba Y 523,5-529,5, face em Z 270) atras da faixa de
# cima das portas de baixo, 3,5 mm abaixo da face da impressora (Z 273,5). Uma placa preta reta por porta preenche esse rebaixo
# (Y 523,7-529,3, Z 270-273,5), com a frente alinhada a face da impressora, para receber a espuma de vedacao onde o acrilico
# apoia. Fixacao por dentro: 3 furos cegos de 2,5 mm por tras (Z 270-273, frente lisa), alinhados aos furos que a aba ja tem
# (X 4 / 201,5 / 211,5); o parafuso vem por dentro da impressora, pela aba.
import numpy as np, pickle, json, trimesh
exec(open('geo.py').read())
P={p[0]:p[3] for p in pickle.load(open('parts.pkl','rb'))}
Z0,Z1=270.0,273.5
HOL=[(4.0,526.15),(201.5,526.3),(211.5,526.3)]
pl=D(B(0.2,222.1,523.7,529.3,Z0,Z1),*[CYL([x,y,Z0-1],[x,y,Z1-0.5],2.5) for x,y in HOL])
R={'placaTopo':pl}
chk={}
for k,m in R.items():
    for q in ('trvF','perfil','topImp','tfED','tfEE','acr1','mold2','reguaPortaB','dobr','espFs','thCantF'):
        Q=P[q]; b=Q.bounds
        if np.any(b[0]>m.bounds[1]) or np.any(m.bounds[0]>b[1]): continue
        v=I(m,Q).volume
        if v>0.01: chk[k+' x '+q]=round(v,2)
print(json.dumps({'chk':chk,'vol':{k:bool(v.is_volume) for k,v in R.items()},'b':{k:np.round(v.bounds,2).tolist() for k,v in R.items()}}))
pickle.dump(R,open('PTOPO.pkl','wb'))
