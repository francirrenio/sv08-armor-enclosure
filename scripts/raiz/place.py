import trimesh, numpy as np, os, json
D='/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/coluna_frontal_D/_mundo/'
O='/mnt/user-data/outputs/coluna_FD/'; os.makedirs(O,exist_ok=True)
R={'-Z':np.eye(3),'+Z':np.diag([1,-1,-1]),'-Y':np.array([[1,0,0],[0,0,-1],[0,1,0]]),'+Y':np.array([[1,0,0],[0,0,1],[0,-1,0]]),
   '-X':np.array([[0,0,-1],[0,1,0],[1,0,0]]),'+X':np.array([[0,0,1],[0,1,0],[-1,0,0]])}
P=[('01','54_cantoneira_base_D','preto','-Y','em pe; suporte so no degrau baixo (2,5 mm)'),
   ('02','58_coluna_inferior_lateral_frontal_D_interna','preto','-Z','deitada'),
   ('03','58_coluna_inferior_lateral_frontal_D_externa','preto','-X','deitada, sem suporte'),
   ('04','69_coluna_chapa_frontal_restaurada_D','preto','-Z','face interna na mesa (lingueta rente)'),
   ('05','72_verde_inferior_D_encaixe','verde','+Z','face externa na mesa; pontes de ~6 mm'),
   ('06','72_suporte_central_D_chanfro','preto','-Y','em pe na ponta, sem suporte (brim)'),
   ('07','74_capa_central_D_interior_continuo','preto','-Y','em pe; suporte no degrau baixo (3 mm)'),
   ('08','58_coluna_superior_lateral_frontal_D_interna','preto','-Z','deitada'),
   ('09','58_coluna_superior_lateral_frontal_D_externa','preto','-X','deitada, sem suporte'),
   ('10','75_coluna_superior_frontal_D','preto','-Z','face interna na mesa (lingueta rente)'),
   ('11','75_verde_superior_D','verde','+X','deitada de lado, sem suporte'),
   ('12','V2_Riser_Enchimento_Canto_Black','preto','+Z','deitada; precisa suporte'),
   ('13','V2_Riser_Cantoneira_FD_Suporte','preto','+Z','deitada, quase sem suporte'),
   ('14','V2_Riser_Cantoneira_FD_Capa','preto','-Y','em pe; suporte no degrau baixo (3 mm)'),
   ('15','SV-30-03a_batente_lateral_D_1_de_2','preto','-Z','plana; 358 mm: imprimir na diagonal da mesa'),
   ('16','SV-30-03a_batente_lateral_D_2_de_2','preto','-Z','plana')]
rows=[]
for num,n,cor,k,nota in P:
    m=trimesh.load(D+n+'.stl'); T=np.eye(4); T[:3,:3]=R[k]; m.apply_transform(T)
    m.apply_translation(-m.bounds[0])
    fn=f'{num}_{n}_{cor}.stl'; m.export(O+fn)
    rows.append((fn, np.round(m.extents,1).tolist(), round(m.volume/1000,1), nota))
import shutil
shutil.copy('/mnt/user-data/outputs/k1v3/SV-30-05_dobradica_K1_270_direita_v3_imprimir_x2.stl', O+'17_dobradica_K1_direita_v3_preto_imprimir_x2.stl')
for r in rows: print(r)
print(sum(r[2] for r in rows))
