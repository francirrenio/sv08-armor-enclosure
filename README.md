# SV08 Armor Enclosure

Carenagem termica (camara fechada para ABS/ASA) para a impressora 3D Sovol SV08: colunas, paineis de acrilico 3 mm,
portas duplas, top hat com exaustor de aletas e extensao de cima nos perfis 2020 do DragonSlider.

## Pastas

- `visualizador/visualizador_carenagem.html` - visualizador 3D da proposta (abre direto no navegador, sem internet para os modelos).
- `visualizador/lista_materiais.html` - lista de parafusos (externos e internos), porcas, insertos, acrilicos, pecas compradas e pecas impressas.
- `stl/` - um STL por peca final, em pastas por conjunto (`01_Base`, `02_Colunas`, `03_Paineis`, `04_Portas`, `05_TopHat`,
  `06_Extensao`). Os `_Acrilico_3mm` sao so referencia de corte. `stl/indice.json` liga cada arquivo a descricao da peca.
- `scripts/` - geracao das pecas em Python (trimesh + manifold3d) e montagem do visualizador.
- `docs/` - anotacoes de projeto.
- `dados/` (fora do git) - malhas de trabalho (.pkl), STEP/STL de referencia da impressora e renders. Fica so na pasta local.

## Nomes das pecas

Padrao `SV08_<Local>_<Peca>_<Posicao>`, igual no visualizador, na lista de materiais, nos STLs e no Fusion.
Exemplo: `SV08_Base_Placa_Frente_Lateral-E`.

- Local: `Base`, `Coluna`, `Painel`, `Porta`, `TopHat`, `Extensao`.
- Peca: palavras separadas por `_`; partes de uma peca dividida em `1de2`, `2de3`...
- Posicao: lugar e lado com hifen. `Canto-FD/FE/TD/TE` (frente/tras, direita/esquerda), `Lateral-D/E`, `Frente`, `Frente-D/E`,
  `Tras-D/E`, `Fundo-D/E`, `Porta-D/E`, `Centro`. Lado visto de frente; a peca do lado E e o espelho da do lado D.
- A cor nao vai no nome: esta na lista de materiais e em `stl/indice.json`. Tabela completa em `scripts/names.py`.

## Regerar

Os scripts usam o caminho absoluto da pasta de trabalho original (`/tmp/claude-0/.../scratchpad/pe`); para rodar de novo,
ajuste esse caminho para a copia em `dados/scratchpad/pe`. Ordem usual: os `build_*.py` / `portas_*.py` da parte mexida,
depois `export_web8.py` (gera parts.pkl), `make_page.py` (gera o visualizador) e `chk_ext.py` (interferencias).

Nada desta proposta foi aplicado ainda no Fusion 360.
