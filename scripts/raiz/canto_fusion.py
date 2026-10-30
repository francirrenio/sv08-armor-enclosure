import adsk.core, adsk.fusion, json, traceback

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
        BLK = A.itemByName('R59_body'); GRN = A.itemByName('R59_green'); GL = A.itemByName('R59_glass')
        HW = A.itemByName('R59_hardware') or BLK
        for o in list(root.occurrences):
            if o.component.name == 'V2_ESTUDO_Canto_Harmonico':
                o.deleteMe()
        m = adsk.core.Matrix3D.create(); m.translation = V3(100.0, 0, 0)
        occ = root.occurrences.addNewComponent(m)
        comp = occ.component
        comp.name = 'V2_ESTUDO_Canto_Harmonico'
        planes = comp.constructionPlanes
        ext = comp.features.extrudeFeatures

        def off_plane(base, val, axis):
            pin = planes.createInput(); pin.setByOffset(base, VI.createByReal(val / 10.0)); p = planes.add(pin)
            o = p.geometry.origin
            cur = {'x': o.x, 'y': o.y, 'z': o.z}[axis] * 10
            if abs(cur - val) > 0.01:
                p.deleteMe()
                pin = planes.createInput(); pin.setByOffset(base, VI.createByReal(-val / 10.0)); p = planes.add(pin)
            p.isLightBulbOn = False
            return p

        def sketch_poly(pl, polys, to3d):
            sk = comp.sketches.add(pl)
            L = sk.sketchCurves.sketchLines
            for pts in polys:
                Q = [sk.modelToSketchSpace(to3d(*p)) for p in pts]
                for i in range(len(Q)):
                    L.addByTwoPoints(Q[i], Q[(i + 1) % len(Q)])
            sk.isVisible = False
            return sk

        def extrude(sk, pl, dist, op, bodies=None, into=False, taper=None):
            n = pl.geometry.normal
            coll = adsk.core.ObjectCollection.create()
            for i in range(sk.profiles.count): coll.add(sk.profiles.item(i))
            return extrude_profiles(coll, pl, dist, op, bodies, into, taper)

        def extrude_profiles(coll, pl, dist, op, bodies=None, into=False, taper=None, axis_sign=None):
            n = pl.geometry.normal
            comp_n = n.x + n.y + n.z
            pos = comp_n > 0
            if into: pos = not pos
            d = adsk.fusion.ExtentDirections.PositiveExtentDirection if pos else adsk.fusion.ExtentDirections.NegativeExtentDirection
            alts = [taper] + ([taper[1:] if taper.startswith('-') else '-' + taper] if taper else []) + [None]
            last = None
            for t in alts:
                try:
                    inp = ext.createInput(coll, op)
                    ed = adsk.fusion.DistanceExtentDefinition.create(VI.createByReal(dist / 10.0))
                    if t: inp.setOneSideExtent(ed, d, VI.createByString(t))
                    else: inp.setOneSideExtent(ed, d)
                    if bodies is not None: inp.participantBodies = bodies
                    return ext.add(inp)
                except Exception as ex:
                    last = ex
            log.append('extrude fail ' + str(last)[:60])
            return None

        XZ = comp.xZConstructionPlane; XY = comp.xYConstructionPlane; YZ = comp.yZConstructionPlane

        def prism_y(poly_xz, y0, y1, ap, nm):
            pl = off_plane(XZ, y0, 'y')
            sk = sketch_poly(pl, [poly_xz], lambda x, z: P3(x / 10.0, y0 / 10.0, z / 10.0))
            f = extrude(sk, pl, y1 - y0, FO.NewBodyFeatureOperation)
            b = f.bodies.item(0); b.appearance = ap; b.name = nm
            return b

        CANT = [(236, 280), (275, 280), (275, 214), (287, 214), (287, 286), (281, 292), (236, 292)]
        GREEN = [(244, 281), (278.5, 281), (278.5, 222), (281, 222), (281, 282), (277, 286), (244, 286)]
        CORE = [(240, 274.5), (278.5, 274.5), (278.5, 281), (240, 281)]
        g = 0.4
        cants = [(0.0, 92 - g), (286 + g, 366 - g), (520 + g, 636.0)]
        covers = [(92 + g, 286 - g), (366 + g, 520 - g)]
        core = prism_y(CORE, 0, 636, BLK, 'Nucleo_preto')
        C = [prism_y(CANT, a, b, BLK, 'Cantoneira_%d' % i) for i, (a, b) in enumerate(cants)]
        G = [prism_y(GREEN, a, b, GRN, 'Capa_verde_%d' % i) for i, (a, b) in enumerate(covers)]
        # door stile + acrylic (context)
        D = prism_y([(224, 276), (238, 276), (238, 286), (224, 286)], 86, 515, BLK, 'Porta_montante')
        AC = prism_y([(196, 279.5), (229, 279.5), (229, 282.5), (196, 282.5)], 100, 500, GL, 'Porta_acrilico')
        D2 = prism_y([(196, 276), (210, 276), (210, 286), (196, 286)], 86, 515, BLK, 'Porta_corte')
        log.append('bodies ok')
        # chamfers on outward faces
        ch = comp.features.chamferFeatures
        for b, d in [(cb, 1.5) for cb in C] + [(gb, 1.2) for gb in G] + [(D, 1.2), (D2, 1.0)]:
            e = adsk.core.ObjectCollection.create(); seen = set()
            for f in b.faces:
                ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
                if not ok: continue
                if n.z > 0.99 or n.x > 0.99 or abs(n.y) > 0.99:
                    if f.area < 0.5: continue
                    for ed in f.edges:
                        if ed.tempId in seen: continue
                        # only convex edges between outward faces
                        fs = [ff for ff in ed.faces]
                        ok2 = True
                        for ff in fs:
                            okn, nn = ff.evaluator.getNormalAtPoint(ff.pointOnFace)
                            if okn and (nn.z < -0.5 or nn.x < -0.5): ok2 = False
                        if ok2:
                            seen.add(ed.tempId); e.add(ed)
            if e.count:
                inp = ch.createInput2()
                inp.chamferEdgeSets.addEqualDistanceChamferEdgeSet(e, VI.createByReal(d / 10.0), False)
                try:
                    ch.add(inp)
                except Exception as ex:
                    log.append('ch fail %s %s' % (b.name, str(ex)[:50]))
        log.append('chamfer done')
        # hinge notches in green covers (front leg)
        zf = off_plane(XY, 286.0, 'z')
        for c, gb in ((150.0, G[0]), (450.0, G[1])):
            poly = [(243.0, c - 25), (252.0, c - 25), (257.0, c - 20), (257.0, c + 20), (252.0, c + 25), (243.0, c + 25)]
            sk = sketch_poly(zf, [poly], lambda x, y: P3(x / 10.0, y / 10.0, 28.6))
            extrude(sk, zf, 6.0, FO.CutFeatureOperation, [gb], into=True)
        log.append('notch ok')
        # side fields (opcao 1) on green covers, side face X=281
        xs = off_plane(YZ, 281.0, 'x')
        for (a, b), gb in zip(covers, G):
            poly = [(a + 18, 228.0), (b - 18, 228.0), (b - 18, 276.0), (a + 18, 276.0)]
            sk = sketch_poly(xs, [poly], lambda y, z: P3(28.1, y / 10.0, z / 10.0))
            extrude(sk, xs, 0.8, FO.CutFeatureOperation, [gb], into=True, taper='-45 deg')
        # cantoneira fields front (Z=292) and side (X=287)
        zc = off_plane(XY, 292.0, 'z'); xc = off_plane(YZ, 287.0, 'x')
        for (a, b), cb in zip(cants, C):
            fa, fb = a + 20, b - 20
            sk = sketch_poly(zc, [[(242.0, fa), (276.0, fa), (276.0, fb), (242.0, fb)]], lambda x, y: P3(x / 10.0, y / 10.0, 29.2))
            extrude(sk, zc, 0.8, FO.CutFeatureOperation, [cb], into=True, taper='-45 deg')
            sk = sketch_poly(xc, [[(fa, 220.0), (fb, 220.0), (fb, 280.0), (fa, 280.0)]], lambda y, z: P3(28.7, y / 10.0, z / 10.0))
            extrude(sk, xc, 0.8, FO.CutFeatureOperation, [cb], into=True, taper='-45 deg')
        log.append('fields ok')
        # screws: functional pairs
        def box(x0, x1, y0, y1, z0, z1):
            ob = adsk.core.OrientedBoundingBox3D.create(P3((x0+x1)/20.0, (y0+y1)/20.0, (z0+z1)/20.0), V3(1,0,0), V3(0,1,0), (x1-x0)/10.0, (y1-y0)/10.0, (z1-z0)/10.0)
            return tbm.createBox(ob)
        front_scr = []  # (x, y, zface, body)
        side_scr = []   # (y, z, xface, body)
        for (a, b), cb in zip(cants, C):
            for y in (a + 10, b - 10):
                front_scr.append((259.0, y, 292.0, cb)); side_scr.append((y, 247.0, 287.0, cb))
        for (a, b), gb in zip(covers, G):
            for y in (a + 9, b - 9):
                front_scr.append((268.0, y, 286.0, gb)); side_scr.append((y, 252.0, 281.0, gb))
        for (x, y, zf_, b) in front_scr:
            pl = off_plane(XY, zf_, 'z')
            sk = comp.sketches.add(pl)
            sk.sketchCurves.sketchCircles.addByCenterRadius(sk.modelToSketchSpace(P3(x / 10.0, y / 10.0, zf_ / 10.0)), 0.325)
            sk.isVisible = False
            extrude(sk, pl, 0.9, FO.CutFeatureOperation, [b], into=True)
        for (y, z, xf, b) in side_scr:
            pl = off_plane(YZ, xf, 'x')
            sk = comp.sketches.add(pl)
            sk.sketchCurves.sketchCircles.addByCenterRadius(sk.modelToSketchSpace(P3(xf / 10.0, y / 10.0, z / 10.0)), 0.325)
            sk.isVisible = False
            extrude(sk, pl, 0.9, FO.CutFeatureOperation, [b], into=True)
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        n0 = comp.bRepBodies.count
        try:
            for (x, y, zf_, b) in front_scr:
                z = zf_ - 0.9
                s = tbm.createSphere(P3(x / 10.0, y / 10.0, (z - 1.9) / 10.0), 0.35)
                tbm.booleanOperation(s, box(x - 4, x + 4, y - 4, y + 4, z, z + 3), adsk.fusion.BooleanTypes.IntersectionBooleanType)
                tbm.booleanOperation(s, box(x - 1, x + 1, y - 1, y + 1, z + 1.0, z + 3), adsk.fusion.BooleanTypes.DifferenceBooleanType)
                comp.bRepBodies.add(s, bf)
            for (y, z, xf, b) in side_scr:
                x = xf - 0.9
                s = tbm.createSphere(P3((x - 1.9) / 10.0, y / 10.0, z / 10.0), 0.35)
                tbm.booleanOperation(s, box(x, x + 3, y - 4, y + 4, z - 4, z + 4), adsk.fusion.BooleanTypes.IntersectionBooleanType)
                tbm.booleanOperation(s, box(x + 1.0, x + 3, y - 1, y + 1, z - 1, z + 1), adsk.fusion.BooleanTypes.DifferenceBooleanType)
                comp.bRepBodies.add(s, bf)
            # hinges (simplified, black)
            for c in (150.0, 450.0):
                leaf = box(244.6, 256.4, c - 21, c + 21, 281.2, 289.5)
                kn = tbm.createCylinderOrCone(P3(24.05, (c - 24) / 10.0, 28.85), 0.36, P3(24.05, (c + 24) / 10.0, 28.85), 0.36)
                dl = box(222.0, 240.0, c - 16, c + 16, 286.2, 288.6)
                tbm.booleanOperation(leaf, kn, adsk.fusion.BooleanTypes.UnionBooleanType)
                tbm.booleanOperation(leaf, dl, adsk.fusion.BooleanTypes.UnionBooleanType)
                comp.bRepBodies.add(leaf, bf)
        finally:
            bf.finishEdit()
        nsc = len(front_scr) + len(side_scr)
        for i in range(n0, comp.bRepBodies.count):
            bb = comp.bRepBodies.item(i)
            if i - n0 < nsc:
                bb.appearance = HW; bb.name = 'M3_ISO7380'
            else:
                bb.appearance = BLK; bb.name = 'Dobradica_simplificada'
        log.append('ok %d' % comp.bRepBodies.count)
    except Exception:
        log.append(traceback.format_exc()[-600:])
    print(json.dumps(log))
