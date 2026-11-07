"""Gerador simples de bairro genérico (T7c, Etapa 0.2).

Ideia (D-03): contorno REAL do bairro, encolhido na escala do mapa (1:15),
preenchido com ruas e lotes em ESCALA DE JOGO (quarteirões e casas do
tamanho dos do jogo base). O resultado é um "desenho" (GeoJSON) que o
KnoxMap monta: mobilia, compila e instala.

Truque de escala: o KnoxMap mede tudo em metros. Desenhamos o bairro num
espaço "falso" onde 1 tile do jogo = METROS_FALSOS metros, e pedimos ao
KnoxMap exatamente essa escala. Assim uma rua residencial (largura padrão do
KnoxMap ~7 m) sai com ~7 tiles, como no jogo base, enquanto o tamanho total
do bairro respeita o contorno real a 1:15.

Uso (com o Python do .venv do KnoxMap, que tem o shapely):
    python -I gerador_t7c.py <contorno.geojson> <saida_config.json> [semente]
"""
from __future__ import annotations

import json
import math
import random
import sys

from shapely.geometry import LineString, Polygon, box, mapping
from shapely.ops import unary_union

ESCALA_MAPA = 15.0        # metros reais por tile (D-01)
METROS_FALSOS = 1.0       # metros "do KnoxMap" por tile (escala de jogo)

# Medidas em tiles, inspiradas no jogo base (estimativas para o teste).
PASSO_X = 46              # distância entre ruas na direção x
PASSO_Y = 38              # distância entre ruas na direção y
AVENIDA_A_CADA = 3        # uma rua em cada N é avenida (mais larga)
RECUO_RUA = 6             # da linha central da rua até o começo do lote
FRACAO_MIN_QUARTEIRAO = 0.6  # quarteirão cortado pelo contorno: mínimo dentro


def ler_contorno(caminho: str) -> list[tuple[float, float]]:
    with open(caminho, encoding="utf-8") as fh:
        dados = json.load(fh)
    geom = dados["features"][0]["geometry"] if "features" in dados else dados
    if geom["type"] == "Polygon":
        return [tuple(p) for p in geom["coordinates"][0]]
    if geom["type"] == "MultiPolygon":  # pega o maior pedaço
        aneis = [g[0] for g in geom["coordinates"]]
        return [tuple(p) for p in max(aneis, key=len)]
    raise SystemExit(f"Contorno sem polígono: {geom['type']}")


class Projecao:
    """lon/lat reais -> tiles (1:15) -> lon/lat "falsos" para o KnoxMap."""

    def __init__(self, anel):
        self.lon0 = sum(p[0] for p in anel) / len(anel)
        self.lat0 = sum(p[1] for p in anel) / len(anel)
        self.mx = 111320.0 * math.cos(math.radians(self.lat0))
        self.my = 110540.0

    def para_tile(self, lon, lat):
        return ((lon - self.lon0) * self.mx / ESCALA_MAPA,
                (lat - self.lat0) * self.my / ESCALA_MAPA)

    def para_falso(self, x, y):
        return [round(self.lon0 + x * METROS_FALSOS / self.mx, 8),
                round(self.lat0 + y * METROS_FALSOS / self.my, 8)]


def feature(kind, geom, proj, tags=None):
    def conv(coords):
        return [proj.para_falso(x, y) for x, y in coords]
    g = mapping(geom)
    if g["type"] == "LineString":
        coords = conv(g["coordinates"])
    else:
        coords = [conv(g["coordinates"][0])]
    props = {"kind": kind}
    if tags:
        props["tags"] = tags
    return {"type": "Feature", "properties": props,
            "geometry": {"type": g["type"], "coordinates": coords}}


