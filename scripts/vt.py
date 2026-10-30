exec(open('v.py').read().split("K=['Corpo1@071.stl'")[0])
K=['Corpo1@071.stl','Corpo1@072.stl','65_suporte_P01_D']+[k for k in M if k.startswith('Corpo1@') and k not in ('Corpo1@071.stl','Corpo1@072.stl')]
clip=(np.array([0,-5,120]),np.array([300,82,300]))
pl=None
shot(K,np.array([140,900,215]),np.array([140,40,215]),95,'Base — vista de cima (Y), frente embaixo','t1.png',clip)
shot(K,np.array([140,-900,215]),np.array([140,40,215]),95,'Base — vista de baixo','t2.png',clip)
