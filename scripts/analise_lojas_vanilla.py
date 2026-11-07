"""Que móveis o jogo base põe em cada tipo de loja? (T8)

Lê os arquivos do mapa original (Knox County): em cada cômodo com o nome pedido,
conta os tiles de móvel e os associa aos "papéis" do KnoxMap (shop_case,
gun_locker...). Grava `catalogo/lojas_vanilla.json` e `catalogo/LOJAS_VANILLA.md`.

Uso (Python do .venv do KnoxMap):
    python -I scripts/analise_lojas_vanilla.py <pasta do KnoxMap> [cômodo ...]
"""
from __future__ import annotations

import collections
import json
import os
import sys
from pathlib import Path

KNOX = sys.argv[1]
ALVOS = set(sys.argv[2:]) or {"pharmacy", "pharmacystorage", "gunstore", "gunstorestorage"}
MAPAS = Path("C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/maps/Muldraugh, KY")
SAIDA = Path(__file__).resolve().parent.parent / "catalogo"

sys.path.insert(0, KNOX)
os.chdir(KNOX)
from knoxbuild import catalog as C  # noqa: E402
from tools.building_stats import read_header, read_squares  # noqa: E402

# Só conta móvel e objeto; piso e parede ficam de fora.
PREFIXOS = ("furniture_", "appliances_", "fixtures_", "location_", "recreational_",
            "d_plants", "lighting_indoor", "walls_decoration", "trash_", "carpentry_",
            "vegetation_indoor", "camping_", "constructedobjects_")
IGNORAR = ("floors_", "walls_exterior", "walls_interior", "walls_commercial", "roofs_",
           "fencing_", "lighting_outdoor")


def norm(tile: str) -> str:
    """location_shop_generic_01_015 -> location_shop_generic_01_15 (o jogo não usa zeros)."""
    base, _, n = tile.rpartition("_")
    return f"{base}_{int(n)}" if n.isdigit() else tile


def papel_por_tile() -> dict[str, str]:
    out = {}
    for papel, lados in C.FURNITURE.items():
        if not isinstance(lados, dict):
            continue
        for _lado, pecas in lados.items():
            if isinstance(pecas, dict):
                for tile in pecas.values():
                    out.setdefault(norm(tile), papel)
    return out


def main() -> None:
    papeis = papel_por_tile()
    comodos: dict[str, dict] = {a: {"n": 0, "tiles": collections.Counter(),
                                    "comodos_com": collections.Counter()} for a in ALVOS}
    cabecas = sorted(MAPAS.glob("*.lotheader"))
    print(f"{len(cabecas)} células no jogo base", flush=True)
    for cab in cabecas:
        nomes, lo, hi, rooms, _b = read_header(str(cab))
        if not any(r[0] in ALVOS for r in rooms):
            continue
        pack = cab.with_name("world_" + cab.name.replace(".lotheader", ".lotpack"))
        if not pack.exists():
            continue
        quadrados = read_squares(str(pack), nomes, lo, hi)
        for nome, nivel, rects in rooms:
            if nome not in ALVOS or nivel < 0:
                continue
            info = comodos[nome]
            info["n"] += 1
            vistos = set()
            for x, y, w, h in rects:
                for dx in range(w):
                    for dy in range(h):
                        for tile in quadrados.get((x + dx, y + dy, nivel), ()):
                            if tile.startswith(IGNORAR) or not tile.startswith(PREFIXOS):
                                continue
                            info["tiles"][tile] += 1
                            vistos.add(tile)
            for t in vistos:
                info["comodos_com"][t] += 1
        print(cab.name, {a: comodos[a]["n"] for a in sorted(ALVOS)}, flush=True)

    saida = {}
    for nome, info in comodos.items():
        n = max(info["n"], 1)
        linhas = []
        for tile, qtd in info["tiles"].most_common(40):
            linhas.append({"tile": tile, "total": qtd,
                           "em_%_dos_comodos": round(100 * info["comodos_com"][tile] / n),
                           "papel_knoxmap": papeis.get(tile)})
        saida[nome] = {"comodos_vistos": info["n"], "moveis": linhas}
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / "lojas_vanilla.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
    md = ["# Móveis do jogo base por tipo de cômodo (gerado por `scripts/analise_lojas_vanilla.py`)", "",
          "Contagem nos cômodos de Knox County. `%` = em quantos cômodos do tipo o tile aparece; "
          "`papel` = nome do móvel no catálogo do KnoxMap (vazio = o KnoxMap não tem esse papel).", ""]
    for nome, d in saida.items():
        md += [f"## `{nome}` ({d['comodos_vistos']} cômodos)", "", "| Tile | Total | % | Papel |", "|---|---|---|---|"]
        for m in d["moveis"][:25]:
            md.append(f"| `{m['tile']}` | {m['total']} | {m['em_%_dos_comodos']} | {m['papel_knoxmap'] or ''} |")
        md.append("")
    (SAIDA / "LOJAS_VANILLA.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
