"""Kit Brasil: empacota as folhas de peças novas (kits/tiles/) para o jogo (B42).

Saída (pasta `saida/kit_tiles/`):
- `rsb_kitbrasil.floor.pack`: as imagens, no formato de PackFile::read do jogo
  ("PZPK", versão 1, páginas PNG de até 1024 px, cada peça recortada como nos
  pacotes originais: o losango do piso 126 x 64, na posição 0,192 da peça
  128 x 256). O ".floor" no nome faz o jogo carregar sem compressão, como os
  pisos originais (Tiles2x.floor.pack; lido em ChooseGameInfo).
- `rsb_kitbrasil.tiles`: as propriedades ("tdef", versão 1: para cada folha,
  nome, imagem, colunas, linhas, número da folha e, para cada peça, a lista de
  propriedades nome/valor). Os pisos levam as mesmas da calçada original
  (`blends_street_01_96`): FloorMaterial Road_07, diamondFloor, exterior,
  fireRequirement 80, solidfloor.

`instalar(mod)` copia os dois para `<mod>/common/media/` e acrescenta ao
mod.info (raiz, 42/ e common/) as linhas `pack=rsb_kitbrasil.floor` e
`tiledef=rsb_kitbrasil 7391` (número de arquivo só nosso, 100 a 8189).
`ferramentas(pasta Tiles/2x)` copia as folhas PNG para as ferramentas de mapa
(render_lots, satélite, TileZed/BuildingEd enxergam as peças).

Uso: python -I -X utf8 kit_tiles.py <kits/tiles> <saida> [pasta do mod] [Tiles/2x]
"""
from __future__ import annotations

import io
import json
import shutil
import struct
import sys
from pathlib import Path

from PIL import Image

NOME = "rsb_kitbrasil"
NUMERO_ARQUIVO = 7391
PISO = [("FloorMaterial", "Road_07"), ("diamondFloor", ""), ("exterior", ""),
        ("fireRequirement", "80"), ("solidfloor", "")]


def _s(txt: str) -> bytes:
    b = txt.encode("latin-1")
    return struct.pack("<i", len(b)) + b


def folhas(kit: Path) -> list[tuple[Path, dict]]:
    out = []
    for js in sorted(kit.glob("rsb_*.json")):
        man = json.loads(js.read_text(encoding="utf-8"))
        png = js.with_suffix(".png")
        if png.exists():
            out.append((png, man))
    return out


