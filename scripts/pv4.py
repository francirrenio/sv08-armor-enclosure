import pickle
exec(open('v.py').read().split("K=['Corpo1@071.stl'")[0])
R=pickle.load(open('R4.pkl','rb'))
for k,v in R.items(): M['R_'+k]=v
COL.update({'R_est_D':'#4a4f53','R_est_Cs':'#4a4f53','R_est_Ci':'#4a4f53'})
K=['Corpo1@071.stl','R_est_D','R_est_Cs','R_est_Ci']
clip=(np.array([40,-5,240]),np.array([260,90,300]))
shot(K,np.array([150,40,-600]),np.array([150,40,268]),75,'Apoios finos vistos por dentro da base','t4.png',clip)
clip=(np.array([40,-5,258]),np.array([260,90,300]))
shot(K,np.array([150,40,-300]),np.array([150,40,268]),70,'Apoios finos (vista de dentro, so a parede da frente da base)','t5.png',clip,op={'Corpo1@071.stl':0.55})
