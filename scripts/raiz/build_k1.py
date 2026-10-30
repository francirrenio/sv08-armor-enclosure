"""K1 print-in-place geared hinge (270 deg) adapted to the SV08 V2 lower doors.
Right-door local frame (mm): X right, Y up (hinge centre Y=0), Z front.
Door axis D, fixed axis F. Original gears + cage kept within r=11; new leaves added."""
import trimesh, numpy as np, manifold3d as mf, json, sys, os

SRC = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

Ds = np.array([485.6, 294.39]); Fs = np.array([495.6, 284.39]); ZC = -57.175
D = np.array([282.4, 294.6]); F = D + (Fs - Ds)          # F = (292.4, 284.6)
RCORE = 11.0

m = trimesh.load(SRC)
A0, B0, C0 = [p for p in m.split(only_watertight=False) if len(p.faces) > 100]

# STL (x, y, z) -> local (X, Y, Z) = (x - Ds.x + D.x, z - ZC, y - Ds.y + D.z)   (reflection, trimesh fixes winding)
T = np.array([[1, 0, 0, D[0] - Ds[0]],
              [0, 0, 1, -ZC],
              [0, 1, 0, D[1] - Ds[1]],
              [0, 0, 0, 1]], float)
for p in (A0, B0, C0):
    p.apply_transform(T)

def to_mf(t):
    return mf.Manifold(mf.Mesh(vert_properties=np.asarray(t.vertices, np.float32), tri_verts=np.asarray(t.faces, np.uint32)))

def to_tm(x):
    me = x.to_mesh(); return trimesh.Trimesh(me.vert_properties[:, :3], me.tri_verts, process=False)

def box(x0, x1, y0, y1, z0, z1):
    return mf.Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])

def cbox(x0, x1, y0, y1, z0, z1, c=1.0):
    pts = []
    for (a, b, cc) in ((c, c, 0), (c, 0, c), (0, c, c)):
        for X in (x0 + a, x1 - a):
            for Y in (y0 + b, y1 - b):
                for Z in (z0 + cc, z1 - cc):
                    pts.append([X, Y, Z])
    return mf.Manifold.hull_points(pts)

def cylY(cx, cz, r, y0, y1, n=96):
    return mf.Manifold.cylinder(y1 - y0, r, r, n).rotate([-90, 0, 0]).translate([cx, y0, cz])

def cylX(y, z, r, x0, x1, n=48):
    return mf.Manifold.cylinder(x1 - x0, r, r, n).rotate([0, 90, 0]).translate([x0, y, z])

def cylZ(x, y, r, z0, z1, n=48):
    return mf.Manifold.cylinder(z1 - z0, r, r, n).translate([x, y, z0])

A = to_mf(A0); B = to_mf(B0)
print('A,B status', A.status(), B.status(), round(A.volume(), 1), round(B.volume(), 1))
ya0, ya1 = A0.bounds[0][1], A0.bounds[1][1]
yb0, yb1 = B0.bounds[0][1], B0.bounds[1][1]
print('Y ranges A %.2f..%.2f  B %.2f..%.2f  C %.2f..%.2f' % (ya0, ya1, yb0, yb1, C0.bounds[0][1], C0.bounds[1][1]))

# ---- door block (A'): core + leaf over door frame and column front ----
LEAF_A = dict(x0=222.0, x1=D[0] - 5.6, z0=D[1] - 8.0, z1=D[1] + 2.4)   # Z 286.6..297.0
Ap = (A ^ cylY(D[0], D[1], RCORE, ya0 - 1, ya1 + 1)) + cbox(LEAF_A['x0'], LEAF_A['x1'], ya0, ya1, LEAF_A['z0'], LEAF_A['z1'], 1.0)
Ap = Ap + cbox(222.0, 233.0, ya0, ya1, 286.0, LEAF_A['z0'] + 1.5, 0.4)          # 0.6 pad seated on the door frame
SA = []
for yy in (-9.0, 9.0):
    Ap = Ap - cylZ(231.0, yy, 1.7, 280.0, 300.0) - cylZ(231.0, yy, 3.1, LEAF_A['z1'] - 3.2, 300.0)
    SA.append([231.0, yy])

# ---- fixed block (B'): core + leaf against the column side face ----
LEAF_B = dict(x0=283.8, x1=F[0] + 3.6, z0=255.0, z1=F[1] - 5.6)        # X 283.8..296.0 (seated on the black boss), Z 255..279.0
Bp = (B ^ cylY(F[0], F[1], RCORE, yb0 - 1, yb1 + 1)) + cbox(LEAF_B['x0'], LEAF_B['x1'], yb0, yb1, LEAF_B['z0'], LEAF_B['z1'], 1.0)
SB = []
for yy in (-9.0, 9.0):
    Bp = Bp - cylX(yy, 266.0, 1.7, 270.0, 300.0) - cylX(yy, 266.0, 3.1, LEAF_B['x1'] - 3.2, 300.0)
    SB.append([yy, 266.0])
