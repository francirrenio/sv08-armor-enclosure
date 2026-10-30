# EXTENSAO DE CIMA (perfis 2020 do DragonSlider, Y 634 a 962,2): colunas, laterais, fundo e porta dupla no MESMO plano da parte
# de baixo, feitos a partir das pecas de baixo. Cada peca de baixo (Y 81 a 531,5) e levada para cima tirando uma faixa de
# 122,1 mm (Y 167 a 289,1, entre a dobradica/fecho de baixo e a cantoneira do meio): o que esta abaixo da faixa sobe 552,8
# (Y 81,2 -> 634) e o que esta acima sobe 430,7 (porta: Y 531,5 -> 962,2). Pecas continuas sao cortadas e emendadas na
# propria secao; ferragens (parafusos, dobradicas, fechos) vao inteiras pelo centro. O fecho de baixo (que caia na faixa)
# e recolocado em Y 690. A fixacao nos 2020 e por garras nas faixas batente (porca T M5 no rasgo de fora da coluna 2020)
# e por apoios/batentes horizontais presos nas barras 2020 de baixo e de cima.
import numpy as np, pickle, json, trimesh
exec(open('geo.py').read())
P=pickle.load(open('parts.pkl','rb')); Pm={p[0]:p[3] for p in P}; Lb={p[0]:p[1] for p in P}
PC=pickle.load(open('PC.pkl','rb'))
# CANTONEIRA_NO_MEIO: 3 trechos, para a cantoneira do meio (e as emendas sob ela) ficar no meio do acrilico de cima (Y 797,1):
#   Y 81,2-214 sobe 552,8 | Y 295,7-365 sobe 471,1 | Y 405,4-531,5 sobe 430,7 (saem as faixas 214-295,7 e 365-405,4)
DA,DM,DB=552.8,471.1,430.7; YMIN,YMAX=634.2,962.2
SEG=[(-50.0,214.0,DA),(214.0+(DA-DM),365.0,DM),(365.0+(DM-DB),2000.0,DB)]
BIG=lambda y0,y1: B(-400,400,y0,y1,-400,400)
def mapy(y):
    for a_,b_,d_ in SEG:
        if a_<=y<b_: return y+d_
    return None
def remap_c(m):                    # peca continua
    out=[]
    for a_,b_,d_ in SEG:
        q=I(m,BIG(a_,b_))
        if len(q.faces): q.apply_translation([0,d_,0]); out.append(q)
    if not out: return None
    r=U(*out); r=I(r,BIG(YMIN,YMAX))
    return r if len(r.faces) else None
def remap_d(m):                    # ferragens: cada componente vai inteiro, pelo centro (as que caem nas faixas retiradas saem)
    out=[]
    for c in m.split(only_watertight=False):
        y=c.bounds.mean(0)[1]; ny=mapy(y)
        if ny is None: continue
        q=c.copy(); q.apply_translation([0,ny-y,0])
        if YMIN-1<q.bounds[0][1] and q.bounds[1][1]<YMAX+1: out.append(q)
    return trimesh.util.concatenate(out) if out else None
def remap(m):
    cs=m.split(only_watertight=False)
    if len(cs)==1 and m.is_volume: return remap_c(m)
    vs=[remap_c(c) for c in cs if c.is_volume]; vs=[v for v in vs if v is not None]
    return U(*vs) if vs else None
CONT=['esp1','esp1s','espF','espFs','v72','vsup1','capa74','fbI','fbS','acI','acS','tcMolI','tcMolS','tcEL','tcELs','tcEF','tcEFs','tcV72','tcVs','tcCapa','tcFb','pfMolI','pfMolS','mold1','mold2','acr1','ved1','bat1']
DISC=['hwCapa','fixesp','hwcol','acHW','fechos','fechosHW','tcHW','pfHW','pfFch','pfFchHW','dobr','dobrG','dobrHW']
R={}; LOG={}
for k in CONT: R['u_'+k]=remap(Pm[k])
for k in DISC: R['u_'+k]=remap_d(Pm[k])
R['u_mold1_Esrc']=remap(PC['mold1_Esrc']); R['u_mold2_Esrc']=remap(PC['mold2_Esrc'])
# puxador: vai pelo centro (Y 300 -> 730,7)
q=Pm['pux'].copy(); q.apply_translation([0,mapy(300.0)-300.0,0]); R['u_pux']=q
# acrilicos novos (lateral e fundo), com os furos levados para cima
SA_L=[mapy(y) for y in (120.0,326.0,490.5)]; SR_L=[mapy(y) for y in (87.1,519.75)]
acrL=B(277.5,280.5,634.2,960.0,-219.9,219.9)
for y in SA_L:
    for s in (1,-1): acrL=D(acrL,CYL([276,y,s*213.9],[282,y,s*213.9],3.6))
