# PORTAS_CIMA: as portas de cima funcionam como as laterais. A moldura fica so na frente (Z 281-286, 5 mm), e o acrilico 3 mm
# vai atras dela, do tamanho da porta inteira (Z 278-281). Os parafusos M3 de cabeca abaulada entram por dentro, passam pelo
# acrilico e rosqueiam em insertos de latao na moldura (cabeca de 1,65 mm, livre dos batentes). A vedacao (3 mm) fica colada
# atras do acrilico, com furos nas cabecas. As dobradicas rosqueiam pela frente nos insertos (sem porca atras). O batente do
# meio vira uma regua reta preta (300 mm) aparafusada na porta D: os parafusos dela passam pela regua e pelo acrilico e
# rosqueiam nos insertos. A porta E fecha por cima da regua, com as cabecas dela em bolsoes da regua. Abre-se a E primeiro.
import numpy as np, pickle, json, trimesh
exec(open('geo.py').read())
X=pickle.load(open('EXT.pkl','rb'))
ZA0,ZA1,ZF1=278.0,281.0,286.0          # acrilico Z 278-281, moldura Z 281-286
YB,YT,XH,XC=640.9,956.1,228.5,5.0      # linhas dos parafusos: faixa de baixo, de cima, lado da dobradica, montante do meio
PB=[(x,YB) for x in (30.0,115.0,200.0)]+[(x,YT) for x in (30.0,115.0,200.0)]+[(XH,y) for y in (660.0,758.0,778.0,935.0)]
PC_=[(XC,y) for y in (665.0,758.0,778.0,935.0)]                  # montante do meio (D pela regua, E direto)
PX=[(16.0,751.1),(16.0,791.1)]                                    # puxador (porcas sextavadas que ja estao nele)
RG=(-9.0,9.5,648.5,948.5,275.0,278.0)                             # regua: 18,5 x 300 x 3 mm
def bolt(x,y,z_head,L,up=True,hd=5.7,hh=1.65,d=3.0):              # cabeca em z_head (lado de dentro), corpo para +Z
    return U(CYL([x,y,z_head-hh],[x,y,z_head],hd),CYL([x,y,z_head],[x,y,z_head+L],d))
def insert(x,y): return D(CYL([x,y,ZA1],[x,y,ZA1+4.0],4.6),CYL([x,y,ZA1-1],[x,y,ZA1+5],3.0))
# hinge screws (folha da porta, eixo Z em X ~231)
dhw=[c for c in X['u_dobrHW'].split(only_watertight=False) if c.is_volume]
hs=[c for c in dhw if c.bounds[1][0]<240 and (c.bounds[1][2]-c.bounds[0][2])>10]
PH=[tuple(np.round(c.bounds.mean(0)[:2],2)) for c in hs]
dobrHW=U(*[c for c in dhw if c.bounds[1][0]>=240],*[I(c,B(-50,400,0,2000,281.6,400)) for c in hs])
# molduras: so a frente (Z>=282,5 da peca antiga) + preenchimento Z 281-283 pela secao em Z 284
INS=PB+PC_+PH
R={}
for k in ('u_mold1','u_mold2'):
    m=X[k]; fr=I(m,B(-20,260,600,1000,282.5,300)); s=section_polys(m,'z',284.0)
    n=U(fr,prism_xy(s,ZA1,283.0))
    n=D(n,*[CYL([x,y,ZA1-1],[x,y,ZA1+4.0],4.6) for x,y in INS],*[CYL([x,y,ZA1-1],[x,y,ZF1-0.8],3.4) for x,y in PH])
    R[k]=max(n.split(only_watertight=False),key=lambda q:q.volume)
