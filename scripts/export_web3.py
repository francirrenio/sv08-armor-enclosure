import pickle, json, gzip, base64, numpy as np, trimesh
exec(open('load.py').read()); exec(open('geo.py').read())
P=pickle.load(open('P.pkl','rb')); Q=pickle.load(open('Q.pkl','rb')); R=pickle.load(open('R.pkl','rb'))
def clipm(m,lo,hi):
    for ax in range(3):
        n=[0,0,0]; n[ax]=1; m=m.slice_plane([lo[0],lo[1],lo[2]],n,cap=True)
        n=[0,0,0]; n[ax]=-1; m=m.slice_plane([hi[0],hi[1],hi[2]],n,cap=True)
    return m
LO=np.array([-20,-5,90]); HI=np.array([300,200,300])
parts=[]  # (id, label, group, color, mesh, mode, extra)
def add(pid,label,grp,col,m,mode='ambos',hint=''):
    parts.append(dict(id=pid,label=label,grp=grp,col=col,mesh=m,mode=mode,hint=hint))
# referencia
add('base','Base da impressora (STEP)','ref','#cfc8b8',clipm(M['Corpo1@071.stl'],LO,HI))
add('perfil','Perfil de canto (STEP)','ref','#b7bec7',clipm(M['Corpo1@072.stl'],LO,HI))
# comuns
add('p01','65_suporte_P01_D','comum','#8a8f96',M['65_suporte_P01_D'])
add('espinha','SV08_Espinha_L_FD_Black','comum','#2f6fd6',clipm(M['SV08_Espinha_L_FD_Black'],LO,HI))
add('c22','10_chassis_2_2 (baixo central)','atual','#3b3d40',M['10_chassis_2_2'],'atual')
add('led','LED (referencia)','comum','#f2b13c',clipm(M['LED_REFERENCIA'],LO,HI))
add('regua','Regua_baixo_central_mod (verde)','comum','#35a853',clipm(M['Regua_baixo_central_mod'],LO,HI))
add('molled','Moldura_LED_D_mod (verde do LED)','comum','#35a853',M['Moldura_LED_D_mod'])
add('placa','22_lateral_placa_3_1_D','comum','#4f6f2a',M['22_lateral_placa_3_1_D'])
add('faixa','22_lateral_faixa_3_1_D','comum','#4f6f2a',M['22_lateral_faixa_3_1_D'])
add('mollat','Moldura painel lateral (SV-40-01)','comum','#8fa6d9',clipm(M['SV-40-01c inf +u'],LO,HI))
hw=[k for k in M if k.startswith(('M3_22_','M3_lateral_apoio','46_M3x10','46_porca'))]
add('hw','Parafusos e porcas existentes','comum','#c43b3b',U(*[M[k] for k in hw]))
# atual
add('roxa0','10_chassis_3_1 (roxa)','atual','#8e3bc4',M['10_chassis_3_1'],'atual')
add('cen0','10_chassis_2_1 (central)','atual','#55585c',M['10_chassis_2_1'],'atual')
add('lar0','21_lateral_chassis_2_D (laranja)','atual','#ee8a1c',M['21_lateral_chassis_2_D'],'atual')
add('sol0','Soleira / degrau (SV-30-03c 2/2)','atual','#7fa0d0',M['SV-30-03c soleira (degrau) (2 de 2)'],'atual')
add('mold0','Porta direita - moldura','atual','#c6a3df',clipm(M['SV-30-01a moldura (1 de 2)'],LO,HI),'atual')
add('acr0','Porta direita - acrilico','atual','#bfe3f5',clipm(M['SV-30-01b acrilico 225x453'],LO,HI),'atual')
add('ved0','Porta direita - vedacao','atual','#cc3b3b',clipm(M['SV-30-01c vedacao EPDM 8x2'],LO,HI),'atual')
add('bat0','Batente lateral da porta','atual','#7a7a7a',clipm(M['SV-30-03a batente lateral D (1 de 3)'],LO,HI),'atual')
# proposta
EST='#4a4f53'; PRE='#1e2123'; VER='#35a853'
add('pR','Roxa - placa preta (mesmo desenho)','prop',PRE,R['placa_roxa'],'prop')
add('gV','Detalhe verde na parte que subiu','prop',VER,R['verde_topo'],'prop')
add('p21','Central de cima - placa preta','prop',PRE,R['placa_21'],'prop')
add('p22','Central de baixo - placa preta','prop',PRE,R['placa_22'],'prop')
add('pL','Lateral - placa preta (desenho da laranja)','prop',PRE,R['placa_lateral'],'prop')
add('eD','Estrutura frente D (escondida)','prop',EST,R['est_D'],'prop')
add('eCs','Estrutura central cima (escondida)','prop',EST,R['est_Cs'],'prop')
add('eCi','Estrutura central baixo (escondida)','prop',EST,R['est_Ci'],'prop')
add('eCsL','Estrutura central cima E (espelho)','prop',EST,clipm(R['est_CsL'],LO,HI),'prop')
add('eCiL','Estrutura central baixo E (espelho)','prop',EST,clipm(R['est_CiL'],LO,HI),'prop')
add('eL','Estrutura lateral (escondida)','prop',EST,R['est_lateral'],'prop')
add('sol1','Soleira / degrau - proposta','prop','#7fa0d0',R['soleira'],'prop')
add('mold1','Porta direita - moldura (mais baixa)','prop','#c6a3df',clipm(P['SV-30-01a moldura (proposta)'],LO,HI),'prop')
add('acr1','Porta direita - acrilico (mais baixo)','prop','#bfe3f5',clipm(P['SV-30-01b acrilico (proposta)'],LO,HI),'prop')
add('ved1','Porta direita - vedacao','prop','#cc3b3b',clipm(P['SV-30-01c vedacao EPDM (proposta)'],LO,HI),'prop')
add('bat1','Batente lateral da porta','prop','#7a7a7a',clipm(P['SV-30-03a batente lateral D (proposta)'],LO,HI),'prop')
add('hw1','Parafusos M3','prop','#e0402f',R['ferragens'],'prop')
meta=[]; bufs=[]; off=0
for p in parts:
    m=p['mesh']; v=np.asarray(m.vertices,np.float32); f=np.asarray(m.faces,np.uint32).ravel()
    vb=v.tobytes(); fb=f.tobytes()
    meta.append(dict(id=p['id'],label=p['label'],grp=p['grp'],col=p['col'],mode=p['mode'],vo=off,vn=len(v),fo=off+len(vb),fn=len(f)))
    bufs+= [vb,fb]; off+=len(vb)+len(fb)
blob=b''.join(bufs)
gz=gzip.compress(blob,9)
open('web_meta.json','w').write(json.dumps(meta))
open('web_blob.b64','w').write(base64.b64encode(gz).decode())
print(len(blob)/1e6,'MB raw', len(gz)/1e6,'MB gz', sum(x['fn']//3 for x in meta),'tris')
