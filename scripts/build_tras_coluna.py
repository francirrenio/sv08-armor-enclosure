# COLUNAS_TRAS: as colunas de tras (TD e, por espelho em X na pagina, TE) passam a ter o mesmo desenho da coluna FD.
# Cada peca da FD e espelhada em Z (frente -> tras). Na traseira nao ha porta: os furos das dobradicas (folha fixa, na perna
# lateral da espinha e nas verdes da coluna) sao fechados com o proprio perfil da peca (mesma secao extrudada), sem remendo.
# A lateral fica simetrica: riser, moldura das aletas, banda, apoio do acrilico, moldura+acabamento e acrilico = espelho da metade da frente.
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
P={pid:m for pid,lab,grp,m in pickle.load(open('parts.pkl','rb'))}
def mz(m):
    q=m.copy(); q.apply_transform(np.diag([1,1,-1,1]))
    if q.volume<0: q.invert()
    return q
def _secy(m,y):
    s_=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,_=s_.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float))
    from shapely.ops import unary_union as _uu
    return _uu([p for p in p2.polygons_full])
def _ext_xz(pg,y0,y1):
    ms=[]
    for g in (pg.geoms if hasattr(pg,'geoms') else [pg]):
        mm=trimesh.creation.extrude_polygon(g,y1-y0); mm.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
        if mm.volume<0: mm.invert()
        ms.append(mm)
    return U(*ms)
def fecha(m,yref,caixas):
    pr=_ext_xz(_secy(m,yref),min(c.bounds[0][1] for c in caixas)-0.5,max(c.bounds[1][1] for c in caixas)+0.5)
    return max(U(m,*[I(pr,c) for c in caixas]).split(only_watertight=False),key=lambda p:p.volume)
DH=(-6.75,5.25); ZB=-266.0
T={}
src={'esp_lat_inf':'esp1','esp_lat_sup':'esp1s','esp_fre_inf':'espF','esp_fre_sup':'espFs','verde_72':'v72','verde_sup':'vsup1','capa_74':'capa74',
     'hw_capa':'hwCapa','batente_inf':'fbI','batente_sup':'fbS','fix_espinha':'fixesp','hw_verdes':'hwcol','cant_top':'thCantF','sup_canto':'thSupF',
     'hw_topo':'hwTopo','riser':'riser47','mold_aletas':'molAl47','banda':'bandaB','apoio_acr':'apB','moldura_inf':'acI','moldura_sup':'acS','hw_moldura':'acHW'}
for k,s in src.items(): T[k]=mz(P[s])
# furos das dobradicas: fechados (espinha lateral: furo 3,4 + bolsa da porca X 272-275,6; verdes: furo 3,4)
for k,yc in (('esp_lat_inf',150.0),('esp_lat_sup',450.0)):
    T[k]=fecha(T[k],yc,[B(270.0,284.5,yc+d-3.6,yc+d+3.6,ZB-4.0,ZB+4.0) for d in DH])
for k,yc in (('verde_72',150.0),('verde_sup',450.0)):
    T[k]=fecha(T[k],yc,[B(277.0,285.5,yc+d-2.6,yc+d+2.6,ZB-4.0,ZB+4.0) for d in DH])
# acrilico lateral simetrico: metade da frente + espelho
a=P['acrL1']; af=I(a,B(270,290,0,700,-0.01,300)); T['acrilico_lat']=U(af,mz(af))
# conferencia: furos fechados de verdade
chk={}
for k,yc in (('esp_lat_inf',150.0),('esp_lat_sup',450.0),('verde_72',150.0),('verde_sup',450.0)):
    xs=np.arange(271,285,0.25); pts=[[x,yc+d,ZB] for d in DH for x in xs]
    chk['vazio_'+k]=int((~T[k].contains(np.array(pts))).sum())
ENV=['base','perfT','apT','topImp','pLA','v24','v15','trD','trE','trL','fechos','acHW']
for k,m in T.items():
    for e in ENV:
        v=P[e]
        if np.any(v.bounds[0]>m.bounds[1]) or np.any(v.bounds[1]<m.bounds[0]): continue
        try: x=I(m,v).volume
        except Exception: x=-1
        if x>0.5 or x<0: chk[k+'_x_'+e]=round(x,1)
RL=pickle.load(open('RL.pkl','rb')); eT=RL['est_tras']
for k,m in T.items():
    if np.any(eT.bounds[0]>m.bounds[1]) or np.any(eT.bounds[1]<m.bounds[0]): continue
    x=I(m,eT).volume
    if x>0.5: chk[k+'_x_estTras']=round(x,1)
chk['vol']={k:bool(v.is_volume) for k,v in T.items()}
pickle.dump(T,open('TC.pkl','wb')); print(json.dumps(chk,default=str))
