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
            if o.component.name.startswith('V2_ESTUDO_Canto_Encaixe'):
                o.deleteMe()
        occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component
        comp.name = 'V2_ESTUDO_Canto_Encaixe'
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


        # ---------- real corner, V2 volumes (front Z, side X), V1 layout (Y) ----------
        core = nb(prism('xz', [(240, 0, 274.5), (269.5, 0, 274.5), (269.5, 0, 216), (272.5, 0, 216), (272.5, 0, 274.5), (277, 0, 274.5), (277, 0, 281), (240, 0, 281)], 0, 636, FO.NewBodyFeatureOperation), 'Nucleo_preto', BLK)
        GREEN = [(244, 0, 281), (277, 0, 281), (277, 0, 222), (281, 0, 222), (281, 0, 283), (278, 0, 286), (244, 0, 286)]
        CANT = [(239.5, 0, 280), (275, 0, 280), (275, 0, 214), (287, 0, 214), (287, 0, 289), (284, 0, 292), (239.5, 0, 292)]
        cants = [(0.0, 92.0), (298.0, 354.0), (552.0, 636.0)]
        covers = [(92.8, 297.2), (354.8, 551.2)]
        C = [nb(prism('xz', CANT, a, b, FO.NewBodyFeatureOperation), 'Cantoneira_%s' % n, BLK) for (a, b), n in zip(cants, ('base', 'central', 'topo'))]
        G = [nb(prism('xz', GREEN, a, b, FO.NewBodyFeatureOperation), 'Capa_verde_%s' % n, GRN) for (a, b), n in zip(covers, ('inferior', 'superior'))]
        HC = (150.0, 450.0)
        BOSSES = []
        for c in HC:
            poly = [(240, c - 25), (250, c - 25), (255, c - 20), (255, c + 20), (250, c + 25), (240, c + 25)]
            BOSSES.append((c, poly, nb(prism('xy', [(x, y, 0) for (x, y) in poly], 281, 286, FO.NewBodyFeatureOperation), 'Ressalto_dobradica_%d' % int(c), BLK)))
        log.append('bodies ok')
        for (c, poly, b), gb in zip(BOSSES, G):
            notch = [((236.0 if x < 244.4 else x), y) for (x, y) in offset_poly(poly, 0.8)]
            prism('xy', [(x, y, 0) for (x, y) in notch], 287, 280, FO.CutFeatureOperation, [gb])
        log.append('notch ok')
        # one detail per green cover: chamfered pocket on the side face
        def floor_area(gb):
            best = 0
            for f in gb.faces:
                ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
                if ok and n.x > 0.99 and abs(f.pointOnFace.x * 10 - 280.2) < 0.05:
                    best = max(best, f.area * 100)
            return best
        for (a, b), gb in zip(covers, G):
            P = [(281, a + 36, 236), (281, b - 36, 236), (281, b - 30, 242), (281, b - 30, 262), (281, b - 36, 268), (281, a + 36, 268), (281, a + 30, 262), (281, a + 30, 242)]
            full = (b - a - 60) * 32 - 4 * 18
            done = False
            for t in ('-45 deg', '45 deg'):
                try:
                    f = prism('yz', P, 281, 280.2, FO.CutFeatureOperation, [gb], t)
                    fa = floor_area(gb)
                    if fa and fa < full * 0.97:
                        log.append('pocket %s %.0f/%.0f' % (t, fa, full)); done = True; break
                    f.deleteMe()
                except Exception as ex:
                    log.append('pocket %s: %s' % (t, str(ex)[:60]))
            if not done:
                prism('yz', P, 281, 280.2, FO.CutFeatureOperation, [gb]); log.append('pocket straight')

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
        def mkpred(zf, xf):
            def P(n, p):
                return (n.z > 0.99 and abs(p.z * 10 - zf) < 0.02) or (xf is not None and n.x > 0.99 and abs(p.x * 10 - xf) < 0.02) or (xf is not None and n.x > 0.6 and n.z > 0.6)
            return P
        for gb in G: chamfer_outer(gb, mkpred(286, 281), 1.2)
        for (c, poly, b) in BOSSES: chamfer_outer(b, mkpred(286, None), 1.2)
        for cb in C: chamfer_outer(cb, mkpred(292, 287), 2.5)

        GF = []; GS = []; CF = []; CS = []
        for (a, b), gb in zip(covers, G):
            GF += [(266, a + 12, 286), (266, b - 12, 286)]; GS += [(281, a + 12, 252), (281, b - 12, 252)]
        for ys in ((20, 72), (326,), (574, 614)):
            for y in ys:
                CF.append((263, y, 292)); CS.append((287, y, 250))
        for cs, pl, s0, bodies in ((GF, 'xy', 286, G), (GS, 'yz', 281, G), (CF, 'xy', 292, C), (CS, 'yz', 287, C)):
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
        # frame column (context) from the original STEP
        frame = None
        for o in root.allOccurrences:
            if '1.20.2' not in o.name: continue
            for b in o.bRepBodies:
                bb = b.boundingBox
                if abs(bb.maxPoint.x * 10 - 268.5) < 1 and abs(bb.maxPoint.z * 10 - 273.5) < 1 and bb.maxPoint.y * 10 > 500 and bb.minPoint.y * 10 < 5:
                    frame = b
        GL = A.itemByName('R59_glass')
        extra = []
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        n0 = comp.bRepBodies.count
        try:
            for p in GF + CF: comp.bRepBodies.add(head(p, 2), bf)
            for p in GS + CS: comp.bRepBodies.add(head(p, 0), bf)
            for c in HC:
                leaf = box((241, c - 21, 286.2), (254, c + 21, 290))
                kn = tbm.createCylinderOrCone(P3(23.85, (c - 24) / 10.0, 28.85), 0.36, P3(23.85, (c + 24) / 10.0, 28.85), 0.36)
                dl = box((222, c - 16, 286.2), (238, c + 16, 288.6))
                tbm.booleanOperation(leaf, kn, adsk.fusion.BooleanTypes.UnionBooleanType)
                tbm.booleanOperation(leaf, dl, adsk.fusion.BooleanTypes.UnionBooleanType)
                comp.bRepBodies.add(leaf, bf); extra.append(('Dobradica_simplificada', BLK))
            comp.bRepBodies.add(box((224, 100, 276), (238, 505, 286)), bf); extra.append(('Porta_montante', BLK))
            comp.bRepBodies.add(box((196, 114, 279.5), (229, 491, 282.5)), bf); extra.append(('Porta_acrilico', GL))
            if frame is not None:
                comp.bRepBodies.add(tbm.copy(frame), bf); extra.append(('Perfil_impressora_ref', frame.appearance))
        finally:
            bf.finishEdit()
        ns = len(GF + CF + GS + CS)
        for i in range(n0, comp.bRepBodies.count):
            b = comp.bRepBodies.item(i)
            if i - n0 < ns:
                b.appearance = HW; b.name = 'M3_ISO7380_%d' % (i - n0)
            else:
                nm, ap = extra[i - n0 - ns]; b.name = nm
                if ap: b.appearance = ap
        log.append('screws/context ok frame=%s' % (frame is not None))
        for o in root.occurrences:
            if o.component.name in ('V2_ESTUDO_Canto_Harmonico', 'V2_EXEMPLO_Encaixe_Verde_Preto'):
                o.isLightBulbOn = False

        m = occ.transform2; m.translation = V3(100.0, 0, 0); occ.transform2 = m
        if des.snapshots.hasPendingSnapshot: des.snapshots.add()
        v = app.activeViewport; cam = v.camera; cam.isSmoothTransition = False
        cam.target = P3(124.0, 31.8, 26.0); cam.eye = P3(196.0, 70.0, 205.0); cam.upVector = V3(0, 1, 0)
        v.camera = cam; v.refresh()
        log.append('ok %d bodies' % comp.bRepBodies.count)
    except Exception:
        log.append(traceback.format_exc()[-600:])
    print(json.dumps(log))
