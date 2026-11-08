"""Copia um prédio do mapa original (Knox County) para um .tbx que o KnoxMap estampa.

A estrutura inteira vem junto: piso, paredes, portas, janelas/vitrine, móveis,
cômodos (com os nomes do jogo, então o loot é o do jogo) e telhado. Cada quadrado
do prédio vira uma pilha de tiles "pintados" (camadas <tiles> do BuildingEd), na
mesma ordem do mapa original; as paredes automáticas do KnoxMap ficam desligadas.

Uso (Python do .venv do KnoxMap):
  listar:  python -I copiar_predio_vanilla.py <KnoxMap> listar pharmacy [gunstore ...]
  copiar:  python -I copiar_predio_vanilla.py <KnoxMap> copiar <célula X_Y> <nº do prédio> <nome> <saída.tbx> [oeste,norte,leste,sul]
           (o último, opcional: tiles de entorno em volta do prédio, copiados com o chão)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

KNOX = sys.argv[1]
sys.path.insert(0, KNOX)
PASTA_ORIGEM = os.getcwd()   # caminhos de saída relativos valem a partir daqui (K34)
os.chdir(KNOX)
from tools.building_stats import read_header, read_squares  # noqa: E402

MAPAS = Path("C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/maps/Muldraugh, KY")
# Cômodos que podem existir numa loja "sozinha" além do tipo procurado.
APOIO = {"bathroom", "storage", "office", "janitor", "breakroom", "hall", "hallway", "empty",
         "closet", "stockroom", "backroom"}
# Peças de chão/terreno: ficam de fora da cópia (o KnoxMap faz o terreno em volta).
CHAO = ("blends_", "floors_exterior", "vegetation_", "e_", "d_", "f_", "overlay_grime_floor",
        "street_", "natural_")


def _predios(cab: Path):
    nomes, lo, hi, rooms, predios = read_header(str(cab))
    return nomes, lo, hi, rooms, predios


def listar(alvos: set[str]) -> None:
    for cab in sorted(MAPAS.glob("*.lotheader")):
        _n, _lo, _hi, rooms, predios = _predios(cab)
        for i, ids in enumerate(predios):
            rs = [rooms[k] for k in ids if 0 <= k < len(rooms)]
            nomes = {r[0] for r in rs}
            principais = nomes & alvos
            if not principais or not nomes <= (alvos | APOIO | {r + "storage" for r in alvos}):
                continue
            xs = [x for _nm, _lv, rects in rs for x, _y, w, _h in rects for x in (x, x + w)]
            ys = [y for _nm, _lv, rects in rs for _x, y, _w, h in rects for y in (y, y + h)]
            niveis = sorted({lv for _nm, lv, _r in rs})
            print(f"{cab.stem:>7} prédio {i:4d}: {max(xs) - min(xs):3d} x {max(ys) - min(ys):3d} tiles, "
                  f"andares {niveis}, cômodos {sorted(nomes)}")


def copiar(celula: str, indice: int, nome: str, saida: str, margens=(0, 0, 0, 0)) -> None:
    """`margens` = tiles a mais em volta do prédio (oeste, norte, leste, sul): o
    "entorno" (estacionamento, cerca, postes, gramado) vem junto, com o chão."""
    cab = MAPAS / f"{celula}.lotheader"
    nomes, lo, hi, rooms, predios = _predios(cab)
    sq = read_squares(str(MAPAS / f"world_{celula}.lotpack"), nomes, lo, hi)
    rs = [rooms[k] for k in predios[indice]]
    x0 = min(x for _n, _l, rects in rs for x, _y, _w, _h in rects)
    y0 = min(y for _n, _l, rects in rs for _x, y, _w, _h in rects)
    x1 = max(x + w for _n, _l, rects in rs for x, _y, w, _h in rects)
    y1 = max(y + h for _n, _l, rects in rs for _x, y, _w, h in rects)
    mo, mn, ml, ms = margens
    bx, by, bw, bh = mo, mn, x1 - x0, y1 - y0          # o prédio dentro do retângulo copiado
    x0, y0 = x0 - mo, y0 - mn
    W, H = bw + mo + ml, bh + mn + ms
    # quadrados de cômodos de outros prédios (no entorno não se copia vizinho)
    meus = set(predios[indice])
    alheio = {}
    for k, (_nm, lv, rects) in enumerate(rooms):
        if k in meus:
            continue
        for x, y, w, h in rects:
            for a in range(w):
                for b in range(h):
                    alheio.setdefault(lv, set()).add((x + a, y + b))
    niveis = sorted({lv for _n, lv, _r in rs if lv >= 0})
    topo = max(niveis) + 1          # o telhado fica no andar de cima do último

    # cômodos do tbx: um por nome e andar
    tipos = []
    grade = {z: [[0] * W for _ in range(H)] for z in range(topo + 1)}
    for nm, lv, rects in rs:
        if lv < 0:
            continue
        if nm not in tipos:
            tipos.append(nm)
        for x, y, w, h in rects:
            for dx in range(w):
                for dy in range(h):
                    grade[lv][y - y0 + dy][x - x0 + dx] = tipos.index(nm) + 1
    dentro = {z: {(x, y) for y in range(H) for x in range(W) if grade[z][y][x]} for z in grade}

    # pilhas de tiles por quadrado (inclui a faixa de 1 quadrado a leste e ao sul: paredes de fora)
    pilhas: dict[int, dict[tuple[int, int], list[str]]] = {}
    for z in range(topo + 1):
        pz = {}
        for y in range(H + 1):
            for x in range(W + 1):
                ts = sq.get((x0 + x, y0 + y, z), [])
                if not ts:
                    continue
                no_predio = bx <= x <= bx + bw and by <= y <= by + bh
                if not no_predio:
                    # entorno: tudo, com o chão (menos vizinho e menos o chão da faixa de
                    # fora a leste e ao sul, que é a calçada do KnoxMap)
                    if (x0 + x, y0 + y) in alheio.get(z, set()):
                        continue
                    if x == W or y == H:
                        ts = [t for t in ts if not t.startswith(CHAO)]
                elif (x, y) not in dentro.get(z, set()) and not (z == topo and dentro.get(z - 1, set())
                                                                   and (x, y) in dentro[z - 1]):
                    # Fora dos cômodos, mas no retângulo do prédio (com a faixa das paredes
                    # de fora a leste e ao sul): fica tudo menos o chão. As paredes de fora
                    # podem ser de qualquer conjunto de peças (o quartel 47_27 usa "industry_",
                    # que não estava na lista antiga, e as paredes sumiam: U22).
                    ts = [t for t in ts if not t.startswith(CHAO)]
                if ts:
                    pz[(x, y)] = ts
        pilhas[z] = pz

    todos = sorted({t for pz in pilhas.values() for ts in pz.values() for t in ts})
    idx = {t: i + 1 for i, t in enumerate(todos)}
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           f'<building version="4" width="{W}" height="{H}" ExteriorWall="0" ExteriorWallTrim="0" '
           'Door="0" DoorFrame="0" Window="0" Curtains="0" Shutters="0" Stairs="0" RoofCap="0" '
           'RoofSlope="0" RoofTop="0" GrimeWall="0">',
           " <user_tiles>"]
    out += [f"  <tile tile={quoteattr(t)}/>" for t in todos]
    out += [" </user_tiles>", " <used_tiles></used_tiles>", " <used_furniture></used_furniture>"]
    for nm in tipos:
        out.append(f' <room Name={quoteattr(nm)} InternalName={quoteattr(nm)} Color="176 92 195" '
                   'InteriorWall="0" InteriorWallTrim="0" Floor="0" GrimeFloor="0" GrimeWall="0" Ceiling="0"/>')
    for z in range(topo + 1):
        out.append(" <floor>")
        pz = pilhas.get(z, {})
        camadas = max((len(v) for v in pz.values()), default=0)
        for c in range(camadas):
            linhas = []
            for y in range(H + 1):
                linhas.append(",".join(str(idx[pz[(x, y)][c]]) if (x, y) in pz and c < len(pz[(x, y)]) else "0"
                                       for x in range(W + 1)))
            out.append(f'  <tiles layer="Camada{c}">' + escape("\n" + ",\n".join(linhas) + "\n") + "</tiles>")
        g = grade.get(z, [[0] * W for _ in range(H)])
        out.append("  <rooms>\n" + ",\n".join(",".join(str(v) for v in row) for row in g) + "\n  </rooms>")
        out.append(" </floor>")
    out.append("</building>")
    Path(saida).parent.mkdir(parents=True, exist_ok=True)
    Path(saida).write_text("\n".join(out), encoding="utf-8")
    print(f"{nome}: {W} x {H} tiles, {topo + 1} andares (com telhado), {len(todos)} tiles diferentes, "
          f"cômodos {tipos} -> {saida}")


if __name__ == "__main__":
    if sys.argv[2] == "listar":
        listar(set(sys.argv[3:]))
    else:
        m = tuple(int(v) for v in sys.argv[7].split(",")) if len(sys.argv) > 7 else (0, 0, 0, 0)
        copiar(sys.argv[3], int(sys.argv[4]), sys.argv[5], os.path.join(PASTA_ORIGEM, sys.argv[6]), m)
