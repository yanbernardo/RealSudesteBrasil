"""Prédio desenhado por planta (marcos e prédios especiais), virado .tbx para o KnoxMap.

Usa o "desenhador" do próprio KnoxMap (knoxbuild/designer.py): a planta diz só os
cômodos de cada andar; paredes, portas, janelas e escada saem das regras dele. Aqui
dá para trocar o estilo da fachada (peças do jogo base) e deixar o prédio vazio,
sem móveis. A cópia não gira: a planta é desenhada com a frente para o sul e
`--frente E` grava a versão virada para o leste (x e y trocados).

Uso (Python do .venv do KnoxMap):
  python -I predio_desenhado.py <KnoxMap> <planta.json> <saída.tbx> [--frente S|E]
"""
from __future__ import annotations

import json
import os
import sys


def _girar_para_leste(d: dict) -> dict:
    """Frente sul -> frente leste: troca x por y (o fundo vira o oeste)."""
    g = dict(d)
    g["width"], g["height"] = d["height"], d["width"]
    g["rooms"] = [{**r, "x": r["y"], "y": r["x"], "w": r["h"], "h": r["w"]} for r in d["rooms"]]
    return g


def main() -> None:
    knox, planta, saida = sys.argv[1], os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3])
    frente = sys.argv[sys.argv.index("--frente") + 1] if "--frente" in sys.argv else "S"
    sys.path.insert(0, knox)
    os.chdir(knox)
    from knoxbuild import build as B, designer, layout as L

    d = json.load(open(planta, encoding="utf-8"))
    if frente == "E":
        d = _girar_para_leste(d)

    estilo = d.get("estilo_fachada")
    if estilo:
        base = dict(B.style_named(estilo.get("base", "civic"), d.get("kind") or None))
        p = estilo["parede"]           # ex.: walls_commercial_02_048 (as 8 peças seguem a ordem do jogo)
        folha, n = p.rsplit("_", 1)
        n = int(n)
        nomes = ["West", "North", "NorthWest", "SouthEast", None, None, None, None,
                 "WestWindow", "NorthWindow", "WestDoor", "NorthDoor"]
        base["exterior"] = {"category": "exterior_walls",
                            "tiles": {k: f"{folha}_{n + i:03d}" for i, k in enumerate(nomes) if k}}
        if estilo.get("janela"):
            j = estilo["janela"]
            jf, jn = j.rsplit("_", 1)
            base["window"] = {"category": "windows", "tiles": {"West": j, "North": f"{jf}_{int(jn) + 1:03d}"}}
            base["windows_by_levels"] = None
        base["grime"] = None
        designer.style_for = lambda _design, _s=base: _s
    if d.get("vazio"):
        L._furnish = lambda *a, **k: None          # sem móveis (pedido do usuário)

    texto = designer.tbx_text(d, d.get("name"))
    with open(saida, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"{d.get('name')}: {d['width']} x {d['height']} tiles, {d['storeys']} andares, "
          f"frente {frente}, {len(d['rooms'])} cômodos na planta -> {saida}")


if __name__ == "__main__":
    main()
