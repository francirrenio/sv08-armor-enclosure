import adsk.core, adsk.fusion, json, traceback, math

def run(context):
    log = []
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        tbm = adsk.fusion.TemporaryBRepManager.get()
        P3 = adsk.core.Point3D.create; V3 = adsk.core.Vector3D.create; VI = adsk.core.ValueInput
        FO = adsk.fusion.FeatureOperations
        A = des.appearances
        BLK = A.itemByName('R59_body'); GRN = A.itemByName('R59_green'); HW = A.itemByName('R59_hardware') or BLK
        for o in list(root.occurrences):
            if o.component.name.startswith('V2_EXEMPLO_Encaixe'):
                o.deleteMe()
        occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component
        comp.name = 'V2_EXEMPLO_Encaixe_Verde_Preto'
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

        def nb(feat, nm, ap):
            b = feat.bodies.item(0); b.name = nm; b.appearance = ap; return b

        # ---------- bodies ----------
        core = nb(prism('xz', [(-40, 0, -12), (-40, 0, -5), (-5, 0, -5), (-5, 0, -40), (-12, 0, -40), (-12, 0, -12)], 0, 300, FO.NewBodyFeatureOperation), 'Nucleo_preto', BLK)
        green = nb(prism('xz', [(-40, 0, -5), (-40, 0, 0), (-3, 0, 0), (0, 0, -3), (0, 0, -40), (-5, 0, -40), (-5, 0, -5)], 50.8, 249.2, FO.NewBodyFeatureOperation), 'Capa_verde', GRN)
        CANT = [(-46, 0, -12), (-46, 0, 4), (1, 0, 4), (4, 0, 1), (4, 0, -46), (-12, 0, -46), (-12, 0, -12)]
        cantB = nb(prism('xz', CANT, 0, 50, FO.NewBodyFeatureOperation), 'Cantoneira_inferior', BLK)
        cantT = nb(prism('xz', CANT, 250, 300, FO.NewBodyFeatureOperation), 'Cantoneira_superior', BLK)
        BOSS = [(-40, 120), (-32, 120), (-27, 125), (-27, 165), (-32, 170), (-40, 170)]
        boss = nb(prism('xy', [(x, y, 0) for (x, y) in BOSS], -5, 0, FO.NewBodyFeatureOperation), 'Ressalto_dobradica', BLK)
        log.append('bodies ok')

        # ---------- notch in green around the boss (0.8 gap) ----------
        notch = [((-43.0 if x < -40.4 else x), y) for (x, y) in offset_poly(BOSS, 0.8)]
        prism('xy', [(x, y, 0) for (x, y) in notch], 1, -6, FO.CutFeatureOperation, [green])
        log.append('notch ok')

        # ---------- one detail on green: chamfered pocket on side face ----------
        POCK = [(0, 90, -31), (0, 210, -31), (0, 215, -26), (0, 215, -17), (0, 210, -12), (0, 90, -12), (0, 85, -17), (0, 85, -26)]
        def floor_area():
            best = 0
            for f in green.faces:
                ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
                if ok and n.x > 0.99 and abs(f.pointOnFace.x * 10 + 0.8) < 0.05:
                    best = max(best, f.area * 100)
            return best
        done = False
        for t in ('-45 deg', '45 deg'):
            try:
                f = prism('yz', POCK, 0, -0.8, FO.CutFeatureOperation, [green], t)
                fa = floor_area()
                if fa and fa < 130 * 19 - 50:
                    log.append('pocket ok %s floor %.0f' % (t, fa)); done = True; break
                f.deleteMe()
            except Exception as ex:
                log.append('pocket %s: %s' % (t, str(ex)[:60]))
        if not done:
            prism('yz', POCK, 0, -0.8, FO.CutFeatureOperation, [green]); log.append('pocket straight')

        # ---------- chamfers on every outer edge (V groove at each meeting) ----------
        ch = comp.features.chamferFeatures
        def chamfer_outer(body, pred, dist):
            e = adsk.core.ObjectCollection.create(); seen = set()
            for f in body.faces:
                ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
                if not (ok and pred(n, f.pointOnFace)): continue
                for ed in f.edges:
                    if ed.tempId in seen: continue
                    for af in ed.faces:
                        if af == f: continue
                        ok2, n2 = af.evaluator.getNormalAtPoint(af.pointOnFace)
                        if ok2 and abs(n.dotProduct(n2)) < 0.05:
                            seen.add(ed.tempId); e.add(ed)
            for d in (dist, dist * 0.6):
                try:
                    ci = ch.createInput2()
                    ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(e, VI.createByReal(d / 10.0), False)
                    ch.add(ci); log.append('ch %s %.1f n%d' % (body.name, d, e.count)); return
                except Exception as ex:
                    log.append('ch fail %s %s' % (body.name, str(ex)[:60]))
        def P_green(n, p):
            return (n.z > 0.99 and abs(p.z) < 0.002) or (n.x > 0.99 and abs(p.x) < 0.002) or (n.x > 0.6 and n.z > 0.6)
        def P_boss(n, p):
            return n.z > 0.99 and abs(p.z) < 0.002
        def P_cant(n, p):
            return (n.z > 0.99 and abs(p.z - 0.4) < 0.002) or (n.x > 0.99 and abs(p.x - 0.4) < 0.002) or (n.x > 0.6 and n.z > 0.6)
        chamfer_outer(green, P_green, 1.2)
        chamfer_outer(boss, P_boss, 1.2)
        chamfer_outer(cantB, P_cant, 2.5)
        chamfer_outer(cantT, P_cant, 2.5)

        # ---------- screws: counterbore 6.5 x 0.9 + ISO7380 head ----------
        GF = [(-20, 65, 0), (-20, 235, 0)]
        GS = [(0, 65, -21.5), (0, 235, -21.5)]
        CF = [(-22, 25, 4), (-22, 275, 4)]
        CS = [(4, 25, -22), (4, 275, -22)]
        for cs, pl, s0, bodies in ((GF, 'xy', 0, [green]), (GS, 'yz', 0, [green]), (CF, 'xy', 4, [cantB, cantT]), (CS, 'yz', 4, [cantB, cantT])):
            try:
                circles(pl, cs, 3.25, s0, s0 - 0.9, bodies)
            except Exception as ex:
                log.append('cb fail ' + str(ex)[:60])
        def box(c0, c1):
            return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(P3((c0[0] + c1[0]) / 20.0, (c0[1] + c1[1]) / 20.0, (c0[2] + c1[2]) / 20.0), V3(1, 0, 0), V3(0, 1, 0), abs(c1[0] - c0[0]) / 10.0, abs(c1[1] - c0[1]) / 10.0, abs(c1[2] - c0[2]) / 10.0))
        def head(p, ax):
            p = list(p); f = p[ax] - 0.9
            c = list(p); c[ax] = f - 1.9
            sph = tbm.createSphere(P3(c[0] / 10.0, c[1] / 10.0, c[2] / 10.0), 0.35)
            lo = [v - 4 for v in p]; hi = [v + 4 for v in p]; lo[ax] = f; hi[ax] = f + 3
            tbm.booleanOperation(sph, box(lo, hi), adsk.fusion.BooleanTypes.IntersectionBooleanType)
            lo = [v - 1.0 for v in p]; hi = [v + 1.0 for v in p]; lo[ax] = f + 1.0; hi[ax] = f + 3
            tbm.booleanOperation(sph, box(lo, hi), adsk.fusion.BooleanTypes.DifferenceBooleanType)
            return sph
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        n0 = comp.bRepBodies.count
        try:
            for p in GF + CF: comp.bRepBodies.add(head(p, 2), bf)
            for p in GS + CS: comp.bRepBodies.add(head(p, 0), bf)
        finally:
            bf.finishEdit()
        for i in range(n0, comp.bRepBodies.count):
            b = comp.bRepBodies.item(i); b.appearance = HW; b.name = 'M3_ISO7380_%d' % (i - n0)
        log.append('screws ok')

        m = occ.transform2; m.translation = V3(150.0, 0, 0); occ.transform2 = m
        if des.snapshots.hasPendingSnapshot: des.snapshots.add()
        v = app.activeViewport; cam = v.camera; cam.isSmoothTransition = False
        cam.target = P3(148.0, 15.0, -2.0); cam.eye = P3(178.0, 33.0, 52.0); cam.upVector = V3(0, 1, 0)
        v.camera = cam; v.refresh()
        log.append('ok %d bodies' % comp.bRepBodies.count)
    except Exception:
        log.append(traceback.format_exc()[-600:])
    print(json.dumps(log))
