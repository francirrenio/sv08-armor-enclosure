import math, sys
from PIL import Image, ImageDraw
from shapely.geometry import Polygon, box
from shapely import affinity
from shapely.ops import unary_union

S = 2.0 * 3            # px per mm (supersampled x3)
XMIN, XMAX, YMIN, YMAX = -300, 300, -5, 995
W, H = int((XMAX - XMIN) * S), int((YMAX - YMIN) * S)
BG = (245, 244, 240, 0)
GAP = (20, 20, 19, 255)
L = (-0.6, 0.8)

PAL = {
    'k': ((42, 42, 40), (78, 77, 73), (18, 18, 17)),
    'g': ((94, 109, 59), (128, 142, 86), (58, 70, 36)),
    'gr': ((79, 92, 49), (110, 124, 72), (50, 60, 30)),
}

def P(x, y):
    return ((x - XMIN) * S, (YMAX - y) * S)

def cham(x0, y0, x1, y1, c):
    if not isinstance(c, (tuple, list)):
        c = (c, c, c, c)          # bl, br, tr, tl
    bl, br, tr, tl = c
    pts = [(x0 + bl, y0), (x1 - br, y0), (x1, y0 + br), (x1, y1 - tr), (x1 - tr, y1), (x0 + tl, y1), (x0, y1 - tl), (x0, y0 + bl)]
    out = []
    for p in pts:
        if not out or (abs(p[0] - out[-1][0]) > 1e-6 or abs(p[1] - out[-1][1]) > 1e-6):
            out.append(p)
    return Polygon(out)

def mirror(poly):
    return affinity.scale(poly, xfact=-1, yfact=1, origin=(0, 0))

img = Image.new('RGBA', (W, H), BG)
d = ImageDraw.Draw(img)
parts = []   # (poly, palette, bevel, invert)

def add(poly, pal='k', bevel=1.6, invert=False, both=True):
    for g in getattr(poly, 'geoms', [poly]):
        if g.is_empty or g.area < 1:
            continue
        parts.append((g, pal, bevel, invert))
        if both:
            parts.append((mirror(g), pal, bevel, invert))

HC = (150, 450, 748.9, 877.4)
NOTCH = unary_union([cham(229, c - 30, 259, c + 30, 6) for c in HC])
def notched(p, extra=0):
    return p.difference(NOTCH.buffer(extra, join_style=2) if extra else NOTCH)

def fillpoly(poly, col):
    if poly.is_empty:
        return
    geoms = getattr(poly, 'geoms', [poly])
    for g in geoms:
        d.polygon([P(*p) for p in list(g.exterior.coords)], fill=col)

def draw_part(poly, pal, bevel, invert, reveal=0.7):
    base, light, dark = PAL[pal]
    shp = poly.buffer(-reveal, join_style=2)
    if shp.is_empty:
        return
    inner = shp.buffer(-bevel, join_style=2)
    fillpoly(shp, base)
    ext = list(shp.exterior.coords)
    # orientation
    area = sum(ext[i][0] * ext[i + 1][1] - ext[i + 1][0] * ext[i][1] for i in range(len(ext) - 1))
    sgn = 1 if area > 0 else -1
    inn = inner.exterior.coords if not inner.is_empty else None
    for i in range(len(ext) - 1):
        (x1, y1), (x2, y2) = ext[i], ext[i + 1]
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        if ln < 1e-6:
            continue
        nx, ny = sgn * dy / ln, -sgn * dx / ln
        sh = nx * L[0] + ny * L[1]
        if invert:
            sh = -sh
        if sh > 0.25:
            col = light
        elif sh < -0.25:
            col = dark
        else:
            col = tuple(int((a + b) / 2) for a, b in zip(base, light if sh > 0 else dark))
        # quad: outer edge + offset inward
        ox, oy = -nx * bevel, -ny * bevel
        d.polygon([P(x1, y1), P(x2, y2), P(x2 + ox, y2 + oy), P(x1 + ox, y1 + oy)], fill=col)
    if not inner.is_empty:
        fillpoly(inner, base)

