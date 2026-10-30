import adsk.core, adsk.fusion, json, traceback
FR = [[[230.7, 272.7], [231.8, 272.7]], [[231.8, 272.7], [231.94, 272.76], [232.0, 272.9]], [[232.0, 272.9], [232.0, 273.3]], [[232.0, 273.3], [232.06, 273.44], [232.2, 273.5]], [[232.2, 273.5], [260.66, 273.5]], [[260.66, 273.5], [260.8, 273.44]], [[260.8, 273.44], [261.47, 272.77]], [[261.47, 272.77], [261.53, 272.63], [261.47, 272.49]], [[261.47, 272.49], [261.19, 272.2]], [[261.19, 272.2], [261.13, 272.06], [261.19, 271.92]], [[261.19, 271.92], [261.97, 271.14]], [[261.97, 271.14], [262.11, 271.08], [262.25, 271.14]], [[262.25, 271.14], [262.54, 271.42]], [[262.54, 271.42], [262.68, 271.48], [262.82, 271.42]], [[262.82, 271.42], [263.95, 270.29]], [[263.95, 270.29], [264.01, 270.15], [263.95, 270.01]], [[263.95, 270.01], [263.67, 269.73]], [[263.67, 269.73], [263.61, 269.59], [263.67, 269.44]], [[263.67, 269.44], [264.44, 268.67]], [[264.44, 268.67], [264.59, 268.61], [264.73, 268.67]], [[264.73, 268.67], [265.01, 268.95]], [[265.01, 268.95], [265.15, 269.01], [265.29, 268.95]], [[265.29, 268.95], [266.42, 267.82]], [[266.42, 267.82], [266.48, 267.68], [266.42, 267.54]], [[266.42, 267.54], [266.14, 267.25]], [[266.14, 267.25], [266.08, 267.11], [266.14, 266.97]], [[266.14, 266.97], [266.92, 266.19]], [[266.92, 266.19], [267.06, 266.13], [267.2, 266.19]], [[267.2, 266.19], [267.49, 266.47]], [[267.49, 266.47], [267.63, 266.53], [267.77, 266.47]], [[267.77, 266.47], [268.44, 265.8]], [[268.44, 265.8], [268.5, 265.66]], [[268.5, 265.66], [268.5, 237.2]], [[268.5, 237.2], [268.44, 237.06], [268.3, 237.0]], [[268.3, 237.0], [267.9, 237.0]], [[267.9, 237.0], [267.76, 236.94], [267.7, 236.8]], [[267.7, 236.8], [267.7, 235.7]], [[267.7, 235.7], [267.76, 235.56], [267.9, 235.5]], [[267.9, 235.5], [268.3, 235.5]], [[268.3, 235.5], [268.44, 235.44], [268.5, 235.3]], [[268.5, 235.3], [268.5, 231.7]], [[268.5, 231.7], [268.44, 231.56], [268.3, 231.5]], [[268.3, 231.5], [265.1, 231.5]], [[265.1, 231.5], [265.0, 231.4]], [[265.0, 231.4], [265.0, 225.6]], [[265.0, 225.6], [264.9, 225.5]], [[264.9, 225.5], [262.6, 225.5]], [[262.6, 225.5], [262.5, 225.6]], [[262.5, 225.6], [262.5, 231.4]], [[262.5, 231.4], [262.4, 231.5]], [[262.4, 231.5], [260.1, 231.5]], [[260.1, 231.5], [260.0, 231.6]], [[260.0, 231.6], [260.0, 233.9]], [[260.0, 233.9], [260.06, 233.99]], [[260.06, 233.99], [263.0, 233.6]], [[263.0, 233.6], [265.5, 233.6]], [[265.5, 233.6], [265.5, 240.5]], [[265.5, 240.5], [265.4, 240.6]], [[265.4, 240.6], [263.01, 240.6]], [[263.01, 240.6], [262.99, 240.6]], [[262.99, 240.6], [260.11, 240.22]], [[260.11, 240.22], [260.0, 240.31]], [[260.0, 240.31], [260.0, 241.11]], [[260.0, 241.11], [260.09, 241.21]], [[260.09, 241.21], [262.99, 241.6]], [[262.99, 241.6], [263.01, 241.6]], [[263.01, 241.6], [265.4, 241.6]], [[265.4, 241.6], [265.5, 241.7]], [[265.5, 241.7], [265.5, 264.46]], [[265.5, 264.46], [265.47, 264.53]], [[265.47, 264.53], [259.53, 270.47]], [[259.53, 270.47], [259.46, 270.5]], [[259.46, 270.5], [256.1, 270.5]], [[256.1, 270.5], [256.0, 270.4]], [[256.0, 270.4], [256.0, 268.6]], [[256.0, 268.6], [256.1, 268.5]], [[256.1, 268.5], [258.93, 268.5]], [[258.93, 268.5], [259.03, 268.44]], [[259.03, 268.44], [259.79, 266.52]], [[259.79, 266.52], [259.8, 266.48]], [[259.8, 266.48], [259.8, 265.6]], [[259.8, 265.6], [259.7, 265.5]], [[259.7, 265.5], [259.1, 265.5]], [[259.1, 265.5], [259.0, 265.6]], [[259.0, 265.6], [259.0, 266.4]], [[259.0, 266.4], [258.9, 266.5]], [[258.9, 266.5], [250.1, 266.5]], [[250.1, 266.5], [250.0, 266.6]], [[250.0, 266.6], [250.0, 268.4]], [[250.0, 268.4], [250.1, 268.5]], [[250.1, 268.5], [252.9, 268.5]], [[252.9, 268.5], [253.0, 268.6]], [[253.0, 268.6], [253.0, 270.4]], [[253.0, 270.4], [252.9, 270.5]], [[252.9, 270.5], [229.1, 270.5]], [[229.1, 270.5], [229.0, 270.4]], [[229.0, 270.4], [229.0, 264.6]], [[229.0, 264.6], [228.9, 264.5]], [[228.9, 264.5], [226.6, 264.5]], [[226.6, 264.5], [226.5, 264.6]], [[226.5, 264.6], [226.5, 273.3]], [[226.5, 273.3], [226.56, 273.44], [226.7, 273.5]], [[226.7, 273.5], [230.3, 273.5]], [[230.3, 273.5], [230.44, 273.44], [230.5, 273.3]], [[230.5, 273.3], [230.5, 272.9]], [[230.5, 272.9], [230.56, 272.76], [230.7, 272.7]]]
def run(context):
    log = []
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        tbm = adsk.fusion.TemporaryBRepManager.get()
        P3 = adsk.core.Point3D.create; V3 = adsk.core.Vector3D.create; VI = adsk.core.ValueInput
        A = des.appearances
        BLK = A.itemByName('R59_body'); GRN = A.itemByName('R59_green'); GL = A.itemByName('R59_glass')
        GSK = A.itemByName('R59_led'); ALU = A.itemByName('Opaque(181,182,184)') or A.itemByName('R59_support')
        L = 60.0
        def box(x0, x1, z0, z1):
            ob = adsk.core.OrientedBoundingBox3D.create(P3((x0+x1)/20.0, L/20.0, (z0+z1)/20.0), V3(1,0,0), V3(0,1,0), (x1-x0)/10.0, L/10.0, (z1-z0)/10.0)
            return tbm.createBox(ob)
        def U(*bs):
            r = bs[0]
            for b in bs[1:]:
                tbm.booleanOperation(r, b, adsk.fusion.BooleanTypes.UnionBooleanType)
            return r
        m = adsk.core.Matrix3D.create(); m.translation = V3(60.0, 0, 0)
        occ = root.occurrences.addNewComponent(m)
        comp = occ.component
        comp.name = 'V2_ESTUDO_Vedacao_Corte'
        items = []
        # right door D
        items.append((U(box(0.6, 14, 276, 279.5), box(0.6, 14, 282.5, 286), box(0.6, 9, 279.5, 282.5), box(-8.5, 0.6, 276, 279)), BLK, 'Porta_D_montante_central'))
        items.append((U(box(224, 238, 276, 279.5), box(224, 238, 282.5, 286), box(229, 238, 279.5, 282.5)), BLK, 'Porta_D_montante_externo'))
        items.append((box(9, 229, 279.5, 282.5), GL, 'Porta_D_acrilico'))
        items.append((box(228, 236, 274.1, 276), GSK, 'Vedacao_perimetral_porta'))
        # left door E (partial)
        items.append((U(box(-14, -0.6, 280.5, 286), box(-14, -9.1, 276, 280.5)), BLK, 'Porta_E_montante_central'))
        items.append((box(-70, -9, 279.5, 282.5), GL, 'Porta_E_acrilico'))
        items.append((U(box(-70, -14, 276, 279.5), box(-70, -14, 282.5, 286)), BLK, 'Porta_E_moldura_corte'))
        items.append((box(-8.6, -1.2, 279, 280.5), GSK, 'Vedacao_encontro_portas'))
        # column
        items.append((U(box(240, 278.5, 274.5, 281), box(269.5, 272.5, 222, 274.5), box(272.5, 278.5, 222, 226)), BLK, 'Coluna_nucleo_preto'))
        items.append((box(242, 266, 274.0, 274.5), GSK, 'Espuma_coluna_frame'))
        for z in (238.0, 250.0, 262.0):
            c = tbm.createCylinderOrCone(P3(27.55, 0, z/10.0), 0.25, P3(27.55, L/10.0, z/10.0), 0.25)
            items.append((c, BLK, 'Cabo_5mm'))
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        try:
            for t, ap, nm in items:
                comp.bRepBodies.add(t, bf)
        finally:
            bf.finishEdit()
        for i, (t, ap, nm) in enumerate(items):
            b = comp.bRepBodies.item(i); b.appearance = ap; b.name = nm
        ext = comp.features.extrudeFeatures
        def sk_extrude(polys, ap, nm, largest=True):
            sk = comp.sketches.add(comp.xZConstructionPlane)
            lines = sk.sketchCurves.sketchLines
            for pts in polys:
                Q = [sk.modelToSketchSpace(P3(x/10.0, 0, z/10.0)) for (x, z) in pts]
                for i in range(len(Q) - 1):
                    if Q[i].distanceTo(Q[i+1]) > 1e-5:
                        lines.addByTwoPoints(Q[i], Q[i+1])
            sk.isVisible = False
            best = None; ba = -1
            for i in range(sk.profiles.count):
                pr = sk.profiles.item(i)
                a = pr.areaProperties().area
                if a > ba: best, ba = pr, a
            inp = ext.createInput(best, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            d = adsk.fusion.DistanceExtentDefinition.create(VI.createByReal(L/10.0))
            inp.setOneSideExtent(d, adsk.fusion.ExtentDirections.PositiveExtentDirection)
            f = ext.add(inp)
            b = f.bodies.item(0)
            bb = b.boundingBox
            if bb.minPoint.y < -0.01:
                f.deleteMe()
                inp = ext.createInput(best, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                inp.setOneSideExtent(d, adsk.fusion.ExtentDirections.NegativeExtentDirection)
                f = ext.add(inp); b = f.bodies.item(0)
            b.appearance = ap; b.name = nm
            return b
        green = [(244, 281), (278.5, 281), (278.5, 222), (281, 222), (281, 282), (277, 286), (244, 286), (244, 281)]
        sk_extrude([green], GRN, 'Coluna_capa_verde')
        sk_extrude(FR, ALU, 'Perfil_impressora_canto')
        log.append('ok %d' % comp.bRepBodies.count)
    except Exception:
        log.append(traceback.format_exc()[-500:])
    print(json.dumps(log))
