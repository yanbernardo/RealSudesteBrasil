"""Gerador de cidade v1 (Etapa 2.1/2.2; D-02, D-03, D-21, D-38).

Monta um pedaço de cidade real na grade do jogo e grava o config do
`knoxmap_pipeline.py` (o KnoxMap monta, mobilia, compila e instala):

1. Chão: mar pela costa do OSM, lagoas, praias, parques; fora da mancha
   urbana do IBGE, mata (morros). Túneis viram rua comum atravessando a mata.
2. Esqueleto: as avenidas reais (OSM), da mais importante para a menor. Uma
   avenida que corre PARALELA e perto (< PARALELA tiles) de outra já aceita é
   descartada nesse trecho (a 1:15, Atlântica e N. S. de Copacabana ficam a
   ~17 tiles); onde só cruza, fica.
3. Preenchimento (D-03): ruas em grade alinhada ao grid do jogo, só dentro da
   mancha urbana, ligadas às avenidas com VÉRTICE EM COMUM. Cada cruzamento
   corta a avenida em trechos curtos, e o modo de ruas 2 do KnoxMap encaixa
   cada trecho nas curvas do jogo sem perder o traçado real (K15).
4. Quarteirões e lotes do tamanho dos prédios do jogo; tipo de lote pelo tipo
   de bairro (kit); lojas e serviços nos lugares reais (pontos do OSM).
5. Posição REAL na grade (D-02): a moldura do KnoxMap começa num múltiplo de
   300 tiles e cada ponto é convertido com o `Projector` do próprio KnoxMap.

Uso (Python do .venv do KnoxMap):
    python -I -X utf8 cidade.py <pasta KnoxMap> <pasta dados> <kit.json> <saida_config.json> <figura.png> [semente]
"""
from __future__ import annotations

import json
import math
import pathlib
import random
import sys

import numpy as np
import shapely
from shapely.geometry import LineString, MultiLineString, Point, Polygon, box, mapping
from shapely.ops import linemerge, split, unary_union
from shapely.strtree import STRtree

AQUI = pathlib.Path(__file__).resolve().parent
sys.path += [str(AQUI.parent), str(AQUI.parent / "dados")]
import grade  # noqa: E402
from leitores import ler_overpass, ler_shapefile_zip  # noqa: E402

KNOX_CELULA = 300          # unidade de posição do KnoxMap (K16)
PARALELA = 30              # tiles: avenida paralela mais perto que isto some
ANGULO_PARALELO = 30       # graus
TRECHO_MIN = 18            # tiles: pedaço de rua menor que isto some
LIGAR = 14                 # tiles: ponta de rua até esta distância de outra se liga a ela
PASSO_X, PASSO_Y = 50, 44  # grade do preenchimento (quarteirão livre de ~38 x 32)
RECUO = 6                  # da linha central da rua até o lote
FAIXA_AVENIDA = 8          # da linha central da avenida até o lote

# highway do OSM -> (ordem, tipo no KnoxMap, largura em tiles). Sem "tertiary":
# a 1:15 as ruas reais ficam 15 vezes mais juntas e picotavam os quarteirões
# (1ª rodada: 83 avenidas, 69 prédios). Secundária só se for longa.
CLASSES = {"motorway": (0, "primary", 10), "trunk": (0, "primary", 10),
           "primary": (1, "primary", 9), "secondary": (2, "secondary", 8)}
SECUNDARIA_MIN = 60        # tiles

# Áreas do OSM -> tipo no KnoxMap (paleta do sketch)
def tipo_area(t):
    if t.get("natural") in ("beach", "sand"):
        return "sand"
    if t.get("leisure") in ("park", "garden") or t.get("landuse") == "grass":
        return "park"
    if t.get("natural") in ("wood", "scrub") or t.get("landuse") == "forest":
        return "forest"
    if t.get("natural") in ("bare_rock", "cliff"):
        return "scrub"
    if t.get("landuse") == "cemetery":
        return "cemetery"
    if t.get("leisure") == "pitch":
        return "pitch"
    return None

