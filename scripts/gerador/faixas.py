"""Faixa amarela no meio do asfalto (U13).

No modo de ruas 2 do KnoxMap ("Vanilla curves"), o asfalto sai 1 tile
deslocado em relação à linha central que ele usa para pintar a faixa: numa rua
de 6 tiles ficavam 2 tiles de asfalto de um lado da faixa e 4 do outro (medido
no rio_piloto, 08/11/2026: só 2% das faixas no meio). A linha central está no
lugar certo; quem anda 1 tile é o asfalto.

Depois de gerar o mapa (e antes dos prédios), este script move cada trecho de
faixa amarela para o meio do asfalto, nos dois desenhos de detalhes do KnoxMap:
`<mapa>_veg.bmp` e `<mapa>_veg_base.bmp` (a etapa dos prédios recomeça do
`_base`). Rua de largura ímpar não tem meio exato e fica como está.

Chamado pelo `knoxmap_pipeline.py` quando o config tem `"centrarFaixas": true`.
Sozinho (Python do .venv do KnoxMap):
    python -I faixas.py <pasta output/<mapa> do KnoxMap> <mapa>
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
from PIL import Image

# cores do desenho do chão e do desenho de detalhes (generator/pz_colors.py do KnoxMap)
ASFALTO = [(150, 150, 150), (100, 100, 100), (80, 80, 80), (110, 100, 100), (130, 120, 120)]
AMARELA = {"N": (12, 35, 200), "W": (12, 35, 201)}   # faixa na borda norte / oeste do tile
LIVRE = {(0, 0, 0), (12, 36, 200), (12, 36, 201)}      # nada, sujeira, rachadura: a faixa vai por cima
LARGURA_MAX = 16                                       # mais que isto é pátio ou cruzamento: não mexe


def _corrida(asf, y, x, dy, dx):
    n = 0
    H, W = asf.shape
    while 0 <= y < H and 0 <= x < W and asf[y, x]:
        n += 1
        y += dy
        x += dx
    return n


def centrar(pasta: pathlib.Path, nome: str) -> dict:
    chao = np.asarray(Image.open(pasta / f"{nome}.bmp").convert("RGB"))
    asf = np.zeros(chao.shape[:2], bool)
    for c in ASFALTO:
        asf |= (chao == c).all(axis=2)
    caminhos = [p for p in (pasta / f"{nome}_veg.bmp", pasta / f"{nome}_veg_base.bmp") if p.exists()]
    vegs = [np.array(Image.open(p).convert("RGB")) for p in caminhos]
    v0 = vegs[0]
    movs, no_meio, impares, total = [], 0, 0, 0
    for borda, cor in AMARELA.items():
        ys, xs = np.nonzero((v0 == cor).all(axis=2))
        for y, x in zip(ys.tolist(), xs.tolist()):
            total += 1
            if borda == "N":   # faixa entre as linhas y-1 (acima) e y (abaixo)
                a, b = _corrida(asf, y - 1, x, -1, 0), _corrida(asf, y, x, 1, 0)
            else:              # entre as colunas x-1 (oeste) e x (leste)
                a, b = _corrida(asf, y, x - 1, 0, -1), _corrida(asf, y, x, 0, 1)
            d = b - a
            if a + b > LARGURA_MAX:
                continue
            if d == 0:
                no_meio += 1
            elif d % 2:
                impares += 1
            else:
                movs.append((borda, cor, y, x, d // 2))
    for v in vegs:
        for borda, cor, y, x, s in movs:
            if (v[y, x] == cor).all():
                v[y, x] = (0, 0, 0)
        for borda, cor, y, x, s in movs:
            ny, nx = (y + s, x) if borda == "N" else (y, x + s)
            if tuple(int(c) for c in v[ny, nx]) in LIVRE:
                v[ny, nx] = cor
    for p, v in zip(caminhos, vegs):
        Image.fromarray(v, "RGB").save(p, format="BMP")
    return {"faixas": total, "ja_no_meio": no_meio, "movidas": len(movs), "largura_impar": impares,
            "arquivos": [p.name for p in caminhos]}


if __name__ == "__main__":
    print(centrar(pathlib.Path(sys.argv[1]), sys.argv[2]))
