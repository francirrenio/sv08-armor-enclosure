"""Height-map relief renderer for the SV08 V2 front view (mm, Y up, front = +Z)."""
import math, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from shapely.geometry import Polygon, Point, box
from shapely import affinity
from shapely.ops import unary_union

S = 4.0
XMIN, XMAX, YMIN, YMAX = -300, 300, -5, 995
W, H = int((XMAX - XMIN) * S), int((YMAX - YMIN) * S)
REVEAL = 0.5

MAT = {  # albedo, spec, shininess, emissive
    'void':   ((24, 24, 23), 0.0, 1, 0),
    'blk':    ((47, 47, 46), 0.16, 16, 0),
    'grn':    ((88, 102, 60), 0.10, 12, 0),
    'glass':  ((64, 76, 86), 0.55, 70, 0),
    'screw':  ((40, 40, 42), 0.55, 40, 0),
    'led':    ((255, 168, 72), 0.2, 30, 1),
    'screen': ((14, 18, 22), 0.6, 90, 0),
    'pin':    ((120, 120, 122), 0.7, 60, 0),
}
MID = {k: i for i, k in enumerate(MAT)}

Hm = np.zeros((H, W), np.float32)
M = np.full((H, W), MID['void'], np.uint8)


def cham(x0, y0, x1, y1, c=0):
    if not isinstance(c, (tuple, list)):
        c = (c, c, c, c)  # bl, br, tr, tl
    bl, br, tr, tl = c
    pts = [(x0 + bl, y0), (x1 - br, y0), (x1, y0 + br), (x1, y1 - tr), (x1 - tr, y1), (x0 + tl, y1), (x0, y1 - tl), (x0, y0 + bl)]
    out = []
    for p in pts:
        if not out or abs(p[0] - out[-1][0]) > 1e-6 or abs(p[1] - out[-1][1]) > 1e-6:
            out.append(p)
    if abs(out[0][0] - out[-1][0]) < 1e-6 and abs(out[0][1] - out[-1][1]) < 1e-6:
        out.pop()
    return Polygon(out)


def mirror(p):
    return affinity.scale(p, xfact=-1, yfact=1, origin=(0, 0))


def px(x, y):
    return ((x - XMIN) * S, (YMAX - y) * S)


def raster(poly):
    """mask + distance-to-edge (mm) on a crop. returns (r0, c0, mask, dist)."""
    minx, miny, maxx, maxy = poly.bounds
    c0 = max(int((minx - XMIN) * S) - 3, 0)
    c1 = min(int((maxx - XMIN) * S) + 4, W)
    r0 = max(int((YMAX - maxy) * S) - 3, 0)
    r1 = min(int((YMAX - miny) * S) + 4, H)
    im = Image.new('L', (c1 - c0, r1 - r0), 0)
    d = ImageDraw.Draw(im)
    for g in getattr(poly, 'geoms', [poly]):
        d.polygon([(a - c0, b - r0) for a, b in (px(*q) for q in g.exterior.coords)], fill=255)
        for hole in g.interiors:
            d.polygon([(a - c0, b - r0) for a, b in (px(*q) for q in hole.coords)], fill=0)
    m = np.asarray(im) > 127
    dist = ndimage.distance_transform_edt(m) / S
    return r0, c0, m, dist


def add(poly, z, ch, mat, both=True, reveal=REVEAL, round_=False):
    polys = [poly, mirror(poly)] if both else [poly]
    for p in polys:
        q = p.buffer(-reveal, join_style=2) if reveal else p
        if q.is_empty:
            continue
        r0, c0, m, dist = raster(q)
        if round_:  # quarter-round profile
            t = np.clip((ch - dist) / max(ch, 1e-6), 0, 1)
            h = z - ch * (1 - np.sqrt(np.clip(1 - t * t, 0, 1)))
        else:
            h = z - np.maximum(0, ch - dist)
        sl = (slice(r0, r0 + m.shape[0]), slice(c0, c0 + m.shape[1]))
        cur = Hm[sl]
        upd = m & (h >= cur)
        cur[upd] = h[upd]
        M[sl][upd] = MID[mat]


def cut(poly, zf, ch, mat=None, both=True):
    """recess: floor at zf, chamfered walls of width ch."""
    polys = [poly, mirror(poly)] if both else [poly]
    for p in polys:
        r0, c0, m, dist = raster(p)
        h = zf + np.maximum(0, ch - dist)
        sl = (slice(r0, r0 + m.shape[0]), slice(c0, c0 + m.shape[1]))
        cur = Hm[sl]
        upd = m & (h < cur)
        cur[upd] = h[upd]
        if mat:
            fl = m & (dist >= ch)
            M[sl][fl] = MID[mat]


SCREWS = []
def screw(*a, **k):
    SCREWS.append((a, k))

def _screw(x, y, z, r=2.7, both=True):
    for sx in ((x, -x) if both else (x,)):
        add(Point(sx, y).buffer(r, 32), z + 2.0, r * 0.55, 'screw', both=False, reveal=0, round_=True)
        hexp = Polygon([(sx + 1.25 * math.cos(math.radians(a)), y + 1.25 * math.sin(math.radians(a))) for a in range(0, 360, 60)])
        cut(hexp, z + 0.6, 0.2, 'void', both=False)


