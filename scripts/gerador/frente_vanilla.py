"""Descobre de que lado fica a frente (a rua) de um prédio do mapa original.

Conta, em faixas de 7 quadrados em volta do prédio, os tiles de rua (asfalto,
meio-fio, faixa) ao nível do chão; o lado com mais rua é a frente. Serve para
as cópias do D-38 (a cópia não gira, então precisamos saber o lado da porta).
NÃO CONFIÁVEL (08/11/2026): no teste acertou a loja de armas (W), o quartel (W) e a delegacia (E), mas errou a
farmácia (deu E, é W) e o mercado (deu E, é S). Conferir sempre olhando `render_lots --world`. Melhorar
contando só o asfalto e o meio-fio, ou achando a porta pelos tiles de porta.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

MAPAS = Path("C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/maps/Muldraugh, KY")
RUA = ("blends_street", "street_", "blends_natural_01_0")


def caixa(rooms, ids):
    rs = [rooms[k] for k in ids if 0 <= k < len(rooms)]
    xs = [x for _n, _l, rc in rs for x, _y, w, _h in rc for x in (x, x + w)]
    ys = [y for _n, _l, rc in rs for _x, y, _w, h in rc for y in (y, y + h)]
    return min(xs), min(ys), max(xs), max(ys)


def portas(sq, x0, y0, x1, y1):
    """Lados do perímetro (andar 0) que têm porta de entrada."""
    lados = set()
    for (x, y, z), ts in sq.items():
        if z != 0 or not any(t.startswith(("fixtures_doors_01", "fixtures_doors_frames")) for t in ts):
            continue
        if not (x0 - 1 <= x <= x1 and y0 - 1 <= y <= y1):
            continue
        if x in (x0 - 1, x0) and y0 <= y < y1:
            lados.add("W")
        if x in (x1 - 1, x1) and y0 <= y < y1:
            lados.add("E")
        if y in (y0 - 1, y0) and x0 <= x < x1:
            lados.add("N")
        if y in (y1 - 1, y1) and x0 <= x < x1:
            lados.add("S")
    return lados


def frente(sq, x0, y0, x1, y1, faixa=7):
    """Devolve (lado, contagens). Lados: N (y menor), S, W (x menor), E."""
    cont = {"N": 0, "S": 0, "W": 0, "E": 0}
    for (x, y, z), ts in sq.items():
        if z != 0 or not any(t.startswith(RUA) for t in ts):
            continue
        if x0 <= x < x1 and y0 <= y < y1:
            continue
        if x0 - faixa <= x < x1 + faixa and y0 - faixa <= y < y1 + faixa:
            # de que lado do prédio fica este quadrado (o lado em que mais "passa" do retângulo)
            dx = max(x0 - x, x - (x1 - 1), 0)
            dy = max(y0 - y, y - (y1 - 1), 0)
            if dx >= dy:
                cont["W" if x < x0 else "E"] += 1
            if dy >= dx:
                cont["N" if y < y0 else "S"] += 1
    p = portas(sq, x0, y0, x1, y1)
    cands = {k: v for k, v in cont.items() if k in p} or cont
    lado = max(cands, key=cands.get)
    return lado, {**cont, "portas": "".join(sorted(p))}


if __name__ == "__main__":
    KNOX = sys.argv[1]
    sys.path.insert(0, KNOX)
    os.chdir(KNOX)
    from tools.building_stats import read_header, read_squares
    for arg in sys.argv[2:]:
        cel, i = arg.split(":")
        nomes, lo, hi, rooms, predios = read_header(str(MAPAS / f"{cel}.lotheader"))
        sq = read_squares(str(MAPAS / f"world_{cel}.lotpack"), nomes, lo, hi)
        print(arg, *frente(sq, *caixa(rooms, predios[int(i)])))
