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
        for o in list(root.occurrences):
            if o.component.name.startswith('V2_ESTUDO_Base_Friso_LED'):
                o.deleteMe()
        GRN = des.appearances.itemByName('R59_green')
        HW = des.appearances.itemByName('R59_hardware') or des.appearances.itemByName('R59_body')
        NAMES = ['02_moldura_LED_relevo_3_1:1', '02_moldura_LED_relevo_1_1:1', '02_moldura_LED_relevo_2_1:1', '03_faixa_superior_1_1:1', '03_faixa_superior_2_1:1', '03_faixa_superior_3_1:1']
        SRC = [root.occurrences.itemByName(n).bRepBodies.item(0) for n in NAMES]
        occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component
        comp.name = 'V2_ESTUDO_Base_Friso_LED_13mm_v4'
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        try:
            for sb in SRC:
                comp.bRepBodies.add(tbm.copy(sb), bf)
        finally:
            bf.finishEdit()
        BB = [comp.bRepBodies.item(i) for i in range(len(SRC))]
        sideR, sideL, botC, fxL, fxC, fxR = BB
        for b, nm in zip(BB, ['Moldura_LED_D_mod', 'Moldura_LED_E_mod', 'Regua_baixo_central_mod', 'Faixa_sup_E_mod', 'Faixa_sup_C_mod', 'Faixa_sup_D_mod']):
            b.name = nm
        ZB, ZF = 292.5, 295.5
        Y0, Y1 = 42.0, 55.0
        def xs(y): return 132.3 + (y - Y0) * 1.5
        def xc(y): return xs(y) + 1.0
        ext = comp.features.extrudeFeatures
        def prism(polys, op, bodies=None):
            sk = comp.sketches.add(comp.xYConstructionPlane)
            L = sk.sketchCurves.sketchLines
            for pts in polys:
                Q = [P3(x/10.0, y/10.0, 0) for (x, y) in pts]
                for i in range(len(Q)):
                    L.addByTwoPoints(Q[i], Q[(i + 1) % len(Q)])
            sk.isVisible = False
            coll = adsk.core.ObjectCollection.create()
            for i in range(sk.profiles.count): coll.add(sk.profiles.item(i))
            inp = ext.createInput(coll, op)
            inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI.createByReal((ZF - ZB + (0.6 if op == FO.CutFeatureOperation else 0)) / 10.0)), adsk.fusion.ExtentDirections.PositiveExtentDirection)
            inp.startExtent = adsk.fusion.OffsetStartDefinition.create(VI.createByReal((ZB - (0.3 if op == FO.CutFeatureOperation else 0)) / 10.0))
            if bodies is not None:
                inp.participantBodies = bodies
            return ext.add(inp)
        # cut old nib/slope region from side pieces
        cutR = [(100.0, 41.0), (xc(41.0), 41.0), (xc(57.0), 57.0), (100.0, 57.0)]
        cutL = [(-x, y) for (x, y) in cutR]
        prism([cutR], FO.CutFeatureOperation, [sideR])
        prism([cutL], FO.CutFeatureOperation, [sideL])
        # extend side pieces top band to Y55
        bandR = [(xc(52.0), 52.0), (237.5, 52.0), (237.5, Y1), (xc(Y1), Y1)]
        bandL = [(-x, y) for (x, y) in bandR]
        prism([bandR], FO.JoinFeatureOperation, [sideR])
        prism([bandL], FO.JoinFeatureOperation, [sideL])
        log.append('sides ok')
        import math
        def circ_join(pts, body):
            sk = comp.sketches.add(comp.xYConstructionPlane)
            for (x, y) in pts:
                sk.sketchCurves.sketchCircles.addByCenterRadius(P3(x/10.0, y/10.0, 0), 0.2)
            sk.isVisible = False
            coll = adsk.core.ObjectCollection.create()
            for i in range(sk.profiles.count): coll.add(sk.profiles.item(i))
            inp = ext.createInput(coll, FO.JoinFeatureOperation)
            inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI.createByReal((ZF - ZB) / 10.0)), adsk.fusion.ExtentDirections.PositiveExtentDirection)
            inp.startExtent = adsk.fusion.OffsetStartDefinition.create(VI.createByReal(ZB / 10.0))
            inp.participantBodies = [body]
            try:
                ext.add(inp)
            except Exception as ex:
                log.append('fill fail ' + str(ex)[:50])
        circ_join([(130, 10), (175, 10)], sideR)
        circ_join([(-130, 10), (-175, 10)], sideL)
        circ_join([(-60, 10), (60, 10)], botC)
        circ_join([(-216, 73), (-95, 73)], fxL)
        circ_join([(-45, 71), (45, 71)], fxC)
        circ_join([(95, 73), (216, 73)], fxR)
        log.append('holes filled')
        # center strip
        cen = [(-xs(Y0), Y0), (xs(Y0), Y0), (xs(Y1), Y1), (-xs(Y1), Y1)]
        f = prism([cen], FO.NewBodyFeatureOperation)
        strip = f.bodies.item(0); strip.name = 'Friso_LED_central_13mm'
        for b in BB + [strip]:
            b.appearance = GRN
        # chamfer front edges that are still sharp
        ch = comp.features.chamferFeatures
        for b in (strip, sideR, sideL):
            front = None; fz = -1e9
            for fc in b.faces:
                ok, n = fc.evaluator.getNormalAtPoint(fc.pointOnFace)
                if ok and n.z > 0.99 and fc.pointOnFace.z > fz:
                    front, fz = fc, fc.pointOnFace.z
            e = adsk.core.ObjectCollection.create()
            for ed in front.edges:
                sharp = True
                for af in ed.faces:
                    if af == front: continue
                    ok, n = af.evaluator.getNormalAtPoint(af.pointOnFace)
                    if ok and abs(n.z) > 0.05: sharp = False
                if sharp and ed.length > 0.15: e.add(ed)
            if e.count:
                ci = ch.createInput2()
                ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(e, VI.createByReal(0.1), False)
                try:
                    ch.add(ci)
                except Exception as ex:
                    log.append('ch fail ' + str(ex)[:60])
        # screws on center strip
        def box(x0, x1, y0, y1, z0, z1):
            ob = adsk.core.OrientedBoundingBox3D.create(P3((x0+x1)/20.0, (y0+y1)/20.0, (z0+z1)/20.0), V3(1,0,0), V3(0,1,0), (x1-x0)/10.0, (y1-y0)/10.0, (z1-z0)/10.0)
            return tbm.createBox(ob)
        scr = []
        for sx in (-1, 1):
            for (x, y) in ((45, 70.5), (105, 70.5), (200, 70.5), (105, 48.5), (200, 48.5), (105, 11.5), (200, 11.5)):
                scr.append((sx * x, y))
        sk = comp.sketches.add(comp.xYConstructionPlane)
        for (x, y) in scr:
            sk.sketchCurves.sketchCircles.addByCenterRadius(P3(x/10.0, y/10.0, 0), 0.325)
        sk.isVisible = False
        coll = adsk.core.ObjectCollection.create()
        for i in range(sk.profiles.count): coll.add(sk.profiles.item(i))
        inp = ext.createInput(coll, FO.CutFeatureOperation)
        inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI.createByReal(0.09)), adsk.fusion.ExtentDirections.NegativeExtentDirection)
        inp.startExtent = adsk.fusion.OffsetStartDefinition.create(VI.createByReal(ZF / 10.0))
        inp.participantBodies = BB + [strip]
        ext.add(inp)
        bf2 = comp.features.baseFeatures.add(); bf2.startEdit()
        n0 = comp.bRepBodies.count
        try:
            for (x, y) in scr:
                zf = ZF - 0.9
                sph = tbm.createSphere(P3(x/10.0, y/10.0, (zf - 1.9)/10.0), 0.35)
                tbm.booleanOperation(sph, box(x - 4, x + 4, y - 4, y + 4, zf, zf + 3), adsk.fusion.BooleanTypes.IntersectionBooleanType)
                tbm.booleanOperation(sph, box(x - 1.0, x + 1.0, y - 1.0, y + 1.0, zf + 1.0, zf + 3), adsk.fusion.BooleanTypes.DifferenceBooleanType)
                comp.bRepBodies.add(sph, bf2)
        finally:
            bf2.finishEdit()
        for i in range(n0, comp.bRepBodies.count):
            comp.bRepBodies.item(i).appearance = HW
        # hide originals
        for o in root.occurrences:
            if o.name in NAMES or o.name == '02_moldura_LED_relevo_2_2:1' or o.name.startswith('M25_02_moldura_LED') or o.name.startswith('M25_03_faixa_superior'):
                o.isLightBulbOn = False
        m = occ.transform2; m.translation = V3(0, 0, 0.01); occ.transform2 = m
        if des.snapshots.hasPendingSnapshot: des.snapshots.add()
        log.append('ok %d' % comp.bRepBodies.count)
    except Exception:
        log.append(traceback.format_exc()[-500:])
    print(json.dumps(log))
