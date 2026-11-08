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
    if d.get("moveis"):
        g["moveis"] = _girar_moveis(d["moveis"], d["width"], d["height"])
    g["rooms"] = [{**r, "x": d["width"] - r["x"] - r["w"], "y": d["height"] - r["y"] - r["h"]}
                  for r in d["rooms"]]
    return g


_LADO: list = [None]   # lado da porta só enquanto montamos as nossas plantas
_MOVEIS: list = [None]   # lista de móveis da planta em construção (ou None)
# O que o gerador põe sozinho e que mantemos (luz, balcão do caixa, caixa registradora).
_MANTER = {"switch", "register", "shop_counter", "shop_counter_red"}
_OPOSTO = {"N": "S", "S": "N", "E": "W", "W": "E"}


def _celulas(papel: str, x: int, y: int, lado: str) -> list[tuple[int, int]]:
    from knoxbuild import catalog as C
    pecas = C.FURNITURE.get(papel, {}).get(lado) or {}
    out = []
    for k in pecas:
        dx, dy = (int(v) for v in k.split(","))
        out.append((x + dx, y + dy))
    return out or [(x, y)]


def _girar_moveis(moveis: list, w: int, h: int) -> list:
    """A mesma lista de móveis virada 180 graus (ponto de ancoragem = canto de menor x,y)."""
    from knoxbuild import catalog as C
    out = []
    for papel, x, y, lado in moveis:
        cel = _celulas(papel, x, y, lado)
        novas = [(w - 1 - cx, h - 1 - cy) for cx, cy in cel]
        # Peças que só existem em alguns lados (ex.: corredor só W/N) ficam como estão.
        novo_lado = _OPOSTO[lado] if _OPOSTO[lado] in C.FURNITURE.get(papel, {}) else lado
        out.append([papel, min(c[0] for c in novas), min(c[1] for c in novas), novo_lado])
    return out


def _porta_no_lado_da_rua() -> None:
    """O desenhista do KnoxMap põe a porta sempre no lado sul (street=None).
    Aqui a porta passa a seguir `_LADO`, que mudamos a cada planta."""
    from knoxbuild import layout as L
    if getattr(L._exterior_door, "_rsb", False):
        return
    original = L._exterior_door

    def porta(plan, rng, avoid=None, street=None, entrances=None):
        # Só durante a montagem das NOSSAS plantas (_LADO[0] definido); nos outros
        # prédios vale o lado da rua que o KnoxMap achou (K33: antes isto valia para
        # todas as casas, e as com rua ao sul ficavam com a porta nos fundos).
        lado = _LADO[0] if _LADO[0] is not None else street
        return original(plan, rng, avoid=avoid, street=lado, entrances=entrances)
    porta._rsb = True
    L._exterior_door = porta

    # Móveis desenhados à mão: entram por último, depois de todas as limpezas do
    # KnoxMap (que tiram e movem peças), só com a luz, o balcão e o caixa do
    # gerador junto. A planta é que garante que o caminho da porta fica livre.
    limpar = L._clear_the_way

    def por_ultimo(building):
        r = limpar(building)
        if _MOVEIS[0] is not None and building.storeys:
            piso = building.storeys[0]
            # A porta é o KnoxMap quem põe; nenhum móvel nosso pode ficar nos
            # dois quadrados de uma porta (dentro e fora), senão bloqueia a passagem.
            from knoxbuild import catalog as C
            livres = set()
            for x, y, lado in piso.doors:
                # dois quadrados de cada lado da porta, para dar para passar
                livres |= ({(x, y + k) for k in (-2, -1, 0, 1)} if lado == "N"
                           else {(x + k, y) for k in (-2, -1, 0, 1)})
            meus = []
            for m in _MOVEIS[0]:
                parede = C.FURNITURE_LAYERS.get(m[0]) == "WallFurniture"
                if not parede and set(_celulas(*m)) & livres:
                    print(f"    móvel tirado da frente de uma porta: {m}", flush=True)
                    continue
                meus.append(tuple(m))
            piso.furniture = [f for f in piso.furniture if f[0] in _MANTER] + meus
        return r
    L._clear_the_way = por_ultimo


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
            # Itens de parede (cartaz, relógio) só existem virados a oeste/norte:
            # não giram com a planta; cada versão tem a sua lista ("parede": {"S": [...], "N": [...]}).
            _MOVEIS[0] = (plano.get("moveis") or []) + (d.get("parede", {}).get(lado) or [])
            nome = f"{d['name']} {lado}"
            designer.keep(knoxpaths.BASE_DIR, nome, {**plano, "name": nome})
            out[f"{arq.stem}:{lado}"] = nome
    _MOVEIS[0] = None
    _LADO[0] = None
    # Cópias de prédios do mapa original (scripts/gerador/copiar_predio_vanilla.py):
    # usadas como estão, só onde a rua fica do lado da frente delas.
    from knoxbuild import presets as P
    for shop, cfg in _ler(kit / "lojas.json").items():
        if shop.startswith("_") or "vanilla" not in cfg:
            continue
        v = cfg["vanilla"]
        nome = "RSB Vanilla " + Path(v["arquivo"]).stem
        P.save(knoxpaths.BASE_DIR, nome, (kit / v["arquivo"]).read_text(encoding="utf-8"), kind="shop")
        out[f"vanilla:{shop}:{v['frente']}"] = nome
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
    if melhor is None:
        return None
    if abs(melhor[2]) >= abs(melhor[1]):
        return "N" if melhor[2] > 0 else "S"
    return "E" if melhor[1] > 0 else "W"


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
        shop = tags.get("shop") or tags.get("rsb_copia")   # serviços especiais (polícia, bombeiros) usam rsb_copia
        if shop not in mapa or f["geometry"]["type"] != "Polygon":
            continue
        anel = f["geometry"]["coordinates"][0]
        lado = _lado_da_rua(anel, ruas)
        planta = (presets.get(f"vanilla:{shop}:{lado}")
                  or presets.get(f"{mapa[shop].get('planta')}:{lado}")) if lado else None
        print(f"  {tags.get('name', shop)}: rua ao {lado} -> {planta or 'gerador do KnoxMap'}", flush=True)
        if planta:
            zs.append({"name": tags.get("name", shop), "ring": anel, "settings": {}, "presets": [planta]})
    return zs
