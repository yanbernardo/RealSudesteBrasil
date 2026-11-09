"""Quadras de vôlei na areia da praia (pedido do usuário, 08/11/2026).

O tipo "quadra esportiva" do KnoxMap só pinta grama (estranho na areia). Aqui a
areia fica e a rede do jogo base (recreational_sports_01) é posta na linha do
meio de cada quadra, por cores no desenho de detalhes e regras no Rules.txt das
ferramentas de mapa (rótulo "RSB praia"; as regras desta marca são regravadas a
cada execução).

As quadras vêm do gerador (`quadrasPraia` no config, em pixels do desenho):
"W" = rede na borda oeste dos quadrados da coluna x, de y0 a y1;
"N" = rede na borda norte dos quadrados da linha y, de x0 a x1.

Chamado pelo `knoxmap_pipeline.py` quando o config tem `"quadrasPraia"`.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from PIL import Image

# Rede com poste nas duas pontas, conferida na folha (a 1ª versão apontava para
# placares, peças 97 e 100). Borda oeste (a linha sobe para a direita na tela):
# 93 = ponta norte, 92 = meio, 91 = ponta sul. Borda norte (desce para a direita):
# 88 = ponta oeste, 89 = meio, 90 = ponta leste.
PECAS = {("W", "ini"): ((12, 41, 200), "recreational_sports_01_93"),
         ("W", "meio"): ((12, 41, 201), "recreational_sports_01_92"),
         ("W", "fim"): ((12, 41, 202), "recreational_sports_01_91"),
         ("N", "ini"): ((12, 41, 203), "recreational_sports_01_88"),
         ("N", "meio"): ((12, 41, 204), "recreational_sports_01_89"),
         ("N", "fim"): ((12, 41, 205), "recreational_sports_01_90")}
MARCA = "RSB praia"
# Linha branca de tinta nova (a "desbotada" do KnoxMap saía tracejada e fraca na areia):
# folha street_trafficlines_01, peças 8, 10, 12 e 14 = bordas oeste, norte, leste e sul.
LINHAS = {"W": ((12, 41, 206), "street_trafficlines_01_8"), "N": ((12, 41, 207), "street_trafficlines_01_10"),
          "E": ((12, 41, 208), "street_trafficlines_01_12"), "S": ((12, 41, 209), "street_trafficlines_01_14")}
LINHA_W, LINHA_N, LINHA_E, LINHA_S = (LINHAS[k][0] for k in "WNES")


def garantir_regras(knox: Path) -> int:
    import sys
    sys.path.insert(0, str(knox))
    import knoxpaths
    caminho = Path(knoxpaths.mapping_tools_dir()) / "config" / "Rules.txt"
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    texto = re.sub(r"\n?rule\s*\{\s*label = " + MARCA + r" [^\n]*\n.*?\}\s*", "\n", texto, flags=re.S)
    novas = []
    for (lado, parte), (cor, peca) in PECAS.items():
        novas.append(f"\nrule\n{{\n    label = {MARCA} rede {lado} {parte}\n    bitmap = 1\n"
                     f"    color = {cor[0]} {cor[1]} {cor[2]}\n"
                     f"    tiles = {peca}\n    layer = 0_Furniture\n}}\n")
    for lado, (cor, peca) in LINHAS.items():
        novas.append(f"\nrule\n{{\n    label = {MARCA} linha {lado}\n    bitmap = 1\n"
                     f"    color = {cor[0]} {cor[1]} {cor[2]}\n"
                     f"    tiles = {peca}\n    layer = 0_FloorOverlay5\n}}\n")
    caminho.write_text(texto.rstrip() + "\n" + "".join(novas), encoding="utf-8")
    return len(novas)


def colocar(knox: Path, nome: str, cfg: dict) -> dict:
    out = knox / "output" / nome
    quadras = cfg.get("quadrasPraia") or []
    for p in (out / f"{nome}_veg.bmp", out / f"{nome}_veg_base.bmp"):
        if not p.exists():
            continue
        img = np.array(Image.open(p).convert("RGB"))
        H, W = img.shape[:2]
        # contorno: linhas brancas de borda do jogo (as mesmas regras "Edge line" do KnoxMap)
        for q in quadras:
            x0, y0, x1, y1 = q["rx0"], q["ry0"], q["rx1"], q["ry1"]
            for y in range(y0, y1 + 1):
                if 0 <= y < H:
                    if 0 <= x0 < W:
                        img[y, x0] = LINHA_W
                    if 0 <= x1 < W:
                        img[y, x1] = LINHA_E
            for x in range(x0 + 1, x1):
                if 0 <= x < W:
                    if 0 <= y0 < H:
                        img[y0, x] = LINHA_N
                    if 0 <= y1 < H:
                        img[y1, x] = LINHA_S
        for q in quadras:
            if q["tipo"] == "W":
                pts = [(q["x"], y) for y in range(q["y0"], q["y1"] + 1)]
            else:
                pts = [(x, q["y"]) for x in range(q["x0"], q["x1"] + 1)]
            for k, (x, y) in enumerate(pts):
                parte = "ini" if k == 0 else ("fim" if k == len(pts) - 1 else "meio")
                if 0 <= x < W and 0 <= y < H:
                    img[y, x] = PECAS[(q["tipo"], parte)][0]
        Image.fromarray(img, "RGB").save(p, format="BMP")
    return {"quadras": len(quadras), "regras": garantir_regras(knox)}
