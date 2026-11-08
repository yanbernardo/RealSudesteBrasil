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
MIOLO = 22                 # tiles: quarteirão com o centro mais longe que isto da rua ganha rua no meio
MIOLO_ORLA = 16            # tiles: o mesmo, na faixa da orla (U19: ali todo espaço conta)
TOCO_BORDA = 8             # tiles: ponta de avenida mais perto que isto da borda do recorte não é toco
TOCO_RUA = 12              # tiles: pedaço de rua comum depois do último cruzamento, menor que isto, é cortado
LIGAR_TOCO = 40            # tiles: ponta solta de avenida vai até a rua mais perto, se estiver a menos disto
AVENIDA_SOLTA = 60         # tiles: avenida sem cruzamento nenhum, mas longa, fica (caminho próprio)
PARALELA_GRADE = 30       # tiles: linha da grade paralela e mais perto que isto de uma rua some

# highway do OSM -> (ordem, tipo no KnoxMap, largura em tiles). Sem "tertiary":
# a 1:15 as ruas reais ficam 15 vezes mais juntas e picotavam os quarteirões
# (1ª rodada: 83 avenidas, 69 prédios). Secundária só se for longa.
CLASSES = {"motorway": (0, "primary", 10), "trunk": (0, "primary", 10),
           "primary": (1, "primary", 10), "secondary": (2, "secondary", 8)}   # larguras pares: faixa no meio (U13)
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
ESPECIAL_ENTRE = 50        # tiles entre dois serviços especiais quaisquer


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


def praias(kit, mar):
    """U18: praia em escala de jogo. A 1:15 a areia real (100–150 m) vira 7–8
    tiles e some debaixo da avenida da orla. Para cada praia do kit, a costa
    entre 'de' e 'ate' ganha uma faixa de areia de 'largura' tiles do lado do
    mar (o mar recua). Devolve [{nome, costa, faixa_mar, sinal_terra, largura}]."""
    if not kit.get("praias"):
        return []
    costas = linhas(linemerge(linhas(mar.boundary)))
    out = []
    for pr in kit["praias"]:
        a = Point(tiles(Point(*pr["de"])).coords[0])
        b = Point(tiles(Point(*pr["ate"])).coords[0])
        L = min(costas, key=lambda l: l.distance(a) + l.distance(b))
        da, db = sorted((L.project(a), L.project(b)))
        S = shapely.ops.substring(L, da, db)
        if L.is_ring and L.length - S.length < S.length:      # o outro arco é o mais curto
            S = linemerge([shapely.ops.substring(L, db, L.length), shapely.ops.substring(L, 0, da)])
        larg = float(pr.get("largura", 22))
        esq, dir_ = S.buffer(larg, single_sided=True), S.buffer(-larg, single_sided=True)
        if esq.intersection(mar).area >= dir_.intersection(mar).area:
            faixa, sinal_terra = esq.intersection(mar), -1
        else:
            faixa, sinal_terra = dir_.intersection(mar), 1
        out.append({"nome": pr["nome"], "costa": S, "faixa_mar": faixa, "sinal_terra": sinal_terra,
                    "largura": larg, "ruas_orla": pr.get("ruas_orla")})
    return out


def ruas_da_orla(praias_, urbano):
    """U19: faixa da cidade atrás de uma praia com `"ruas_orla"` no kit. Devolve
    ({"v"|"h": área onde essa família de ruas da grade some}, [áreas da orla]).
    A família que fica é a que atravessa a faixa (a mais perpendicular à costa):
    com uma família só, os quarteirões viram paralelogramos com dois lados retos,
    onde os prédios cabem inteiros, e o lado da praia em degraus."""
    sem, regs = {}, []
    for p in praias_:
        cfg = p.get("ruas_orla")
        if not cfg:
            continue
        S = p["costa"]
        prof = cfg.get("profundidade", 60)
        faixa = S.buffer(p["sinal_terra"] * prof, single_sided=True)
        reg = unary_union([g for g in poligonos(faixa.intersection(urbano)) if g.distance(S) < 25])
        if reg.is_empty:
            continue
        # Trecho a trecho da costa (a orla é curva: em Copacabana o Leme é quase
        # horizontal e o Posto 6 quase vertical): some a família paralela à costa ali.
        passo = cfg.get("trecho", 30)
        for d in np.arange(0, S.length, passo):
            t = shapely.ops.substring(S, d, min(S.length, d + passo))
            if t.length < 2:
                continue
            (ax, ay), (bx, by) = t.coords[0], t.coords[-1]
            fam = "v" if abs(by - ay) > abs(bx - ax) else "h"
            pedaco = reg.intersection(t.buffer(p["sinal_terra"] * (prof + 10), single_sided=True))
            if pedaco.is_empty:
                continue
            fica = "h" if fam == "v" else "v"
            if not cfg.get("so_medir"):                  # so_medir: só conta os lotes (comparação)
                sem[fam] = unary_union([sem.get(fam, Polygon()), pedaco])
                regs.append((pedaco, fica))
            else:
                regs.append((pedaco, None))
    return sem, regs


