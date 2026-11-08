"""Roda o caminho completo do KnoxMap sem abrir a janela (Etapa 0.2, T1/T7).

Usa o próprio servidor do KnoxMap por dentro (Flask test_client), na mesma
ordem da janela: gerar mapa -> prédios -> compilar -> instalar.

Uso (rodar com o Python do .venv do KnoxMap):
    .venv\\Scripts\\python -I <este arquivo> <pasta do KnoxMap> <config.json>

O config.json tem: mapName, title, modId, south, west, north, east,
metersPerTile e, opcionalmente, settings, sketch e drawnOnly (T7).
"""
from __future__ import annotations

import json
import os
import sys
import time


def main() -> int:
    knox, cfg_path = sys.argv[1], sys.argv[2]
    with open(cfg_path, encoding="utf-8") as fh:
        cfg = json.load(fh)
    os.chdir(knox)
    sys.path.insert(0, knox)
    from app import app  # noqa: E402

    client = app.test_client()
    name = cfg["mapName"]

    # Etiquetas extras permitidas nos desenhos (ex.: "shop", "amenity" para o
    # tipo de loja). O KnoxMap só deixa passar as da lista EXTRA_TAGS; aqui, no
    # nosso próprio script, a lista é ampliada sem mexer nos arquivos dele.
    if cfg.get("extraTags"):
        from generator import sketch as _sk
        _sk.EXTRA_TAGS.update(cfg["extraTags"])

    # Decoração das lojas: troca peças de um tipo de loja (ex.: gunstore) só
    # durante esta execução, sem mexer nos arquivos do KnoxMap.
    if cfg.get("storeOverrides"):
        from knoxbuild import interiors as _it
        for _kind, _over in cfg["storeOverrides"].items():
            _it.STORES[_kind] = {**_it.STORES.get(_kind, {}), **_over}

    # D-42: legenda do mapa do jogo igual à do Knox County. A tabela do KnoxMap
    # não tem polícia nem bombeiros: caíam em "yes", que o mapa pinta como
    # residencial. No original os dois são "CommunityServices" (conferido no
    # worldmap.xml de Muldraugh: delegacias 9_54 e 7_23, quartéis 23_20 e 47_27).
    from knoxbuild import worldmap as _wm
    _wm.BUILDING_VALUE.update({"police": "CommunityServices", "fire": "CommunityServices",
                               "garage": "Industrial", "fuel": "RetailAndCommercial",
                               "hotel": "Hospitality"})
    # Farmácia é "Medical" no original (RoomTone Pharmacy), mas para o KnoxMap é uma
    # loja ("shop"), e o mapa só recebe o tipo e o contorno de cada prédio (o nome,
    # só de prédio "notável"). As farmácias são achadas pela posição: o prédio que
    # contém o centro de uma farmácia do nosso desenho vira "medical".
    def _centro(f):
        anel = f["geometry"]["coordinates"][0]
        return (sum(p[1] for p in anel) / len(anel), sum(p[0] for p in anel) / len(anel))
    _farmacias = [_centro(f) for f in cfg.get("sketch", {}).get("features", [])
                  if f.get("geometry", {}).get("type") == "Polygon"
                  and (f.get("properties", {}).get("tags") or {}).get("shop") in ("chemist", "pharmacy")]
    _escrever_mapa = _wm.write

    def _mapa_com_legenda(out_dir, map_name, proj, info, buildings):
        from shapely.geometry import Point, Polygon
        pontos = [Point(proj.to_px(lat, lon)) for lat, lon in _farmacias]
        # prédio-marco com legenda própria (ex.: hotel desenhado como "townhall" para
        # o KnoxMap não dividir): pelo nome, que ele guarda por ser prédio público
        legenda = {(f.get("properties", {}).get("tags") or {}).get("name"): (f.get("properties", {}).get("tags") or {}).get("rsb_legenda")
                   for f in cfg.get("sketch", {}).get("features", [])
                   if (f.get("properties", {}).get("tags") or {}).get("rsb_legenda")}
        novos = []
        for px, kind, nome in buildings:
            if nome in legenda:
                kind = legenda[nome]
            if kind == "shop" and len(px) >= 3 and any(Polygon(px).buffer(0.5).contains(q) for q in pontos):
                kind = "medical"
            novos.append((px, kind, nome))
        print(f"legenda: {sum(1 for _p, k, _n in novos if k == 'medical')} prédios médicos "
              f"({len(pontos)} farmácias no desenho)", flush=True)
        return _escrever_mapa(out_dir, map_name, proj, info, novos)
    _wm.write = _mapa_com_legenda

    def post(route: str, body: dict) -> dict:
        t0 = time.time()
        r = client.post(route, json=body)
        data = r.get_json(silent=True) or {}
        print(f"{route}: HTTP {r.status_code} em {time.time() - t0:.0f}s", flush=True)
        short = {k: v for k, v in data.items() if not isinstance(v, (list, dict))}
        print("  ", json.dumps(short, ensure_ascii=False)[:1500], flush=True)
        if r.status_code >= 400:
            raise SystemExit(f"falhou em {route}")
        return data

    def drawn_as_download() -> None:
        """Mapa só desenhado (drawnOnly): o mapa de papel (tecla M) do KnoxMap
        lê ruas, água e mata apenas do "download" do OSM guardado ao lado do
        mapa. Sem download, ele sai só com os prédios (problema U12). Aqui os
        nossos desenhos são gravados nesse mesmo formato."""
        if not cfg.get("drawnOnly") or "sketch" not in cfg:
            return
        from pathlib import Path
        from generator import osm, sketch
        out = Path(knox) / "output" / name
        info = json.loads((out / f"{name}_info.json").read_text(encoding="utf-8"))
        feats = sketch.features(cfg["sketch"])
        osm.save_cache(str(out / info["osm_cache"]), tuple(info["osm_bbox"]), feats)
        print(f"mapa de papel: {len(feats)} desenhos gravados como download", flush=True)

    def install() -> None:
        post("/api/install", {"mapName": name, "title": cfg.get("title", name),
                              "modId": cfg.get("modId", name)})
        zonas_historias()
        teleporte_debug()
        satelite()

    def satelite() -> None:
        """D-41: visão de satélite do mapa do jogo (pyramid.zip ao lado do worldmap.xml),
        montada dos arquivos compilados por scripts/gerador/satelite.py."""
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parent / "gerador"))
        import satelite as _sat
        out = Path(knox) / "output" / name
        info = json.loads((out / f"{name}_info.json").read_text(encoding="utf-8"))
        pl = json.loads((out / "placement.json").read_text(encoding="utf-8")) if (out / "placement.json").exists() else {}
        x0, y0 = int(pl.get("cell_x") or 0) * 300, int(pl.get("cell_y") or 0) * 300
        w, h = int(info["width_tiles"]), int(info["height_tiles"])
        mapas = list((Path.home() / "Zomboid" / "mods" / cfg.get("modId", name) / "common/media/maps").glob("*/map.info"))
        if not mapas:
            print("satélite: pasta do mapa instalado não achada", flush=True)
            return
        img = _sat.montar(knox, str(out / "lots"), x0, y0, w, h)
        os.chdir(knox)                      # montar() entra na pasta do KnoxMap; garante o mesmo lugar
        n = _sat.gravar_piramide(img, x0, y0, str(mapas[0].parent / "pyramid.zip"))
        print(f"satélite: {w} x {h} pixels, {n} quadros -> {mapas[0].parent / 'pyramid.zip'}", flush=True)

    def teleporte_debug() -> None:
        """D-39: todo mod RSB leva o menu de teleporte do modo debug (só aparece em debug).
        O Lua é gerado por scripts/gerador/teleporte_debug.py em saida/teleporte/."""
        import shutil
        from pathlib import Path
        lua = Path(__file__).resolve().parent.parent / "saida" / "teleporte" / "RSB_TeleporteDebug.lua"
        if not lua.exists():
            print("teleporte debug: Lua ainda não gerado (rode scripts/gerador/teleporte_debug.py)", flush=True)
            return
        destino = Path.home() / "Zomboid" / "mods" / cfg.get("modId", name) / "common/media/lua/client/RSB"
        destino.mkdir(parents=True, exist_ok=True)
        shutil.copy(lua, destino / lua.name)
        # U21: o contorno exato deste mapa (tiles do mundo), para o menu e a tecla F7
        # nunca mandarem para o vazio (a conta do jogo deixou passar Arraial do Cabo).
        out = Path(knox) / "output" / name
        info = json.loads((out / f"{name}_info.json").read_text(encoding="utf-8"))
        pl = json.loads((out / "placement.json").read_text(encoding="utf-8")) if (out / "placement.json").exists() else {}
        x0, y0 = int(pl.get("cell_x") or 0) * 300, int(pl.get("cell_y") or 0) * 300
        area = (x0, y0, x0 + int(info["width_tiles"]), y0 + int(info["height_tiles"]))
        (destino / "RSB_TeleporteArea.lua").write_text(
            "-- Gerado pelo knoxmap_pipeline.py: contorno do mapa deste mod (x0, y0, x1, y1 em tiles do mundo).\n"
            "RSB_Teleporte = RSB_Teleporte or {}\n"
            f"RSB_Teleporte.areas = {{ {{ {area[0]}, {area[1]}, {area[2]}, {area[3]} }} }}\n", encoding="utf-8")
        print("teleporte debug: área do mapa", area, flush=True)
        print("teleporte debug instalado:", destino / lua.name, flush=True)

    def zonas_historias() -> None:
        """T8 (eventos, D-17): o KnoxMap só grava vagas e área urbana. Aqui entram
        as zonas que ligam as histórias do jogo base: estrada ("Nav"), mata/praia/
        lago ("ZoneStory") e engarrafamento. Ver scripts/gerador/zonas_historias.py."""
        if "zonasHistorias" not in cfg:
            return
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parent / "gerador"))
        import zonas_historias as zh
        mods = Path.home() / "Zomboid" / "mods" / cfg.get("modId", name)
        objs = sorted(mods.glob("common/media/maps/*/objects.lua"))
        if not objs:
            raise SystemExit(f"objects.lua do mod não encontrado em {mods}")
        png = Path(__file__).resolve().parent.parent / "saida" / name / "zonas_historias.png"
        png.parent.mkdir(parents=True, exist_ok=True)
        zcfg = dict(cfg["zonasHistorias"] or {})
        if cfg.get("rodovias"):
            # Linha da rodovia (desenho) -> tiles do mapa, com a mesma projeção
            # que o KnoxMap usou (caixa e escala gravadas no _info.json).
            from generator.rendering.projection import Projector
            info = json.loads((Path(knox) / "output" / name / f"{name}_info.json").read_text(encoding="utf-8"))
            bb = info["bbox"]
            pj = Projector.build(bb["south"], bb["west"], bb["north"], bb["east"],
                                 info["meters_per_tile"], info.get("rotation", 0.0))
            zcfg["navPolilinhas"] = [{"pontos": [pj.to_px(lat, lon) for lon, lat in r["coords"]],
                                      "largura": r["largura"]} for r in cfg["rodovias"]]
        res = zh.aplicar(Path(knox) / "output" / name / "lots", objs[0], png, zcfg or None)
        print("zonas de história:", json.dumps(res, ensure_ascii=False), flush=True)
        print("figura:", png, flush=True)

    # "--so-instalar": reinstala um mapa já compilado (ex.: depois de fechar o jogo).
    if "--so-instalar" in sys.argv[3:]:
        install()
        return 0

    gen = {k: cfg[k] for k in ("south", "west", "north", "east", "metersPerTile")}
    gen["mapName"] = name
    for key in ("settings", "sketch", "drawnOnly", "shape"):
        if key in cfg:
            gen[key] = cfg[key]
    post("/api/generate", gen)
    drawn_as_download()   # antes dos prédios: é nessa etapa que o mapa de papel é escrito

    # U13: no modo de ruas 2 o asfalto sai 1 tile deslocado da faixa amarela;
    # a faixa volta para o meio antes dos prédios (eles releem o _veg_base.bmp).
    if cfg.get("centrarFaixas"):
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parent / "gerador"))
        import faixas
        print("faixas:", faixas.centrar(Path(knox) / "output" / name, name), flush=True)

    # U25: o acabamento de cruzamento do KnoxMap faz a rua "vazar" para a areia
    # da praia; a areia volta onde não é a pista da avenida da orla.
    if cfg.get("limparOrla"):
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parent / "gerador"))
        import limpar_orla
        print("orla:", limpar_orla.limpar(Path(knox), name, cfg), flush=True)

    # Mapa independente (D-36): o mapa fica sozinho no mundo, na célula 0,0,
    # sem o Knox County do jogo base.
    if "standalone" in cfg:
        post(f"/api/placement/{name}", {"standalone": bool(cfg["standalone"])})

    # Posição escolhida por nós (T2 parte 2): "cell": [x, y] em células de 300
    # tiles do KnoxMap, contadas a partir da origem do mundo.
    if "cell" in cfg:
        post(f"/api/placement/{name}", {"cell_x": cfg["cell"][0], "cell_y": cfg["cell"][1]})

    # Kit de lojas (T8): plantas nossas escolhidas pelo tipo de loja, com a
    # decoração em papéis de móvel (kits/lojas/). Ver scripts/gerador/kit_lojas.py.
    if cfg.get("kitLojas"):
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parent / "gerador"))
        import kit_lojas
        from knoxbuild import zones as _zones
        kit = Path(__file__).resolve().parent.parent / cfg["kitLojas"]
        print("decoração:", kit_lojas.aplicar_decoracao(kit), flush=True)
        presets = kit_lojas.instalar_plantas(kit)
        zs = kit_lojas.zonas(cfg.get("sketch", {}), kit, presets)
        _zones.save(str(Path(knox) / "output" / name), name, zs)
        # O cache de prédios do KnoxMap não percebe que a planta mudou: limpar.
        (Path(knox) / "output" / name / "build_cache.json").unlink(missing_ok=True)
        print(f"kit de lojas: {len(presets)} plantas, {len(zs)} lojas com planta própria", flush=True)

    build = {"mapName": name}
    for key in ("sketch", "drawnOnly"):
        if key in cfg:
            build[key] = cfg[key]
    post("/api/buildings", build)

    post("/api/compile", {"mapName": name})
    t0 = time.time()
    while True:
        time.sleep(5)
        st = client.get(f"/api/compile-status?map={name}").get_json() or {}
        if st.get("state") not in ("running", "stopping", "starting", "queued"):
            print(f"compilação: {json.dumps(st, ensure_ascii=False)[:1500]} "
                  f"({time.time() - t0:.0f}s)", flush=True)
            break
    if st.get("state") != "done" or st.get("error"):
        raise SystemExit("compilação falhou")

    # "--sem-instalar": gera e compila, mas não cria o mod (para comparar versões).
    if "--sem-instalar" not in sys.argv[3:]:
        install()
    return 0


if __name__ == "__main__":
    sys.exit(main())
