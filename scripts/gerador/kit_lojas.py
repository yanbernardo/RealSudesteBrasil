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
    dec = {k: v for k, v in _ler(kit / "decoracao.json").items() if not k.startswith("_")}
    for tipo, regras in dec.items():
        it.STORES[tipo] = {**it.STORES.get(tipo, {}), **regras}
    return sorted(dec)


def instalar_plantas(kit: Path) -> dict[str, str]:
    """Grava as plantas como presets do KnoxMap. Devolve planta -> nome do preset."""
    import knoxpaths
    from knoxbuild import designer
    out = {}
    for arq in sorted((kit / "plantas").glob("*.json")):
        d = _ler(arq)
        designer.keep(knoxpaths.BASE_DIR, d["name"], d)
        out[arq.stem] = d["name"]
    return out


def zonas(sketch: dict, kit: Path, presets: dict[str, str]) -> list[dict]:
    """Uma zona por loja desenhada com etiqueta conhecida, nomeando a planta."""
    mapa = {k: v for k, v in _ler(kit / "lojas.json").items() if not k.startswith("_")}
    zs = []
    for f in sketch.get("features", []):
        p = f.get("properties", {})
        shop = (p.get("tags") or {}).get("shop")
        if shop not in mapa or f["geometry"]["type"] != "Polygon":
            continue
        planta = presets.get(mapa[shop]["planta"])
        if planta:
            zs.append({"name": (p.get("tags") or {}).get("name", shop),
                       "ring": f["geometry"]["coordinates"][0], "settings": {},
                       "presets": [planta]})
    return zs
