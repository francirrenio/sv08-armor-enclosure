import adsk.core, adsk.fusion, json, traceback, os

# Remove a 11.5 mm slab from the front (Z 276..287.5) and from the rear (Z -287.5..-276)
# of every visible enclosure body, moving what is outside the slab toward the printer.
# Originals are hidden (list saved for restore); copies go into one study component.
ZF0, ZF1 = 276.0, 287.5
HIDDEN_LOG = r'F:\SV08 Eclosure\docs\planos\carenagem\_scripts\v2_profundidade_ocultos.json'
COMP = 'V2_ESTUDO_Profundidade_Reduzida'
SKIP = ('Vedacao_Central_Portas_Feltro_REFERENCIA',)


def run(context):
    log = []
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        tbm = adsk.fusion.TemporaryBRepManager.get()
        P3 = adsk.core.Point3D.create; V3 = adsk.core.Vector3D.create

        # restore from a previous run
        if os.path.exists(HIDDEN_LOG):
            prev = json.load(open(HIDDEN_LOG, encoding='utf-8'))
            want = set(prev)
            for o in root.allOccurrences:
                for b in o.bRepBodies:
                    if (o.fullPathName + '|' + b.name) in want: b.isLightBulbOn = True
            for o in root.occurrences:
                if (o.fullPathName + '|OCC') in want: o.isLightBulbOn = True
        for o in list(root.occurrences):
            if o.component.name == COMP: o.deleteMe()

        def vis(o):
            while o:
                if not o.isLightBulbOn: return False
                o = o.assemblyContext
            return True

        picks = []
        for o in root.allOccurrences:
            if not vis(o): continue
            cn = o.component.name
            if cn.startswith('V2_E') and cn != 'V2_ESTUDO_Verde_Linha_Sombra_Colunas': continue
            path = o.fullPathName
            if any(s in path for s in SKIP): continue
            for b in o.bRepBodies:
                if not b.isLightBulbOn: continue
                bb = b.boundingBox
                z0, z1 = bb.minPoint.z * 10, bb.maxPoint.z * 10
                if z1 > ZF0 or z0 < -ZF0:
                    picks.append((path, b))
        log.append('picked %d' % len(picks))

        def slab(z0, z1):
            ob = adsk.core.OrientedBoundingBox3D.create(P3(0, 50.0, (z0 + z1) / 20.0), V3(1, 0, 0), V3(0, 1, 0), 300.0, 300.0, (z1 - z0) / 10.0)
            return tbm.createBox(ob)
        mf = adsk.core.Matrix3D.create(); mf.translation = V3(0, 0, -(ZF1 - ZF0) / 10.0)
        mr = adsk.core.Matrix3D.create(); mr.translation = V3(0, 0, (ZF1 - ZF0) / 10.0)
        I = adsk.fusion.BooleanTypes.IntersectionBooleanType
        U = adsk.fusion.BooleanTypes.UnionBooleanType
        items = []
        fails = 0
        for (path, b) in picks:
            bb = b.boundingBox
            z0, z1 = bb.minPoint.z * 10, bb.maxPoint.z * 10
            parts = []
            try:
                # middle (kept in place): -ZF0..ZF0
                if z0 < ZF0 and z1 > -ZF0:
                    t = tbm.copy(b); tbm.booleanOperation(t, slab(-ZF0, ZF0), I); parts.append(t)
                if z1 > ZF1:
                    t = tbm.copy(b); tbm.booleanOperation(t, slab(ZF1, 3000), I); tbm.transform(t, mf); parts.append(t)
                if z0 < -ZF1:
                    t = tbm.copy(b); tbm.booleanOperation(t, slab(-3000, -ZF1), I); tbm.transform(t, mr); parts.append(t)
                parts = [p for p in parts if p and p.faces.count > 0]
                if not parts: continue
                res = parts[0]
                for p in parts[1:]:
                    try:
                        tbm.booleanOperation(res, p, U)
                    except Exception:
                        items.append((path, b, p))
                items.append((path, b, res))
            except Exception as ex:
                fails += 1
        log.append('copies %d fails %d' % (len(items), fails))

        occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component; comp.name = COMP
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        try:
            for (path, b, t) in items: comp.bRepBodies.add(t, bf)
        finally:
            bf.finishEdit()
        for i, (path, b, t) in enumerate(items):
            nb_ = comp.bRepBodies.item(i)
            nm = path.split('+')[-1].split(':')[0]
            nb_.name = (b.name if b.name.startswith(('SV08_', 'V2_')) or nm.startswith('V2_ESTUDO') else nm)[:60]
            if b.appearance: nb_.appearance = b.appearance
        hidden = []
        for (path, b) in picks:
            b.isLightBulbOn = False
            hidden.append(path + '|' + b.name)
        for o in root.occurrences:
            if o.component.name == 'V2_ESTUDO_Verde_Linha_Sombra_Colunas':
                o.isLightBulbOn = False; hidden.append(o.fullPathName + '|OCC')
        json.dump(hidden, open(HIDDEN_LOG, 'w', encoding='utf-8'))
        if des.snapshots.hasPendingSnapshot: des.snapshots.add()
        v = app.activeViewport; cam = v.camera; cam.isSmoothTransition = False
        cam.target = P3(0, 45.0, 0); cam.eye = P3(130.0, 110.0, 190.0); cam.upVector = V3(0, 1, 0)
        v.camera = cam; v.refresh()
        log.append('ok %d bodies, hidden %d' % (comp.bRepBodies.count, len(hidden)))
    except Exception:
        log.append(traceback.format_exc()[-700:])
    print(json.dumps(log))
