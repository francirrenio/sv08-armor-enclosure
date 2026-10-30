import adsk.core, adsk.fusion, json
D = {"A": {"rail_bot": [[[0.724, 0.3], [24.0, 23.576], [33.876, 13.7], [202.124, 13.7], [212.0, 23.576], [235.276, 0.3]]], "rail_top": [[[235.276, 440.7], [212.0, 417.424], [202.124, 427.3], [33.876, 427.3], [24.0, 417.424], [0.724, 440.7]]], "stile_L": [[[0.3, 440.276], [23.576, 417.0], [13.7, 407.124], [13.7, 33.876], [23.576, 24.0], [0.3, 0.724]]], "stile_R": [[[235.7, 0.724], [212.424, 24.0], [222.3, 33.876], [222.3, 407.124], [212.424, 417.0], [235.7, 440.276]]]}, "B": {"U_bot": [[[0.3, 220.2], [13.7, 220.2], [13.7, 33.876], [33.876, 13.7], [202.124, 13.7], [222.3, 33.876], [222.3, 220.2], [235.7, 220.2], [235.7, 0.3], [0.3, 0.3]]], "U_top": [[[0.3, 440.7], [235.7, 440.7], [235.7, 220.8], [222.3, 220.8], [222.3, 407.124], [202.124, 427.3], [33.876, 427.3], [13.7, 407.124], [13.7, 220.8], [0.3, 220.8]]]}, "acr": [[[29.0, 6.0], [207.0, 6.0], [230.0, 29.0], [230.0, 412.0], [207.0, 435.0], [29.0, 435.0], [6.0, 412.0], [6.0, 29.0]]]}
def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    root = des.rootComponent
    m = adsk.core.Matrix3D.create()
    m.translation = adsk.core.Vector3D.create(0, 8.2, 28.0)
    occ = root.occurrences.addNewComponent(m)
    comp = occ.component
    comp.name = 'V2_ESTUDO_Molduras_Portas_A_B'
    BLK = des.appearances.itemByName('R59_body'); GL = des.appearances.itemByName('R59_glass')
    sk_plane = comp.xYConstructionPlane
    ext = comp.features.extrudeFeatures
    made = []
    def prism(pts, x0, z0, h, ap, nm):
        sk = comp.sketches.add(sk_plane)
        lines = sk.sketchCurves.sketchLines
        P = [adsk.core.Point3D.create((x0 + p[0]) / 10.0, p[1] / 10.0, 0) for p in pts]
        for i in range(len(P)):
            lines.addByTwoPoints(P[i], P[(i + 1) % len(P)])
        prof = sk.profiles.item(0)
        inp = ext.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(h / 10.0)), adsk.fusion.ExtentDirections.PositiveExtentDirection)
        inp.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(z0 / 10.0))
        f = ext.add(inp)
        b = f.bodies.item(0)
        b.name = nm
        b.appearance = ap
        made.append(b)
        sk.isVisible = False
        return b
    frames = []
    for key, x0 in (('A', 400.0), ('B', 700.0)):
        for n, polys in D[key].items():
            frames.append(prism(polys[0], x0, 0.0, 10.0, BLK, 'Moldura_%s_%s' % (key, n)))
        prism(D['acr'], x0, 3.0, 3.0, GL, 'Acrilico_%s' % key)
    ch = comp.features.chamferFeatures
    for b in frames:
        best = None
        for f in b.faces:
            ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
            if ok and n.z > 0.99:
                best = f
        e = adsk.core.ObjectCollection.create()
        for ed in best.edges: e.add(ed)
        inp = ch.createInput2()
        inp.chamferEdgeSets.addEqualDistanceChamferEdgeSet(e, adsk.core.ValueInput.createByReal(0.12), False)
        ch.add(inp)
    print(json.dumps({'bodies': comp.bRepBodies.count}))
