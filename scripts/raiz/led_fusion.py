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
        A = des.appearances
        BLK = A.itemByName('R59_body'); GRN = A.itemByName('R59_green')
        LED = A.itemByName('R59_led') or GRN; HW = A.itemByName('R59_hardware') or BLK

        def box(x0, x1, y0, y1, z0, z1):
            ob = adsk.core.OrientedBoundingBox3D.create(P3((x0+x1)/20.0, (y0+y1)/20.0, (z0+z1)/20.0), V3(1,0,0), V3(0,1,0), (x1-x0)/10.0, (y1-y0)/10.0, (z1-z0)/10.0)
            return tbm.createBox(ob)

        m = adsk.core.Matrix3D.create()
        m.translation = V3(100.0, 50.0, 28.0)
        occ = root.occurrences.addNewComponent(m)
        comp = occ.component
        comp.name = 'V2_ESTUDO_Frente_Base_LED_A_B'
        OA, OB = 125.0, 0.0
        items = []  # (tbody, appearance, name, chamfer_mm)
        for oy in (OA, OB):
            items.append((box(-236, 236, oy, oy + 82, -8, 0), BLK, 'nucleo', 1.5))
            items.append((box(236.6, 293, oy - 4, oy + 92, -14, 12), BLK, 'cantoneira_D', 3.0))
            items.append((box(-293, -236.6, oy - 4, oy + 92, -14, 12), BLK, 'cantoneira_E', 3.0))
        # option A
        items.append((box(-226, -0.4, OA + 4, OA + 78, 0, 5), GRN, 'A_verde_E', 1.2))
        items.append((box(0.4, 226, OA + 4, OA + 78, 0, 5), GRN, 'A_verde_D', 1.2))
        items.append((box(-198, 198, OA + 24, OA + 34, -3, 1.5), LED, 'A_difusor_LED', 0))
        # option B
        items.append((box(-222, 222, OB + 6, OB + 30, 0, 6), BLK, 'B_barra_LED_preta', 1.5))
        items.append((box(-194, 194, OB + 13, OB + 23, -2, 3), LED, 'B_difusor_LED', 0))
        items.append((box(-226, -0.4, OB + 34, OB + 78, 0, 5), GRN, 'B_verde_E', 1.2))
        items.append((box(0.4, 226, OB + 34, OB + 78, 0, 5), GRN, 'B_verde_D', 1.2))
        bf = comp.features.baseFeatures.add()
        bf.startEdit()
        try:
            for t, ap, nm, c in items:
                comp.bRepBodies.add(t, bf)
        finally:
            bf.finishEdit()
        B = {}
        for i, (t, ap, nm, c) in enumerate(items):
            b = comp.bRepBodies.item(i)
            b.appearance = ap
            key = nm if nm not in B else nm + '_%d' % i
            b.name = key
            B[key] = (b, c)
        ch = comp.features.chamferFeatures
        for key, (b, c) in B.items():
            if c <= 0: continue
            best = None; bz = -1e9
            for f in b.faces:
                ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
                if ok and n.z > 0.99 and f.pointOnFace.z > bz:
                    best, bz = f, f.pointOnFace.z
            e = adsk.core.ObjectCollection.create()
            for ed in best.edges: e.add(ed)
            inp = ch.createInput2()
            inp.chamferEdgeSets.addEqualDistanceChamferEdgeSet(e, VI.createByReal(c / 10.0), False)
            try:
                ch.add(inp)
            except Exception as ex:
                log.append('ch ' + key + str(ex)[:40])
        log.append('base ok')

        planes = comp.constructionPlanes
        ext = comp.features.extrudeFeatures
        def plane_at(z):
            pin = planes.createInput(); pin.setByOffset(comp.xYConstructionPlane, VI.createByReal(z / 10.0))
            p = planes.add(pin); p.isLightBulbOn = False; return p
        P5 = plane_at(5.0); P6 = plane_at(6.0)
        def cut_rects(pl, rects, depth, bodies, taper):
            sk = comp.sketches.add(pl)
            for (x0, y0, x1, y1) in rects:
                sk.sketchCurves.sketchLines.addTwoPointRectangle(P3(x0/10.0, y0/10.0, 0), P3(x1/10.0, y1/10.0, 0))
            coll = adsk.core.ObjectCollection.create()
            for i in range(sk.profiles.count): coll.add(sk.profiles.item(i))
            sk.isVisible = False
            alt = taper[1:] if taper and taper.startswith('-') else ('-' + taper if taper else None)
            for t in (taper, alt, None):
                try:
                    inp = ext.createInput(coll, adsk.fusion.FeatureOperations.CutFeatureOperation)
                    ed = adsk.fusion.DistanceExtentDefinition.create(VI.createByReal(depth / 10.0))
                    if t: inp.setOneSideExtent(ed, adsk.fusion.ExtentDirections.NegativeExtentDirection, VI.createByString(t))
                    else: inp.setOneSideExtent(ed, adsk.fusion.ExtentDirections.NegativeExtentDirection)
                    inp.participantBodies = bodies
                    return ext.add(inp)
                except Exception as ex:
                    log.append('cut %s: %s' % (t, str(ex)[:50]))
        gA = [B['A_verde_E'][0], B['A_verde_D'][0]]
        gB = [B['B_verde_E'][0], B['B_verde_D'][0]]
        bar = [B['B_barra_LED_preta'][0]]
        # A: LED slot through both halves, fields, grooves
        cut_rects(P5, [(-200, OA + 23, 200, OA + 35)], 5.0, gA, '-15 deg')
        cut_rects(P5, [(-214, OA + 44, -12, OA + 68), (12, OA + 44, 214, OA + 68)], 0.8, gA, '-45 deg')
        cut_rects(P5, [(-220, OA + 39.4, -6, OA + 40.6), (6, OA + 39.4, 220, OA + 40.6)], 0.6, gA, '-30 deg')
        # B: LED slot in black bar, fields on green
        cut_rects(P6, [(-196, OB + 13, 196, OB + 23)], 6.0, bar, '-15 deg')
        cut_rects(P5, [(-208, OB + 44, -18, OB + 68), (18, OB + 44, 208, OB + 68)], 0.8, gB, '-45 deg')
        log.append('cuts ok')
        # screws
        scr = []
        for sx in (-1, 1):
            for (x, y, z) in ((218, OA + 13, 5), (218, OA + 70, 5), (10, OA + 13, 5), (10, OA + 70, 5),
                              (210, OB + 18, 6), (218, OB + 40.5, 5), (218, OB + 71.5, 5), (10, OB + 40.5, 5), (10, OB + 71.5, 5)):
                scr.append((sx * x, y, z))
        for zf in (5, 6):
            sk = comp.sketches.add(P5 if zf == 5 else P6)
            for (x, y, z) in scr:
                if z == zf:
                    sk.sketchCurves.sketchCircles.addByCenterRadius(P3(x/10.0, y/10.0, 0), 0.325)
            coll = adsk.core.ObjectCollection.create()
            for i in range(sk.profiles.count): coll.add(sk.profiles.item(i))
            sk.isVisible = False
            inp = ext.createInput(coll, adsk.fusion.FeatureOperations.CutFeatureOperation)
            inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI.createByReal(0.09)), adsk.fusion.ExtentDirections.NegativeExtentDirection)
            inp.participantBodies = (gA + gB) if zf == 5 else bar
            try:
                ext.add(inp)
            except Exception as ex:
                log.append('cb ' + str(ex)[:60])
        bf2 = comp.features.baseFeatures.add(); bf2.startEdit()
        n0 = comp.bRepBodies.count
        try:
            for (x, y, zt) in scr:
                z = zt - 0.9
                sph = tbm.createSphere(P3(x/10.0, y/10.0, (z - 2.6)/10.0), 0.42)
                tbm.booleanOperation(sph, box(x - 4, x + 4, y - 4, y + 4, z, z + 1.7), adsk.fusion.BooleanTypes.IntersectionBooleanType)
                tbm.booleanOperation(sph, box(x - 1.0, x + 1.0, y - 1.0, y + 1.0, z + 0.8, z + 3), adsk.fusion.BooleanTypes.DifferenceBooleanType)
                comp.bRepBodies.add(sph, bf2)
        finally:
            bf2.finishEdit()
        for i in range(n0, comp.bRepBodies.count):
            comp.bRepBodies.item(i).appearance = HW
        log.append('screws ok %d' % (comp.bRepBodies.count - n0))
    except Exception:
        log.append(traceback.format_exc()[-500:])
    print(json.dumps(log))
