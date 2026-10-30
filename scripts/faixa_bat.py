import numpy as np, pickle, json, trimesh
exec(open('load.py').read()); exec(open('latload.py').read()); exec(open('geo.py').read())
from shapely.geometry import box, Polygon
RL=pickle.load(open('RL.pkl','rb')); CF=pickle.load(open('CF.pkl','rb'))
Y0,Y1,YM=81.2,551.0,81.2      # labio em toda a altura
corpo=B(265.3,272.8,Y0,Y1,207.0,231.3)                    # entre a aba do perfil (X 265) e a espinha (X 273), presa pelos 3 parafusos da espinha
labio=B(272.8,277.3,YM,Y1,207.0,219.9)                    # batente do acrilico lateral (face de dentro X 277,5), acima da moldura de baixo
f=U(corpo,labio)
f=I(f,HS([0,0,207.0+1.0],(0,0,-1)).__class__(f) if False else f)
for y in (137.8,322.8,507.8): f=D(f,CYL([255,y,228.0],[280,y,228.0],3.4))
f=chamfer_top(f,'z',207.0,0.0) if False else f
YS=262.0                                                   # emenda (limite 300 mm): longe das emendas da capa (298/354) e da verde (326)
fb=I(f,B(250,290,0,YS-0.1,190,240)); ft=I(f,B(250,290,YS+0.1,600,190,240))
esp=B(267.3,270.8,YS-8.0,YS+0.2,212.0,226.0)               # espiga escondida da peca de cima entrando na de baixo
ft=U(ft,esp); fb=D(fb,grow(esp,0.2))
# moldura do painel: sai o montante do lado da coluna (o acrilico apoia direto no labio da faixa)
mol=D(RL['moldura_lat_c'],B(270,290,93.2,400,190,230))       # sai o montante inteiro (corte rente ao topo do trilho, Y 93,2: sem sobra de 0,1) (o desenho do canto passa para a moldura de acabamento)
mol=I(mol,B(280.7,290,0,400,-300,300))                        # trilho de baixo so na frente: o acrilico desce e encosta na lateral (Y 81)
mold=I(RL['moldura_lat_d'],B(280.7,290,0,93.3,-300,300))      # metade de tras: mesmo trilho so na frente (o montante de tras fica para a coluna TD)
mold=U(mold,I(RL['moldura_lat_d'],B(270,290,93.3,400,-300,300)))
# moldura de acabamento por fora: prende a borda do acrilico contra o labio (folga 0,2 de cada lado), face no plano da lateral (X 283,8)
YA0,YA1,YAS=93.4,513.0,330.0
# acrilico vai ate encostar na espinha (borda em Z 219,9, folga 0,2 da espinha em Z 220,1); apoia direto no labio da faixa
acr=RL['acrilico_lat']; ab=acr.bounds
acr=U(acr,B(277.5,280.5,ab[0][1],ab[1][1],210.0,219.9))
acr=U(acr,B(277.5,280.5,81.2,ab[0][1]+0.5,ab[0][2],219.9))   # acrilico desce ate Y 81,2 e apoia no topo da lateral
acr=U(acr,B(277.5,280.5,ab[1][1]-0.5,522.8,ab[0][2],219.9))   # e sobe ate Y 522,8, encostando na banda do topo (Y 523)
# moldura de acabamento por fora, 12 mm (largura do montante antigo), com o mesmo desenho do canto: desce em diagonal ate o trilho de baixo
aco=Polygon([(207.9,129.8),(207.9,473.2),(207.1,476.2),(198.4,511.0),(219.9,511.0),(219.9,93.0),(198.62,93.0),(207.1,126.8)])
# DIAGONAL_LIMPA: cada diagonal e uma reta so ate a borda vertical (Z 207,9), sem a dobrinha de 0,8 mm que sobrou da QUINA_20;
# embaixo ela continua por dentro do trilho (ate Y 90,5), para encontrar a borda de cima do trilho sem degrau
_kb=(207.1-198.62)/(126.8-93.0); _kt=(207.1-198.4)/(511.0-476.2)
aco=Polygon([(207.9,93.0+(207.9-198.62)/_kb),(207.9,476.2-(207.9-207.1)/_kt),(198.4,511.0),(219.9,511.0),(219.9,90.5),(198.62-2.5*_kb,90.5)])   # QUINA_20: diagonal 20 mm mais baixa (em cima, 20 mm mais alta), mesmo angulo   # desenho do canto embaixo e em cima (espelhado); entra nos trilhos
TL=trimesh.load('/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/')if False else None
TOPC=trimesh.load('/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/009.stl'); TOPD=trimesh.load('/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/007.stl')
BANDA=U(trimesh.load('/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/046.stl'),trimesh.load('/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/049.stl'))
molS=I(D(TOPC,B(270,290,0,510.1,190,230)),B(280.7,290,0,600,-300,300))     # moldura de cima: sai o montante; trilho de cima so na frente
molSd=I(TOPD,B(280.7,290,500,600,-300,300)); molSd=U(molSd,I(TOPD,B(270,290,0,500,-300,300)))
def prism_xz2(poly,y0,y1):
    m=trimesh.creation.extrude_polygon(poly,y1-y0); m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
