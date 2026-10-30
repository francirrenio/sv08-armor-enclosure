import adsk.core, adsk.fusion, json, traceback

GROUPS = ['00_REFERENCIA_SV08', '05_CONJUNTO_V2_APROXIMADO', '10_BASE', '20_COLUNAS', '30_PORTAS_FRENTE',
          '40_LATERAIS_E_FUNDO', '50_RISER', '60_EXTENSAO', '70_TAMPA', '80_DIVERSOS', '90_ESTUDOS', '99_V1_ORIGINAIS_OCULTAS']
ACTIVE = {
    'V2_ESTUDO_Profundidade_Reduzida': '05_CONJUNTO_V2_APROXIMADO',
    'V2_ESTUDO_Portas_Inferiores_Acrilico453': '30_PORTAS_FRENTE',
    'V2_ESTUDO_Base_Friso_LED_13mm_v4': '10_BASE',
    'SV08_V2_Extensao_Portas_Cantos': '60_EXTENSAO',
    'SV08_V2_Riser_Display_Persianas': '50_RISER',
    'SV08_V2_Tampa_Acrilicos': '40_LATERAIS_E_FUNDO',
}
PREFIX = [
    ('ESTRUTURA_ORIGINAL', '00_REFERENCIA_SV08'),
    ('SV08_Ext_', '60_EXTENSAO'), ('77_EXTENSAO', '60_EXTENSAO'),
    ('77_TOPO', '50_RISER'), ('SV08_Banda_Topo', '50_RISER'), ('37_', '50_RISER'), ('40_', '50_RISER'),
    ('39_aro_tampa', '70_TAMPA'), ('39_TAMPA', '70_TAMPA'), ('39_', '50_RISER'),
    ('SV08_Moldura_', '40_LATERAIS_E_FUNDO'), ('42_', '40_LATERAIS_E_FUNDO'),
    ('59_', '30_PORTAS_FRENTE'), ('PORTA_', '30_PORTAS_FRENTE'), ('62_', '30_PORTAS_FRENTE'), ('68_', '30_PORTAS_FRENTE'),
    ('70_', '30_PORTAS_FRENTE'), ('71_', '30_PORTAS_FRENTE'), ('75_ENCAIXES', '30_PORTAS_FRENTE'),
    ('SV08_Vedacao_Central', '30_PORTAS_FRENTE'), ('41_verde_superior', '30_PORTAS_FRENTE'),
    ('44_', '20_COLUNAS'), ('46_', '20_COLUNAS'), ('47_', '20_COLUNAS'), ('49_', '20_COLUNAS'), ('51_', '20_COLUNAS'),
    ('55_', '20_COLUNAS'), ('57_', '20_COLUNAS'), ('58_', '20_COLUNAS'), ('69_', '20_COLUNAS'), ('72_', '20_COLUNAS'),
    ('74_', '20_COLUNAS'), ('75_', '20_COLUNAS'), ('M3_travessa', '20_COLUNAS'), ('M3_acabamento', '20_COLUNAS'),
    ('M25_tampa', '20_COLUNAS'), ('54_', '20_COLUNAS'), ('12_cantoneira', '20_COLUNAS'), ('M3_cantoneira', '20_COLUNAS'),
    ('02_', '10_BASE'), ('03_', '10_BASE'), ('07_', '10_BASE'), ('10_', '10_BASE'), ('11_', '10_BASE'), ('20_', '10_BASE'),
    ('21_', '10_BASE'), ('22_', '10_BASE'), ('41_', '10_BASE'), ('LED_', '10_BASE'), ('M25_02', '10_BASE'), ('M25_03', '10_BASE'),
    ('M25_22', '10_BASE'), ('M3_lateral_apoio', '10_BASE'), ('64_', '10_BASE'), ('65_', '10_BASE'), ('66_', '10_BASE'), ('67_', '10_BASE'),
]


def run(context):
    log = []
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        if app.activeDocument.name != 'SV08_V2_conceito':
            print('wrong doc'); return
        root = des.rootComponent
        grp = {}
        for o in root.occurrences:
            if o.component.name in GROUPS: grp[o.component.name] = o
        for g in GROUPS:
            if g not in grp:
                oc = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
                oc.component.name = g
                grp[g] = oc

        def any_visible_body(o):
            for b in o.component.bRepBodies:
                if b.isLightBulbOn: return True
            for c in o.childOccurrences:
                if c.isLightBulbOn and any_visible_body(c): return True
            return False

        plan = []
        for o in list(root.occurrences):
            cn = o.component.name
            if cn in GROUPS: continue
            name = o.name
            if cn in ACTIVE:
                g = ACTIVE[cn]
            elif cn.startswith('V2_ESTUDO') or cn.startswith('V2_EXEMPLO'):
                g = '90_ESTUDOS'
            elif not o.isLightBulbOn or not any_visible_body(o):
                g = '99_V1_ORIGINAIS_OCULTAS'
            else:
                g = '80_DIVERSOS'
                for p, gg in PREFIX:
                    if name.startswith(p):
                        g = gg; break
            plan.append((o, g))
        counts = {}
        fails = []
        for o, g in plan:
            try:
                o.moveToComponent(grp[g])
                counts[g] = counts.get(g, 0) + 1
            except Exception as ex:
                fails.append([o.name[:40], str(ex)[:60]])
        for g in ('90_ESTUDOS', '99_V1_ORIGINAIS_OCULTAS'):
            grp[g].isLightBulbOn = False
        log.append(counts)
        log.append({'fails': fails[:20], 'nfail': len(fails)})
        log.append('root now %d' % root.occurrences.count)
    except Exception:
        log.append(traceback.format_exc()[-700:])
    print(json.dumps(log))
