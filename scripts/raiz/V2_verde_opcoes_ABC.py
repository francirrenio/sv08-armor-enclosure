import adsk.core, adsk.fusion, json, traceback, math

GREENS = {'72_verde_inferior_D_encaixe': (94.0, 298.0), '75_verde_superior_D': (354.0, 552.0)}

def run(context):
    log = []
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        tbm = adsk.fusion.TemporaryBRepManager.get()
        P3 = adsk.core.Point3D.create; V3 = adsk.core.Vector3D.create; VI = adsk.core.ValueInput
        FO = adsk.fusion.FeatureOperations
        base_occ = [o for o in root.occurrences if o.component.name == 'V2_ESTUDO_Canto_V1_Aproximado'][0]
        base = base_occ.component
        # 1) undo the side pocket (my last features in the study)
        for i in range(base.features.extrudeFeatures.count - 1, -1, -1):
            base.features.extrudeFeatures.item(i).deleteMe()
        for i in range(base.sketches.count - 1, -1, -1):
            base.sketches.item(i).deleteMe()
        log.append('pocket removed')
        for o in list(root.occurrences):
            if o.component.name.startswith('V2_ESTUDO_Verde_Opcao_'):
                o.deleteMe()

        def make_copy(tag, dx):
            m = adsk.core.Matrix3D.create(); m.translation = V3(dx, 0, 0)
            occ = root.occurrences.addNewComponent(m)
            comp = occ.component; comp.name = 'V2_ESTUDO_Verde_Opcao_' + tag
            src = [b for b in base.bRepBodies]
            bf = comp.features.baseFeatures.add(); bf.startEdit()
            try:
                for b in src: comp.bRepBodies.add(tbm.copy(b), bf)
            finally:
                bf.finishEdit()
            for i, b in enumerate(src):
                nb_ = comp.bRepBodies.item(i); nb_.name = b.name
                if b.appearance: nb_.appearance = b.appearance
            return comp

        def front_face(gb):
            best = None
            for f in gb.faces:
                ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
                if ok and n.z > 0.99 and abs(f.pointOnFace.z * 10 - 286.0) < 0.05:
                    if best is None or f.area > best.area: best = f
            return best

        def outer_poly(face):
            for lp in face.loops:
                if not lp.isOuter: continue
                pts = []
                for ce in lp.coEdges:
                    e = ce.edge
                    p = e.endVertex.geometry if ce.isOpposedToEdge else e.startVertex.geometry
                    pts.append((round(p.x * 10, 3), round(p.y * 10, 3)))
                return pts
            return []


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


        # ---------- option A: shadow line (V groove) ----------
        comp = make_copy('A_linha', 135.0)
        ext = comp.features.extrudeFeatures
        PL = {'xy': (comp.xYConstructionPlane, 2), 'yz': (comp.yZConstructionPlane, 0), 'xz': (comp.xZConstructionPlane, 1)}
        for nm, (y0, y1) in GREENS.items():
            gb = comp.bRepBodies.itemByName(nm)
            P = [(269.4, y0 - 6, 0), (270.6, y0 - 6, 0), (270.6, y1 + 6, 0), (269.4, y1 + 6, 0)]
            ok = False
            for t in ('-45 deg', '45 deg', None):
                try:
                    prism('xy', P, 286.01, 285.5, FO.CutFeatureOperation, [gb], t); ok = True; log.append('A %s %s' % (nm, t)); break
                except Exception as ex:
                    log.append('A fail %s %s' % (t, str(ex)[:50]))
        # ---------- option B: recessed field following the outline ----------
        comp = make_copy('B_degrau', 170.0)
        ext = comp.features.extrudeFeatures
        PL = {'xy': (comp.xYConstructionPlane, 2), 'yz': (comp.yZConstructionPlane, 0), 'xz': (comp.xZConstructionPlane, 1)}
        for nm, (y0, y1) in GREENS.items():
            gb = comp.bRepBodies.itemByName(nm)
            ff = front_face(gb)
            poly = outer_poly(ff)
            # drop collinear points
            clean = []
            n = len(poly)
            for i in range(n):
                a_, b_, c_ = poly[i - 1], poly[i], poly[(i + 1) % n]
                cr = (b_[0] - a_[0]) * (c_[1] - b_[1]) - (b_[1] - a_[1]) * (c_[0] - b_[0])
                if abs(cr) > 1e-3 and math.hypot(b_[0] - a_[0], b_[1] - a_[1]) > 0.05: clean.append(b_)
            inner = offset_poly(clean, -4.0)
            inner = [(x, min(max(y, y0 + 4.0), y1 - 4.0)) for (x, y) in inner]
            log.append('B %s outline %d -> %s' % (nm, len(clean), [(round(x, 1), round(y, 1)) for (x, y) in inner]))
            done = False
            for t in ('-45 deg', '45 deg'):
                try:
                    f = prism('xy', [(x, y, 0) for (x, y) in inner], 286.01, 285.2, FO.CutFeatureOperation, [gb], t)
                    # floor must be smaller than opening (walls flare outward)
                    fl = 0
                    for fc in gb.faces:
                        ok_, nn = fc.evaluator.getNormalAtPoint(fc.pointOnFace)
                        if ok_ and nn.z > 0.99 and abs(fc.pointOnFace.z * 10 - 285.2) < 0.05: fl = max(fl, fc.area)
                    xs = [x for x, y in inner]
                    if fl and fl * 100 < (max(xs) - min(xs)) * (y1 - y0) * 0.98:
                        done = True; log.append('B ok %s %s' % (nm, t)); break
                    f.deleteMe()
                except Exception as ex:
                    log.append('B fail %s %s' % (t, str(ex)[:60]))
            if not done:
                try:
                    prism('xy', [(x, y, 0) for (x, y) in inner], 286.01, 285.2, FO.CutFeatureOperation, [gb]); log.append('B straight')
                except Exception as ex:
                    log.append('B straight fail ' + str(ex)[:60])
        # ---------- option C: double facet on the corner ----------
        comp = make_copy('C_faceta', 205.0)
        ch = comp.features.chamferFeatures
        for nm in GREENS:
            gb = comp.bRepBodies.itemByName(nm)
            e = adsk.core.ObjectCollection.create()
            for ed in gb.edges:
                fs = [f for f in ed.faces]
                if len(fs) != 2: continue
                ns = []
                for f in fs:
                    ok_, nn = f.evaluator.getNormalAtPoint(f.pointOnFace); ns.append(nn)
                diag = [n_ for n_ in ns if n_.x > 0.6 and n_.z > 0.6]
                other = [n_ for n_ in ns if (n_.z > 0.99 or n_.x > 0.99)]
                if diag and other and ed.length > 5.0:
                    e.add(ed)
            for d in (2.5, 1.8):
                try:
                    ci = ch.createInput2(); ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(e, VI.createByReal(d / 10.0), False)
                    ch.add(ci); log.append('C %s n%d d%.1f' % (nm, e.count, d)); break
                except Exception as ex:
                    log.append('C fail ' + str(ex)[:60])
        v = app.activeViewport; cam = v.camera; cam.isSmoothTransition = False
        cam.target = P3(178.0, 20.0, 27.5); cam.eye = P3(205.0, 42.0, 190.0); cam.upVector = V3(0, 1, 0)
        v.camera = cam; v.refresh()
    except Exception:
        log.append(traceback.format_exc()[-700:])
    print(json.dumps(log))
