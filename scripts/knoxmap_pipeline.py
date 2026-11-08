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