ac=prism_zy(aco,280.7,283.8)
# FRISO_FRENTE: o chanfro 1,2 agora tambem corre na borda da frente (Z 219,9, junto da espinha), como nos outros lados
# peca unica: trilho (metade da frente) + acabamento, com a face de fora e o chanfro continuos
_rs=I(mol,B(270,290,80,94,149.5,150.5)); _ext=I(mol,B(270,290,80,94,140,150)); _ext.apply_translation([0,0,219.9-150.0]); _ext=I(_ext,B(270,290,80,94,209.9,219.9))
_tr=U(mol,_ext,B(281.0,283.8,90.5,93.2,0.0,219.9))
_tr=I(_tr,B(280.7,290,0,400,-300,300))          # ponta do trilho ate Z 219,9 (encosta na espinha) e borda de cima reta (o chanfro e refeito junto)
_pc=U(_tr,ac)
# BORDA_BAIXO_LIMPA: o trilho original ja vinha com chanfro embaixo; a quina e refeita reta antes do chanfro novo,
# para a borda de baixo ficar com um chanfro so de 1,2 (igual a metade de tras), sem a sobra entre os dois
_pc=U(_pc,B(280.7,283.8,81.2,83.6,0.0,219.9),B(280.7,283.8,90.6,93.2,0.0,219.9))   # idem na borda de cima do trilho
_sec=section_polys(_pc,'x',283.75)
_edge=lambda a,b: (abs(a[0])<0.05 and abs(b[0])<0.05) or (a[1]>YAS-1 and b[1]>YAS-1)
_pc=D(_pc,chamfer_cutter(_sec,'x',283.8,1.2,skip=_edge))
ac=D(ac,chamfer_cutter(aco,'x',283.8,1.2,skip=lambda a,b: a[1]<YAS+1 or b[1]<YAS+1))
# PARAFUSOS_MOLDURA: distribuidos simetricos em relacao ao meio da moldura (Y 305,25), 2 em cada peca, fora dos fechos (Y 165-215 / 405-455)
SA=[(y,213.9) for y in (120.0,240.0,370.5,490.5)]
# trilhos de baixo e de cima: 2 parafusos no meio da altura de cada trilho (Y 87,1 / 519,75), dividindo o trilho (Z 0-219,9) em 3: Z 73,3 e 146,6;
# so de acabamento: rosca feita no proprio acrilico
SR=[(y,z) for y in (87.1,519.75) for z in (73.3,146.6)]
for y,z in SA+SR: ac=D(ac,CYL([265,y,z],[290,y,z],3.4)); ac=D(ac,CYL([282.0,y,z],[290,y,z],6.2))
for y,z in SA: fb=D(fb,CYL([264,y,z],[278,y,z],2.5)); ft=D(ft,CYL([264,y,z],[278,y,z],2.5))
acI=I(_pc,B(260,300,0,YAS-0.1,-10,240))
# MOLDURA_CIMA_LIMPA: trilho de cima refeito como bloco limpo (X 280,7-283,8, Y 510,2 ate a borda do acrilico Y 529,3, Z 0-219,9)
# + o acabamento de 12 mm com o desenho do canto; chanfro 1,2 continuo em todas as arestas de fora (sem as sobras do trilho original)
YTOP=529.3
_trT=B(280.7,283.8,510.2,YTOP,0.0,219.9)
_pcT=U(_trT,I(prism_zy(aco,280.7,283.8),B(270,290,YAS+0.1,600,190,240)))
_pcT=D(_pcT,B(280.6,282.85,516.4,519.5,-1,8.0))       # encaixe da metade de tras (o mesmo de antes)
_secT=section_polys(_pcT,'x',283.75)
_pcT=D(_pcT,chamfer_cutter(_secT,'x',283.8,1.2,skip=lambda a,b: (abs(a[0])<0.05 and abs(b[0])<0.05) or (a[1]<YAS+1 and b[1]<YAS+1)))
acS=_pcT
for y,z in SA+SR:
    if y>YAS: acS=D(acS,CYL([265,y,z],[290,y,z],3.4),CYL([282.0,y,z],[290,y,z],6.2))
ft=D(ft,B(276.8,280,522.9,600,195,225))                    # labio livra a banda do topo
for y,z in SA+SR:
    if y<YAS: acI=D(acI,CYL([265,y,z],[290,y,z],3.4),CYL([282.0,y,z],[290,y,z],6.2))
def bolt(p,axis,Lg,d=3.0,hd=5.5,hh=3.0):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*Lg,d))
hw=U(*[bolt([282.0,y,z],[1,0,0],14,hd=5.7,hh=1.65) for y,z in SA],*[bolt([282.0,y,z],[1,0,0],5,hd=5.7,hh=1.65) for y,z in SR])
for y,z in SA: acr=D(acr,CYL([276,y,z],[282,y,z],3.6))
for y,z in SR: acr=D(acr,CYL([276,y,z],[282,y,z],2.5))   # furo roscado M3 no acrilico (trilhos)