def screw(x, y, r=2.6, both=True):
    for sx in ((x, -x) if both else (x,)):
        cx, cy = P(sx, y)
        rr = r * S
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(16, 16, 15))
        r2 = rr * 0.72
        d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(46, 46, 44))
        r3 = rr * 0.28
        d.ellipse([cx - r2 * 0.5 - r3, cy - r2 * 0.5 - r3, cx - r2 * 0.5 + r3, cy - r2 * 0.5 + r3], fill=(110, 110, 104))

def rot_plate(cx, cy, ang, length, width, c=4):
    p = cham(-length / 2, -width / 2, length / 2, width / 2, c)
    p = affinity.rotate(p, ang, origin=(0, 0))
    return affinity.translate(p, cx, cy)

# ---------------- geometry (mm, Y up) ----------------
# base
add(cham(-236, 0, 236, 80, 2), 'k', 1.6, both=False)
add(cham(236, 0, 292, 92, (2, 10, 10, 2)), 'k', 3.2)
add(cham(-226, 8, 226, 50, 6), 'g', 1.4, both=False)
add(cham(-200, 13, 200, 35, 5), 'k', 1.4, invert=True, both=False)
add(Polygon([(-205, 55), (205, 55), (214, 64), (205, 73), (-205, 73), (-214, 64)]), 'g', 1.4, both=False)
# lower columns
add(cham(228, 92, 282, 284, 2), 'k', 1.6)
add(cham(234, 288, 292, 366, (2, 8, 8, 2)), 'k', 3.2)
add(cham(228, 370, 282, 513, 2), 'k', 1.6)
add(notched(cham(246, 112, 274, 280, 3)), 'g', 1.3)
add(notched(cham(246, 372, 274, 489, 3)), 'g', 1.3)
add(notched(cham(253, 128, 267, 264, 3), 4), 'gr', 1.0, invert=True)
add(notched(cham(253, 388, 267, 473, 3), 4), 'gr', 1.0, invert=True)
# lower doors
add(cham(1.5, 86, 224, 515, (2, 14, 14, 2)), 'k', 1.8)
add(cham(19, 105, 207, 497, 26), 'k', 1.6, invert=True)
# band + riser
add(cham(-236, 519, 236, 556, 2), 'k', 1.6, both=False)
add(cham(-236, 560, 236, 627, 2), 'k', 1.6, both=False)
add(cham(234, 517, 292, 631, (2, 8, 8, 2)), 'k', 3.2)
add(Polygon([(-212, 528), (56, 528), (66, 538), (66, 612), (56, 622), (-212, 622), (-222, 612), (-222, 538)]), 'g', 1.4, both=False)
add(cham(-196, 541, 40, 609, 8), 'gr', 1.2, invert=True, both=False)
add(cham(80, 524, 228, 624, 10), 'g', 1.5, both=False)
add(cham(90, 532, 218, 616, 6), 'k', 1.4, invert=True, both=False)
# upper
add(cham(228, 634, 282, 956, 2), 'k', 1.6)
add(notched(cham(246, 662, 274, 924, 3)), 'g', 1.3)
add(notched(cham(253, 678, 267, 908, 3), 4), 'gr', 1.0, invert=True)
add(cham(1.5, 636, 224, 950, (2, 14, 14, 2)), 'k', 1.8)
add(cham(19, 655, 207, 931, 26), 'k', 1.6, invert=True)
add(cham(-292, 958, 292, 988, (2, 2, 10, 10)), 'k', 3.0, both=False)
# handles
add(cham(5, 270, 13, 340, 2), 'k', 1.2)
add(cham(5, 765, 13, 835, 2), 'k', 1.2)
# hinge recesses
for c in (150, 450, 748.9, 877.4):
    add(cham(229, c - 28, 257, c + 28, 4), 'k', 1.2, invert=True)
