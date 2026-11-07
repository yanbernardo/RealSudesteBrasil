"""Copia um prédio do mapa original (Knox County) para um .tbx que o KnoxMap estampa.

A estrutura inteira vem junto: piso, paredes, portas, janelas/vitrine, móveis,
cômodos (com os nomes do jogo, então o loot é o do jogo) e telhado. Cada quadrado
do prédio vira uma pilha de tiles "pintados" (camadas <tiles> do BuildingEd), na
mesma ordem do mapa original; as paredes automáticas do KnoxMap ficam desligadas.

Uso (Python do .venv do KnoxMap):
  listar:  python -I copiar_predio_vanilla.py <KnoxMap> listar pharmacy [gunstore ...]
  copiar:  python -I copiar_predio_vanilla.py <KnoxMap> copiar <célula X_Y> <nº do prédio> <nome> <saída.tbx>
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

KNOX = sys.argv[1]
sys.path.insert(0, KNOX)
os.chdir(KNOX)
from tools.building_stats import read_header, read_squares  # noqa: E402

MAPAS = Path("C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/maps/Muldraugh, KY")
# Cômodos que podem existir numa loja "sozinha" além do tipo procurado.
APOIO = {"bathroom", "storage", "office", "janitor", "breakroom", "hall", "hallway", "empty",
         "closet", "stockroom", "backroom"}
# Fora dos cômodos (na faixa da parede de fora) só vem o que é do prédio.
DO_PREDIO = ("walls_", "fixtures_", "roofs_", "location_shop", "location_business",
             "lighting_outdoor", "fixtures_signs", "signs_")


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


def copiar(celula: str, indice: int, nome: str, saida: str) -> None:
    cab = MAPAS / f"{celula}.lotheader"
    nomes, lo, hi, rooms, predios = _predios(cab)
    sq = read_squares(str(MAPAS / f"world_{celula}.lotpack"), nomes, lo, hi)
    rs = [rooms[k] for k in predios[indice]]
    x0 = min(x for _n, _l, rects in rs for x, _y, _w, _h in rects)
    y0 = min(y for _n, _l, rects in rs for _x, y, _w, _h in rects)
    x1 = max(x + w for _n, _l, rects in rs for x, _y, w, _h in rects)
    y1 = max(y + h for _n, _l, rects in rs for _x, y, _w, h in rects)
    W, H = x1 - x0, y1 - y0
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
                if (x, y) not in dentro.get(z, set()) and not (z == topo and dentro.get(z - 1, set())
                                                                 and (x, y) in dentro[z - 1]):
                    # fora dos cômodos: só parede, porta, janela, telhado, letreiro
                    vizinho = any((x + a, y + b) in dentro.get(z, set()) or (x + a, y + b) in dentro.get(max(z - 1, 0), set())
                                  for a in (-1, 0) for b in (-1, 0))
                    ts = [t for t in ts if t.startswith(DO_PREDIO)] if vizinho else \
                         [t for t in ts if t.startswith("roofs_")]
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
        copiar(sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6])
