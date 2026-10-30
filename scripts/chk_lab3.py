import pickle,numpy as np
exec(open('load.py').read()); exec(open('geo.py').read()); exec(open('latload.py').read())
RL=pickle.load(open('RL.pkl','rb')); FB=pickle.load(open('FB.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
O={}
for d,p in ((FB,'FB_'),(CT,'CT_')):
    for k,v in d.items(): O[p+k]=v
for k in ('placa_A','placa_B','espinha','coluna_TD_ext','cantoneira_T_L','cantoneira_F_L','verde_sup_F','verde_asa_F','verde_sup_T','verde_asa_T','verde_central'): O['RL_'+k]=RL[k]
O['apoio_tras']=L['20_apoio_traseiro_D']; O['p01']=M['65_suporte_P01_D']; O['base']=M['Corpo1@071.stl']; O['perfil']=M['Corpo1@072.stl']; O['perfT']=L['Corpo1@069.stl']
for e in ('est_tras','est_meio','est_frente'):
    m=RL[e]; print(e,np.round(m.bounds,1).tolist(),m.is_watertight, 'compr',round(m.bounds[1][2]-m.bounds[0][2],1))
    for k,v in O.items():
        try:
            if not v.is_volume: v=v.convex_hull if False else v
            x=I(m,v); 
            if x.volume>0.01: print('  x',k,round(x.volume,2))
        except Exception as ex: print('  ERR',k,str(ex)[:40])
