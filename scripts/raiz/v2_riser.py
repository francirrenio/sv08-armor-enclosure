import adsk.core, adsk.fusion, json, math, traceback

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    root = des.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()
    INT = adsk.fusion.BooleanTypes.IntersectionBooleanType
    UNI = adsk.fusion.BooleanTypes.UnionBooleanType
    DIF = adsk.fusion.BooleanTypes.DifferenceBooleanType
    P = adsk.core.Point3D.create
    V = adsk.core.Vector3D.create

    def box(x0, x1, y0, y1, z0, z1):  # mm
        ob = adsk.core.OrientedBoundingBox3D.create(P((x0+x1)/20.0, (y0+y1)/20.0, (z0+z1)/20.0), V(1,0,0), V(0,1,0), (x1-x0)/10.0, (y1-y0)/10.0, (z1-z0)/10.0)
        return tbm.createBox(ob)

    def mv(t, dx=0, dy=0, dz=0):
        m = adsk.core.Matrix3D.create(); m.translation = V(dx/10.0, dy/10.0, dz/10.0); tbm.transform(t, m); return t

    def mirx(t):
        m = adsk.core.Matrix3D.create(); m.setCell(0, 0, -1); tbm.transform(t, m); return t

    def mirz(t):
        m = adsk.core.Matrix3D.create(); m.setCell(2, 2, -1); tbm.transform(t, m); return t

    def stretch_remove(b, c0, c1, dlo, dhi):
        lo = tbm.copy(b); tbm.booleanOperation(lo, box(-1000, 1000, -1000, c0, -1000, 1000), INT); mv(lo, dy=dlo)
        hi = tbm.copy(b); tbm.booleanOperation(hi, box(-1000, 1000, c1, 3000, -1000, 1000), INT); mv(hi, dy=dhi)
        tbm.booleanOperation(lo, hi, UNI)
        return lo

    def screw(x, y, z, axis='z', r=2.6, h=1.6):
        # button head: cylinder + sphere cap, along +axis from point
        d = {'z': V(0,0,1), 'x': V(1,0,0), '-x': V(-1,0,0)}[axis]
        p0 = P(x/10.0, y/10.0, z/10.0)
        p1 = P((x + d.x*h*0.4)/10.0, (y)/10.0, (z + d.z*h*0.4)/10.0)
        cyl = tbm.createCylinderOrCone(p0, r/10.0, p1, r/10.0)
        sph = tbm.createSphere(P((x - d.x*r*0.6)/10.0, y/10.0, (z - d.z*r*0.6)/10.0), (r*1.25)/10.0)
        cap = box(x - 10, x + 10, y - 10, y + 10, z - 10, z + 10)
        # keep only the part in front of the surface
        if axis == 'z':
            tbm.booleanOperation(cap, box(x-10, x+10, y-10, y+10, z, z+h), INT)
        elif axis == 'x':
            tbm.booleanOperation(cap, box(x, x+h, y-10, y+10, z-10, z+10), INT)
        else:
            tbm.booleanOperation(cap, box(x-h, x, y-10, y+10, z-10, z+10), INT)
        tbm.booleanOperation(sph, cap, INT)
        tbm.booleanOperation(sph, cyl, UNI)
        # hex socket
        hx = box(x-1.0, x+1.0, y-1.0, y+1.0, z-1.0, z+1.0)
        if axis == 'z':
            hx = box(x-1.0, x+1.0, y-1.0, y+1.0, z+h-0.8, z+h+1)
        elif axis == 'x':
            hx = box(x+h-0.8, x+h+1, y-1.0, y+1.0, z-1.0, z+1.0)
        else:
            hx = box(x-h-1, x-h+0.8, y-1.0, y+1.0, z-1.0, z+1.0)
        tbm.booleanOperation(sph, hx, DIF)
        return sph

    BLK = des.appearances.itemByName('R59_body')
    GRN = des.appearances.itemByName('R59_green')
    HW = des.appearances.itemByName('R59_hardware')
    SCR = des.appearances.itemByName('R59_screen')
    if SCR is None:
        try:
            SCR = des.appearances.addByCopy(des.appearances.itemByName('R59_body'), 'R59_screen')
            for i in range(SCR.appearanceProperties.count):
                pr = SCR.appearanceProperties.item(i)
                if pr.objectType == adsk.core.ColorProperty.classType():
                    try:
                        pr.value = adsk.core.Color.create(12, 14, 18, 255)
                    except Exception:
                        pass
        except Exception:
            SCR = BLK

    items = []   # (tbody, appearance, name, chamfer_dir, chamfer_mm)

    Y0, Y1 = 558.0, 634.0
    # --- walls ---
    items.append((box(-236, 236, Y0, Y1, 290, 297), BLK, 'V2_Riser_Parede_Frente_Black', 'z', 1.2))
    items.append((box(-236, 236, Y0, Y1, -297, -290), BLK, 'V2_Riser_Parede_Tras_Black', '-z', 1.2))
    for side in (1, -1):
        w = box(277, 284, Y0, Y1, -248, 248)
        # louver windows
        for (za, zb) in ((-190, -60), (60, 190)):
            tbm.booleanOperation(w, box(276, 285, 568, 624, za, zb), DIF)
        back = box(276.5, 278, 568, 624, -190, 190)
        if side < 0:
            mirx(w); mirx(back)
        nm = 'D' if side > 0 else 'E'
        items.append((w, BLK, 'V2_Riser_Lateral_%s_Black' % nm, 'x' if side > 0 else '-x', 1.2))
        items.append((back, BLK, 'V2_Riser_Persiana_Fundo_%s_Black' % nm, None, 0))
        for (za, zb) in ((-190, -60), (60, 190)):
            for i in range(4):
                ya = 569 + i * 13.75
                s = box(279.5, 284, ya, ya + 12.6, za + 1.5, zb - 1.5)
                lip = box(278.2, 279.5, ya + 9.5, ya + 13.6, za + 1.5, zb - 1.5)
                tbm.booleanOperation(s, lip, UNI)
                if side < 0:
                    mirx(s)
                items.append((s, BLK, 'V2_Riser_Aleta_%s_%d_%d' % (nm, za, i), 'x' if side > 0 else '-x', 0.8))
        cov = box(284, 287.5, 574, 618, -42, 42)
        if side < 0:
            mirx(cov)
        items.append((cov, BLK, 'V2_Riser_Tampa_Servo_%s_Black' % nm, 'x' if side > 0 else '-x', 1.5))
        for (yy, zz) in ((580, -34), (580, 34), (612, -34), (612, 34)):
            sc = screw(287.5 if side > 0 else -287.5, yy, zz, axis='x' if side > 0 else '-x', r=2.3, h=1.5)
            items.append((sc, HW or BLK, 'V2_Riser_M3_Servo_%s' % nm, None, 0))

    # --- corner cantoneiras: reuse V1 mid cantoneira, shrink 80 -> 76 ---
    src = []
    for n in ('72_suporte_central_D_chanfro:1', '74_capa_central_D_interior_continuo:1'):
        o = root.occurrences.itemByName(n)
        for b in o.bRepBodies:
            src.append((n, b))
    for n, b in src:
        base = stretch_remove(b, 310.0, 314.0, 0.0, -4.0)
        mv(base, dy=(Y0 - 286.0))
        for (fx, fz, tag) in ((1, 1, 'FD'), (-1, 1, 'FE'), (1, -1, 'TD'), (-1, -1, 'TE')):
            c = tbm.copy(base)
            if fx < 0: mirx(c)
            if fz < 0: mirz(c)
            items.append((c, BLK, 'V2_Riser_Cantoneira_%s_%s' % (tag, 'Suporte' if '72_' in n else 'Capa'), None, 0))
    for (fx, fz) in ((1, 1), (-1, 1)):
        for yy in (Y0 + 12, Y1 - 12):
            items.append((screw(fx * 276, yy, 307 * fz, axis='z', r=2.6, h=1.6), HW or BLK, 'V2_Riser_M3_Cantoneira', None, 0))

    # --- front green panel (left) with engraved outline ---
    gp = box(-224, 36, 563, 629, 297, 300.5)
    ring = box(-214, 26, 571, 621, 299.7, 301)
    tbm.booleanOperation(ring, box(-212.6, 24.6, 572.4, 619.6, 299, 302), DIF)
    tbm.booleanOperation(gp, ring, DIF)
    items.append((gp, GRN, 'V2_Riser_Painel_Verde_Esquerdo', 'z', 1.2))
    for (xx, yy) in ((-218, 569), (-218, 623), (30, 569), (30, 623)):
        items.append((screw(xx, yy, 300.5, r=2.2, h=1.4), HW or BLK, 'V2_Riser_M3_Painel', None, 0))

    # --- right green plate + display module ---
    rp = box(46, 226, 563, 629, 297, 300.5)
    items.append((rp, GRN, 'V2_Riser_Painel_Verde_Display', 'z', 1.2))
    hous = box(64, 216, 560, 632, 300.5, 312)
    tbm.booleanOperation(hous, box(72, 208, 566, 626, 310.8, 313), DIF)
    items.append((hous, BLK, 'V2_Display_Moldura_Black', 'z', 2.0))
    scr = box(72.4, 207.6, 566.4, 625.6, 310, 311.4)
    items.append((scr, SCR, 'V2_Display_Tela_5pol', None, 0))
    for (xx, yy) in ((52, 569), (52, 623), (220, 569), (220, 623)):
        items.append((screw(xx, yy, 300.5, r=2.2, h=1.4), HW or BLK, 'V2_Riser_M3_Painel', None, 0))

    # --- build ---
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = 'SV08_V2_Riser_Display_Persianas'
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    made = []
    try:
        for t, ap, nm, cd, cm in items:
            nb = comp.bRepBodies.add(t, bf)
            made.append((nb, ap, nm, cd, cm))
    finally:
        bf.finishEdit()
    bodies = comp.bRepBodies
    errs = []
    for i, (nb0, ap, nm, cd, cm) in enumerate(made):
        nb = bodies.item(i)
        try:
            nb.name = nm
        except Exception:
            pass
        try:
            if ap: nb.appearance = ap
        except Exception as e:
            errs.append(str(e)[:80])
    # chamfers on outward faces
    ch = comp.features.chamferFeatures
    nch = 0
    for i, (nb0, ap, nm, cd, cm) in enumerate(made):
        if not cd or cm <= 0:
            continue
        nb = bodies.item(i)
        dvec = {'z': (0, 0, 1), '-z': (0, 0, -1), 'x': (1, 0, 0), '-x': (-1, 0, 0)}[cd]
        best, bestv = None, -1e9
        for f in nb.faces:
            ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
            if not ok: continue
            dot = n.x*dvec[0] + n.y*dvec[1] + n.z*dvec[2]
            if dot > 0.99:
                c = f.pointOnFace
                v = c.x*dvec[0] + c.y*dvec[1] + c.z*dvec[2]
                if v > bestv:
                    best, bestv = f, v
        if best is None:
            continue
        edges = adsk.core.ObjectCollection.create()
        for e in best.edges:
            edges.add(e)
        try:
            inp = ch.createInput2()
            inp.chamferEdgeSets.addEqualDistanceChamferEdgeSet(edges, adsk.core.ValueInput.createByReal(cm / 10.0), False)
            ch.add(inp)
            nch += 1
        except Exception as e:
            errs.append(nm + ':' + str(e)[:60])
    print(json.dumps({'bodies': bodies.count, 'chamfers': nch, 'errs': errs[:8]}))
