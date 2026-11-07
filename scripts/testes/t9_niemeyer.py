"""T9 (curvas): a Av. Niemeyer real, encolhida a 1:15, como rua desenhada.

Gera um config por modo de rua do KnoxMap (`straight_roads`):
0 = como no mapa, 1 = retas e 45 graus (Knox County),
2 = 16 direções do B42 com as curvas do jogo, 3 = 2 + ruas de bairro no grid.

Uso (Python do .venv do KnoxMap):
    python -I t9_niemeyer.py <niemeyer.json da Overpass> <pasta de saída>
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gerador"))
from gerador_t7c import METROS_FALSOS, Projecao, feature  # noqa: E402

from shapely.geometry import LineString, MultiLineString  # noqa: E402
from shapely.ops import linemerge  # noqa: E402


def main() -> int:
    src, pasta = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as fh:
        ways = json.load(fh)["elements"]
    pontos = [(p["lon"], p["lat"]) for w in ways for p in w["geometry"]]
    proj = Projecao(pontos)
    linhas = [LineString([proj.para_tile(p["lon"], p["lat"]) for p in w["geometry"]])
              for w in ways if len(w["geometry"]) >= 2]
    junto = linemerge(MultiLineString(linhas))
    partes = list(getattr(junto, "geoms", [junto]))
    # Pistas duplas (mão única) viram duas linhas paralelas; para o teste fica
    # só o traçado contínuo mais longo, como uma avenida de mão dupla.
    rua = max(partes, key=lambda g: g.length).simplify(0.3)
    feats = [feature("primary", rua, proj, {"name": "Avenida Niemeyer"})]
    # Variante "acessos" (modo 2b): o modo 2 dá a cada trecho entre dois
    # cruzamentos no máximo 1 ou 2 curvas, como no jogo base. Acessos curtos
    # (como as entradas reais da Niemeyer) a cada ~ACESSO_A_CADA tiles criam
    # cruzamentos, e cada trecho ganha as suas curvas.
    ACESSO_A_CADA = 30
    acessos = []
    d = ACESSO_A_CADA
    while d < rua.length - 10:
        p = rua.interpolate(d)
        q = rua.interpolate(d + 1)
        dx, dy = q.x - p.x, q.y - p.y
        n = (dx * dx + dy * dy) ** 0.5 or 1
        # perpendicular, 10 tiles, para o lado de fora da curva (alternando)
        lado = 1 if (d // ACESSO_A_CADA) % 2 else -1
        fim = (p.x - dy / n * 10 * lado, p.y + dx / n * 10 * lado)
        acessos.append(feature("service", LineString([(p.x, p.y), fim]), proj))
        d += ACESSO_A_CADA
    minx, miny, maxx, maxy = rua.bounds
    folga = 25
    sw = proj.para_falso(minx - folga, miny - folga)
    ne = proj.para_falso(maxx + folga, maxy + folga)
    print(f"Niemeyer a 1:15: {rua.length:.0f} tiles de comprimento, "
          f"caixa {maxx - minx:.0f} x {maxy - miny:.0f} tiles, {len(rua.coords)} pontos")
    # Variante "cidade" (modo 2c): fora da cidade o modo 2 deixa a rua se
    # afastar muito do traçado real; dentro, segue de perto. Uma faixa de área
    # urbana em volta da avenida (como os prédios e o Vidigal reais) a deixa
    # "dentro da cidade".
    faixa = rua.buffer(18)
    cidade = [feature("houses_land", faixa, proj)]
    extras = {"2b": acessos, "2c": cidade, "2d": cidade + acessos}
    for modo in (0, 1, 2, 3, "2b", "2c", "2d"):
        nome = f"rsb_t9_niemeyer_m{modo}"
        cfg = {
            "mapName": nome, "modId": nome,
            "title": f"RSB Teste T9 - Niemeyer modo {modo}",
            "south": sw[1], "west": sw[0], "north": ne[1], "east": ne[0],
            "metersPerTile": METROS_FALSOS, "drawnOnly": True, "standalone": True,
            "settings": {"align_streets": 0,
                         "straight_roads": 2 if isinstance(modo, str) else modo},
            "sketch": {"type": "FeatureCollection",
                       "features": feats + extras.get(str(modo), [])},
        }
        with open(os.path.join(pasta, f"t9_niemeyer_m{modo}.json"), "w", encoding="utf-8") as fh:
            json.dump(cfg, fh, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
