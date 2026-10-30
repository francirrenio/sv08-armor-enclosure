import pickle,numpy as np,trimesh
from shapely.geometry import Polygon
exec(open('load.py').read()); exec(open('geo.py').read()); exec(open('latload.py').read())
RL=pickle.load(open('RL.pkl','rb')); FB=pickle.load(open('FB.pkl','rb')); CT=pickle.load(open('CT.pkl','rb')); TL=pickle.load(open('TL.pkl','rb')) if __import__('os').path.exists('TL.pkl') else {}
XF,XS1,YT=268.7,276.8,81.0
_lab=Polygon([(XF,YT),(277.3,YT),(277.3,YT+4.4),(276.7,YT+5.0),(XF+1.0,YT+5.0),(XF,YT+4.0)])
lab=prism_xy(_lab,-261,261)
O={'acril_CT':CT['acrilico_lat']}
for d,p in ((FB,'FB_'),(RL,'RL_'),(TL,'TL_'),(CT,'CT_')):
    for k,v in d.items(): O[p+k]=v
for k,v in list(M.items())+list(L.items()):
    try:
        b=v.bounds
        if b[1][0]>268 and b[0][0]<278 and b[0][1]<86 and b[1][1]>81: O['M_'+k]=v
    except Exception: pass
for k,v in O.items():
    try:
        x=I(lab,v); vol=x.volume
        if vol>0.01: print(k,round(vol,1),'Z',np.round([x.bounds[0][2],x.bounds[1][2]],1))
    except Exception as ex: print(k,'ERR',str(ex)[:50])
