import json, os, trimesh, numpy as np
D='/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/pe/COLUNA_FD/'
idx=json.load(open(D+'index.json'))['itens']
M={}; INFO={}
for n,p,fn,bb,lb,v in idx:
    k=n if n not in M else n+'@'+fn
    M[k]=trimesh.load(D+fn); INFO[k]=(p,lb,bb)
