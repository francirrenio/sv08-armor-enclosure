import json, numpy as np
R=json.load(open('m25plan.json'))
ops=[]; hw=[]; hide=[]
def P(r,t):
    c=np.array(r['center'],float); c[r['axis']]=r['head_end']+r['dir'][r['axis']]*t; return [round(v,3) for v in c]
for r in R:
    st=r['stack']; mode=r['mode']
    green=[l for l in st if l[3]=='green']; black=[l for l in st if l[3]=='black']
    g0=st[0][0]                       # visible surface
    hb=g0+0.9                         # head bottom (recess 0.9)
    tgt=lambda l:(l[4],l[2])
    # recess + clearance in green
    for l in green:
        ops.append({'t':tgt(l),'op':'cut','cyl':[P(r,g0-1.0),P(r,hb),3.25]})
        ops.append({'t':tgt(l),'op':'cut','cyl':[P(r,g0-1.0),P(r,l[1]+0.5),1.7]})
    if mode=='nut':
        lb=black[-1]; inner=r['inner']; th=lb[1]-lb[0]
        for l in black:
            ops.append({'t':tgt(l),'op':'cut','cyl':[P(r,l[0]-0.5),P(r,inner+3.5),1.7]})
        if th>=5.5:
            nut0,nut1=inner-2.9,inner-0.5; pocket=[P(r,inner-3.0),P(r,inner+0.5)]
            L=12
        else:
            ops.append({'t':tgt(lb),'op':'join','cyl':[P(r,inner-0.2),P(r,inner+3.0),5.5]})
            pocket=[P(r,inner+0.4),P(r,inner+3.5)]; nut0,nut1=inner+0.5,inner+2.9
            L=10
        ops.append({'t':tgt(lb),'op':'cut','hex':[pocket[0],pocket[1],5.7]})
        ops.append({'t':tgt(lb),'op':'cut','cyl':[P(r,lb[0]-0.5),P(r,inner+3.5),1.7]})
        hw.append({'comp_of':[r['occ'],r['name']],'name':'M3x%d ISO7380'%L,'screw':[P(r,hb),P(r,hb+L)],'head':[P(r,hb-1.65),P(r,hb)]})
        hw.append({'comp_of':[r['occ'],r['name']],'name':'porca M3','hex':[P(r,nut0),P(r,nut1),5.5]})
    else:
        L=8; tip=hb+L
        for l in black:
            ops.append({'t':tgt(l),'op':'cut','cyl':[P(r,l[0]-0.5),P(r,min(tip+0.6,l[1]+0.5) if l is not black[-1] else tip+0.6),1.25]})
        hw.append({'comp_of':[r['occ'],r['name']],'name':'M3x%d ISO7380 autoatarraxante'%L,'screw':[P(r,hb),P(r,tip)],'head':[P(r,hb-1.65),P(r,hb)]})
    hide.append([r['occ'],r['name']])
json.dump({'ops':ops,'hw':hw,'hide':hide},open('/mnt/user-data/outputs/revisao/m3_ops.json','w'))
import collections
print(len(ops),len(hw),len(hide), collections.Counter(r['mode'] for r in R))
