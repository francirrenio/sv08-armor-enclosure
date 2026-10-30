import pickle
exec(open('v.py').read().split("K=['Corpo1@071.stl'")[0])
P=pickle.load(open('P.pkl','rb'))
for k,v in P.items(): M[k]=v
COL.update({'10_chassis_3_1 (proposta)':'#963cc8','10_chassis_2_1 (proposta)':'#5a5a5a','SV08_Friso_Base_FD_Green (novo)':'#3aa655','SV-30-03c soleira (degrau) (proposta)':'#7fa0d0','SV-30-01a moldura (proposta)':'#c8a2e0','SV-30-01b acrilico (proposta)':'#bfe3f5','SV-30-01c vedacao EPDM (proposta)':'#dd3333','SV-30-03a batente lateral D (proposta)':'#777777','21_lateral_chassis_2_D (proposta)':'#f08c14','M3 novos (proposta)':'#d62728'})
K=['Corpo1@071.stl','Corpo1@072.stl','10_chassis_3_1 (proposta)','10_chassis_2_1 (proposta)','10_chassis_2_2','LED_REFERENCIA','Regua_baixo_central_mod','SV08_Friso_Base_FD_Green (novo)','SV-30-03c soleira (degrau) (proposta)','SV-30-01a moldura (proposta)','SV-30-01b acrilico (proposta)','SV-30-03a batente lateral D (proposta)','65_suporte_P01_D','21_lateral_chassis_2_D (proposta)','22_lateral_placa_3_1_D','22_lateral_faixa_3_1_D','SV08_Espinha_L_FD_Black','M3 novos (proposta)']
clip=(np.array([40,-5,150]),np.array([300,140,300]))
shot(K,np.array([150,60,900]),np.array([160,65,270]),80,'Proposta — frente','p1.png',clip,op={'SV-30-01b acrilico (proposta)':0.4})
shot(K,np.array([160,60,270])+np.array([500,350,600]),np.array([180,60,250]),110,'Proposta — iso','p2.png',clip,op={'SV-30-01b acrilico (proposta)':0.4})
K2=['Corpo1@071.stl','10_chassis_3_1 (proposta)','10_chassis_2_1 (proposta)','SV-30-03c soleira (degrau) (proposta)','M3 novos (proposta)','21_lateral_chassis_2_D (proposta)']
shot(K2,np.array([160,60,270])+np.array([200,500,-700]),np.array([160,50,260]),110,'Proposta — por tras/de cima (base transparente)','p3.png',clip,op={'Corpo1@071.stl':0.25})
clip3=(np.array([255,-5,-20]),np.array([300,100,300]))
shot(['21_lateral_chassis_2_D (proposta)','M3 novos (proposta)'],np.array([-400,200,130]),np.array([275,47,130]),150,'Laranja proposta — lado de dentro','p4.png',clip3)