def gerar(anel, semente=1):
    rnd = random.Random(semente)
    proj = Projecao(anel)
    contorno = Polygon([proj.para_tile(*p) for p in anel]).buffer(0)
    minx, miny, maxx, maxy = contorno.bounds
    feats = []
    resumo = {"ruas": 0, "avenidas": 0, "casas": 0, "predios": 0, "lojas": 0,
              "quarteiroes": 0}

    # 1) Malha de ruas alinhada ao grid do jogo (norte para cima, D-02).
    xs = [minx + PASSO_X * i for i in range(int((maxx - minx) // PASSO_X) + 2)]
    ys = [miny + PASSO_Y * j for j in range(int((maxy - miny) // PASSO_Y) + 2)]
    for i, x in enumerate(xs):
        corte = contorno.intersection(LineString([(x, miny - 1), (x, maxy + 1)]))
        avenida = i % AVENIDA_A_CADA == 1
        for parte in getattr(corte, "geoms", [corte]):
            if parte.length >= 8:
                feats.append(feature("secondary" if avenida else "residential",
                                     parte, proj))
                resumo["avenidas" if avenida else "ruas"] += 1
    for j, y in enumerate(ys):
        corte = contorno.intersection(LineString([(minx - 1, y), (maxx + 1, y)]))
        avenida = j % AVENIDA_A_CADA == 1
        for parte in getattr(corte, "geoms", [corte]):
            if parte.length >= 8:
                feats.append(feature("secondary" if avenida else "residential",
                                     parte, proj))
                resumo["avenidas" if avenida else "ruas"] += 1

    # 2) Quarteirões e lotes.
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            q = box(xs[i] + RECUO_RUA, ys[j] + RECUO_RUA,
                    xs[i + 1] - RECUO_RUA, ys[j + 1] - RECUO_RUA)
            dentro = q.intersection(contorno)
            if dentro.area < FRACAO_MIN_QUARTEIRAO * q.area:
                continue
            resumo["quarteiroes"] += 1
            feats.append(feature("houses_land", dentro if dentro.geom_type == "Polygon"
                                 else q, proj))
            qx0, qy0, qx1, qy1 = q.bounds
            fundo = (qy1 - qy0) / 2  # duas fileiras de lotes, costas com costas
            for lado in (0, 1):
                x = qx0
                while True:
                    sorteio = rnd.random()
                    if sorteio < 0.12:
                        kind, w, d, andares = "shop", rnd.randint(8, 12), min(fundo - 1, 12), 1
                    elif sorteio < 0.32:
                        kind, w, d, andares = ("apartments", rnd.randint(10, 14),
                                               min(fundo - 1, 14), rnd.randint(3, 6))
                    else:
                        kind, w, d, andares = ("house", rnd.randint(7, 9),
                                               min(fundo - 3, rnd.randint(8, 10)),
                                               rnd.choice((1, 1, 2)))
                    if x + w > qx1:
                        break
                    if lado == 0:   # fileira de baixo: frente para a rua de baixo
                        lote = box(x, qy0 + 1, x + w, qy0 + 1 + d)
                    else:           # fileira de cima: frente para a rua de cima
                        lote = box(x, qy1 - 1 - d, x + w, qy1 - 1)
                    if contorno.contains(lote):
                        feats.append(feature(kind, lote, proj,
                                             {"building:levels": str(andares)}))
                        resumo[{"house": "casas", "apartments": "predios",
                                "shop": "lojas"}[kind]] += 1
                    x += w + rnd.randint(2, 4)   # vão lateral entre lotes

    # Caixa total (com folga) em coordenadas falsas, para o KnoxMap.
    folga = 20
    sw = proj.para_falso(minx - folga, miny - folga)
    ne = proj.para_falso(maxx + folga, maxy + folga)
    resumo["tamanho_tiles"] = [round(maxx - minx), round(maxy - miny)]
    resumo["area_real_km2"] = round(contorno.area * ESCALA_MAPA ** 2 / 1e6, 2)
    return feats, (sw[1], sw[0], ne[1], ne[0]), resumo


def main() -> int:
    contorno_path, saida = sys.argv[1], sys.argv[2]
    semente = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    feats, (s, w, n, e), resumo = gerar(ler_contorno(contorno_path), semente)
    cfg = {
        "mapName": "rsb_t7c_botafogo",
        "title": "RSB Teste T7c - Botafogo 1:15",
        "modId": "rsb_t7c_botafogo",
        "south": s, "west": w, "north": n, "east": e,
        "metersPerTile": METROS_FALSOS,
        "drawnOnly": True,
        "standalone": True,
        "settings": {"align_streets": 0},
        "sketch": {"type": "FeatureCollection", "features": feats},
    }
    with open(saida, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False)
    print(json.dumps(resumo, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
