"""Ruas diagonais sem calçada em degraus (K15/U20).

O KnoxMap desenha calçada (concreto claro, `PALE_CONCRETE`, peças
blends_street_01_96-103) em volta de toda rua. Numa rua diagonal ela sai em
escada, com quadradinhos de grama, e o meio-fio reto vira degrau (usuário, em
jogo, Rua Santa Clara, 08/11/2026). No jogo original (Muldraugh), os trechos
diagonais e curvos NÃO têm calçada: o asfalto encosta na grama e o próprio
WorldEd faz a borda em triângulo (meios-tiles blends_street_01_65-68), como
ele já faz com o asfalto "que mistura nas bordas" (`MEDIUM_ASPHALT`).

Aqui, depois de gerar (antes dos prédios), nos trechos de rua com rumo entre
20 e 70 graus, a calçada de concreto vira a grama do lado e o meio-fio, a
sujeira e os postes daquela calçada saem. Os trechos retos (e a calçada deles
nos cruzamentos) ficam como estão. Mexe nos dois desenhos do chão e nos dois de
detalhes (`_base` incluídos: a etapa dos prédios recomeça deles).

Chamado pelo `knoxmap_pipeline.py` quando o config tem `"semCalcadaDiagonal": true`.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import shapely
from PIL import Image
from shapely.geometry import LineString
from shapely.ops import unary_union

PALE_CONCRETE = (120, 120, 120)      # generator/pz_colors.py do KnoxMap
GRAMAS = [(90, 100, 35), (117, 117, 47), (145, 135, 60)]
GRAMA_PADRAO = (117, 117, 47)
CALCADA = 3.0           # tiles além da meia pista em que pode haver calçada
ANG_MIN, ANG_MAX = 20, 70
TRECHO_MIN = 6          # tiles: trecho diagonal mais curto que isto não conta (curva de esquina)


ASFALTO = [(150, 150, 150), (100, 100, 100), (80, 80, 80)]
# Meios-tiles de asfalto (blends_street_01_65-68, o "street3" das ruas do KnoxMap):
# a metade do quadrado de grama que fica do lado do asfalto. Lado de cada metade
# medido nos pixels da folha (65 em cima, 66 embaixo, 67 à esquerda, 68 à direita
# da tela); em cima = bordas oeste e norte do quadrado, embaixo = leste e sul,
# esquerda = oeste e sul, direita = norte e leste.
TRIANGULOS = {("W", "N"): ((12, 40, 200), "blends_street_01_65"),
              ("E", "S"): ((12, 40, 201), "blends_street_01_66"),
              ("W", "S"): ((12, 40, 202), "blends_street_01_67"),
              ("N", "E"): ((12, 40, 203), "blends_street_01_68")}
MARCA = "RSB diagonal"


def garantir_regras(knox: Path) -> int:
    """Acrescenta ao Rules.txt das ferramentas de mapa as regras dos meios-tiles
    (uma cor do desenho de detalhes -> uma peça), sem repetir. Devolve quantas entraram."""
    import sys
    sys.path.insert(0, str(knox))
    import knoxpaths
    caminho = Path(knoxpaths.mapping_tools_dir()) / "config" / "Rules.txt"
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    novas = []
    for (lados, (cor, peca)) in TRIANGULOS.items():
        rotulo = f"{MARCA} {''.join(lados)}"
        if f"label = {rotulo}" in texto:
            continue
        novas.append(f"\nrule\n{{\n    label = {rotulo}\n    bitmap = 1\n"
                     f"    color = {cor[0]} {cor[1]} {cor[2]}\n"
                     f"    tiles = {peca}\n    layer = 0_FloorOverlay6\n}}\n")
    if novas:
        caminho.write_text(texto.rstrip() + "\n" + "".join(novas), encoding="utf-8")
    return len(novas)


def _diagonal(a, b) -> bool:
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 90
    return ANG_MIN <= ang <= ANG_MAX and math.dist(a, b) >= TRECHO_MIN


def tirar(knox: Path, nome: str, cfg: dict) -> dict:
    import sys
    sys.path.insert(0, str(knox))
    from generator.rendering.projection import Projector
    out = knox / "output" / nome
    info = json.loads((out / f"{nome}_info.json").read_text(encoding="utf-8"))
    bb = info["bbox"]
    pj = Projector.build(bb["south"], bb["west"], bb["north"], bb["east"],
                         info["meters_per_tile"], info.get("rotation", 0.0))
    feats = cfg.get("sketch", {}).get("features", [])
    largura = {str(-(i + 1)): float((f["properties"].get("tags") or {}).get("width", 6))
               for i, f in enumerate(feats) if f["geometry"]["type"] == "LineString"}
    rg = json.loads((out / f"{nome}_roadgraph.json").read_text(encoding="utf-8"))
    diag, reto = [], []
    for w, v in rg["ways"].items():
        pts = [pj.to_px(la, lo) for la, lo in v["geometry"]]
        meia = largura.get(w, 6) / 2 + CALCADA
        for a, b in zip(pts, pts[1:]):
            if math.dist(a, b) < 0.5:
                continue
            seg = LineString([a, b]).buffer(meia, cap_style="flat")
            (diag if _diagonal(a, b) else reto).append(seg)
    if not diag:
        return {"tiles": 0}
    alvo = unary_union(diag).difference(unary_union(reto)) if reto else unary_union(diag)
    shapely.prepare(alvo)
    x0, y0, x1, y1 = (max(0, int(v)) for v in alvo.bounds)

    chao = [out / f"{nome}.bmp", out / f"{nome}_ground_base.bmp"]
    det = [out / f"{nome}_veg.bmp", out / f"{nome}_veg_base.bmp"]
    trocados = None
    total = 0
    for p in chao:
        if not p.exists():
            continue
        img = np.array(Image.open(p).convert("RGB"))
        H, W = img.shape[:2]
        x1c, y1c = min(x1, W - 1), min(y1, H - 1)
        xs, ys = np.meshgrid(np.arange(x0, x1c + 1) + 0.5, np.arange(y0, y1c + 1) + 0.5)
        dentro = shapely.contains_xy(alvo, xs, ys)
        parte = img[y0:y1c + 1, x0:x1c + 1]
        concreto = (parte == PALE_CONCRETE).all(axis=2) & dentro
        grama = np.zeros(parte.shape[:2], bool)
        for g in GRAMAS:
            grama |= (parte == g).all(axis=2)
        nova = parte.copy()
        for r, c in zip(*np.nonzero(concreto)):
            # a grama mais comum em volta (mantém o tipo de grama do lugar)
            r0, r1, c0, c1 = max(0, r - 4), r + 5, max(0, c - 4), c + 5
            viz = parte[r0:r1, c0:c1][grama[r0:r1, c0:c1]]
            if len(viz):
                cores, n = np.unique(viz.reshape(-1, 3), axis=0, return_counts=True)
                nova[r, c] = cores[int(np.argmax(n))]
            else:
                nova[r, c] = GRAMA_PADRAO
        img[y0:y1c + 1, x0:x1c + 1] = nova
        Image.fromarray(img, "RGB").save(p, format="BMP")
        if trocados is None:
            trocados = (concreto, (y0, y1c, x0, x1c))
        total = max(total, int(concreto.sum()))
    # Dentes da borda do asfalto: o quadrado de grama com asfalto em dois lados
    # vizinhos (e não nos outros dois) ganha a metade de asfalto daquele lado.
    tri = None
    if chao[0].exists():
        img = np.array(Image.open(chao[0]).convert("RGB"))
        H, W = img.shape[:2]
        asf = np.zeros((H, W), bool)
        for c in ASFALTO:
            asf |= (img == c).all(axis=2)
        gram = np.zeros((H, W), bool)
        for g in GRAMAS:
            gram |= (img == g).all(axis=2)
        viz = {"N": np.zeros_like(asf), "S": np.zeros_like(asf), "W": np.zeros_like(asf), "E": np.zeros_like(asf)}
        viz["N"][1:, :] = asf[:-1, :]
        viz["S"][:-1, :] = asf[1:, :]
        viz["W"][:, 1:] = asf[:, :-1]
        viz["E"][:, :-1] = asf[:, 1:]
        ys2, xs2 = np.mgrid[0:H, 0:W]
        perto = np.zeros((H, W), bool)
        sub = shapely.contains_xy(alvo, xs2[y0:min(y1, H - 1) + 1, x0:min(x1, W - 1) + 1] + 0.5,
                                  ys2[y0:min(y1, H - 1) + 1, x0:min(x1, W - 1) + 1] + 0.5)
        perto[y0:y0 + sub.shape[0], x0:x0 + sub.shape[1]] = sub
        tri = np.zeros((H, W, 3), np.uint8)
        for lados, (cor, _p) in TRIANGULOS.items():
            outros = [l for l in "NSWE" if l not in lados]
            m2 = gram & perto & viz[lados[0]] & viz[lados[1]] & ~viz[outros[0]] & ~viz[outros[1]]
            tri[m2] = cor
        n_tri = int(tri.any(axis=2).sum())
    if trocados is not None:
        m, (ya, yb, xa, xb) = trocados
        for p in det:
            if not p.exists():
                continue
            img = np.array(Image.open(p).convert("RGB"))
            parte = img[ya:yb + 1, xa:xb + 1]
            # meio-fio (12,34,*), sujeira e postes de calçada (12,36,*) saem; as faixas da pista ficam
            calcada = m & (parte[..., 0] == 12) & np.isin(parte[..., 1], (34, 36))
            parte[calcada] = (0, 0, 0)
            img[ya:yb + 1, xa:xb + 1] = parte
            if tri is not None:
                tem = tri.any(axis=2) & (img == 0).all(axis=2)
                img[tem] = tri[tem]
            Image.fromarray(img, "RGB").save(p, format="BMP")
    return {"tiles_de_calcada_que_viraram_grama": total, "trechos_diagonais": len(diag),
            "meios_tiles_na_borda": n_tri if tri is not None else 0,
            "regras_novas": garantir_regras(knox)}
