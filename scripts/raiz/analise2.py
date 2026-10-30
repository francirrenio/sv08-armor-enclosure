"""Audit v2: classification, overlaps (enclosure x enclosure, enclosure x printer, + hinge meshes), gantry intrusion,
support graph (acrylic does not carry load), and a priority cut plan.
usage: python analise2.py AUD_DIR AUDP_DIR OUT_JSON [hinge_stl ...]"""
import json, numpy as np, trimesh, manifold3d as mf, collections, time, re, sys, os, glob
t0 = time.time()
AUD, AUDP, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HINGES = sys.argv[4:]


def load(dirn, man):
    meshes = {}; mans = {}
    for i, x in enumerate(man):
        t = trimesh.load(os.path.join(dirn, x['f']), process=True); t.merge_vertices(digits_vertex=4)
        T = np.array(x['T']).reshape(4, 4); T[:3, 3] *= 10.0; t.apply_transform(T)
        meshes[i] = t
        try:
            m = mf.Manifold(mf.Mesh(vert_properties=np.asarray(t.vertices, np.float32), tri_verts=np.asarray(t.faces, np.uint32)))
            mans[i] = m if m.status() == mf.Error.NoError else None
        except Exception:
            mans[i] = None
    return meshes, mans


E = json.load(open(os.path.join(AUD, 'manifest.json'))); P = json.load(open(os.path.join(AUDP, 'manifest.json')))
for h in HINGES:   # hinge meshes (world coordinates)
    E.append({'f': os.path.abspath(h), 'ok': True, 'body': os.path.basename(h)[:-4], 'occ': 'HINGE', 'T': list(np.eye(4).ravel()), 'ap': 'R59_body', 'bb': None, 'mesh': True})
em, ema = {}, {}
_m, _ma = load(AUD, [x for x in E if not x.get('mesh')])
n0 = len(_m)
for i in range(n0): em[i], ema[i] = _m[i], _ma[i]
for k, x in enumerate(E[n0:]):
    t = trimesh.load(x['f'], process=True); t.merge_vertices(digits_vertex=4)
    em[n0 + k] = t
    try:
        m = mf.Manifold(mf.Mesh(vert_properties=np.asarray(t.vertices, np.float32), tri_verts=np.asarray(t.faces, np.uint32)))
        ema[n0 + k] = m if m.status() == mf.Error.NoError else None
    except Exception:
        ema[n0 + k] = None
pm, pma = load(AUDP, P)
print('loaded', len(E), len(P), round(time.time() - t0), 'nonmanifold', [E[i]['body'] for i in ema if ema[i] is None][:20])


def kind(x):
    a = x['ap']; n = x['body']; o = x['occ']; last = o.split('+')[-1]
    s = n + ' ' + last
    if x.get('mesh'): return 'hinge'
    if a == 'R59_hardware' or re.search(r'M3x|M25_|M3_|M5|porca|parafuso|Ferragem|Ferragens|insert|pino_|ISO7380|77_T_|porca_T|aux eixo', s, re.I): return 'hw'
    if a == 'R59_glass' or re.search(r'acrilico|Acrilico|glass|vidro', s): return 'acr'
    if re.search(r'2020|perfil|chapa_canto|chapa_lateral|REF\b|_REF|REFERENCIA', s): return 'ref'
    if re.search(r'Tela', n): return 'screen'
    if a in ('R59_led',) or re.search(r'LED_REF|Vedante|vedacao|EPDM|Junta_Perimetral|Feltro', n): return 'seal'
    if a == 'R59_green' or re.search(r'verde|Verde|green|Green', n): return 'green'
    return 'black'


K = [kind(x) for x in E]
print(collections.Counter(K))
EB = np.array([em[i].bounds.ravel() for i in range(len(E))]); PB = np.array([pm[i].bounds.ravel() for i in range(len(P))])


def near(a, b, t=0.1): return not (a[3] < b[0] - t or b[3] < a[0] - t or a[4] < b[1] - t or b[4] < a[1] - t or a[5] < b[2] - t or b[5] < a[2] - t)


def rank(i):
    k = K[i]; n = E[i]['body'] + ' ' + E[i]['occ'].split('+')[-1]
    if k in ('hw', 'acr', 'ref', 'screen', 'hinge'): return 1.0
    if k == 'seal': return 9.0          # seals are compressed, never cut and never cut others
    if k == 'green': return 3.0
    if re.search(r'Enchimento', n): return 4.0
    if re.search(r'Riser_Cantoneira', n): return 2.5
    if re.search(r'Riser_|Banda_Topo|Display_Moldura|Persiana|Aleta', n): return 2.7
    return 2.0