for y in SR_L:
    for z in (73.3,146.6):
        for s in (1,-1): acrL=D(acrL,CYL([276,y,s*z],[282,y,s*z],2.5))
R['u_tcAcr']=acrL
pa=Pm['pfAcr']; R['u_pfAcr']=remap(pa)
# PARAFUSO_MEIO: com a faixa de 365-405 retirada, o parafuso da moldura de Y 370,5 saiu; entra 1 no meio do acrilico (Y 797,1),
# na lateral (moldura, acrilico e labio da faixa batente) e no fundo (moldura, acrilico e labio da espinha de tras)
YSM=mapy(326.0); HWX=[]
for key,sz in (('u_acI',1),('u_tcMolI',-1)):
    R[key]=D(R[key],CYL([265,YSM,sz*213.9],[290,YSM,sz*213.9],3.4),CYL([282.0,YSM,sz*213.9],[290,YSM,sz*213.9],6.2))
for key,sz in (('u_fbI',1),('u_fbS',1),('u_tcFb',-1)):
    if R[key] is not None and R[key].bounds[0][1]<YSM<R[key].bounds[1][1]: R[key]=D(R[key],CYL([264,YSM,sz*213.9],[278,YSM,sz*213.9],2.5))
XSM=213.9+15.4
R['u_pfMolI']=D(R['u_pfMolI'],CYL([XSM,YSM,-290],[XSM,YSM,-275],3.4),CYL([XSM,YSM,-290],[XSM,YSM,-284.2],6.2))
for key in ('u_tcEF','u_tcEFs'):
    if R[key].bounds[0][1]<YSM<R[key].bounds[1][1]: R[key]=D(R[key],CYL([XSM,YSM,-280],[XSM,YSM,-275.5],2.5))