def zonas_de_praia(pr, tam=13, passo=55):
    """Retângulos 'Beach' (histórias de praia: churrasco, festa, pescaria) na
    faixa nova de areia, sem água dentro, de passo em passo ao longo da costa."""
    S, faixa = pr["costa"], pr["faixa_mar"].buffer(-1.0)
    shapely.prepare(faixa)
    out = []
    for d in np.arange(20, S.length - 20, passo):
        p, q = S.interpolate(d - 2), S.interpolate(d + 2)
        tx, ty = q.x - p.x, q.y - p.y
        n = math.hypot(tx, ty) or 1.0
        c = S.interpolate(d)
        for nx, ny in ((-ty / n, tx / n), (ty / n, -tx / n)):
            if not faixa.contains(Point(c.x + nx * 5, c.y + ny * 5)):
                continue                                # esse lado é a terra
            for k in (0, -2, 2, -4, 4):
                m = pr["largura"] / 2 + k
                x0, y0 = round(c.x + nx * m - tam / 2), round(c.y + ny * m - tam / 2)
                if faixa.contains(box(x0, y0, x0 + tam, y0 + tam)):
                    out.append(["Beach", int(x0), int(y0), tam, tam])
                    break
            break
    return out


def clareiras(mata, kit, rnd):
    """U23: a mata do KnoxMap já está no grau mais ralo (árvores esparsas em 100%
    do morro) e ainda não se vê à frente. Abre clareiras: campo aberto em
    `fracao` da mata, em manchas de `raio` tiles, mais as clareiras fixas do kit
    (ex.: o topo do Corcovado, onde fica o Cristo). Devolve a mata que sobra."""
    cfg = kit.get("clareiras")
    if not cfg or mata.is_empty:
        return mata
    r0, r1 = cfg.get("raio", [8, 18])
    alvo = cfg.get("fracao", 0.45) * mata.area
    x0, y0, x1, y1 = mata.bounds
    furos, area = [], 0.0
    for _ in range(20000):
        if area >= alvo:
            break
        p = Point(rnd.uniform(x0, x1), rnd.uniform(y0, y1))
        if not mata.contains(p):
            continue
        r = rnd.uniform(r0, r1)
        furos.append(p.buffer(r))
        area += math.pi * r * r * 0.7          # 0,7: as manchas se sobrepõem um pouco
    for x, y, r in cfg.get("fixas_tiles", []):
        furos.append(Point(x, y).buffer(r))
    return mata.difference(unary_union(furos).buffer(2).buffer(-2))


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


def preenchimento(urbano, aceitas, sem=None):
    """Ruas em grade alinhada ao grid, só na mancha urbana, ligadas às avenidas.
    `sem` = {"v": área, "h": área}: onde NÃO pôr as linhas verticais (ou
    horizontais). Numa orla inclinada (Copacabana), só a família que atravessa a
    faixa fica: a outra cortava a faixa em triângulos onde não cabe prédio (U19)."""
    x0, y0, x1, y1 = urbano.bounds
    gx = [math.floor(x0 / PASSO_X) * PASSO_X + PASSO_X * i for i in range(int((x1 - x0) / PASSO_X) + 3)]
    gy = [math.floor(y0 / PASSO_Y) * PASSO_Y + PASSO_Y * j for j in range(int((y1 - y0) / PASSO_Y) + 3)]
    sem = sem or {}
    area = {k: urbano.difference(sem[k]) if k in sem and not sem[k].is_empty else urbano for k in ("v", "h")}
    brutas = []
    for x in gx:   # com um vértice em cada cruzamento da grade
        brutas.append(("v", LineString([(x, y) for y in gy])))
    for y in gy:
        brutas.append(("h", LineString([(x, y) for x in gx])))
    novas = []
    todas = list(aceitas)
    for fam, L in brutas:
        for p in linhas(L.intersection(area[fam])):
            if p.length < TRECHO_MIN:
                continue
            arvore = STRtree(todas)
            for q in trechos_novos(p, todas, arvore, limite=PARALELA_GRADE):
                q = ligar_pontas(q, todas, arvore)
                novas.append(q)
    return novas, gx, gy


