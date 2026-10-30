import adsk.core, adsk.fusion, traceback, os, json

LOG = 'F:/SV08 Eclosure/docs/planos/carenagem/_medidas/SV-03_modelagem.txt'
out = []
def log(s): out.append(str(s))

def P(x, y, z=0):  # mm -> cm
    return adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0)

def VI(cm): return adsk.core.ValueInput.createByReal(cm)

def occ_by_name(root, name):
    for o in root.occurrences:
        if o.name.split(':')[0] == name:
            return o
    return None

def offset_plane(comp, base, cm):
    ci = comp.constructionPlanes.createInput()
    ci.setByOffset(base, VI(cm))
    return comp.constructionPlanes.add(ci)

def poly_sketch(comp, plane, pts_world):
    sk = comp.sketches.add(plane)
    lines = sk.sketchCurves.sketchLines
    sp = [sk.modelToSketchSpace(p) for p in pts_world]
    for i in range(len(sp)):
        lines.addByTwoPoints(sp[i], sp[(i + 1) % len(sp)])
    return sk

def smallest_profile(sk):
    best = None
    for pr in sk.profiles:
        a = pr.areaProperties().area
        if best is None or a < best[0]:
            best = (a, pr)
    return best[1]

def extrude_sym(comp, sk, total_cm, body, op):
    ext = comp.features.extrudeFeatures
    ei = ext.createInput(smallest_profile(sk), op)
    ei.setSymmetricExtent(VI(total_cm), True)
    ei.participantBodies = [body]
    return ext.add(ei)

