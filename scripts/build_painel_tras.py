# PAINEL_FUNDO: o painel de tras (entre as colunas de tras) feito igual ao das laterais. As molduras de acabamento das laterais
# (acI/acS: trilhos de baixo e de cima, desenho do canto em diagonal, vincos do centro, chanfro 1,2) sao alargadas no trecho reto
# (de 219,9 para 235,3, que e a borda da espinha de tras) e giradas para a face de tras (Z -286). O acrilico vai de borda a borda
# da espinha (X +-235,2), apoia no topo da base e encosta na parede do top hat (Y 522,8). A borda do acrilico e presa como na
# lateral: parafusos da moldura atravessam o acrilico e entram num labio da espinha de tras (por dentro); nos trilhos a rosca e no
# proprio acrilico. Em cima, a estrutura escondida do top hat desce ate Y 505 e serve de encosto do acrilico.
import numpy as np, pickle, json, trimesh
exec(open('geo.py').read())
FB=pickle.load(open('FB.pkl','rb')); TC=pickle.load(open('TC.pkl','rb')); TR=pickle.load(open('TR.pkl','rb')); ES=pickle.load(open('ESPC.pkl','rb'))
def PXY(poly,z0,z1):
    m=prism_xy(poly,z0,z1)
    if m.volume<0: m.invert()
    return m
U0=219.9; U1=235.3; DU=U1-U0; UC=110.0
SRL=[73.3,146.6]; SRN=[U1/3.0,2*U1/3.0]; YRB=87.1; YRT_OLD=519.75; YTOP=529.3; YRT=0.5*(510.2+YTOP)
def fill_hole(m,y,z): return U(m,I(CYL([280.7,y,z],[283.8,y,z],6.6),B(280.7,283.8,y-3.4,y+3.4,z-3.4,z+3.4)))
def stretch(m):
    a=I(m,B(200,320,0,700,-50,UC)); b=I(m,B(200,320,0,700,UC,400)); b.apply_translation([0,0,DU])
    s=section_polys(m,'z',UC); mid=PXY(s,UC,UC+DU)
    return U(a,mid,b)
def furo_trilho(m,y,z): return D(m,CYL([265,y,z],[290,y,z],3.4),CYL([282.0,y,z],[290,y,z],6.2))
mi=FB['acab_inf']; ms=FB['acab_sup']
for z in SRL: mi=fill_hole(mi,YRB,z); ms=fill_hole(ms,YRT_OLD,z)
mi=stretch(mi); ms=stretch(ms)
for z in SRN: mi=furo_trilho(mi,YRB,z)
ms=I(ms,B(270,300,300,YTOP,-20,260))                           # trilho de cima termina na borda do acrilico (a parede do top hat comeca em Y 523)
from shapely.geometry import Polygon
if YTOP<529.2: ms=D(ms,PXY(Polygon([(283.9,YTOP-1.3),(283.9,YTOP+0.1),(282.5,YTOP+0.1)]),-20,260))   # chanfro 1,2 refeito na borda nova
for z in SRN: ms=furo_trilho(ms,YRT,z)
# lateral (x,y,z) -> fundo (X=z, Y=y, Z=-x-2,2): face de fora X 283,8 -> Z -286
T=np.array([[0,0,1,0],[0,1,0,0],[-1,0,0,-2.2],[0,0,0,1]],float)
def tr(m):
    q=m.copy(); q.apply_transform(T)
    if q.volume<0: q.invert()
    return q
R={'mol_inf':tr(mi),'mol_sup':tr(ms)}
def bolt(p,axis,Lg,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*Lg,d))
SA=[(y,213.9+DU) for y in (120.0,240.0,370.5,490.5)]; SR=[(YRB,z) for z in SRN]+[(YRT,z) for z in SRN]
hw=U(*[bolt([282.0,y,z],[1,0,0],8) for y,z in SA],*[bolt([282.0,y,z],[1,0,0],4.4) for y,z in SR])
R['hw']=tr(hw)
# acrilico (peca unica de borda a borda)
acr=B(-235.2,235.2,81.2,YTOP,-282.7,-279.7)                   # vai ate a parede de tras (Y 529,5), na altura da lateral
for y,z in SA:
    for s in (1,-1): acr=D(acr,CYL([s*z,y,-284],[s*z,y,-278],3.6))
