import adsk.core, adsk.fusion, json, traceback, math

# Lower front doors sized for the original Sovol acrylic (225 x 453 per door).
# Acrylic: X +-(1.5..226.5), Y 70.5..523.5 (touches column inner edge and top beam; bottom 10.5 mm in front of the step).
# Frame sits OUTSIDE the acrylic (8 mm) + 4 mm lip; seals on the printer faces (Z 273.5) with a 2 mm gasket.
ZP = 273.5; ZB = 275.5; ZFR = 285.5
AX0, AX1, AY0, AY1 = 1.5, 226.5, 70.5, 523.5
B = 8.0; LIP = 4.0
HING = (150.0, 450.0)
AXX, AXZ, RK = 236.0, 288.0, 3.5
ZONE = (-235.5, 235.5, 61.5, 532.5, 273.6, 300.0)
COMP = 'V2_ESTUDO_Portas_Inferiores_Acrilico453'
GUS = 25.0

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
        BLK = A.itemByName('R59_body'); GL = A.itemByName('R59_glass'); GK = A.itemByName('R59_led') or BLK
        D = adsk.fusion.BooleanTypes.DifferenceBooleanType; U = adsk.fusion.BooleanTypes.UnionBooleanType
        def box(x0, x1, y0, y1, z0, z1):
            return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(P3((x0 + x1) / 20.0, (y0 + y1) / 20.0, (z0 + z1) / 20.0), V3(1, 0, 0), V3(0, 1, 0), abs(x1 - x0) / 10.0, abs(y1 - y0) / 10.0, abs(z1 - z0) / 10.0))
        def mbox(s, x0, x1, *r):
            a_, b_ = s * x0, s * x1
            return box(min(a_, b_), max(a_, b_), *r)

        red = [o for o in root.occurrences if o.component.name == 'V2_ESTUDO_Profundidade_Reduzida'][0].component
        for o in list(root.occurrences):
            if o.component.name == COMP: o.deleteMe()

        # ---- 1) hide old V1 lower-door parts, cut the clearance zone out of the rest ----
        zx0, zx1, zy0, zy1, zz0, zz1 = ZONE
        hidden = []; parts = []
        for bd in red.bRepBodies:
            bb = bd.boundingBox
            x0, y0, z0, x1, y1, z1 = [v * 10 for v in (bb.minPoint.x, bb.minPoint.y, bb.minPoint.z, bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z)]
            if x0 > -252 and x1 < 252 and y0 > 61.0 and y1 < 545 and z0 > 270:
                if bd.isLightBulbOn:
                    bd.isLightBulbOn = False; hidden.append(bd.name)
                continue
            if not bd.isLightBulbOn: continue
            if x1 > zx0 and x0 < zx1 and y1 > zy0 and y0 < zy1 and z1 > zz0 and z0 < zz1:
                parts.append(bd)
        log.append('hidden %d, to trim %d: %s' % (len(hidden), len(parts), sorted(set(p.name for p in parts))[:40]))
        done_cut = any(red.features.item(i).name == 'V2_folga_portas_inferiores' for i in range(red.features.count))
        if parts and not done_cut:
            sk = red.sketches.add(red.xYConstructionPlane)
            sk.sketchCurves.sketchLines.addTwoPointRectangle(P3(zx0 / 10, zy0 / 10, 0), P3(zx1 / 10, zy1 / 10, 0))
            sk.isVisible = False
            ext = red.features.extrudeFeatures
            inp = ext.createInput(sk.profiles.item(0), FO.CutFeatureOperation)
            inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI.createByReal((zz1 - zz0) / 10)), adsk.fusion.ExtentDirections.PositiveExtentDirection)
            inp.startExtent = adsk.fusion.OffsetStartDefinition.create(VI.createByReal(zz0 / 10))
            inp.participantBodies = parts
            f = ext.add(inp); f.name = 'V2_folga_portas_inferiores'
            log.append('zone cut ok')

        # ---- 2) doors ----
        items = []  # (tbody, name, appearance)
        for s, side in ((1, 'D'), (-1, 'E')):
            fr = mbox(s, AX0, AX1 + B, AY0 - B, AY1 + B, ZB, ZFR)
            tbm.booleanOperation(fr, mbox(s, AX0 + 8.0, AX1 - LIP, AY0 + LIP, AY1 - LIP, ZB - 1, ZFR + 1), D)   # window
            tbm.booleanOperation(fr, mbox(s, AX0 - 2.0, AX1 + 0.5, AY0 - 0.5, AY1 + 0.5, 279.0, 282.4), D)   # acrylic slot (open at the centre)
            # 45 deg corner gussets inside the window (front layer only, over the acrylic corner)
            L = GUS; r2 = math.sqrt(2.0); big = 400.0
            wx0, wx1, wy0, wy1 = AX0 + 8.0, AX1 - LIP, AY0 + LIP, AY1 - LIP
            for (cx, cy, dx, dy) in ((wx0, wy0, 1, 1), (wx1, wy0, -1, 1), (wx0, wy1, 1, -1), (wx1, wy1, -1, -1)):
                ux, uy = s * dx / r2, dy / r2
                off = L / r2 - big / 2.0
                cxx, cyy = s * cx + ux * off, cy + uy * off
                ob = adsk.core.OrientedBoundingBox3D.create(P3(cxx / 10.0, cyy / 10.0, (282.4 + ZFR) / 20.0), V3(ux, uy, 0), V3(-uy, ux, 0), big / 10.0, big / 10.0, (ZFR - 282.4) / 10.0)
                tri = tbm.createBox(ob)
                sq = mbox(s, cx, cx + dx * L, min(cy, cy + dy * L), max(cy, cy + dy * L), 282.4, ZFR)
                tbm.booleanOperation(tri, sq, adsk.fusion.BooleanTypes.IntersectionBooleanType)
                tbm.booleanOperation(fr, tri, U)
            for c in HING:
                tbm.booleanOperation(fr, mbox(s, 231.5, AX1 + B + 1, c - 25, c + 25, 284.0, ZFR + 1), D)   # knuckle relief
            if s < 0:
                tbm.booleanOperation(fr, box(-AX0 - 8.5, -1.0, AY0 - B - 1, AY1 + B + 1, ZB - 1, 277.8), D)  # clears the right door's flange
            items.append((fr, 'Porta_%s_moldura' % side, BLK))
            items.append((mbox(s, AX0, AX1, AY0, AY1, 279.2, 282.2), 'Porta_%s_acrilico_225x453' % side, GL))
            gk = mbox(s, 0.0, AX1 + B, AY0 - B, AY1 + B, ZP, ZB)
            tbm.booleanOperation(gk, mbox(s, -1.0, AX1, AY0, AY1, ZP - 1, ZB + 1), D)
            items.append((gk, 'Porta_%s_vedacao_8x2' % side, GK))
            for c in HING:
                kn = tbm.createCylinderOrCone(P3(s * AXX / 10, (c - 24) / 10, AXZ / 10), RK / 10, P3(s * AXX / 10, (c + 24) / 10, AXZ / 10), RK / 10)
                leaf_f = mbox(s, 237.0, 252.0, c - 21, c + 21, 285.9, 288.9)
                leaf_d = mbox(s, 214.0, 234.0, c - 16, c + 16, ZFR, ZFR + 3.0)
                tbm.booleanOperation(kn, leaf_f, U); tbm.booleanOperation(kn, leaf_d, U)
                items.append((kn, 'Porta_%s_dobradica_%d' % (side, int(c)), BLK))
            items.append((mbox(s, 12.0, 20.0, 270.0, 330.0, ZFR, ZFR + 12.0), 'Porta_%s_puxador' % side, BLK))
        # right door centre flange (sits behind the left door's centre stile; left opens first)
        fl = box(-AX0 - 6.5, AX0, AY0 - B, AY1 + B, ZB, 277.3)
        items.append((fl, 'Porta_D_aba_central_vedacao', BLK))

        occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component; comp.name = COMP
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        try:
            for (t, n, ap) in items: comp.bRepBodies.add(t, bf)
        finally:
            bf.finishEdit()
        for i, (t, n, ap) in enumerate(items):
            bd = comp.bRepBodies.item(i); bd.name = n
            if ap: bd.appearance = ap
        # chamfer 1.2 on the front face of each frame
        ch = comp.features.chamferFeatures
        for side in ('D', 'E'):
            fb = comp.bRepBodies.itemByName('Porta_%s_moldura' % side)
            e = adsk.core.ObjectCollection.create()
            for f in fb.faces:
                ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
                if ok and n.z > 0.99 and abs(f.pointOnFace.z * 10 - ZFR) < 0.05:
                    for ed in f.edges: e.add(ed)
            for d in (1.2, 0.8):
                try:
                    ci = ch.createInput2(); ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(e, VI.createByReal(d / 10), False)
                    ch.add(ci); log.append('chamfer %s %.1f' % (side, d)); break
                except Exception as ex:
                    log.append('ch fail ' + str(ex)[:50])
        v = app.activeViewport; cam = v.camera; cam.isSmoothTransition = False
        cam.target = P3(0, 30.0, 27.0); cam.eye = P3(70.0, 55.0, 150.0); cam.upVector = V3(0, 1, 0); cam.viewExtents = 60.0
        v.camera = cam; v.refresh()
        log.append('ok %d bodies' % comp.bRepBodies.count)
    except Exception:
        log.append(traceback.format_exc()[-700:])
    print(json.dumps(log))