for s_ in (1,-1): R['u_pfAcr']=D(R['u_pfAcr'],CYL([s_*XSM,YSM,-284],[s_*XSM,YSM,-278],3.6))
def boltx(p,axis,L,d=3.0,hd=5.7,hh=1.65):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*L,d))
HWX+= [boltx([282.0,YSM,sz*213.9],[1,0,0],14) for sz in (1,-1)]+[boltx([XSM,YSM,-284.2],[0,0,-1],8)]
R['u_acHW']=trimesh.util.concatenate([R['u_acHW']]+HWX[:1]); R['u_tcHW']=trimesh.util.concatenate([R['u_tcHW']]+HWX[1:2]); R['u_pfHW']=trimesh.util.concatenate([R['u_pfHW']]+HWX[2:])
# GARRAS_2020: as faixas batente (lado da coluna, por dentro do acrilico) ganham 3 garras que encostam na face de fora da coluna
# 2020 (X 260) e sao presas com M5x10 + porca T no rasgo (Z +-255,5); Y 665, 815 e 935
YGW=[(668.0,700.0),(838.0,862.0),(912.0,946.0)]; HW=[]        # janelas das garras: pegam tambem os parafusos das verdes e da espinha
def bolt(p,axis,L,d,hd,hh):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*L,d))
for key,sg,hwk in (('u_fbI',1,('u_hwcol','u_fixesp')),('u_fbS',1,('u_hwcol','u_fixesp')),('u_tcFb',-1,('u_tcHW',))):
    m=R[key]
    if m is None: continue
    for y0,y1 in YGW:
        lo,hi=max(y0,m.bounds[0][1]),min(y1,m.bounds[1][1])
        if hi-lo<15: continue
        m=U(m,B(260.2,272.8,lo,hi,sg*224.0,sg*263.0))
        zc=sg*255.0; y=0.5*(lo+hi)                                    # rasgo do 2020: centro Z 255, gargalo X 258-260, camara X 255-258
        m=D(m,CYL([259,y,zc],[273.5,y,zc],5.5),CYL([266.0,y,zc],[273.5,y,zc],9.6))
        HW.append(U(bolt([266.0,y,zc],[1,0,0],10,5.0,8.5,5.0),B(255.2,257.8,y-5,y+5,zc-3.8,zc+3.8)))
        for hk in hwk:                                                # parafusos das verdes/espinha que antes entravam no perfil da impressora: rosca na garra
            for c in R[hk].split(only_watertight=False):
                cb=c.bounds; cy,cz=0.5*(cb[0][1]+cb[1][1]),0.5*(cb[0][2]+cb[1][2])
                if lo<cy<hi and cb[0][0]<272.8 and cb[1][0]>262 and (cb[1][0]-cb[0][0])>10 and sg*cz>200: m=D(m,CYL([258.0,cy,cz],[273.0,cy,cz],2.5))
    for hk in hwk:                                                    # parafusos das verdes/espinha que passam pela faixa batente: rosca nela (em toda a altura)
        for c in R[hk].split(only_watertight=False):
            cb=c.bounds; cy,cz=0.5*(cb[0][1]+cb[1][1]),0.5*(cb[0][2]+cb[1][2])
            if m.bounds[0][1]<cy<m.bounds[1][1] and cb[0][0]<272.8 and cb[1][0]>262 and (cb[1][0]-cb[0][0])>10 and sg*cz>200:
                fill=I(CYL([258.0,cy,cz],[273.0,cy,cz],4.2),B(260.2,272.8,cy-3,cy+3,cz-3,cz+3))     # fecha o furo passante de baixo (ia ate o perfil da impressora)
                m=D(U(m,I(fill,m.convex_hull)),CYL([258.0,cy,cz],[273.0,cy,cz],2.5))
    R[key]=m
# APOIOS de baixo e de cima do acrilico (lateral e fundo) e BATENTES de baixo e de cima da porta, presos nas barras 2020
# (M5x10 + porca T no rasgo de fora: barra de baixo Y 633,4, de cima Y 952,4)
YB_=(634.2,650.0); YT_=(945.0,960.0); YSL={'b':633.4,'t':951.4}           # centros dos rasgos das barras 2020 (barra de cima Y 941,4-961,4)
def apoio_lat(zs):                 # lateral D, metade com Z de sinal zs
    out=[]
    for tag,(y0,y1) in (('b',YB_),('t',YT_)):
        z0,z1=sorted((zs*0.2,zs*206.8)); m=B(260.2,277.3,y0,y1,z0,z1)
        for z in (zs*60.0,zs*160.0):
            m=D(m,CYL([259,YSL[tag],z],[278,YSL[tag],z],5.5),CYL([266.0,YSL[tag],z],[278,YSL[tag],z],9.6))
            HW.append(U(bolt([266.0,YSL[tag],z],[1,0,0],10,5.0,8.5,5.0),B(255.2,257.8,YSL[tag]-3.8,YSL[tag]+3.8,z-5,z+5)))
        for yy in ([mapy(87.1)] if tag=='b' else [mapy(519.75)]):
            for z in (zs*73.3,zs*146.6): m=D(m,CYL([275.5,yy,z],[278,yy,z],3.4))        # ponta dos parafusos do trilho (rosca no acrilico)
        out.append(m)
    return out
R['u_apLatF']=U(*apoio_lat(1)); R['u_apLatT']=U(*apoio_lat(-1))
def faixa_z(zb,zo,x0,x1,tag,y0,y1,xs,furos_trilho=()):   # faixa ao longo de X (fundo ou frente): face da barra 2020 em zb, face de fora em zo
    sg=np.sign(zb); z0,z1=sorted((zb+sg*0.7,zo)); m=B(x0,x1,y0,y1,z0,z1); zh=zb+sg*4.0
    for x in xs:
        m=D(m,CYL([x,YSL[tag],zb-sg*1.0],[x,YSL[tag],zo+sg*1.0],5.5),CYL([x,YSL[tag],zh],[x,YSL[tag],zo+sg*1.0],9.6))
        HW.append(U(bolt([x,YSL[tag],zh],[0,0,sg],8,5.0,8.5,5.0),B(x-5,x+5,YSL[tag]-3.8,YSL[tag]+3.8,*sorted((sg*260.2,sg*262.8)))))
    for x,y in furos_trilho:
        if y0<y<y1: m=D(m,CYL([x,y,zo-sg*2.0],[x,y,zo+sg*1.0],3.4))
    return m
