# PORTAS_FRENTE v4: as 4 portas da frente (2 de baixo, 2 de cima) ficam como os paineis das laterais: moldura so por fora
# (Z 278-286, 8 mm, frente no plano das colunas) e acrilico 3 mm inteiro atras dela, do tamanho da porta (Z 275-278), que
# encosta direto nos batentes / base da impressora. Moldura SEM insertos: parafusos M3x10 de cabeca abaulada pela frente,
# atravessando a moldura e o acrilico, com inserto ou porca no acrilico (furo de 3,4 no acrilico; a ponta para 1 mm antes
# da face de tras). Dobradicas: os parafusos da folha da porta atravessam moldura e acrilico do mesmo jeito.
# Batente do meio: regua reta preta 5 mm atras da porta D, com porcas M3 embutidas por tras; os parafusos do montante do meio
# da porta D (M3x16) atravessam moldura, acrilico e regua. A porta E fecha encostando o acrilico na regua.
import numpy as np, pickle, json, trimesh
exec(open('geo.py').read()); exec(open('geo_ch2.py').read())
X=pickle.load(open('EXT.pkl','rb')); PC=pickle.load(open('PC.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
Lp={p[0]:p[3] for p in pickle.load(open('parts.pkl','rb'))}
ZA0,ZA1,ZF1=275.0,278.0,286.0
def bolt(x,y,zh,L,hd=5.7,hh=1.65,d=3.0): return U(CYL([x,y,zh-hh],[x,y,zh],hd),CYL([x,y,zh],[x,y,zh+L],d))
def boltF(x,y,L,hd=5.7,hh=1.65,d=3.0): return U(CYL([x,y,ZF1],[x,y,ZF1+hh],hd),CYL([x,y,ZF1-L],[x,y,ZF1],d))   # cabeca na frente da moldura
def hexnut(x,y,z0,z1,af=5.5): return CYL([x,y,z0],[x,y,z1],af/np.cos(np.pi/6),sec=6)
def csk(x,y,zb,L):   # M3 escareado (DIN 7991): cabeca 6,0 x 1,86, face da cabeca em zb, corpo para +Z
    cone=trimesh.creation.cone(radius=3.0,height=3.0,sections=32); cone.apply_translation([x,y,zb])   # base (Ø6) na face zb, afina para +Z
    return U(I(cone,B(x-4,x+4,y-4,y+4,zb,zb+1.86)),CYL([x,y,zb],[x,y,zb+L],3.0))
def cskhole(x,y,zb):  # furo escareado no acrilico
    cone=trimesh.creation.cone(radius=3.2,height=3.2,sections=32); cone.apply_translation([x,y,zb])   # escareado: Ø6,4 na face de tras, afina para a frente
    return U(I(cone,B(x-5,x+5,y-5,y+5,zb-0.5,zb+2.0)),CYL([x,y,zb-1],[x,y,zb+4],3.4),CYL([x,y,zb-1],[x,y,zb+0.01],6.4))
def M_(m):
    q=m.copy(); q.apply_transform(np.diag([-1,1,1,1]))
    if q.volume<0: q.invert()
    return q
def door(F,pux0,dhw0,y0,y1,YB,YT,YH,YC,PX,REG,FR):
    R={}
    dhw=[c for c in dhw0.split(only_watertight=False) if c.is_volume]
    hs=[c for c in dhw if c.bounds[1][0]<240 and (c.bounds[1][2]-c.bounds[0][2])>10]
    PH=[tuple(np.round(c.bounds.mean(0)[:2],2)) for c in hs]
    R['dobrHW']=U(*[c for c in dhw if c.bounds[1][0]>=240],*[U(I(c,B(-50,400,-100,2000,ZA1,400)),CYL([*c.bounds.mean(0)[:2],ZA0+1.0],[*c.bounds.mean(0)[:2],ZA1+0.5],3.0)) for c in hs if c.bounds[1][2]-c.bounds[0][2]>10])
    PB=[(x,YB) for x in (30.0,115.0,200.0)]+[(x,YT) for x in (30.0,115.0,200.0)]+[(228.5,y) for y in YH]
    PC_=[(5.0,y) for y in YC]; HOLES=PB+PC_+PH
    # moldura feita do zero (sem herdar a malha antiga): contorno X 0,5-234,5 com janela X 9,5-222,5 e cantos de 25 mm a 45 graus,
    # extrudada Z 278-286; chanfro 1,2 mm na frente em todo o contorno e na janela; na borda do meio o degrau de 1,5 x 0,7 mm +
    # chanfro de 0,7 (forma o V entre as 2 portas); emenda reta em yj. Furos passantes de 3,4 (sem insertos).
    yw0,yw1,yj=FR; c=25.0
    win=Polygon([(9.5+c,yw0),(222.5-c,yw0),(222.5,yw0+c),(222.5,yw1-c),(222.5-c,yw1),(9.5+c,yw1),(9.5,yw1-c),(9.5,yw0+c)])
    poly=sbox(0.5,y0,234.5,y1).difference(win)
    n=prism_xy(poly,ZA1,ZF1)
    cut=chamfer_cutter(poly,'z',ZF1,1.2,skip=lambda a,b: abs(a[0]-0.5)<1e-6 and abs(b[0]-0.5)<1e-6)
    stp=trimesh.creation.extrude_polygon(Polygon([(-1.0,285.3),(2.0,285.3),(2.7,286.0),(2.7,287.5),(-1.0,287.5)]),y1-y0+2.0)
    stp.apply_transform(np.array([[1,0,0,0],[0,0,1,y0-1.0],[0,1,0,0],[0,0,0,1]],float))
    if stp.volume<0: stp.invert()
    n=D(n,cut,stp,*[CYL([x,y,ZA1-1],[x,y,ZF1+1],3.4) for x,y in HOLES])
    ks=list(F)
    R[ks[0]]=I(n,B(-5,240,y0-5,yj,270,290)); R[ks[1]]=I(n,B(-5,240,yj,y1+5,270,290))
    X0,X1,Y0,Y1=1.0,234.0,y0+0.5,y1-0.5
    R['acr']=D(B(X0,X1,Y0,Y1,ZA0,ZA1),*[cskhole(x,y,ZA0) for x,y in PX],*[CYL([x,y,ZA0-1],[x,y,ZA1+1],3.4) for x,y in HOLES])
    R['acrE']=R['acr']                                                                     # porta E: mesmos furos (espelhados)
    s=section_polys(pux0,'z',283.2); R['pux']=U(pux0,prism_xy(s,ZA1,283.3))
    regs=[]
    for rg in REG:
        rg=D(rg,*[CYL([x,y,268.0],[x,y,276.0],3.4) for x,y in PC_],*[hexnut(x,y,269.0,272.6,5.7) for x,y in PC_])   # porca M3 embutida por tras
        regs.append(max(rg.split(only_watertight=False),key=lambda q:q.volume))
    R['regua']=regs
    R['HW']=trimesh.util.concatenate([boltF(x,y,10.0) for x,y in PB]+[csk(x,y,ZA0,12.0) for x,y in PX])
    R['HWcD']=trimesh.util.concatenate([boltF(x,y,16.0) for x,y in PC_]+[hexnut(x,y,270.0,272.4) for x,y in PC_])
    R['HWcE']=trimesh.util.concatenate([boltF(-x,y,10.0) for x,y in PC_])
    return R,PH
OUT={}
# portas de cima (Y 634,8-962,2), regua 296 mm em 1 peca (entre os batentes de baixo e de cima)
RC,PHc=door({'mold1':X['u_mold1'],'mold2':X['u_mold2']},X['u_pux'],X['u_dobrHW'],634.8,962.2,640.9,956.1,
            (660.0,758.0,778.0,935.0),(665.0,758.0,778.0,935.0),[(16.0,751.1),(16.0,791.1)],
            [B(-9.0,9.5,650.2,946.2,270.0,275.0)],(646.8,950.2,768.1))
# portas de baixo (Y 82-531,5), regua em 2 pecas com meia-junta (Y 297,1-316,7)
RA=U(B(-9.0,9.5,90.2,297.0,270.0,275.0),B(-9.0,9.5,296.9,316.7,272.5,275.0))
RB=U(B(-9.0,9.5,316.9,523.3,270.0,275.0),B(-9.0,9.5,297.1,316.9,270.0,272.5))
RB_,PHb=door({'mold1':PC['mold1'],'mold2':PC['mold2']},CT['porta_pux'],CT['dobr_hw'],82.0,531.5,88.1,525.4,
            (110.0,287.0,307.0,505.0),(115.0,200.0,285.0,330.0,415.0,500.0),[(16.0,280.0),(16.0,320.0)],[RA,RB],(94.0,519.5,297.0))
for pre,R in (('u_',RC),('',RB_)):
    OUT[pre+'mold1']=R['mold1']; OUT[pre+'mold2']=R['mold2']; OUT[pre+'mold1_Esrc']=R['mold1']; OUT[pre+'mold2_Esrc']=R['mold2']
    OUT[pre+'acr1']=R['acr']; OUT[pre+'acr1_Esrc']=R['acrE']; OUT[pre+'pux']=R['pux']; OUT[pre+'dobrHW']=R['dobrHW']
    OUT[pre+'portaHW']=R['HW']; OUT[pre+'portaHWcD']=R['HWcD']; OUT[pre+'portaHWcE']=R['HWcE']
OUT['u_reguaPorta']=RC['regua'][0]; OUT['reguaPortaA']=RB_['regua'][0]; OUT['reguaPortaB']=RB_['regua'][1]
# checagens contra o resto (pecas de baixo contra parts.pkl, de cima contra EXT)
chk={}
def ov(a,b):
    if np.any(a.bounds[0]>b.bounds[1]) or np.any(b.bounds[0]>a.bounds[1]): return 0
    try: return I(a,b).volume
    except Exception: return -1
OTHL={k:Lp[k] for k in ('sol1','sol1E','bat1','dobr','espF','espFs','perfil','p01','trvF','tfED','tfEE','tfD','tfE','eCs','eCsL','eD','pR','p21','capa74','thCantF','base')}
OTHU={k:X[k] for k in ('u_batPorta','u_bat1','u_dobr','u_espF','u_espFs','u_v72','u_vsup1','u_capa74','u_hw2020')}
for pre,OTH in (('',OTHL),('u_',OTHU)):
    ks=['mold1','mold2','acr1','pux','portaHW','portaHWcD','portaHWcE','dobrHW']+(['reguaPortaA','reguaPortaB'] if pre=='' else ['reguaPorta'])
    NEW={pre+k:OUT[pre+k] for k in ks}
    NEW.update({pre+k+'_E':M_(OUT[pre+k]) for k in ('mold1','mold2','pux','portaHW')}); NEW[pre+'acr1_E']=M_(OUT[pre+'acr1_Esrc'])
    for a,A in NEW.items():
        for b,Bm in list(OTH.items())+[(k,v) for k,v in NEW.items() if k>a]:
            x=ov(A,Bm)
            if abs(x)>0.05: chk[a+' x '+b]=round(x,2)
print(json.dumps({'chk':chk,'PHb':PHb,'vol':{k:bool(v.is_volume) for k,v in OUT.items()},'b':{k:np.round(v.bounds,1).tolist() for k,v in OUT.items() if not k.startswith('u_')}}))
pickle.dump(OUT,open('PF.pkl','wb'))
