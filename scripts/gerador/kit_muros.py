"""Kit Brasil, morro e favela: muros de quintal (divisa), só as peças.

Muro de 2 m (o andar inteiro do jogo tem 2,8 m): o desenho vem da parede lisa
do jogo (`walls_interior_house_01`, peças 4-7) cortada na altura do muro, com a
"tampa" (o topo da parede, a espessura) descida para o novo topo. Textura com
relevo das paredes da favela (`texturas_favela.py`). Variações:
- liso: tijolo baiano, tijolo sujo, bloco, reboco cru, reboco branco, reboco amarelo;
- com cacos de vidro no topo (tijolo e reboco branco);
- com grade: base de 0,9 m e grade de ferro até 2 m (bloco e reboco branco),
  vazado (o jogo deixa ver através: `WallWTrans`/`WallNTrans`).
Cada estilo: oeste, norte, quina e pilar. No BuildingEd: lista de móveis,
grupo "Kit Brasil - Muros de quintal: ...", camada de paredes.

Uso: python -I -X utf8 kit_muros.py <pasta Tiles/2x> <kits/tiles>
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit_favela as kf  # noqa: E402
import texturas_favela as tf  # noqa: E402

PX_M = tf.PX_M
H_MURO = round(2.0 * PX_M)          # 137 px
H_BASE_GRADE = round(0.9 * PX_M)
MOLDE = ("walls_interior_house_01", 4)
PAPEIS = [(0, "W", "WallW"), (1, "N", "WallN"), (2, "NW", "WallNW"), (3, "SE", "WallSE")]

ESTILOS = [  # (chave, descrição, textura, material, extra)
    ("tijolo_baiano", "muro de tijolo baiano aparente", "tijolo_baiano", "Brick", None),
    ("tijolo_baiano_sujo", "muro de tijolo baiano sujo", "tijolo_baiano_sujo", "Brick", None),
    ("bloco_concreto", "muro de bloco de concreto", "bloco_concreto", "Stone", None),
    ("reboco_cru", "muro de reboco cru / chapisco", "reboco_cru", "Plaster", None),
    ("reboco_branco", "muro rebocado branco encardido", "reboco_branco_encardido", "Plaster", None),
    ("reboco_amarelo", "muro rebocado amarelo desbotado", "reboco_amarelo", "Plaster", None),
    ("tijolo_cacos", "muro de tijolo com cacos de vidro no topo", "tijolo_baiano", "Brick", "cacos"),
    ("reboco_cacos", "muro rebocado branco com cacos de vidro", "reboco_branco_encardido", "Plaster", "cacos"),
    ("bloco_grade", "mureta de bloco com grade de ferro", "bloco_concreto", "Stone", "grade"),
    ("reboco_grade", "mureta rebocada com grade de ferro", "reboco_branco_encardido", "Plaster", "grade"),
]


def _z(X, Y, face):
    """Altura (px) e posição ao longo (u) de cada pixel na face da parede."""
    uw = np.clip((63 - X) / 63, 0, 0.9999)
    un = np.clip((X - 63) / 63, 0, 0.9999)
    zw, zn = 192 + 32 * uw - Y, 192 + 32 * un - Y
    if face == "W":
        oeste = np.ones_like(X, dtype=bool)
    elif face == "N":
        oeste = np.zeros_like(X, dtype=bool)
    else:
        oeste = X < 63
    return np.where(oeste, zw, zn), np.where(oeste, uw, un), oeste


def cortar(molde: np.ndarray, face: str, altura: int) -> np.ndarray:
    """Molde de parede cortado em `altura` px, com a tampa (topo) descida."""
    Y, X = np.mgrid[0:256, 0:128].astype(float) + 0.5
    z, _u, _o = _z(X, Y, face)
    a = molde[..., 3] > 0
    tampa = a & (z > 191.0)                   # pixels acima do topo da face = espessura/tampa
    out = np.zeros_like(molde)
    corpo = a & (z <= altura) & ~tampa
    out[corpo] = molde[corpo]
    dy = 192 - altura
    ys, xs = np.nonzero(tampa)
    ok = ys + dy < 256
    out[ys[ok] + dy, xs[ok]] = molde[ys[ok], xs[ok]]
    return out


def pintar(cel: np.ndarray, face: str, texs, Lref, altura: int) -> np.ndarray:
    """Textura com relevo sobre o molde cortado (3 x 3 amostras por pixel)."""
    L = kf._lum(cel)
    acc = np.zeros((256, 128, 3))
    Y0, X0 = np.mgrid[0:256, 0:128].astype(float)
    for a in range(kf.SS):
        for b in range(kf.SS):
            X, Y = X0 + (a + 0.5) / kf.SS, Y0 + (b + 0.5) / kf.SS
            z, u, oeste = _z(X, Y, face)
            # a tampa descida lê a textura do alto do muro
            zz = np.clip(np.abs(np.minimum(z, altura)), 0, 191.9)
            cw = tf.amostrar_parede(texs["W"], u, zz)
            cn = tf.amostrar_parede(texs["N"], u, zz)
            acc += np.where(oeste[..., None], cw, cn)
    cor = acc / kf.SS ** 2 * np.clip(L / Lref, 0.35, 1.7)[..., None]
    out = np.zeros((256, 128, 4), dtype=np.uint8)
    out[..., :3] = np.clip(cor, 0, 255).astype(np.uint8)
    out[..., 3] = cel[..., 3]
    return out


def cacos(img: np.ndarray, face: str, altura: int, seed: int) -> np.ndarray:
    """Cacos de vidro (verde, marrom, branco) espetados na tampa do muro."""
    rnd = np.random.default_rng(seed)
    out = img.copy()
    Y, X = np.mgrid[0:256, 0:128]
    xs = range(2, 126, 3)
    cores = [(70, 150, 90), (120, 80, 40), (220, 228, 230), (90, 170, 120)]
    for x in xs:
        if face == "W" and x > 63 or face == "N" and x < 63:
            continue
        u = (63 - x) / 63 if (face == "W" or (face != "N" and x < 63)) else (x - 63) / 63
        yt = 192 + 32 * u - altura - 2                  # topo da tampa nesse x
        if rnd.random() < 0.25:
            continue
        h = rnd.integers(3, 8)
        w = rnd.integers(1, 3)
        c = np.array(cores[rnd.integers(len(cores))], float)
        for k in range(h):
            yy = int(yt - k)
            larg = max(0, int(w * (1 - k / h)))
            for dx in range(-larg, larg + 1):
                if 0 <= x + dx < 128 and 0 <= yy < 256:
                    luz = 1.25 if dx < 0 else 0.85
                    out[yy, x + dx, :3] = np.clip(c * luz, 0, 255)
                    out[yy, x + dx, 3] = 235
    return out


def grade(img: np.ndarray, face: str, seed: int) -> np.ndarray:
    """Grade de ferro (barras verticais e um tubo em cima) entre 0,9 m e 2 m."""
    out = img.copy()
    Y, X = np.mgrid[0:256, 0:128].astype(float) + 0.5
    z, u, oeste = _z(X, Y, face)
    if face == "SE":
        return out
    lado = np.where(oeste, X <= 63.5, X >= 62.5)                 # só a metade do tile onde está a face
    no_plano = (z > H_BASE_GRADE + 2) & (z < H_MURO) & lado
    barra = (np.abs(((u * 10) % 1) - 0.5) * 6.3 < 0.75)
    tubo = (np.abs(z - H_MURO + 2) < 1.6) | (np.abs(z - (H_BASE_GRADE + 4)) < 1.2)
    ferro = no_plano & (barra | tubo)
    luz = np.where(oeste, 0.85, 1.1)
    cor = np.array([58, 56, 54.0]) * luz[..., None]
    brilho = barra & (np.abs(((u * 10) % 1) - 0.5) * 6.3 < 0.3)
    cor = np.where(brilho[..., None], cor * 1.6, cor)
    ferrugem = tf.vn(u, z / 192, 30, 20, seed) > 0.72
    cor = np.where(ferrugem[..., None], np.array([110, 62, 40.0]), cor)
    out[ferro, :3] = np.clip(cor[ferro], 0, 255).astype(np.uint8)
    out[ferro, 3] = 255
    return out


def muros(tiles2x: Path, saida: Path) -> dict:
    molde_im = Image.open(tiles2x / f"{MOLDE[0]}.png").convert("RGBA")
    w = kf._celula(molde_im, MOLDE[1])
    Lref = np.median(kf._lum(w)[w[..., 3] > 200])
    nome = "rsb_muros_favela_01"
    linhas = (len(ESTILOS) + 1) // 2
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{nome}_{i}", "props": []} for i in range(linhas * 8)]
    grupos = {}
    for k, (chave, desc, tex_nome, material, extra) in enumerate(ESTILOS):
        texs = kf.texturas_estilo(tex_nome)
        alt = H_BASE_GRADE if extra == "grade" else H_MURO
        base = (k // 2) * 8 + (k % 2) * 4
        idx = {}
        for off, face, prop in PAPEIS:
            cel = cortar(kf._celula(molde_im, MOLDE[1] + off), face, alt)
            img = pintar(cel.astype(float), face, texs, Lref, alt)
            if extra == "cacos":
                img = cacos(img, face, alt, 100 + k * 4 + off)
            if extra == "grade":
                img = grade(img, face, 200 + k)
            i = base + off
            folha.alpha_composite(Image.fromarray(img, "RGBA"), ((i % 8) * 128, (i // 8) * 256))
            idx[prop] = i
            props = [["MaterialType", material], [prop, ""], ["wall", ""]] if prop != "WallSE" else [["WallSE", ""], ["wall", ""]]
            if extra == "grade" and prop in ("WallW", "WallN", "WallNW"):
                props += [[{"WallW": "WallWTrans", "WallN": "WallNTrans", "WallNW": "WallNWTrans"}[prop], ""]]
            pecas[i] = {"peca": f"{nome}_{i}", "nome": f"{chave} {prop}", "descricao": desc, "props": props}
        pecas[idx["WallNW"]]["props"] = [["CornerNorthWall", f"{nome}_{idx['WallN']}"],
                                         ["CornerWestWall", f"{nome}_{idx['WallW']}"]] + pecas[idx["WallNW"]]["props"]
        tema = {"cacos": "com cacos de vidro", "grade": "com grade"}.get(extra, "lisos")
        grupos.setdefault(f"Kit Brasil - Muros de quintal: {tema}", []).extend([
            [{"orient": "W", "tiles": {"0,0": idx["WallW"]}}, {"orient": "N", "tiles": {"0,0": idx["WallN"]}}],
            [{"orient": "W", "tiles": {"0,0": idx["WallNW"]}}],
            [{"orient": "W", "tiles": {"0,0": idx["WallSE"]}}],
        ])
    moveis = [{"grupo": g, "camada": "Walls", "itens": it} for g, it in grupos.items()]
    return kf._gravar(folha, nome, "parede", pecas, saida, {}, moveis=moveis)


if __name__ == "__main__":
    print(muros(Path(sys.argv[1]), Path(sys.argv[2])))