# Serviços especiais: (tipo no KnoxMap, largura, fundo, espaçamento mínimo em tiles)
ESPECIAIS = {"school": ("school", 16, 12, 130), "college": ("school", 16, 12, 130),
             "place_of_worship": ("church", 10, 13, 120), "police": ("police", 12, 10, 220),
             "hospital": ("hospital", 14, 12, 240), "clinic": ("hospital", 12, 10, 240),
             "fire_station": ("fire", 12, 10, 320), "fuel": ("fuel", 10, 8, 170)}


def loja_de(t):
    """Etiquetas de uma loja real -> (tipo no KnoxMap, etiquetas)."""
    a, s = t.get("amenity"), t.get("shop")
    if a == "pharmacy" or s in ("chemist", "pharmacy"):
        return "shop", {"shop": "chemist"}          # K17: chemist = loja; vira cópia da Pharmahug (D-38)
    if s in ("supermarket", "convenience", "greengrocer", "kiosk"):
        return "shop", {"shop": "convenience"}      # cópia do mercado 52_8 (D-38)
    if s in ("bakery", "pastry"):
        return "shop", {"shop": "bakery"}
    if s in ("clothes", "shoes", "fashion", "boutique"):
        return "shop", {"shop": "clothes"}
    if s in ("hardware", "doityourself", "paint"):
        return "shop", {"shop": "hardware"}
    if a in ("bar", "pub"):
        return "pub", None
    if a in ("restaurant", "fast_food"):
        return "restaurant", None
    if a == "cafe":
        return "cafe", None
    if a == "bank":
        return "bank", None
    if s:
        return "shop", {"shop": s}
    return None


# ---------------------------------------------------------------- grade
def _para_tile(c):
    e, n = grade._ida.transform(c[:, 0], c[:, 1])
    return np.column_stack(((np.asarray(e) - grade.E0) / grade.METROS_POR_TILE + grade.OFFSET_X,
                            (grade.N0 - np.asarray(n)) / grade.METROS_POR_TILE + grade.OFFSET_Y))


def tiles(g):
    """lon/lat -> tiles do mundo (com fração; y cresce para o sul)."""
    return shapely.transform(g, _para_tile)


