"""Catálogo do jogo base (T8): nomes de cômodo, listas de loot, zonas de zumbi e de veículo.

Lê os arquivos Lua do Project Zomboid e grava um índice de consulta pequeno em
`catalogo/` (JSON + Markdown), para não precisar reabrir arquivos de 1 MB.

Uso:  python -I scripts/catalogo_jogo.py [pasta do jogo]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

JOGO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid")
LUA = JOGO / "media" / "lua"
SAIDA = Path(__file__).resolve().parent.parent / "catalogo"


def ler(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def chaves_nivel(texto: str, inicio: int, profundidade: int) -> list[tuple[str, int, int]]:
    """Chaves `nome = {` na profundidade dada, a partir de `inicio` (dentro de uma tabela).

    Devolve (nome, começo, fim) de cada bloco. Ignora comentários de linha e strings.
    """
    out, d, i, n = [], 0, inicio, len(texto)
    abertas: list[tuple[str, int]] = []
    while i < n:
        c = texto[i]
        if texto.startswith("--[[", i):
            j = texto.find("]]", i)
            i = n if j < 0 else j + 2
            continue
        if texto.startswith("--", i):
            j = texto.find("\n", i)
            i = n if j < 0 else j
            continue
        if c in "\"'":
            j = i + 1
            while j < n and texto[j] != c:
                j += 2 if texto[j] == "\\" else 1
            i = j + 1
            continue
        if c == "{":
            d += 1
            if d == profundidade:
                m = re.search(r"([A-Za-z_][\w]*)\s*=\s*$|\[\s*\"([^\"]+)\"\s*\]\s*=\s*$",
                              texto[max(0, i - 80):i])
                nome = (m.group(1) or m.group(2)) if m else ""
                abertas.append((nome, i))
        elif c == "}":
            if d == profundidade and abertas:
                nome, ini = abertas.pop()
                if nome:
                    out.append((nome, ini, i))
            d -= 1
            if d < 0:
                break
        i += 1
    return out


def distribuicoes() -> dict:
    t = ler(LUA / "server/Items/Distributions.lua")
    ini = t.index("local distributionTable = {") + len("local distributionTable = ")
    comodos = {}
    for nome, a, b in chaves_nivel(t, ini, 2):
        corpo = t[a:b + 1]
        # contêineres = chaves de profundidade 1 dentro do cômodo
        cont = [c for c, _, _ in chaves_nivel(corpo, 0, 2)]
        procs = sorted(set(re.findall(r'name\s*=\s*"([^"]+)"', corpo)))
        real = set(cont) - {"items", "junk", "rolls", "dontSpawnAmmo", "fillRand", "procedural", "procList"}
        comodos[nome] = {"tipo": "comodo" if real else "bolsa_ou_esconderijo", "conteineres": cont, "listas_procedurais": procs}
    return comodos


def listas_procedurais() -> dict:
    t = ler(LUA / "server/Items/ProceduralDistributions.lua")
    ini = t.index("ProceduralDistributions.list = {") + len("ProceduralDistributions.list = ")
    out = {}
    for nome, a, b in chaves_nivel(t, ini, 2):
        corpo = t[a:b + 1]
        rolls = re.search(r"rolls\s*=\s*(\d+)", corpo)
        itens = re.findall(r'"([A-Za-z_][\w.]*)"\s*,\s*([\d.]+)', corpo)
        top = sorted(itens, key=lambda x: -float(x[1]))[:6]
        out[nome] = {"rolls": int(rolls.group(1)) if rolls else None,
                     "n_itens": len(itens), "mais_comuns": [i for i, _ in top]}
    return out


def zonas_zumbi() -> dict:
    t = ler(LUA / "shared/NPCs/ZombiesZoneDefinition.lua")
    out = {}
    for nome in re.findall(r"^ZombiesZoneDefinition\.(\w+)\s*=\s*\{", t, re.M):
        m = re.search(rf"^ZombiesZoneDefinition\.{nome}\s*=\s*\{{(.*?)^\}};?", t, re.M | re.S)
        corpo = m.group(1) if m else ""
        out[nome] = {
            "chanceToSpawn": (re.search(r"chanceToSpawn\s*=\s*(\d+)", corpo) or [None, None])[1],
            "toSpawn": (re.search(r"^\s*toSpawn\s*=\s*(\d+)", corpo, re.M) or [None, None])[1],
            "roupas": sorted(set(re.findall(r'name\s*=\s*"([^"]+)"', corpo)))[:12],
        }
    return out


def zonas_veiculo() -> dict:
    t = ler(LUA / "shared/VehicleZoneDefinition.lua")
    out = {}
    for nome in re.findall(r"^VehicleZoneDistribution\.(\w+)\s*=", t, re.M):
        m = re.search(rf"^VehicleZoneDistribution\.{nome}\s*=\s*\{{(.*?)^\}};?", t, re.M | re.S)
        corpo = m.group(1) if m else ""
        out[nome] = {"veiculos": sorted(set(re.findall(r'vehicle\s*=\s*"([^"]+)"', corpo))),
                     "burnt": "chanceToSpawnBurnt" in corpo}
    return out


def historias() -> dict:
    """Histórias de cena (lixo/cenas) em Lua; as histórias de casa/veículo ficam no Java."""
    out = {}
    d = LUA / "server/RandomizedWorldContent/StoryClutter/StoryClutter_Definitions.lua"
    if d.exists():
        t = ler(d)
        out["StoryClutter"] = sorted(set(re.findall(r"^\s*(\w+)\s*=\s*\{", t, re.M)))
    return out


def md(c: dict) -> str:
    L = ["# Catálogo do jogo base (gerado por `scripts/catalogo_jogo.py`)", "",
         f"Fonte: jogo 42.21. Cômodos e bolsas: {len(c['comodos'])}; listas de loot: {len(c['listas_loot'])}; "
         f"zonas de zumbi: {len(c['zonas_zumbi'])}; zonas de veículo: {len(c['zonas_veiculo'])}.", "",
         "## Cômodos (nome no mapa → contêineres)", "", "| Cômodo | Contêineres |", "|---|---|"]
    for k, v in sorted(c["comodos"].items()):
        if v["tipo"] == "comodo":
            L.append(f"| `{k}` | {', '.join(v['conteineres'])} |")
    L += ["", "## Zonas de zumbi (tipo `ZombiesType` no WorldEd)", "", "| Zona | Chance | Roupas |", "|---|---|---|"]
    for k, v in sorted(c["zonas_zumbi"].items()):
        L.append(f"| `{k}` | {v['chanceToSpawn'] or ''} | {', '.join(v['roupas'][:6])} |")
    L += ["", "## Zonas de veículo (tipo `VehicleZoneDistribution`)", "", "| Zona | Veículos |", "|---|---|"]
    for k, v in sorted(c["zonas_veiculo"].items()):
        L.append(f"| `{k}` | {', '.join(v['veiculos'][:8])}{' (+queimados)' if v['burnt'] else ''} |")
    L += ["", f"## Bolsas e esconderijos ({sum(1 for v in c['comodos'].values() if v['tipo'] != 'comodo')})", "",
          ", ".join(f"`{k}`" for k, v in sorted(c["comodos"].items()) if v["tipo"] != "comodo"),
          "", f"## Listas de loot procedurais: {len(c['listas_loot'])} (nome → itens no JSON, `listas_loot`)"]
    return "\n".join(L) + "\n"


def main() -> None:
    c = {"comodos": distribuicoes(), "listas_loot": listas_procedurais(),
         "zonas_zumbi": zonas_zumbi(), "zonas_veiculo": zonas_veiculo(), "historias": historias()}
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / "catalogo_jogo.json").write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
    (SAIDA / "CATALOGO.md").write_text(md(c), encoding="utf-8")
    print({k: len(v) for k, v in c.items()})


if __name__ == "__main__":
    main()
