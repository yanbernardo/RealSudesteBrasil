"""Visão de satélite do mapa do jogo (D-41): grava o pyramid.zip da pasta do mapa.

O botão de satélite do mapa do jogo (tecla M) mostra a imagem `pyramid.zip` que
fica ao lado do worldmap.xml (ISWorldMap.lua: newPyramidLayer("pyramid.zip")). No
Knox County ela tem 1 pixel por tile, em quadros de 256 px, cada nível com metade
do tamanho do anterior. Aqui a imagem é montada dos próprios arquivos compilados
(.lotheader/.lotpack): cada pixel recebe a cor do que se vê de cima naquele
quadrado (telhado, copa de árvore, chão, água), tirada da média dos pixels do
desenho da peça do jogo.

Uso (Python do .venv do KnoxMap):
  python -I satelite.py <KnoxMap> <pasta dos lots> <x0> <y0> <largura> <altura> <saída.zip> [figura.png]
"""
from __future__ import annotations

import io
import os
import re
import sys
import zipfile
from pathlib import Path

QUADRO = 256
# peças que não se veem de cima (ou são pequenas demais para um pixel)
IGNORAR = ("lighting_", "fixtures_doors", "fixtures_windows", "overlay_grime", "street_decoration",
           "location_", "furniture_", "appliances_", "fixtures_", "recreational_", "trash", "d_generic",
           "walls_interior", "industry_", "signs_", "camping_", "carpentry_")
ARVORE = ("vegetation_trees", "e_americanholly", "e_americanlinden", "e_canadianhemlock",
          "e_carolinasilverbell", "e_cockspurhawthorn", "e_dogwood", "e_easternredbud", "e_redmaple",
          "e_riverbirch", "e_virginiapine", "e_yellowwood", "e_americanbeech", "e_whitecedar",
          "e_blackcherry", "e_sugarmaple", "e_whiteoak", "e_eastern")


