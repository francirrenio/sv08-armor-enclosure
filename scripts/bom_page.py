import json,pickle,collections,html
R=json.load(open('bom_parts.json'))
rows=pickle.load(open('bom_rows.pkl','rb'))
esc=html.escape
# ---------- ferragens ----------
HKN={'abaulada (ISO 7380)':'cabeça abaulada (ISO 7380)','cilindrica (DIN 912)':'cabeça cilíndrica Allen (DIN 912)','escareada (DIN 7991)':'escareado (DIN 7991)','cilindrica':'cabeça cilíndrica'}
scr=collections.Counter(); notes={}
nutM3=0; tnut=0; ins=0; pins=0
for r in rows:
    if r['k']=='parafuso':
        pid=r['pid'].replace('_E','')
        M,nom,hk,ext=r['M'],r['nom'],HKN.get(r['hk'],r['hk']),r['ext']
        if pid in ('tnF','tnL','tnT') and M=='M5': nom=10                      # rotulo do projeto: M5x10 + porca T
        if pid=='hwRiser': M,nom,hk,ext='M3',8,HKN['escareada (DIN 7991)'],True      # rotulo do projeto: 8x M3x8 escareado
        if pid=='tbHW' and M=='M2': M,nom,hk='M3',14,'conforme a tomada'; notes[('EXT',M,nom,hk)]='fixação da tomada AS03 (confira o furo da sua tomada)'
        if pid=='exHW' and M=='M2': notes[('INT',M,nom,hk)]='fixação do servo SG90 (já vêm com o servo)'
        if r['nut']=='porca M3': nutM3+=1
        if r['nut']=='porca T 2020 M5': tnut+=1
        scr[('EXT' if ext else 'INT',M,nom,hk)]+=1
    elif r['k']=='porca M3': nutM3+=1
    elif r['k']=='inserto M3': ins+=1
    elif r['k']=='pino 3x3': pins+=1
def scr_table(kind):
    items=sorted([(k,v) for k,v in scr.items() if k[0]==kind],key=lambda kv:(kv[0][1],kv[0][2],kv[0][3]))
    out=[]; tot=0
    for (e,M,nom,hk),v in items:
        tot+=v; n=notes.get((e,M,nom,hk),'')
        out.append(f'<tr><td class="ck"><input type="checkbox" id="s-{e}-{M}-{nom}-{abs(hash(hk))%999}"></td><td class="mono">{M} x {nom}</td><td>{esc(hk)}</td><td class="num">{v}</td><td class="note">{esc(n)}</td></tr>')
    return '\n'.join(out),tot
ext_rows,ext_tot=scr_table('EXT'); int_rows,int_tot=scr_table('INT')
# ---------- pecas ----------
EXCL={'tbAS03','dsF','fita','exSopr','exServo','tcAcr','pfAcr','acr1','u_acr1','u_tcAcr','u_pfAcr'}
def region(r):
    i=r['id']; l=r['label']
    if i.startswith('u_'): return 'Extensão de cima'
    if i in ('mold1','mold2','pux','reguaPortaA','reguaPortaB','placaTopo','dobr','dobrG','bat1'): return 'Portas de baixo'
    if i.startswith(('ex','al')) or i in ('riser47','tcRiser','molAl47','tcMolAl','bandaB','tcBanda','apB','tcApoio'): return 'Top hat: laterais (riser, aletas e exaustor)'
    if i.startswith(('tf','tr','sup','thCant','thSup','thTr')) or i in ('tcCant','tcSup'): return 'Top hat: frente, fundo e cantos'
    if i in ('acI','acS','tcMolI','tcMolS','pfMolI','pfMolS','fechos','pfFch'): return 'Painéis laterais e do fundo'
    if i.startswith(('esp','tcE','tcV','tcF','v72','vsup','capa','tcCapa','fb')): return 'Colunas'
    return 'Base (frente, laterais e traseira)'
def color(l):
    s=l.lower()
    if 'verde' in s: return 'verde'
    if 'branca' in s or 'branco' in s: return 'branco'
    return 'preto'
def clean(l):
    for p in ('Extensao de cima - ',): l=l.replace(p,'')
    return l
