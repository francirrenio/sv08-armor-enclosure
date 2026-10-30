import trimesh, numpy as np, glob, os
D='/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/coluna_frontal_D/_mundo/'
NUM={'54_cantoneira_base_D':'01','58_coluna_inferior_lateral_frontal_D_interna':'02','58_calco_dobradica_inferior_frontal_D':'02b',
 '58_coluna_inferior_lateral_frontal_D_externa':'03','69_coluna_chapa_frontal_restaurada_D':'04','72_verde_inferior_D_encaixe':'05',
 '72_suporte_central_D_chanfro':'06','74_capa_central_D_interior_continuo':'07','58_coluna_superior_lateral_frontal_D_interna':'08',
 '58_calco_dobradica_superior_frontal_D':'08b','58_coluna_superior_lateral_frontal_D_externa':'09','75_coluna_superior_frontal_D':'10',
 '75_verde_superior_D':'11','V2_Riser_Enchimento_Canto_Black':'12','V2_Riser_Cantoneira_FD_Suporte':'13','V2_Riser_Cantoneira_FD_Capa':'14',
 'SV-30-03a_batente_lateral_D_1_de_2':'15','SV-30-03a_batente_lateral_D_2_de_2':'16'}
parts={}
for n,num in NUM.items():
    parts[f'{num}_{n}']=(trimesh.load(D+n+'.stl'), 'verde' if 'verde' in n else 'preto')
for y in (150,450):
    for k,lab in (('a_folha_porta','folha_porta'),('b_folha_fixa','folha_fixa'),('c_gaiola','gaiola')):
        m=trimesh.load(f'k1new/local_D_{k}.stl'); m.apply_translation([0,y,0])
        parts[f'17_dobradica_K1_Y{y}_{lab}']=(m,'gaiola' if k=='c_gaiola' else 'preto')
for f in glob.glob(D+'SV-40-05_fecho*.stl'):
    n=os.path.basename(f)[:-4]; parts['fecho_'+n.split('frente_')[1]]=(trimesh.load(f),'metal' if 'pino' in n else 'preto')
for f in glob.glob(D+'REF_impressora_*.stl'):
    parts['REF_'+os.path.basename(f)[:-4]]=(trimesh.load(f),'ref')
COL={'preto':[45,45,45,255],'verde':[111,138,58,255],'gaiola':[120,120,120,255],'metal':[190,190,190,255],'ref':[200,205,215,255]}
sc=trimesh.Scene()
for n,(m,c) in parts.items():
    m=m.copy(); m.visual.face_colors=COL[c]; sc.add_geometry(m,node_name=n,geom_name=n)
O='/mnt/user-data/outputs/coluna_FD/'
sc.export(O+'MONTAGEM_coluna_frontal_D.3mf')
sc.export(O+'MONTAGEM_coluna_frontal_D.glb')
allm=trimesh.util.concatenate([p[0] for k,p in parts.items() if not k.startswith('REF')])
allm.export(O+'MONTAGEM_coluna_frontal_D_sem_impressora.stl')
print(len(parts)); import pickle
pickle.dump({k:(v[1]) for k,v in parts.items()},open('asm_cols.pkl','wb'))
