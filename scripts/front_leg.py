import numpy as np, trimesh, pickle, json
exec(open('geo.py').read())
from shapely.geometry import Polygon, box
_G={}; exec(open('esb/geom_lat.py').read(),_G); rc=_G['rc']
R=pickle.load(open('R4.pkl','rb')); RL=pickle.load(open('RL.pkl','rb'))
T60=np.tan(np.radians(60))
# perna de baixo da cantoneira na FRENTE (menor que a da lateral): face no plano da aba da frente (Z 295,5), chanfro 5,5 igual
ZP,ZC=284.0,295.5
XI=234.0; YL=18.0; XT=222.0
p=Polygon([(250.0,2.0),(250.0,94.0),(XI,94.0),(XI,YL),(XT,YL),(XT-(YL-2.0)/T60,2.0)])
p=rc(p.buffer(8.0,join_style=1,resolution=16).buffer(-8.0,join_style=1,resolution=16))      # canto de dentro R 8, cantos de fora R 2,5
p=p.intersection(box(150,2.0,XI+6.0,40.0))
leg=prism_xy(p,ZP,ZC); leg=chamfer_top(leg,'z',ZC,5.5,n=18)
cF=U(RL['cantoneira_F_L'],leg)
mol=D(R['moldura_led'],prism_xy(p.buffer(4.0,join_style=1,resolution=16).union(box(XI-4.0,0,300,100)),279.0,290.0))   # verde do LED contorna a perna (vao 4)
out={'cantoneira_F_L2':cF,'moldura_led2':mol,'perna_frente':leg}
log={'perna_bb':np.round(leg.bounds,1).tolist(),'mol_bb':np.round(mol.bounds,1).tolist(),'wt':[cF.is_watertight,mol.is_watertight],
     'interf_roxa':round(I(leg,R['placa_roxa']).volume,2),'interf_mol':round(I(leg,mol).volume,2),'interf_verde_topo':round(I(leg,R['verde_topo']).volume,2)}
pickle.dump(out,open('RF.pkl','wb')); print(json.dumps(log))
