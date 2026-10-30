# VINCOS_TRAS: os 3 vincos verticais do centro (X -6 / 0 / +6, V de 2 mm x 1 mm), que ja descem pela moldura do painel do fundo,
# continuam na parede preta de tras do top hat (de Y 529,5 ao topo, interrompidos so no trilho) e na placa preta central da base.
# A emenda da parede (X 0) fica no fundo do vinco do meio.
import numpy as np, pickle, trimesh
exec(open('geo.py').read())
from shapely.geometry import Polygon
TR=pickle.load(open('TR.pkl','rb')); TB=pickle.load(open('TB.pkl','rb'))
def vinco(x,y0,y1,zf=-286.0):
    m=trimesh.creation.extrude_polygon(Polygon([(x-1.6,zf-0.6),(x+1.6,zf-0.6),(x,zf+1.0)]),y1-y0)   # (x,z) extrudado em Y
    m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
VW=[vinco(x,y0,y1) for x in (-6.0,0.0,6.0) for (y0,y1) in ((520.0,539.9),(554.1,640.0))]
VB=[vinco(x,-5.0,86.0) for x in (-6.0,0.0,6.0)]
print({k:np.round(TB[k].bounds,1).tolist() for k in TB if 'placa' in k or 'PC' in k or 'central' in k})
R={'trE':D(TR['parede_tras_E'],*VW),'trD':D(TR['parede_tras_D'],*VW)}
k=[k for k in TB if 'central' in k and 'placa' in k] or [k for k in TB if k.lower().startswith('placa')]
print('chave base',k)
R['tbPC']=D(TB[k[0]],*VB)
print({kk:(bool(v.is_volume),round(float(v.volume),1)) for kk,v in R.items()})
pickle.dump(R,open('VT.pkl','wb'))