ORDER=['Base (frente, laterais e traseira)','Colunas','Painéis laterais e do fundo','Portas de baixo','Top hat: frente, fundo e cantos','Top hat: laterais (riser, aletas e exaustor)','Extensão de cima']
grp=collections.defaultdict(list); total_pcs=0; over=[]
for r in R:
    if r['id'] in EXCL: continue
    n=max(r['n'],1); q=n*(2 if r['E'] else 1); total_pcs+=q
    big=max((s[0] for s in r['sizes']),default=0)
    if big>300: over.append((clean(r['label']),big))
    grp[region(r)].append((r,n,q,big))
part_html=[]
for g in ORDER:
    lst=grp.get(g,[])
    if not lst: continue
    sub=sum(q for _,_,q,_ in lst)
    trs=[]
    for r,n,q,big in lst:
        c=color(r['label'])
        qs=f'{q}' + (f' <span class="dim">({n} + {n} espelhada)</span>' if r['E'] else '')
        flag=' <span class="warn">passa de 300 mm</span>' if big>300 else ''
        trs.append(f'<tr><td class="ck"><input type="checkbox" id="p-{r["id"]}"></td><td>{esc(clean(r["label"]))}</td><td><span class="sw sw-{c}"></span>{c}</td><td class="num">{qs}</td><td class="num mono">{big} mm{flag}</td></tr>')
    part_html.append(f'<section class="grp"><h3>{esc(g)} <span class="dim">· {sub} peças</span></h3><div class="tw"><table><thead><tr><th></th><th>Peça</th><th>Cor</th><th class="num">Qtd</th><th class="num">Maior medida</th></tr></thead><tbody>{"".join(trs)}</tbody></table></div></section>')
# ---------- acrilicos ----------
ACR=[('Painel lateral de baixo','452 x 440',2),('Painel lateral de cima (extensão)','440 x 326',2),('Fundo de baixo','470,4 x 448,1',1),('Fundo de cima (extensão)','470 x 326',1),('Porta de baixo','448,5 x 233',2),('Porta de cima (extensão)','326,4 x 233',2)]
acr_rows=''.join(f'<tr><td class="ck"><input type="checkbox" id="a-{i}"></td><td>{esc(a)}</td><td class="num mono">{s} mm</td><td class="num">{q}</td></tr>' for i,(a,s,q) in enumerate(ACR))
# ---------- comprados ----------
BUY=[('Soprador (blower) 4020 12 V','8','4 por lateral, 2 em cada janela de aletas'),('Servo SG90','2','1 por lateral, no centro entre as janelas'),('Fita LED ARGB 12 mm','~290 mm','3 trechos em série: 184 + 52 + 52 mm, atrás da logo da frente'),('Tomada AS03 (C14 com fusível e chave)','1','na traseira de baixo'),('Perfil de alumínio 2020 (estrutura do DragonSlider)','12 barras','4 de 520 mm, 4 de 490 mm, 4 de 298 mm'),('Espuma de vedação 1,5 mm','2 x 222 mm','na placa do rebaixo da travessa de cima, onde o acrílico das portas de baixo apoia')]
buy_rows=''.join(f'<tr><td class="ck"><input type="checkbox" id="b-{i}"></td><td>{esc(a)}</td><td class="num">{esc(q)}</td><td class="note">{esc(n)}</td></tr>' for i,(a,q,n) in enumerate(BUY))
# ---------- outras ferragens ----------
oth=[('Porca sextavada M3','DIN 934',nutM3,''),('Porca T 2020 M5 (deslizante ou martelo)','para perfil 2020',tnut,'uma para cada parafuso M5'),('Inserto roscado de latão M3 x 4 mm','para aplicar a quente',ins,'molduras das portas, cantoneiras e topo'),('Pino quadrado 3 x 3 x 16 mm','impresso ou cortado',pins,'emendas da banda do topo e do riser')]
oth_rows=''.join(f'<tr><td class="ck"><input type="checkbox" id="o-{i}"></td><td>{esc(a)}</td><td>{esc(b)}</td><td class="num">{q}</td><td class="note">{esc(n)}</td></tr>' for i,(a,b,q,n) in enumerate(oth))
data=dict(ext_rows=ext_rows,int_rows=int_rows,ext_tot=ext_tot,int_tot=int_tot,part_html='\n'.join(part_html),total_pcs=total_pcs,acr_rows=acr_rows,buy_rows=buy_rows,oth_rows=oth_rows,over=over)
pickle.dump(data,open('bom_page_data.pkl','wb'))
print(ext_tot,int_tot,total_pcs,nutM3,tnut,ins,pins,over)
