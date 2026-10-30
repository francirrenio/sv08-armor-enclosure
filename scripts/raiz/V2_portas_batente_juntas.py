import adsk.core, adsk.fusion, json, traceback, math

# Lower front doors (original 225x453 acrylic) + black door stop (batente) + revolute joints.
# Printer front face Z 273.5. Batente skin Z 273.5..275.0; gasket 1 mm compressed; door Z 276..286 (flush with green).
ZP, ZSK, ZB, ZFR = 273.5, 275.0, 276.0, 286.0
AX0, AX1, AY0, AY1 = 1.5, 226.5, 70.5, 523.5
B, LIP, GUS = 8.0, 4.0, 25.0
SLOT0, SLOT1 = 279.5, 282.9          # acrylic slot
ACR0, ACR1 = 279.7, 282.7            # acrylic 3 mm
HING = (150.0, 450.0)
AXX, AXZ, RK = 236.0, 288.5, 3.5
GRP = '30_PORTAS_FRENTE'
NAMES = {'D': 'SV-30-01 Porta direita', 'E': 'SV-30-02 Porta esquerda', 'BAT': 'SV-30-03 Batente portas', 'TST': 'SV-30-99 Corpo de prova canto'}


def run(context):
    log = []
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        if app.activeDocument.name != 'SV08_V2_conceito':
            print('wrong doc'); return
        root = des.rootComponent
        tbm = adsk.fusion.TemporaryBRepManager.get()
        P3 = adsk.core.Point3D.create; V3 = adsk.core.Vector3D.create; VI = adsk.core.ValueInput
        A = des.appearances
        BLK = A.itemByName('R59_body'); GL = A.itemByName('R59_glass'); GK = A.itemByName('R59_led') or BLK
        D = adsk.fusion.BooleanTypes.DifferenceBooleanType; U = adsk.fusion.BooleanTypes.UnionBooleanType; I = adsk.fusion.BooleanTypes.IntersectionBooleanType

        def box(x0, x1, y0, y1, z0, z1):
            return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(P3((x0 + x1) / 20.0, (y0 + y1) / 20.0, (z0 + z1) / 20.0), V3(1, 0, 0), V3(0, 1, 0), abs(x1 - x0) / 10.0, abs(y1 - y0) / 10.0, abs(z1 - z0) / 10.0))
        def mbox(s, x0, x1, *r):
            a_, b_ = s * x0, s * x1
            return box(min(a_, b_), max(a_, b_), *r)

        # ---------- 0) suppress the user's merging extrusions (Extrusão2..16) in the depth-reduced set ----------
        red = None
        for o in root.allOccurrences:
            if o.component.name == 'V2_ESTUDO_Profundidade_Reduzida': red = o.component
        sup = []
        for f in red.features.extrudeFeatures:
            if f.name.startswith('Extrus') and f.name != 'V2_folga_portas_inferiores' and not f.timelineObject.isSuppressed:
                f.timelineObject.isSuppressed = True; sup.append(f.name)
        log.append('suppressed ' + ','.join(sup))

        grp = [o for o in root.occurrences if o.component.name == GRP][0]
        # remove previous runs, park the old door study
        for o in list(grp.childOccurrences):
            if o.component.name in NAMES.values(): o.deleteMe()
        for o in list(root.occurrences):
            if o.component.name == NAMES['TST']: o.deleteMe()
        for o in grp.childOccurrences:
            if o.component.name == 'V2_ESTUDO_Portas_Inferiores_Acrilico453': o.isLightBulbOn = False

        def make_comp(parent_occ, name, items, dx=0.0):
            m = adsk.core.Matrix3D.create(); m.translation = V3(dx / 10.0, 0, 0)
            occ = parent_occ.component.occurrences.addNewComponent(m)
            comp = occ.component; comp.name = name
            bf = comp.features.baseFeatures.add(); bf.startEdit()
            try:
                for (t, n, ap) in items: comp.bRepBodies.add(t, bf)
            finally:
                bf.finishEdit()
            for i, (t, n, ap) in enumerate(items):
                bd = comp.bRepBodies.item(i); bd.name = n
                if ap: bd.appearance = ap
            return occ, comp

        def chamfer_front(comp, bname, zf, d=1.2):
            fb = comp.bRepBodies.itemByName(bname)
            e = adsk.core.ObjectCollection.create()
            for f in fb.faces:
                ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
                if ok and n.z > 0.99 and abs(f.pointOnFace.z * 10 - zf) < 0.05:
                    for ed in f.edges: e.add(ed)
            for dd in (d, d * 0.6):
                try:
                    ci = comp.features.chamferFeatures.createInput2(); ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(e, VI.createByReal(dd / 10), False)
                    comp.features.chamferFeatures.add(ci); return True
                except Exception:
                    pass
            return False

        # ---------- 1) batente (door stop): thin black skin on the printer face + bottom sill filling the printer recess ----------
        bat = []
        for s in (1, -1):
            bat.append((mbox(s, 226.5, 235.5, 61.5, 532.5, ZP, ZSK), 'SV-30-03a batente lateral %s' % ('D' if s > 0 else 'E'), BLK))
        bat.append((box(-226.5, 226.5, 523.5, 532.5, ZP, ZSK), 'SV-30-03b batente superior', BLK))
        sill = box(-226.5, 226.5, 61.5, 81.0, 258.6, ZSK)
        prn = None
        for o in root.allOccurrences:
            if '1.20.1.1.54' in o.name and o.bRepBodies.count: prn = o.bRepBodies.item(0)
        if prn is not None:
            try:
                tbm.booleanOperation(sill, tbm.copy(prn), D); log.append('sill fitted to printer base')
            except Exception as ex:
                log.append('sill fit fail ' + str(ex)[:50])
        bat.append((sill, 'SV-30-03c soleira (degrau)', BLK))
        # fixed hinge leaves (on the column plate)
        for s in (1, -1):
            for c in HING:
                bat.append((mbox(s, 238.0, 252.0, c - 21, c + 21, 285.9, 288.9), 'SV-30-03d folha fixa %s %d' % ('D' if s > 0 else 'E', int(c)), BLK))
        bat_occ, bat_comp = make_comp(grp, NAMES['BAT'], bat)
        log.append('batente ok')

        # ---------- 2) doors ----------
        door_occ = {}
        for s, side in ((1, 'D'), (-1, 'E')):
            fr = mbox(s, AX0, AX1 + B, AY0 - B, AY1 + B, ZB, ZFR)
            tbm.booleanOperation(fr, mbox(s, AX0 + 8.0, AX1 - LIP, AY0 + LIP, AY1 - LIP, ZB - 1, ZFR + 1), D)
            tbm.booleanOperation(fr, mbox(s, AX0 - 2.0, AX1 + 0.5, AY0 - 0.5, AY1 + 0.5, SLOT0, SLOT1), D)
            L = GUS; r2 = math.sqrt(2.0); big = 400.0
            wx0, wx1, wy0, wy1 = AX0 + 8.0, AX1 - LIP, AY0 + LIP, AY1 - LIP
            for (cx, cy, dx, dy) in ((wx0, wy0, 1, 1), (wx1, wy0, -1, 1), (wx0, wy1, 1, -1), (wx1, wy1, -1, -1)):
                ux, uy = s * dx / r2, dy / r2
                off = L / r2 - big / 2.0
                ob = adsk.core.OrientedBoundingBox3D.create(P3((s * cx + ux * off) / 10.0, (cy + uy * off) / 10.0, (SLOT1 + ZFR) / 20.0), V3(ux, uy, 0), V3(-uy, ux, 0), big / 10.0, big / 10.0, (ZFR - SLOT1) / 10.0)
                tri = tbm.createBox(ob)
                tbm.booleanOperation(tri, mbox(s, cx, cx + dx * L, min(cy, cy + dy * L), max(cy, cy + dy * L), SLOT1, ZFR), I)
                tbm.booleanOperation(fr, tri, U)
            for c in HING:
                tbm.booleanOperation(fr, mbox(s, 231.5, AX1 + B + 1, c - 25, c + 25, 284.5, ZFR + 1), D)
            if s < 0:
                tbm.booleanOperation(fr, box(-AX0 - 8.5, -1.0, AY0 - B - 1, AY1 + B + 1, ZB - 1, 278.3), D)
            items = [(fr, 'SV-30-0%sa moldura' % ('1' if s > 0 else '2'), BLK),
                     (mbox(s, AX0, AX1, AY0, AY1, ACR0, ACR1), 'SV-30-0%sb acrilico 225x453' % ('1' if s > 0 else '2'), GL)]
            gk = mbox(s, 0.0, AX1 + B, AY0 - B, AY1 + B, ZSK, ZB)
            tbm.booleanOperation(gk, mbox(s, -1.0, AX1, AY0, AY1, ZSK - 1, ZB + 1), D)
            items.append((gk, 'SV-30-0%sc vedacao EPDM 8x2' % ('1' if s > 0 else '2'), GK))
            for c in HING:
                kn = tbm.createCylinderOrCone(P3(s * AXX / 10, (c - 24) / 10, AXZ / 10), RK / 10, P3(s * AXX / 10, (c + 24) / 10, AXZ / 10), RK / 10)
                items.append((kn, 'SV-30-0%sd eixo dobradica %d' % ('1' if s > 0 else '2', int(c)), BLK))
                items.append((mbox(s, 214.0, 234.0, c - 16, c + 16, ZFR, ZFR + 3.0), 'SV-30-0%se folha porta %d' % ('1' if s > 0 else '2', int(c)), BLK))
            items.append((mbox(s, 12.0, 20.0, 270.0, 330.0, ZFR, ZFR + 12.0), 'SV-30-0%sf puxador' % ('1' if s > 0 else '2'), BLK))
            if s > 0:
                items.append((box(-AX0 - 6.5, AX0, AY0 - B, AY1 + B, ZB, 277.8), 'SV-30-01g aba central vedacao', BLK))
            occ, comp = make_comp(grp, NAMES[side], items)
            chamfer_front(comp, items[0][1], ZFR)
            door_occ[side] = occ
        log.append('doors ok')

        # ---------- 3) ground the batente, revolute as-built joints on the hinge axis, 0..110 deg ----------
        bat_occ.isGrounded = True
        jl = []
        for side, s in (('D', 1), ('E', -1)):
            occ = door_occ[side]
            kn = occ.component.bRepBodies.itemByName('SV-30-0%sd eixo dobradica 150' % ('1' if s > 0 else '2'))
            cyl = None
            for f in kn.faces:
                if isinstance(f.geometry, adsk.core.Cylinder): cyl = f
            cyl_p = cyl.createForAssemblyContext(occ)
            jg = adsk.fusion.JointGeometry.createByNonPlanarFace(cyl_p, adsk.fusion.JointKeyPointTypes.MiddleKeyPoint)
            ji = grp.component.asBuiltJoints.createInput(occ, bat_occ, jg)
            ji.setAsRevoluteJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
            j = grp.component.asBuiltJoints.add(ji)
            j.name = 'Junta ' + NAMES[side]
            m = j.jointMotion
            # find opening sign: rotate +60 and see if the free edge moves to +Z
            fr = occ.component.bRepBodies.itemByName('SV-30-0%sa moldura' % ('1' if s > 0 else '2'))
            m.rotationValue = math.radians(60)
            zmax = occ.boundingBox.maxPoint.z * 10
            sign = 1 if zmax > 330 else -1
            m.rotationValue = 0
            lim = m.rotationLimits
            if sign > 0:
                lim.isMinimumValueEnabled = True; lim.minimumValue = 0.0
                lim.isMaximumValueEnabled = True; lim.maximumValue = math.radians(110)
            else:
                lim.isMinimumValueEnabled = True; lim.minimumValue = math.radians(-110)
                lim.isMaximumValueEnabled = True; lim.maximumValue = 0.0
            jl.append('%s sign %d zmax60 %.0f' % (side, sign, zmax))
        log.append(jl)

        # ---------- 4) test coupon: bottom outer corner of the right door + batente, 60 mm, set aside at X+80 cm ----------
        cut = box(170.0, 240.0, 55.0, 115.0, 250.0, 300.0)
        tst = []
        for comp, occ in ((door_occ['D'].component, door_occ['D']), (bat_comp, bat_occ)):
            for bd in comp.bRepBodies:
                t = tbm.copy(bd)
                try:
                    tbm.booleanOperation(t, tbm.copy(cut), I)
                    if t.faces.count: tst.append((t, bd.name, bd.appearance))
                except Exception:
                    pass
        make_comp(grp, NAMES['TST'], tst, dx=800.0)
        log.append('coupon %d bodies' % len(tst))
        if des.snapshots.hasPendingSnapshot: des.snapshots.add()
    except Exception:
        log.append(traceback.format_exc()[-800:])
    print(json.dumps(log))
