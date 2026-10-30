import adsk.core, adsk.fusion, json, traceback, math

def run(context):
    log = []
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        if app.activeDocument.name != 'SV08_V2_conceito':
            print('wrong doc'); return
        root = des.rootComponent
        grp = [o for o in root.occurrences if o.component.name == '30_PORTAS_FRENTE'][0]
        ch = {o.component.name: o for o in grp.childOccurrences}
        bat = ch['SV-30-03 Batente portas']
        # proxies in root context
        bat_p = bat.createForAssemblyContext(grp) if bat.assemblyContext is None else bat
        try:
            bat_p.isGrounded = True; log.append('grounded')
        except Exception as ex:
            log.append('ground fail ' + str(ex)[:60])
        for side, s, key in (('SV-30-01 Porta direita', 1, '1'), ('SV-30-02 Porta esquerda', -1, '2')):
            occ = ch[side]
            occ_p = occ.createForAssemblyContext(grp) if occ.assemblyContext is None else occ
            kn = occ.component.bRepBodies.itemByName('SV-30-0%sd eixo dobradica 150' % key)
            cyl = [f for f in kn.faces if isinstance(f.geometry, adsk.core.Cylinder)][0]
            cyl_p = cyl.createForAssemblyContext(occ_p)
            jg = None
            for kp in (adsk.fusion.JointKeyPointTypes.CenterKeyPoint, adsk.fusion.JointKeyPointTypes.MiddleKeyPoint, adsk.fusion.JointKeyPointTypes.StartKeyPoint):
                try:
                    jg = adsk.fusion.JointGeometry.createByNonPlanarFace(cyl_p, kp); break
                except Exception as ex:
                    log.append('kp fail ' + str(ex)[:50])
            ji = root.asBuiltJoints.createInput(occ_p, bat_p, jg)
            ji.setAsRevoluteJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
            j = root.asBuiltJoints.add(ji)
            j.name = 'Junta ' + side
            m = j.jointMotion
            m.rotationValue = math.radians(60)
            zmax = occ_p.boundingBox.maxPoint.z * 10
            sign = 1 if zmax > 330 else -1
            m.rotationValue = 0
            lim = m.rotationLimits
            lim.isMinimumValueEnabled = True; lim.isMaximumValueEnabled = True
            if sign > 0:
                lim.minimumValue = 0.0; lim.maximumValue = math.radians(110)
            else:
                lim.minimumValue = math.radians(-110); lim.maximumValue = 0.0
            log.append('%s ok sign %d zmax60 %.0f' % (side, sign, zmax))
    except Exception:
        log.append(traceback.format_exc()[-800:])
    print(json.dumps(log))