FT=[(x,mapy(y)) for x in (235.3/3.0,2*235.3/3.0) for y in (87.1,519.75)]
R['u_apFundo']=U(*[faixa_z(-265.0,-279.5,0.2,222.2,t,y0,y1,(60.0,160.0),FT) for t,(y0,y1) in (('b',YB_),('t',YT_))])
R['u_batPorta']=U(*[faixa_z(265.0,274.8,0.2,226.0,t,y0,y1,(60.0,180.0)) for t,(y0,y1) in (('b',(634.2,650.0)),('t',(946.4,962.0)))])
R['u_hw2020']=trimesh.util.concatenate(HW)
# PE_SOB_CANTONEIRA: a espinha (azul) e a verde de cima descem ate Y 622,2 (logo acima da espinha de baixo), por dentro da
# cantoneira de cima do top hat, para a ponta delas ficar escondida; o trecho novo e a propria secao da peca, cortada com as
# pecas que ja estao ali (riser, parede, suporte de canto, cantoneira, parafusos) + 0,2 de folga
OBS_ID=['riser47','tcRiser','tfD','trD','thSupF','tcSup','thCantF','tcCant','hwTopo','tcHW','espFs','esp1s','tcEFs','tcELs','vsup1','tcVs','bandaB','tcBanda','dsF','tfED','trEE']
def obst(m):
    box=B(m.bounds[0][0]-3,m.bounds[1][0]+3,600.0,650.0,m.bounds[0][2]-3,m.bounds[1][2]+3); out=[]
    for k in OBS_ID:
        q=Pm[k]; qs=[q] if q.is_volume else [c for c in q.split(only_watertight=False) if c.is_volume]
        for c in qs:
            if np.all(c.bounds[0]<box.bounds[1]) and np.all(box.bounds[0]<c.bounds[1]):
                x=I(c,box)
                if len(x.faces): out.append(grow(x,0.2))
    return out
for key in ('u_esp1','u_espF','u_v72','u_tcEL','u_tcEF','u_tcV72'):
    m=R[key]; _s=m.section(plane_origin=[0,646.0,0],plane_normal=[0,1,0])
    _p,_=_s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-646.0],[0,0,0,1]],float)); sec=__import__('shapely.ops',fromlist=['unary_union']).unary_union(_p.polygons_full)
    ext=trimesh.creation.extrude_polygon(sec,646.5-622.2); ext.apply_transform(np.array([[1,0,0,0],[0,0,1,622.2],[0,1,0,0],[0,0,0,1]],float))
    if ext.volume<0: ext.invert()
    ext=D(ext,*obst(ext))
    R[key]=max(U(m,ext).split(only_watertight=False),key=lambda q:q.volume)
# conferencias
DS=pickle.load(open('DS.pkl','rb')); FR=DS['frame2020']
chk={}
vol={k:(v is not None and bool(v.is_volume)) for k,v in R.items()}
for k,m in R.items():
    if m is None or k.endswith('_Esrc') or k=='u_hw2020': continue
    try:
        x=I(m,FR).volume if m.is_volume else sum(I(c,FR).volume for c in m.split(only_watertight=False) if c.is_volume)
        if x>0.05: chk[k+'_x_2020']=round(x,2)
    except Exception as e: chk[k+'_x_2020']=str(e)[:20]
LOG['chk']=chk; LOG['vol']=vol; LOG['b']={k:np.round(v.bounds,1).tolist() for k,v in R.items() if v is not None}
LOG['tam']={k:round(float(max(v.extents)),1) for k,v in R.items() if v is not None and not k.startswith('u_hw')}
print(json.dumps(LOG,default=str))
pickle.dump(R,open('EXT.pkl','wb'))
