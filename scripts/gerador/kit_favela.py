"""Kit Brasil, grupo "Morro e favela": peças para construir casas (só as peças).

Folhas geradas em `kits/tiles/` (cada uma com o .json do que é cada peça, as
propriedades do jogo e as entradas do BuildingEd):

- `rsb_paredes_favela_01`: 10 estilos de parede, no mesmo arranjo das paredes
  do jogo (por estilo: oeste, norte, quina, pilar; janela O/N, porta O/N; dois
  estilos por par de linhas). Formato e sombra vêm de uma parede lisa do jogo
  (`walls_interior_house_01`, peças 4-7 e 12-15); a textura é desenhada sobre
  cada face pela posição na parede (u ao longo, z de altura), com número inteiro
  de tijolos por tile, para emendar entre tiles e entre andares.
- `rsb_pisos_favela_01`: contrapiso, laje, cimento queimado, cerâmica barata.
- (Telhado inclinado de fibrocimento/zinco foi tirado a pedido do usuário: favela tem
  laje plana. A função `telhados()` ficou para uso futuro em outras construções.)
- `rsb_escadas_favela_01`: as escadas maciças do jogo (`fixtures_stairs_01`
  16-18/24-26 e 19-21/27-29) em concreto cru e cimento queimado vermelho.

Uso (Python do .venv do KnoxMap):
    python -I -X utf8 kit_favela.py <pasta Tiles/2x> <newtiledefinitions.tiles> <kits/tiles>
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit_tiles  # noqa: E402
import pisos_brasil as pb  # noqa: E402
import texturas_favela as tf  # noqa: E402

PX_M = 192 / 2.8          # pixels de altura por metro (um andar = 192 px)


# ---------------------------------------------------------------- ruído
def _h(a, b, s=0):
    a = np.asarray(a, dtype=np.int64)
    b = np.asarray(b, dtype=np.int64)
    h = (a * 374761393 + b * 668265263 + s * 2246822519) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFFFFFF) / 4294967295.0


def ruido(u, z, ku, kz, seed=0):
    """Ruído suave, periódico em u (ku células por tile) para emendar entre tiles."""
    gu, gz = u * ku, z * kz
    iu, iz = np.floor(gu).astype(int), np.floor(gz).astype(int)
    fu, fz = gu - iu, gz - iz
    fu, fz = fu * fu * (3 - 2 * fu), fz * fz * (3 - 2 * fz)
    a = _h(iu % ku, iz, seed)
    b = _h((iu + 1) % ku, iz, seed)
    c = _h(iu % ku, iz + 1, seed)
    d = _h((iu + 1) % ku, iz + 1, seed)
    return (a * (1 - fu) + b * fu) * (1 - fz) + (c * (1 - fu) + d * fu) * fz


def fbm(u, z, seed=0):
    return 0.5 * ruido(u, z, 4, 4, seed) + 0.3 * ruido(u, z, 9, 9, seed + 1) + 0.2 * ruido(u, z, 23, 23, seed + 2)


def grao(u, z, forca, seed):
    return (_h(np.floor(u * 140).astype(int) % 140, np.floor(z * 140).astype(int), seed) - 0.5) * 2 * forca


# ---------------------------------------------------------------- texturas de parede
def tijolos(u, z, por_tile, fiadas_andar, cor_bloco, cor_junta, junta=0.06, seed=0, sujo=0.0):
    """Tijolos/blocos em amarração (meia peça de deslocamento a cada fiada)."""
    fz = z / (192 / fiadas_andar)                          # z em px -> fiadas
    linha = np.floor(fz).astype(int)
    gu = u * por_tile + 0.5 * (linha % 2)
    col = np.floor(gu).astype(int)
    du, dz = gu - col, fz - linha
    var = 0.86 + 0.28 * _h(col % (2 * por_tile), linha, seed)
    cor = np.array(cor_bloco, dtype=float) * var[..., None]
    # tijolo baiano: furos não aparecem, mas a face tem leve sombra nas bordas
    borda_u = np.minimum(du, 1 - du) * (1 / por_tile)
    borda_z = np.minimum(dz, 1 - dz) * (192 / fiadas_andar / PX_M)
    j = junta * (0.7 + 0.6 * ruido(u, z / PX_M, 12, 8, seed + 9))   # argamassa irregular
    em_junta = (borda_u < j / 2) | (borda_z < j / 2)
    cor = np.where(em_junta[..., None], np.array(cor_junta, dtype=float) * (0.9 + 0.2 * _h(col, linha, seed + 4))[..., None], cor)
    cor = cor + grao(u, z / PX_M, 10, seed + 2)[..., None]
    if sujo:
        m = z / PX_M
        mancha = np.clip(1 - m / 0.6, 0, 1) * sujo + sujo * 0.5 * (fbm(u, m, seed + 7) > 0.62)
        cor = cor * (1 - 0.35 * mancha[..., None])
    return cor


def reboco(u, z, cor, seed=0, desbotado=0.25, descascado=0.0, tijolo=None):
    m = z / PX_M
    n = fbm(u, m, seed)
    cor = 0.78 * np.array(cor, dtype=float) + 0.22 * np.mean(cor)      # tinta barata, menos viva
    base = cor * (1 - desbotado * (n - 0.5))[..., None]
    base = base + grao(u, m, 7, seed + 3)[..., None]
    # escorrido de chuva (listras verticais escuras que descem do alto)
    escorre = ruido(u, m * 0.15, 17, 1, seed + 5) ** 3 * np.clip(m / 2.8, 0, 1)
    base = base * (1 - 0.25 * escorre[..., None])
    # sujeira perto do chão
    base = base * (1 - 0.3 * np.clip(1 - m / 0.5, 0, 1) * (0.6 + 0.4 * n))[..., None]
    if descascado and tijolo is not None:
        buraco = fbm(u, m, seed + 11) > (0.80 - descascado)
        base = np.where(buraco[..., None], tijolo(u, z), base)
    return base


def madeira(u, z, seed=0):
    m = z / PX_M
    # 5 tábuas por tile, larguras irregulares (periódico em u)
    bordas = np.cumsum([0.0] + [0.7 + 0.6 * _h(i, 0, seed) for i in range(5)])
    bordas = bordas / bordas[-1]
    idx = np.clip(np.searchsorted(bordas, u % 1.0, side="right") - 1, 0, 4)
    esq, dir_ = bordas[idx], bordas[idx + 1]
    cor_tab = np.array([[118, 98, 74], [104, 88, 70], [132, 112, 84], [96, 84, 70], [124, 104, 80]], dtype=float)
    cor = cor_tab[(idx + seed) % 5] * (0.9 + 0.2 * ruido(u, m, 5, 2, seed + idx.astype(int)))[..., None]
    veio = np.sin((u * 37 + ruido(u, m, 5, 3, seed + 2) * 6) * 2 * math.pi + m * 0.3) * 6
    cor = cor + veio[..., None] + grao(u, m, 8, seed + 4)[..., None]
    fresta = np.minimum(u % 1.0 - esq, dir_ - u % 1.0) < 0.012
    cor = np.where(fresta[..., None], np.array([34, 28, 24.0]), cor)
    # pregos e tábua de travessa a 0,4 m e 2,2 m
    trav = (np.abs(m - 0.4) < 0.05) | (np.abs(m - 2.2) < 0.05)
    cor = np.where(trav[..., None], cor * 0.85, cor)
    return cor


TIJOLO = lambda u, z: tijolos(u, z, 3, 14, (184, 106, 70), (148, 140, 126), 0.07, 1)
ESTILOS = [
    ("tijolo_baiano", "tijolo baiano aparente (laranja), argamassa grossa", "Brick", TIJOLO),
    ("tijolo_baiano_sujo", "tijolo baiano aparente, escurecido e sujo embaixo", "Brick",
     lambda u, z: tijolos(u, z, 3, 14, (166, 92, 60), (126, 120, 110), 0.08, 2, sujo=0.7)),
    ("bloco_concreto", "bloco de concreto aparente (cinza)", "Stone",
     lambda u, z: tijolos(u, z, 2, 12, (150, 148, 142), (118, 114, 108), 0.03, 3)),
    ("reboco_cru", "reboco cru / chapisco cinza, sem pintura", "Plaster",
     lambda u, z: reboco(u, z, (156, 152, 144), 4, 0.35)),
    ("reboco_rosa", "reboco pintado de rosa, desbotado e descascando", "Plaster",
     lambda u, z: reboco(u, z, (206, 150, 150), 5, 0.3, 0.12, TIJOLO)),
    ("reboco_azul", "reboco pintado de azul, desbotado", "Plaster",
     lambda u, z: reboco(u, z, (130, 164, 196), 6, 0.3, 0.08, TIJOLO)),
    ("reboco_verde_agua", "reboco verde-água, desbotado", "Plaster",
     lambda u, z: reboco(u, z, (140, 190, 172), 7, 0.3, 0.1, TIJOLO)),
    ("reboco_amarelo", "reboco amarelo, desbotado", "Plaster",
     lambda u, z: reboco(u, z, (214, 190, 112), 8, 0.3, 0.1, TIJOLO)),
    ("reboco_branco_encardido", "reboco branco encardido", "Plaster",
     lambda u, z: reboco(u, z, (214, 210, 198), 9, 0.4, 0.05, TIJOLO)),
    ("madeira_barraco", "tábuas de madeira de barraco", "Wood", lambda u, z: madeira(u, z, 10)),
]

# papel de cada uma das 8 peças de um estilo: (índice no molde, face, propriedade)
PAPEIS = [  # deslocamento dentro do bloco do estilo: 0..3 e 8..11
    (0, "W", "WallW"), (1, "N", "WallN"), (2, "NW", "WallNW"), (3, "SE", "WallSE"),
    (8, "W", "WindowW"), (9, "N", "WindowN"), (10, "W", "DoorWallW"), (11, "N", "DoorWallN"),
]
MOLDE_PAREDE = ("walls_interior_house_01", 4)     # estilo liso; peças 4-7 e 12-15


def _celula(im, i):
    return np.array(im.crop(((i % 8) * 128, (i // 8) * 256, (i % 8) * 128 + 128, (i // 8) * 256 + 256))).astype(float)


def _lum(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


def peca_parede(molde, face, tex):
    """Pinta `tex(u, z)` na face da parede do molde, mantendo forma e sombra dele."""
    alfa = molde[..., 3]
    L = _lum(molde)
    Y, X = np.mgrid[0:256, 0:128].astype(float)
    X, Y = X + 0.5, Y + 0.5
    uw = np.clip((63 - X) / 63, 0, 1)
    un = np.clip((X - 63) / 63, 0, 1)
    zw = 192 + 32 * uw - Y
    zn = 192 + 32 * un - Y
    if face == "W":
        oeste = np.ones_like(X, dtype=bool)
    elif face == "N":
        oeste = np.zeros_like(X, dtype=bool)
    else:                                   # quina e pilar: lado pela posição
        oeste = X < 63
    u = np.where(oeste, uw, un)
    z = np.clip(np.where(oeste, zw, zn), 0, 191.99)
    cor = tex(u, z)
    return cor, L, alfa


SS = 3                    # amostras por pixel em cada eixo (antisserrilhado)


def peca_parede_tex(molde, face, texs, Lref):
    """Peça de parede: forma e luz grande do molde do jogo, textura com relevo
    (`texs` = {"W": ..., "N": ...} de texturas_favela.parede_iluminada) lida
    com SS x SS amostras por pixel."""
    alfa = molde[..., 3]
    L = _lum(molde)
    acc = np.zeros((256, 128, 3))
    Y0, X0 = np.mgrid[0:256, 0:128].astype(float)
    for a in range(SS):
        for b in range(SS):
            X, Y = X0 + (a + 0.5) / SS, Y0 + (b + 0.5) / SS
            uw = np.clip((63 - X) / 63, 0, 0.9999)
            un = np.clip((X - 63) / 63, 0, 0.9999)
            zw, zn = 192 + 32 * uw - Y, 192 + 32 * un - Y
            if face == "W":
                oeste = np.ones_like(X, dtype=bool)
            elif face == "N":
                oeste = np.zeros_like(X, dtype=bool)
            else:
                oeste = X < 63
            # abaixo da linha do chão (espessura da parede) lê a textura espelhada
            cw = tf.amostrar_parede(texs["W"], uw, np.clip(np.abs(zw), 0, 191.9))
            cn = tf.amostrar_parede(texs["N"], un, np.clip(np.abs(zn), 0, 191.9))
            acc += np.where(oeste[..., None], cw, cn)
    cor = acc / (SS * SS)
    razao = np.clip(L / Lref, 0.35, 1.7)[..., None]
    img = np.zeros((256, 128, 4), dtype=np.uint8)
    img[..., :3] = np.clip(cor * razao, 0, 255).astype(np.uint8)
    img[..., 3] = alfa.astype(np.uint8)
    return Image.fromarray(img, "RGBA")


_TEX_CACHE: dict = {}


def texturas_estilo(chave, limpo=False):
    if (chave, limpo) not in _TEX_CACHE:
        _TEX_CACHE[(chave, limpo)] = tf.parede_iluminada(chave, limpo)
    return _TEX_CACHE[(chave, limpo)]


def paredes(tiles2x: Path, defs: dict, saida: Path, limpo: bool = True) -> dict:
    """Paredes da favela. `limpo` (padrão): só a textura base, folha
    `rsb_paredes_favela_01`; o desgaste vem como grime e manchas avulsas
    (`kit_desgaste.py`). `limpo=False`: com o desgaste pintado, folha
    `rsb_paredes_favela_desgaste_01` (rápido, mas repete em todo tile)."""
    molde_im = Image.open(tiles2x / f"{MOLDE_PAREDE[0]}.png").convert("RGBA")
    base = MOLDE_PAREDE[1]
    # referência de luz: mediana da face oeste lisa do molde
    w = _celula(molde_im, base)
    Lref = np.median(_lum(w)[w[..., 3] > 200])
    nome = "rsb_paredes_favela_01" if limpo else "rsb_paredes_favela_desgaste_01"
    linhas = ((len(ESTILOS) + 1) // 2) * 2
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{nome}_{i}", "props": []} for i in range(linhas * 8)]
    entradas = []
    for k, (chave, desc, material, _tex) in enumerate(ESTILOS):
        texs = texturas_estilo(chave, limpo)
        b = (k // 2) * 16 + (k % 2) * 4
        papel_nome = {}
        for off, face, prop in PAPEIS:
            i = b + off
            folha.alpha_composite(peca_parede_tex(_celula(molde_im, base + off), face, texs, Lref),
                                  ((i % 8) * 128, (i // 8) * 256))
            papel_nome[prop] = i
            props = [["MaterialType", material], [prop, ""], ["wall", ""]] if prop.startswith("Wall") else [[prop, ""], ["wall", ""]]
            pecas[i] = {"peca": f"{nome}_{i}", "nome": f"{chave} {prop}",
                        "descricao": desc if limpo else desc + " (com desgaste pintado)", "props": props}
        nw = papel_nome["WallNW"]
        pecas[nw]["props"] = [["CornerNorthWall", f"{nome}_{papel_nome['WallN']}"],
                              ["CornerWestWall", f"{nome}_{papel_nome['WallW']}"]] + pecas[nw]["props"]
        entradas.append({"West": papel_nome["WallW"], "North": papel_nome["WallN"], "NorthWest": nw,
                         "SouthEast": papel_nome["WallSE"], "WestWindow": papel_nome["WindowW"],
                         "NorthWindow": papel_nome["WindowN"], "WestDoor": papel_nome["DoorWallW"],
                         "NorthDoor": papel_nome["DoorWallN"]})
    return _gravar(folha, nome, "parede", pecas, saida,
                   {"exterior_walls": entradas, "interior_walls": entradas})


# ---------------------------------------------------------------- pisos e laje
def peca_piso(cor_h, tiles2x: Path) -> Image.Image:
    """Piso do jogo (losango 126 x 64 na peça 128 x 256) a partir de (cor, altura)."""
    tex = tf.piso_iluminado(*cor_h)
    ys, xs = np.mgrid[192:256, 0:128].astype(float)
    acc = np.zeros(xs.shape + (3,))
    for a in range(SS):
        for b in range(SS):
            X, Y = xs + (a + 0.5) / SS, ys + (b + 0.5) / SS
            u, v = (X - 63.0) / 63.0, (Y - 192.0) / 32.0
            s, t = (u + v) / 2, (v - u) / 2
            acc += tf.amostrar_piso(tex, s, t)
    out = np.zeros((256, 128, 4), dtype=np.uint8)
    out[192:256, :, :3] = np.clip(acc / (SS * SS), 0, 255).astype(np.uint8)
    out[..., 3] = pb.cal.mascara(tiles2x)
    return Image.fromarray(out, "RGBA")


PISOS = [
    ("contrapiso_a", "contrapiso de cimento grosso (sem acabamento)", lambda: tf.contrapiso(21)),
    ("contrapiso_b", "contrapiso de cimento rachado", lambda: tf.contrapiso(22, rachado=True)),
    ("laje_a", "laje de concreto (chão do andar de cima e telhado plano)", lambda: tf.laje_crua(23)),
    ("laje_b", "laje de concreto com poça", lambda: tf.laje_crua(24, poca=True)),
    ("cimento_queimado_vermelho", "cimento queimado vermelho", lambda: tf.cimento_queimado((172, 62, 50), 25)),
    ("cimento_queimado_verde", "cimento queimado verde", lambda: tf.cimento_queimado((80, 122, 86), 26)),
    ("ceramica_vermelha_barata", "cerâmica vermelha barata 30 x 30",
     lambda: tf.ceramica([(150, 66, 50), (142, 60, 46), (158, 72, 54)], 27, (176, 170, 156), quebrada=0.0)),
    ("ceramica_bege_barata", "cerâmica bege barata 30 x 30",
     lambda: tf.ceramica([(208, 194, 166), (200, 186, 160)], 28, (160, 154, 140), quebrada=0.0)),
]


def pisos(tiles2x: Path, saida: Path) -> dict:
    nome = "rsb_pisos_favela_01"
    folha = Image.new("RGBA", (1024, 256), (0, 0, 0, 0))
    pecas = []
    for n, (chave, desc, f) in enumerate(PISOS):
        folha.alpha_composite(peca_piso(f(), tiles2x), ((n % 8) * 128, 0))
        interior = chave.startswith(("ceramica", "cimento"))
        props = [["diamondFloor", ""], ["solidfloor", ""]] + ([] if interior else [["exterior", ""]])
        pecas.append({"peca": f"{nome}_{n}", "nome": chave, "descricao": desc, "props": props})
    laje_i = 2
    topos = [{"West1": laje_i, "West2": laje_i, "West3": laje_i, "North1": laje_i, "North2": laje_i,
              "North3": laje_i, "_offset": True}]
    return _gravar(folha, nome, "piso", pecas, saida,
                   {"floors": [{"Floor": i} for i in range(len(PISOS))], "roof_tops": topos})


# ---------------------------------------------------------------- recolorir folhas do jogo
def recolorir(tiles2x: Path, defs: dict, molde: str, nome: str, tipo: str, cor_de, so: list | None,
              saida: Path, mapa: dict | None = None) -> dict:
    """Recolore uma folha do jogo mantendo forma e sombra (luminância).
    `mapa`: {índice novo: índice no molde} (só essas peças); sem ele, a folha inteira."""
    im = Image.open(tiles2x / f"{molde}.png").convert("RGBA")
    a = np.array(im).astype(float)
    alfa = a[..., 3] > 0
    Lref = np.median(_lum(a)[alfa]) if alfa.any() else 128
    sd = defs[molde]
    if mapa is None:
        mapa = {i: i for i in range(sd["colunas"] * sd["linhas"])}
    linhas = max(mapa) // 8 + 1
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{nome}_{i}", "props": []} for i in range(linhas * 8)]
    for novo, velho in mapa.items():
        cel = _celula(im, velho)
        if not (cel[..., 3] > 0).any():
            continue
        L = _lum(cel)
        Y, X = np.mgrid[0:256, 0:128]
        cor = cor_de(novo, X, Y, L / Lref)
        img = np.zeros((256, 128, 4), dtype=np.uint8)
        img[..., :3] = np.clip(cor, 0, 255).astype(np.uint8)
        img[..., 3] = cel[..., 3].astype(np.uint8)
        folha.alpha_composite(Image.fromarray(img, "RGBA"), ((novo % 8) * 128, (novo // 8) * 256))
        props = [[k, v.replace(molde, nome) if v.startswith(molde) else v] for k, v in sd["pecas"][velho]]
        pecas[novo] = {"peca": f"{nome}_{novo}", "props": props}
    return {"folha": folha, "nome": nome, "tipo": tipo, "pecas": pecas, "mapa": mapa}


def telhados(tiles2x: Path, defs: dict, saida: Path, bt_texto: str) -> list:
    out = []
    # entrada do BuildingEd do roofs_03 (inclinações): copiada trocando o nome
    entrada = _entrada_bt(bt_texto, "roof_slopes", "roofs_03_")
    for nome, desc, base, ferrugem in (
            ("rsb_telhado_fibrocimento_01", "telha ondulada de fibrocimento (cinza)", (140, 140, 134), 0.0),
            ("rsb_telhado_zinco_01", "telha de zinco com ferrugem", (122, 128, 134), 0.45)):
        def cor_de(i, X, Y, r, base=base, ferrugem=ferrugem, seed=len(out)):
            c = np.array(base, dtype=float) * np.clip(r, 0.3, 1.45)[..., None]
            c = c + grao(X / 128, Y / 128, 6, seed + i)[..., None]
            if ferrugem:
                f = fbm(X / 128 + i * 0.37, Y / 128, seed + 40)
                mistura = np.clip((f - (1 - ferrugem)) * 4, 0, 1)[..., None]
                c = c * (1 - mistura) + np.array([118, 62, 34.0]) * np.clip(r, 0.3, 1.45)[..., None] * mistura
            return c
        r = recolorir(tiles2x, defs, "roofs_03", nome, "telhado", cor_de, None, saida)
        for p in r["pecas"]:
            if p["props"]:
                p["descricao"] = desc
        bt = {k: (v.replace("roofs_03_", f"{nome}_") if v.startswith("roofs_03_") else "") for k, v in entrada.items()}
        out.append(_gravar(r["folha"], nome, "telhado", r["pecas"], saida, {"roof_slopes": [bt]}, bruto=True))
    return out


def escadas(tiles2x: Path, defs: dict, saida: Path) -> dict:
    # estilo A: escada maciça escura (16-18 oeste, 24-26 norte) -> concreto cru
    # estilo B: escada maciça clara (19-21, 27-29) -> cimento queimado vermelho
    mapa = {0: 16, 1: 17, 2: 18, 8: 24, 9: 25, 10: 26, 3: 19, 4: 20, 5: 21, 11: 27, 12: 28, 13: 29}

    def cor_de(i, X, Y, r):
        cru = i in (0, 1, 2, 8, 9, 10)
        base = np.array((158, 154, 146) if cru else (128, 54, 46), dtype=float)
        u, v = X / 128.0, Y / 256.0
        c = base * np.clip(r, 0.3, 1.5 if cru else 1.22)[..., None]
        c = c * (0.9 + 0.18 * tf.fbm(u, v, 4, 8, 4, 50 + i))[..., None]           # manchas
        poro, _ = tf.pontos(u, v, 64, 128, 0.5, 0.45 if cru else 0.15, 60 + i)
        c = c * (1 - 0.3 * poro)[..., None]                                        # poros
        gasto = tf.sstep(1.15, 1.45, r)                                            # quina dos degraus gasta
        c = tf.mistura(c, np.minimum(c * 1.18 + 8, 255), gasto * (0.5 if cru else 0.25))
        canto = tf.sstep(0.75, 0.45, r)                                            # sujeira nos cantos
        c = c * (1 - 0.25 * canto)[..., None]
        if not cru:                                                                # tinta vermelha gasta no meio do degrau
            pe = tf.sstep(0.6, 0.8, tf.fbm(u, v, 3, 6, 4, 70 + i))
            c = tf.mistura(c, np.array([112, 92, 82.0]) * np.clip(r, 0.3, 1.2)[..., None], pe * 0.35)
        return c + grao(X / 128, Y / 128, 4, 50 + i)[..., None]
    nome = "rsb_escadas_favela_01"
    r = recolorir(tiles2x, defs, "fixtures_stairs_01", nome, "escada", cor_de, None, saida, mapa)
    for p in r["pecas"]:
        p["props"] = [[k, ("Stone" if k.startswith("Material") else v)] for k, v in p["props"]]
        if p["props"]:
            p["descricao"] = "escada maciça de concreto"
    bt = [{"West1": 0, "West2": 1, "West3": 2, "North1": 8, "North2": 9, "North3": 10},
          {"West1": 3, "West2": 4, "West3": 5, "North1": 11, "North2": 12, "North3": 13}]
    return _gravar(r["folha"], nome, "escada", r["pecas"], saida, {"stairs": bt})


# ---------------------------------------------------------------- gravação
def _entrada_bt(texto: str, categoria: str, prefixo: str) -> dict:
    """A 1ª entrada da categoria do BuildingTiles.txt que usa peças com `prefixo`."""
    ini = texto.index(f"name = {categoria}")
    pos = texto.index(prefixo, ini)
    a = texto.rindex("entry", 0, pos)
    b = texto.index("}", pos)
    out = {}
    for l in texto[a:b].splitlines()[2:]:
        if "=" in l:
            k, v = (x.strip() for x in l.split("=", 1))
            out[k] = v
    return out


def _gravar(folha, nome, tipo, pecas, saida: Path, buildingtiles: dict, bruto=False, moveis=None) -> dict:
    """`moveis`: grupos para a lista de móveis do BuildingEd (BuildingFurniture.txt):
    [{"grupo": rótulo, "camada": opcional, "itens": [[{"orient", "tiles": {"x,y": índice}}]]}]."""
    saida.mkdir(parents=True, exist_ok=True)
    import estilo_pz  # filtro de estilo do jogo (D-46); peças de conjunto sem contorno na emenda
    juntas = {i for i, pc in enumerate(pecas) if str(pc.get("nome", "")).startswith(("letreiro", "quadro"))}
    estilo_pz.filtrar_folha(folha, tipo, sem_contorno=juntas).save(saida / f"{nome}.png")
    man = {"folha": nome, "tipo": tipo, "pecas": pecas, "buildingtiles": buildingtiles, "bt_nomes_prontos": bruto,
           "moveis": moveis or [], "estilo": estilo_pz.ESTILO}
    (saida / f"{nome}.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(1 for p in pecas if p.get("props"))
    return {"folha": nome, "pecas": n}


def previa(saida: Path, nomes: list[str], destino: Path) -> None:
    ims = [Image.open(saida / f"{n}.png").convert("RGBA") for n in nomes]
    alt = sum(min(im.height, 1024) for im in ims) // 2
    out = Image.new("RGBA", (512, alt), (70, 92, 70, 255))
    y = 0
    for im in ims:
        c = im.crop((0, 0, 1024, min(im.height, 1024)))
        c = c.resize((512, c.height // 2))
        out.alpha_composite(c, (0, y))
        y += c.height
    out.save(destino)


if __name__ == "__main__":
    tiles2x, tdefs, saida = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    defs = {d["nome"]: d for d in kit_tiles.ler_definicoes(tdefs)}
    bt = (tiles2x.parent.parent / "config" / "BuildingTiles.txt").read_text(encoding="utf-8", errors="replace")
    # telhado inclinado saiu (usuário, 08/11/2026): favela tem laje plana; ver kit_laje.py
    res = [paredes(tiles2x, defs, saida), paredes(tiles2x, defs, saida, limpo=False),
           pisos(tiles2x, saida), escadas(tiles2x, defs, saida)]
    print(json.dumps(res, ensure_ascii=False))