def poligonos(g):
    return [p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon" and not p.is_empty]


def linhas(g):
    out = []
    for p in getattr(g, "geoms", [g]):
        if p.geom_type == "LineString" and not p.is_empty:
            out.append(p)
        elif p.geom_type == "MultiLineString":
            out += list(p.geoms)
    return out


class Moldura:
    """Moldura do KnoxMap em múltiplos de 300 tiles e conversão exata tile -> lon/lat "falsos"."""

    def __init__(self, knox, x0, y0, x1, y1):
        sys.path.insert(0, str(knox))
        from generator.rendering.projection import Projector
        self.kx, self.ky = int(x0) // KNOX_CELULA, int(y0) // KNOX_CELULA
        self.X0, self.Y0 = self.kx * KNOX_CELULA, self.ky * KNOX_CELULA
        self.W = (int(x1) // KNOX_CELULA + 1) * KNOX_CELULA - self.X0
        self.H = (int(y1) // KNOX_CELULA + 1) * KNOX_CELULA - self.Y0
        # Lugar "falso" (1 m por tile; só o KnoxMap vê), no meridiano central da
        # zona UTM 23 (45 W): fora dele a UTM gira a caixa e a moldura cresce 300 tiles.
        lat0, lon0 = -22.95, -45.0
        dlon = (self.W / 2 - 3) / (111320 * math.cos(math.radians(lat0)))
        dlat = (self.H / 2 - 3) / 110540
        self.bbox = (lat0 - dlat, lon0 - dlon, lat0 + dlat, lon0 + dlon)   # sul, oeste, norte, leste
        self.pj = Projector.build(*self.bbox, 1.0)
        assert (self.pj.width, self.pj.height) == (self.W, self.H), (self.pj.width, self.W)

    def caixa(self):
        return box(self.X0, self.Y0, self.X0 + self.W, self.Y0 + self.H)

    def falso(self, x, y):
        lat, lon = self.pj.to_latlon(x - self.X0, y - self.Y0)
        return [round(lon, 9), round(lat, 9)]

    def feature(self, kind, geom, tags=None):
        if geom.geom_type == "LineString":
            gj = {"type": "LineString", "coordinates": [self.falso(x, y) for x, y in geom.coords]}
        elif geom.geom_type == "Polygon":
            gj = {"type": "Polygon", "coordinates": [[self.falso(x, y) for x, y in geom.exterior.coords]]}
        else:
            gj = {"type": "Point", "coordinates": self.falso(geom.x, geom.y)}
        props = {"kind": kind}
        if tags:
            props["tags"] = tags
        return {"type": "Feature", "properties": props, "geometry": gj}


# ---------------------------------------------------------------- chão
def chao(dados, kit, mold, recorte):
    caixa = mold.caixa()
    s, w, n, e = mold.bbox
    # lon/lat da moldura real (para filtrar os dados antes de projetar)
    cantos = [grade.tile_para_latlon(x, y) for x, y in ((mold.X0, mold.Y0), (mold.X0 + mold.W, mold.Y0 + mold.H))]
    (la_n, lo_w), (la_s, lo_e) = cantos
    filtro = box(lo_w - 0.05, la_s - 0.05, lo_e + 0.05, la_n + 0.05)
    costa = [tiles(g) for _, g in ler_overpass(dados / "osm_rj/costa.json") if g.intersects(filtro)]
    pecas = [caixa]
    juntas = linhas(linemerge(costa)) if costa else []
    ilhas = []
    for l in juntas:
        if l.is_ring:
            ilhas.append(Polygon(l.coords))
        else:
            pecas = [q for p in pecas for q in split(p, l).geoms]
    pontos_mar = [Point(tiles(Point(lo, la)).coords[0]) for lo, la in kit["mar"]]
    mar = unary_union([p for p in pecas if any(p.contains(m) for m in pontos_mar)])
    mar = mar.difference(unary_union(ilhas)) if ilhas else mar
    fontes = [dados / "osm_rj/lagoas.json", dados / kit["dados"] / "agua.json"]
    agua = [tiles(g.buffer(0)) for f in fontes if f.exists() for t, g in ler_overpass(f)
            if g.geom_type in ("Polygon", "MultiPolygon") and g.intersects(filtro)]
    lagoas = unary_union([g for g in agua if g.area > 200]).intersection(caixa)
    terra = caixa.difference(mar).difference(lagoas)
    return mar, lagoas, terra


def areas_osm(dados, kit, terra):
    out = {}
    for t, g in ler_overpass(dados / kit["dados"] / "areas.json"):
        k = tipo_area(t)
        if k is None:
            continue
        if g.geom_type == "LineString":
            if not g.is_ring or len(g.coords) < 4:
                continue
            g = Polygon(g.coords)
        g = tiles(g.buffer(0)).intersection(terra)
        if g.area >= 30:
            out.setdefault(k, []).append(g)
    return {k: unary_union(v) for k, v in out.items()}


# ---------------------------------------------------------------- ruas
def direcao(linha, d):
    a = linha.interpolate(max(0.0, d - 1.5))
    b = linha.interpolate(min(linha.length, d + 1.5))
    return math.atan2(b.y - a.y, b.x - a.x)


def paralela(a1, a2):
    d = abs(a1 - a2) % math.pi
    return min(d, math.pi - d) < math.radians(ANGULO_PARALELO)


def trechos_novos(cand, aceitas, arvore, limite=PARALELA):
    """Partes de `cand` que não correm paralelas e perto de uma rua aceita."""
    if not aceitas:
        return [cand]
    passo = 2.0
    n = max(2, int(cand.length / passo) + 1)
    ds = np.linspace(0, cand.length, n)
    ok = []
    for d in ds:
        p = cand.interpolate(d)
        perto = arvore.query(p.buffer(limite))
        bom = True
        for i in perto:
            L = aceitas[i]
            if L.distance(p) < limite and paralela(direcao(cand, d), direcao(L, L.project(p))):
                bom = False
                break
        ok.append(bom)
    out, ini = [], None
    for k, bom in enumerate(ok + [False]):
        if bom and ini is None:
            ini = k
        elif not bom and ini is not None:
            a, b = ds[ini], ds[min(k, n - 1) if k < n else n - 1]
            if k < n:
                b = ds[k - 1]
            if b - a >= TRECHO_MIN:
                out.append(shapely.ops.substring(cand, a, b))
            ini = None
    return out


def ligar_pontas(linha, aceitas, arvore):
    """Estica as pontas soltas de `linha` até a rua aceita mais perto (cruzamento)."""
    cs = list(linha.coords)
    for idx in (0, -1):
        p = Point(cs[idx])
        melhor = None
        for i in arvore.query(p.buffer(LIGAR)) if aceitas else []:
            d = aceitas[i].distance(p)
            if 0.01 < d < LIGAR and (melhor is None or d < melhor[0]):
                melhor = (d, i)
        if melhor:
            L = aceitas[melhor[1]]
            q = L.interpolate(L.project(p))
            if idx == 0:
                cs.insert(0, (q.x, q.y))
            else:
                cs.append((q.x, q.y))
    return LineString(cs)


def esqueleto(dados, kit, recorte, terra_urbana_ou_mata):
    vias = {}
    for t, g in ler_overpass(dados / kit["dados"] / "vias.json"):
        h = t.get("highway", "")
        if h not in CLASSES or g.geom_type != "LineString":
            continue
        nome = t.get("name") or t.get("ref") or ""
        vias.setdefault((CLASSES[h][0], h, nome), []).append(tiles(g))
    cands = []
    lim = recorte.buffer(4)
    for (ordem, h, nome), ls in vias.items():
        for l in linhas(linemerge(ls)):
            for p in linhas(l.intersection(lim)):
                p = p.simplify(1.0)
                if p.length >= (SECUNDARIA_MIN if h == "secondary" else TRECHO_MIN):
                    cands.append((ordem, -p.length, h, nome, p))
    cands.sort(key=lambda c: (c[0], c[1]))
    aceitas, info = [], []
    for ordem, _, h, nome, p in cands:
        arvore = STRtree(aceitas) if aceitas else None
        for q in trechos_novos(p, aceitas, arvore):
            q = ligar_pontas(q, aceitas, arvore) if aceitas else q
            aceitas.append(q)
            info.append((CLASSES[h][1], CLASSES[h][2], nome))
    return aceitas, info


def preenchimento(urbano, aceitas):
    """Ruas em grade alinhada ao grid, só na mancha urbana, ligadas às avenidas."""
    x0, y0, x1, y1 = urbano.bounds
    gx = [math.floor(x0 / PASSO_X) * PASSO_X + PASSO_X * i for i in range(int((x1 - x0) / PASSO_X) + 3)]
    gy = [math.floor(y0 / PASSO_Y) * PASSO_Y + PASSO_Y * j for j in range(int((y1 - y0) / PASSO_Y) + 3)]
    brutas = []
    for x in gx:   # com um vértice em cada cruzamento da grade
        brutas.append(LineString([(x, y) for y in gy]))
    for y in gy:
        brutas.append(LineString([(x, y) for x in gx]))
    novas = []
    todas = list(aceitas)
    for L in brutas:
        for p in linhas(L.intersection(urbano)):
            if p.length < TRECHO_MIN:
                continue
            arvore = STRtree(todas)
            for q in trechos_novos(p, todas, arvore, limite=12):
                q = ligar_pontas(q, todas, arvore)
                novas.append(q)
    return novas, gx, gy


def com_cruzamentos(ruas):
    """Põe o MESMO vértice nas duas ruas em cada cruzamento: o KnoxMap só vê
    cruzamento onde as linhas dividem um ponto (K15)."""
    coords = [list(l.coords) for l in ruas]
    arvore = STRtree(ruas)
    extra = [[] for _ in ruas]
    for i, a in enumerate(ruas):
        for j in arvore.query(a):
            if j <= i:
                continue
            inter = a.intersection(ruas[j])
            pts = [g for g in getattr(inter, "geoms", [inter]) if g.geom_type == "Point"]
            # pontas encostadas (ligar_pontas): a distância é ~0, mas a interseção pode falhar
            for ponta in (Point(coords[j][0]), Point(coords[j][-1])):
                if a.distance(ponta) < 1e-6:
                    pts.append(ponta)
            for ponta in (Point(coords[i][0]), Point(coords[i][-1])):
                if ruas[j].distance(ponta) < 1e-6:
                    pts.append(ponta)
            for p in pts:
                k = (round(p.x, 4), round(p.y, 4))
                extra[i].append(k)
                extra[j].append(k)
    out = []
    for l, cs, ex in zip(ruas, coords, extra):
        cs = [(round(x, 4), round(y, 4)) for x, y in cs]
        for k in set(ex):
            if k in cs:
                continue
            d = l.project(Point(k))
            acc = 0.0
            for s in range(len(cs) - 1):
                seg = math.dist(cs[s], cs[s + 1])
                if acc + seg >= d - 1e-6:
                    cs.insert(s + 1, k)
                    break
                acc += seg
            else:
                if math.dist(k, cs[0]) < math.dist(k, cs[-1]):
                    cs.insert(0, k)
                else:
                    cs.append(k)
        out.append(LineString(cs))
    return out


# ---------------------------------------------------------------- lotes
def pontos_reais(dados, kit, recorte):
    lojas, especiais = [], {}
    for t, g in ler_overpass(dados / kit["dados"] / "comercio.json"):
        if g.geom_type != "Point" or not g.within(recorte):
            continue
        p = Point(tiles(g).coords[0])
        a = t.get("amenity")
        if a in ESPECIAIS:
            especiais.setdefault(a, []).append(p)
        else:
            l = loja_de(t)
            if l:
                lojas.append((p, l))
    return lojas, especiais


def espalhar(pontos, minimo):
    escolhidos = []
    for p in pontos:
        if all(p.distance(q) >= minimo for q in escolhidos):
            escolhidos.append(p)
    return escolhidos


def lotes(livre, corredor, gx, gy, bairro_de, kit, lojas, especiais, rnd):
    """Duas fileiras de lotes por pedaço livre (frente para a rua de cima e de
    baixo), varrendo de 1 em 1 tile onde o lote não cabe."""
    frente = corredor.buffer(1.5)          # lote tem de encostar aqui (frente para a rua)
    shapely.prepare(frente)
    resumo = {"casas": 0, "predios": 0, "lojas": 0, "especiais": {}}
    out = []
    usados = set()
    arv_lojas = STRtree([p for p, _ in lojas]) if lojas else None
    # Quarteirões de verdade: o espaço livre entre as ruas (os cortados por uma
    # avenida real são irregulares e também recebem lotes).
    quarteiroes = [p for p in poligonos(livre) if p.area >= 60]
    centros = STRtree([q.centroid for q in quarteiroes])
    reservado = {}
    for a, pts in especiais.items():
        tipo, w, d, minimo = ESPECIAIS[a]
        for p in espalhar(pts, minimo):
            k = int(centros.nearest(p))
            if quarteiroes[k].centroid.distance(p) < 60:
                reservado.setdefault(k, []).append((a, p))
    for k, q in enumerate(quarteiroes):
        qx0, qy0, qx1, qy1 = q.bounds
        fundo = 16
        tipo_b = bairro_de(q.centroid)
        mix = kit["mistura"].get(tipo_b, kit["mistura"]["misto"])
        fila = list(reservado.get(k, []))
        postos = []                         # lotes já postos neste quarteirão
        # Fileiras de 2 em 2 tiles, de cima para baixo; lote "pendurado" na
        # fileira (lado 0) ou apoiado nela por baixo (lado 1). Só fica o lote que
        # cabe, encosta numa rua e não sobrepõe outro.
        for y in np.arange(qy0, qy1, 2.0):
          for lado in (0, 1):
            x = qx0
            while x < qx1:
                tags, ponto, fila_atual = None, None, None
                if fila:
                    fila_atual = fila.pop(0)
                    a, _p = fila_atual
                    kind, w, d, _ = ESPECIAIS[a]
                    d = min(d, fundo - 1)
                    andares = 1
                    if kind == "fuel":
                        kind, ponto = "shop", True
                        tags = {"name": "Posto"}
                else:
                    r = rnd.random()
                    pl, pp, _pc = mix["lote"]
                    if r < pl:
                        kind, w, d, andares = "shop", rnd.randint(8, 11), min(fundo - 1, 12), 1
                    elif r < pl + pp:
                        kind, w, d = "apartments", rnd.randint(10, 14), min(fundo - 1, 14)
                        andares = rnd.randint(*mix["andares"])
                    else:
                        kind, w, d, andares = "house", rnd.randint(7, 9), min(fundo - 2, rnd.randint(8, 10)), rnd.choice((1, 1, 2))
                if x + w > qx1 or d < 6:
                    if fila_atual is not None:
                        fila.insert(0, fila_atual)
                    break
                lote = box(x, y, x + w, y + d) if lado == 0 else box(x, y - d, x + w, y)
                # Todo lote cabe no pedaço livre, tem frente para uma rua e não sobrepõe outro.
                if not (q.contains(lote) and frente.intersects(lote)
                        and not any(lote.intersects(o) for o in postos)):
                    if fila_atual is not None:
                        fila.insert(0, fila_atual)   # o serviço tenta de novo mais adiante
                    x += 1
                    continue
                if True:
                    if kind == "shop" and not tags and arv_lojas is not None:
                        for idx in arv_lojas.query(lote.buffer(40)):
                            if idx not in usados:
                                usados.add(int(idx))
                                kind, tags = lojas[idx][1]
                                tags = dict(tags) if tags else None
                                break
                    t = dict(tags or {})
                    t["building:levels"] = str(andares)
                    out.append((kind, lote, t))
                    postos.append(lote.buffer(0.9, join_style="mitre"))   # 1 tile de vão entre lotes
                    if ponto:
                        out.append(("fuel", lote.centroid, None))
                    nome = {"house": "casas", "apartments": "predios"}.get(kind, "lojas")
                    if kind in ("school", "church", "police", "hospital", "fire") or ponto:
                        resumo["especiais"][kind if not ponto else "posto"] = resumo["especiais"].get(kind if not ponto else "posto", 0) + 1
                    else:
                        resumo[nome] += 1
                x += w + rnd.randint(1, 2)
    resumo["quarteiroes"] = len(quarteiroes)
    return out, resumo


# ---------------------------------------------------------------- figura
def figura(caminho, mold, camadas, ruas, lotes_):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (mold.W, mold.H), (70, 110, 60))
    d = ImageDraw.Draw(img)
    cor = {"mar": (90, 140, 200), "lagoa": (90, 140, 200), "urbano": (205, 195, 170), "forest": (40, 85, 40),
           "park": (110, 160, 80), "sand": (230, 215, 150), "scrub": (120, 120, 100), "cemetery": (150, 150, 130),
           "pitch": (120, 180, 90)}

    def px(cs):
        return [(x - mold.X0, y - mold.Y0) for x, y in cs]
    for nome, g in camadas:
        for p in poligonos(g):
            d.polygon(px(p.exterior.coords), fill=cor[nome])
            for b in p.interiors:
                d.polygon(px(b.coords), fill=(70, 110, 60))
    for kind, l in ruas:
        d.line(px(l.coords), fill=(60, 60, 60), width={"primary": 9, "secondary": 7}.get(kind, 5))
    cl = {"house": (200, 120, 90), "apartments": (150, 90, 160), "shop": (230, 160, 40)}
    for kind, g, _t in lotes_:
        if g.geom_type == "Polygon":
            d.rectangle([g.bounds[0] - mold.X0, g.bounds[1] - mold.Y0, g.bounds[2] - mold.X0, g.bounds[3] - mold.Y0],
                        fill=cl.get(kind, (220, 40, 40)))
    img.save(caminho)


# ---------------------------------------------------------------- principal
def main() -> int:
    knox, dados, kit_path, saida, png = (pathlib.Path(a) for a in sys.argv[1:6])
    semente = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    rnd = random.Random(semente)
    kit = json.loads(kit_path.read_text(encoding="utf-8"))
    recorte_ll = Polygon(kit["recorte"])
    recorte = tiles(recorte_ll)
    mold = Moldura(knox, *recorte.bounds)
    mar, lagoas, terra = chao(dados, kit, mold, recorte)
    areas = areas_osm(dados, kit, terra)

    urb = []
    for a, g in ler_shapefile_zip(dados / "ibge/areas_urbanizadas/AreasUrbanizadas2019_Brasil.zip",
                                  bbox=recorte_ll.bounds):
        if a.get("Tipo") in ("Área urbanizada", "Outros equipamentos urbanos") and g.intersects(recorte_ll):
            urb.append(tiles(g.buffer(0)))
    nao_construir = unary_union([areas.get(k, Polygon()) for k in ("sand", "park", "cemetery", "pitch")])
    urbano = unary_union(urb).intersection(recorte).intersection(terra).buffer(-1).buffer(1)
    mata = terra.difference(urbano).difference(areas.get("sand", Polygon()))

    aceitas, info = esqueleto(dados, kit, recorte, terra)
    infill, gx, gy = preenchimento(urbano.difference(nao_construir), aceitas)
    ruas = com_cruzamentos(aceitas + infill)
    tipos = info + [("residential", 6, "")] * len(infill)

    corredor = unary_union([l.buffer(FAIXA_AVENIDA if i < len(aceitas) else RECUO - 0.5)
                            for i, l in enumerate(ruas)])
    livre = urbano.difference(nao_construir).difference(corredor).difference(lagoas)

    nomes = {}
    for t, g in ler_overpass(dados / "osm_rj/lugares.json"):
        if t.get("place") in ("suburb", "quarter", "neighbourhood") and g.within(recorte_ll.buffer(0.01)):
            nomes[t.get("name")] = Point(tiles(g).coords[0])
    tipo_de_nome = {n: tb for tb, ns in kit["bairros"].items() for n in ns}
    arv_b = STRtree(list(nomes.values()))
    nomes_l = list(nomes)

    def bairro_de(p):
        return tipo_de_nome.get(nomes_l[int(arv_b.nearest(p))], "misto")

    lojas, especiais = pontos_reais(dados, kit, recorte_ll)
    lotes_, resumo = lotes(livre, corredor, gx, gy, bairro_de, kit, lojas, especiais, rnd)

    feats = []
    for p in poligonos(mar.simplify(0.5)):
        feats.append(mold.feature("water", p))
    for p in poligonos(lagoas.simplify(0.5)):
        feats.append(mold.feature("water", p))
    for p in poligonos(mata.simplify(1.0)):
        if p.area > 50:
            feats.append(mold.feature("forest", p))
    for k in ("sand", "park", "cemetery", "pitch", "scrub"):
        for p in poligonos(areas.get(k, Polygon()).simplify(0.5)):
            feats.append(mold.feature(k, p))
    for p in poligonos(urbano.simplify(1.0)):
        if p.area > 400:
            feats.append(mold.feature("houses_land", p))
    for (kind, largura, nome), l in zip(tipos, ruas):
        tags = {"width": str(largura)}
        if nome:
            tags["name"] = nome
        feats.append(mold.feature(kind, l, tags))
    for kind, g, t in lotes_:
        feats.append(mold.feature(kind, g, t))

    cfg = {
        "mapName": kit["mapName"], "title": kit["title"], "modId": kit["mapName"],
        "south": mold.bbox[0], "west": mold.bbox[1], "north": mold.bbox[2], "east": mold.bbox[3],
        "metersPerTile": 1.0, "drawnOnly": True, "standalone": True,
        "cell": [mold.kx, mold.ky],
        "settings": {"align_streets": 0, "straight_roads": 2, "forest_density": 0.5, "tree_density": 0.7},
        "extraTags": ["shop", "amenity", "lanes", "width", "name"],
        "kitLojas": "kits/lojas",
        "sketch": {"type": "FeatureCollection", "features": feats},
        "zonasHistorias": {"engarrafamento": False},
    }
    saida.write_text(json.dumps(cfg, ensure_ascii=False), encoding="utf-8")
    figura(png, mold, [("mar", mar), ("forest", mata), ("urbano", urbano)]
           + [(k, v) for k, v in areas.items() if k in ("sand", "park", "cemetery", "pitch", "scrub")]
           + [("lagoa", lagoas)],
           [(k, l) for (k, _w, _n), l in zip(tipos, ruas)], lotes_)
    resumo.update({"moldura_tiles": [mold.X0, mold.Y0, mold.W, mold.H], "cell_knoxmap": [mold.kx, mold.ky],
                   "avenidas": len(aceitas), "ruas_preenchimento": len(infill),
                   "lojas_reais": len(lojas), "desenhos": len(feats)})
    print(json.dumps(resumo, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