def _cor_media(img):
    """Média das cores dos pixels visíveis da peça (RGB) ou None."""
    dados = img.get_flattened_data() if hasattr(img, "get_flattened_data") else img.getdata()
    px = [p for p in dados if p[3] > 128]
    if not px:
        return None
    n = len(px)
    return (sum(p[0] for p in px) // n, sum(p[1] for p in px) // n, sum(p[2] for p in px) // n)


def montar(knox: str, lots: str, x0: int, y0: int, w: int, h: int):
    """A imagem de satélite (RGBA, 1 pixel por tile) da área x0,y0,w,h (tiles do mundo)."""
    sys.path.insert(0, knox)
    os.chdir(knox)
    from PIL import Image
    import knoxpaths
    from tools.render_lots import CELL, read_header, read_squares

    folhas: dict[str, object] = {}
    cores: dict[str, tuple | None] = {}
    pasta = knoxpaths.mapping_tools_dir() / "Tiles" / "2x"

    def cor(nome: str):
        if nome in cores:
            return cores[nome]
        c = None
        m = re.match(r"^(.*)_(\d+)$", nome)
        if m:
            folha, i = m.group(1), int(m.group(2))
            if folha not in folhas:
                p = pasta / f"{folha}.png"
                folhas[folha] = Image.open(p).convert("RGBA") if p.exists() else None
            f = folhas[folha]
            if f is not None:
                cols = max(1, f.width // 128)
                cx, cy = (i % cols) * 128, (i // cols) * 256
                if cy + 256 <= f.height:
                    c = _cor_media(f.crop((cx, cy, cx + 128, cy + 256)).resize((32, 64)))
        cores[nome] = c
        return c

    topo: dict[tuple[int, int], list] = {}      # (x, y) -> [(z, peças)]
    for cab in Path(lots).glob("*.lotheader"):
        cxw, cyw = (int(v) for v in cab.stem.split("_"))
        bx, by = cxw * CELL, cyw * CELL
        if bx + CELL <= x0 or by + CELL <= y0 or bx >= x0 + w or by >= y0 + h:
            continue
        nomes, lo, hi = read_header(str(cab))
        for (sx, sy, z), ts in read_squares(str(Path(lots) / f"world_{cxw}_{cyw}.lotpack"), nomes, lo, hi,
                                                 (0, 0, CELL, CELL)).items():
            X, Y = bx + sx - x0, by + sy - y0
            if 0 <= X < w and 0 <= Y < h:
                topo.setdefault((X, Y), []).append((z, ts))

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    for (X, Y), andares in topo.items():
        andares.sort(key=lambda a: -a[0])
        escolhida = None
        for z, ts in andares:
            # telhado: peça de telhado ou, num andar de cima, chão (laje/telhado plano de prédio)
            telhado = [t for t in ts if t.startswith("roofs_") or (z > 0 and t.startswith("floors_"))]
            c = next((cor(t) for t in reversed(telhado) if cor(t)), None)
            if c:
                escolhida = c
                break
            if z > 0:
                continue        # andar sem telhado (parede, móvel): de cima vê-se o telhado ou o chão
            chao = [t for t in ts if not t.startswith(IGNORAR) and not t.startswith(ARVORE)
                    and not t.startswith("walls_")]
            base = None
            for t in reversed(chao):         # a última camada de chão por cima (mistura de grama/areia)
                base = cor(t)
                if base:
                    break
            arv = next((cor(t) for t in ts if t.startswith(ARVORE) and cor(t)), None)
            parede = any(t.startswith("walls_") for t in ts)
            if arv and base:
                escolhida = tuple((a * 2 + b) // 3 for a, b in zip(arv, base))
            elif parede and base:
                escolhida = tuple(v * 2 // 3 for v in base)   # contorno do prédio, um pouco mais escuro
            elif parede and not base:
                escolhida = (150, 140, 130)                   # dentro de prédio sem telhado conhecido
            else:
                escolhida = base or arv
            break
        if escolhida:
            px[X, Y] = (*escolhida, 255)
    return img


def gravar_piramide(img, x0: int, y0: int, saida: str) -> int:
    """pyramid.zip no formato do jogo (como o spawnSelectImagePyramid do KnoxMap)."""
    from PIL import Image
    w, h = img.size
    n = 0
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_STORED) as z:
        z.writestr("pyramid.txt", "VERSION=1\n"
                   f"bounds={x0} {y0} {x0 + w} {y0 + h}\n"
                   f"imageSize={w} {h}\n"
                   "minFilter=linear\nmagFilter=nearest\n")
        nivel, atual = 0, img
        while True:
            cols, rows = -(-atual.width // QUADRO), -(-atual.height // QUADRO)
            z.writestr(f"{nivel}/", b"")
            for cx in range(cols):
                for cy in range(rows):
                    q = Image.new("RGBA", (QUADRO, QUADRO), (0, 0, 0, 0))
                    q.paste(atual.crop((cx * QUADRO, cy * QUADRO, min(atual.width, (cx + 1) * QUADRO),
                                        min(atual.height, (cy + 1) * QUADRO))))
                    raw = io.BytesIO()
                    q.save(raw, format="PNG")
                    z.writestr(f"{nivel}/tile{cx}x{cy}.png", raw.getvalue())
                    n += 1
            if cols <= 3 and rows <= 3:
                break
            atual = atual.resize((max(1, -(-atual.width // 2)), max(1, -(-atual.height // 2))), Image.LANCZOS)
            nivel += 1
    return n


if __name__ == "__main__":
    knox, lots = sys.argv[1], os.path.abspath(sys.argv[2])
    x0, y0, w, h = (int(v) for v in sys.argv[3:7])
    saida = os.path.abspath(sys.argv[7])
    figura = os.path.abspath(sys.argv[8]) if len(sys.argv) > 8 else None
    imagem = montar(knox, lots, x0, y0, w, h)
    if figura:
        imagem.save(figura)
    print(f"satélite: {w} x {h} pixels, {gravar_piramide(imagem, x0, y0, saida)} quadros -> {saida}")