def pacote(lista, destino: Path) -> int:
    """Grava o .floor.pack. Cada peça entra recortada (só o losango do piso)."""
    pecas = []
    for png, man in lista:
        im = Image.open(png).convert("RGBA")
        for n, _p in enumerate(man["pecas"]):
            cel = im.crop(((n % 8) * 128, (n // 8) * 256, (n % 8) * 128 + 128, (n // 8) * 256 + 256))
            caixa = cel.getchannel("A").getbbox()
            if caixa:
                pecas.append((f"{man['folha']}_{n}", cel.crop(caixa), caixa))
    # páginas de 1024 x 1024, peças em fileiras
    paginas, atual, x, y, alt = [], [], 0, 0, 0
    for nome, img, caixa in pecas:
        w, h = img.size
        if x + w > 1024:
            x, y, alt = 0, y + alt, 0
        if y + h > 1024:
            paginas.append(atual)
            atual, x, y, alt = [], 0, 0, 0
        atual.append((nome, img, caixa, x, y))
        x += w + 2
        alt = max(alt, h + 2)
    if atual:
        paginas.append(atual)
    out = bytearray(b"PZPK" + struct.pack("<2i", 1, len(paginas)))
    for i, pag in enumerate(paginas):
        altura = max(py + img.size[1] for _n, img, _c, _px, py in pag)
        folha = Image.new("RGBA", (1024, altura), (0, 0, 0, 0))
        out += _s(f"{NOME}{i}") + struct.pack("<2i", len(pag), 1)
        for nome, img, (bx, by, _bx2, _by2), px, py in pag:
            folha.paste(img, (px, py))
            out += _s(nome) + struct.pack("<8i", px, py, img.size[0], img.size[1], bx, by, 128, 256)
        buf = io.BytesIO()
        folha.save(buf, format="PNG")
        out += struct.pack("<i", len(buf.getvalue())) + buf.getvalue()
    destino.write_bytes(bytes(out))
    return len(pecas)


def definicoes(lista, destino: Path) -> None:
    """Grava o .tiles (formato "tdef" do jogo)."""
    out = bytearray(b"tdef" + struct.pack("<2i", 1, len(lista)))
    for num, (png, man) in enumerate(lista, start=1):
        cols = 8
        linhas = (len(man["pecas"]) + cols - 1) // cols
        out += f"{man['folha']}\n{man['folha']}.png\n".encode("latin-1")
        out += struct.pack("<4i", cols, linhas, num, cols * linhas)
        for n in range(cols * linhas):
            props = (man["pecas"][n].get("props") or PISO) if n < len(man["pecas"]) else []
            out += struct.pack("<i", len(props))
            for k, v in props:
                out += f"{k}\n{v}\n".encode("latin-1")
    destino.write_bytes(bytes(out))


def ler_definicoes(path: Path) -> list:
    """Lê um .tiles (para conferir o que gravamos e o do jogo)."""
    d = path.read_bytes()
    assert d[:4] == b"tdef", "não é um .tiles"
    ver, n = struct.unpack_from("<2i", d, 4)
    pos, out = 12, []

    def linha():
        nonlocal pos
        fim = d.index(b"\n", pos)
        s = d[pos:fim].decode("latin-1")
        pos = fim + 1
        return s

    for _ in range(n):
        nome, img = linha(), linha()
        cols, rows, num, cont = struct.unpack_from("<4i", d, pos)
        pos += 16
        pecas = []
        for _t in range(cont):
            (np_,) = struct.unpack_from("<i", d, pos)
            pos += 4
            pecas.append([(linha(), linha()) for _p in range(np_)])
        out.append({"nome": nome, "imagem": img, "colunas": cols, "linhas": rows, "numero": num, "pecas": pecas})
    assert pos == len(d), "sobrou coisa no fim do .tiles"
    return out


def montar(kit: Path, saida: Path) -> dict:
    saida.mkdir(parents=True, exist_ok=True)
    lista = folhas(kit)
    n = pacote(lista, saida / f"{NOME}.floor.pack")
    definicoes(lista, saida / f"{NOME}.tiles")
    # conferências: o .tiles relido e o .pack relido pelo leitor do KnoxMap
    defs = ler_definicoes(saida / f"{NOME}.tiles")
    return {"folhas": [m["folha"] for _p, m in lista], "pecas": n,
            "tiles": [(d["nome"], d["colunas"], d["linhas"], sum(1 for p in d["pecas"] if p)) for d in defs]}


def instalar(saida: Path, mod: Path) -> list[str]:
    media = mod / "common" / "media"
    (media / "texturepacks").mkdir(parents=True, exist_ok=True)
    shutil.copy2(saida / f"{NOME}.floor.pack", media / "texturepacks" / f"{NOME}.floor.pack")
    shutil.copy2(saida / f"{NOME}.tiles", media / f"{NOME}.tiles")
    linhas = [f"pack={NOME}.floor", f"tiledef={NOME} {NUMERO_ARQUIVO}"]
    mexidos = []
    for info in (mod / "mod.info", mod / "42" / "mod.info", mod / "common" / "mod.info"):
        if not info.exists():
            continue
        txt = info.read_text(encoding="utf-8")
        velhas = [l for l in txt.splitlines() if not l.startswith((f"pack={NOME}", f"tiledef={NOME}"))]
        info.write_text("\n".join(velhas + linhas) + "\n", encoding="utf-8")
        mexidos.append(str(info))
    return mexidos


def ferramentas(kit: Path, tiles2x: Path) -> list[str]:
    feitas = []
    for png, man in folhas(kit):
        shutil.copy2(png, tiles2x / png.name)
        feitas.append(man["folha"])
    return feitas


if __name__ == "__main__":
    a = sys.argv[1:]
    res = montar(Path(a[0]), Path(a[1]))
    if len(a) > 2 and a[2] not in ("", "-"):
        res["mod_info"] = instalar(Path(a[1]), Path(a[2]))
    if len(a) > 3:
        res["ferramentas"] = ferramentas(Path(a[0]), Path(a[3]))
    print(json.dumps(res, ensure_ascii=False, indent=1))
