# MECANISMO DAS ALETAS: veneziana fixa + placa corredica + 1 servo no centro (Klipper)
# Na espessura do riser, de dentro para fora:
#   X 275,2-277,1  labios que seguram a placa pelas bordas de cima e de baixo (|Z| >= 21)
#   X 276,6-278,0  placa corredica, desliza 12 mm em Z no canal do riser (janela 11 / barra 13, passo 24)
#   X 278,2-279,4  pente fixo do riser (janela 12 / barra 12, passo 24)
#   X 279,3-284,0  6 aletas fixas a 45 graus, parte do riser
#   X 284,0-288,0  moldura verde (sem mudanca)
# Servo MG90S por dentro, no centro, eixo vertical (Y), preso num berco que faz parte do riser (2 de 2).
# Pinhao m1 z10 (raio primitivo 5); as 2 cremalheiras ficam do mesmo lado do pinhao, em alturas diferentes,
# entao as 2 placas andam juntas no mesmo sentido: aberto = janelas alinhadas; fechado = placas 12 mm para -Z.
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
from shapely.geometry import Polygon
from shapely.ops import unary_union
CT=pickle.load(open('CT_before_mech.pkl','rb'))
ZO,YO=(58.0,196.0),(574.0,618.0)
WIN=[(ZO[0]+24.0*k,ZO[0]+24.0*k+12.0) for k in range(6)]   # janelas do pente fixo: Z 58-70, 82-94, ..., 178-190
CURSO=12.0
XC,ZP,RP,MOD=267.5,-5.5,5.0,1.0                            # eixo do servo/pinhao (x,z), raio primitivo, modulo
XR=XC+RP                                                   # linha primitiva das cremalheiras (X 272,5)
XRB=276.3                                                  # costas das cremalheiras (0,3 da placa)
YA,YB=(588.6,594.4),(594.8,600.6)                          # faixas das cremalheiras A (placa da frente) e B (placa de tras)

def ext_xz(poly,y0,y1):
    m=trimesh.creation.extrude_polygon(poly,y1-y0)
    m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
def ext_xy(poly,z0,z1):
    m=trimesh.creation.extrude_polygon(poly,z1-z0); m.apply_translation([0,0,z0])
    if m.volume<0: m.invert()
    return m
def zz(s,a,b): return (min(s*a,s*b),max(s*a,s*b))

def cremalheira(z0,z1,y):
    # dentes de 20 graus, passo pi*m, voltados para -X; vao centrado no pinhao (Z = ZP) na posicao ABERTA
    p=np.pi*MOD; xt,xr=XR-1.0*MOD,XR+1.25*MOD
    ht,hr=(p/2-2*1.0*MOD*np.tan(np.radians(20)))/2-0.1,(p/2+2*1.25*MOD*np.tan(np.radians(20)))/2-0.1   # 0,2 de folga no dente
    polys=[Polygon([(xr,z0),(XRB,z0),(XRB,z1),(xr,z1)])]
    k0=int(np.floor((z0-ZP)/p))-1; k1=int(np.ceil((z1-ZP)/p))+1
    for k in range(k0,k1):
        zc=ZP+p/2+k*p
        if zc-hr<z0 or zc+hr>z1: continue
        polys.append(Polygon([(xr+0.01,zc-hr),(xt,zc-ht),(xt,zc+ht),(xr+0.01,zc+hr)]))
    return ext_xz(unary_union(polys),*y)
def pinhao():
    z=10; ra,rf=RP+MOD,RP-1.25*MOD; P=2*np.pi/z; da,dr=0.4/ra,np.radians(15)
    pts=[]
    for k in range(z):
        t=k*P
        for r,a in ((rf,t-dr),(ra,t-da),(ra,t+da),(rf,t+dr)): pts.append((XC+r*np.cos(a),ZP+r*np.sin(a)))
    g=Polygon(pts)
    m=U(ext_xz(g,YA[0]-0.2,YB[1]+0.2),ext_xz(Polygon([(XC+3.5*np.cos(a),ZP+3.5*np.sin(a)) for a in np.linspace(0,2*np.pi,40)[:-1]]),588.3,YA[0]))
    m=D(m,CYL([XC,587.0,ZP],[XC,591.0,ZP],5.0),CYL([XC,590.0,ZP],[XC,602.0,ZP],2.2))   # cubo no estriado do servo + parafuso M2 do braco
    return m
def lamina(yt):   # aleta fixa a 45 graus, borda de fora mais baixa (agua/luz nao passam reto)
    return Polygon([(279.3,yt),(284.0,yt-4.7),(284.0,yt-6.7),(279.3,yt-2.0)])

out={}
for nome,s in (('riser47',+1),('riser35',-1)):
    r=CT[nome]
    # canal da placa ate |Z| 210 (frente, aberto) / 222 (tras, fechado)
    r=D(r,B(276.9,278.2,567.8,624.2,*zz(s,150.0,210.0 if s>0 else 222.0)))
    # pente fixo + 6 aletas fixas dentro da abertura
    zo=zz(s,*ZO)
    pente=D(B(278.2,279.4,YO[0],YO[1],*zo),*[B(278.0,279.6,YO[0]+1.0,YO[1]-1.0,*zz(s,a,b)) for a,b in WIN])
    lam=[ext_xy(lamina(618.0-k*44.0/6.0),*zo) for k in range(6)]
    r=U(r,pente,*lam)
    # labios (bordas de cima e de baixo da placa), longe do berco do servo
    lz=zz(s,21.0,210.0 if s>0 else 222.0)
    r=U(r,B(275.2,277.1,565.6,567.8,*lz),B(275.2,276.3,565.6,570.2,*lz),
          B(275.2,277.1,624.2,626.4,*lz),B(275.2,276.3,621.8,626.4,*lz))
    out[nome]=r

