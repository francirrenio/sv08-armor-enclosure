import adsk.core, adsk.fusion, json, traceback
FR = [p for n, polys in json.load(open(r'F:\SV08 Eclosure\docs\planos\carenagem\_scripts\v1_secoes_canto.json'))['230.0'] if '1.20.2' in n for p in polys]
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
