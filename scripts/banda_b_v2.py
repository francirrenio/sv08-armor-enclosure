# banda do topo - frente como PECA UNICA, feita direto da banda original (049):
#  - face de dentro em X 277,4 (folga 0,1 do apoio do acrilico em X 277,3)
#  - sem canal do acrilico: a banda fica toda acima da borda do acrilico (Y 529,5); a moldura de acabamento sobe ate Y 529,3
#  - recuo na ponta da frente onde a verde e a espinha sobem (Y < 538,2, Z >= 219,9)
#  - folga de 0,1 das pecas vizinhas (combine cut)
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
CT=pickle.load(open('CT.pkl','rb')); TL=pickle.load(open('TL.pkl','rb'))
o=trimesh.load('../ltop/049.stl')
bd=I(o,B(277.4,300,500,600,-300,300))
bd=D(bd,B(270,300,500,529.5,-300,300))       # SEM_CANAL: a banda comeca em Y 529,5 em toda a espessura (0,2 acima da borda do acrilico e da moldura, que sobe ate Y 529,3)
from shapely.geometry import Polygon as _P
bd=D(bd,prism_xy(_P([(282.8,529.4),(283.9,529.4),(283.9,530.5)]),-60,260))   # chanfro de 1 na aresta de baixo por fora (igual ao de cima)
bd=D(bd,B(279.0,290.0,520.0,538.2,219.9,300))
FB=pickle.load(open('FB.pkl','rb'))
viz={'acab_sup':FB['acab_sup'],'apB':TL['apoio_B'],'apA':TL['apoio_A'],'apHW':TL['apoio_hw'],'acr':TL['acrilico'],'esp':CT['espinha'],'vs':CT['verde_sup'],'cap':CT['cant_top_F'],'bandaA':TL['bandaA']}
for f in ('035','047','050','060','062'): viz[f]=trimesh.load('../ltop/'+f+'.stl')
cut=[grow(m,0.1) for k,m in viz.items() if m.is_volume and (m.bounds[0]<bd.bounds[1]).all() and (m.bounds[1]>bd.bounds[0]).all() and I(bd,grow(m,0.1)).volume>1e-3]
if cut: bd=D(bd,*cut)
parts=bd.split(only_watertight=False); bd=max(parts,key=lambda p:p.volume)
chk={k:I(bd,m).volume for k,m in viz.items() if m.is_volume}
print('cortes',len(cut),json.dumps({k:round(float(v),3) for k,v in chk.items()}), bd.is_volume, [round(p.volume,1) for p in parts], np.round(bd.bounds,2).tolist())
CT['bandaB']=bd; pickle.dump(CT,open('CT.pkl','wb'))
# banda de tras (046): mesmo desenho - peca unica, sem canal do acrilico, comeca em Y 529,5, face de dentro em X 277,4
oa=trimesh.load('../ltop/046.stl')
ba=I(oa,B(277.4,300,500,600,-300,300))
ba=D(ba,B(270,300,500,529.5,-300,300))
ba=D(ba,prism_xy(_P([(282.8,529.4),(283.9,529.4),(283.9,530.5)]),-260,40))
vizA={'molS1':FB['moldura_sup_d2'],'apA':TL['apoio_A'],'apB':TL['apoio_B'],'apHW':TL['apoio_hw'],'acr':TL['acrilico'],'bandaB':bd}
for f in ('035','047','051','054','077','078','079','080','081','082','083','084','085','086','059','061','069','060'):
    try: vizA[f]=trimesh.load('../ltop/'+f+'.stl')
    except Exception: pass
cutA=[grow(m,0.1) for k,m in vizA.items() if m.is_volume and (m.bounds[0]<ba.bounds[1]).all() and (m.bounds[1]>ba.bounds[0]).all() and I(ba,grow(m,0.1)).volume>1e-3]
if cutA: ba=D(ba,*cutA)
pa=ba.split(only_watertight=False); ba=max(pa,key=lambda p:p.volume)
chkA={k:I(ba,m).volume for k,m in vizA.items() if m.is_volume}
print('A cortes',len(cutA),json.dumps({k:round(float(v),3) for k,v in chkA.items()}), ba.is_volume, [round(p.volume,1) for p in pa], np.round(ba.bounds,2).tolist())
CT['bandaA']=ba; pickle.dump(CT,open('CT.pkl','wb'))
