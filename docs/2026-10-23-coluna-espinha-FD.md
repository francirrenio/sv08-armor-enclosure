# Coluna FD em "espinhas" — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Substituir as peças pretas e verdes da coluna FD por 4 peças únicas e limpas (espinha lateral, espinha frontal, verde em L, suporte central), sem remendos, com encaixes em rabo de andorinha.

**Architecture:** Cada peça nova é construída do zero num script Fusion (TemporaryBRep: caixas + semiespaços + furos), num componente novo dentro de `COLUNA_FD`. As peças antigas ficam ocultas (não apagadas) até o dono conferir. Cada script tem modo DRY (exporta malha para prévia) e modo aplicar (cria o corpo e salva).

**Tech Stack:** Autodesk Fusion API (Python, design direto), scripts em `F:\SV08 Eclosure\docs\planos\carenagem\_scripts\`, prévias renderizadas com trimesh/pyvista na nuvem.

**Spec:** `F:\SV08 Eclosure\docs\planos\carenagem\DESIGN_coluna_espinha.md`

## Global Constraints

- Corpo único (1 lump) por peça; nada de correção sobre peça antiga — tudo nasce de contorno limpo.
- Folga 0,2 mm entre peças; rabo de andorinha com 0,2 de folga lateral; chanfros 45°.
- Nada avança para dentro do perfil `Corpo1` (X ≤ 268,5, Z ≤ 273,5 na região da coluna).
- Parafusos/porcas existentes permanecem; só furos/alojamentos com função (piloto Ø2,5 para M3 autoatarraxante; Ø3,4 de passagem; sextavado 5,7+0,4 para porca M3).
- Peças antigas: só ocultar. Apagar exige resumo + confirmação do dono.
- Nomes: `SV08_Espinha_Lateral_FD_Black`, `SV08_Espinha_Frontal_FD_Black`, `SV08_Verde_Coluna_FD_Green`, `SV08_Suporte_Central_FD_Black`, cada um no seu componente sob `COLUNA_FD`.
- Prévia (DRY + imagem) antes de aplicar cada peça.

## Review Focus

1. Parafusos que atravessam duas peças (M3x10 laterais Y110/126, parafuso original Y322, capa lado Y324, M3x16 dos fechos): furo alinhado em todas as peças do caminho.
2. Encontro das duas espinhas no canto (Z 275,8/276,0): sem sobreposição e com o rabo de andorinha montável de cima para baixo.
3. Verde x espinhas: assentos planos a 0,2; trilho andorinha não pode cruzar furo de parafuso.
4. Cantoneira de baixo (Y ≤ 98,7) e do top hat (Y ≥ 523): espinhas e verde não podem invadir.
5. Moldura lateral (Z ≤ 219,2) e porta (X ≤ 234,5): faixa rente com a mesma geometria já aprovada (D64–D66).

---

### Task 0: Segurança e limpeza
**Files:** Create `_scripts/V3_e00_backup.py`
- [ ] Exportar SMT de todos os corpos atuais de `COLUNA_FD` para `_stl/backup_v50_FD/` (rollback).
- [ ] Pedir ao dono para apagar `Corpo20/21/22` (componente `75_verde_superior_D`).
- Verificação: `index.json` com todos os corpos e volumes.

### Task 1: Espinha lateral
**Files:** Create `_scripts/V3_e01_espinha_lateral.py`
**Produces:** corpo `SV08_Espinha_Lateral_FD_Black`; constantes `XL0=273.0`, `XL1=279.6`, `ZL0=220.1`, `ZL1=275.8`, `Y0=93.0`, `Y1=554.0`.
- [ ] Placa X 273,0–279,6 · Z 220,1–275,8 · Y 93–554.
- [ ] Faixa rente até X 283,8 entre moldura e verde: regra D65 (parede da verde 234, recortes de fecho Y190/430, diagonais das pontas paradas em 225, chanfros 1,25 / 1,4).
- [ ] Furos: M3x10 laterais Y110/126 (Ø3,4 + rebaixo da cabeça até X 279,6), parafuso original Y322 (Ø3,4), capa lado Y324 (Ø3,4 + sextavado), M3x16 dos fechos (Ø3,4 + sextavado), tampa lado Y266/384/494 (piloto Ø2,5), dobradiça Y141/159/441/459 Z266 (piloto Ø2,5).
- [ ] Trilho andorinha macho (verde): Z 247,5–252,5, altura 2,0, base 4,0 / topo 5,0, Y 94,2–522,6.
- [ ] Rabo de andorinha do canto, macho na lateral: sai da borda Z 275,8 até Z 278,8, centrado em X 276,3, base 4 / topo 5, Y 93–554.
- Verificação: 1 lump; interferência 0 com perfil, suportes, P01, moldura, verde (após Task 3), fechos; prévia aprovada.

### Task 2: Espinha frontal
**Files:** Create `_scripts/V3_e02_espinha_frontal.py`
**Consumes:** constantes e trilho do canto da Task 1.
**Produces:** `SV08_Espinha_Frontal_FD_Black`; `ZF0=276.0`, `ZF1=281.8`, `XF0=235.4`, `XF1=279.6`.
- [ ] Placa Z 276,0–281,8 · X 235,4–279,6 · Y 81–554; faixa rente até Z 286 entre porta e verde (regra D66, ponta inferior parada em 240,3).
- [ ] Canaleta fêmea para o rabo de andorinha do canto (+0,2).
- [ ] Furos: tampa frente Y126/266/384/494 (piloto Ø2,5).
- [ ] Trilho andorinha macho (verde) em X 249–255.
- Verificação: idem Task 1.

### Task 3: Verde em L única
**Files:** Create `_scripts/V3_e03_verde_unica.py`
**Consumes:** posições dos trilhos (Tasks 1–2).
- [ ] União de `72_verde_inferior_D_encaixe` + `75_verde_superior_D` (já limpas pelo dono), cortada em Y 94,2–522,6, vinco reto X 268,34–269,52 × 0,5 contínuo.
- [ ] Canaletas fêmeas dos dois trilhos (+0,2); furos já existentes da verde mantidos.
- Verificação: 1 lump; folga 0,2 às espinhas; prévia.

### Task 4: Suporte central
**Files:** Create `_scripts/V3_e04_suporte_central.py`
- [ ] Bloco X 235,5–272,8 · Z 224–275,8 · Y 296,2–355,8 menos `Corpo1` (+0,2) — fica atrás das duas espinhas.
- [ ] Parafuso original Y322 passando (Ø3,4); pilotos Ø2,5 para 2 M3 novos vindos de cada espinha (Y 310 e 342).
- Verificação: 1 lump; zero interferência; prévia.

### Task 5: Trocar e conferir
**Files:** Create `_scripts/V3_e05_troca.py`
- [ ] Ocultar as peças antigas (interna/externa inf/sup, 69, 75_coluna_superior_frontal, 72_suporte_central, 72/75 verdes).
- [ ] Auditoria de colisões da coluna FD; render do conjunto; registrar E01–E05 no `DECISAO.md`.
- Verificação: auditoria sem pares novos; imagens enviadas ao dono.
