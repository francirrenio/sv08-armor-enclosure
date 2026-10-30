# PORTAS_CIMA v2: as portas de cima nao tem moldura. Cada porta e so o acrilico 3 mm do tamanho da porta (Z 283-286, face da
# frente no plano das colunas), com a dobradica e o puxador presos direto nele. A folha da dobradica continua onde estava
# (Z 286): seus 2 parafusos passam pelo acrilico e prendem em porca M3 atras. O puxador sobe 3,3 mm (base no acrilico novo)
# e prende com 2 M3x8 por dentro nas porcas que ja tem. A vedacao 3 mm vai colada atras do acrilico (Z 280-283). Os batentes
# de baixo/cima e o do lado da dobradica avancam ate Z 279,8 para a vedacao encostar (os furos dos M5 continuam abertos).
# O batente do meio e uma regua reta preta (18,5 x 295,5 x 6,5 mm) atras da porta D, presa por 4 M3x8 pela frente do
# acrilico em porcas embutidas na regua (encaixe pela lateral). A porta E fecha por cima da regua: abre-se a E primeiro.
import numpy as np, pickle, json, trimesh
exec(open('geo.py').read())
X=pickle.load(open('EXT.pkl','rb'))
ZA0,ZA1=283.0,286.0                    # acrilico
ZV0=280.0; ZB=279.8                    # vedacao Z 280-283; batentes ate 279,8
X0,X1,Y0,Y1=1.0,234.0,635.3,961.7      # contorno do acrilico da porta D
RG=(-9.0,9.5,650.5,946.0,276.5,ZA0)    # regua
PC_=[(5.0,y) for y in (672.0,757.0,842.0,927.0)]
PX=[(16.0,751.1),(16.0,791.1)]
def hexnut(x,y,z0,z1,af=5.5): return CYL([x,y,z0],[x,y,z1],af/np.cos(np.pi/6),sec=6)
def bolt_in(x,y,zh,L,hd=5.7,hh=1.65,d=3.0):   # cabeca atras (lado de dentro) em zh, corpo para +Z
    return U(CYL([x,y,zh-hh],[x,y,zh],hd),CYL([x,y,zh],[x,y,zh+L],d))
def bolt_out(x,y,zh,L,hd=5.7,hh=1.65,d=3.0):  # cabeca na frente em zh, corpo para -Z
    return U(CYL([x,y,zh],[x,y,zh+hh],hd),CYL([x,y,zh-L],[x,y,zh],d))
def PXY(poly,z0,z1):
    ps=list(poly.geoms) if hasattr(poly,'geoms') else [poly]
    return U(*[prism_xy(q,z0,z1) for q in ps])
R={}
# dobradica: parafusos da folha da porta passam pelo acrilico, porca atras
dhw=[c for c in X['u_dobrHW'].split(only_watertight=False) if c.is_volume]
hs=[c for c in dhw if c.bounds[1][0]<240 and (c.bounds[1][2]-c.bounds[0][2])>10]
PH=[tuple(np.round(c.bounds.mean(0)[:2],2)) for c in hs]
R['u_dobrHW']=U(*[c for c in dhw if c.bounds[1][0]>=240],*[I(c,B(-50,400,0,2000,ZV0+0.2,400)) for c in hs],*[hexnut(x,y,ZA0-2.4,ZA0) for x,y in PH])
# acrilico
R['u_acr1']=D(B(X0,X1,Y0,Y1,ZA0,ZA1),*[CYL([x,y,ZA0-1],[x,y,ZA1+1],3.4) for x,y in PH+PC_+PX])
R['u_acr1_Esrc']=D(B(X0,X1,Y0,Y1,ZA0,ZA1),*[CYL([x,y,ZA0-1],[x,y,ZA1+1],3.4) for x,y in PH+PX])   # porta E: sem os furos da regua
# vedacao
s=section_polys(X['u_ved1'],'z',275.5)
ved=I(PXY(s,ZV0,ZA0),B(X0,X1,Y0,Y1,270,290))
ved=U(ved,B(0.0,9.5,642.0,RG[2]-0.2,ZV0,ZA0),B(0.0,9.5,RG[3]+0.2,955.0,ZV0,ZA0))
R['u_ved1']=D(ved,*[CYL([x,y,270],[x,y,290],7.0) for x,y in PH])
# puxador: sobe 3,3 mm
p=X['u_pux'].copy(); p.apply_translation([0,0,ZA1-282.7]); R['u_pux']=p
# batentes avancam ate Z 279,8
bp=X['u_batPorta']; s=section_polys(bp,'z',274.5); add=PXY(s,274.6,ZB)
add=D(add,*[CYL([x,y,270],[x,y,290],10.5) for x in (60.0,180.0) for y in (633.45,951.45)])
R['u_batPorta']=U(bp,add)
b1=X['u_bat1']; s=section_polys(b1,'z',274.5); R['u_bat1']=U(b1,I(PXY(s,274.9,ZB),B(0,235.2,0,2000,270,290)))
# regua com porcas embutidas (encaixe pela lateral X+)
rg=B(*RG)
rg=D(rg,*[CYL([x,y,RG[4]-1],[x,y,RG[5]+1],3.4) for x,y in PC_],
     *[U(hexnut(x,y,279.4,281.9,5.7),B(x,RG[1]+1,y-2.9,y+2.9,279.4,281.9)) for x,y in PC_])
R['u_reguaPorta']=rg
# ferragens
R['u_portaHW']=trimesh.util.concatenate([bolt_in(x,y,ZA0,8.0) for x,y in PX])
R['u_portaHWcD']=trimesh.util.concatenate([bolt_out(x,y,ZA1,8.0) for x,y in PC_]+[hexnut(x,y,279.5,281.9) for x,y in PC_])
# checagens
def M_(m):
    q=m.copy(); q.apply_transform(np.diag([-1,1,1,1]))
    if q.volume<0: q.invert()
    return q
chk={}
OTH={k:X[k] for k in ('u_dobr','u_espF','u_espFs','u_v72','u_vsup1','u_capa74','u_hw2020')}
ALL={**{k:R[k] for k in ('u_acr1','u_ved1','u_reguaPorta','u_pux','u_portaHW','u_portaHWcD','u_dobrHW','u_batPorta','u_bat1')},**{k+'_E':M_(R[k]) for k in ('u_acr1','u_ved1','u_pux','u_portaHW','u_batPorta','u_bat1')},**OTH}
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
