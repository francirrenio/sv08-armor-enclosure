import adsk.core, adsk.fusion, json, traceback

DZ = -11.5  # mm: front stack moves toward the printer (V1 front 297.5 -> 286)

INCLUDE = ['54_cantoneira_base_D', '69_coluna_chapa_frontal_restaurada_D', '72_verde_inferior_D_encaixe',
           '71_dobradica_fixa_base_continua', '68_dobradica_movel_CAD', '70_eixo_M3x40', '70_porca_eixo',
           '62_M3x16_base_', '72_suporte_central_D_chanfro', '74_capa_central_D_interior_continuo',
           '44_M3_capa_frente', '44_M3_capa_lado', 'M3_cantoneira_1_',
           '75_verde_superior_D', '75_coluna_superior_frontal_D', '75_dobradica_fixa_base_continua_superior_D',
           '75_dobradica_movel_CAD_superior_D', '75_eixo_M3x40_superior_D', '75_M3x16_base_', '75_porca_eixo_superior_D',
           '59_PORTA_02_montante_externa_inferior_D', '59_PORTA_02_montante_externa_superior_D',
           'PORTA_04_uniao_inferior_externa_D', 'PORTA_04_uniao_superior_externa_D', 'PORTA_03_emenda_externa_D',
           '75_acrilico_D', 'V2_Riser_Cantoneira_FD_Capa', 'V2_Riser_Cantoneira_FD_Suporte',
           'V2_Riser_Enchimento_Canto_Blac', 'V2_Riser_M3_Cantoneira',
           '58_coluna_inferior_lateral_frontal_D_externa', '58_coluna_superior_lateral_frontal_D_externa', 'Moldura_Lateral_D_Inf_Frente_Black', 'Moldura_Lateral_D_Sup_Frente_Black']
FIXED = ['1.20.2']  # frame stays
Z0, Z1 = 276.0, 287.5  # band removed (DZ = Z0 - Z1)


def run(context):
    log = []
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        tbm = adsk.fusion.TemporaryBRepManager.get()
        V3 = adsk.core.Vector3D.create
        for o in list(root.occurrences):
            if o.component.name == 'V2_ESTUDO_Canto_V1_Aproximado':
                o.deleteMe()

        def vis(o):
            while o:
                if not o.isLightBulbOn: return False
                o = o.assemblyContext
            return True

        picks = []  # (label, body, fixed)
        for o in root.allOccurrences:
            if not vis(o) or o.component.name.startswith('V2_E'): continue
            path = o.fullPathName
            for b in o.bRepBodies:
                if not b.isLightBulbOn: continue
                bb = b.boundingBox
                x0, y0, z0, x1, y1, z1 = [v * 10 for v in (bb.minPoint.x, bb.minPoint.y, bb.minPoint.z, bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z)]
                if y0 > 640 or x1 < 180 or z1 < 200: continue
                key = path + '/' + b.name
                if '1.20.2' in path and abs(x1 - 268.5) < 1 and abs(z1 - 273.5) < 1 and y1 > 500:
                    picks.append(('Perfil_impressora_ref', b, True)); continue
                hit = [p for p in INCLUDE if p in key]
                if not hit: continue
                if '75_acrilico_D' in key and x0 < 0: pass
                fixed = any(f in key for f in FIXED)
                label = o.name.split(':')[0][:60]
                if b.name.startswith('V2_'): label = b.name[:60]
                picks.append((label, b, fixed))
        log.append('picked %d' % len(picks))

        P3 = adsk.core.Point3D.create
        def half(z0, z1):
            ob = adsk.core.OrientedBoundingBox3D.create(P3(0, 50.0, (z0 + z1) / 20.0), V3(1, 0, 0), V3(0, 1, 0), 300.0, 140.0, (z1 - z0) / 10.0)
            return tbm.createBox(ob)
        mv = adsk.core.Matrix3D.create(); mv.translation = V3(0, 0, (Z0 - Z1) / 10.0)
        items = []
        for (label, b, fixed) in picks:
            t = tbm.copy(b)
            if not fixed:
                bb = b.boundingBox; zmin, zmax = bb.minPoint.z * 10, bb.maxPoint.z * 10
                lo = hi = None
                if zmin < Z0:
                    lo = tbm.copy(b); tbm.booleanOperation(lo, half(-2000, Z0), adsk.fusion.BooleanTypes.IntersectionBooleanType)
                if zmax > Z1:
                    hi = tbm.copy(b); tbm.booleanOperation(hi, half(Z1, 2000), adsk.fusion.BooleanTypes.IntersectionBooleanType)
                    tbm.transform(hi, mv)
                if lo is not None and hi is not None:
                    try:
                        tbm.booleanOperation(lo, hi, adsk.fusion.BooleanTypes.UnionBooleanType); t = lo
                    except Exception as ex:
                        log.append('union fail %s %s' % (label, str(ex)[:40])); t = lo
                elif hi is not None: t = hi
                elif lo is not None: t = lo
                else:
                    log.append('skip ' + label); continue
            items.append((label, t, b.appearance))

        m = adsk.core.Matrix3D.create(); m.translation = V3(100.0, 0, 0)
        occ = root.occurrences.addNewComponent(m)
        comp = occ.component
        comp.name = 'V2_ESTUDO_Canto_V1_Aproximado'
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        try:
            for (label, t, ap) in items:
                comp.bRepBodies.add(t, bf)
        finally:
            bf.finishEdit()
        for i, (label, t, ap) in enumerate(items):
            bb = comp.bRepBodies.item(i)
            bb.name = label
            if ap: bb.appearance = ap
        for o in root.occurrences:
            if o.component.name in ('V2_ESTUDO_Canto_Encaixe', 'V2_ESTUDO_Canto_Harmonico', 'V2_EXEMPLO_Encaixe_Verde_Preto'):
                o.isLightBulbOn = False
        v = app.activeViewport; cam = v.camera; cam.isSmoothTransition = False
        cam.target = adsk.core.Point3D.create(124.0, 31.8, 26.0); cam.eye = adsk.core.Point3D.create(196.0, 70.0, 205.0); cam.upVector = V3(0, 1, 0)
        v.camera = cam; v.refresh()
        log.append('ok %d bodies' % comp.bRepBodies.count)
        log.append(sorted(set(l for (l, t, a) in items)))
    except Exception:
        log.append(traceback.format_exc()[-600:])
    print(json.dumps(log))
