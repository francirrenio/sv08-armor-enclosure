# PAREDE_SOB_CANTONEIRA: as pontas das paredes da frente e de tras do top hat entram por baixo da cantoneira (ate X 242);
# a espinha da frente/de tras (peca de cima) ganha o bolso para elas, cortado com a propria parede + 0,2 de folga.
import numpy as np, pickle, json
exec(open('geo.py').read())
CT=pickle.load(open('CT.pkl','rb')); TC=pickle.load(open('TC.pkl','rb')); TF=pickle.load(open('TF.pkl','rb')); TR=pickle.load(open('TR.pkl','rb'))
pF=I(TF['parede_topo_D'],B(233.0,250.0,500,640,270,300)); pT=I(TR['parede_tras_D'],B(233.0,250.0,500,640,-300,-270))
R={'espFs':D(CT['espinha_fre_sup'],grow(pF,0.2)),'tcEFs':D(TC['esp_fre_sup'],grow(pT,0.2))}
P=pickle.load(open('parts.pkl','rb')); chk={}
for nm,w in (('tfD',TF['parede_topo_D']),('trD',TR['parede_tras_D'])):
    for pid,lab,grp,pm in P:
        if grp not in ('prop','comum','ref') or pid.endswith('_E') or pid in ('tfD','trD','espFs','tcEFs','tfE','trE'): continue
        try:
            if not (np.all(pm.bounds[0]<w.bounds[1]) and np.all(w.bounds[0]<pm.bounds[1])): continue
            x=I(w,pm).volume
        except Exception as e: x=str(e)[:20]
        if not isinstance(x,float) or x>0.05: chk[nm+'_x_'+pid]=round(x,2) if isinstance(x,float) else x
chk['tfD_x_espFs']=round(I(TF['parede_topo_D'],R['espFs']).volume,3); chk['trD_x_tcEFs']=round(I(TR['parede_tras_D'],R['tcEFs']).volume,3)
print(json.dumps({'chk':chk,'vol':{k:bool(v.is_volume) for k,v in R.items()},'lumps':{k:len(v.split(only_watertight=False)) for k,v in R.items()}}))
pickle.dump(R,open('ESPC.pkl','wb'))
