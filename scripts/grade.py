"""Grade do Real Sudeste Brasil (D-02): latitude/longitude <-> tile do jogo.

Projecao: SIRGAS 2000, policonica (a do IBGE) com o meridiano central em 45 W,
no meio do Sudeste (escolha do usuario em 08/11/2026). Norte para cima.
Escala: 1 tile = 15 m (D-01). Celula do jogo (B42) = 256 x 256 tiles.

    tile_x = floor((E - E0) / 15) + OFFSET_X
    tile_y = floor((N0 - N) / 15) + OFFSET_Y
    celula = tile // 256

Uso (Python do .venv do KnoxMap, que tem o pyproj):
    python scripts/grade.py -22.9068 -43.1729        # lat lon -> tile e celula
    python scripts/grade.py --tile 59000 52000        # tile -> lat lon
    python scripts/grade.py --conferir                # pontos de referencia

NAO mude estes numeros depois que o mapa comecar a ser gerado: tudo muda de lugar.
"""
import argparse
import math

from pyproj import Transformer

# --- Parametros fixos da grade (gravados tambem no plano, secao 6) ---
PROJ = "+proj=poly +lat_0=0 +lon_0=-45 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs"
GEO = "EPSG:4674"          # SIRGAS 2000 geografico (na pratica igual ao WGS84 do OSM)
METROS_POR_TILE = 15.0
E0 = -860_000.0            # 26 km a oeste do ponto mais a oeste de SP (Pontal)
N0 = -1_550_000.0          # 24 km ao norte do ponto mais ao norte de MG
OFFSET_X = 0
OFFSET_Y = 0
TILES_POR_CELULA = 256      # celula da B42
TILES_POR_CELULA_KNOXMAP = 300  # unidade de posicao do KnoxMap (K16), teto 400

_ida = Transformer.from_crs(GEO, PROJ, always_xy=True)
_volta = Transformer.from_crs(PROJ, GEO, always_xy=True)


def latlon_para_metros(lat, lon):
    """(lat, lon) -> (E, N) em metros na projecao da grade."""
    return _ida.transform(lon, lat)


def latlon_para_tile_real(lat, lon):
    """Posicao em tiles com fracao (para desenhar linhas sem arredondar)."""
    e, n = latlon_para_metros(lat, lon)
    return (e - E0) / METROS_POR_TILE + OFFSET_X, (N0 - n) / METROS_POR_TILE + OFFSET_Y


def latlon_para_tile(lat, lon):
    x, y = latlon_para_tile_real(lat, lon)
    return math.floor(x), math.floor(y)


def tile_para_latlon(tx, ty):
    """Canto noroeste do tile -> (lat, lon). Use tx+0.5, ty+0.5 para o centro."""
    e = (tx - OFFSET_X) * METROS_POR_TILE + E0
    n = N0 - (ty - OFFSET_Y) * METROS_POR_TILE
    lon, lat = _volta.transform(e, n)
    return lat, lon


def celula(tx, ty):
    return tx // TILES_POR_CELULA, ty // TILES_POR_CELULA


def celula_knoxmap(tx, ty):
    """Valor para "cell": [x, y] no config do knoxmap_pipeline (K16)."""
    return tx // TILES_POR_CELULA_KNOXMAP, ty // TILES_POR_CELULA_KNOXMAP


# Pontos de referencia: extremos do Sudeste (sem as ilhas de Trindade e Martim Vaz) e capitais
REFERENCIAS = {
    "Extremo norte (MG)": (-14.2334, -44.20),
    "Extremo sul (SP, Ilha do Cardoso)": (-25.3121, -48.05),
    "Extremo oeste (SP, Pontal)": (-22.5300, -53.1101),
    "Extremo leste (ES, continente)": (-19.6500, -39.6649),
    "Rio de Janeiro (Centro)": (-22.9068, -43.1729),
    "Sao Paulo (Se)": (-23.5505, -46.6333),
    "Belo Horizonte": (-19.9167, -43.9345),
    "Vitoria": (-20.3155, -40.3128),
}


def _linha(nome, lat, lon):
    tx, ty = latlon_para_tile(lat, lon)
    cx, cy = celula(tx, ty)
    kx, ky = celula_knoxmap(tx, ty)
    return f"{nome:36s} tile {tx:6d},{ty:6d}  celula {cx:3d},{cy:3d}  KnoxMap {kx:3d},{ky:3d}"


def conferir():
    for nome, (lat, lon) in REFERENCIAS.items():
        print(_linha(nome, lat, lon))
        # ida e volta tem de dar o mesmo tile
        tx, ty = latlon_para_tile(lat, lon)
        la2, lo2 = tile_para_latlon(tx + 0.5, ty + 0.5)
        assert latlon_para_tile(la2, lo2) == (tx, ty), nome
    xs, ys = zip(*(latlon_para_tile(*p) for p in REFERENCIAS.values()))
    print(f"\nAte a celula {max(xs)//256},{max(ys)//256} (de 256); "
          f"KnoxMap ate {max(xs)//300},{max(ys)//300} (teto 400). Ida e volta: ok.")
    assert min(xs) > 0 and min(ys) > 0 and max(xs) // 300 < 400 and max(ys) // 300 < 400


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lat", nargs="?", type=float)
    ap.add_argument("lon", nargs="?", type=float)
    ap.add_argument("--tile", nargs=2, type=float, metavar=("X", "Y"))
    ap.add_argument("--conferir", action="store_true")
    a = ap.parse_args()
    if a.conferir:
        conferir()
    elif a.tile:
        lat, lon = tile_para_latlon(*a.tile)
        print(f"lat {lat:.6f}  lon {lon:.6f}")
    elif a.lat is not None and a.lon is not None:
        print(_linha("ponto", a.lat, a.lon))
    else:
        ap.print_help()
