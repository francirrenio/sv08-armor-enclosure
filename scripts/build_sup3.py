# SUPORTES_3: suportes do trilho (frente e laterais) refeitos em 3 pecas iguais (~128 mm), emendas em +-64,3;
# a peca do meio leva o parafuso central (u=0) que prende o suporte na impressora, livre na janela do meio.
# Cada emenda: 2 montantes lado a lado (11,8 cada), lingueta no meio e 2 parafusos M3x20 na horizontal (Y 572 e 605).
# Mantem: furos da estrutura da frente, porcas T do perfil 2020 (frente +-40/+-165; laterais +-40/+-150), furos originais.
import numpy as np, trimesh, pickle, json
exec(open('geo.py').read())
TF=pickle.load(open('TF.pkl','rb'))
TD_='/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/'
P=np.array([[0,0,1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]],float)       # lateral <-> quadro local (u=z, w=x)
def loc(m):
    q=m.copy(); q.apply_transform(P)
    if q.volume<0: q.invert()
    return q
YB=(554.0,563.1); YT=(611.4,623.4); YP=(563.1,611.4)            # faces exatas das barras (sem filme nem degrau)
S0=61.6; G=0.15; PW=11.9                   # 3 pecas iguais entre as faces das pontas (+-184,8)
def BX(u0,u1,y0,y1,w0,w1): return B(u0,u1,y0,y1,w0,w1)
def CYLu(u0,u1,y,w,d): return CYL([u0,y,w],[u1,y,w],d)
def hexu(uc,y,w,h=2.4):
    n=trimesh.creation.cylinder(radius=3.3,height=h,sections=6); n.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0])); n.apply_translation([uc,y,w]); return n
def build(A,Bm,w0,w1,old,oldhole,TN,extra_holes=()):
    wm=0.5*(w0+w1); U_=U(A,Bm)
    U_=U(U_,BX(old[0],old[1],YP[0],YP[1],w0,w1),BX(0.5*(old[0]+old[1])-0.5,0.5*(old[0]+old[1])+0.5,YB[0],YT[1],w0,w1))   # emenda antiga vira poste macico
    if oldhole:                                                                       # SO_ONDE_PRECISA: sem poste espelhado; o poste da emenda antiga
        hc=oldhole[0][0]                                                              # fica so com 12 mm em volta do furo que tem funcao
        U_=D(U_,BX(old[0]-0.5,hc-6.0,YP[0],YP[1],w0-1,w1+1),BX(hc+6.0,old[1]+0.5,YP[0],YP[1],w0-1,w1+1))
    else: U_=D(U_,BX(old[0]-0.5,old[1]+0.5,YP[0],YP[1],w0-1,w1+1))                    # sem funcao: sai inteiro (janela limpa)
    U_=D(U_,BX(184.8,193.0,YP[0],YP[1],w0-1,w1+1),BX(-193.0,-184.8,YP[0],YP[1],w0-1,w1+1))   # ressaltos das pontas (furo +-188,9) sem funcao
    for s in (-S0,S0): U_=U(U_,BX(s-PW,s+PW,YP[0],YP[1],w0,w1))                       # postes das emendas novas
    for (u,y,ax) in oldhole: U_=D(U_,CYL([u,y,w0-1],[u,y,w1+1],3.4))                 # refura o furo que passava na emenda antiga
    # abas das porcas T (rasgo do perfil em w0-0.6)
    wc=w0-0.6
    for u in TN: U_=U(U_,BX(u-9,u+9,YT[0]+0.5,YT[1],w0-7.1,w0+0.7))
    for u in TN: U_=D(U_,CYL([u,YT[0]-1,wc],[u,YT[1]+1,wc],5.5),CYL([u,YT[0]-1,wc],[u,617.0,wc],9.5))
    # tres pecas
    TG={s:BX(s-G if s>0 else s-7.9,s+7.9 if s>0 else s+G,580.0,598.0,w0+3.4,w0+6.9) for s in (-S0,S0)}
    left=D(I(U_,BX(-400,-S0-G,500,700,w0-20,w1+20)),TG[-S0].bounding_box.copy() if False else BX(-S0-8.1,-S0-G+0.01,579.8,598.2,w0+3.2,w0+7.1))
    right=D(I(U_,BX(S0+G,400,500,700,w0-20,w1+20)),BX(S0+G-0.01,S0+8.1,579.8,598.2,w0+3.2,w0+7.1))
    cen=U(I(U_,BX(-S0+G,S0-G,500,700,w0-20,w1+20)),TG[-S0],TG[S0])
    # parafusos horizontais da emenda
    HW=[]
    for s in (-S0,S0):
        sg=np.sign(s); fo=s+sg*PW; fi=s-sg*PW            # face de fora (peca da ponta) e face de dentro (peca do meio)
        for y in (572.0,605.0):
            hole=CYLu(s-13,s+13,y,wm,3.4)
            cb=CYLu(fo-sg*3.0,fo+sg*1.0,y,wm,6.2)
            nut=hexu(fi+sg*1.2-sg*0.01,y,wm)
            if s>0: right=D(right,hole,cb); cen=D(cen,hole,nut)
            else:   left=D(left,hole,cb);  cen=D(cen,hole,nut)
            HW.append(U(CYLu(fo-sg*3.0-sg*0.0,fo-sg*3.0+sg*3.0,y,wm,5.5) if False else CYL([fo-sg*3.0,y,wm],[fo,y,wm],5.5),CYL([fo-sg*3.0,y,wm],[fo-sg*23.0,y,wm],3.0),hexu(fi+sg*1.2,y,wm,2.2)))
    for u in TN:
        HW.append(U(CYL([u,612.0,wc],[u,617.0,wc],8.5),CYL([u,617.0,wc],[u,627.0,wc],5.0),BX(u-5,u+5,625.3,628.4,wc-2.8,wc+2.8)))
    big=lambda m:max(m.split(only_watertight=False),key=lambda q:q.volume)
    return big(left),big(cen),big(right),U(*HW)
R={}
# frente (u=x, w=z)
fl,fc,fr,fh=build(TF['ref_supA'],TF['ref_supB'],255.6,265.85,(8.1,31.9),[],[-165.0,-40.0,40.0,165.0])   # sem torres: o poste do furo X 16,1 sai
R.update({'f_E':fl,'f_C':fc,'f_D':fr,'hw_frente':fh})
# lateral (quadro local), depois volta
L52=loc(trimesh.load(TD_+'052.stl')); L55=loc(trimesh.load(TD_+'055.stl'))
ll,lc,lr,lh=build(L52,L55,250.6,260.85,(88.1,111.9),[],[-150.0,-40.0,40.0,150.0])   # furo Z 96,1 era so o pino da emenda antiga
for k,m in (('l_T',ll),('l_C',lc),('l_F',lr),('hw_lat',lh)): R[k]=loc(m)
LOG={k:[bool(v.is_volume),np.round(v.bounds,1).tolist(),round(float(max(v.extents)),1)] for k,v in R.items()}
for a,b in (('f_E','f_C'),('f_C','f_D'),('l_T','l_C'),('l_C','l_F')): LOG[a+'x'+b]=round(I(R[a],R[b]).volume,3)
pickle.dump(R,open('SUP3.pkl','wb')); print(json.dumps(LOG))
