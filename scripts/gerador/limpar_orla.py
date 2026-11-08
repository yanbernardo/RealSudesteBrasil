"""Areia limpa na orla (U25).

Onde uma rua reta chega numa avenida diagonal da orla (Av. Atlântica), o
acabamento de cruzamento do KnoxMap faz um "quadrado" de asfalto e calçada que
sai da faixa da avenida e entra na areia: a rua parece "vazar" para a praia
(usuário, 08/11/2026). O nosso desenho termina a rua exatamente na avenida; o
quadrado é do KnoxMap.

Depois de gerar o mapa (antes dos prédios), dentro das áreas de areia do nosso
desenho, todo tile mais longe da avenida que meia pista + calçada volta a ser
areia, e os detalhes por cima (poste, meio-fio, faixa) saem. Mexe nos dois
desenhos do chão e nos dois de detalhes (`_base` incluídos: a etapa dos prédios
recomeça deles).

Chamado pelo `knoxmap_pipeline.py` quando o config tem `"limparOrla": true`.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import shapely
from PIL import Image
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union

SAND = (210, 200, 160)          # generator/pz_colors.py do KnoxMap
CALCADA = 2.0                   # tiles de calçada além da meia pista
CORRE_NA_ORLA = 30              # tiles de via a menos de 12 da areia: é avenida da orla


def limpar(knox: Path, nome: str, cfg: dict) -> dict:
    import sys
    sys.path.insert(0, str(knox))
    from generator.rendering.projection import Projector
    out = knox / "output" / nome
    info = json.loads((out / f"{nome}_info.json").read_text(encoding="utf-8"))
    bb = info["bbox"]
    pj = Projector.build(bb["south"], bb["west"], bb["north"], bb["east"],
                         info["meters_per_tile"], info.get("rotation", 0.0))
    feats = cfg.get("sketch", {}).get("features", [])
    areia = unary_union([Polygon([pj.to_px(la, lo) for lo, la in f["geometry"]["coordinates"][0]])
                         for f in feats if f["properties"].get("kind") == "sand"
                         and f["geometry"]["type"] == "Polygon"]).buffer(0)
    if areia.is_empty:
        return {"tiles": 0}
    # avenidas como o KnoxMap as traçou (roadgraph), com a largura do desenho
    largura = {str(-(i + 1)): float((f["properties"].get("tags") or {}).get("width", 6))
               for i, f in enumerate(feats) if f["geometry"]["type"] == "LineString"}
    rg = json.loads((out / f"{nome}_roadgraph.json").read_text(encoding="utf-8"))
    perto = areia.buffer(12)
    faixas = []
    for w, v in rg["ways"].items():
        L = LineString([pj.to_px(la, lo) for la, lo in v["geometry"]])
        # só a avenida que CORRE ao longo da praia; a rua que só chega nela
        # não protege nada (a ponta dela é justamente o "vazamento")
        if L.intersection(perto).length >= CORRE_NA_ORLA:
            faixas.append(L.buffer(largura.get(w, 6) / 2 + CALCADA, cap_style="flat"))
    pista = unary_union(faixas) if faixas else Polygon()
    alvo = areia.difference(pista)
    shapely.prepare(alvo)
    x0, y0, x1, y1 = (int(v) for v in alvo.bounds)
    xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
    m = shapely.contains_xy(alvo, xs, ys)
    arquivos = {"chao": [out / f"{nome}.bmp", out / f"{nome}_ground_base.bmp"],
                "det": [out / f"{nome}_veg.bmp", out / f"{nome}_veg_base.bmp"]}
    mudou = 0
    for tipo, caminhos in arquivos.items():
        for p in caminhos:
            if not p.exists():
                continue
            img = np.array(Image.open(p).convert("RGB"))
            parte = img[y0:y1 + 1, x0:x1 + 1]
            if tipo == "chao":
                trocar = m & ~(parte == SAND).all(axis=2)
                parte[trocar] = SAND
                mudou = max(mudou, int(trocar.sum()))
            else:
                parte[m] = (0, 0, 0)
            img[y0:y1 + 1, x0:x1 + 1] = parte
            Image.fromarray(img, "RGB").save(p, format="BMP")
    return {"tiles_que_voltaram_a_ser_areia": mudou}