ov = []
for i in range(len(E)):
    if ema[i] is None: continue
    for j in range(i + 1, len(E)):
        if ema[j] is None or not near(EB[i], EB[j], 0): continue
        v = (ema[i] ^ ema[j]).volume()
        if v > 0.3: ov.append([i, j, round(v, 2)])
op = []
for i in range(len(E)):
    if ema[i] is None: continue
    for j in range(len(P)):
        if pma[j] is None or not near(EB[i], PB[j], 0): continue
        v = (ema[i] ^ pma[j]).volume()
        if v > 0.3: op.append([i, j, round(v, 2)])
print('overlaps', len(ov), 'printer', len(op), round(time.time() - t0))

# gantry: region inside the aluminium frame faces, R1 U R2 (Y 81..523.5)
R1 = mf.Manifold.cube([2 * 226.5, 523.5 - 81.0, 2 * 273.5]).translate([-226.5, 81.0, -273.5])
R2 = mf.Manifold.cube([2 * 268.5, 523.5 - 81.0, 2 * 225.5]).translate([-268.5, 81.0, -225.5])
env = R1 + R2
gi = []
for i in range(len(E)):
    if ema[i] is None or K[i] not in ('black', 'green'): continue
    b = EB[i]
    if b[3] < -268.5 or b[0] > 268.5 or b[4] < 81.0 or b[1] > 523.5 or b[5] < -273.5 or b[2] > 273.5: continue
    v = (ema[i] ^ env).volume()
    if v > 0.3: gi.append([i, round(v, 2)])
print('gantry', len(gi), round(time.time() - t0))

# plan
plan = []; undecided = []
for i, j, v in ov:
    ri, rj = rank(i), rank(j)
    if 9.0 in (ri, rj): continue
    if K[i] in ('hw',) and K[j] in ('hw',): continue
    if ri == 1.0 and rj == 1.0: undecided.append([i, j, v, 'ref x ref']); continue
    if ri == rj: undecided.append([i, j, v, 'same rank']); continue
    tgt, tool = (i, j) if ri > rj else (j, i)
    if K[tgt] == 'hinge': undecided.append([i, j, v, 'hinge target']); continue
    plan.append({'target': tgt, 'tool': tool, 'vol': v})
for i, j, v in op:
    if K[i] in ('black', 'green'): plan.append({'target': i, 'tool': 'P%d' % j, 'vol': v})
    else: undecided.append([i, 'P%d' % j, v, 'nonprinted x printer'])
for i, v in gi: plan.append({'target': i, 'tool': 'GANTRY', 'vol': v})

# support graph: acrylic and seals do not carry; hw carries
N = len(E); adj = collections.defaultdict(set)
for i in range(N):
    if ema[i] is None or K[i] in ('acr', 'seal'): continue
    for j in range(i + 1, N):
        if ema[j] is None or K[j] in ('acr', 'seal') or not near(EB[i], EB[j], 0.1): continue
        if ema[i].min_gap(ema[j], 0.1) <= 0.05: adj[i].add(j); adj[j].add(i)
    for j in range(len(P)):
        if pma[j] is None or not near(EB[i], PB[j], 0.1): continue
        if ema[i].min_gap(pma[j], 0.1) <= 0.05: adj[i].add(('p', j))
anch = [i for i in range(N) if any(isinstance(x, tuple) for x in adj[i])]
seen = set(anch); st = list(anch)
while st:
    a = st.pop()
    for b in adj[a]:
        if isinstance(b, tuple): continue
        if b not in seen: seen.add(b); st.append(b)
floating = [i for i in range(N) if i not in seen and ema[i] is not None and K[i] not in ('seal',)]
print('floating', len(floating), round(time.time() - t0))


def nm(i):
    if isinstance(i, str): return i
    return '%s @%s' % (E[i]['body'], E[i]['occ'].split('+')[-1])


json.dump({'E': [{'body': x['body'], 'occ': x['occ'], 'kind': K[k]} for k, x in enumerate(E)], 'ov': ov, 'op': op, 'gi': gi, 'plan': plan, 'undecided': undecided,
           'floating': floating}, open(OUT, 'w'))
with open(OUT.replace('.json', '.txt'), 'w') as f:
    f.write('PLAN (target <- tool)\n')
    for p in sorted(plan, key=lambda p: -p['vol']):
        f.write('%9.1f  %s  <-  %s\n' % (p['vol'], nm(p['target']), nm(p['tool']) if not isinstance(p['tool'], str) else p['tool']))
    f.write('\nUNDECIDED\n')
    for u in sorted(undecided, key=lambda u: -u[2]):
        f.write('%9.1f  %s | %s  (%s)\n' % (u[2], nm(u[0]), nm(u[1]) if not isinstance(u[1], str) else u[1], u[3]))
    f.write('\nFLOATING\n')
    for i in floating:
        f.write('  %s [%s]\n' % (nm(i), K[i]))
print('done', round(time.time() - t0))
