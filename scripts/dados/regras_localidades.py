"""Aplica kits/localidades/regras_v1.json as localidades do RJ (D-22).

Saida: <saida>/localidades_rj.csv e um resumo na tela.
Uso: python -I scripts/dados/regras_localidades.py <pasta dados> <pasta saida>
"""
import collections
import csv
import json
import pathlib
import sys
import unicodedata

from shapely.geometry import Point
from shapely.ops import unary_union
from shapely.strtree import STRtree

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(AQUI.parent))
sys.path.insert(0, str(AQUI))
import grade  # noqa: E402
from leitores import ler_gpkg, ler_overpass, ler_shapefile_zip  # noqa: E402

GRAU_2KM = 2.0 / 111.0  # ~2 km em graus (suficiente para contar vizinhos)


def sem_acento(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def main(pasta_dados, pasta_saida):
    pasta_dados, pasta_saida = pathlib.Path(pasta_dados), pathlib.Path(pasta_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)
    regras = json.load(open(RAIZ / "kits/localidades/regras_v1.json", encoding="utf-8"))

    pop = {r["D1C"]: int(r["V"]) for r in json.load(open(pasta_dados / "ibge/censo2022/pop_municipios_rj.json",
                                                        encoding="utf-8"))[1:]}
    locs = ler_gpkg(pasta_dados / "ibge/localidades/BR_localidades_2022.gpkg", onde="where CD_UF='33'")
    # A capital vem duas vezes (Capital Estadual e Sede Municipal): fica uma so
    capitais = {a["CD_MUN"] for a, _ in locs if a["SCT_LOCALIDADE"] == "Capital Estadual"}
    locs = [(a, g) for a, g in locs
            if not (a["SCT_LOCALIDADE"] == "Sede Municipal" and a["CD_MUN"] in capitais)]

    # Manchas urbanas (so as de area urbanizada), juntadas em "grupos" continuos
    au = ler_shapefile_zip(pasta_dados / "ibge/areas_urbanizadas/AreasUrbanizadas2019_Brasil.zip",
                           bbox=(-45.2, -23.6, -40.6, -20.5))
    manchas = [g for a, g in au if a.get("Tipo") == "Área urbanizada"]
    grupos = list(getattr(unary_union([g.buffer(0.002) for g in manchas]), "geoms", []))  # ~200 m de tolerancia
    arvore_grupos = STRtree(grupos)

    def grupo_de(pt):
        for i in arvore_grupos.query(pt):
            if grupos[i].contains(pt):
                return int(i)
        return None

    turismo_pts = []
    tur = pasta_dados / "osm_rj/turismo.json"
    if tur.exists():
        turismo_pts = [g for t, g in ler_overpass(tur)
                       if t.get("tourism") or t.get("waterway") == "waterfall"]
    arvore_tur = STRtree(turismo_pts) if turismo_pts else None

    tipos = {sem_acento(k): v for k, v in regras["tipos_ibge"].items()}
    sede_do_grupo = {}

    def tx_ty(pt):
        return grade.latlon_para_tile_real(pt.y, pt.x)
    linhas = []
    for a, g in locs:
        pt = Point(a["LONG_LOCALIDADE"], a["LAT_LOCALIDADE"])
        ct = a["CT_LOCALIDADE"]
        gi = grupo_de(pt)
        if ct == "Cidade":
            p = pop.get(a["CD_MUN"], 0)
            cat = next(c["categoria"] for c in regras["categorias_sede"] if p >= c["pop_min"])
            if gi is not None:
                sede_do_grupo.setdefault(gi, []).append((a["NM_LOCALIDADE"], tx_ty(pt)))
        else:
            p = pop.get(a["CD_MUN"], 0)
            cat = tipos.get(sem_acento(ct), "vilarejo")
        n_tur = 0
        if arvore_tur is not None:
            n_tur = sum(1 for i in arvore_tur.query(pt.buffer(GRAU_2KM)) if turismo_pts[i].distance(pt) <= GRAU_2KM)
        tx, ty = grade.latlon_para_tile_real(pt.y, pt.x)
        linhas.append({"nome": a["NM_LOCALIDADE"], "municipio": a["NM_MUN"], "tipo_ibge": ct,
                       "categoria": cat, "pop_municipio": p, "tile_x": round(tx), "tile_y": round(ty),
                       "celula_x": int(tx) // 256, "celula_y": int(ty) // 256,
                       "grupo": gi, "n_turismo": n_tur})

    for r in linhas:
        gi = r["grupo"]
        r["dentro_de"] = ""
        r["area_urbana_jogo_tiles"] = ""
        if gi is not None:
            # area real da mancha em km2 (aprox. pela latitude) -> tiles a 1:15
            g = grupos[gi]
            km2 = g.area * (111.32 ** 2) * abs(__import__("math").cos(__import__("math").radians(g.centroid.y)))
            r["area_urbana_jogo_tiles"] = round(km2 * 1e6 / 225)
        if r["categoria"] in ("metropole", "grande", "media", "pequena"):
            pass
        elif gi is not None and gi in sede_do_grupo:
            # mancha continua com varias sedes (ex.: Rio + Baixada): fica com a sede mais proxima
            r["dentro_de"] = min(sede_do_grupo[gi], key=lambda s: (s[1][0] - r["tile_x"]) ** 2 + (s[1][1] - r["tile_y"]) ** 2)[0]
            r["categoria"] = "bairro"
        elif r["categoria"] == "so_com_mancha":
            r["categoria"] = "vilarejo" if gi is not None else "so_nome"
        sede = r["tipo_ibge"] == "Cidade"
        r["turistica"] = "sim" if r["n_turismo"] >= (5 if sede else 3) else "nao"
        del r["grupo"]

    campos = list(linhas[0].keys())
    with open(pasta_saida / "localidades_rj.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(sorted(linhas, key=lambda r: (r["municipio"], r["nome"])))

    cont = collections.Counter(r["categoria"] for r in linhas)
    print("Localidades do RJ:", len(linhas))
    for c in ["metropole", "grande", "media", "pequena", "distrito", "vilarejo", "bairro", "so_nome"]:
        print(f"  {c:10s} {cont[c]}")
    tur = [r for r in linhas if r["turistica"] == "sim" and r["categoria"] not in ("bairro", "so_nome")]
    print("Turisticas:", len(tur), "-", ", ".join(sorted(r["nome"] for r in tur))[:1500])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