# diagonal corner plates
# green corner plates: follow the door chamfer with a gap (fitted piece)
G2 = 2.83
def corner_plate(yd, bottom):
    if bottom:   # door corner chamfer from (210,yd) to (224,yd+14): x - y = 210 - yd
        ya, yb = yd + 8, yd + 23
        xl = lambda y: y + 210 - yd + G2
        return Polygon([(xl(ya), ya), (268, ya), (274, ya + 6), (274, yb), (xl(yb), yb)])
    else:        # chamfer from (224,yd-14) to (210,yd): x + y = 210 + yd
        ya, yb = yd - 23, yd - 8
        xl = lambda y: 210 + yd + G2 - y
        return Polygon([(xl(ya), ya), (274, ya), (274, yb - 6), (268, yb), (xl(yb), yb)])
PLATES = ((86, True), (515, False), (636, True), (950, False))
for yd, b in PLATES:
    add(corner_plate(yd, b).intersection(box(229.5, 0, 300, 1000)), 'g', 1.3)

# backing silhouette (gaps)
allp = unary_union([p for p, *_ in parts])
fillpoly(allp.buffer(0.2, join_style=2), GAP)
fillpoly(box(-282, 0, 282, 988), GAP)
for p, pal, bev, inv in parts:
    draw_part(p, pal, bev, inv)

# glass
for (y0, y1) in ((108, 494), (658, 928)):
    g = cham(22, y0, 204, y1, 24)
    for gg in (g, mirror(g)):
        d.polygon([P(*q) for q in gg.exterior.coords], fill=(163, 190, 210))
        d.line([P(*q) for q in gg.buffer(-3, join_style=2).exterior.coords], fill=(186, 208, 224), width=int(S * 0.6))
# LED
led = cham(-194, 18, 194, 30, 4)
d.polygon([P(*q) for q in led.exterior.coords], fill=(244, 160, 52))
d.polygon([P(*q) for q in cham(-188, 22, 188, 26, 2).exterior.coords], fill=(255, 214, 140))
# display screen
scr = cham(97, 539, 211, 609, 3)
d.polygon([P(*q) for q in scr.exterior.coords], fill=(22, 34, 42))
d.line([P(100, 605), P(150, 605)], fill=(50, 70, 82), width=int(S * 0.8))
# hinges (black)
def hinge(c):
    for sgn in (1, -1):
        leafA = cham(206, c - 22, 226, c + 22, 2)
        leafB = cham(232, c - 22, 252, c + 22, 2)
        kn = cham(226, c - 24, 232, c + 24, 1)
        for poly in (leafA, leafB, kn):
            pp = poly if sgn > 0 else mirror(poly)
            draw_part(pp.buffer(0.7, join_style=2), 'k', 1.0, False, reveal=0.7)
        for yy in (c - 14, c + 14):
            screw(sgn * 216, yy, 1.6, both=False)
            screw(sgn * 242, yy, 1.6, both=False)
        for yy in (c - 8, c + 8):
            x0, y0p = P(sgn * 226, yy)
            x1, _ = P(sgn * 232, yy)
            d.line([(x0, y0p), (x1, y0p)], fill=(14, 14, 13), width=int(S * 0.5))
for c in (150, 450, 748.9, 877.4):
    hinge(c)
# screws
for (x, y) in ((214, 42), (214, 16), (196, 64), (260, 120), (260, 272), (260, 380), (260, 481), (256, 101.5), (256, 499.5), (256, 651.5), (256, 934.5),
               (260, 670), (260, 916), (263, 296), (263, 358), (263, 527), (263, 621), (263, 8), (263, 84), (263, 966), (263, 980)):
    screw(x, y)
for (x, y) in ((-211, 575), (55, 575), (85, 574), (223, 574)):
    screw(x, y, both=False)

out = img.resize((W // 3, H // 3), Image.LANCZOS)
out.save(sys.argv[1])
print(out.size)
