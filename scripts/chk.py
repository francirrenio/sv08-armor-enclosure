import pickle, numpy as np, trimesh
exec(open('load.py').read()); exec(open('geo.py').read())
P=pickle.load(open('P.pkl','rb'))
base=M['Corpo1@071.stl']
pairs=[('10_chassis_3_1 (proposta)','Corpo1@071.stl'),('10_chassis_2_1 (proposta)','Corpo1@071.stl'),('SV-30-03c soleira (degrau) (proposta)','Corpo1@071.stl'),('21_lateral_chassis_2_D (proposta)','Corpo1@071.stl'),
 ('10_chassis_3_1 (proposta)','SV-30-03c soleira (degrau) (proposta)'),('10_chassis_3_1 (proposta)','10_chassis_2_1 (proposta)'),('10_chassis_3_1 (proposta)','SV-30-01a moldura (proposta)'),
 ('SV-30-03c soleira (degrau) (proposta)','SV-30-01a moldura (proposta)'),('SV-30-03c soleira (degrau) (proposta)','SV-30-01c vedacao EPDM (proposta)'),('10_chassis_3_1 (proposta)','LED_REFERENCIA'),('10_chassis_2_1 (proposta)','LED_REFERENCIA'),
 ('21_lateral_chassis_2_D (proposta)','65_suporte_P01_D'),('21_lateral_chassis_2_D (proposta)','Corpo1@072.stl'),('21_lateral_chassis_2_D (proposta)','22_lateral_placa_3_1_D'),('21_lateral_chassis_2_D (proposta)','SV08_Espinha_L_FD_Black'),
 ('10_chassis_3_1 (proposta)','65_suporte_P01_D'),('10_chassis_3_1 (proposta)','21_lateral_chassis_2_D (proposta)'),('10_chassis_3_1 (proposta)','10_chassis_2_2'),('SV08_Friso_Base_FD_Green (novo)','SV-30-01a moldura (proposta)'),('10_chassis_3_1 (proposta)','SV08_Espinha_L_FD_Black'),('SV-30-01c vedacao EPDM (proposta)','10_chassis_3_1 (proposta)')]
G=lambda k: P[k] if k in P else M[k]
for a,b in pairs:
    try:
        x=I(G(a),G(b)); v=x.volume if len(x.faces) else 0
    except Exception as e: v=str(e)[:40]
    print(a[:34].ljust(34),'x',b[:34].ljust(34), v if isinstance(v,str) else round(v,2), np.round(x.bounds,1).tolist() if not isinstance(v,str) and v>0.05 else '')
