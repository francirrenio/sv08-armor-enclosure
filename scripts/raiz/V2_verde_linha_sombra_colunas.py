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
        for o in list(root.occurrences):
            if o.component.name == 'V2_ESTUDO_Verde_Linha_Sombra_Colunas':
                o.deleteMe()
        def vis(o):
            while o:
                if not o.isLightBulbOn: return False
                o = o.assemblyContext
            return True
        picks = []
        for o in root.allOccurrences:
            if not vis(o) or o.component.name.startswith('V2_E'): continue
            for bd in o.bRepBodies:
                if not bd.isLightBulbOn or not bd.appearance or bd.appearance.name != 'R59_green': continue
                bb = bd.boundingBox
                x0, z0, x1, z1 = bb.minPoint.x * 10, bb.minPoint.z * 10, bb.maxPoint.x * 10, bb.maxPoint.z * 10
                # vertical column covers: L-shaped, at the corners (|x| > 225 and |z| > 245)
                if min(abs(x0), abs(x1)) > 225 and min(abs(z0), abs(z1)) > 245:
                    label = (o.name.split(':')[0] if not bd.name.startswith('SV08_') else bd.name)[:60]
                    picks.append((label, bd))
        log.append('covers %d' % len(picks))
        occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component; comp.name = 'V2_ESTUDO_Verde_Linha_Sombra_Colunas'
        ext = comp.features.extrudeFeatures
        PL = {'xy': (comp.xYConstructionPlane, 2), 'yz': (comp.yZConstructionPlane, 0), 'xz': (comp.xZConstructionPlane, 1)}
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        try:
            for (l, bd) in picks: comp.bRepBodies.add(tbm.copy(bd), bf)
        finally:
            bf.finishEdit()
        bodies = []
        for i, (l, bd) in enumerate(picks):
            nb_ = comp.bRepBodies.item(i); nb_.name = l; nb_.appearance = bd.appearance; bodies.append(nb_)
            bd.isLightBulbOn = False
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


        for gb in bodies:
            bb = gb.boundingBox
            sz = 1 if (bb.minPoint.z + bb.maxPoint.z) > 0 else -1
            sx = 1 if (bb.minPoint.x + bb.maxPoint.x) > 0 else -1
            best = None
            for f in gb.faces:
                ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
                if ok and n.z * sz > 0.99:
                    if best is None or f.area > best.area: best = f
            if best is None:
                log.append('no face ' + gb.name); continue
            fb = best.boundingBox
            zf = best.pointOnFace.z * 10
            xe = max(abs(fb.minPoint.x), abs(fb.maxPoint.x)) * 10  # facet side edge
            xc = sx * (xe - 5.2)
            y0 = bb.minPoint.y * 10 - 6; y1 = bb.maxPoint.y * 10 + 6
            P = [(xc - 0.6, y0, 0), (xc + 0.6, y0, 0), (xc + 0.6, y1, 0), (xc - 0.6, y1, 0)]
            done = False
            for t in ('-45 deg', '45 deg', None):
                try:
                    prism('xy', P, zf + 0.01 * sz, zf - 0.5 * sz, FO.CutFeatureOperation, [gb], t)
                    log.append('%s x%.1f z%.1f %s' % (gb.name, xc, zf, t)); done = True; break
                except Exception as ex:
                    last = str(ex)[:50]
            if not done: log.append('fail %s %s' % (gb.name, last))
        v = app.activeViewport; cam = v.camera; cam.isSmoothTransition = False
        cam.target = P3(0, 45.0, 0); cam.eye = P3(130.0, 110.0, 190.0); cam.upVector = V3(0, 1, 0)
        v.camera = cam; v.refresh()
    except Exception:
        log.append(traceback.format_exc()[-700:])
    print(json.dumps(log))