def ruas_no_miolo(area, ruas, n_avenidas, rodadas=3, orlas=()):
    """Quarteirão grande demais (o centro a mais de MIOLO tiles da rua, porque
    uma linha da grade caiu perto de uma avenida ou o quarteirão é torto) ganha
    uma rua reta no meio, ligada às ruas dos dois lados (cruzamento com vértice).
    Na orla (`orlas` = [(área, família que fica)]) o limite é MIOLO_ORLA e a rua
    nova é sempre da família que atravessa a faixa (U19: miolo vazio no Leme)."""
    novas = []
    for _ in range(rodadas):
        todas = ruas + novas
        corredor = unary_union([l.buffer(FAIXA_AVENIDA if i < n_avenidas else RECUO - 0.5)
                                for i, l in enumerate(todas)])
        arvore = STRtree(todas)
        achou = False
        for q in poligonos(area.difference(corredor)):
            na_orla = next((fam for reg, fam in orlas if reg.contains(q.representative_point())), None)
            if q.area < (500 if na_orla else 1200):
                continue
            circ = shapely.maximum_inscribed_circle(q, 1.0)
            if circ.length < (MIOLO_ORLA if na_orla else MIOLO):
                continue
            cx, cy = (round(v) for v in circ.coords[0])
            x0, y0, x1, y1 = q.bounds
            if na_orla:
                norte_sul = na_orla == "v"
            else:
                norte_sul = x1 - x0 >= y1 - y0      # largo: rua norte-sul
            if norte_sul:
                L = LineString([(cx, y0 - 20), (cx, y1 + 20)])
            else:                           # comprido: rua leste-oeste
                L = LineString([(x0 - 20, cy), (x1 + 20, cy)])
            pedacos = linhas(L.intersection(q.buffer(RECUO + 1.5)))
            if not pedacos:
                continue
            p = min(pedacos, key=lambda s: s.distance(Point(cx, cy)))
            if p.length < TRECHO_MIN:
                continue
            novas.append(ligar_pontas(p, todas, arvore))
            achou = True
        if not achou:
            break
    return novas


def ligar_tocos(aceitas, outras, terra):
    """Ponta solta de avenida (o resto dela caiu no filtro de paralelas) vai até
    a rua mais perto, até LIGAR_TOCO tiles, sem atravessar água."""
    todas = aceitas + outras
    arvore = STRtree(todas)
    seca = terra.buffer(1.0)
    shapely.prepare(seca)
    out = []
    for i, l in enumerate(aceitas):
        cs = list(l.coords)
        for idx in (0, -1):
            p = Point(cs[idx])
            if any(j != i and todas[j].distance(p) < 0.01 for j in arvore.query(p.buffer(0.5))):
                continue                                   # já encosta noutra rua
            melhor = None
            for j in arvore.query(p.buffer(LIGAR_TOCO)):
                if j == i:
                    continue
                d = todas[j].distance(p)
                if d < LIGAR_TOCO and (melhor is None or d < melhor[0]):
                    melhor = (d, int(j))
            if melhor is None:
                continue
            L = todas[melhor[1]]
            q = L.interpolate(L.project(p))
            if not seca.contains(LineString([p, q])):
                continue
            if idx == 0:
                cs.insert(0, (q.x, q.y))
            else:
                cs.append((q.x, q.y))
        out.append(LineString(cs))
    return out


LIGAR_ILHA = 150           # tiles: ilha de ruas solta (ex.: túnel pela mata, U28) liga à rede até esta distância


def ligar_ilhas(linhas, terra, recorte, relatorio):
    """Rede de ruas em pedaços soltos (U28: o túnel real passa por baixo do morro e o
    trecho que sobra na mata não encontra as outras ruas): cada pedaço pequeno ganha
    uma rua reta até o ponto mais perto da rede maior, sem cruzar água. Ponta na
    borda do recorte não conta (a rua continua fora do pedaço). Ligação provisória;
    o túnel de concreto de verdade fica para o acabamento final (plano, Etapa 5)."""
    n = len(linhas)
    arvore = STRtree(linhas)
    pai = list(range(n))

    def raiz(i):
        while pai[i] != i:
            pai[i] = pai[pai[i]]
            i = pai[i]
        return i

    for i, l in enumerate(linhas):
        for j in arvore.query(l.buffer(0.6)):
            if j != i and linhas[j].distance(l) < 0.6:
                pai[raiz(int(j))] = raiz(i)
    comps = {}
    for i in range(n):
        comps.setdefault(raiz(i), []).append(i)
    if len(comps) < 2:
        return []
    comp_len = {r: sum(linhas[i].length for i in m) for r, m in comps.items()}
    principal = max(comp_len, key=comp_len.get)
    seca = terra.buffer(1.0)
    shapely.prepare(seca)
    borda = recorte.exterior
    novas = []
    for r in sorted(comps, key=lambda r: -comp_len[r]):
        if r == principal:
            continue
        pontas = [Point(l.coords[k]) for i in comps[r] for l in [linhas[i]] for k in (0, -1)]
        pontas = [p for p in pontas if p.distance(borda) > TOCO_BORDA]
        if not pontas:
            relatorio.append(("na borda", round(comp_len[r])))
            continue
        melhor = None
        for p in pontas:
            for j in comps[principal]:
                d = linhas[j].distance(p)
                if d < LIGAR_ILHA and (melhor is None or d < melhor[0]):
                    q = linhas[j].interpolate(linhas[j].project(p))
                    if seca.contains(LineString([p, q])):
                        melhor = (d, p, q)
        if melhor is None:
            relatorio.append(("sem ligacao", round(comp_len[r])))
            continue
        _d, p, q = melhor
        novas.append(LineString([(p.x, p.y), (q.x, q.y)]))
        relatorio.append(("ligada", round(comp_len[r]), round(_d)))
        comps[principal] += comps[r]          # já faz parte da rede principal
    return novas


