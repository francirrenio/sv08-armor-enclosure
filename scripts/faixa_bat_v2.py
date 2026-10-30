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
mol=D(RL['moldura_lat_c'],B(270,290,93.3,400,190,230))       # sai o montante inteiro (o desenho do canto passa para a moldura de acabamento)
mol=I(mol,B(280.7,290,0,400,-300,300))                        # trilho de baixo so na frente: o acrilico desce e encosta na lateral (Y 81)
mold=I(RL['moldura_lat_d'],B(280.7,290,0,93.3,-300,300))      # metade de tras: mesmo trilho so na frente (o montante de tras fica para a coluna TD)
mold=U(mold,I(RL['moldura_lat_d'],B(270,290,93.3,400,-300,300)))
# moldura de acabamento por fora: prende a borda do acrilico contra o labio (folga 0,2 de cada lado), face no plano da lateral (X 283,8)
YA0,YA1,YAS=93.4,513.0,330.0
# acrilico vai ate encostar na espinha (borda em Z 219,9, folga 0,2 da espinha em Z 220,1); apoia direto no labio da faixa
acr=RL['acrilico_lat']; ab=acr.bounds
acr=U(acr,B(277.5,280.5,ab[0][1],ab[1][1],210.0,219.9))
acr=U(acr,B(277.5,280.5,81.2,ab[0][1]+0.5,ab[0][2],219.9))   # acrilico desce ate Y 81,2 e apoia no topo da lateral
# moldura de acabamento por fora, 12 mm (largura do montante antigo), com o mesmo desenho do canto: desce em diagonal ate o trilho de baixo
aco=Polygon([(207.9,YA1),(219.9,YA1),(219.9,93.0),(193.6,93.0),(207.1,146.8),(207.9,149.8)])   # base entra no trilho: vira uma peca so com a moldura de baixo
def prism_xz2(poly,y0,y1):
    m=trimesh.creation.extrude_polygon(poly,y1-y0); m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
ac=prism_zy(aco,280.7,283.8)
# peca unica: trilho (metade da frente) + acabamento, com a face de fora e o chanfro continuos
_rs=I(mol,B(270,290,80,94,149.5,150.5)); _ext=I(mol,B(270,290,80,94,140,150)); _ext.apply_translation([0,0,219.9-150.0]); _ext=I(_ext,B(270,290,80,94,209.9,219.9))
_tr=U(mol,_ext,B(281.0,283.8,90.5,93.2,0.0,219.9))
_tr=I(_tr,B(280.7,290,0,400,-300,300))          # ponta do trilho ate Z 219,9 (encosta na espinha) e borda de cima reta (o chanfro e refeito junto)
_pc=U(_tr,ac)
_sec=section_polys(_pc,'x',283.75)
_edge=lambda a,b: (abs(a[0]-219.9)<0.05 and abs(b[0]-219.9)<0.05) or (abs(a[0])<0.05 and abs(b[0])<0.05) or (a[1]>YAS-1 and b[1]>YAS-1)
_pc=D(_pc,chamfer_cutter(_sec,'x',283.8,1.2,skip=_edge))
ac=D(ac,chamfer_cutter(aco,'x',283.8,1.2,skip=lambda a,b: a[1]<YAS+1 or b[1]<YAS+1 or (abs(a[0]-219.9)<0.05 and abs(b[0]-219.9)<0.05)))
SA=[(y,213.9) for y in (170.0,230.0,300.0,365.0,440.0,495.0)]
for y,z in SA: ac=D(ac,CYL([265,y,z],[290,y,z],3.4)); ac=D(ac,CYL([282.0,y,z],[290,y,z],6.2))
for y,z in SA: fb=D(fb,CYL([264,y,z],[278,y,z],2.5)); ft=D(ft,CYL([264,y,z],[278,y,z],2.5))
acI=I(_pc,B(260,300,0,YAS-0.1,-10,240)); acS=I(ac,B(270,290,YAS+0.1,600,190,240))
for y,z in SA:
    if y<YAS: acI=D(acI,CYL([265,y,z],[290,y,z],3.4),CYL([282.0,y,z],[290,y,z],6.2))
def bolt(p,axis,Lg,d=3.0,hd=5.5,hh=3.0):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*Lg,d))
hw=U(*[bolt([280.8,y,z],[1,0,0],14) for y,z in SA])
for y,z in SA: acr=D(acr,CYL([276,y,z],[282,y,z],3.6))

print('peca unica: lumps',len(acI.split(only_watertight=False)),'bb',np.round(acI.bounds,1).tolist())
out={'moldura_lat_d2':mold,'faixa_batente_inf':fb,'faixa_batente_sup':ft,'moldura_lat_c2':mol,'acab_inf':acI,'acab_sup':acS,'acab_hw':hw,'acrilico_lat2':acr}
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
