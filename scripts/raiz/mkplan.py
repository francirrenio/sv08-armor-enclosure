import json, sys, collections
A = json.load(open(sys.argv[1])); M = json.load(open(sys.argv[2])); MP = json.load(open(sys.argv[3])); OUT = sys.argv[4]
E = A['E']
plan = list(A['plan'])
# owner decisions for same-rank pairs
for i, j, v, why in A['undecided']:
    if why != 'same rank': continue
    ni, nj = E[i]['body'], E[j]['body']
    def pick(a, b):  # target a, tool b
        plan.append({'target': a, 'tool': b, 'vol': v})
    if 'Riser_Lateral' in ni and ('Persiana_Fundo' in nj or 'Banda_Topo' in nj): pick(i, j)
    elif 'Riser_Lateral' in nj and ('Persiana_Fundo' in ni or 'Banda_Topo' in ni): pick(j, i)
    elif 'Parede' in ni and 'Banda_Topo' in nj: pick(i, j)
    elif 'Parede' in nj and 'Banda_Topo' in ni: pick(j, i)
    else: print('left undecided', ni, nj, v)
groups = collections.OrderedDict()
for p in sorted(plan, key=lambda p: p['target']):
    t = p['target']
    if E[t]['occ'] == 'HINGE': continue
    key = (E[t]['occ'], E[t]['body'])
    g = groups.setdefault(key, {'occ': E[t]['occ'], 'body': E[t]['body'], 'tools': []})
    tl = p['tool']
    if tl == 'GANTRY': g['tools'].append({'kind': 'gantry'})
    elif isinstance(tl, str) and tl.startswith('P'):
        x = MP[int(tl[1:])]; g['tools'].append({'kind': 'body', 'occ': x['occ'], 'body': x['body'], 'clr': 0.2})
    else:
        if E[tl]['occ'] == 'HINGE': continue
        g['tools'].append({'kind': 'body', 'occ': E[tl]['occ'], 'body': E[tl]['body'], 'clr': 0.2})
json.dump(list(groups.values()), open(OUT, 'w'), indent=0)
print('targets', len(groups), 'tools', sum(len(g['tools']) for g in groups.values()))
