"""Põe mureta (guarda-corpo) e caixa d'água na laje de um .tbx (casa de laje brasileira).

A laje é o telhado Flat Top com profundidade Three: vira o chão do andar de cima.
Aqui entram, nesse andar, um guarda-corpo branco em volta da borda e uma caixa
d'água (peças do jogo base). Uso: python laje.py <casa.tbx> [x,y da caixa d'água]
"""
import re
import sys

MURETA_O, MURETA_N = "fixtures_railings_01_64", "fixtures_railings_01_65"   # lado oeste / lado norte
CAIXA = "rooftop_furniture_001"


def main():
    caminho = sys.argv[1]
    cx, cy = (int(v) for v in sys.argv[2].split(",")) if len(sys.argv) > 2 else (1, 1)
    t = open(caminho, encoding="utf-8").read()
    W = int(re.search(r'<building[^>]* width="(\d+)"', t).group(1))
    H = int(re.search(r'<building[^>]* height="(\d+)"', t).group(1))
    n = len(re.findall(r"^ <furniture[ >]", t, re.M))       # índice das novas peças (conta também as com layer=)
    defs = (f' <furniture>\n  <entry orient="W">\n   <tile x="0" y="0" name="{MURETA_O}"/>\n  </entry>\n </furniture>\n'
            f' <furniture>\n  <entry orient="N">\n   <tile x="0" y="0" name="{MURETA_N}"/>\n  </entry>\n </furniture>\n'
            f' <furniture>\n  <entry orient="W">\n   <tile x="0" y="0" name="{CAIXA}"/>\n  </entry>\n </furniture>\n')
    t = t.replace(" <used_tiles>", defs + " <used_tiles>", 1)
    t = re.sub(r"<used_furniture>([^<]*)</used_furniture>",
               lambda m: f"<used_furniture>{m.group(1).strip()} {n} {n + 1} {n + 2}</used_furniture>", t, 1)
    objs = []
    for y in range(H):              # bordas oeste e leste (a leste, na borda oeste do quadrado de fora)
        objs.append(f'  <object type="furniture" FurnitureTiles="{n}" orient="W" x="0" y="{y}"/>')
        objs.append(f'  <object type="furniture" FurnitureTiles="{n}" orient="W" x="{W}" y="{y}"/>')
    for x in range(W):              # bordas norte e sul
        objs.append(f'  <object type="furniture" FurnitureTiles="{n + 1}" orient="N" x="{x}" y="0"/>')
        objs.append(f'  <object type="furniture" FurnitureTiles="{n + 1}" orient="N" x="{x}" y="{H}"/>')
    objs.append(f'  <object type="furniture" FurnitureTiles="{n + 2}" orient="W" x="{cx}" y="{cy}"/>')
    # no último andar (o de cima da laje), antes da grade de cômodos
    i = t.rfind(" <floor>")
    j = t.index("  <rooms>", i)
    t = t[:j] + "\n".join(objs) + "\n" + t[j:]
    open(caminho, "w", encoding="utf-8").write(t)
    print(f"laje: mureta em volta de {W} x {H} tiles e caixa d'água em {cx},{cy} -> {caminho}")


if __name__ == "__main__":
    main()
