# Remonta lista_materiais.html a partir de bom_page_data.pkl (gerado por bom_page.py), trocando so as tabelas.
import pickle,re
d=pickle.load(open('bom_page_data.pkl','rb')); h=open('lista_materiais.html').read()
i=h.index('<section><h2>Peças impressas</h2>'); j=h.index('<section class="notes">')
k=h.index('</p>',i)+4
h=h[:k]+'\n'+d['part_html']+'\n</section>\n'+h[j:]
h=re.sub(r'(<div><b>)\d+(</b><span>Peças impressas)',lambda m:m.group(1)+str(d['total_pcs'])+m.group(2),h)
h=h.replace('A faixa batente do acrílico da coluna de trás, na extensão de cima, tem 328 mm e passa do limite de 300 mm.','A peça SV08_Ext_Coluna_TD_Batente_Acrilico_Preto (e a E) tem 328 mm e passa do limite de 300 mm.')
h=h.replace('<p class="lead">Cor conforme o projeto:','<p class="lead">O nome é o mesmo do visualizador e do arquivo STL; a quantidade conta o lado direito (D) e o esquerdo (E). Cor conforme o projeto:')
open('lista_materiais.html','w').write(h); print(len(h))
