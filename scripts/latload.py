import json, trimesh
LD='/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/lat/'
L={}
for n,p,fn,bb,lb,v in json.load(open(LD+'index.json'))['itens']:
    k=n if n not in L else n+'@'+fn
    L[k]=trimesh.load(LD+fn)