def aparar_tocos(ruas, tipos, n_av, recorte):
    """Avenida com ponta solta no meio da cidade (sobra do filtro de paralelas:
    o resto dela foi descartado) volta até o último cruzamento; sem cruzamento,
    some. Ponta na borda do recorte fica (a avenida continua fora do pedaço).
    Devolve (ruas, tipos, nº de avenidas, nº de avenidas mexidas)."""
    borda = recorte.exterior
    usos = {}
    for l in ruas:
        for c in l.coords:
            usos[c] = usos.get(c, 0) + 1

    def solta(c):
        return usos[c] == 1 and Point(c).distance(borda) > TOCO_BORDA

    def toco_curto(cs, ponta):
        """Índice do último cruzamento antes da ponta solta, se o pedaço solto for
        menor que TOCO_RUA; senão None (rua sem saída de verdade fica)."""
        idx = range(1, len(cs)) if ponta == 0 else range(len(cs) - 2, -1, -1)
        anterior, comp = cs[ponta], 0.0
        for j in idx:
            comp += math.dist(anterior, cs[j])
            anterior = cs[j]
            if comp >= TOCO_RUA:
                return None
            if usos[cs[j]] >= 2:
                return j
        return None

    out, tps, n_novo, mexidas = [], [], 0, 0
    for k, (l, t) in enumerate(zip(ruas, tipos)):
        if k >= n_av:
            # Rua comum: a ponta que passa poucos tiles do último cruzamento é
            # cortada nele (a rua da grade atravessava a Av. Atlântica e "vazava"
            # 5-8 tiles para o lado da praia; usuário, 08/11/2026).
            cs = list(l.coords)
            a, b = 0, len(cs) - 1
            if solta(cs[0]):
                a = toco_curto(cs, 0) or 0
            if solta(cs[-1]):
                b = toco_curto(cs, len(cs) - 1) or b
            if (a, b) != (0, len(cs) - 1):
                mexidas += 1
                if b - a < 1 or LineString(cs[a:b + 1]).length < TRECHO_MIN:
                    continue
                l = LineString(cs[a:b + 1])
            out.append(l)
            tps.append(t)
            continue
        cs = list(l.coords)
        a, b = 0, len(cs) - 1
        if solta(cs[a]):
            a = next((j for j in range(1, len(cs)) if usos[cs[j]] >= 2), None)
        if a is not None and solta(cs[b]):
            b = next((j for j in range(len(cs) - 2, -1, -1) if usos[cs[j]] >= 2), None)
        if a is None or b is None or b - a < 1:
            if l.length >= AVENIDA_SOLTA:     # caminho próprio (ex.: túnel pela mata): fica inteira
                out.append(l)
                tps.append(t)
                n_novo += 1
            else:
                mexidas += 1
            continue
        nova = LineString(cs[a:b + 1])
        if (a, b) != (0, len(cs) - 1):
            mexidas += 1
            if nova.length < TRECHO_MIN:
                continue
        out.append(nova)
        tps.append(t)
        n_novo += 1
    # as avenidas continuam na frente da lista (o corredor delas é mais largo)
    return out, tps, n_novo, mexidas


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


LADOS = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
# Lojas que viram cópia de uma loja original (D-38; kits/lojas/lojas.json):
# a cópia não gira, então só entram com a rua do lado da porta, num lote maior
# que o prédio (frente x fundo, em tiles). As outras lojas cabem em qualquer lado.
COPIAS = {"chemist": ("W", 21, 16), "pharmacy": ("W", 21, 16), "weapons": ("W", 15, 15),
          "convenience": ("S", 13, 16), "greengrocer": ("S", 13, 16)}
# Serviços especiais com cópia do mapa original (U22): tipo -> (lado da rua, frente, fundo).
# Se a cópia não couber no quarteirão, o serviço sai no tamanho do ESPECIAIS (gerador do KnoxMap).
COPIAS_ESP = {"police": ("S", 14, 16), "fire": ("S", 16, 25)}


