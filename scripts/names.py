# NOMES: padrao SV08_<Local>_<Peca>_<Posicao> (sem cor no nome; a cor fica na lista de materiais).
#  Local: Base, Coluna, Painel, Porta, TopHat, Extensao.  Peca: palavras separadas por "_".
#  Posicao: lugar-lado com hifen: Canto-FD/FE/TD/TE, Lateral-D/E, Frente(-D/E), Tras(-D/E), Fundo(-D/E), Porta-D/E, Centro.
#  {S} = lado: a peca espelhada (_E) troca D por E (Canto-F{S} -> Canto-FD / Canto-FE).
PASTAS={'B':'01_Base','C':'02_Colunas','P':'03_Paineis','R':'04_Portas','T':'05_TopHat','X':'06_Extensao','H':'07_Ferragens','K':'08_Comprados'}
P_,V_,W_,A_,F_,C_='Preto','Verde','Branco','Acrilico 3 mm','Ferragem','Comprado'
N={
# ---------------- base: traseira
'tbPC':('B','Base','Placa_Central','Tras',P_),'tbPD':('B','Base','Placa_Lado','Tras-D',P_),'tbPE':('B','Base','Placa_Lado_Tomada','Tras-E',P_),
'tbVC':('B','Base','Hexagono_Central','Tras',V_),'tbVS':('B','Base','Faixas_Superiores','Tras',V_),'tbVA':('B','Base','Asas','Tras',V_),
'tbMol':('B','Base','Moldura_Tomada','Tras-E',P_),'tbEst':('B','Base','Estruturas_Ocultas','Tras',P_),
# ---------------- base: frente
'p21':('B','Base','Placa_Central','Frente',P_),'pR':('B','Base','Placa_Lado','Frente-{S}',P_),'gC':('B','Base','Logo_Central','Frente',V_),
'fS':('B','Base','Faixa_Superior','Frente-{S}',V_),'fA':('B','Base','Asa','Frente-{S}',V_),'logoW':('B','Base','Logo_Difusor','Frente',W_),
'cxLuz':('B','Base','Caixa_Luz','Frente',W_),'eD':('B','Base','Estrutura_Oculta','Frente-{S}',P_),
'eCs':('B','Base','Estrutura_Oculta_Centro','Frente-D',P_),'eCsL':('B','Base','Estrutura_Oculta_Centro','Frente-E',P_),
'sol1':('B','Base','Soleira','Frente-D',P_),'sol1E':('B','Base','Soleira_Centro','Frente-E',P_),
# ---------------- base: laterais e cantos
'pLA':('B','Base','Placa_Tras','Lateral-{S}',P_),'pLB':('B','Base','Placa_Frente','Lateral-{S}',P_),'v3':('B','Base','Capa_Central','Lateral-{S}',V_),
'v24':('B','Base','Asas','Lateral-{S}',V_),'v15':('B','Base','Faixas_Superiores','Lateral-{S}',V_),
'eLT':('B','Base','Estrutura_Oculta_Tras','Lateral-{S}',P_),'eLM':('B','Base','Estrutura_Oculta_Meio','Lateral-{S}',P_),
'eLF':('B','Base','Estrutura_Oculta_Frente','Lateral-{S}',P_),
'cantF':('B','Base','Cantoneira','Canto-F{S}',P_),'cantT2':('B','Base','Cantoneira','Canto-T{S}',P_),
# ---------------- colunas
'esp1':('C','Coluna','Espinha_Lateral_1de2','Canto-F{S}',P_),'esp1s':('C','Coluna','Espinha_Lateral_2de2','Canto-F{S}',P_),
'espF':('C','Coluna','Espinha_Frente_1de2','Canto-F{S}',P_),'espFs':('C','Coluna','Espinha_Frente_2de2','Canto-F{S}',P_),
'v72':('C','Coluna','Capa_Inferior','Canto-F{S}',V_),'vsup1':('C','Coluna','Capa_Superior','Canto-F{S}',V_),
'capa74':('C','Coluna','Cantoneira_Meio','Canto-F{S}',P_),
'fbI':('C','Coluna','Batente_Acrilico_Inferior','Canto-F{S}',P_),'fbS':('C','Coluna','Batente_Acrilico_Superior','Canto-F{S}',P_),
'tcEL':('C','Coluna','Espinha_Lateral_1de2','Canto-T{S}',P_),'tcELs':('C','Coluna','Espinha_Lateral_2de2','Canto-T{S}',P_),
'tcEF':('C','Coluna','Espinha_Fundo_1de2','Canto-T{S}',P_),'tcEFs':('C','Coluna','Espinha_Fundo_2de2','Canto-T{S}',P_),
'tcV72':('C','Coluna','Capa_Inferior','Canto-T{S}',V_),'tcVs':('C','Coluna','Capa_Superior','Canto-T{S}',V_),
'tcCapa':('C','Coluna','Cantoneira_Meio','Canto-T{S}',P_),'tcFb':('C','Coluna','Batentes_Acrilico','Canto-T{S}',P_),
# ---------------- paineis laterais e fundo
'acI':('P','Painel','Moldura_Frente_Inferior','Lateral-{S}',P_),'acS':('P','Painel','Moldura_Frente_Superior','Lateral-{S}',P_),
'tcMolI':('P','Painel','Moldura_Tras_Inferior','Lateral-{S}',P_),'tcMolS':('P','Painel','Moldura_Tras_Superior','Lateral-{S}',P_),
'tcAcr':('P','Painel','Acrilico','Lateral-{S}',A_),'fechos':('P','Painel','Fechos','Lateral-{S}',P_),
'pfAcr':('P','Painel','Acrilico','Fundo',A_),'pfMolI':('P','Painel','Moldura_Inferior','Fundo-{S}',P_),'pfMolS':('P','Painel','Moldura_Superior','Fundo-{S}',P_),
'pfFch':('P','Painel','Fechos','Fundo-{S}',P_),
# ---------------- portas de baixo
'mold1':('R','Porta','Moldura_Inferior','Porta-{S}',P_),'mold2':('R','Porta','Moldura_Superior','Porta-{S}',P_),'acr1':('R','Porta','Acrilico','Porta-{S}',A_),
'pux':('R','Porta','Puxador','Porta-{S}',P_),'reguaPortaA':('R','Porta','Batente_Meio_1de2','Centro',P_),'reguaPortaB':('R','Porta','Batente_Meio_2de2','Centro',P_),
'placaTopo':('R','Porta','Placa_Rebaixo_Travessa','Porta-{S}',P_),'dobr':('R','Porta','Dobradicas_Folhas','Porta-{S}',P_),
'dobrG':('R','Porta','Dobradicas_Gaiola','Porta-{S}',P_),'bat1':('R','Porta','Batente_Lateral','Porta-{S}',P_),
# ---------------- top hat: frente, fundo, cantos
'tfE':('T','TopHat','Parede','Frente-E',P_),'tfD':('T','TopHat','Parede','Frente-D',P_),'tfC':('T','TopHat','Hexagono','Frente',V_),
'tfL':('T','TopHat','Verdes_Laterais','Frente',V_),'tfEE':('T','TopHat','Estrutura_Oculta','Frente-E',P_),'tfED':('T','TopHat','Estrutura_Oculta','Frente-D',P_),
'supF1':('T','TopHat','Suporte_Trilho_1de3','Frente-E',P_),'supF2':('T','TopHat','Suporte_Trilho_2de3','Frente-Centro',P_),'supF3':('T','TopHat','Suporte_Trilho_3de3','Frente-D',P_),
'trE':('T','TopHat','Parede','Fundo-E',P_),'trD':('T','TopHat','Parede','Fundo-D',P_),'trH':('T','TopHat','Hexagono','Fundo',V_),
'trL':('T','TopHat','Verdes_Laterais','Fundo',V_),'trEE':('T','TopHat','Estruturas_Ocultas','Fundo',P_),
'supT1':('T','TopHat','Suporte_Trilho_1de3','Fundo-E',P_),'supT2':('T','TopHat','Suporte_Trilho_2de3','Fundo-Centro',P_),'supT3':('T','TopHat','Suporte_Trilho_3de3','Fundo-D',P_),
'thCantF':('T','TopHat','Cantoneira','Canto-F{S}',P_),'tcCant':('T','TopHat','Cantoneira','Canto-T{S}',P_),
'thSupF':('T','TopHat','Suporte_Canto','Canto-F{S}',P_),'tcSup':('T','TopHat','Suporte_Canto','Canto-T{S}',P_),
# ---------------- top hat: laterais (riser, aletas, exaustor)
'thTrA':('T','TopHat','Suporte_Trilho_1de3_Tras','Lateral-{S}',P_),'thTrC':('T','TopHat','Suporte_Trilho_2de3_Meio','Lateral-{S}',P_),
'thTrB':('T','TopHat','Suporte_Trilho_3de3_Frente','Lateral-{S}',P_),
'riser47':('T','TopHat','Riser_Frente','Lateral-{S}',P_),'tcRiser':('T','TopHat','Riser_Tras','Lateral-{S}',P_),
'molAl47':('T','TopHat','Moldura_Aletas_Frente','Lateral-{S}',V_),'tcMolAl':('T','TopHat','Moldura_Aletas_Tras','Lateral-{S}',V_),
'bandaB':('T','TopHat','Banda_Frente','Lateral-{S}',P_),'tcBanda':('T','TopHat','Banda_Tras','Lateral-{S}',P_),
'apB':('T','TopHat','Apoio_Acrilico_Frente','Lateral-{S}',P_),'tcApoio':('T','TopHat','Apoio_Acrilico_Tras','Lateral-{S}',P_),
'alF1':('T','TopHat','Aleta_Frente_1de3','Lateral-{S}',P_),'alF2':('T','TopHat','Aleta_Frente_2de3','Lateral-{S}',P_),'alF3':('T','TopHat','Aleta_Frente_3de3','Lateral-{S}',P_),
'alT1':('T','TopHat','Aleta_Tras_1de3','Lateral-{S}',P_),'alT2':('T','TopHat','Aleta_Tras_2de3','Lateral-{S}',P_),'alT3':('T','TopHat','Aleta_Tras_3de3','Lateral-{S}',P_),
'exCaixa':('T','TopHat','Exaustor_Caixa_Sopradores','Lateral-{S}',P_),'exCamara':('T','TopHat','Exaustor_Camara_Ar','Lateral-{S}',P_),
'exSupServo':('T','TopHat','Exaustor_Suporte_Servo','Lateral-{S}',P_),'exHornF':('T','TopHat','Exaustor_Braco_Servo','Lateral-{S}',P_),
'exBarF':('T','TopHat','Exaustor_Barra_Aletas','Lateral-{S}',P_),
# ---------------- extensao de cima
'u_esp1':('X','Extensao','Espinha_Lateral_1de2','Canto-F{S}',P_),'u_esp1s':('X','Extensao','Espinha_Lateral_2de2','Canto-F{S}',P_),
'u_espF':('X','Extensao','Espinha_Frente_1de2','Canto-F{S}',P_),'u_espFs':('X','Extensao','Espinha_Frente_2de2','Canto-F{S}',P_),
'u_v72':('X','Extensao','Capa_Inferior','Canto-F{S}',V_),'u_vsup1':('X','Extensao','Capa_Superior','Canto-F{S}',V_),
'u_capa74':('X','Extensao','Cantoneira_Meio','Canto-F{S}',P_),
'u_fbI':('X','Extensao','Batente_Acrilico_Inferior','Canto-F{S}',P_),'u_fbS':('X','Extensao','Batente_Acrilico_Superior','Canto-F{S}',P_),
'u_tcEL':('X','Extensao','Espinha_Lateral_1de2','Canto-T{S}',P_),'u_tcELs':('X','Extensao','Espinha_Lateral_2de2','Canto-T{S}',P_),
'u_tcEF':('X','Extensao','Espinha_Fundo_1de2','Canto-T{S}',P_),'u_tcEFs':('X','Extensao','Espinha_Fundo_2de2','Canto-T{S}',P_),
'u_tcV72':('X','Extensao','Capa_Inferior','Canto-T{S}',V_),'u_tcVs':('X','Extensao','Capa_Superior','Canto-T{S}',V_),
'u_tcCapa':('X','Extensao','Cantoneira_Meio','Canto-T{S}',P_),'u_tcFb':('X','Extensao','Batente_Acrilico','Canto-T{S}',P_),
'u_acI':('X','Extensao','Moldura_Frente_Inferior','Lateral-{S}',P_),'u_acS':('X','Extensao','Moldura_Frente_Superior','Lateral-{S}',P_),
'u_tcMolI':('X','Extensao','Moldura_Tras_Inferior','Lateral-{S}',P_),'u_tcMolS':('X','Extensao','Moldura_Tras_Superior','Lateral-{S}',P_),
'u_tcAcr':('X','Extensao','Acrilico','Lateral-{S}',A_),'u_fechos':('X','Extensao','Fechos','Lateral-{S}',P_),
'u_apLatF':('X','Extensao','Apoios_Acrilico_Frente','Lateral-{S}',P_),'u_apLatT':('X','Extensao','Apoios_Acrilico_Tras','Lateral-{S}',P_),
'u_pfAcr':('X','Extensao','Acrilico','Fundo',A_),'u_pfMolI':('X','Extensao','Moldura_Inferior','Fundo-{S}',P_),'u_pfMolS':('X','Extensao','Moldura_Superior','Fundo-{S}',P_),
'u_pfFch':('X','Extensao','Fechos','Fundo-{S}',P_),'u_apFundo':('X','Extensao','Apoios_Acrilico','Fundo-{S}',P_),
'u_mold1':('X','Extensao','Moldura_Inferior','Porta-{S}',P_),'u_mold2':('X','Extensao','Moldura_Superior','Porta-{S}',P_),'u_acr1':('X','Extensao','Acrilico','Porta-{S}',A_),
'u_pux':('X','Extensao','Puxador','Porta-{S}',P_),'u_reguaPorta':('X','Extensao','Batente_Meio','Centro',P_),'u_bat1':('X','Extensao','Batente_Lateral','Porta-{S}',P_),
'u_dobr':('X','Extensao','Dobradicas_Folhas','Porta-{S}',P_),'u_dobrG':('X','Extensao','Dobradicas_Gaiola','Porta-{S}',P_),
'u_batPorta':('X','Extensao','Batentes_Cima_Baixo','Porta-{S}',P_),
# ---------------- ferragens (nao imprimem)
'hw1':('H','Base','Parafusos','Lado-{S}',F_),'tbHW':('H','Base','Parafusos','Tras',F_),'hwcol':('H','Coluna','Parafusos_Capas','Canto-F{S}',F_),
'fixesp':('H','Coluna','Parafusos_Espinha','Canto-F{S}',F_),'hwCapa':('H','Coluna','Parafusos_Cantoneira','Canto-F{S}',F_),
'tcHW':('H','Coluna','Parafusos','Canto-T{S}',F_),'acHW':('H','Painel','Parafusos_Moldura','Lateral-{S}',F_),
'fechosHW':('H','Painel','Parafusos_Fechos','Lateral-{S}',F_),'pfHW':('H','Painel','Parafusos_Moldura','Fundo-{S}',F_),
'pfFchHW':('H','Painel','Parafusos_Fechos','Fundo-{S}',F_),'portaHW':('H','Porta','Parafusos','Porta-{S}',F_),
'portaIns':('H','Porta','Insertos_M3','Porta-{S}',F_),'portaHWcD':('H','Porta','Parafusos_Batente_Meio','Porta-D',F_),
'portaHWcE':('H','Porta','Parafusos_Meio','Porta-E',F_),'dobrHW':('H','Porta','Parafusos_Dobradicas','Porta-{S}',F_),
'tnF':('H','TopHat','Parafusos_Perfil','Frente',F_),'tfHW':('H','TopHat','Parafusos','Frente',F_),'tnT':('H','TopHat','Parafusos_Perfil','Fundo',F_),
'trHW':('H','TopHat','Parafusos','Fundo',F_),'tnL':('H','TopHat','Parafusos_Perfil','Lateral-{S}',F_),'hwTopo':('H','TopHat','Parafusos','Canto-F{S}',F_),
'apHW':('H','TopHat','Parafusos_Apoio','Lateral-{S}',F_),'hwRiser':('H','TopHat','Parafusos_Riser','Lateral-{S}',F_),
'bandaPin':('H','TopHat','Pinos_Banda','Lateral-{S}',F_),'exHW':('H','TopHat','Parafusos_Exaustor','Lateral-{S}',F_),
'u_hwCapa':('H','Extensao','Parafusos_Cantoneira','Canto-F{S}',F_),'u_fixesp':('H','Extensao','Parafusos_Espinha','Canto-F{S}',F_),
'u_hwcol':('H','Extensao','Parafusos_Capas','Canto-F{S}',F_),'u_acHW':('H','Extensao','Parafusos_Moldura','Lateral-{S}',F_),
'u_fechosHW':('H','Extensao','Parafusos_Fechos','Lateral-{S}',F_),'u_tcHW':('H','Extensao','Parafusos','Canto-T{S}',F_),
'u_pfHW':('H','Extensao','Parafusos_Moldura','Fundo-{S}',F_),'u_pfFchHW':('H','Extensao','Parafusos_Fechos','Fundo-{S}',F_),
'u_dobrHW':('H','Extensao','Parafusos_Dobradicas','Porta-{S}',F_),'u_portaHW':('H','Extensao','Parafusos','Porta-{S}',F_),
'u_portaIns':('H','Extensao','Insertos_M3','Porta-{S}',F_),'u_portaHWcD':('H','Extensao','Parafusos_Batente_Meio','Porta-D',F_),
'u_portaHWcE':('H','Extensao','Parafusos_Meio','Porta-E',F_),'u_hw2020':('H','Extensao','Parafusos_Perfil_2020','Lado-{S}',F_),
# ---------------- comprados
'tbAS03':('K','Base','Tomada_AS03','Tras-E',C_),'fita':('K','Base','Fita_LED_ARGB','Frente',C_),'exSopr':('K','TopHat','Sopradores_4020','Lateral-{S}',C_),
'exServo':('K','TopHat','Servo_SG90','Lateral-{S}',C_),'dsF':('K','Extensao','Estrutura_Perfis_2020','Topo',C_),
}
def nome(pid):
    """(pasta, nome) da peca; _E troca o lado D->E."""
    e=pid.endswith('_E'); b=pid[:-2] if e else pid
    if b not in N: return None
    k,loc,pc,pos,cor=N[b]; s='E' if e else 'D'
    return PASTAS[k],'SV08_'+loc+'_'+pc+('_'+pos.replace('{S}',s) if pos else '')
def cor(pid):
    b=pid[:-2] if pid.endswith('_E') else pid
    return N[b][4] if b in N else ''