R['u_mold1_Esrc']=R['u_mold1']; R['u_mold2_Esrc']=R['u_mold2']
# acrilico do tamanho da porta
X0,X1,Y0,Y1=1.0,234.0,635.3,961.7
acr=D(B(X0,X1,Y0,Y1,ZA0,ZA1),*[CYL([x,y,ZA0-1],[x,y,ZA1+1],3.4) for x,y in PB+PC_+PX])
R['u_acr1']=acr
# vedacao: mesma pegada em C, agora 3 mm (Z 275-278), dentro do contorno do acrilico, furos nas cabecas e linguetas ate a regua
v=X['u_ved1']; s=section_polys(v,'z',275.5)
ved=I(prism_xy(s,275.0,ZA0),B(X0,X1,Y0,Y1,270,290))
ved=U(ved,B(0.0,9.5,642.0,RG[2]-0.2,275.0,ZA0),B(0.0,9.5,RG[3]+0.2,955.0,275.0,ZA0))
ved=D(ved,*[CYL([x,y,270],[x,y,290],7.0) for x,y in PB+PC_])
R['u_ved1']=max(ved.split(only_watertight=False),key=lambda q:q.volume) if False else ved
# puxador: base desce ate o acrilico novo
p=X['u_pux']; sp=section_polys(p,'z',283.2); R['u_pux']=U(p,prism_xy(sp,ZA1,283.3))
# regua do batente (so na porta D)
rg=B(*RG)
rg=D(rg,*[CYL([x,y,RG[4]-1],[x,y,RG[4]+1.9],6.2) for x,y in PC_],*[CYL([x,y,RG[4]-1],[x,y,RG[5]+1],3.4) for x,y in PC_])
rg=D(rg,*[CYL([-x,y,RG[5]-2.0],[-x,y,RG[5]+1],6.6) for x,y in PC_])          # bolsoes das cabecas da porta E
ch=0.8                                                                         # quebra-canto nas pontas da regua
R['u_reguaPorta']=rg
# ferragens
hw=[bolt(x,y,ZA0,6.0) for x,y in PB]+[bolt(x,y,ZA0,10.0) for x,y in PX]
R['u_portaHW']=trimesh.util.concatenate(hw)
R['u_portaIns']=trimesh.util.concatenate([insert(x,y) for x,y in INS])
R['u_portaHWcD']=trimesh.util.concatenate([bolt(x,y,RG[4]+1.9,8.0) for x,y in PC_])
R['u_portaHWcE']=trimesh.util.concatenate([bolt(-x,y,ZA0,6.0) for x,y in PC_])
R['u_dobrHW']=dobrHW
# checagens
def M_(m):
    q=m.copy(); q.apply_transform(np.diag([-1,1,1,1]))
    if q.volume<0: q.invert()
    return q
chk={}
E={k:M_(R[k]) for k in ('u_mold1','u_mold2','u_acr1','u_ved1','u_portaHW','u_portaIns')}
OTH={k:X[k] for k in ('u_batPorta','u_bat1','u_dobr','u_dobrG','u_espF','u_espFs','u_v72','u_vsup1','u_capa74')}
ALL={**{k:R[k] for k in ('u_mold1','u_mold2','u_acr1','u_ved1','u_reguaPorta','u_pux','u_portaHW','u_portaHWcD','u_dobrHW')},**{k+'_E':v for k,v in E.items()},'u_portaHWcE':R['u_portaHWcE'],**OTH}
ks=list(ALL)
for i,a in enumerate(ks):
    for b in ks[i+1:]:
        A,Bm=ALL[a],ALL[b]
        if np.any(A.bounds[0]>Bm.bounds[1]) or np.any(Bm.bounds[0]>A.bounds[1]): continue
        try: x=I(A,Bm).volume
        except Exception as e: x=-1
        if abs(x)>0.05: chk[a+' x '+b]=round(x,2)
print(json.dumps({'chk':chk,'PH':PH,'vol':{k:bool(v.is_volume) for k,v in R.items()},'b':{k:np.round(v.bounds,1).tolist() for k,v in R.items()}}))
pickle.dump(R,open('PCC.pkl','wb'))
