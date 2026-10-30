# Coluna da carenagem SV08 — refazer como "espinha" única por face (abordagem A)

Data: 2026-10-23 · Projeto: carenagem SV08 (Fusion, arquivo `SV08_Carenagem`, design direto, sem linha do tempo) · Piloto: coluna FD (frente-direita). Depois replicar em FE, TD, TE.

## Por que

As peças pretas das colunas acumularam dezenas de correções locais (recortes, degraus, rebaixos, sobras de furos de pinos antigos). Ficaram feias, frágeis e difíceis de imprimir e de corrigir. O dono quer recomeçar as peças estruturais do zero com uma regra simples:

- cada peça é um corpo único, sem remendos, sem recortes que não tenham função;
- faces planas e contínuas; onde uma peça apoia em outra, as duas faces são planas ("sempre uma em cima da outra");
- cantos retos e chanfros contínuos (chanfro 45° nas arestas visíveis), preservando só os contornos com função;
- encaixes entre peças sempre em rabo de andorinha;
- peças inteiras de baixo até em cima; o corte para caber na impressora (máx. 300 mm) vem depois, num passo separado.

As referências de estilo são as peças que o próprio dono limpou à mão: `69_coluna_chapa_frontal_restaurada_D` (placa reta, só furos) e `72_verde_inferior_D_encaixe` / `75_verde_superior_D` (casca em L de 4,0 mm, lisa por dentro, chanfros por fora).

## Como é hoje (coluna FD, coordenadas do mundo em mm; Y para cima, X para fora da lateral, Z para fora da frente)

- Perfil de alumínio da impressora (`Corpo1`, ESTRUTURA_ORIGINAL): X 226,5–268,5 · Z 225,5–273,5 · Y 0–552. É a referência estrutural; nada pode avançar para dentro da face interna do perfil (gantry flutuante passa rente).
- Suportes presos no perfil: `65_suporte_P01_D` (Y 4–136), `72_suporte_central_D_chanfro` (Y 296–356, com o parafuso original da impressora `44_M3_fixacao_original_central` em Y≈322), `SV08_TopHat_Suporte_Canto_FD_Black` (Y 554–623).
- Lateral (face X≈283,8): `58_coluna_inferior_lateral_frontal_D_interna` (X 265–277,8, Y 81–296), `..._superior_..._interna` (X 265–278,6, Y 356–558), `..._inferior_..._externa` e `..._superior_..._externa` (X 276,4–283,8, Y 93–558). Parafusos `46_M3x10_lateral_110/126` com porca na interna.
- Frente (face Z≈286): `69_coluna_chapa_frontal_restaurada_D` (já limpa pelo dono, X 235,4–264, Y 81–306) e `75_coluna_superior_frontal_D` (Y 346–558).
- Verdes (já limpas pelo dono): casca em L, perna lateral X 279,8–283,8, perna frontal Z 282,0–286,0; `72_...` Y 94,2–326 e `75_verde_superior_D` Y 326–551. Presas por M3x8 ISO7380 da tampa (frente Y 126/266/384/494; lado Y 266/384/494).
- Por cima: capa central `74_capa_central_D_interior_continuo` (Y 298–354), cantoneira de baixo `54_cantoneira_base_D` (Y 2–98,7, já alterada pelo dono para ser reta por dentro e por fora) e cantoneira do top hat (Y 523–634).
- Fechos laterais `SV-40-05 fecho D frente Y190/Y430` (corpo e M3x16 + porca entram na peça preta da lateral). Moldura lateral `SV-40-01*` (borda X 274–284, Z ≤ 219,2) e porta da frente `SV-30-01*` (X ≤ 234,5).

## Objetivo (o que será construído)

Para cada coluna, duas peças pretas inteiras ("espinhas"), uma por face, e uma verde inteira:

1. **Espinha lateral** — substitui interna + externa (inferior e superior), de Y 93 (topo da base/chassis) até Y 554 (base do suporte de canto do top hat). Presa no perfil pelos três suportes e pelos M3 laterais. Face de fora plana em X 279,6 (assento da verde, 0,2 de folga); faixa entre a moldura e a verde rente à face (X 283,8) com o padrão já aprovado (borda a 0,75 da verde, chanfro 45°×1,25 oposto ao da verde; lado da moldura parede a 0,9 + chanfro 1,4); recortes dos fechos com o padrão aprovado (entradas a 45°, assento 0,2).
2. **Espinha frontal** — substitui 69 + 75_coluna_superior_frontal, de Y 81 até Y 554, placa reta como a 69 do dono; face de fora plana em Z 281,8 sob a verde e faixa rente (Z 286) entre a porta e a verde com o mesmo padrão de chanfros.
3. **Verde em L única** — junta 72 + 75_verde_superior_D (Y 94,2–522,6), no estilo das peças limpas pelo dono (casca 4,0, vinco reto X 268,34–269,52 × 0,5 na frente, chanfros externos).
4. **Fixação da verde nas espinhas:** trilho em rabo de andorinha vertical na lateral (a verde desce por cima) + os M3x8 da tampa existentes (furo piloto 2,5 na espinha).
5. **União das duas espinhas no canto:** rabo de andorinha vertical (espinha frontal entra na lateral) — sem cola.
6. **Suporte central** (`72_suporte_central_D_chanfro`) refeito como peça única, presa ao perfil pelo parafuso original de Y 322, prendendo as duas espinhas à meia altura; a capa central cobre.

Fora do escopo agora: o corte das peças para impressão (passo seguinte), as cantoneiras (já ficam como o dono deixou, retas; apoiam nas faces planas das espinhas e são presas pelos parafusos existentes), o top hat.

## Restrições

- Nada avança para dentro da face interna do perfil de alumínio (gantry).
- Folgas: 0,2 mm entre peças que se encostam/encaixam; rabo de andorinha com 0,15–0,25 de folga lateral.
- Impressão sem suportes: cada peça com uma face grande plana para a mesa; ângulos de rabo de andorinha e chanfros a 45° ou menos de balanço.
- Corpo único (1 lump), sem remendos; construída a partir de um contorno limpo, não por correções sobre a peça antiga.
- Parafusos e porcas existentes permanecem; só os alojamentos necessários (furo piloto 2,5 para autoatarraxante; folga 3,4 + sextavado onde há porca).

## Abordagens consideradas

- **A (escolhida):** uma espinha por face, juntando interna e externa. Menos peças, mais rígida, cada peça presa direto nos suportes. Custo: o canal de cabos fica só no vão entre espinha e perfil.
- **B:** interna e externa inteiras e separadas, unidas por rabo de andorinha. Mantém o canal de cabos maior; mais peças e encaixes.
- **C:** só limpar as peças atuais mantendo inferior/superior — descartada, contraria "peças inteiras".

## Decidido pelo dono

Abordagem A; peças únicas sem remendos; faces planas onde há apoio; encaixes em rabo de andorinha; cantoneiras retas por dentro e por fora (são as outras peças que se adaptam a elas); estilo das peças 69, 72 e 75 limpas por ele; piloto na FD.

## Decisões minhas (o dono pode corrigir)

- Espinha lateral = placa plana dos dois lados, X 273,0–279,6 (6,6 mm), Z 220,1 (lado da moldura) a 275,8 (canto); fica fora do perfil (X ≤ 268,5) e do suporte de baixo (X ≤ 272,8); o vão de 4,5 mm entre perfil e placa é o canal de cabos. Presa por parafusos que atravessam a placa até os três suportes (furos com função, não recortes).
- Espinha frontal = placa plana Z 276,0–281,8 sob a verde (faixa até Z 286 entre porta e verde), X 235,4 até o canto.
- O parafuso original da impressora (Y≈322) atravessa a espinha lateral por um furo simples.
- Parafusos da verde: mantidos onde estão agora; deixá-los simétricos fica para o passo de corte para impressão (cada trecho precisa dos seus).
- Capa central mantida como acabamento: apoia na verde (que já é plana ali) com folga 0,2 e é presa na espinha pelos parafusos atuais da capa; cobre a cabeça do parafuso original da impressora (Y≈322) e, no passo de corte para impressão, as emendas da verde e das espinhas ficam escondidas debaixo dela (a verde passa de 300 mm e vai precisar de uma emenda).
- Desenho feito de forma espelhável para FE/TD/TE (faixa e recortes de fecho parametrizados por lado).
- Trilho andorinha: macho na espinha, fêmea na verde, 6 mm de largura na base, 60° , 2 mm de altura, ao longo de toda a altura da verde.
- O vão entre espinha e perfil continua livre para cabos.

## Deixado para quem constrói

Posição exata dos rabos de andorinha no canto; forma do novo suporte central dentro do envelope atual; ordem de montagem; verificação de colisões com a auditoria existente.