# ======================= GEOMETRY (right half, mirrored) =======================
Z_CORE, Z_GRN, Z_BLOCK, Z_DOOR = 8.0, 11.0, 18.0, 12.0

# ---- backing (printer frame seen through gaps) ----
add(box(-284.5, 0, 284.5, 988), 2.0, 0, 'void', both=False, reveal=0)

# ---- base ----
add(cham(-236, 0, 236, 82, 1.5), Z_CORE, 1.5, 'blk', both=False)
add(cham(-224, 7, 224, 74, 5), Z_GRN, 2.0, 'grn', both=False)
cut(cham(-192, 15, 192, 27, 5), 6.0, 1.5, 'void', both=False)
add(cham(-188, 18, 188, 24, 2.5), 7.0, 1.0, 'led', both=False, reveal=0, round_=True)
cut(cham(-150, 47, 150, 49.2, 1.1), Z_GRN - 1.0, 0.6, None, both=False)   # fine engraved line
for x, y in ((212, 15.5), (212, 65.5)):
    screw(x, y, Z_GRN)
# base corner blocks
add(cham(236, 0, 293, 92, (6, 10, 10, 2)), Z_BLOCK, 3.0, 'blk')
screw(266, 22, Z_BLOCK)
screw(266, 70, Z_BLOCK)

# ---- hinge centres ----
HC_LO = (150, 450)
HC_UP = (748.9, 877.4)
HC = HC_LO + HC_UP


def hinge_notch():
    return unary_union([cham(226, c - 25, 250.5, c + 25, (0, 5, 5, 0)) for c in HC])


# ---- corner columns: black core + full-width green cover notched for hinges ----
for (y0, y1) in ((92, 286), (366, 517), (631, 958)):
    add(cham(225.5, y0, 284.5, y1, 1.0), Z_CORE, 1.2, 'blk')


def green_cover(y0, y1, cb, ct):
    """cb/ct: chamfer of the inner (door-side) bottom/top corner, follows door corner."""
    p = cham(231, y0, 281, y1, (cb, 2, 2, ct))
    return p.difference(hinge_notch())


add(green_cover(95, 283, 10, 3), Z_GRN, 2.0, 'grn')
add(green_cover(369, 514, 3, 10), Z_GRN, 2.0, 'grn')
add(green_cover(634, 955, 10, 10), Z_GRN, 2.0, 'grn')
# cover screws on the solid inner wall (cable channel sits under the outer part)
for y in (106, 272, 380, 503, 646, 944):
    screw(241, y, Z_GRN, 2.3)
# subtle engraved line on the cover over the channel edge
for (y0, y1) in ((112, 270), (392, 496), (660, 930)):
    cut(cham(275.3, y0, 276.5, y1, 0.6), Z_GRN - 0.8, 0.5, None)

# mid side cantoneira
add(cham(233, 286, 292, 366, (3, 9, 9, 3)), Z_BLOCK, 3.0, 'blk')
screw(273, 300, Z_BLOCK)
screw(273, 352, Z_BLOCK)

# ---- doors ----
def door(y0, y1):
    add(cham(1.5, y0, 224, y1, (2, 12, 12, 2)), Z_DOOR, 2.0, 'blk')
    cut(cham(12, y0 + 11, 213.5, y1 - 11, 20), 8.0, 2.5, 'glass')

door(86, 515)
door(636, 950)
# pulls at the meeting edge
for (y0, y1) in ((272, 338), (766, 832)):
    add(cham(4.5, y0, 11, y1, 3), 17.0, 2.5, 'blk', round_=True)

# ---- band + riser + display ----
add(cham(-236, 517, 236, 557, 1.5), Z_CORE, 1.5, 'blk', both=False)
add(cham(-236, 559, 236, 631, 1.5), Z_CORE, 1.5, 'blk', both=False)
add(cham(233, 517, 292, 631, (3, 9, 9, 3)), Z_BLOCK, 3.0, 'blk')
screw(273, 531, Z_BLOCK)
screw(273, 617, Z_BLOCK)
# green riser panel
add(cham(-222, 526, 66, 622, 7), Z_GRN + 1, 2.0, 'grn', both=False)
cut(cham(-204, 540, 48, 608, 5), Z_GRN - 0.2, 1.2, None, both=False)
for x in (-213, 57):
    screw(x, 574, Z_GRN + 1, 2.3, both=False)
# display module (5")
add(cham(80, 524, 226, 624, 8), Z_GRN + 2, 2.2, 'grn', both=False)
add(cham(89, 532, 217, 616, 5), Z_GRN + 3.0, 1.0, 'screen', both=False, round_=True)
cut(cham(96, 539, 210, 609, 2.5), Z_GRN + 2.6, 0.3, 'screen', both=False)

