"""Kit de lojas (T8): plantas feitas por nós, escolhidas pelo tipo de loja.

Três partes, todas em `kits/lojas/` (dados, fáceis de trocar pelo Kit Brasil):
  plantas/*.json   desenho de cômodos de cada loja (retângulos com o tipo do cômodo)
  decoracao.json   papéis de móvel por tipo de cômodo (o catálogo do KnoxMap diz
                   qual tile é cada papel; o Kit Brasil acrescenta papéis/tiles novos)
  lojas.json       etiqueta shop= do OSM -> planta

Usado por scripts/knoxmap_pipeline.py (chave "kitLojas" no config). Rodar sempre
com o Python do .venv do KnoxMap.
"""
from __future__ import annotations

import json
from pathlib import Path


def _ler(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def aplicar_decoracao(kit: Path) -> list[str]:
    from knoxbuild import interiors as it
    from knoxbuild import layout as L
    dec = _ler(kit / "decoracao.json")
    from knoxbuild import catalog as C
    for nome, (piso, rotulo, papeis, cor_de) in dec.get("comodos", {}).items():
        L.ROOM_STYLE[nome] = (piso, rotulo, list(papeis))
        C.ROOM_COLORS[nome] = C.ROOM_COLORS[cor_de]
    for tipo, regras in dec.get("lojas", {}).items():
        it.STORES[tipo] = {**it.STORES.get(tipo, {}), **regras}
    return sorted(dec.get("comodos", {})) + sorted(dec.get("lojas", {}))


def _girar(d: dict) -> dict:
    """A mesma planta virada 180 graus (a porta passa do lado sul para o norte)."""
    g = dict(d)
    g["rooms"] = [{**r, "x": d["width"] - r["x"] - r["w"], "y": d["height"] - r["y"] - r["h"]}
                  for r in d["rooms"]]
    return g


_LADO = ["S"]


def _porta_no_lado_da_rua() -> None:
    """O desenhista do KnoxMap põe a porta sempre no lado sul (street=None).
    Aqui a porta passa a seguir `_LADO`, que mudamos a cada planta."""
    from knoxbuild import layout as L
    if getattr(L._exterior_door, "_rsb", False):
        return
    original = L._exterior_door

    def porta(plan, rng, avoid=None, street=None, entrances=None):
        return original(plan, rng, avoid=avoid, street=_LADO[0], entrances=entrances)
    porta._rsb = True
    L._exterior_door = porta


def instalar_plantas(kit: Path) -> dict[str, str]:
    """Grava as plantas como presets do KnoxMap, uma por lado da rua.

    O KnoxMap não gira prédios feitos à mão e põe a porta no lado sul; por isso
    cada planta vira duas: <nome> S (rua ao sul) e <nome> N (rua ao norte).
    Devolve "planta:lado" -> nome do preset.
    """
    import knoxpaths
    from knoxbuild import designer
    out = {}
    _porta_no_lado_da_rua()
    for arq in sorted((kit / "plantas").glob("*.json")):
        d = _ler(arq)
        for lado, plano in (("S", d), ("N", _girar(d))):
            _LADO[0] = lado
            nome = f"{d['name']} {lado}"
            designer.keep(knoxpaths.BASE_DIR, nome, {**plano, "name": nome})
            out[f"{arq.stem}:{lado}"] = nome
    return out


def _lado_da_rua(poly: list, ruas: list) -> str | None:
    """N ou S: de que lado da loja fica a rua mais próxima (None se for leste/oeste)."""
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    melhor = None
    for linha in ruas:
        for (x0, y0), (x1, y1) in zip(linha, linha[1:]):
            dx, dy = x1 - x0, y1 - y0
            t = 0 if dx == dy == 0 else max(0, min(1, ((cx - x0) * dx + (cy - y0) * dy) / (dx * dx + dy * dy)))
            px, py = x0 + t * dx, y0 + t * dy
            # graus de longitude valem menos que os de latitude (cos 23 graus)
            ex, ey = (px - cx) * 0.92, py - cy
            d = ex * ex + ey * ey
            if melhor is None or d < melhor[0]:
                melhor = (d, ex, ey)
    if melhor is None or abs(melhor[2]) < abs(melhor[1]):
        return None
    return "N" if melhor[2] > 0 else "S"


def zonas(sketch: dict, kit: Path, presets: dict[str, str]) -> list[dict]:
    """Uma zona por loja desenhada com etiqueta conhecida, nomeando a planta do lado da rua."""
    mapa = {k: v for k, v in _ler(kit / "lojas.json").items() if not k.startswith("_")}
    feats = sketch.get("features", [])
    ruas = [f["geometry"]["coordinates"] for f in feats
            if f["geometry"]["type"] == "LineString"
            and f["properties"].get("kind") in ("motorway", "primary", "secondary", "residential", "service")]
    zs = []
    for f in feats:
        p = f.get("properties", {})
        tags = p.get("tags") or {}
        shop = tags.get("shop")
        if shop not in mapa or f["geometry"]["type"] != "Polygon":
            continue
        anel = f["geometry"]["coordinates"][0]
        lado = _lado_da_rua(anel, ruas)
        planta = presets.get(f"{mapa[shop]['planta']}:{lado}") if lado else None
        print(f"  {tags.get('name', shop)}: rua ao {lado or 'leste/oeste'} -> {planta or 'gerador do KnoxMap'}", flush=True)
        if planta:
            zs.append({"name": tags.get("name", shop), "ring": anel, "settings": {}, "presets": [planta]})
    return zs
