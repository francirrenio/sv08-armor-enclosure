# topo da lateral: acrilico sobe ate a altura do original (Y 529,3), banda fica fina (so por fora), peca de apoio aparafusada no batente original da impressora
import numpy as np, pickle, json, trimesh
exec(open('load.py').read()); exec(open('geo.py').read())
from shapely.geometry import Polygon
FB=pickle.load(open('FB.pkl','rb')); CF=pickle.load(open('CF.pkl','rb'))
T='/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/'
beam=trimesh.load(T+'060.stl'); cbr=trimesh.load(T+'062.stl'); cbrT=trimesh.load(T+'061.stl')
bandA=trimesh.load(T+'046.stl'); bandB=trimesh.load(T+'049.stl')
OUT={}; LOG={}
YT=529.3
# acrilico: borda de cima sobe de 522,8 para 529,3
acr=FB['acrilico_lat2']; ab=acr.bounds
acr=U(acr,B(277.5,280.5,ab[1][1]-0.5,YT,-210.2,219.9))
OUT['acrilico']=acr
# banda do topo mais fina: so a parte de fora (X 280,7-283,8), o acrilico passa por tras
OUT['bandaA']=I(bandA,B(280.7,290,500,600,-300,300)); OUT['bandaB']=I(bandB,B(280.7,290,500,600,-300,300))
# peca de apoio: encosta na travessa da impressora e no batente original; o acrilico apoia na face X 277,3
sec=Polygon([(265.2,523.7),(277.3,523.7),(277.3,557.6),(268.7,557.6),(268.7,529.7),(265.2,529.7)])
def prism_xy_z(poly,z0,z1):
    m=trimesh.creation.extrude_polygon(poly,z1-z0); m.apply_translation([0,0,z0]); return m
Z0,Z1,ZS=-223.8,206.8,20.0
ap=prism_xy_z(sec,Z0,Z1)
ap=D(ap,grow(beam,0.2),grow(cbr,0.2),grow(cbrT,0.2))
for z in (-211.3,0.0,211.3):
    if Z0<z<Z1: ap=D(ap,CYL([255,525.8,z],[290,525.8,z],3.4),CYL([274.3,525.8,z],[290,525.8,z],6.2))
apA=I(ap,B(250,290,500,600,Z0-1,ZS-0.1)); apB=I(ap,B(250,290,500,600,ZS+0.1,Z1+1))
tz=Polygon([(ZS+0.2,540.0),(ZS+0.2,546.0),(ZS-4.5,547.5),(ZS-4.5,538.5)])          # rabo de andorinha escondido na emenda
def prism_zy_y(poly,x0,x1): return prism_zy(poly,x0,x1)
tong=prism_zy(tz,269.5,276.5)
apB=U(apB,tong); apA=D(apA,prism_zy(tz.buffer(0.2,join_style=2),268.0,278.0))
OUT['apoio_A']=apA; OUT['apoio_B']=apB
def bolt(p,axis,Lg,d=3.0,hd=5.5,hh=3.0):
    p=np.array(p,float); a=np.array(axis,float); return U(CYL(p,p+a*hh,hd),CYL(p,p-a*Lg,d))
OUT['apoio_hw']=U(*[bolt([274.3,525.8,z],[1,0,0],12) for z in (-211.3,0.0)],bolt([270.5,525.8,211.3],[1,0,0],8))
# faixa batente: livra a travessa e o canto da impressora
fsup=D(FB['faixa_batente_sup'],grow(beam,0.2),grow(cbr,0.2))
fsup=D(fsup,CYL([255,525.8,211.3],[290,525.8,211.3],3.4),CYL([270.5,525.8,211.3],[290,525.8,211.3],6.2))   # faixa tambem presa no 3o furo do batente original
esp=B(269.5,272.0,538.0,548.0,206.6,211.0)                 # espiga da ponta da peca B entrando na faixa
apB=U(apB,esp); fsup=D(fsup,grow(esp,0.2))
OUT['apoio_B']=apB; OUT['faixa_sup']=fsup
chk={}
for a in ('apoio_A','apoio_B'):
    for k,m in (('acr',acr),('beam',beam),('canto',cbr),('cantoT',cbrT),('espinha',CF['espinha']),('faixa',OUT['faixa_sup']),('acab_sup',FB['acab_sup']),('bandaA',OUT['bandaA']),('bandaB',OUT['bandaB'])):
        chk[a+' x '+k]=round(I(OUT[a],m).volume,2)
for k,m in (('beam',beam),('bandaA',OUT['bandaA']),('bandaB',OUT['bandaB']),('espinha',CF['espinha']),('acab_sup',FB['acab_sup'])): chk['acr x '+k]=round(I(acr,m).volume,2)
chk['faixa x beam']=round(I(OUT['faixa_sup'],beam).volume,2)
for t in ('027','028','029','030','031'):
    mm=trimesh.load(T+t+'.stl')
    if mm.is_volume: chk['acr x fecho '+t]=round(I(acr,mm).volume,2)
LOG['interf']={k:v for k,v in chk.items() if v}
LOG['compr']=[round(OUT[k].bounds[1][2]-OUT[k].bounds[0][2],1) for k in ('apoio_A','apoio_B')]
pickle.dump(OUT,open('TL.pkl','wb')); print(json.dumps(LOG))
