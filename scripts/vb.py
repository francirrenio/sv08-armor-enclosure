exec(open('v.py').read().split("K=['Corpo1@071.stl'")[0])
K=['Corpo1@071.stl','Corpo1@072.stl','SV-30-03c soleira (degrau) (2 de 2)','65_suporte_P01_D']+[k for k in M if k.startswith('Corpo1@') and k not in ('Corpo1@071.stl','Corpo1@072.stl')]
clip=(np.array([0,-5,150]),np.array([300,100,300]))
shot(K,np.array([150,45,900]),np.array([140,45,270]),75,'Base da impressora — frente (sem pecas impressas)','b1.png',clip)
shot(K,np.array([150,45,270])+np.array([450,250,650]),np.array([170,45,250]),95,'Base — iso','b2.png',clip)
clip2=(np.array([180,-5,-40]),np.array([300,100,300]))
shot(K+['21_lateral_chassis_2_D'],np.array([900,45,130]),np.array([270,45,130]),110,'Base — lateral direita (com laranja)','b3.png',clip2,op={'21_lateral_chassis_2_D':0.35})
shot(K,np.array([900,45,130]),np.array([270,45,130]),110,'Base — lateral direita (sem laranja)','b4.png',clip2)