print('peca unica: lumps',len(acI.split(only_watertight=False)),'bb',np.round(acI.bounds,1).tolist())
# metade de tras da moldura de cima: a borda de cima (por fora, X 280,7-283,8) tambem sobe ate a borda do acrilico (Y 529,3), chanfro 1,2 por fora
from shapely.geometry import Polygon as _P
molSd=U(molSd,B(280.7,283.8,521.0,YTOP,-219.2,0.0))
molSd=D(molSd,prism_xy(_P([(282.6,YTOP+0.1),(283.9,YTOP+0.1),(283.9,YTOP-1.3)]),-230,1))
# VINCOS_CENTRO: os mesmos 3 vincos verticais do riser (Z -6 / 0 / +6, V de 2 mm x 1 mm) descem pela moldura do painel;
# a emenda das 2 metades da moldura (Z 0) fica no fundo do vinco do meio
def _vinco(z,xf=283.8,y0=70.0,y1=540.0):
    m=trimesh.creation.extrude_polygon(Polygon([(z-1.6,xf+0.6),(z+1.6,xf+0.6),(z,xf-1.0)]),y1-y0)
    m.apply_transform(np.array([[0,1,0,0],[0,0,1,y0],[1,0,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
_VZ=[_vinco(z) for z in (-6.0,0.0,6.0)]
acI=D(acI,*_VZ); acS=D(acS,*_VZ); molSd=D(molSd,*_VZ); mold=D(mold,*_VZ)
out={'banda_topo':BANDA,'moldura_sup_d2':molSd,'moldura_lat_d2':mold,'faixa_batente_inf':fb,'faixa_batente_sup':ft,'moldura_lat_c2':mol,'acab_inf':acI,'acab_sup':acS,'acab_hw':hw,'acrilico_lat2':acr}
print('topo: acS bb',np.round(acS.bounds,1).tolist(),'lumps',len(acS.split(only_watertight=False)),'acS x banda',round(I(acS,BANDA).volume,2),'acr x banda',round(I(acr,BANDA).volume,2),'faixa x banda',round(I(U(fb,ft),BANDA).volume,2),'acr x molSd',round(I(acr,molSd).volume,2),'acS x acr',round(I(acS,acr).volume,2))
print('acr x placaB',round(I(acr,RL['placa_B']).volume,2),'acr x placaA',round(I(acr,RL['placa_A']).volume,2),'acr x molD',round(I(acr,mold).volume,2),'acr bb',np.round(acr.bounds,1).tolist())
print('acr2 x esp',round(I(acr,CF['espinha']).volume,2),'x faixa',round(I(acr,U(fb,ft)).volume,2),'x mol',round(I(acr,mol).volume,2),'x v72',round(I(acr,CF['verde_72']).volume,2),'x placaB',round(I(acr,RL['placa_B']).volume,2))
for k in ('acab_inf','acab_sup'): print(k, round(out[k].bounds[1][1]-out[k].bounds[0][1],1), 'x acr', round(I(out[k],acr).volume,2), 'x placaB', round(I(out[k],RL['placa_B']).volume,2), 'x esp', round(I(out[k],CF['espinha']).volume,2),'x v72',round(I(out[k],CF['verde_72']).volume,2),'x mol',round(I(out[k],mol).volume,2))
fe=[k for k in M if 'fecho D frente' in k and M[k].is_volume]
print('acab x fechos', round(sum(I(ac,M[k]).volume for k in fe),2), 'labio x mol', round(I(U(fb,ft),mol).volume,2), 'labio x acr', round(I(U(fb,ft),RL['acrilico_lat']).volume,2))
print('comprimentos',round(fb.bounds[1][1]-fb.bounds[0][1],1),round(ft.bounds[1][1]-ft.bounds[0][1],1))
chk={}
for k in ('espinha','verde_72','verde_sup','capa_74','fix_espinha'): chk[k]=round(I(f,CF[k]).volume,2)
for k in ('moldura_lat_c','acrilico_lat','placa_B','est_frente'): chk[k]=round(I(f,RL[k]).volume,2)
for k in ('Corpo1@072.stl','65_suporte_P01_D','SV-30-01a moldura (1 de 2)','SV-30-01c vedacao EPDM 8x2','SV-30-03a batente lateral D (1 de 3)'):
    try: chk[k]=round(I(f,M[k]).volume,2)
    except Exception as e: chk[k]='n/a'
fe=[k for k in M if 'fecho D frente' in k]
chk['fechos']=round(sum(I(f,M[k]).volume for k in fe if M[k].is_volume),2)
print(json.dumps(chk)); print(np.round(f.bounds,1).tolist(), f.is_watertight)
pickle.dump(out,open('FB.pkl','wb'))
