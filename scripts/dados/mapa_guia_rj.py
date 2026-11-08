"""Mapa-guia do RJ (Etapa 1): PNG leve, ja na grade do jogo (D-02).

Camadas: mar e terra (costa do OSM), divisa do estado e dos municipios (IBGE),
manchas urbanas (IBGE 2019), lagoas, rios e rodovias (OSM) e nomes.
Linhas da grade a cada 10 celulas do jogo, com o numero da celula na borda.

Uso (Python do .venv do KnoxMap):
    python -I scripts/dados/mapa_guia_rj.py <pasta dados> <pasta saida> [tiles_por_pixel]
Le tambem saida/localidades_rj.csv (de regras_localidades.py) se existir.
"""
import csv
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Point, Polygon, box
from shapely.ops import linemerge, split, transform, unary_union

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
sys.path.insert(0, str(AQUI))
import grade  # noqa: E402
from leitores import ler_overpass, ler_shapefile_zip  # noqa: E402

COR = {
    "mar": (170, 205, 235), "terra_fora": (226, 226, 222), "terra_rj": (244, 238, 222),
    "urbano": (232, 170, 120), "agua": (120, 170, 220), "rio": (90, 145, 210),
    "costa": (60, 100, 160), "divisa": (90, 60, 120), "municipio": (185, 170, 190),
    "motorway": (200, 30, 30), "trunk": (225, 90, 40), "primary": (235, 150, 40),
    "secondary": (200, 175, 60), "grade": (150, 150, 150), "texto": (30, 30, 30),
}


def para_tile(geom):
    def f(lon, lat, z=None):
        e, n = grade._ida.transform(lon, lat)
        return (e - grade.E0) / grade.METROS_POR_TILE, (grade.N0 - n) / grade.METROS_POR_TILE
    return transform(f, geom)


class Tela:
    def __init__(self, x0, y0, x1, y1, tpp):
        self.x0, self.y0, self.tpp = x0, y0, tpp
        self.w, self.h = int((x1 - x0) / tpp), int((y1 - y0) / tpp)
        self.img = Image.new("RGB", (self.w, self.h), COR["mar"])
        self.d = ImageDraw.Draw(self.img)

    def px(self, coords):
        return [((x - self.x0) / self.tpp, (y - self.y0) / self.tpp) for x, y in coords]

    def poligono(self, g, cor, contorno=None, fundo=None):
        for p in getattr(g, "geoms", [g]):
            if p.geom_type != "Polygon" or p.is_empty:
                continue
            self.d.polygon(self.px(p.exterior.coords), fill=cor, outline=contorno)
            for b in p.interiors:
                self.d.polygon(self.px(b.coords), fill=fundo or COR["terra_rj"])

    def linha(self, g, cor, largura=1):
        for l in getattr(g, "geoms", [g]):
            if l.geom_type == "LineString":
                self.d.line(self.px(l.coords), fill=cor, width=largura, joint="curve")
            elif l.geom_type in ("Polygon",):
                self.linha(l.exterior, cor, largura)


