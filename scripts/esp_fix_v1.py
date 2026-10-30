# espinha aparafusada nos 2 ressaltos da lateral do suporte de canto do top hat (Y 563,5 / 614, Z 259,5):
#  - a perna estreita ganha espessura ate a face de fora (X 283,8, alinhada com a verde) de Y 558,4 a 622, cobrindo a ponta dos ressaltos
#  - parafuso M3x8 ISO7380 por fora, rosca no furo do ressalto; a cabeca fica num rebaixo por dentro da cantoneira de cima (escondida)
# cantoneira de cima presa na espinha por 2 M3x16 em Z 235,2 (meio da perna larga) com porca sextavada embutida por dentro da espinha
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
CT=pickle.load(open('CT.pkl','rb'))
sup=trimesh.load('../ltop/050.stl')
YS=(563.5,614.0); ZS=259.5; ZF=235.2
es=CT['espinha']; cap=CT['cant_top_F']; r47=CT['riser47']
pad=B(279.6,283.8,558.4,622.0,250.2,276.1)
es=U(es,pad)
es=D(es,I(grow(sup,0.2),B(279.0,284.5,550,630,245,285)))                     # alojamento da ponta dos ressaltos (folga 0,2)
es=D(es,*[CYL([281.0,y,ZS],[285.0,y,ZS],3.4) for y in YS])                    # passante do parafuso no fundo (2 mm sobre o ressalto)
es=D(es,*[CYL([268.0,y,ZF],[285.0,y,ZF],3.4) for y in YS])                    # passante do parafuso da cantoneira
es=D(es,*[CYL([272.0,y,ZF],[275.6,y,ZF],2*3.406,sec=6) for y in YS])         # porca M3 embutida por dentro (5,9 entre faces, 2,6 de fundo)
es=max(es.split(only_watertight=False),key=lambda p:p.volume)
# ferragens
hw=[]
for y in YS:   # espinha -> ressalto: M3x8 ISO7380
    hw+= [CYL([283.8,y,ZS],[285.45,y,ZS],5.7), CYL([275.8,y,ZS],[283.8,y,ZS],3.0)]
for y in YS:   # cantoneira -> espinha: M3x16 ISO7380 + porca
    hw+= [CYL([287.5,y,ZF],[289.15,y,ZF],5.7), CYL([271.5,y,ZF],[287.5,y,ZF],3.0), CYL([273.2,y,ZF],[275.6,y,ZF],2*3.175,sec=6)]
HW=trimesh.util.concatenate(hw)
cap=D(cap,grow(pad,0.2),*[CYL([283.0,y,ZS],[286.0,y,ZS],6.4) for y in YS])   # cantoneira: folga da perna engrossada e rebaixo da cabeca (por dentro)
cap=max(cap.split(only_watertight=False),key=lambda p:p.volume)
r47=D(r47,*[CYL([278.0,y,ZF],[285.0,y,ZF],3.4) for y in YS])                # riser: passante do parafuso da cantoneira
r47=max(r47.split(only_watertight=False),key=lambda p:p.volume)
chk={'es_cap':I(es,cap).volume,'es_sup':I(es,sup).volume,'es_r47':I(es,r47).volume,'es_vs':I(es,CT['verde_sup']).volume,'es_bd':I(es,CT['bandaB']).volume,'cap_r47':I(cap,r47).volume}
for k,m in (('es',es),('cap',cap),('r47',r47),('sup',sup),('vs',CT['verde_sup'])):
    chk['hw_'+k]=sum(I(h,m).volume for h in hw if h.is_volume)
for f in ('035','052','055','060','062'): chk['es_'+f]=I(es,trimesh.load('../ltop/'+f+'.stl')).volume
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}), es.is_volume, cap.is_volume, r47.is_volume, np.round(es.bounds,1).tolist())
CT['espinha']=es; CT['cant_top_F']=cap; CT['riser47']=r47; CT['hw_topo']=HW
pickle.dump(CT,open('CT.pkl','wb'))
