"""T8d (D-35): viagem de rodovia pela Dutra real, Piraí -> Volta Redonda, a 1:15.

- Rodovia: traçado real da BR-116 (Overpass, `dados/contornos/dutra_pirai_vr.json`),
  encolhido a 1:15, cortado entre os pontos mais perto de Piraí e de Volta
  Redonda e suavizado; vira pista dupla (2 faixas por sentido e canteiro) com
  `scripts/gerador/rodovia.py`. Bordas e faixas pintadas ainda em degraus nas
  diagonais (K15): o desenho de curvas nosso é da Etapa 2.
- Vila A (ponta de Piraí), nível "completa" (D-35): casas, posto com bombas do
  jogo (ponto "fuel" do KnoxMap), mercadinho e farmácia (cópia da Pharmahug, D-38).
- Vila B (ponta de Volta Redonda), nível "seca": só casas.
- Zonas de estrada e de mata ao longo da rodovia: `zonas_historias.py`, a partir
  da linha guardada em "rodovias" no config.

Uso (Python do .venv do KnoxMap):
    python -I t8d_dutra.py <dutra_pirai_vr.json> <saida.json>
"""
from __future__ import annotations

import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gerador"))
from gerador_t7c import METROS_FALSOS, Projecao, feature  # noqa: E402
import rodovia  # noqa: E402

from shapely.geometry import LineString, MultiLineString, Point, box  # noqa: E402
from shapely.ops import linemerge, substring  # noqa: E402

PASSO_X, PASSO_Y = 46, 46     # quarteirões quadrados (cabe a farmácia original com a rua a oeste)
AFASTAMENTO_VILA = 95         # do fim da rodovia até o centro da vila


def cadeia_da_dutra(elementos, proj):
    linhas = [LineString([proj.para_tile(p["lon"], p["lat"]) for p in e["geometry"]])
              for e in elementos if e["type"] == "way" and len(e.get("geometry", [])) >= 2]
    junto = linemerge(MultiLineString(linhas))
    partes = list(getattr(junto, "geoms", [junto]))
    # Uma pista (mão única) contínua; a outra corre colada a ela a 1:15.
    return max(partes, key=lambda g: g.length)


def lotes_de_casas(q, rnd_semente, pular=None):
    """Duas fileiras de casas (frente para a rua de baixo e para a de cima)."""
    import random
    rnd = random.Random(rnd_semente)
    qx0, qy0, qx1, qy1 = q.bounds
    out = []
    for lado in (0, 1):
        x = qx0
        while True:
            w, d = rnd.randint(7, 9), rnd.randint(8, 10)
            if x + w > qx1:
                break
            lote = (box(x, qy0 + 1, x + w, qy0 + 1 + d) if lado == 0
                    else box(x, qy1 - 1 - d, x + w, qy1 - 1))
            if pular is not None and lote.intersects(pular):
                # pula a loja e continua do outro lado dela (casas em volta das lojas)
                fim = max(g.bounds[2] for g in getattr(pular, "geoms", [pular]) if g.intersects(lote))
                x = max(x + 1, int(fim) + 1)
                continue
            out.append((lote, rnd.choice((1, 1, 2))))
            x += w + rnd.randint(2, 4)
    return out


def vila(cx, cy, completa, proj, semente):
    """Vila de 2 x 2 quarteirões com centro (cx, cy) em tiles (y para o norte)."""
    feats, ruas = [], []
    xs = [cx - PASSO_X, cx, cx + PASSO_X]
    ys = [cy - PASSO_Y, cy, cy + PASSO_Y]
    for x in xs:
        g = LineString([(x, ys[0] - 8), (x, ys[-1] + 8)])
        ruas.append(g)
        feats.append(feature("residential", g, proj))
    for y in ys:
        g = LineString([(xs[0] - 8, y), (xs[-1] + 8, y)])
        ruas.append(g)
        feats.append(feature("residential", g, proj))
    resumo = {"casas": 0, "lojas": []}
    # Vila "completa": lojas com casas em volta, no mesmo quarteirão (como no
    # jogo base). Cada loja reserva um pedaço; as casas preenchem o resto.
    # Lojas = cópias do mapa original (D-38) via kit de lojas, escolhidas pela
    # etiqueta shop= e pela rua mais próxima (precisa ser a da frente da cópia).
    lojas = {}
    if completa:
        lojas[(1, 0)] = [("shop", box(xs[1] + 8, ys[0] + 11, xs[1] + 28, ys[0] + 35),
                          {"shop": "chemist", "name": "Farmacia", "building:levels": "1"},
                          box(xs[1] + 4, ys[0] + 4, xs[1] + 30, ys[0] + 40), "farmacia (Pharmahug, rua a oeste)")]
        lojas[(0, 1)] = [("shop", box(xs[0] + 12, ys[1] + 7, xs[0] + 26, ys[1] + 24),
                          {"shop": "convenience", "name": "Mercadinho", "building:levels": "1"},
                          box(xs[0] + 8, ys[1] + 4, xs[0] + 29, ys[1] + 27), "mercadinho (mercearia 52_8, rua ao sul)")]
        # Posto: loja de 10 x 8 e um ponto "fuel" dentro dela; o KnoxMap faz o
        # pátio com as bombas do jogo para o lado da rua mais próxima (oeste).
        lojas[(0, 0)] = [("posto", box(xs[0] + 14, ys[0] + 18, xs[0] + 24, ys[0] + 26),
                          {"name": "Posto", "building:levels": "1"},
                          box(xs[0] + 4, ys[0] + 4, xs[0] + 27, ys[0] + 28), "posto (bombas do jogo)")]
    for i in range(2):
        for j in range(2):
            q = box(xs[i] + 6, ys[j] + 6, xs[i + 1] - 6, ys[j + 1] - 6)
            feats.append(feature("houses_land", q, proj))
            reserva = None
            for tipo, lote, tags, res, nome in lojas.get((i, j), []):
                feats.append(feature("shop", lote, proj, tags))
                if tipo == "posto":
                    c = lote.centroid
                    feats.append({"type": "Feature", "properties": {"kind": "fuel"},
                                  "geometry": {"type": "Point", "coordinates": proj.para_falso(c.x, c.y)}})
                reserva = res if reserva is None else reserva.union(res)
                resumo["lojas"].append(nome)
            for lote, andares in lotes_de_casas(q, semente * 10 + i * 2 + j, reserva):
                feats.append(feature("house", lote, proj, {"building:levels": str(andares)}))
                resumo["casas"] += 1
    return feats, ruas, resumo


