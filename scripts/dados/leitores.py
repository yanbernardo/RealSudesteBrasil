"""Leitores simples de shapefile (.shp/.dbf), GeoPackage e JSON da Overpass.

Sem geopandas/fiona (nao estao instalados): o formato shapefile e simples e o
GeoPackage e um banco SQLite. Devolvem geometrias do shapely em lat/lon.
"""
import io
import json
import sqlite3
import struct
import zipfile

from shapely import wkb
from shapely.geometry import LineString, MultiPolygon, Point, Polygon
from shapely.ops import unary_union


# ---------- Shapefile ----------
def _ler_dbf(dados, codificacao):
    n, tam_cab, tam_reg = struct.unpack("<xxxxIHH", dados[:12])
    campos, pos = [], 32
    while dados[pos] != 0x0D:
        nome = dados[pos:pos + 11].split(b"\0")[0].decode("ascii")
        tamanho = dados[pos + 16]
        campos.append((nome, tamanho))
        pos += 32
    regs = []
    for i in range(n):
        base = tam_cab + i * tam_reg + 1  # 1 byte de "apagado"
        reg = {}
        for nome, tamanho in campos:
            reg[nome] = dados[base:base + tamanho].decode(codificacao, "replace").strip()
            base += tamanho
        regs.append(reg)
    return regs


def _anel_e_horario(pts):
    a = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        a += (x2 - x1) * (y2 + y1)
    return a > 0


def _poligono_shp(partes):
    """Shapefile: aneis em sentido horario sao cascas, anti-horario sao buracos."""
    cascas, buracos = [], []
    for p in partes:
        if len(p) < 4:
            continue
        (cascas if _anel_e_horario(p) else buracos).append(p)
    polis = [Polygon(c) for c in cascas]
    for b in buracos:
        bp = Polygon(b)
        for i, p in enumerate(polis):
            if p.contains(bp.representative_point()):
                polis[i] = Polygon(p.exterior.coords, list(p.interiors) + [bp.exterior.coords])
                break
    polis = [p if p.is_valid else p.buffer(0) for p in polis]
    return polis[0] if len(polis) == 1 else MultiPolygon([q for p in polis for q in getattr(p, "geoms", [p])])


def ler_shapefile_zip(caminho_zip, nome_base=None, bbox=None):
    """Lista de (atributos, geometria). bbox = (oeste, sul, leste, norte) filtra antes de montar."""
    z = zipfile.ZipFile(caminho_zip)
    nomes = z.namelist()
    shp = [n for n in nomes if n.lower().endswith(".shp") and (nome_base is None or nome_base in n)][0]
    base = shp[:-4]
    dbf = z.read([n for n in nomes if n.lower() == (base + ".dbf").lower()][0])
    cpg = [n for n in nomes if n.lower() == (base + ".cpg").lower()]
    codificacao = z.read(cpg[0]).decode().strip() if cpg else "utf-8"
    if codificacao.upper() in ("UTF8", "UTF-8"):
        codificacao = "utf-8"
    atributos = _ler_dbf(dbf, codificacao)
    dados = z.read(shp)
    pos, i, saida = 100, 0, []
    while pos < len(dados):
        _, tam = struct.unpack(">ii", dados[pos:pos + 8])
        conteudo = dados[pos + 8:pos + 8 + tam * 2]
        pos += 8 + tam * 2
        attrs = atributos[i]
        i += 1
        tipo = struct.unpack("<i", conteudo[:4])[0]
        if tipo == 0:
            continue
        if tipo == 1:
            x, y = struct.unpack("<dd", conteudo[4:20])
            if bbox and not (bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]):
                continue
            saida.append((attrs, Point(x, y)))
            continue
        xmin, ymin, xmax, ymax, npartes, npts = struct.unpack("<ddddii", conteudo[4:44])
        if bbox and (xmax < bbox[0] or xmin > bbox[2] or ymax < bbox[1] or ymin > bbox[3]):
            continue
        inicios = list(struct.unpack(f"<{npartes}i", conteudo[44:44 + 4 * npartes]))
        p0 = 44 + 4 * npartes
        coords = list(struct.iter_unpack("<dd", conteudo[p0:p0 + 16 * npts]))
        partes = [coords[a:b] for a, b in zip(inicios, inicios[1:] + [npts])]
        if tipo in (5, 15, 25):
            saida.append((attrs, _poligono_shp(partes)))
        elif tipo in (3, 13, 23):
            saida.append((attrs, [LineString(p) for p in partes if len(p) > 1]))
    return saida


# ---------- GeoPackage ----------
def _gpkg_para_shapely(blob):
    flags = blob[3]
    env = (flags >> 1) & 0b111
    tam_env = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[env]
    return wkb.loads(bytes(blob[8 + tam_env:]))


def ler_gpkg(caminho, tabela=None, onde=""):
    """Lista de (atributos, geometria) de uma tabela de um GeoPackage."""
    con = sqlite3.connect(f"file:{caminho}?mode=ro", uri=True)
    if tabela is None:
        tabela = con.execute("select table_name from gpkg_contents where data_type='features'").fetchone()[0]
    col_geo = con.execute("select column_name from gpkg_geometry_columns where table_name=?", (tabela,)).fetchone()[0]
    cur = con.execute(f'select * from "{tabela}" {onde}')
    nomes = [d[0] for d in cur.description]
    saida = []
    for linha in cur:
        attrs = dict(zip(nomes, linha))
        g = attrs.pop(col_geo)
        saida.append((attrs, _gpkg_para_shapely(g) if g else None))
    return saida


def tabelas_gpkg(caminho):
    con = sqlite3.connect(f"file:{caminho}?mode=ro", uri=True)
    return [r[0] for r in con.execute("select table_name from gpkg_contents")]


# ---------- Overpass ----------
def ler_overpass(caminho):
    """Lista de (tags, geometria) a partir de 'out geom' / 'out center'."""
    with open(caminho, encoding="utf-8") as f:
        elems = json.load(f)["elements"]
    saida = []
    for e in elems:
        tags = e.get("tags", {})
        if e["type"] == "node":
            saida.append((tags, Point(e["lon"], e["lat"])))
        elif "center" in e:
            saida.append((tags, Point(e["center"]["lon"], e["center"]["lat"])))
        elif e["type"] == "way" and "geometry" in e:
            pts = [(p["lon"], p["lat"]) for p in e["geometry"]]
            if len(pts) > 3 and pts[0] == pts[-1] and tags.get("natural") == "water":
                saida.append((tags, Polygon(pts)))
            elif len(pts) > 1:
                saida.append((tags, LineString(pts)))
        elif e["type"] == "relation" and "members" in e:
            from shapely.ops import polygonize
            linhas = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
                      for m in e["members"] if m.get("role") == "outer" and m.get("geometry")]
            polis = list(polygonize(unary_union(linhas))) if linhas else []
            if polis:
                saida.append((tags, unary_union(polis)))
    return saida
