# PORTAS_FRENTE: as 4 portas da frente (2 de baixo, 2 de cima) ficam como os paineis das laterais: a moldura so por fora
# (Z 281-286, 5 mm, mesmo desenho visto de frente) e o acrilico 3 mm inteiro atras dela, do tamanho da porta (Z 278-281).
# Parafusos M3 de cabeca abaulada por dentro, pelo acrilico, em insertos de latao na moldura (cabeca 1,65 mm livre dos
# batentes). Vedacao 3 mm colada atras do acrilico (Z 275-278) com furos nas cabecas. Dobradicas rosqueiam pela frente nos
# insertos. Batente do meio: regua reta preta 3 mm atras da porta D (cima: 1 peca de 300 mm; baixo: 2 pecas com meia-junta
# de 20 mm, porque passa de 300), com as cabecas rebaixadas; a porta E fecha por cima, cabecas dela em bolsoes da regua.
import numpy as np, pickle, json, trimesh
exec(open('geo.py').read())
X=pickle.load(open('EXT.pkl','rb')); PC=pickle.load(open('PC.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
Lp={p[0]:p[3] for p in pickle.load(open('parts.pkl','rb'))}
ZA0,ZA1,ZF1=278.0,281.0,286.0
def bolt(x,y,zh,L,hd=5.7,hh=1.65,d=3.0): return U(CYL([x,y,zh-hh],[x,y,zh],hd),CYL([x,y,zh],[x,y,zh+L],d))
def insert(x,y): return D(CYL([x,y,ZA1],[x,y,ZA1+4.0],4.6),CYL([x,y,ZA1-1],[x,y,ZA1+5],3.0))
def M_(m):
    q=m.copy(); q.apply_transform(np.diag([-1,1,1,1]))
    if q.volume<0: q.invert()
    return q
def door(F,ved0,pux0,dhw0,y0,y1,YB,YT,YH,YC,PX,REG,tabs):
    R={}
    dhw=[c for c in dhw0.split(only_watertight=False) if c.is_volume]
    hs=[c for c in dhw if c.bounds[1][0]<240 and (c.bounds[1][2]-c.bounds[0][2])>10]
    PH=[tuple(np.round(c.bounds.mean(0)[:2],2)) for c in hs]
    R['dobrHW']=U(*[c for c in dhw if c.bounds[1][0]>=240],*[I(c,B(-50,400,-100,2000,281.6,400)) for c in hs])
    PB=[(x,YB) for x in (30.0,115.0,200.0)]+[(x,YT) for x in (30.0,115.0,200.0)]+[(228.5,y) for y in YH]
    PC_=[(5.0,y) for y in YC]; INS=PB+PC_+PH
    for k,m in F.items():
        fr=I(m,B(-20,260,-100,1100,282.5,300)); s=section_polys(m,'z',284.0)
        n=U(fr,prism_xy(s,ZA1,283.0))
        n=D(n,*[CYL([x,y,ZA1-1],[x,y,ZA1+4.0],4.6) for x,y in INS],*[CYL([x,y,ZA1-1],[x,y,ZF1-0.8],3.4) for x,y in PH])
        R[k]=max(n.split(only_watertight=False),key=lambda q:q.volume)
    X0,X1,Y0,Y1=1.0,234.0,y0+0.5,y1-0.5
    R['acr']=D(B(X0,X1,Y0,Y1,ZA0,ZA1),*[CYL([x,y,ZA0-1],[x,y,ZA1+1],3.4) for x,y in PB+PC_+PX])
    s=section_polys(ved0,'z',275.5)
    v=I(prism_xy(s,275.0,ZA0),B(X0,X1,Y0,Y1,270,290))
    for t in tabs: v=U(v,B(*t))
    R['ved']=D(v,*[CYL([x,y,270],[x,y,290],7.0) for x,y in PB+PC_])
    s=section_polys(pux0,'z',283.2); R['pux']=U(pux0,prism_xy(s,ZA1,283.3))
    regs=[]
    for rg in REG:
        rg=D(rg,*[CYL([x,y,274.0],[x,y,276.9],6.2) for x,y in PC_],*[CYL([x,y,274.0],[x,y,279.0],3.4) for x,y in PC_],
             *[CYL([-x,y,276.0],[-x,y,279.0],6.6) for x,y in PC_])
        regs.append(max(rg.split(only_watertight=False),key=lambda q:q.volume))
    R['regua']=regs
    R['HW']=trimesh.util.concatenate([bolt(x,y,ZA0,6.0) for x,y in PB]+[bolt(x,y,ZA0,10.0) for x,y in PX])
    R['Ins']=trimesh.util.concatenate([insert(x,y) for x,y in INS])
    R['HWcD']=trimesh.util.concatenate([bolt(x,y,276.9,8.0) for x,y in PC_])
    R['HWcE']=trimesh.util.concatenate([bolt(-x,y,ZA0,6.0) for x,y in PC_])
    return R,PH
OUT={}
# portas de cima (Y 634,8-962,2), regua 300 mm em 1 peca
RC,PHc=door({'mold1':X['u_mold1'],'mold2':X['u_mold2']},X['u_ved1'],X['u_pux'],X['u_dobrHW'],634.8,962.2,640.9,956.1,
            (660.0,758.0,778.0,935.0),(665.0,758.0,778.0,935.0),[(16.0,751.1),(16.0,791.1)],
            [B(-9.0,9.5,648.5,948.5,275.0,278.0)],[(0.0,9.5,642.0,648.3,275.0,278.0),(0.0,9.5,948.7,955.0,275.0,278.0)])
# portas de baixo (Y 82-531,5), regua em 2 pecas com meia-junta (Y 297,1-316,7)
RA=U(B(-9.0,9.5,90.2,297.0,275.0,278.0),B(-9.0,9.5,296.9,316.7,276.5,278.0))
RB=U(B(-9.0,9.5,316.9,523.3,275.0,278.0),B(-9.0,9.5,297.1,316.9,275.0,276.5))
RB_,PHb=door({'mold1':PC['mold1'],'mold2':PC['mold2']},Lp['ved1'],CT['porta_pux'],CT['dobr_hw'],82.0,531.5,88.1,525.4,
            (110.0,287.0,307.0,505.0),(115.0,200.0,285.0,330.0,415.0,500.0),[(16.0,280.0),(16.0,320.0)],[RA,RB],[])
for pre,R in (('u_',RC),('',RB_)):
    OUT[pre+'mold1']=R['mold1']; OUT[pre+'mold2']=R['mold2']; OUT[pre+'mold1_Esrc']=R['mold1']; OUT[pre+'mold2_Esrc']=R['mold2']
    OUT[pre+'acr1']=R['acr']; OUT[pre+'ved1']=R['ved']; OUT[pre+'pux']=R['pux']; OUT[pre+'dobrHW']=R['dobrHW']
    OUT[pre+'portaHW']=R['HW']; OUT[pre+'portaIns']=R['Ins']; OUT[pre+'portaHWcD']=R['HWcD']; OUT[pre+'portaHWcE']=R['HWcE']
OUT['u_reguaPorta']=RC['regua'][0]; OUT['reguaPortaA']=RB_['regua'][0]; OUT['reguaPortaB']=RB_['regua'][1]
# checagens contra o resto (pecas de baixo contra parts.pkl, de cima contra EXT)
chk={}
def ov(a,b):
    if np.any(a.bounds[0]>b.bounds[1]) or np.any(b.bounds[0]>a.bounds[1]): return 0
    try: return I(a,b).volume
    except Exception: return -1
low=['mold1','mold2','acr1','ved1','pux','portaHW','portaHWcD','portaHWcE','reguaPortaA','reguaPortaB','dobrHW']
OTHL={k:Lp[k] for k in ('sol1','sol1E','bat1','dobr','espF','espFs','perfil','p01','trvF','tfED','tfEE','tfD','tfE','eCs','eCsL','eD','pR','p21','capa74','thCantF','base')}
NEW={k:OUT[k] for k in low}; NEW.update({k+'_E':M_(OUT[k]) for k in ('mold1','mold2','acr1','ved1','pux','portaHW','portaIns')})
for a,A in NEW.items():
    for b,Bm in list(OTHL.items())+[(k,v) for k,v in NEW.items() if k>a]:
        x=ov(A,Bm)
        if abs(x)>0.05: chk[a+' x '+b]=round(x,2)
print(json.dumps({'chk':chk,'PHb':PHb,'vol':{k:bool(v.is_volume) for k,v in OUT.items()},'b':{k:np.round(v.bounds,1).tolist() for k,v in OUT.items() if not k.startswith('u_')}}))
pickle.dump(OUT,open('PF.pkl','wb'))