def main() -> int:
    src, saida = sys.argv[1], sys.argv[2]
    dados = json.load(open(src, encoding="utf-8"))["elements"]
    pts = [(p["lon"], p["lat"]) for e in dados if e["type"] == "way" for p in e["geometry"]]
    proj = Projecao(pts)
    cidades = {e["tags"]["name"]: proj.para_tile(e["lon"], e["lat"])
               for e in dados if e["type"] == "node" and "name" in e.get("tags", {})}
    dutra = cadeia_da_dutra(dados, proj)
    a = dutra.project(Point(cidades["Piraí"]))
    b = dutra.project(Point(cidades["Volta Redonda"]))
    trecho = substring(dutra, min(a, b), max(a, b))
    if a > b:
        trecho = LineString(list(trecho.coords)[::-1])   # sempre de Piraí para VR
    # Pista dupla suavizada (peça do gerador: scripts/gerador/rodovia.py).
    trecho = rodovia.suavizar(trecho)
    feats, rodovias = rodovia.pista_dupla(trecho, "Rodovia Presidente Dutra (BR-116)", proj, feature)

    def ponta(linha, inicio):
        cs = list(linha.coords)
        p, q = (cs[0], cs[1]) if inicio else (cs[-1], cs[-2])
        d = math.hypot(p[0] - q[0], p[1] - q[1])
        return p, ((p[0] - q[0]) / d, (p[1] - q[1]) / d)

    resumo = {"comprimento_tiles": round(trecho.length),
              "comprimento_real_km": round(trecho.length * 15 / 1000, 1)}
    for nome, inicio, completa in (("A_Pirai", True, True), ("B_VoltaRedonda", False, False)):
        p, u = ponta(trecho, inicio)
        cx, cy = round(p[0] + u[0] * AFASTAMENTO_VILA), round(p[1] + u[1] * AFASTAMENTO_VILA)
        fs, ruas, r = vila(cx, cy, completa, proj, 1 if completa else 2)
        # Acesso: da ponta da rodovia até a ponta de rua da vila mais próxima.
        fim = min((Point(c) for g in ruas for c in (g.coords[0], g.coords[-1])),
                  key=lambda c: c.distance(Point(p)))
        feats.append(feature("primary", LineString([p, (fim.x, fim.y)]), proj,
                             {"name": f"Acesso {nome}"}))
        feats += fs
        resumo[nome] = r

    # Caixa total com folga (coordenadas falsas, 1 m por tile).
    tudo = [c for f in feats for c in (f["geometry"]["coordinates"] if f["geometry"]["type"] == "LineString"
                                       else f["geometry"]["coordinates"][0] if f["geometry"]["type"] == "Polygon"
                                       else [f["geometry"]["coordinates"]])]
    lons = [c[0] for c in tudo]
    lats = [c[1] for c in tudo]
    folga_lon = 40 * METROS_FALSOS / proj.mx
    folga_lat = 40 * METROS_FALSOS / proj.my
    cfg = {
        "mapName": "rsb_t8d_dutra",
        "title": "RSB Teste T8d - Dutra",
        "modId": "rsb_t8d_dutra",
        "south": min(lats) - folga_lat, "west": min(lons) - folga_lon,
        "north": max(lats) + folga_lat, "east": max(lons) + folga_lon,
        "metersPerTile": METROS_FALSOS,
        "drawnOnly": True,
        "standalone": True,
        "settings": {"align_streets": 0, "straight_roads": 0},
        "extraTags": ["shop", "amenity", "lanes"],
        "kitLojas": "kits/lojas",
        "sketch": {"type": "FeatureCollection", "features": feats},
        # Para as zonas de estrada e de mata (zonas_historias.py via pipeline).
        "rodovias": rodovias,
        "zonasHistorias": {"navAuto": False, "engarrafamento": False, "historias": [],
                           "matasRurais": True},
    }
    with open(saida, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False)
    print(json.dumps(resumo, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