def fonte(tam, negrito=False):
    for nome in (("arialbd.ttf" if negrito else "arial.ttf"), "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(nome, tam)
        except OSError:
            pass
    return ImageFont.load_default()


def main(pasta_dados, pasta_saida, tpp=16):
    pasta_dados, pasta_saida = pathlib.Path(pasta_dados), pathlib.Path(pasta_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)

    munis = ler_shapefile_zip(pasta_dados / "ibge/municipios_rj/RJ_Municipios_2024.zip")
    munis_t = [(a, para_tile(g)) for a, g in munis]
    rj = unary_union([g for _, g in munis_t])
    bx0, by0, bx1, by1 = rj.bounds
    m = 1500  # folga em tiles
    x0, y0 = (int(bx0 - m) // 256) * 256, (int(by0 - m) // 256) * 256
    x1, y1 = (int(bx1 + m) // 256 + 1) * 256, (int(by1 + m) // 256 + 1) * 256
    quadro = box(x0, y0, x1, y1)
    t = Tela(x0, y0, x1, y1, tpp)
    lonlat_bbox = (-45.2, -23.6, -40.6, -20.5)

    # Terra e mar: poligonos fechados pela costa do OSM + borda do quadro
    osm = pasta_dados / "osm_rj"
    costa = [para_tile(g) for _, g in ler_overpass(osm / "costa.json")]
    # Moldura = retangulo baixado da Overpass (a costa so cruza essa borda), dentro do quadro
    import numpy as np
    lo0, la0, lo1, la1 = -44.95, -23.40, -40.95, -20.75  # um pouco menor que o baixado: a costa cruza a borda
    borda = [(lo, la0) for lo in np.linspace(lo0, lo1, 60)] + [(lo1, la) for la in np.linspace(la0, la1, 60)] + \
            [(lo, la1) for lo in np.linspace(lo1, lo0, 60)] + [(lo0, la) for la in np.linspace(la1, la0, 60)]
    moldura = para_tile(Polygon(borda)).intersection(quadro)
    t.poligono(quadro.difference(moldura), COR["terra_fora"], fundo=COR["mar"])  # fora do baixado: neutro
    costa_q = unary_union([c.intersection(moldura) for c in costa])
    # Continente: a linha aberta corta a moldura (split e robusto; polygonize falhava por arredondamento, G4)
    # Ilhas: os aneis fechados da costa
    linhas = list(getattr(linemerge(costa), "geoms", [linemerge(costa)]))
    abertas = [l for l in linhas if not l.is_ring]
    pecas = [moldura]
    for l in abertas:
        pecas = [q for p in pecas for q in split(p, l).geoms]
    mar_ref = Point(para_tile(Point(-42.5, -23.25)).coords[0])  # alto-mar, dentro da moldura
    terra = [p for p in pecas if not p.contains(mar_ref)]
    terra += [Polygon(l.coords).intersection(moldura) for l in linhas if l.is_ring]
    if len(terra) == len(pecas) + sum(l.is_ring for l in linhas):
        print("Aviso: a costa nao separou o mar; desenhando so a terra do RJ")
        terra = []
    for p in terra:  # terra de outros estados (e ilhas); o RJ vai por cima
        t.poligono(p, COR["terra_fora"], fundo=COR["mar"])
    t.poligono(rj.intersection(unary_union(terra)) if terra else rj, COR["terra_rj"], fundo=COR["mar"])

    # Manchas urbanas (IBGE 2019)
    au = pasta_dados / "ibge/areas_urbanizadas/AreasUrbanizadas2019_Brasil.zip"
    if au.exists():
        for a, g in ler_shapefile_zip(au, bbox=lonlat_bbox):
            t.poligono(para_tile(g), COR["urbano"], fundo=COR["terra_rj"])

    # Municipios e divisa
    for _, g in munis_t:
        t.linha(g.boundary, COR["municipio"], 1)

    # Agua
    for tags, g in (ler_overpass(osm / "lagoas.json") if (osm / "lagoas.json").exists() else []):
        g = para_tile(g)
        if g.area > 2000:  # tiles^2; tira acudes pequenos
            t.poligono(g, COR["agua"], fundo=COR["agua"])
    for tags, g in ler_overpass(osm / "rios.json"):
        t.linha(para_tile(g), COR["rio"], 1)
    t.linha(costa_q, COR["costa"], 1)
    t.linha(rj.boundary, COR["divisa"], 3)

    # Rodovias (as maiores por cima)
    ordem = ["secondary", "primary", "trunk", "motorway"]
    vias = {k: [] for k in ordem}
    for tags, g in (ler_overpass(osm / "rodovias.json") if (osm / "rodovias.json").exists() else []):
        tipo = tags.get("highway", "").replace("_link", "")
        if tipo in vias:
            vias[tipo].append(para_tile(g))
    for k, larg in zip(ordem, (1, 2, 3, 3)):
        if vias[k]:
            t.linha(linemerge(unary_union(vias[k])), COR[k], larg)

    # Grade: linhas a cada 10 celulas
    f_peq = fonte(13)
    for cx in range(x0 // 256, x1 // 256 + 1):
        if cx % 10 == 0:
            X = (cx * 256 - x0) / tpp
            t.d.line([(X, 0), (X, t.h)], fill=COR["grade"], width=1)
            t.d.text((X + 3, 3), str(cx), fill=COR["grade"], font=f_peq)
    for cy in range(y0 // 256, y1 // 256 + 1):
        if cy % 10 == 0:
            Y = (cy * 256 - y0) / tpp
            t.d.line([(0, Y), (t.w, Y)], fill=COR["grade"], width=1)
            t.d.text((3, Y + 3), str(cy), fill=COR["grade"], font=f_peq)

    # Localidades e nomes
    loc = pasta_saida / "localidades_rj.csv"
    if loc.exists():
        estilo = {"metropole": (9, 26, True), "grande": (7, 20, True), "media": (5, 16, True),
                  "pequena": (4, 13, False), "distrito": (3, 11, False), "vilarejo": (2, 0, False)}
        linhas = [r for r in csv.DictReader(open(loc, encoding="utf-8")) if r["categoria"] in estilo]
        ordem_cat = list(estilo)
        linhas.sort(key=lambda r: -ordem_cat.index(r["categoria"]))
        ocupado = []
        for r in linhas:
            raio, tam, neg = estilo[r["categoria"]]
            X, Y = (float(r["tile_x"]) - x0) / tpp, (float(r["tile_y"]) - y0) / tpp
            cor = (170, 30, 120) if r.get("turistica") == "sim" else COR["texto"]
            t.d.ellipse([X - raio, Y - raio, X + raio, Y + raio], fill=cor, outline=(255, 255, 255))
        for r in reversed(linhas):  # nomes: maiores primeiro, sem sobrepor
            raio, tam, neg = estilo[r["categoria"]]
            if not tam:
                continue
            f = fonte(tam, neg)
            cx, cy = (float(r["tile_x"]) - x0) / tpp, (float(r["tile_y"]) - y0) / tpp
            larg = t.d.textlength(r["nome"], font=f)
            # tenta direita, esquerda, acima e abaixo do ponto
            for X, Y in ((cx + raio + 2, cy - tam / 2), (cx - raio - 2 - larg, cy - tam / 2),
                         (cx - larg / 2, cy - raio - tam - 2), (cx - larg / 2, cy + raio + 1)):
                caixa = t.d.textbbox((X, Y), r["nome"], font=f)
                if not any(not (caixa[2] < o[0] or caixa[0] > o[2] or caixa[3] < o[1] or caixa[1] > o[3])
                           for o in ocupado):
                    ocupado.append(caixa)
                    t.d.text((X, Y), r["nome"], fill=COR["texto"], font=f, stroke_width=2, stroke_fill=(255, 255, 255))
                    break

    # Legenda
    f_leg = fonte(14)
    itens = [("Rodovia expressa", COR["motorway"]), ("Rodovia tronco", COR["trunk"]),
             ("Rodovia principal", COR["primary"]), ("Rodovia secundaria", COR["secondary"]),
             ("Rio / lagoa", COR["rio"]), ("Mancha urbana (IBGE 2019)", COR["urbano"]),
             ("Divisa do RJ", COR["divisa"]), ("Localidade turistica", (170, 30, 120))]
    lx, ly = t.w - 340, t.h - 30 - 20 * len(itens)
    t.d.rectangle([lx - 10, ly - 30, t.w - 10, t.h - 10], fill=(255, 255, 255), outline=(120, 120, 120))
    t.d.text((lx, ly - 25), f"Mapa-guia RJ  1 px = {tpp} tiles  (linhas: 10 celulas)", fill=COR["texto"], font=fonte(12, True))
    for i, (nome, cor) in enumerate(itens):
        y = ly + i * 20
        t.d.rectangle([lx, y + 3, lx + 24, y + 13], fill=cor)
        t.d.text((lx + 32, y), nome, fill=COR["texto"], font=f_leg)

    saida = pasta_saida / "mapa_guia_rj.png"
    t.img.save(saida, optimize=True)
    print(f"{saida}: {t.w} x {t.h} px; tiles {x0}-{x1} x {y0}-{y1}; celulas {x0//256}-{x1//256 - 1} x {y0//256}-{y1//256 - 1}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 16)