class Quarteirao:
    """Um quarteirão em tiles inteiros: onde cabe lote (M), quais tiles têm a
    rua logo ao lado em cada direção (F) e o que já está ocupado (occ)."""

    def __init__(self, q, corredor):
        x0, y0, x1, y1 = q.bounds
        self.x0, self.y0 = math.floor(x0), math.floor(y0)
        W, H = math.ceil(x1) - self.x0, math.ceil(y1) - self.y0
        xs, ys = np.meshgrid(np.arange(W) + self.x0 + 0.5, np.arange(H) + self.y0 + 0.5)
        self.M = shapely.contains_xy(q, xs, ys)
        self.F = {}
        for k, (dx, dy) in LADOS.items():
            perto = np.zeros_like(self.M)
            for passo in (1, 2):
                perto |= shapely.contains_xy(corredor, xs + dx * passo, ys + dy * passo)
            self.F[k] = self.M & perto
        self.occ = np.zeros_like(self.M)

    def retangulo(self, lado, r, c, frente, fundo, para_tras=False):
        """Lote com a frente no tile (r, c), virado para a rua do `lado`. A frente
        cresce para a direita (N/S) ou para baixo (W/E); com `para_tras`, para o
        outro lado: numa avenida diagonal em degraus, só um dos dois cabe (U19:
        sem isso, a orla de Copacabana, que desce para a esquerda, ficava vazia)."""
        if lado in ("N", "S"):
            r0 = r if lado == "N" else r - fundo + 1
            return r0, (c - frente + 1 if para_tras else c), fundo, frente
        c0 = c if lado == "W" else c - fundo + 1
        return (r - frente + 1 if para_tras else r), c0, frente, fundo

    def encaixe(self, lado, r, c, frente, fundo):
        """O retângulo que cabe com a frente no tile (r, c), ou None."""
        for tras in (False, True):
            ret = self.retangulo(lado, r, c, frente, fundo, tras)
            if self.cabe(lado, *ret):
                return ret
        return None

    def cabe(self, lado, r0, c0, h, w):
        if r0 < 0 or c0 < 0 or r0 + h > self.M.shape[0] or c0 + w > self.M.shape[1]:
            return False
        if not self.M[r0:r0 + h, c0:c0 + w].all() or self.occ[r0:r0 + h, c0:c0 + w].any():
            return False
        # a frente encosta na rua (numa avenida diagonal, só a quina do lote
        # encosta: os lotes ficam em degraus, sempre alinhados ao grid, U2)
        if lado == "N":
            linha = self.F["N"][r0, c0:c0 + w]
        elif lado == "S":
            linha = self.F["S"][r0 + h - 1, c0:c0 + w]
        elif lado == "W":
            linha = self.F["W"][r0:r0 + h, c0]
        else:
            linha = self.F["E"][r0:r0 + h, c0 + w - 1]
        return bool(linha.any())

    def ocupar(self, r0, c0, h, w, vao=1):
        self.occ[max(0, r0 - vao):r0 + h + vao, max(0, c0 - vao):c0 + w + vao] = True

    def caixa(self, r0, c0, h, w):
        return box(self.x0 + c0, self.y0 + r0, self.x0 + c0 + w, self.y0 + r0 + h)

    def frentes(self, lado):
        """Tiles de frente para a rua do `lado`, na ordem em que os lotes se encaixam."""
        rs, cs = np.nonzero(self.F[lado])
        if lado == "N":
            ordem = np.lexsort((cs, rs))
        elif lado == "S":
            ordem = np.lexsort((cs, -rs))
        elif lado == "W":
            ordem = np.lexsort((rs, cs))
        else:
            ordem = np.lexsort((rs, -cs))
        return [(int(rs[i]), int(cs[i])) for i in ordem]


