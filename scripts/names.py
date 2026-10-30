# NOMES: padrao SV08_<Conjunto>_<Posicao>_<Peca>_<Cor>, com pasta por conjunto.
# {S} = lado (D direita / E esquerda): a peca espelhada (_E) troca D por E. Coluna_F{S} = FD/FE, Coluna_T{S} = TD/TE.
# Pecas sem cor (acrilico, comprado, ferragem) levam o material no fim. Ferragens e compradas nao viram STL.
PASTAS={'B':'01_Base','C':'02_Colunas','P':'03_Paineis','R':'04_Portas','T':'05_TopHat','X':'06_Extensao','H':'07_Ferragens','K':'08_Comprados'}
N={
# --- base: traseira
'tbPC':('B','Base_Tras_Placa_Central_Preto'),'tbPD':('B','Base_Tras_Placa_Lado_D_Preto'),'tbPE':('B','Base_Tras_Placa_Lado_E_Tomada_Preto'),
'tbVC':('B','Base_Tras_Hexagono_Central_Verde'),'tbVS':('B','Base_Tras_Faixas_Superiores_Verde'),'tbVA':('B','Base_Tras_Asas_Verde'),
'tbMol':('B','Base_Tras_Moldura_Tomada_Preto'),'tbEst':('B','Base_Tras_Estruturas_Ocultas_Preto'),
# --- base: frente
'p21':('B','Base_Frente_Placa_Central_Preto'),'pR':('B','Base_Frente_Placa_Lado_{S}_Preto'),'gC':('B','Base_Frente_Logo_Central_Verde'),
'fS':('B','Base_Frente_Faixa_Superior_{S}_Verde'),'fA':('B','Base_Frente_Asa_{S}_Verde'),'logoW':('B','Base_Frente_Logo_Difusor_Branco'),
'cxLuz':('B','Base_Frente_Caixa_Luz_Branco'),'eD':('B','Base_Frente_Estrutura_Oculta_{S}_Preto'),
'eCs':('B','Base_Frente_Estrutura_Oculta_Centro_D_Preto'),'eCsL':('B','Base_Frente_Estrutura_Oculta_Centro_E_Preto'),
'sol1':('B','Base_Frente_Soleira_D_Preto'),'sol1E':('B','Base_Frente_Soleira_E_Centro_Preto'),
# --- base: laterais e cantos
'pLA':('B','Base_Lat{S}_Placa_Tras_Preto'),'pLB':('B','Base_Lat{S}_Placa_Frente_Preto'),'v3':('B','Base_Lat{S}_Capa_Central_Verde'),
'v24':('B','Base_Lat{S}_Asas_Verde'),'v15':('B','Base_Lat{S}_Faixas_Superiores_Verde'),'eLT':('B','Base_Lat{S}_Estrutura_Oculta_Tras_Preto'),
'eLM':('B','Base_Lat{S}_Estrutura_Oculta_Meio_Preto'),'eLF':('B','Base_Lat{S}_Estrutura_Oculta_Frente_Preto'),
'cantF':('B','Base_Canto_F{S}_Cantoneira_Preto'),'cantT2':('B','Base_Canto_T{S}_Cantoneira_Preto'),
# --- colunas
'esp1':('C','Coluna_F{S}_Espinha_Lateral_1de2_Preto'),'esp1s':('C','Coluna_F{S}_Espinha_Lateral_2de2_Preto'),
'espF':('C','Coluna_F{S}_Espinha_Frente_1de2_Preto'),'espFs':('C','Coluna_F{S}_Espinha_Frente_2de2_Preto'),
'v72':('C','Coluna_F{S}_Capa_Inferior_Verde'),'vsup1':('C','Coluna_F{S}_Capa_Superior_Verde'),'capa74':('C','Coluna_F{S}_Cantoneira_Meio_Preto'),
'fbI':('C','Coluna_F{S}_Batente_Acrilico_Inferior_Preto'),'fbS':('C','Coluna_F{S}_Batente_Acrilico_Superior_Preto'),
'tcEL':('C','Coluna_T{S}_Espinha_Lateral_1de2_Preto'),'tcELs':('C','Coluna_T{S}_Espinha_Lateral_2de2_Preto'),
'tcEF':('C','Coluna_T{S}_Espinha_Fundo_1de2_Preto'),'tcEFs':('C','Coluna_T{S}_Espinha_Fundo_2de2_Preto'),
'tcV72':('C','Coluna_T{S}_Capa_Inferior_Verde'),'tcVs':('C','Coluna_T{S}_Capa_Superior_Verde'),'tcCapa':('C','Coluna_T{S}_Cantoneira_Meio_Preto'),
'tcFb':('C','Coluna_T{S}_Batentes_Acrilico_Preto'),
# --- paineis laterais e fundo
'acI':('P','Lateral_{S}_Moldura_Frente_Inferior_Preto'),'acS':('P','Lateral_{S}_Moldura_Frente_Superior_Preto'),
'tcMolI':('P','Lateral_{S}_Moldura_Tras_Inferior_Preto'),'tcMolS':('P','Lateral_{S}_Moldura_Tras_Superior_Preto'),
'tcAcr':('P','Lateral_{S}_Acrilico_3mm'),'fechos':('P','Lateral_{S}_Fechos_Preto'),
'pfAcr':('P','Fundo_Acrilico_3mm'),'pfMolI':('P','Fundo_Moldura_Inferior_{S}_Preto'),'pfMolS':('P','Fundo_Moldura_Superior_{S}_Preto'),
'pfFch':('P','Fundo_Fechos_{S}_Preto'),
# --- portas de baixo
'mold1':('R','Porta_{S}_Moldura_Inferior_Preto'),'mold2':('R','Porta_{S}_Moldura_Superior_Preto'),'acr1':('R','Porta_{S}_Acrilico_3mm'),
'pux':('R','Porta_{S}_Puxador_Preto'),'reguaPortaA':('R','Porta_Batente_Meio_1de2_Preto'),'reguaPortaB':('R','Porta_Batente_Meio_2de2_Preto'),
'placaTopo':('R','Porta_{S}_Placa_Rebaixo_Travessa_Preto'),'dobr':('R','Porta_{S}_Dobradicas_Folhas_Preto'),
'dobrG':('R','Porta_{S}_Dobradicas_Gaiola_Preto'),'bat1':('R','Porta_{S}_Batente_Lateral_Preto'),
# --- top hat: frente, fundo, cantos
'tfE':('T','TopHat_Frente_Parede_E_Preto'),'tfD':('T','TopHat_Frente_Parede_D_Preto'),'tfC':('T','TopHat_Frente_Hexagono_Verde'),
'tfL':('T','TopHat_Frente_Laterais_Verde'),'tfEE':('T','TopHat_Frente_Estrutura_Oculta_E_Preto'),'tfED':('T','TopHat_Frente_Estrutura_Oculta_D_Preto'),
'supF1':('T','TopHat_Frente_Suporte_Trilho_1de3_E_Preto'),'supF2':('T','TopHat_Frente_Suporte_Trilho_2de3_Meio_Preto'),'supF3':('T','TopHat_Frente_Suporte_Trilho_3de3_D_Preto'),
'trE':('T','TopHat_Fundo_Parede_E_Preto'),'trD':('T','TopHat_Fundo_Parede_D_Preto'),'trH':('T','TopHat_Fundo_Hexagono_Verde'),
'trL':('T','TopHat_Fundo_Laterais_Verde'),'trEE':('T','TopHat_Fundo_Estruturas_Ocultas_Preto'),
'supT1':('T','TopHat_Fundo_Suporte_Trilho_1de3_E_Preto'),'supT2':('T','TopHat_Fundo_Suporte_Trilho_2de3_Meio_Preto'),'supT3':('T','TopHat_Fundo_Suporte_Trilho_3de3_D_Preto'),
'thCantF':('T','TopHat_Canto_F{S}_Cantoneira_Preto'),'tcCant':('T','TopHat_Canto_T{S}_Cantoneira_Preto'),
'thSupF':('T','TopHat_Canto_F{S}_Suporte_Preto'),'tcSup':('T','TopHat_Canto_T{S}_Suporte_Preto'),
# --- top hat: laterais (riser, aletas, exaustor)
'thTrA':('T','TopHat_Lat{S}_Suporte_Trilho_1de3_Tras_Preto'),'thTrC':('T','TopHat_Lat{S}_Suporte_Trilho_2de3_Meio_Preto'),'thTrB':('T','TopHat_Lat{S}_Suporte_Trilho_3de3_Frente_Preto'),
'riser47':('T','TopHat_Lat{S}_Riser_Frente_Preto'),'tcRiser':('T','TopHat_Lat{S}_Riser_Tras_Preto'),
'molAl47':('T','TopHat_Lat{S}_Moldura_Aletas_Frente_Verde'),'tcMolAl':('T','TopHat_Lat{S}_Moldura_Aletas_Tras_Verde'),
'bandaB':('T','TopHat_Lat{S}_Banda_Frente_Preto'),'tcBanda':('T','TopHat_Lat{S}_Banda_Tras_Preto'),
'apB':('T','TopHat_Lat{S}_Apoio_Acrilico_Frente_Preto'),'tcApoio':('T','TopHat_Lat{S}_Apoio_Acrilico_Tras_Preto'),
'alF1':('T','TopHat_Lat{S}_Aleta_Frente_1de3_Preto'),'alF2':('T','TopHat_Lat{S}_Aleta_Frente_2de3_Preto'),'alF3':('T','TopHat_Lat{S}_Aleta_Frente_3de3_Preto'),
'alT1':('T','TopHat_Lat{S}_Aleta_Tras_1de3_Preto'),'alT2':('T','TopHat_Lat{S}_Aleta_Tras_2de3_Preto'),'alT3':('T','TopHat_Lat{S}_Aleta_Tras_3de3_Preto'),
'exCaixa':('T','TopHat_Lat{S}_Exaustor_Caixa_Sopradores_Preto'),'exCamara':('T','TopHat_Lat{S}_Exaustor_Camara_Ar_Preto'),
'exSupServo':('T','TopHat_Lat{S}_Exaustor_Suporte_Servo_Preto'),'exHornF':('T','TopHat_Lat{S}_Exaustor_Braco_Servo_Preto'),
'exBarF':('T','TopHat_Lat{S}_Exaustor_Barra_Aletas_Preto'),
# --- extensao de cima
'u_esp1':('X','Ext_Coluna_F{S}_Espinha_Lateral_1de2_Preto'),'u_esp1s':('X','Ext_Coluna_F{S}_Espinha_Lateral_2de2_Preto'),
'u_espF':('X','Ext_Coluna_F{S}_Espinha_Frente_1de2_Preto'),'u_espFs':('X','Ext_Coluna_F{S}_Espinha_Frente_2de2_Preto'),
'u_v72':('X','Ext_Coluna_F{S}_Capa_Inferior_Verde'),'u_vsup1':('X','Ext_Coluna_F{S}_Capa_Superior_Verde'),'u_capa74':('X','Ext_Coluna_F{S}_Cantoneira_Meio_Preto'),
'u_fbI':('X','Ext_Coluna_F{S}_Batente_Acrilico_Inferior_Preto'),'u_fbS':('X','Ext_Coluna_F{S}_Batente_Acrilico_Superior_Preto'),
'u_tcEL':('X','Ext_Coluna_T{S}_Espinha_Lateral_1de2_Preto'),'u_tcELs':('X','Ext_Coluna_T{S}_Espinha_Lateral_2de2_Preto'),
'u_tcEF':('X','Ext_Coluna_T{S}_Espinha_Fundo_1de2_Preto'),'u_tcEFs':('X','Ext_Coluna_T{S}_Espinha_Fundo_2de2_Preto'),
'u_tcV72':('X','Ext_Coluna_T{S}_Capa_Inferior_Verde'),'u_tcVs':('X','Ext_Coluna_T{S}_Capa_Superior_Verde'),'u_tcCapa':('X','Ext_Coluna_T{S}_Cantoneira_Meio_Preto'),
'u_tcFb':('X','Ext_Coluna_T{S}_Batente_Acrilico_Preto'),
'u_acI':('X','Ext_Lateral_{S}_Moldura_Frente_Inferior_Preto'),'u_acS':('X','Ext_Lateral_{S}_Moldura_Frente_Superior_Preto'),
'u_tcMolI':('X','Ext_Lateral_{S}_Moldura_Tras_Inferior_Preto'),'u_tcMolS':('X','Ext_Lateral_{S}_Moldura_Tras_Superior_Preto'),
'u_tcAcr':('X','Ext_Lateral_{S}_Acrilico_3mm'),'u_fechos':('X','Ext_Lateral_{S}_Fechos_Preto'),
'u_apLatF':('X','Ext_Lateral_{S}_Apoios_Acrilico_Frente_Preto'),'u_apLatT':('X','Ext_Lateral_{S}_Apoios_Acrilico_Tras_Preto'),
'u_pfAcr':('X','Ext_Fundo_Acrilico_3mm'),'u_pfMolI':('X','Ext_Fundo_Moldura_Inferior_{S}_Preto'),'u_pfMolS':('X','Ext_Fundo_Moldura_Superior_{S}_Preto'),
'u_pfFch':('X','Ext_Fundo_Fechos_{S}_Preto'),'u_apFundo':('X','Ext_Fundo_Apoios_Acrilico_{S}_Preto'),
'u_mold1':('X','Ext_Porta_{S}_Moldura_Inferior_Preto'),'u_mold2':('X','Ext_Porta_{S}_Moldura_Superior_Preto'),'u_acr1':('X','Ext_Porta_{S}_Acrilico_3mm'),
'u_pux':('X','Ext_Porta_{S}_Puxador_Preto'),'u_reguaPorta':('X','Ext_Porta_Batente_Meio_Preto'),'u_bat1':('X','Ext_Porta_{S}_Batente_Lateral_Preto'),
'u_dobr':('X','Ext_Porta_{S}_Dobradicas_Folhas_Preto'),'u_dobrG':('X','Ext_Porta_{S}_Dobradicas_Gaiola_Preto'),
'u_batPorta':('X','Ext_Porta_{S}_Batentes_Cima_Baixo_Preto'),
# --- ferragens (nao imprimem)
'hw1':('H','Base_Parafusos_{S}'),'tbHW':('H','Base_Tras_Parafusos'),'hwcol':('H','Coluna_F{S}_Parafusos_Capas'),'fixesp':('H','Coluna_F{S}_Parafusos_Espinha'),
'hwCapa':('H','Coluna_F{S}_Parafusos_Cantoneira'),'tcHW':('H','Coluna_T{S}_Parafusos'),'acHW':('H','Lateral_{S}_Parafusos_Moldura'),
'fechosHW':('H','Lateral_{S}_Parafusos_Fechos'),'pfHW':('H','Fundo_Parafusos_Moldura_{S}'),'pfFchHW':('H','Fundo_Parafusos_Fechos_{S}'),
'portaHW':('H','Porta_{S}_Parafusos'),'portaIns':('H','Porta_{S}_Insertos_M3'),'portaHWcD':('H','Porta_D_Parafusos_Batente_Meio'),
'portaHWcE':('H','Porta_E_Parafusos_Meio'),'dobrHW':('H','Porta_{S}_Parafusos_Dobradicas'),
'tnF':('H','TopHat_Frente_Parafusos_Perfil'),'tfHW':('H','TopHat_Frente_Parafusos'),'tnT':('H','TopHat_Fundo_Parafusos_Perfil'),'trHW':('H','TopHat_Fundo_Parafusos'),
'tnL':('H','TopHat_Lat{S}_Parafusos_Perfil'),'hwTopo':('H','TopHat_Canto_F{S}_Parafusos'),'apHW':('H','TopHat_Lat{S}_Parafusos_Apoio'),
'hwRiser':('H','TopHat_Lat{S}_Parafusos_Riser'),'bandaPin':('H','TopHat_Lat{S}_Pinos_Banda'),'exHW':('H','TopHat_Lat{S}_Exaustor_Parafusos'),
'u_hwCapa':('H','Ext_Coluna_F{S}_Parafusos_Cantoneira'),'u_fixesp':('H','Ext_Coluna_F{S}_Parafusos_Espinha'),'u_hwcol':('H','Ext_Coluna_F{S}_Parafusos_Capas'),
'u_acHW':('H','Ext_Lateral_{S}_Parafusos_Moldura'),'u_fechosHW':('H','Ext_Lateral_{S}_Parafusos_Fechos'),'u_tcHW':('H','Ext_Coluna_T{S}_Parafusos'),
'u_pfHW':('H','Ext_Fundo_Parafusos_Moldura_{S}'),'u_pfFchHW':('H','Ext_Fundo_Parafusos_Fechos_{S}'),'u_dobrHW':('H','Ext_Porta_{S}_Parafusos_Dobradicas'),
'u_portaHW':('H','Ext_Porta_{S}_Parafusos'),'u_portaIns':('H','Ext_Porta_{S}_Insertos_M3'),'u_portaHWcD':('H','Ext_Porta_D_Parafusos_Batente_Meio'),
'u_portaHWcE':('H','Ext_Porta_E_Parafusos_Meio'),'u_hw2020':('H','Ext_Parafusos_Perfil_2020_{S}'),
# --- comprados
'tbAS03':('K','Base_Tras_Tomada_AS03'),'fita':('K','Base_Frente_Fita_LED_ARGB'),'exSopr':('K','TopHat_Lat{S}_Sopradores_4020'),
'exServo':('K','TopHat_Lat{S}_Servo_SG90'),'dsF':('K','Ext_Estrutura_Perfis_2020'),
}
def nome(pid):
    """(pasta, nome) da peca; _E troca o lado D->E."""
    e=pid.endswith('_E'); b=pid[:-2] if e else pid
    if b not in N: return None
    k,t=N[b]; s='E' if e else 'D'
    return PASTAS[k],'SV08_'+t.replace('{S}',s)
