import pickle, json, gzip, base64, numpy as np, trimesh
exec(open('load.py').read()); exec(open('geo.py').read())
P=pickle.load(open('P.pkl','rb')); Q=pickle.load(open('Q.pkl','rb')); R=pickle.load(open('R4.pkl','rb')); RL=pickle.load(open('RL.pkl','rb')); CF=pickle.load(open('CF.pkl','rb')); FB=pickle.load(open('FB.pkl','rb')); TL=pickle.load(open('TL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
exec(open('latload.py').read())
def clipm(m,lo,hi):
    for ax in range(3):
        n=[0,0,0]; n[ax]=1; m=m.slice_plane([lo[0],lo[1],lo[2]],n,cap=True)
        n=[0,0,0]; n[ax]=-1; m=m.slice_plane([hi[0],hi[1],hi[2]],n,cap=True)
    return m
LO=np.array([-300,-5,-305]); HI=np.array([300,640,300])
parts=[]  # (id, label, group, color, mesh, mode, extra)
def add(pid,label,grp,col,m,mode='ambos',hint=''):
    parts.append(dict(id=pid,label=label,grp=grp,col=col,mesh=m,mode=mode,hint=hint))
# referencia
add('base','Base da impressora (STEP)','ref','#cfc8b8',clipm(M['Corpo1@071.stl'],LO,HI))
add('perfil','Perfil de canto (STEP)','ref','#b7bec7',clipm(M['Corpo1@072.stl'],LO,HI))
# comuns
add('p01','65_suporte_P01_D','comum','#8a8f96',M['65_suporte_P01_D'])
add('espinha','SV08_Espinha_L_FD_Black','atual','#2f6fd6',clipm(M['SV08_Espinha_L_FD_Black'],LO,HI),'atual')
add('c22','10_chassis_2_2 (baixo central)','atual','#3b3d40',M['10_chassis_2_2'],'atual')
add('led','LED (referencia)','comum','#f2b13c',clipm(M['LED_REFERENCIA'],LO,HI))
add('regua','Regua_baixo_central_mod (verde)','atual','#35a853',clipm(M['Regua_baixo_central_mod'],LO,HI),'atual')
add('molled','Moldura_LED_D_mod (verde do LED)','atual','#35a853',M['Moldura_LED_D_mod'],'atual')
add('placa','Verdes da lateral atuais (placas 1_1, 2_1, 3_1)','atual','#35a853',U(*[L['22_lateral_placa_%d_1_D'%i] for i in (1,2,3)]),'atual')
add('faixa','Verdes da lateral atuais (faixas 1_1, 2_1, 3_1)','atual','#35a853',U(*[L['22_lateral_faixa_%d_1_D'%i] for i in (1,2,3)]),'atual')
add('mollat','Moldura painel lateral (SV-40-01 c/d)','atual','#8fa6d9',clipm(trimesh.util.concatenate([L['SV-40-01c inf +u'],L['SV-40-01d inf -u']]),LO,HI),'atual')
add('cant37','37_cantoneira_traseira_D','atual','#2b2e30',L['37_cantoneira_traseira_D'],'atual')
add('apT','20_apoio_traseiro_D','comum','#8a8f96',L['20_apoio_traseiro_D'])
add('perfT','Perfil de canto traseiro (STEP)','ref','#b7bec7',clipm(L['Corpo1@069.stl'],LO,HI))
add('colT0','Coluna TD - lateral externa','atual','#2f6fd6',clipm(L['58_coluna_inferior_lateral_traseiro_D_externa'],LO,HI),'atual')
hw=[k for k in L if k.startswith(('M3_lateral_apoio','M3_cantoneira','37_M3_cantoneira'))]
add('hw','Parafusos existentes (apoio e cantoneiras)','comum','#c43b3b',trimesh.util.concatenate([L[k] for k in hw]))
add('hwG0','Parafusos e porcas das verdes atuais','atual','#c43b3b',trimesh.util.concatenate([L[k] for k in L if k.startswith('M3_22_')]),'atual')
# atual
add('roxa0','10_chassis_3_1 (roxa)','atual','#8e3bc4',M['10_chassis_3_1'],'atual')
add('cen0','10_chassis_2_1 (central)','atual','#55585c',M['10_chassis_2_1'],'atual')
add('lar0','21_lateral_chassis_1_D e 2_D (laranja)','atual','#ee8a1c',U(L['21_lateral_chassis_1_D'],L['21_lateral_chassis_2_D']),'atual')
add('sol0','Soleira / degrau (SV-30-03c 2/2)','atual','#7fa0d0',M['SV-30-03c soleira (degrau) (2 de 2)'],'atual')
add('mold0','Porta direita - moldura','atual','#c6a3df',clipm(M['SV-30-01a moldura (1 de 2)'],LO,HI),'atual')
add('acr0','Porta direita - acrilico','atual','#bfe3f5',clipm(M['SV-30-01b acrilico 225x453'],LO,HI),'atual')
add('ved0','Porta direita - vedacao','atual','#cc3b3b',clipm(M['SV-30-01c vedacao EPDM 8x2'],LO,HI),'atual')
add('bat0','Batente lateral da porta','atual','#7a7a7a',clipm(M['SV-30-03a batente lateral D (1 de 3)'],LO,HI),'atual')
# proposta
EST='#4a4f53'; PRE='#1e2123'; VER='#35a853'
add('pR','Roxa - placa preta (mesmo desenho)','prop',PRE,R['placa_roxa'],'prop')
add('gV','Detalhe verde na parte que subiu','prop',VER,R['verde_topo'],'prop')
add('gC','Faixa verde central','prop',VER,clipm(R['verde_central'],LO,HI),'prop')
add('molled1','Moldura verde do LED (face Z 286)','prop',VER,R['moldura_led'],'prop')
add('regua1','Regua verde de baixo (face Z 286)','prop',VER,clipm(R['regua'],LO,HI),'prop')
add('p21','Central de cima - placa preta','prop',PRE,R['placa_21'],'prop')
add('p22','Central de baixo - placa preta','prop',PRE,R['placa_22'],'prop')
add('pLA','Lateral - placa preta de tras','prop',PRE,RL['placa_A'],'prop')
add('pLB','Lateral - placa preta da frente','prop','#222528',RL['placa_B'],'prop')
add('eD','Estrutura frente D (escondida)','prop',EST,R['est_D'],'prop')
add('eCs','Estrutura central cima (escondida)','prop',EST,R['est_Cs'],'prop')
add('eCi','Estrutura central baixo (escondida)','prop',EST,R['est_Ci'],'prop')
add('eCsL','Estrutura central cima E (espelho)','prop',EST,clipm(R['est_CsL'],LO,HI),'prop')
add('eCiL','Estrutura central baixo E (espelho)','prop',EST,clipm(R['est_CiL'],LO,HI),'prop')
add('v3','Verde 3 - central (em volta do apoio de mao)','prop','#3aa857',RL['verde_central'],'prop')
add('v24','Verdes 2 e 4 - bracos','prop','#45b862',U(RL['verde_braco_F'],RL['verde_braco_T']),'prop')
add('v15','Verdes 1 e 5 - cima e baixo','prop','#2f9449',U(RL['verde_lat_F_sup'],RL['verde_lat_F_inf'],RL['verde_lat_T_sup'],RL['verde_lat_T_inf']),'prop')
add('cantF','Cantoneira da frente (L, peca unica)','prop','#2b2e30',CF['cantoneira_F_L'],'prop')
add('cantT','Cantoneira de tras (L, peca unica)','prop','#2b2e30',RL['cantoneira_T_L'],'prop')
add('eLT','Estrutura lateral de tras (escondida)','prop','#565b60',RL['est_tras'],'prop')
add('eLM','Estrutura lateral do meio (escondida)','prop',EST,RL['est_meio'],'prop')
add('eLF','Estrutura lateral da frente (escondida)','prop','#565b60',RL['est_frente'],'prop')
add('esp1','SV08_Espinha_FD_Lateral_Black (1 de 2, Y 81-345, encaixe da andorinha)','prop','#2f6fd6',CT['espinha_lat_inf'],'prop')
add('esp1s','SV08_Espinha_FD_Lateral_Black (2 de 2, Y 345-622, espiga da andorinha)','prop','#2a63c4',CT['espinha_lat_sup'],'prop')
add('espF','SV08_Espinha_FD_Frente_Black (1 de 2, Y 81-345, encaixe da andorinha)','prop','#3b7be0',CT['espinha_fre_inf'],'prop')
add('espFs','SV08_Espinha_FD_Frente_Black (2 de 2, Y 345-622, espiga da andorinha)','prop','#356fcc',CT['espinha_fre_sup'],'prop')
add('v72_0','Verde de baixo da coluna (72) - antes','atual','#35a853',CF['verde_72'],'atual')
add('v72','Verde de baixo da coluna (72) - recua 2 mm onde e larga (embaixo)','prop','#35a853',CT['verde_72'],'prop')
add('vsup0','Verde de cima da coluna (atual, invade a espinha)','atual','#35a853',M['SV08_Verde_Superior_FD_Green'],'atual')
add('vsup1','Verde de cima da coluna (quina igual a da 72)','prop','#35a853',CT['verde_sup'],'prop')
add('capa74','74_capa_central_D - 1 parafuso no centro de cada aba','prop','#2b2e30',CF['capa_74'],'prop')
add('hwCapa','Parafusos da cantoneira do meio (2x M3x16 cabeca abaulada; porca na lateral, inserto na frente)','prop','#c0392b',CT['hw_capa74'],'prop')
add('fbI','Faixa batente sob a espinha - baixo (batente do acrilico)','prop','#3d4246',FB['faixa_batente_inf'],'prop')
add('acI','Moldura do painel lateral + acabamento (peca unica)','prop','#8fa6d9',FB['acab_inf'],'prop')
add('acS','Moldura do painel lateral (cima) + acabamento (peca unica)','prop','#8fa6d9',FB['acab_sup'],'prop')
add('molS1','Moldura painel lateral cima - metade de tras (trilho so na frente)','prop','#8fa6d9',FB['moldura_sup_d2'],'prop')
TD_='/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/'
def T_(*fs): return trimesh.util.concatenate([trimesh.load(TD_+'%03d.stl'%f) for f in fs])
TOPREF=1
add('topImp','Impressora - travessa lateral de cima e cantos (STEP)','ref','#b7bec7',T_(60,61,62))
add('thCantF0','Top hat - cantoneira de cima da frente (FD) - original','atual','#2b2e30',T_(53),'atual')
add('thCantF','Top hat - cantoneira de cima da frente (FD) - peca limpa, faces de dentro planas','prop','#2b2e30',CT['cant_top_F'],'prop')
add('riser47_0','Riser lateral D (2 de 2) - original','atual','#45484c',T_(47),'atual')
add('riser47','Riser lateral D (2 de 2) - Z 0 a 219,9, emenda no centro dentro do vinco; abertura 138 x 44; ponta entra 10 mm na espinha','prop','#45484c',CT['riser47'],'prop')
add('riser35_0','Riser lateral D (1 de 2) - original','atual','#45484c',T_(35),'atual')
add('riser35','Riser lateral D (1 de 2) - Z -248 a 0, emenda no centro dentro do vinco; abertura 138 x 44','prop','#45484c',CT['riser35'],'prop')
add('molAl47','Moldura verde da abertura das aletas - frente','prop','#35a853',CT['riser47_mold'],'prop')
add('molAl35','Moldura verde da abertura das aletas - tras','prop','#35a853',CT['riser35_mold'],'prop')
add('hwRiser','Parafusos das molduras das aletas (8x M3x8 escareado) e pinos da emenda do riser','prop','#c0392b',trimesh.util.concatenate([CT['riser47_hw'],CT['riser35_hw'],CT['riser_pinos']]),'prop')
add('aletas0','Aletas (persianas) - originais','atual','#5a5e63',T_(37,38,39,40,41,42),'atual')
add('aletas1','Aletas (persianas) - 8 mm mais compridas, na abertura nova','prop','#5a5e63',trimesh.util.concatenate([CT['riser47_aletas'],CT['riser35_aletas']]),'prop')
add('hwTopo','Parafusos do topo FD (espinha no suporte: 2x M3x8; cantoneira na espinha: 2x M3x16 + porca)','prop','#c0392b',CT['hw_topo'],'prop')
add('thCantT','Top hat - cantoneira de cima de tras (TD)','comum','#2b2e30',T_(54))
add('thSupF0','Top hat - suporte de canto da frente (FD) - original','atual','#55595d',T_(50),'atual')
add('thSupF','Top hat - suporte de canto da frente (FD) - ressaltos da lateral encurtados ate X 279,6','prop','#55595d',CT['supF'],'prop')
add('thSupT','Top hat - suporte de canto de tras (TD)','comum','#55595d',T_(51))
add('thTrA','Top hat - suporte do trilho lateral A','comum','#55595d',T_(52))
add('thTrB','Top hat - suporte do trilho lateral B','comum','#55595d',T_(55))
add('colTD','Coluna TD (traseira direita, atual)','comum','#4a7a52',T_(77,78,80,81,82,83,84,85,86))
add('banda0','Banda do topo lateral (V2, atual)','atual','#2b2e30',FB['banda_topo'],'atual')
add('bandaA','Banda do topo lateral - tras (Z -250 a 0, emenda no vinco do centro)','prop','#2b2e30',CT['bandaA'],'prop')
add('bandaPin','Pinos da emenda da banda do topo (2x 3 x 3 x 16)','prop','#c0392b',CT['banda_pinos'],'prop')
add('bandaB','Banda do topo lateral - frente (Z 0 a 219,9, emenda no vinco do centro)','prop','#2b2e30',CT['bandaB'],'prop')
add('apA','Apoio do acrilico no topo - tras (aparafusado no batente original)','prop','#3d4246',TL['apoio_A'],'prop')
add('apB','Apoio do acrilico no topo - frente','prop','#2e3236',TL['apoio_B'],'prop')
add('apHW','Parafusos do apoio do topo (furos do batente original)','prop','#e0402f',TL['apoio_hw'],'prop')
add('acHW','Parafusos da moldura de acabamento','prop','#e0402f',FB['acab_hw'],'prop')
add('fbS','Faixa batente sob a espinha - cima','prop','#2e3236',TL['faixa_sup'],'prop')
add('fixesp','Fixacao da espinha no perfil (2x M3x18, Y 137,8 / 322,8)','prop','#e0402f',CF['fix_espinha'],'prop')
add('hwcol','Parafusos das verdes da coluna (Y 126/266 e 383,5/493,5, nos furos das verdes) e M3x8 embutidos','prop','#e0402f',CT['hw_verdes'],'prop')
add('acrL0','Painel lateral - acrilico','atual','#bfe3f5',clipm(L['SV-40-01e acrilico 3mm 420x411'],LO,HI),'atual')
add('acrL1','Painel lateral - acrilico (ate a espinha; topo sobe 4 mm e entra sob a banda)','prop','#bfe3f5',clipm(CT['acrilico_lat'],LO,HI),'prop')
add('mollat1','Moldura painel lateral - metade de tras (desce 12 mm)','prop','#8fa6d9',clipm(FB['moldura_lat_d2'],LO,HI),'prop')
add('colT1','Coluna TD - lateral externa (desce ate Y 81)','prop','#2f6fd6',clipm(RL['coluna_TD_ext'],LO,HI),'prop')
add('sol1','Soleira / degrau - proposta','prop','#7fa0d0',R['soleira'],'prop')
add('mold1','Porta direita - moldura de baixo (mais baixa; porcas das dobradicas por tras)','prop','#c6a3df',CT['porta_mold1'],'prop')
add('mold2','Porta direita - moldura de cima (porcas das dobradicas por tras)','prop','#c6a3df',CT['porta_mold2'],'prop')
add('pux','Porta direita - puxador','prop','#2b2e30',CT['porta_pux'],'prop')
add('dobr','Dobradicas K1 270 graus da porta direita (Y 150 e 450) - folhas','prop','#2b2e30',CT['dobradicas'],'prop')
add('dobrG','Dobradicas K1 - gaiola das engrenagens','prop','#55595d',CT['dobr_gaiola'],'prop')
add('dobrHW','Parafusos das dobradicas (8x M3 cabeca cilindrica + porca embutida)','prop','#c0392b',CT['dobr_hw'],'prop')
add('fechos','Fechos snap latch do painel lateral (frente e tras, Y 190 e 430)','prop','#3a3e42',CT['fechos_lat'],'prop')
add('fechosHW','Parafusos dos fechos (M3x16 + porca)','prop','#c0392b',CT['fechos_hw'],'prop')
add('acr1','Porta direita - acrilico (mais baixo)','prop','#bfe3f5',clipm(P['SV-30-01b acrilico (proposta)'],LO,HI),'prop')
add('ved1','Porta direita - vedacao','prop','#cc3b3b',clipm(P['SV-30-01c vedacao EPDM (proposta)'],LO,HI),'prop')
add('bat1','Batente lateral da porta','prop','#7a7a7a',clipm(P['SV-30-03a batente lateral D (proposta)'],LO,HI),'prop')
add('hw1','Parafusos M3 novos','prop','#e0402f',trimesh.util.concatenate([b for b in R['ferragens'].split(only_watertight=False) if b.bounds[0][0]<270]+[RL['ferragens']]),'prop')
# LADO_E: a lateral esquerda e o espelho da direita (X -> -X); o quadro da impressora e simetrico (perfis espelhados batem em ~0,05 mm)
MIR_SKIP={'base','led','regua','gC','regua1','eCs','eCi','eCsL','eCiL','c22','cen0','p21','p22'}
_RX=np.diag([-1.0,1.0,1.0,1.0])
def _esp(m):
    q=m.copy(); q.apply_transform(_RX)
    if q.is_volume and q.volume<0: q.invert()
    return q
_novos=[]
E_SRC={'pLB':CT['E_placa_B'],'v24':RL['verde_braco_T'],'v15':U(RL['verde_lat_F_sup'],RL['verde_lat_T_sup'],RL['verde_lat_T_inf']),'eLM':CT['E_est_meio'],'eLF':CT['E_est_frente']}
# JANELA_FORCA: a janela do conector de forca (com 2 furos de fixacao) copiada da base, na carenagem da esquerda:
# janela e furos atravessam ate a face de fora; por dentro, um bolsao do tamanho do rebaixo da base (para o corpo do conector)
# que deixa so os 3 mm de fora (verdes e placa preta entre X -280,8 e -283,8)
from shapely.geometry import Polygon as _SP
def _ints(x,zr):
    s_=section_polys(M['Corpo1@071.stl'],'x',x); gs_=s_.geoms if hasattr(s_,'geoms') else [s_]
    return [_SP(i.coords) for g_ in gs_ for i in g_.interiors if zr[0]<i.bounds[0] and i.bounds[2]<zr[1]]
_jan=_ints(-256.0,(100.0,170.0))                                   # janela 48,6 x 28 + 2 furos D4
_reb=[p_ for p_ in _ints(-264.0,(95.0,175.0)) if p_.bounds[1]<5 and p_.bounds[3]<40 and p_.bounds[2]<175]   # rebaixo 73,4 x 32,8
JAN_CUT=[prism_zy(p_,-300.0,-268.0) for p_ in _jan]+[prism_zy(p_,-280.8,-268.0) for p_ in _reb]
JAN_BOX=B(-300.0,-268.0,0.0,40.0,95.0,175.0)
print('janela',[[round(v,1) for v in p_.bounds] for p_ in _jan],'rebaixo',[[round(v,1) for v in p_.bounds] for p_ in _reb])
for p in parts:
    pid=p['id']; m=p['mesh']
    if pid in MIR_SKIP: continue
    if m.bounds[0][0]<-10:
        if pid!='hw1': print('sem espelho (cruza o centro):',pid); continue
    if pid in ('mold0','mold1'): m=I(m,B(1.5,300,-10,700,-400,400))
    if pid in E_SRC: m=E_SRC[pid]
    if pid=='hw1':
        cs=m.split(only_watertight=False); cen=[c.bounds.mean(0) for c in cs]
        keep=[c for c,cc in zip(cs,cen) if cc[0]>1 and not any(np.linalg.norm(np.array([-cc[0],cc[1],cc[2]])-o)<1.0 for o in cen)]
        keep=[c for c in keep if not (c.bounds[0][1]<37.0 and c.bounds[1][1]>2.0 and c.bounds[0][2]<173.5 and c.bounds[1][2]>98.0) and not (c.bounds[0][1]<40.0 and c.bounds[1][1]>34.0 and c.bounds[0][2]<198.0 and c.bounds[1][2]>192.0)]   # JANELA_FORCA: saem os parafusos que caem na janela/rebaixo (lado E)
        m=trimesh.util.concatenate(keep)
    me=_esp(m)
    if pid=='sol1':   # a base tem uma nervura so do lado E (X -195,5 a -169,9, Y 68,8-69,9): folga de 0,2 por baixo da soleira
        _bE=I(M['Corpo1@071.stl'],B(-197.0,-168.0,67.0,71.5,262.0,271.0))
        me=max(D(me,grow(_bE,0.2)).split(only_watertight=False),key=lambda q:q.volume)
    _novos.append(dict(id=pid+'_E',label=p['label']+' - lado E (espelho)',grp=p['grp'],col=p['col'],mesh=me,mode=p['mode'],hint=p.get('hint','')))
parts+=_novos
parts.append(dict(id='molCon_E',label='Moldura verde do conector de forca (lado E)',grp='prop',col='#35a853',mesh=_esp(CT['E_moldura_conector']),mode='prop',hint=''))
_as=pickle.load(open('../as03/as03_parts_D.pkl','rb'))
parts.append(dict(id='as03_E',label='Tomada AS03 (C14 + fusivel + chave) - STEP do fabricante, na estrutura',grp='comum',col='#3a3a3a',mesh=_esp(trimesh.util.concatenate([_as[20]]+_as[3:4])),mode='ambos',hint=''))
parts.append(dict(id='as03b_E',label='Tomada AS03 - chave e fusivel',grp='comum',col='#d23a2a',mesh=_esp(trimesh.util.concatenate([_as[i] for i in range(21) if i not in (20,3)])),mode='ambos',hint=''))
print('espelhadas',len(_novos))
exec(open('meshclean.py').read())
for p in parts:
    if p['grp']!='ref':
        try: p['mesh']=clean(p['mesh'])
        except Exception: pass
pickle.dump([(p['id'],p['label'],p['grp'],p['mesh']) for p in parts],open('parts.pkl','wb'))
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
