import adsk.core, adsk.fusion, json, traceback, math

def run(context):
    log = []
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        P3 = adsk.core.Point3D.create; V3 = adsk.core.Vector3D.create; VI = adsk.core.ValueInput
        FO = adsk.fusion.FeatureOperations
        occ = [o for o in root.occurrences if o.component.name == 'V2_ESTUDO_Canto_V1_Aproximado'][0]
        comp = occ.component
        ext = comp.features.extrudeFeatures
        PL = {'xy': (comp.xYConstructionPlane, 2), 'yz': (comp.yZConstructionPlane, 0), 'xz': (comp.xZConstructionPlane, 1)}

        def mk_sketch(pl):
            plane, ax = PL[pl]
            sk = comp.sketches.add(plane)
            nrm = sk.xDirection.crossProduct(sk.yDirection)
            sg = [nrm.x, nrm.y, nrm.z][ax]
            return sk, ax, (1 if sg > 0 else -1)

        def to_sk(sk, ax, p):
            c = list(p); c[ax] = 0.0
            return sk.modelToSketchSpace(P3(c[0] / 10.0, c[1] / 10.0, c[2] / 10.0))

        def do_ext(sk, sg, s0, s1, op, bodies, taper):
            sk.isVisible = False
            coll = adsk.core.ObjectCollection.create()
            for i in range(sk.profiles.count): coll.add(sk.profiles.item(i))
            d = 1 if s1 > s0 else -1
            dirn = adsk.fusion.ExtentDirections.PositiveExtentDirection if d * sg > 0 else adsk.fusion.ExtentDirections.NegativeExtentDirection
            inp = ext.createInput(coll, op)
            ed = adsk.fusion.DistanceExtentDefinition.create(VI.createByReal(abs(s1 - s0) / 10.0))
            if taper: inp.setOneSideExtent(ed, dirn, VI.createByString(taper))
            else: inp.setOneSideExtent(ed, dirn)
            inp.startExtent = adsk.fusion.OffsetStartDefinition.create(VI.createByReal(s0 * sg / 10.0))
            if bodies is not None: inp.participantBodies = bodies
            return ext.add(inp)

        def prism(pl, pts, s0, s1, op, bodies=None, taper=None):
            sk, ax, sg = mk_sketch(pl)
            Q = [to_sk(sk, ax, p) for p in pts]
            L = sk.sketchCurves.sketchLines
            for i in range(len(Q)):
                L.addByTwoPoints(Q[i], Q[(i + 1) % len(Q)])
            return do_ext(sk, sg, s0, s1, op, bodies, taper)

        def circles(pl, cs, r, s0, s1, bodies):
            sk, ax, sg = mk_sketch(pl)
            for p in cs:
                sk.sketchCurves.sketchCircles.addByCenterRadius(to_sk(sk, ax, p), r / 10.0)
            return do_ext(sk, sg, s0, s1, FO.CutFeatureOperation, bodies, None)

        def offset_poly(poly, d):
            n = len(poly)
            ar = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
            lines = []
            for i in range(n):
                (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
                L = math.hypot(x1 - x0, y1 - y0); tx, ty = (x1 - x0) / L, (y1 - y0) / L
                nx, ny = (ty, -tx) if ar > 0 else (-ty, tx)
                lines.append(((x0 + d * nx, y0 + d * ny), (tx, ty)))
            out = []
            for i in range(n):
                (p, t), (q, u) = lines[i - 1], lines[i]
                den = t[0] * u[1] - t[1] * u[0]
                s = ((q[0] - p[0]) * u[1] - (q[1] - p[1]) * u[0]) / den
                out.append((p[0] + s * t[0], p[1] + s * t[1]))
            return out


        XF = 283.8; D = 0.8
        jobs = [('72_verde_inferior_D_encaixe', 105.0, 290.0), ('75_verde_superior_D', 364.0, 535.0)]
        for nm, y0, y1 in jobs:
            gb = comp.bRepBodies.itemByName(nm)
            Z0, Z1, K = 255.5, 269.5, 5.0
            P = [(XF, y0 + K, Z0), (XF, y1 - K, Z0), (XF, y1, Z0 + K), (XF, y1, Z1 - K), (XF, y1 - K, Z1), (XF, y0 + K, Z1), (XF, y0, Z1 - K), (XF, y0, Z0 + K)]
            full = (y1 - y0) * (Z1 - Z0) - 2 * K * K
            def floor():
                best = 0
                for f in gb.faces:
                    ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
                    if ok and abs(n.x) > 0.99 and abs(f.pointOnFace.x * 10 - (XF - D)) < 0.05:
                        best = max(best, f.area * 100)
                return best
            done = False
            for t in ('-45 deg', '45 deg'):
                try:
                    f = prism('yz', P, XF + 0.01, XF - D, FO.CutFeatureOperation, [gb], t)
                    fa = floor()
                    if fa and fa < full * 0.97:
                        log.append('%s pocket %s %.0f/%.0f' % (nm, t, fa, full)); done = True; break
                    log.append('%s %s floor %.0f/%.0f retry' % (nm, t, fa, full))
                    f.deleteMe()
                except Exception as ex:
                    log.append('%s %s: %s' % (nm, t, str(ex)[:80]))
            if not done:
                prism('yz', P, XF + 0.01, XF - D, FO.CutFeatureOperation, [gb]); log.append(nm + ' straight')
        v = app.activeViewport; cam = v.camera; cam.isSmoothTransition = False
        cam.target = P3(125.5, 14.0, 27.35); cam.eye = P3(155.0, 30.0, 70.35); cam.upVector = V3(0, 1, 0)
        v.camera = cam; v.refresh()
    except Exception:
        log.append(traceback.format_exc()[-600:])
    print(json.dumps(log))
