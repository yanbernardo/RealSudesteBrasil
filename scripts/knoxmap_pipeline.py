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

    install()
    return 0


if __name__ == "__main__":
    sys.exit(main())