# berco do servo: faz parte do riser (2 de 2), atravessa a emenda por dentro e se apoia no (1 de 2)
berco=U(B(261.5,276.3,558.6,577.0,-19.0,19.0),B(276.3,277.1,558.6,565.5,0.0,19.0),B(276.3,277.0,558.6,565.5,-19.0,0.0))
berco=D(berco,B(261.0,273.8,561.3,590.0,-11.6,11.6))                                  # bolsa do corpo do servo (aberta para dentro)
berco=D(berco,*[CYL([XC,568.0,z],[XC,578.0,z],1.8) for z in (-13.9,13.9)])            # M2 das abas do servo
b47=I(berco,B(260,280,550,600,0.0,20.0)); b35=I(berco,B(260,276.95,550,600,-20.0,0.0))
r47=U(out['riser47'],b47,b35)
out['riser47']=max(r47.split(only_watertight=False),key=lambda p:p.volume)
out['riser35']=max(out['riser35'].split(only_watertight=False),key=lambda p:p.volume)

def placa(s,dz=0.0):
    pz=zz(s,14.0,208.0)
    pl=B(276.6,278.0,568.0,624.0,*pz)
    pl=D(pl,*[B(276.4,278.2,YO[0]+1.0,YO[1]-1.0,*zz(s,a+0.5,b-0.5)) for a,b in WIN])
    if s>0: pl=U(pl,cremalheira(-13.5,30.0,YA),B(XR+1.2,277.0,YA[0],YA[1],14.0,30.0))
    else:   pl=U(pl,cremalheira(-30.0,15.0,YB),B(XR+1.2,277.0,YB[0],YB[1],-30.0,-14.0))
    pl=max(pl.split(only_watertight=False),key=lambda p:p.volume)
    if dz: pl=pl.copy(); pl.apply_translation([0,0,dz])
    return pl
for nome,s in (('riser47',+1),('riser35',-1)):
    out[nome+'_placa']=placa(s); out[nome+'_placa_f']=placa(s,-CURSO)

# servo MG90S (referencia): corpo 22,8 x 12,2 x 22,5; abas a 15,6 da base; torre e estriado no eixo
servo=U(B(XC-6.1,XC+6.1,561.5,584.0,ZP-5.9,ZP+16.9),B(XC-6.1,XC+6.1,577.1,579.6,-16.1,16.1),
        CYL([XC,584.0,ZP],[XC,588.0,ZP],11.8),CYL([XC,588.0,ZP],[XC,591.0,ZP],4.8))
pin=pinhao()
pin_f=pin.copy(); pin_f.apply_transform(trimesh.transformations.rotation_matrix(CURSO/RP,[0,1,0],[XC,0,ZP]))   # girado 137,5 graus (fechado)

# conferencias
chk={}
for st in ('','_f'):
    a,b=out['riser47_placa'+st],out['riser35_placa'+st]
    for nm,m in (('r47',out['riser47']),('r35',out['riser35']),('servo',servo),('pinhao',pin if st=='' else pin_f)):
        chk['A'+st+'_x_'+nm]=I(a,m).volume; chk['B'+st+'_x_'+nm]=I(b,m).volume
    chk['A_x_B'+st]=I(a,b).volume
chk['servo_x_r47']=I(servo,out['riser47']).volume; chk['servo_x_r35']=I(servo,out['riser35']).volume
chk['pin_x_servo']=I(pin,servo).volume; chk['pin_x_r47']=I(pin,out['riser47']).volume
outros=[k for k in CT if k not in ('riser47','riser35') and not k.startswith('riser') and isinstance(CT[k],trimesh.Trimesh)]
for k in outros:
    v=sum(I(CT[k],m).volume for m in (out['riser47'],out['riser35'],servo,pin,out['riser47_placa'],out['riser35_placa'],out['riser47_placa_f'],out['riser35_placa_f']))
    if v>0.01: chk['CT_'+k]=v
for f in ('050','051','052','055','043','053'):
    t=trimesh.load('../ltop/'+f+'.stl')
    if not t.is_volume: t=t.convex_hull if f!='053' else None
    if t is None: continue
    v=sum(I(t,m).volume for m in (servo,pin,out['riser47_placa'],out['riser35_placa'],out['riser47_placa_f'],out['riser35_placa_f']))
    if v>0.01: chk['lt_'+f]=v
# folgas: cremalheira x pinhao (tem que haver dente no vao, sem bater)
chk['vol_r47']=out['riser47'].volume; chk['r47_ok']=float(out['riser47'].is_volume); chk['r35_ok']=float(out['riser35'].is_volume)
chk['pA_ok']=float(out['riser47_placa'].is_volume); chk['pB_ok']=float(out['riser35_placa'].is_volume)
chk['len_pA']=float(np.ptp(out['riser47_placa'].bounds[:,2])); chk['len_pB']=float(np.ptp(out['riser35_placa'].bounds[:,2]))
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}))
CT.update(out); CT['servo']=servo; CT['pinhao']=pin; CT['pinhao_f']=pin_f
pickle.dump(CT,open('CT.pkl','wb'))
