"""Escreve um prédio do BuildingEd (.tbx) "à mão": cada cômodo, porta, janela,
escada, móvel e peça de parede posto por quem chama, sem regras automáticas
(pedido do usuário, 09/11/2026: nada do desenhador do KnoxMap).

Formato (BuildingWriter do BuildingEd, versão 4; conferido no knoxbuild/tbx.py):
- entradas de peça (tile_entry): índice a partir de 1, 0 = nenhuma;
- móveis (furniture): índice a partir de 0;
- ordem: tile_entry, furniture, user_tiles, used_tiles, used_furniture, room, floor.
- porta/janela em (x, y, dir): dir "N" = na borda de cima do tile, "W" = na
  borda esquerda; a fachada sul é y = altura (borda de cima do tile de fora).
- escada: dir "N" corre ao longo de y (3 tiles), "W" ao longo de x.
- móvel: `orient` é o lado onde as COSTAS encostam (o contrário do "Facing" do
  jogo): carteira virada para oeste = orient "E".
- peças de parede soltas (letreiros): camada "WallFurniture" das user_tiles, grade
  (largura+1) x (altura+1), então cabem na fachada sul e leste.
"""
from __future__ import annotations

from xml.sax.saxutils import escape, quoteattr


def _a(pares) -> str:
    return "".join(f" {k}={quoteattr(str(v))}" for k, v in pares)


class Predio:
    def __init__(self, largura: int, altura: int, andares: int):
        self.w, self.h = largura, altura
        self.entradas: list[tuple[str, dict]] = []
        self.moveis: list[tuple[str, str, dict]] = []       # (nome, camada, {orient: {"x,y": peça}})
        self.comodos: list[dict] = []
        self.niveis = [{"grade": [[0] * largura for _ in range(altura)], "obj": [], "user": {}}
                       for _ in range(andares + 1)]          # +1: o andar do telhado
        self.attrs = {}

    # ---- tabela de peças e móveis
    def entrada(self, categoria: str, pecas: dict) -> int:
        e = (categoria, dict(pecas))
        if e in self.entradas:
            return self.entradas.index(e) + 1
        self.entradas.append(e)
        return len(self.entradas)

    def movel(self, nome: str, orients: dict, camada: str = "Furniture") -> int:
        for i, (n, _c, _o) in enumerate(self.moveis):
            if n == nome:
                return i
        self.moveis.append((nome, camada, orients))
        return len(self.moveis) - 1

    def comodo(self, nome: str, cor: str, parede_int: int, piso: int, forro: int) -> int:
        self.comodos.append({"Name": nome, "InternalName": nome, "Color": cor, "InteriorWall": parede_int,
                             "InteriorWallTrim": 0, "Floor": piso, "GrimeFloor": 0, "GrimeWall": 0,
                             "Ceiling": forro})
        return len(self.comodos)

    # ---- desenho
    def sala(self, nivel: int, comodo: int, x: int, y: int, w: int, h: int) -> None:
        g = self.niveis[nivel]["grade"]
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                g[yy][xx] = comodo

    def porta(self, nivel, x, y, d, tile, moldura=0):
        self.niveis[nivel]["obj"].append(("door", _a([("type", "door"), ("FrameTile", moldura), ("x", x), ("y", y),
                                                      ("dir", d), ("Tile", tile)])))

    def janela(self, nivel, x, y, d, tile, cortina=0):
        self.niveis[nivel]["obj"].append(("window", _a([("type", "window"), ("CurtainsTile", cortina),
                                                        ("ShuttersTile", 0), ("x", x), ("y", y), ("dir", d),
                                                        ("Tile", tile)])))

    def escada(self, nivel, x, y, d, tile):
        self.niveis[nivel]["obj"].append(("stairs", _a([("type", "stairs"), ("x", x), ("y", y), ("dir", d),
                                                        ("Tile", tile)])))

    def mob(self, nivel, movel, x, y, orient):
        self.niveis[nivel]["obj"].append(("furniture", _a([("type", "furniture"), ("FurnitureTiles", movel),
                                                           ("orient", orient), ("x", x), ("y", y)])))

    def laje(self, nivel, x, y, w, h, topo, cap, slope):
        self.niveis[nivel]["obj"].append(("roof", _a([
            ("type", "roof"), ("width", w), ("height", h), ("RoofType", "FlatTop"), ("Depth", "Three"),
            ("cappedW", "false"), ("cappedN", "false"), ("cappedE", "false"), ("cappedS", "false"),
            ("CapTiles", cap), ("SlopeTiles", slope), ("TopTiles", topo), ("x", x), ("y", y)])))

    def peca_parede(self, nivel, x, y, peca):
        self.niveis[nivel]["user"][(x, y)] = peca

    # ---- arquivo
    def texto(self) -> str:
        out = ['<?xml version="1.0" encoding="UTF-8"?>', f"<building{_a([('version', 4), ('width', self.w), ('height', self.h)] + list(self.attrs.items()))}>"]
        for cat, pecas in self.entradas:
            out.append(f" <tile_entry category={quoteattr(cat)}>")
            out += [f"  <tile enum={quoteattr(k)} tile={quoteattr(v)}/>" for k, v in pecas.items()]
            out.append(" </tile_entry>")
        for _n, camada, orients in self.moveis:
            out.append(" <furniture>" if camada == "Furniture" else f" <furniture layer={quoteattr(camada)}>")
            for o in ("W", "N", "E", "S"):
                if o in orients:
                    out.append(f'  <entry orient="{o}">')
                    for k, v in orients[o].items():
                        dx, dy = k.split(",")
                        out.append(f'   <tile x="{dx}" y="{dy}" name={quoteattr(v)}/>')
                    out.append("  </entry>")
            out.append(" </furniture>")
        nomes = sorted({p for nv in self.niveis for p in nv["user"].values()})
        if nomes:
            out.append(" <user_tiles>")
            out += [f"  <tile tile={quoteattr(t)}/>" for t in nomes]
            out.append(" </user_tiles>")
        out.append(f" <used_tiles>{' '.join(str(i) for i in range(1, len(self.entradas) + 1))}</used_tiles>")
        out.append(f" <used_furniture>{' '.join(str(i) for i in range(len(self.moveis)))}</used_furniture>")
        out += [f" <room{_a(c.items())}/>" for c in self.comodos]
        ordem = {"door": 0, "window": 1, "furniture": 2, "stairs": 3, "roof": 4}
        for nv in self.niveis:
            out.append(" <floor>")
            out += [f"  <object{a}/>" for _t, a in sorted(nv["obj"], key=lambda o: ordem[o[0]])]
            vals = [str(v) for row in nv["grade"] for v in row]
            linhas = ["\n"]
            for y in range(self.h):
                fim = (y == self.h - 1)
                row = vals[y * self.w:(y + 1) * self.w]
                linhas.append(",".join(row) + ("" if fim else ",") + "\n")
            out.append("  <rooms>" + escape("".join(linhas)) + "</rooms>")
            if nv["user"]:
                txt = ["\n"]
                for y in range(self.h + 1):
                    row = [str(nomes.index(nv["user"][(x, y)]) + 1) if (x, y) in nv["user"] else "0"
                           for x in range(self.w + 1)]
                    txt.append(",".join(row) + ("," if y < self.h else "") + "\n")
                out.append('  <tiles layer="WallFurniture">' + escape("".join(txt)) + "</tiles>")
            out.append(" </floor>")
        out.append("</building>")
        return "\n".join(out) + "\n"