def lotes(livre, corredor, ruas, bairro_de, kit, lojas, especiais, rnd):
    """Lotes encostados nas ruas, contornando cada quarteirão (frente para a rua
    de cima, de baixo e dos lados), com 1 tile de vão entre eles; o miolo fica
    de quintal. Serviços especiais primeiro, perto do lugar real."""
    shapely.prepare(corredor)
    arv_ruas = STRtree(ruas)
    resumo = {"casas": 0, "predios": 0, "lojas": 0, "especiais": {}, "copias": {}}
    out = []
    usados = set()
    arv_lojas = STRtree([p for p, _ in lojas]) if lojas else None
    quarteiroes = [p for p in poligonos(livre) if p.area >= 60]
    Q = [Quarteirao(q, corredor) for q in quarteiroes]
    centros = STRtree([q.centroid for q in quarteiroes])

    def rua_mais_perto(lote):
        """Lado da rua mais próxima do centro do lote (é o que o kit de lojas usa)."""
        c = lote.centroid
        L = ruas[int(arv_ruas.nearest(c))]
        p = L.interpolate(L.project(c))
        dx, dy = p.x - c.x, p.y - c.y
        if abs(dy) >= abs(dx):
            return "N" if dy < 0 else "S"
        return "W" if dx < 0 else "E"

    def registrar(kind, lote, tags, andares, chave):
        t = dict(tags or {})
        t["building:levels"] = str(andares)
        out.append((kind, lote, t))
        if chave == "posto":
            out.append(("fuel", lote.centroid, None))
        if chave in ("casas", "predios", "lojas"):
            resumo[chave] += 1
        else:
            resumo["especiais"][chave] = resumo["especiais"].get(chave, 0) + 1

    # 1) Serviços especiais, no quarteirão mais perto do ponto real. Mesmo tipo
    #    (escola e faculdade, hospital e clínica) conta junto, e dois serviços
    #    quaisquer ficam a ESPECIAL_ENTRE tiles: em Copacabana, hospital, delegacia
    #    e igreja caíam no mesmo quarteirão da orla e tiravam o lugar dos prédios (U19).
    por_tipo = {}
    for a, pts in especiais.items():
        por_tipo.setdefault(ESPECIAIS[a], []).extend(pts)
    postos_esp = []
    prioridade = ["police", "hospital", "fire", "fuel", "school", "church"]   # o mais raro e útil primeiro
    for (tipo, w, d, minimo), pts in sorted(por_tipo.items(), key=lambda kv: prioridade.index(kv[0][0])):
        for p in espalhar(pts, minimo):
            if any(p.distance(q) < ESPECIAL_ENTRE for q in postos_esp):
                continue
            postos_esp.append(p)
            feito = False
            for k in sorted(centros.query(p.buffer(80)), key=lambda k: quarteiroes[k].distance(p)):
                B = Q[k]
                cand = [(math.dist((B.x0 + c, B.y0 + r), (p.x, p.y)), lado, r, c)
                        for lado in LADOS for r, c in B.frentes(lado)]
                # 1ª volta: a cópia do mapa original (só com a rua do lado da frente dela);
                # 2ª volta: o tamanho comum do ESPECIAIS (gerador do KnoxMap)
                voltas = [COPIAS_ESP[tipo]] if tipo in COPIAS_ESP else []
                for copia in voltas + [None]:
                    for _d, lado, r, c in sorted(cand):
                        if copia:
                            if copia[0] != lado:
                                continue
                            ret = B.encaixe(lado, r, c, copia[1], copia[2])
                            if ret and rua_mais_perto(B.caixa(*ret)) != lado:
                                ret = None        # K32: a cópia só vale se esta rua for a mais perto
                        else:
                            ret = B.encaixe(lado, r, c, w, d)
                        if ret:
                            B.ocupar(*ret)
                            lote = B.caixa(*ret)
                            if tipo == "fuel":
                                registrar("shop", lote, {"name": "Posto"}, 1, "posto")
                            else:
                                registrar(tipo, lote, {"rsb_copia": tipo} if copia else None, 1, tipo)
                            if copia:
                                resumo["copias"][tipo] = resumo["copias"].get(tipo, 0) + 1
                            feito = True
                            break
                    if feito:
                        break
                if feito:
                    break

    # 2) O resto, em duas passadas por quarteirão (U19): primeiro só lojas e
    #    prédios, pela mistura do bairro (o lote grande raramente cabe no primeiro
    #    tile tentado, e a casa pegava o lugar); depois as casas no que sobrou.
    for k, (q, B) in enumerate(zip(quarteiroes, Q)):
        mix = kit["mistura"].get(bairro_de(q.centroid), kit["mistura"]["misto"])
        pl, pp, _pc = mix["lote"]
        # Cota da 1ª passada: lotes que cabem no quarteirão (tiles de frente,
        # que vêm em 2 fileiras e contam a quina duas vezes) x mistura.
        n_est = sum(int(B.F[l].sum()) for l in LADOS) / 2 / 18   # calibrado no Rio piloto
        cota = {"loja": round(pl * n_est), "predio": round(pp * n_est)}
        for passada, lado in [(1, l) for l in ("N", "S", "W", "E")] + [(2, l) for l in ("N", "S", "W", "E")]:
            for r, c in B.frentes(lado):
                if B.occ[r, c]:
                    continue
                x = rnd.random() if passada == 1 else 1.0
                if passada == 1 and (x >= pl + pp or cota["loja" if x < pl else "predio"] <= 0):
                    continue                      # este tile fica para as casas
                tentativas = []
                if x < pl and arv_lojas is not None:
                    # a loja real mais perto que caiba deste lado da rua
                    p = Point(B.x0 + c, B.y0 + r)
                    for idx in sorted(arv_lojas.query(p.buffer(40)), key=lambda i: lojas[i][0].distance(p)):
                        if idx in usados:
                            continue
                        kind, tags = lojas[idx][1]
                        shop = (tags or {}).get("shop")
                        if shop in COPIAS:
                            frente_copia, fr, fu = COPIAS[shop]
                            if frente_copia != lado:
                                continue
                            tentativas.append(("loja", int(idx), kind, tags, fr, fu, 1))
                        else:
                            # tamanho flexível: encolhe antes de dar a vez a uma casa
                            for fr, fu in ((rnd.randint(8, 11), 12), (8, 10)):
                                tentativas.append(("loja", int(idx), kind, tags, fr, fu, 1))
                        break
                elif x < pl + pp:
                    andares = rnd.randint(*mix["andares"])
                    # tamanho do prédio por bairro (U19: na orla, prédios maiores
                    # fazem o "paredão"; o espaço não dá para muitos prédios a 1:15)
                    fr = rnd.randint(*mix.get("predio_frente", [10, 14]))
                    fu_max = mix.get("predio_fundo", 14)
                    for f, fu in ((fr, fu_max), (fr, 12), (min(fr, 14), 12), (10, 11)):
                        tentativas.append(("predio", None, "apartments", None, f, fu, andares))
                # casa (só na 2ª passada): se a sorteada não couber, a menor
                # casa (7 x 8) ainda tenta no mesmo lugar
                if passada == 2:
                    andares_casa = rnd.choice((1, 1, 2))
                    tentativas.append(("casa", None, "house", None, rnd.randint(7, 9), rnd.randint(8, 10), andares_casa))
                    tentativas.append(("casa", None, "house", None, 7, 8, andares_casa))
                for tipo, idx, kind, tags, fr, fu, andares in tentativas:
                    ret = B.encaixe(lado, r, c, fr, fu)
                    if not ret:
                        continue
                    lote = B.caixa(*ret)
                    shop = (tags or {}).get("shop")
                    if shop in COPIAS and rua_mais_perto(lote) != lado:
                        continue      # K32: a cópia só vale se esta rua for a mais perto
                    B.ocupar(*ret)
                    if tipo in cota:
                        cota[tipo] -= 1
                    if tipo == "loja":
                        usados.add(idx)
                        if shop in COPIAS:
                            resumo["copias"][shop] = resumo["copias"].get(shop, 0) + 1
                    registrar(kind, lote, tags, andares, {"loja": "lojas", "predio": "predios", "casa": "casas"}[tipo])
                    break
    resumo["quarteiroes"] = len(quarteiroes)
    por_q = [0] * len(quarteiroes)
    for kind, g, _t in out:
        if g.geom_type == "Polygon":
            por_q[int(centros.nearest(g.centroid))] += 1
    resumo["quarteiroes_sem_lote"] = sum(1 for n in por_q if n == 0)
    resumo["ocupacao"] = round(sum(g.area for _k, g, _t in out if g.geom_type == "Polygon") / livre.area, 3)
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
            # -1: o PIL pinta a última linha também, e o vão de 1 tile entre lotes sumia
            d.rectangle([g.bounds[0] - mold.X0, g.bounds[1] - mold.Y0, g.bounds[2] - mold.X0 - 1, g.bounds[3] - mold.Y0 - 1],
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
    praias_ = praias(kit, mar)
    faixas_mar = unary_union([p["faixa_mar"] for p in praias_]) if praias_ else Polygon()
    mar, terra = mar.difference(faixas_mar), terra.union(faixas_mar)       # o mar recua na praia
    areas = areas_osm(dados, kit, terra)

    urb = []
    for a, g in ler_shapefile_zip(dados / "ibge/areas_urbanizadas/AreasUrbanizadas2019_Brasil.zip",
                                  bbox=recorte_ll.bounds):
        if a.get("Tipo") in ("Área urbanizada", "Outros equipamentos urbanos") and g.intersects(recorte_ll):
            urb.append(tiles(g.buffer(0)))
    urbano = unary_union(urb).intersection(recorte).intersection(terra).buffer(-1).buffer(1)

    aceitas, info = esqueleto(dados, kit, recorte, terra)
    # Areia também do lado da terra, da costa até a avenida da orla (o resto
    # depois da avenida é cidade). A avenida e a calçada dela são desenhadas por cima.
    areia = [faixas_mar]
    for p in praias_:
        perto = p["costa"].buffer(p["sinal_terra"] * 12, single_sided=True).intersection(terra)
        orla = [l for l in aceitas if l.distance(p["costa"]) < 20]
        resto = perto.difference(unary_union([l.buffer(5) for l in orla])) if orla else perto
        areia += [g for g in poligonos(resto) if g.distance(p["costa"]) < 1.0]
    praia = unary_union(areia)
    zonas_praia = [z for p in praias_ for z in zonas_de_praia(p)]
    nao_construir = unary_union([areas.get(k, Polygon()) for k in ("sand", "park", "cemetery", "pitch")]
                                + [praia])
    mata = terra.difference(urbano).difference(areas.get("sand", Polygon())).difference(praia)
    mata = clareiras(mata, kit, random.Random(semente + 7))
    area_urb = urbano.difference(nao_construir)
    sem_familia, orla_regs = ruas_da_orla(praias_, urbano)
    infill, gx, gy = preenchimento(area_urb, aceitas, sem_familia)
    miolo = ruas_no_miolo(area_urb.difference(lagoas), aceitas + infill, len(aceitas), orlas=orla_regs)
    infill += miolo
    aceitas = ligar_tocos(aceitas, infill, terra)
    relatorio_ilhas = []
    ilhas = ligar_ilhas(aceitas + infill, terra, recorte, relatorio_ilhas)
    infill += ilhas
    print("ilhas de ruas:", relatorio_ilhas, flush=True)
    ruas = com_cruzamentos(aceitas + infill)
    tipos = info + [("residential", 6, "")] * len(infill)
    ruas, tipos, n_av, tocos = aparar_tocos(ruas, tipos, len(aceitas), recorte)
    resto_ilhas = []
    ligar_ilhas(ruas, terra, recorte, resto_ilhas)       # só para contar: o que ainda está solto depois de aparar
    print("ilhas depois de aparar:", resto_ilhas, flush=True)

    corredor = unary_union([l.buffer(FAIXA_AVENIDA if i < n_av else RECUO - 0.5)
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
    lotes_, resumo = lotes(livre, corredor, ruas, bairro_de, kit, lojas, especiais, rnd)

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
    for p in poligonos(praia.simplify(0.5)):
        if p.area > 20:
            feats.append(mold.feature("sand", p))
    for p in poligonos(urbano.difference(praia).simplify(1.0)):
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
        # spawn_density = teto de zumbis por pedaço do mapa (P19: o máximo do
        # centro de Louisville no jogo original; medido em 08/11/2026 = 7)
        # max_levels: o KnoxMap corta qualquer prédio em 6 andares se não disser (U19)
        # mata mais rala (U9: usuário achou densa de novo no Rio piloto; antes 0.5 / 0.7)
        "settings": {"align_streets": 0, "straight_roads": 2, "forest_density": 0.3, "tree_density": 0.45,
                     "spawn_density": int(kit.get("teto_zumbis", 7)),
                     "max_levels": int(kit.get("andares_max", 6))},
        "extraTags": ["shop", "amenity", "lanes", "width", "name", "rsb_copia"],
        "kitLojas": "kits/lojas",
        "sketch": {"type": "FeatureCollection", "features": feats},
        # Praia: zonas "Beach" fixas na areia (U18); mata e lago, escolhidas pelo script
        # vagasRua: vagas de carro no meio-fio (K11: o KnoxMap só cria ~120 na cidade toda)
        "zonasHistorias": {"engarrafamento": False, "areasFixas": zonas_praia, "vagasRua": True,
                           "historias": [["Forest", 16, 16, 6], ["Lake", 14, 14, 1]]},
        "centrarFaixas": True,          # U13 (scripts/gerador/faixas.py)
        "limparOrla": True,             # U25 (scripts/gerador/limpar_orla.py)
    }
    saida.write_text(json.dumps(cfg, ensure_ascii=False), encoding="utf-8")
    figura(png, mold, [("mar", mar), ("forest", mata), ("urbano", urbano)]
           + [(k, v) for k, v in areas.items() if k in ("sand", "park", "cemetery", "pitch", "scrub")]
           + [("sand", praia), ("lagoa", lagoas)],
           [(k, l) for (k, _w, _n), l in zip(tipos, ruas)], lotes_)
    resumo.update({"moldura_tiles": [mold.X0, mold.Y0, mold.W, mold.H], "cell_knoxmap": [mold.kx, mold.ky],
                   "avenidas": n_av, "tocos_aparados": tocos, "ruas_preenchimento": len(infill), "ruas_miolo": len(miolo),
                   "lojas_reais": len(lojas), "desenhos": len(feats),
                   "praias": [{"nome": p["nome"], "costa_tiles": round(p["costa"].length),
                               "areia_nova_tiles2": round(p["faixa_mar"].area)} for p in praias_],
                   "zonas_praia": len(zonas_praia),
                   "lotes_orla": {k: sum(1 for kind, g, _t in lotes_ if g.geom_type == "Polygon"
                                         and kind == k and any(r.contains(g.centroid) for r, _f in orla_regs))
                                  for k in ("apartments", "house", "shop")}})
    print(json.dumps(resumo, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