print('A\',B\' status', Ap.status(), Bp.status(), round(Ap.volume(), 1), round(Bp.volume(), 1), 'genus', Ap.genus(), Bp.genus())

# ---- kinematic check, planar rotation about +Y (X,Z plane); positive angle = Y-rotation ----
def rotY(t, deg, cx, cz):
    return t.translate([-cx, 0, -cz]).rotate([0, deg, 0]).translate([cx, 0, cz])

def door_pose(t, phi):            # door = Rot_F(phi) o Rot_D(phi)
    return rotY(rotY(t, phi, D[0], D[1]), phi, F[0], F[1])

# cage envelope (stadium r=5.1 around D-F, at plate levels) for leaf clearance
cyl = trimesh.creation.cylinder
env = mf.Manifold.hull_points(np.vstack([
    np.array([[D[0] + 5.1 * np.cos(a), y, D[1] + 5.1 * np.sin(a)] for a in np.linspace(0, 2 * np.pi, 48) for y in (C0.bounds[0][1], C0.bounds[1][1])]),
    np.array([[F[0] + 5.1 * np.cos(a), y, F[1] + 5.1 * np.sin(a)] for a in np.linspace(0, 2 * np.pi, 48) for y in (C0.bounds[0][1], C0.bounds[1][1])])]))
res = {'sense': {}}
for sgn in (1, -1):
    worst = 0.0
    for phi in np.arange(0, 135.01, 2.5):
        v = (door_pose(Ap, sgn * phi) ^ Bp).volume()
        worst = max(worst, v)
    res['sense'][sgn] = round(worst, 3)
print('A\' x B\' worst overlap by sense', res['sense'])
sgn = 1 if res['sense'][1] <= res['sense'][-1] else -1
gaps = []
leafA = cbox(LEAF_A['x0'], LEAF_A['x1'], ya0, ya1, LEAF_A['z0'], LEAF_A['z1'], 1.0)
leafB = cbox(LEAF_B['x0'], LEAF_B['x1'], yb0, yb1, LEAF_B['z0'], LEAF_B['z1'], 1.0)
minA = minB = minAB = 99
for phi in np.arange(0, 135.01, 2.5):
    cg = rotY(env, sgn * phi, F[0], F[1])
    minA = min(minA, door_pose(leafA, sgn * phi).min_gap(cg, 5))
    minB = min(minB, leafB.min_gap(cg, 5))
    minAB = min(minAB, door_pose(leafA, sgn * phi).min_gap(Bp, 5))
print('sense used', sgn, 'min gap leafA-cage %.2f leafB-cage %.2f leafA-B\' %.2f' % (minA, minB, minAB))
for phi in (0, 45, 90, 135):
    bb = door_pose(Ap, sgn * phi).bounding_box()
    print('phi', phi, 'A\' bbox', np.round(bb, 1).tolist())

# ---- export ----
C = C0.copy()
def save(t, name):
    (t if isinstance(t, trimesh.Trimesh) else to_tm(t)).export(os.path.join(OUT, name))

MIR = np.diag([-1, 1, 1, 1.0])
for side in ('D', 'E'):
    for part, t in (('a_folha_porta', to_tm(Ap)), ('b_folha_fixa', to_tm(Bp)), ('c_gaiola', C.copy())):
        if side == 'E':
            t = t.copy(); t.apply_transform(MIR)
        save(t, 'local_%s_%s.stl' % (side, part))
    # print orientation: model Y -> print z (bed at the plate bottom), model Z -> print -y
    R = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1.0]])
    parts = []
    for part in ('a_folha_porta', 'b_folha_fixa', 'c_gaiola'):
        t = trimesh.load(os.path.join(OUT, 'local_%s_%s.stl' % (side, part)))
        t.apply_transform(R); parts.append(t)
    allp = trimesh.util.concatenate(parts)
    sh = -allp.bounds[0]; sh[0] -= 0;
    for t in parts: t.apply_translation(sh)
    trimesh.util.concatenate(parts).export(os.path.join(OUT, 'SV-30-0%s_dobradica_K1_270_%s_imprimir_x2.stl' % ('5' if side == 'D' else '6', 'direita' if side == 'D' else 'esquerda')))
json.dump({'D': D.tolist(), 'F': F.tolist(), 'sense': sgn, 'ya': [ya0, ya1], 'yb': [yb0, yb1],
           'yc': [float(C0.bounds[0][1]), float(C0.bounds[1][1])], 'screwsA': SA, 'screwsB': SB,
           'leafA': LEAF_A, 'leafB': LEAF_B}, open(os.path.join(OUT, 'params.json'), 'w'), indent=1)
print('done')
