import trimesh, numpy as np, base64, json, pickle
sc=trimesh.load('/mnt/user-data/outputs/coluna_FD/MONTAGEM_coluna_frontal_D.glb')
cols=pickle.load(open('asm_cols.pkl','rb'))
NAMES={'01':'Cantoneira da base','02':'Coluna interna inferior','02b':'Calço da dobradiça inferior','03':'Coluna externa inferior',
 '04':'Chapa frontal inferior','05':'Capa verde inferior','06':'Suporte central','07':'Capa central','08':'Coluna interna superior',
 '08b':'Calço da dobradiça superior','09':'Coluna externa superior','10':'Chapa frontal superior','11':'Capa verde superior',
 '12':'Enchimento do canto do riser','13':'Cantoneira do riser (suporte)','14':'Cantoneira do riser (capa)','15':'Batente da porta 1/2','16':'Batente da porta 2/2'}
LAYER={'02':1,'08':1,'15':1,'16':1,'04':2,'10':2,'06':2,'03':3,'09':3,'02b':3,'08b':3,'01':4,'12':4,'13':4,'05':5,'11':5,'07':5,'14':5}
parts=[]; tot=0
for n,g in sc.geometry.items():
    m=trimesh.Trimesh(g.vertices,g.faces,process=True)
    if n=='REF_REF_impressora_2': m=trimesh.load('ref2_simpl.stl')
    if n.startswith('REF'):
        layer=0; num=''; label='Impressora (referência)'; c='ref'; target=6000
    elif n.startswith('fecho'):
        layer=6; num=''; label='Fecho '+n.split('_')[1]+' '+' '.join(n.split('_')[2:]); c=cols[n]; target=1500
    elif n.startswith('17'):
        layer=6; num='17'; y=n.split('_')[3]; label='Dobradiça K1 '+y.replace('Y','Y ')+' – '+' '.join(n.split('_')[4:]).replace('folha porta','folha da porta').replace('folha fixa','folha fixa'); c=cols[n]; target=4000
    else:
        num=n.split('_')[0]; layer=LAYER[num]; label=NAMES[num]; c=cols[n]; target=4000
    if len(m.faces)>target:
        try: m=m.simplify_quadric_decimation(face_count=target)
        except Exception as e: print('dec fail',n,e)
    v=np.asarray(m.vertices,np.float64); f=np.asarray(m.faces,np.uint32)
    lo=v.min(0); hi=v.max(0); sp=np.maximum(hi-lo,1e-6)
    q=np.round((v-lo)/sp*65535).astype(np.uint16)
    idx=f.astype(np.uint16) if len(v)<65536 else f
    tot+=len(f)
    parts.append(dict(id=n,num=num,label=label,layer=layer,color=c,lo=lo.round(3).tolist(),sp=sp.round(4).tolist(),
        v=base64.b64encode(q.tobytes()).decode(),i=base64.b64encode(idx.tobytes()).decode(),i32=int(len(v)>=65536),
        c=[round(x,2) for x in m.bounds.mean(0)]))
js='window.PARTS='+json.dumps(parts,separators=(',',':'))+';'
open('parts_data.js','w').write(js); print('faces',tot,'bytes',len(js))