def run(context):
    try:
        app = adsk.core.Application.get()
        d = adsk.fusion.Design.cast(app.activeProduct)
        root = d.rootComponent
        JOIN = adsk.fusion.FeatureOperations.JoinFeatureOperation
        CUT = adsk.fusion.FeatureOperations.CutFeatureOperation
        ZB, ZF = 291.5, 295.5           # back / front of door frame
        ZM = (ZB + ZF) / 2.0
        L = 35.0                        # ear leg (preliminar)
        WX0, WX1, WY0, WY1 = 34.0, 193.0, 116.0, 488.5   # window opening (D)

        vols = {}
        for side, s in (('D', 1), ('E', -1)):
            names = ['59_PORTA_01_travessa_inferior_' + side, '59_PORTA_01_travessa_superior_' + side,
                     '59_PORTA_02_montante_central_inferior_' + side, '59_PORTA_02_montante_central_superior_' + side,
                     '59_PORTA_02_montante_externa_inferior_' + side, '59_PORTA_02_montante_externa_superior_' + side]
            for n in names:
                o = occ_by_name(root, n)
                vols[n] = round(o.component.bRepBodies.item(0).volume * 1000, 1)

            # ---------- (a) ears on travessas ----------
            for tname, yedge, ydir in (('59_PORTA_01_travessa_inferior_' + side, WY0, 1),
                                        ('59_PORTA_01_travessa_superior_' + side, WY1, -1)):
                o = occ_by_name(root, tname); c = o.component; b = c.bRepBodies.item(0)
                pl = offset_plane(c, c.xYConstructionPlane, ZM / 10.0)
                y0 = yedge - 0.1 * ydir     # 0.1 overlap into travessa
                # central-side ear (x near WX0) and outer-side ear (x near WX1)
                xa = WX0 + 0.1; xb = WX1 - 0.1
                ear_c = [(xa, y0), (WX0 + L, y0), (xa, yedge + ydir * (L - 0.1))]
                if side == 'D' and ydir == 1:
                    # clip for 62_apoio_movel_contato (x183.5-222, y137-163) with 0.5 clearance
                    xc, yc = 183.0, 136.5
                    # hypotenuse from (WX1-L, y0) to (xb, yedge+L-0.1): y = y0 + (x-(WX1-L))*( (L-0.1+0.1)/(xb-(WX1-L)) )
                    k = ((yedge + L - 0.1) - y0) / (xb - (WX1 - L))
                    y_at_xc = y0 + (xc - (WX1 - L)) * k
                    ear_o = [(WX1 - L, y0), (xb, y0), (xb, yc), (xc, yc), (xc, y_at_xc)]
                else:
                    ear_o = [(WX1 - L, y0), (xb, y0), (xb, yedge + ydir * (L - 0.1))]
                for ear in (ear_c, ear_o):
                    pts = [P(s * x, y, ZM) for (x, y) in ear]
                    sk = poly_sketch(c, pl, pts)
                    extrude_sym(c, sk, (ZF - ZB) / 10.0, b, JOIN)
                log('ears ok ' + tname)

            # ---------- (d) batente central ----------
            if side == 'D':
                for mname in ('59_PORTA_02_montante_central_inferior_D', '59_PORTA_02_montante_central_superior_D'):
                    o = occ_by_name(root, mname); c = o.component; b = c.bRepBodies.item(0)
                    bb = b.boundingBox
                    ymid = (bb.minPoint.y + bb.maxPoint.y) / 2.0; ylen = bb.maxPoint.y - bb.minPoint.y
                    ci = c.constructionPlanes.createInput()
                    ci.setByOffset(c.xZConstructionPlane, VI(ymid))
                    pl = c.constructionPlanes.add(ci)
                    # lip profile (x,z): (1.6,291.5) (-3.5,291.5) (0.5,295.5) (1.6,295.5)  -> overlaps 0.1 into body
                    pts = [P(1.6, ymid * 10, 291.5), P(-3.5, ymid * 10, 291.5), P(0.5, ymid * 10, 295.5), P(1.6, ymid * 10, 295.5)]
                    sk = poly_sketch(c, pl, pts)
                    extrude_sym(c, sk, ylen, b, JOIN)
                    log('lip ok ' + mname)
            else:
                for mname in ('59_PORTA_02_montante_central_inferior_E', '59_PORTA_02_montante_central_superior_E'):
                    o = occ_by_name(root, mname); c = o.component; b = c.bRepBodies.item(0)
                    bb = b.boundingBox
                    ymid = (bb.minPoint.y + bb.maxPoint.y) / 2.0; ylen = bb.maxPoint.y - bb.minPoint.y + 0.2
                    ci = c.constructionPlanes.createInput()
                    ci.setByOffset(c.xZConstructionPlane, VI(ymid))
                    pl = c.constructionPlanes.add(ci)
                    # cut region: x <= z - 295.707 is solid; remove triangle (-5.207,291.5)(-1.0,291.5)(-1.0,295.707-... )
                    za = 291.4; zb = -1.0 + 295.707   # line x = z - 295.707 ; at x=-1.0 -> z=294.707
                    pts = [P(za - 295.707, ymid * 10, za), P(-1.0, ymid * 10, za), P(-1.0, ymid * 10, zb)]
                    sk = poly_sketch(c, pl, pts)
                    extrude_sym(c, sk, ylen, b, CUT)
                    log('recess ok ' + mname)

            # ---------- (c) handle on montante central superior ----------
            mname = '59_PORTA_02_montante_central_superior_' + side
            o = occ_by_name(root, mname); c = o.component; b = c.bRepBodies.item(0)
            zt = 307.5
            pl = offset_plane(c, c.xYConstructionPlane, ((ZF - 0.04 + zt) / 2.0) / 10.0)
            pts = [P(s * 4.0, 322.0), P(s * 18.0, 322.0), P(s * 18.0, 402.0), P(s * 4.0, 402.0)]
            pts = [adsk.core.Point3D.create(p.x, p.y, ((ZF - 0.04 + zt) / 2.0) / 10.0) for p in pts]
            sk = poly_sketch(c, pl, pts)
            extrude_sym(c, sk, (zt - (ZF - 0.04)) / 10.0, b, JOIN)
            log('handle ok ' + mname)

        # ---------- (b) chamfers ----------
        def near(a, v, tol=0.02): return abs(a - v) < tol
        for side, s in (('D', 1), ('E', -1)):
            specs = {
                '59_PORTA_01_travessa_inferior_' + side: 'trav_inf',
                '59_PORTA_01_travessa_superior_' + side: 'trav_sup',
                '59_PORTA_02_montante_central_inferior_' + side: 'cent',
                '59_PORTA_02_montante_central_superior_' + side: 'cent',
                '59_PORTA_02_montante_externa_inferior_' + side: 'ext',
                '59_PORTA_02_montante_externa_superior_' + side: 'ext',
            }
            for n, kind in specs.items():
                o = occ_by_name(root, n); c = o.component; b = c.bRepBodies.item(0)
                edges = adsk.core.ObjectCollection.create()
                handle_edges = adsk.core.ObjectCollection.create()
                for e in b.edges:
                    p1 = e.startVertex.geometry; p2 = e.endVertex.geometry
                    if not isinstance(e.geometry, adsk.core.Line3D):
                        continue
                    x1, y1, z1 = p1.x * 10 * s, p1.y * 10, p1.z * 10
                    x2, y2, z2 = p2.x * 10 * s, p2.y * 10, p2.z * 10
                    if near(z1, 307.5, 0.05) and near(z2, 307.5, 0.05):
                        handle_edges.add(e); continue
                    if not (near(z1, ZF, 0.05) and near(z2, ZF, 0.05)):
                        continue
                    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                    ok = False
                    if kind == 'cent' and near(x1, WX0, 0.05) and near(x2, WX0, 0.05): ok = True
                    if kind == 'ext' and near(x1, WX1, 0.05) and near(x2, WX1, 0.05): ok = True
                    if kind in ('trav_inf', 'trav_sup'):
                        yw = WY0 if kind == 'trav_inf' else WY1
                        yo = 82.0 if kind == 'trav_inf' else 522.5
                        if near(y1, yw, 0.05) and near(y2, yw, 0.05) and WX0 + 30 < mx < WX1 - 30: ok = True
                        if (not near(x1, x2, 0.05)) and (not near(y1, y2, 0.05)) and WX0 < mx < WX1: ok = True   # hypotenuse
                        if near(y1, yo, 0.05) and near(y2, yo, 0.05) and 2.0 < mx < 224.0: ok = True
                    if ok: edges.add(e)
                log('%s chamfer edges=%d handle_edges=%d' % (n, edges.count, handle_edges.count))
                for coll, dist in ((edges, 0.15), (handle_edges, 0.15)):
                    if coll.count == 0: continue
                    try:
                        ci = c.features.chamferFeatures.createInput2()
                        ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(coll, VI(dist), False)
                        c.features.chamferFeatures.add(ci)
                        log('  chamfer ok')
                    except:
                        log('  chamfer FAIL ' + traceback.format_exc().splitlines()[-1])

        for n in vols:
            o = occ_by_name(root, n); b = o.component.bRepBodies.item(0); bb = b.boundingBox
            log('%s vol %s -> %.1f | bodies=%d | bbox x%.1f..%.1f y%.1f..%.1f z%.1f..%.1f' % (
                n, vols[n], b.volume * 1000, o.component.bRepBodies.count,
                bb.minPoint.x * 10, bb.maxPoint.x * 10, bb.minPoint.y * 10, bb.maxPoint.y * 10, bb.minPoint.z * 10, bb.maxPoint.z * 10))
    except:
        log(traceback.format_exc())
    open(LOG, 'w', encoding='utf-8').write('\n'.join(out))