for y,z in SR:
    for s in (1,-1): acr=D(acr,CYL([s*z,y,-284],[s*z,y,-278],2.5))     # rosca M3 no acrilico (trilhos)
R['acrilico']=acr
# labio da espinha de tras (por dentro do acrilico), com furo roscado dos parafusos da moldura
XL0=235.2-12.8
lab=lambda y0,y1: B(XL0,235.6,y0,y1,-279.5,-276.0)
eF=U(TC['esp_fre_inf'],lab(81.2,344.9)); eFs=U(ES['tcEFs'],lab(345.1,523.3))          # labio para embaixo da estrutura do top hat (que tambem encosta o acrilico)
for y,z in SA:
    h=CYL([z,y,-280],[z,y,-275.5],2.5)
    if y<345: eF=D(eF,h)
    else: eFs=D(eFs,h)
# FECHOS_FUNDO: os mesmos fechos da lateral (Y 190 e 430), do lado da coluna, levados para o fundo junto com a moldura
CT=pickle.load(open('CT.pkl','rb'))
def leva(m):
    q=m.copy(); q.apply_translation([0,0,DU]); return tr(q)
fch=[leva(c) for c in CT['fechos_lat'].split(only_watertight=False) if c.bounds[0][2]>0]
fhw=[leva(c) for c in CT['fechos_hw'].split(only_watertight=False) if c.bounds[0][2]>0]
for c in fhw:
    g=grow(c,0.2) if c.is_volume else c.convex_hull
    if g.bounds[0][1]<345: eF=D(eF,g)
    else: eFs=D(eFs,g)
for c in fch:                                                          # o corpo do fecho entra 2 mm na espinha (como na lateral): bolso com folga 0,2
    if c.bounds[1][2]>-286.0:
        g=grow(c,0.2)
        if g.bounds[0][1]<345: eF=D(eF,g)
        else: eFs=D(eFs,g)
R['fechos']=trimesh.util.concatenate(fch); R['fechos_hw']=trimesh.util.concatenate(fhw)
R['tcEF']=eF; R['tcEFs']=eFs
# encosto de cima: nenhum (a estrutura do top hat fica na altura da travessa)
XE=60.0
R['estr_E']=TR['estr_tras_E']                                         # (sem a descida ate Y 505: a estrutura fica alinhada com a travessa)
R['estr_D']=TR['estr_tras_D']
# conferencias
P=pickle.load(open('parts.pkl','rb')); chk={}
skip={'tcEF','tcEFs','trEE','tcAcr','pfAcr','pfMolI','pfMolS','pfHW','pfFch','pfFchHW'}
def esp(m):
    q=m.copy(); q.apply_transform(np.diag([-1,1,1,1]))
    if q.volume<0: q.invert()
    return q
chkset={'fechos':U(*[c for c in fch if c.is_volume]),'fechos_hw':U(*[c for c in fhw if c.is_volume]),'mol_inf':R['mol_inf'],'mol_sup':R['mol_sup'],'acrilico':R['acrilico'],'labio_espinha':U(R['tcEF'],R['tcEFs']),'estr':U(R['estr_E'],R['estr_D']),'hw':R['hw']}
for k,m in chkset.items():
    for pid,lab_,grp,pm in P:
        if grp not in ('prop','comum','ref') or pid in skip or pid.replace('_E','') in skip: continue
        try:
            if not (np.all(pm.bounds[0]<m.bounds[1]) and np.all(m.bounds[0]<pm.bounds[1])): continue
            x=I(m,pm).volume
        except Exception as e: x=str(e)[:20]
        if not isinstance(x,float) or x>0.05: chk[k+'_x_'+pid]=round(x,2) if isinstance(x,float) else x
ks=list(chkset)
for i,a in enumerate(ks):
    for b in ks[i+1:]:
        x=I(chkset[a],chkset[b]).volume
        if x>0.05: chk[a+'_x_'+b]=round(x,2)
chk['mol_inf_x_mol_inf_E']=round(I(R['mol_inf'],esp(R['mol_inf'])).volume,3)
LOG={'chk':chk,'vol':{k:bool(v.is_volume) for k,v in R.items()},'b':{k:np.round(v.bounds,1).tolist() for k,v in R.items()},'lumps':{k:len(v.split(only_watertight=False)) for k,v in R.items()},
     'tam':{k:round(float(max(v.extents)),1) for k,v in R.items()}}
print(json.dumps(LOG,default=str))
pickle.dump(R,open('PT.pkl','wb'))
