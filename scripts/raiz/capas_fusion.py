import adsk.core, adsk.fusion, json, traceback

def run(context):
    log = []
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        tbm = adsk.fusion.TemporaryBRepManager.get()
        P3 = adsk.core.Point3D.create
        V3 = adsk.core.Vector3D.create
        VI = adsk.core.ValueInput
        BLK = des.appearances.itemByName('R59_body')
        GRN = des.appearances.itemByName('R59_green')
        HW = des.appearances.itemByName('R59_hardware') or BLK

        def box(x0, x1, y0, y1, z0, z1):
            ob = adsk.core.OrientedBoundingBox3D.create(P3((x0+x1)/20.0, (y0+y1)/20.0, (z0+z1)/20.0), V3(1,0,0), V3(0,1,0), (x1-x0)/10.0, (y1-y0)/10.0, (z1-z0)/10.0)
            return tbm.createBox(ob)

        m = adsk.core.Matrix3D.create()
        m.translation = V3(100.0, 10.0, 28.0)
        occ = root.occurrences.addNewComponent(m)
        comp = occ.component
        comp.name = 'V2_ESTUDO_Capas_Verdes_1_2_3'
        OFFS = (0.0, 90.0, 180.0)
        H = 190.0
        bf = comp.features.baseFeatures.add()
        bf.startEdit()
        try:
            for ox in OFFS:
                core = box(ox - 6, ox + 40, -4, H + 4, -34, 0)
                comp.bRepBodies.add(core, bf)
                g = box(ox, ox + 37, 0, H, 0, 5)
                side = box(ox + 32, ox + 37, 0, H, -30, 5)
                tbm.booleanOperation(g, side, adsk.fusion.BooleanTypes.UnionBooleanType)
                comp.bRepBodies.add(g, bf)
        finally:
            bf.finishEdit()
        bodies = [comp.bRepBodies.item(i) for i in range(comp.bRepBodies.count)]
        cores = bodies[0::2]
        greens = bodies[1::2]
        for i, b in enumerate(cores):
            b.name = 'Nucleo_preto_%d' % (i + 1); b.appearance = BLK
        for i, b in enumerate(greens):
            b.name = 'Capa_verde_opcao_%d' % (i + 1); b.appearance = GRN

        ch = comp.features.chamferFeatures
        def chamfer_faces(b, pred, d):
            e = adsk.core.ObjectCollection.create()
            seen = set()
            for f in b.faces:
                ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
                if ok and pred(n, f):
                    for ed in f.edges:
                        if ed.tempId not in seen:
                            seen.add(ed.tempId); e.add(ed)
            if e.count:
                inp = ch.createInput2()
                inp.chamferEdgeSets.addEqualDistanceChamferEdgeSet(e, VI.createByReal(d / 10.0), False)
                ch.add(inp)
        for b in greens:
            chamfer_faces(b, lambda n, f: n.z > 0.99, 1.2)
        for b in greens:
            chamfer_faces(b, lambda n, f: n.x > 0.99, 1.2)
        for b in cores:
            chamfer_faces(b, lambda n, f: n.z > 0.99, 1.5)
        log.append('base ok')

        planes = comp.constructionPlanes
        pin = planes.createInput()
        pin.setByOffset(comp.xYConstructionPlane, VI.createByReal(0.5))
        front = planes.add(pin)
        front.isLightBulbOn = False
        ext = comp.features.extrudeFeatures

        def cut(sk, profiles, depth, body, taper=None):
            coll = adsk.core.ObjectCollection.create()
            for p in profiles: coll.add(p)
            inp = ext.createInput(coll, adsk.fusion.FeatureOperations.CutFeatureOperation)
            ed = adsk.fusion.DistanceExtentDefinition.create(VI.createByReal(depth / 10.0))
            if taper is not None:
                inp.setOneSideExtent(ed, adsk.fusion.ExtentDirections.NegativeExtentDirection, VI.createByString(taper))
            else:
                inp.setOneSideExtent(ed, adsk.fusion.ExtentDirections.NegativeExtentDirection)
            inp.participantBodies = [body]
            return ext.add(inp)

        def rect(sk, x0, y0, x1, y1):
            sk.sketchCurves.sketchLines.addTwoPointRectangle(P3(x0/10.0, y0/10.0, 0), P3(x1/10.0, y1/10.0, 0))

        def cut_rects(rects, depth, body, taper):
            sk = comp.sketches.add(front)
            for r in rects: rect(sk, *r)
            profs = [sk.profiles.item(i) for i in range(sk.profiles.count)]
            sk.isVisible = False
            alt = taper[1:] if taper and taper.startswith('-') else ('-' + taper if taper else None)
            for t in (taper, alt, None):
                try:
                    return cut(sk, profs, depth, body, t)
                except Exception as e:
                    log.append('taper %s fail: %s' % (t, str(e)[:60]))
            return None

        # --- option 1: recessed field + 2 grooves ---
        o = OFFS[0]; b = greens[0]
        cut_rects([(o + 6, 20, o + 30, 170)], 0.8, b, '-45 deg')
        cut_rects([(o + 3, 14.4, o + 34, 15.6), (o + 3, 174.4, o + 34, 175.6)], 0.6, b, '-30 deg')
        log.append('op1 ok')
        # --- option 2: rib bands top and bottom ---
        o = OFFS[1]; b = greens[1]
        rr = []
        for base in (22.0, 148.0):
            for k in range(5):
                y = base + k * 4.0
                rr.append((o + 6, y, o + 30, y + 1.6))
        cut_rects(rr, 0.8, b, '-30 deg')
        cut_rects([(o + 29.4, 50, o + 30.6, 140)], 0.6, b, '-30 deg')
        log.append('op2 ok')
        # --- option 3: long engraved line + name plate with SV08 ---
        o = OFFS[2]; b = greens[2]
        cut_rects([(o + 28.4, 20, o + 29.6, 135)], 0.6, b, '-30 deg')
        cut_rects([(o + 6, 145, o + 31, 172)], 0.8, b, '-45 deg')
        try:
            pin2 = planes.createInput()
            pin2.setByOffset(comp.xYConstructionPlane, VI.createByReal(0.42))
            fl = planes.add(pin2); fl.isLightBulbOn = False
            sk = comp.sketches.add(fl)
            ti = sk.sketchTexts.createInput2('SV08', 0.55)
            ti.setAsMultiLine(P3((o + 8.5)/10.0, 151.0/10.0, 0), P3((o + 28.5)/10.0, 166.0/10.0, 0), adsk.core.HorizontalAlignments.CenterHorizontalAlignment, adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
            st = sk.sketchTexts.add(ti)
            sk.isVisible = False
            inp = ext.createInput(st, adsk.fusion.FeatureOperations.CutFeatureOperation)
            inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI.createByReal(0.05)), adsk.fusion.ExtentDirections.NegativeExtentDirection)
            inp.participantBodies = [b]
            ext.add(inp)
            log.append('text ok')
        except Exception as e:
            log.append('text fail: ' + str(e)[:100])

        # --- screws: shallow counterbores + ISO7380 heads ---
        screws = []
        for o in OFFS:
            for y in (7.5, 182.5):
                screws.append((o + 18.5, y))
        sk = comp.sketches.add(front)
        for (x, y) in screws:
            sk.sketchCurves.sketchCircles.addByCenterRadius(P3(x/10.0, y/10.0, 0), 0.325)
        profs = []
        for i in range(sk.profiles.count):
            profs.append(sk.profiles.item(i))
        sk.isVisible = False
        for gi, gb in enumerate(greens):
            pp = [p for p in profs if abs(p.boundingBox.minPoint.x*10 - (OFFS[gi] + 15.25)) < 3]
            if pp:
                try:
                    cut(sk, pp, 0.9, gb, None)
                except Exception as e:
                    log.append('cb fail ' + str(e)[:60])
        bf2 = comp.features.baseFeatures.add()
        bf2.startEdit()
        n0 = comp.bRepBodies.count
        try:
            for (x, y) in screws:
                z = 4.1
                r = 2.85
                sph = tbm.createSphere(P3(x/10.0, y/10.0, (z - 2.6)/10.0), 0.42)
                capb = box(x - 4, x + 4, y - 4, y + 4, z, z + 1.7)
                tbm.booleanOperation(sph, capb, adsk.fusion.BooleanTypes.IntersectionBooleanType)
                cyl = tbm.createCylinderOrCone(P3(x/10.0, y/10.0, z/10.0 - 0.3), r/10.0, P3(x/10.0, y/10.0, (z + 0.4)/10.0), r/10.0)
                tbm.booleanOperation(sph, cyl, adsk.fusion.BooleanTypes.UnionBooleanType)
                hx = box(x - 1.0, x + 1.0, y - 1.0, y + 1.0, z + 0.8, z + 3)
                tbm.booleanOperation(sph, hx, adsk.fusion.BooleanTypes.DifferenceBooleanType)
                comp.bRepBodies.add(sph, bf2)
        finally:
            bf2.finishEdit()
        for i in range(n0, comp.bRepBodies.count):
            comp.bRepBodies.item(i).appearance = HW
            comp.bRepBodies.item(i).name = 'M3_ISO7380'
        log.append('screws ok')
    except Exception:
        log.append(traceback.format_exc()[-600:])
    print(json.dumps(log))