# ---- top cap ----
add(cham(-292, 958, 292, 988, (2, 2, 9, 9)), 15.0, 3.0, 'blk', both=False)
add(cham(-200, 964, 200, 982, 5), 16.5, 1.4, 'grn', both=False)
for x, y in ((-276, 973), (276, 973)):
    screw(x, y, 15.0, both=False)

# ---- hinges (sit on the black core inside the green notch) ----
for c in HC:
    for sgn in (1, -1):
        f = (lambda p: p) if sgn > 0 else mirror
        leafC = cham(229.5, c - 21, 247.5, c + 21, (1, 4, 4, 1))
        leafD = Polygon([(203, c - 13), (222, c - 18), (222, c + 18), (203, c + 13)])
        add(f(leafC), 15.5, 2.0, 'blk', both=False)
        add(f(leafD), 15.0, 1.8, 'blk', both=False)
        # knuckle: vertical barrel, round profile
        add(f(cham(220.5, c - 22, 229.5, c + 22, 1.5)), 19.0, 4.5, 'blk', both=False, reveal=0.3, round_=True)
        for yy in (c - 22.6, c + 22.6):
            add(f(cham(222.5, yy - 0.6, 227.5, yy + 0.6, 0)), 17.5, 0.6, 'pin', both=False, reveal=0, round_=True)
        cut(f(cham(220.5, c - 0.5, 229.5, c + 0.5, 0)), 15.0, 0.5, None, both=False)
        sx = 239 * sgn
        screw(sx, c - 12, 15.5, 2.1, both=False)
        screw(sx, c + 12, 15.5, 2.1, both=False)
        screw(211 * sgn, c, 15.0, 2.1, both=False)

# facet pockets on cantoneiras (base, mid, display band)
for (x0, y0, x1, y1) in ((244, 8, 285, 84), (241, 294, 284, 358), (241, 525, 284, 623)):
    cut(cham(x0, y0, x1, y1, (2, 6, 6, 2)), Z_BLOCK - 1.0, 1.0, None)

for a, k in SCREWS:
    _screw(*a, **k)

# ======================= SHADING =======================
Hs = ndimage.gaussian_filter(Hm, 0.35 * S)
gy, gx = np.gradient(Hs, 1.0 / S)          # per mm; rows go down => world dy = -gy
nx, ny, nz = -gx, gy, np.ones_like(Hs)
nl = np.sqrt(nx * nx + ny * ny + nz * nz)
nx, ny, nz = nx / nl, ny / nl, nz / nl

L = np.array([-0.50, 0.62, 0.60]); L /= np.linalg.norm(L)
V = np.array([0, 0, 1.0])
Hh = L + V; Hh /= np.linalg.norm(Hh)
ndl = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
ndh = np.clip(nx * Hh[0] + ny * Hh[1] + nz * Hh[2], 0, 1)

# cast shadows (march toward the light: up-left in the image)
lxy = math.hypot(L[0], L[1])
rise = L[2] / lxy                                 # mm of height per mm travelled
step_mm = math.sqrt(2) / S
shadow = np.zeros_like(Hm)
for t in range(1, 64):
    sh = np.roll(np.roll(Hm, t, axis=0), t, axis=1)
    shadow = np.maximum(shadow, sh - Hm - t * step_mm * rise)
shade = 1.0 - 0.55 * np.clip(shadow / 1.2, 0, 1)
shade = ndimage.gaussian_filter(shade, 0.5 * S)

# ambient occlusion
ao = ndimage.gaussian_filter(Hm, 2.5 * S) - Hm
ao = 1.0 - 0.6 * np.clip(ao / 4.0, 0, 1)

alb = np.zeros((H, W, 3), np.float32)
spec = np.zeros((H, W), np.float32)
shin = np.zeros((H, W), np.float32)
emis = np.zeros((H, W), np.float32)
for k, (col, sp, sn, em) in MAT.items():
    m = M == MID[k]
    alb[m] = np.array(col, np.float32) / 255.0
    spec[m] = sp
    shin[m] = sn
    emis[m] = em

light = (0.38 * ao + 0.85 * ndl * shade)
rgb = alb * light[..., None] + (spec * ndh ** shin * shade)[..., None] * np.array([1.0, 0.98, 0.95])
rgb = np.where(emis[..., None] > 0, alb * (0.85 + 0.25 * ndl[..., None]), rgb)

# glass: soft diagonal reflection
gm = M == MID['glass']
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
band = np.exp(-(((xx - yy * 0.55) % (W * 0.9)) - W * 0.30) ** 2 / (2 * (W * 0.06) ** 2))
rgb[gm] += (0.07 * band[gm])[..., None] + 0.02

# LED glow
led = (M == MID['led']).astype(np.float32)
glow = ndimage.gaussian_filter(led, 3 * S)
rgb += glow[..., None] * np.array([0.55, 0.30, 0.08]) * 0.9

# background
bg = np.array([245, 244, 240], np.float32) / 255
inside = Hm > 0.01
rgb = np.where(inside[..., None], rgb, bg)

img = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8))
img = img.resize((W // 2, H // 2), Image.LANCZOS)
img.save(sys.argv[1])
print(img.size)
