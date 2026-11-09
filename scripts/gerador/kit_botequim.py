"""Kit Brasil, botequim de esquina (pedido do usuário, 09/11/2026).

Nome do bar (fictício): "Bar Ponto Certo". Folhas em `kits/tiles/`:

- `rsb_paredes_botequim_01` (parede): 4 estilos com as 8 peças de sempre
  (parede, janela e porta, faces oeste e norte, quina e pilar), molde
  `walls_interior_house_01` como na favela:
  azulejo branco com faixa verde até 1,6 m e tinta creme em cima (salão),
  azulejo verde-claro com tinta branca (cozinha e banheiro),
  fachada amarela e fachada verde, as duas com barra de cerâmica vermelha.
- `rsb_pisos_botequim_01` (piso): ladrilho hidráulico, xadrez preto e branco,
  granilite e lajota vermelha.
- `rsb_botequim_01` (objeto, renderizador 3D de `kit_laje.py`):
  balcão de azulejo com tampo de granito e balcão com estufa de salgados
  (4 lados; propriedades do balcão de bar do jogo, `location_restaurant_bar_01`),
  freezer horizontal de sorvete (4 lados; do freezer `appliances_refrigeration_01`
  48-51), cervejeira de porta de vidro (2 lados; da geladeira industrial 22-23),
  cadeiras de plástico amarela e branca (4 lados; da cadeira de plástico
  `furniture_seating_outdoor_01` 16-19), mesas de plástico amarela e branca,
  engradados de cerveja e pilha de cadeiras, letreiro do bar em 2 peças
  (fachada para o sul e para o leste), lousa de cardápio, porta de enrolar
  aberta (rolo) e fechada (parede norte e oeste).

Lados: "Facing" igual ao do jogo. S = a frente do móvel para o sul (embaixo à
esquerda na tela), L = leste (embaixo à direita), N e O = de costas.

Uso: python -I -X utf8 kit_botequim.py <pasta Tiles/2x> <newtiledefinitions.tiles> <kits/tiles>
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit_favela as kf  # noqa: E402
import kit_laje as kl  # noqa: E402
import kit_tiles  # noqa: E402
import texturas_favela as tf  # noqa: E402

PX_M = tf.PX_M
NOME_BAR = "BAR PONTO CERTO"
FONTE = "C:/Windows/Fonts/arialbd.ttf"
FONTE_GIZ = "C:/Windows/Fonts/segoeprb.ttf"


# ================================================================ paredes
def _azulejos(U, Z, cor, por_tile, linha_px, seed, junta=(196, 194, 186)):
    """Azulejo quadrado: (cor, altura) na grade da parede."""
    gu, gz = U * por_tile, Z / linha_px
    i, j = np.floor(gu), np.floor(gz)
    fu, fz = gu - i, gz - j
    lado = 63.0 / por_tile
    borda = np.minimum(np.minimum(fu, 1 - fu) * lado, np.minimum(fz, 1 - fz) * linha_px)
    peca = borda > 0.55
    var = tf._h(i.astype(np.int64) % por_tile, j.astype(np.int64), seed)
    c = np.array(cor, float) * (0.95 + 0.07 * var)[..., None]
    brilho = tf.sstep(0.5, 1.0, (1 - fu) * 0.6 + fz * 0.4)
    c = c * (1 + 0.07 * brilho)[..., None]
    h = -0.7 * (1 - tf.sstep(0.55, 1.6, borda))
    # azulejo trincado ou faltando (pé-sujo)
    falta = tf._h(i.astype(np.int64) % por_tile, j.astype(np.int64), seed + 9) < 0.025
    c = np.where(falta[..., None], np.array([150, 146, 138.0]), c)
    h = np.where(falta, -1.4, h)
    jc = np.array(junta, float)
    c = np.where(peca[..., None], c, jc)
    h = np.where(peca, h, -1.0)
    return c, h


def _sujo(U, Z, cor, h, seed, forca):
    if True:                    # D-47: gordura e sujeira vão na folha rsb_overlay_grime_wall_01
        return cor, h
    v = Z / 192
    gordura = tf.sstep(0.6, 0.85, tf.fbm(U, v, 3, 4, 4, seed)) * forca
    cor = tf.mistura(cor, np.array([150, 126, 84.0]), gordura * 0.35)
    base = tf.sstep(0.3, 0.0, Z / PX_M) * forca
    return tf.mistura(cor, np.array([90, 80, 66.0]), base * 0.5), h


def azulejo_salao(cor_az, cor_faixa, tinta, seed):
    U, Z = tf.grade_parede()
    alto = 1.6 * PX_M
    linha = 192 / 18
    ca, ha = _azulejos(U, Z, cor_az, 6, linha, seed)
    cf, hf = _azulejos(U, Z, cor_faixa, 6, linha, seed + 1)
    ct, ht = tf.reboco_pintado(tinta, seed + 2, 0.04, None, limpo=True)
    faixa = (Z >= alto - linha) & (Z < alto)
    rodape = Z < linha * 0.9
    cor = np.where((Z < alto)[..., None], ca, ct)
    h = np.where(Z < alto, ha, ht * 0.6)
    cor = np.where(faixa[..., None], cf, cor)
    h = np.where(faixa, hf, h)
    cor = np.where(rodape[..., None], cf * 0.75, cor)
    # quina do azulejo saliente (sombra embaixo da tinta)
    h = np.where(np.abs(Z - alto) < 1.2, h + 0.8, h)
    return _sujo(U, Z, cor, h, seed + 3, 0.7)


def fachada(tinta, seed):
    U, Z = tf.grade_parede()
    barra = 1.0 * PX_M
    ct, ht = tf.reboco_pintado(tinta, seed, 0.07, None, limpo=True)
    # barra de cerâmica vermelha 10 x 20 deitada, em amarração
    gz = Z / (192 / 20)
    j = np.floor(gz)
    gu = U * 5 + 0.5 * (j % 2)
    i = np.floor(gu)
    fu, fz = gu - i, gz - j
    borda = np.minimum(np.minimum(fu, 1 - fu) * 63 / 5, np.minimum(fz, 1 - fz) * 192 / 20)
    var = tf._h(i.astype(np.int64) % 5, j.astype(np.int64), seed + 1)
    cc = np.array([156, 64, 46.0]) * (0.9 + 0.18 * var)[..., None]
    cc = cc * (1 + 0.06 * tf.sstep(0.4, 1, 1 - fu))[..., None]
    cc = np.where((borda > 0.6)[..., None], cc, np.array([176, 170, 156.0]))
    hc = np.where(borda > 0.6, 0.0, -1.0)
    em = Z < barra
    cor = np.where(em[..., None], cc, ct)
    h = np.where(em, hc, ht * 0.6)
    h = np.where(np.abs(Z - barra) < 1.2, h + 0.9, h)
    return cor, h                        # limpo (D-47)


ESTILOS = [
    ("azulejo_branco_faixa_verde", "salão: azulejo branco até 1,6 m, faixa verde, tinta creme", "Ceramic",
     lambda: azulejo_salao((236, 236, 230), (40, 120, 76), (226, 214, 180), 61)),
    ("azulejo_verde_claro", "cozinha e banheiro: azulejo verde-claro, tinta branca", "Ceramic",
     lambda: azulejo_salao((176, 214, 190), (120, 168, 140), (226, 224, 216), 62)),
    ("fachada_amarela", "fachada amarela com barra de cerâmica vermelha", "Plaster",
     lambda: fachada((222, 186, 70), 63)),
    ("fachada_verde", "fachada verde com barra de cerâmica vermelha", "Plaster",
     lambda: fachada((54, 128, 82), 64)),
]


def _iluminar(cor, h):
    out = {}
    for face, lu in (("W", 0.35), ("N", -0.35)):
        luz = np.array([lu, 0.55, 0.76])
        luz = luz / np.linalg.norm(luz)
        f = tf.relevo(h, 63.0 / tf.WALL_U, 192.0 / tf.WALL_Z, luz) * tf.oclusao(h)
        out[face] = np.clip(cor * f[..., None], 0, 255)
    return out


def paredes(tiles2x: Path, saida: Path) -> dict:
    molde_im = Image.open(tiles2x / f"{kf.MOLDE_PAREDE[0]}.png").convert("RGBA")
    base = kf.MOLDE_PAREDE[1]
    w = kf._celula(molde_im, base)
    Lref = np.median(kf._lum(w)[w[..., 3] > 200])
    nome = "rsb_paredes_botequim_01"
    linhas = ((len(ESTILOS) + 1) // 2) * 2
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{nome}_{i}", "props": []} for i in range(linhas * 8)]
    entradas = []
    for k, (chave, desc, material, f) in enumerate(ESTILOS):
        texs = _iluminar(*f())
        b = (k // 2) * 16 + (k % 2) * 4
        papel = {}
        for off, face, prop in kf.PAPEIS:
            i = b + off
            folha.alpha_composite(kf.peca_parede_tex(kf._celula(molde_im, base + off), face, texs, Lref),
                                  ((i % 8) * 128, (i // 8) * 256))
            papel[prop] = i
            props = ([["MaterialType", material], [prop, ""], ["wall", ""]] if prop.startswith("Wall")
                     else [[prop, ""], ["wall", ""]])
            pecas[i] = {"peca": f"{nome}_{i}", "nome": f"{chave} {prop}", "descricao": desc, "props": props}
        nw = papel["WallNW"]
        pecas[nw]["props"] = [["CornerNorthWall", f"{nome}_{papel['WallN']}"],
                              ["CornerWestWall", f"{nome}_{papel['WallW']}"]] + pecas[nw]["props"]
        entradas.append({"West": papel["WallW"], "North": papel["WallN"], "NorthWest": nw,
                         "SouthEast": papel["WallSE"], "WestWindow": papel["WindowW"],
                         "NorthWindow": papel["WindowN"], "WestDoor": papel["DoorWallW"],
                         "NorthDoor": papel["DoorWallN"]})
    return kf._gravar(folha, nome, "parede", pecas, saida,
                      {"exterior_walls": entradas, "interior_walls": entradas})


# ================================================================ pisos
def ladrilho_hidraulico(seed=71):
    """Ladrilho de 20 cm (5 por tile) com flor de 4 pétalas, vermelho, ocre e creme."""
    S, T = tf.grade_piso()
    n = 5
    gs, gt = S * n, T * n
    fs, ft = gs - np.floor(gs), gt - np.floor(gt)
    x, y = fs - 0.5, ft - 0.5
    r = np.hypot(x, y)
    ang = np.arctan2(y, x)
    creme, verm, ocre, preto = (np.array(c, float) for c in ((222, 208, 176), (150, 52, 40), (196, 146, 58), (52, 48, 44)))
    cor = np.broadcast_to(creme, S.shape + (3,)).copy()
    petala = r < 0.17 + 0.13 * np.abs(np.cos(2 * ang))
    cor = np.where(petala[..., None], verm, cor)
    cor = np.where((r < 0.08)[..., None], ocre, cor)
    canto = (np.abs(x) > 0.36) & (np.abs(y) > 0.36)
    cor = np.where(canto[..., None], ocre, cor)
    aro = np.abs(np.maximum(np.abs(x), np.abs(y)) - 0.44) < 0.015
    cor = np.where(aro[..., None], preto, cor)
    cor = cor * (0.9 + 0.12 * tf.fbm(S, T, 4, 4, 4, seed))[..., None]
    gasto = tf.sstep(0.55, 0.8, tf.fbm(S, T, 2, 2, 4, seed + 1))
    cor = tf.mistura(cor, np.array([180, 170, 150.0]), gasto * 0.35)
    borda = np.minimum(np.minimum(fs, 1 - fs), np.minimum(ft, 1 - ft)) * tf.PX_PISO / n
    junta = borda < 0.5
    cor = np.where(junta[..., None], cor * 0.7, cor)
    h = np.where(junta, -0.8, 0.0)
    return cor, h


def xadrez(seed=72):
    S, T = tf.grade_piso()
    n = 4
    i, j = np.floor(S * n), np.floor(T * n)
    preto = ((i + j) % 2) == 1
    cor = np.where(preto[..., None], np.array([40, 40, 42.0]), np.array([226, 224, 216.0]))
    cor = cor * (0.95 + 0.08 * tf.vn(S, T, 60, 60, seed))[..., None]
    fs, ft = S * n - i, T * n - j
    brilho = tf.sstep(0.6, 1.0, (1 - fs) * 0.5 + (1 - ft) * 0.5)
    cor = cor + 18 * brilho[..., None]
    sujo = tf.sstep(0.5, 0.8, tf.fbm(S, T, 3, 3, 4, seed + 1))
    cor = tf.mistura(cor, np.array([120, 110, 92.0]), sujo * 0.25)
    borda = np.minimum(np.minimum(fs, 1 - fs), np.minimum(ft, 1 - ft)) * tf.PX_PISO / n
    junta = borda < 0.45
    cor = np.where(junta[..., None], np.array([130, 126, 118.0]), cor)
    return cor, np.where(junta, -0.7, 0.0)


def granilite(seed=73):
    S, T = tf.grade_piso()
    cor = np.array([176, 172, 162.0]) * (0.92 + 0.1 * tf.fbm(S, T, 3, 3, 4, seed))[..., None]
    for k, (c, prob) in enumerate((((60, 58, 56), 0.35), ((236, 232, 222), 0.35), ((150, 96, 70), 0.15))):
        p, _ = tf.pontos(S, T, 70, 70, 0.32, prob, seed + 1 + k)
        cor = tf.mistura(cor, np.array(c, float), p * 0.85)
    junta = (np.minimum(S, 1 - S) * tf.PX_PISO < 0.7) | (np.minimum(T, 1 - T) * tf.PX_PISO < 0.7)
    cor = np.where(junta[..., None], np.array([186, 150, 80.0]), cor)       # junta de latão
    return cor, np.where(junta, 0.3, 0.0)


PISOS = [
    ("ladrilho_hidraulico", "ladrilho hidráulico (flor vermelha e ocre)", ladrilho_hidraulico),
    ("xadrez_preto_branco", "piso xadrez preto e branco", xadrez),
    ("granilite", "granilite com junta de latão", granilite),
    ("lajota_vermelha", "lajota vermelha de barro",
     lambda: tf.ceramica([(146, 58, 40), (138, 54, 38), (154, 64, 44)], 74, (120, 110, 98), por_tile=3)),
]


def pisos(tiles2x: Path, saida: Path) -> dict:
    nome = "rsb_pisos_botequim_01"
    folha = Image.new("RGBA", (1024, 256), (0, 0, 0, 0))
    pecas = []
    for n, (chave, desc, f) in enumerate(PISOS):
        folha.alpha_composite(kf.peca_piso(f(), tiles2x), ((n % 8) * 128, 0))
        pecas.append({"peca": f"{nome}_{n}", "nome": chave, "descricao": desc,
                      "props": [["diamondFloor", ""], ["solidfloor", ""]]})
    pecas += [{"peca": f"{nome}_{n}", "props": []} for n in range(len(PISOS), 8)]
    return kf._gravar(folha, nome, "piso", pecas, saida, {"floors": [{"Floor": i} for i in range(len(PISOS))]})


# ================================================================ objetos 3D
def girar(c: kl.Cena, lado: str) -> kl.Cena:
    """Desenho feito com a frente para o sul (S); gira para L, N ou O (sem espelhar)."""
    if lado == "S":
        return c
    for k in range(len(c.p)):
        p, n = c.p[k].copy(), np.array(c.n[k], float).copy()
        x, y, nx, ny = p[:, 0].copy(), p[:, 1].copy(), n[:, 0].copy(), n[:, 1].copy()
        if lado == "L":
            p[:, 0], p[:, 1], n[:, 0], n[:, 1] = y, 1 - x, ny, -nx
        elif lado == "N":
            p[:, 0], p[:, 1], n[:, 0], n[:, 1] = 1 - x, 1 - y, -nx, -ny
        else:  # O
            p[:, 0], p[:, 1], n[:, 0], n[:, 1] = 1 - y, x, -ny, nx
        c.p[k], c.n[k] = p, n
    return c


def texto_img(linhas, larg, alt, fundo, borda=None):
    """Imagem com linhas de texto: [(texto, cor, fração da altura, fonte)]."""
    im = Image.new("RGB", (larg, alt), fundo)
    d = ImageDraw.Draw(im)
    if borda:
        cor_b, esp = borda
        d.rectangle((0, 0, larg - 1, alt - 1), outline=cor_b, width=esp)
    y = int(alt * 0.08)
    for txt, cor, frac, fonte in linhas:
        tam = int(alt * frac)
        fnt = ImageFont.truetype(fonte, tam)
        while d.textlength(txt, font=fnt) > larg * 0.9 and tam > 8:
            tam -= 2
            fnt = ImageFont.truetype(fonte, tam)
        w = d.textlength(txt, font=fnt)
        d.text(((larg - w) / 2, y), txt, fill=cor, font=fnt)
        y += int(tam * 1.18)
    return np.array(im, dtype=float)


def amostra(img, u, v):
    """u, v em 0..1 (v = 0 embaixo)."""
    h, w = img.shape[:2]
    iu = np.clip((u * w).astype(int), 0, w - 1)
    iv = np.clip(((1 - v) * h).astype(int), 0, h - 1)
    return img[iv, iu]


def azulejo_obj(cor, n_por_m=7, seed=0):
    cor = np.array(cor, float)

    def f(u, v, face):
        if face == "topo":
            return np.broadcast_to(cor, np.shape(u) + (3,))
        gu, gv = u * n_por_m, v * n_por_m
        fu, fv = gu - np.floor(gu), gv - np.floor(gv)
        junta = (np.minimum(fu, 1 - fu) < 0.035) | (np.minimum(fv, 1 - fv) < 0.035)
        var = tf._h(np.floor(gu).astype(np.int64) % 64, np.floor(gv).astype(np.int64) % 64, seed)
        c = cor * (0.94 + 0.08 * var)[..., None]
        return np.where(junta[..., None], np.array([200, 198, 190.0]), c)
    return f


def granito(seed=0):
    def f(u, v, face):
        base = np.array([64, 60, 58.0]) * (0.85 + 0.3 * tf.vn(u % 1, v % 1, 40, 40, seed))[..., None]
        p, _ = tf.pontos(u % 1, v % 1, 120, 120, 0.4, 0.35, seed + 1)
        return tf.mistura(base, np.array([196, 186, 176.0]), p * 0.7)
    return f


def balcao(lado, estufa=False, seed=81):
    """Balcão de bar: frente de azulejo branco com faixa verde (cliente), atrás
    prateleira aberta com garrafas, tampo de granito escuro. Desenho com a frente
    para o sul; `girar` faz os outros lados."""
    c = kl.Cena()
    topo = 1.05
    verde = np.array([40, 120, 76.0])
    az = azulejo_obj((244, 244, 238), 5, seed)

    def frente(u, v, face):
        cor = az(u, v, face)
        faixa = (v > 0.78) & (v < 0.86)
        cor = np.where(faixa[..., None], verde * (0.95 + 0.08 * (np.sin(u * 44) > 0))[..., None], cor)
        return np.where((v < 0.1)[..., None], np.array([60, 54, 48.0]), cor)
    # corpo de azulejo (lado do cliente) e, atrás, o vão das prateleiras do balconista
    c.caixa(0.0, 0.52, 0.0, 1.0, 0.86, topo - 0.05, None, frente, faces=("x0", "x1", "y1"))
    madeira = np.array([118, 80, 50.0])
    c.caixa(0.0, 0.5, 0.0, 1.0, 0.52, topo - 0.05, np.array([150, 140, 120.0]), faces=("y0",))
    for x in (0.0, 0.97):                               # laterais do vão
        c.caixa(x, 0.16, 0.0, x + 0.03, 0.52, topo - 0.05, madeira, faces=("x0", "x1", "y0"))
    c.caixa(0.0, 0.16, 0.0, 1.0, 0.52, 0.06, np.array([60, 54, 48.0]), faces=("y0",))
    for z in (0.06, 0.5):
        c.caixa(0.03, 0.18, z, 0.97, 0.5, z + 0.03, madeira, faces=("topo", "y0"))
    rnd = np.random.default_rng(seed)
    for z in (0.09, 0.53):
        for k in range(9):
            x = 0.08 + k * 0.1
            cor = np.array([[70, 40, 20], [30, 80, 40], [200, 190, 160], [90, 30, 30]][rnd.integers(4)], float)
            alt = 0.26 + 0.06 * rnd.random()
            c.haste((x, 0.32, z), (x, 0.32, z + alt * 0.7), 0.028, cor, 0.6)
            c.haste((x, 0.32, z + alt * 0.7), (x, 0.32, z + alt), 0.011, cor, 0.6)
    # tampo de granito com sobra para o cliente
    c.caixa(0.0, 0.14, topo - 0.05, 1.0, 0.94, topo, None, granito(seed + 2), brilho=0.5)
    if estufa:
        # estufa de salgados: caixa de vidro com luz quente e coxinhas
        z0 = topo
        aco = np.array([180, 182, 186.0])
        c.caixa(0.12, 0.3, z0, 0.88, 0.78, z0 + 0.04, aco, brilho=0.6)
        c.caixa(0.12, 0.3, z0 + 0.36, 0.88, 0.78, z0 + 0.4, aco, brilho=0.6)
        for x in (0.12, 0.86):
            for y in (0.3, 0.76):
                c.caixa(x, y, z0, x + 0.02, y + 0.02, z0 + 0.38, aco, brilho=0.6)
        quente = np.array([250, 214, 150.0])
        c.caixa(0.14, 0.32, z0 + 0.04, 0.86, 0.76, z0 + 0.05, quente, faces=("topo",))
        for k in range(14):
            x = 0.2 + (k % 7) * 0.09
            y = 0.42 + (k // 7) * 0.2
            r = 0.035
            c.revolucao(x, y, lambda z, z0=z0, r=r: r * np.clip(np.sin(np.clip((z - z0 - 0.05) / 0.09, 0, 1) * math.pi * 0.95 + 0.15), 0.05, 1),
                        z0 + 0.05, z0 + 0.14, np.array([196, 120, 50.0]), passo=0.004, brilho=0.4)
        # vidro: reflexos brancos inclinados na frente
        for k in range(3):
            x0 = 0.25 + k * 0.22
            c.haste((x0, 0.785, z0 + 0.06), (x0 + 0.08, 0.785, z0 + 0.32), 0.004, np.array([240, 246, 250.0]), 0.8)
    return girar(c, lado).render()


def freezer(lado, seed=83):
    """Freezer horizontal de sorvete: branco, tampa de vidro azulada, faixa azul e
    "SORVETES" na frente, grade do motor atrás."""
    c = kl.Cena()
    branco = np.array([228, 228, 222.0])
    txt = texto_img([("SORVETES", (255, 255, 255), 0.55, FONTE)], 600, 160, (36, 98, 178))

    def frente(u, v, face):
        cor = np.broadcast_to(branco, np.shape(u) + (3,)).copy()
        if face != "y1":
            return cor
        uu, vv = (u - 0.1) / 0.8, (v - 0.32) / 0.3
        dentro = (uu > 0) & (uu < 1) & (vv > 0) & (vv < 1)
        return np.where(dentro[..., None], amostra(txt, np.clip(uu, 0, 1), np.clip(vv, 0, 1)), cor)
    c.caixa(0.08, 0.2, 0.08, 0.92, 0.82, 0.86, None, frente, faces=("x0", "x1", "y1", "y0"), brilho=0.3)
    c.caixa(0.1, 0.22, 0.0, 0.9, 0.8, 0.08, np.array([60, 60, 62.0]))
    # grade do motor atrás (aparece no lado norte/oeste depois de girar)
    for k in range(8):
        c.caixa(0.2 + k * 0.08, 0.195, 0.12, 0.24 + k * 0.08, 0.2, 0.4, np.array([70, 70, 72.0]), faces=("y0",))
    # tampa de vidro em duas folhas com moldura
    vidro = np.array([150, 186, 206.0])
    c.caixa(0.08, 0.2, 0.86, 0.92, 0.82, 0.9, np.array([200, 202, 204.0]), brilho=0.5)
    c.caixa(0.11, 0.23, 0.9, 0.5, 0.79, 0.905, vidro, brilho=0.9)
    c.caixa(0.5, 0.23, 0.9, 0.89, 0.79, 0.905, vidro * 0.95, brilho=0.9)
    for k in range(5):  # picolés vistos pelo vidro
        x = 0.16 + k * 0.15
        c.caixa(x, 0.35, 0.905, x + 0.1, 0.62, 0.906, np.array([[220, 80, 90], [240, 200, 60], [120, 70, 40], [90, 170, 220], [240, 240, 240]][k], float))
    return girar(c, lado).render()


def cervejeira(lado, seed=85):
    """Geladeira vertical de porta de vidro, cheia de garrafas e latas, com o
    cabeçote vermelho escrito "GELADA"."""
    c = kl.Cena()
    verm = np.array([186, 36, 36.0])
    txt = texto_img([("GELADA", (255, 255, 255), 0.6, FONTE)], 500, 120, (186, 36, 36))

    def corpo(u, v, face):
        cor = np.broadcast_to(verm * 0.9, np.shape(u) + (3,)).copy()
        if face == "y1":
            vv = (v - 1.78) / 0.2
            uu = (u - 0.12) / 0.76
            dentro = (vv > 0) & (vv < 1) & (uu > 0) & (uu < 1)
            cor = np.where(dentro[..., None], amostra(txt, np.clip(uu, 0, 1), np.clip(vv, 0, 1)), cor)
        return cor
    c.caixa(0.1, 0.12, 0.0, 0.9, 0.86, 2.0, None, corpo, brilho=0.4, faces=("x0", "x1", "y0", "topo"))
    c.caixa(0.1, 0.84, 0.0, 0.9, 0.86, 0.12, np.array([40, 40, 42.0]))
    c.caixa(0.1, 0.84, 1.76, 0.9, 0.86, 2.0, None, corpo, faces=("y1",))
    # moldura da porta e interior
    c.caixa(0.1, 0.84, 0.12, 0.14, 0.87, 1.76, verm, brilho=0.5)
    c.caixa(0.86, 0.84, 0.12, 0.9, 0.87, 1.76, verm, brilho=0.5)
    c.caixa(0.14, 0.2, 0.12, 0.86, 0.22, 1.76, np.array([236, 240, 244.0]), faces=("y1",))
    rnd = np.random.default_rng(seed)
    for z in (0.14, 0.52, 0.9, 1.28):
        c.caixa(0.14, 0.22, z, 0.86, 0.8, z + 0.02, np.array([200, 204, 210.0]), faces=("topo",), brilho=0.4)
        lata = z > 1.2
        for k in range(8):
            x = 0.19 + k * 0.088
            for y in (0.45, 0.68):
                if lata:
                    cor = np.array([[200, 40, 40], [40, 80, 170], [220, 220, 220]][rnd.integers(3)], float)
                    c.haste((x, y, z + 0.02), (x, y, z + 0.16), 0.03, cor, 0.7)
                else:
                    cor = np.array([96, 52, 22.0]) * (0.9 + 0.2 * rnd.random())
                    c.haste((x, y, z + 0.02), (x, y, z + 0.22), 0.03, cor, 0.8)
                    c.haste((x, y, z + 0.22), (x, y, z + 0.32), 0.012, cor, 0.8)
                    c.haste((x, y, z + 0.32), (x, y, z + 0.335), 0.014, np.array([210, 180, 80.0]), 0.8)
    for k in range(4):  # reflexo do vidro
        x0 = 0.2 + k * 0.17
        c.haste((x0, 0.87, 0.3), (x0 + 0.12, 0.87, 1.5), 0.004, np.array([235, 242, 250.0]), 0.8)
    c.caixa(0.8, 0.875, 0.7, 0.83, 0.9, 1.2, np.array([200, 200, 204.0]), brilho=0.7)   # puxador
    return girar(c, lado).render()


AMARELO = np.array([236, 186, 30.0])
BRANCO_P = np.array([232, 232, 226.0])


def cadeira(lado, cor):
    """Cadeira de plástico de bar: assento, encosto vazado e braços. Desenhada
    virada para o sul (quem senta olha para o sul)."""
    c = kl.Cena()
    cor = np.array(cor, float)
    for x, y in ((0.3, 0.32), (0.7, 0.32), (0.3, 0.72), (0.7, 0.72)):
        c.haste((x + (x - 0.5) * 0.15, y + (y - 0.52) * 0.15, 0.0), (x, y, 0.42), 0.022, cor, 0.5)
    c.caixa(0.27, 0.3, 0.42, 0.73, 0.76, 0.46, cor, brilho=0.5)
    # encosto (lado norte) com ripas
    for k in range(5):
        x = 0.29 + k * 0.1
        c.caixa(x, 0.28, 0.46, x + 0.06, 0.32, 0.86, cor, brilho=0.5)
    c.caixa(0.27, 0.27, 0.84, 0.73, 0.33, 0.9, cor, brilho=0.5)
    for x in (0.25, 0.71):  # braços
        c.caixa(x, 0.3, 0.6, x + 0.04, 0.72, 0.64, cor, brilho=0.5)
        c.haste((x + 0.02, 0.7, 0.46), (x + 0.02, 0.7, 0.62), 0.016, cor, 0.5)
    return girar(c, lado).render()


def mesa(cor):
    c = kl.Cena()
    cor = np.array(cor, float)
    for x, y in ((0.2, 0.2), (0.8, 0.2), (0.2, 0.8), (0.8, 0.8)):
        c.haste((x + (x - 0.5) * 0.12, y + (y - 0.5) * 0.12, 0.0), (x, y, 0.7), 0.026, cor, 0.5)
    c.caixa(0.12, 0.12, 0.7, 0.88, 0.88, 0.74, cor, brilho=0.5)
    c.caixa(0.12, 0.12, 0.66, 0.88, 0.14, 0.7, cor * 0.92)
    c.caixa(0.12, 0.86, 0.66, 0.88, 0.88, 0.7, cor * 0.92)
    c.caixa(0.12, 0.12, 0.66, 0.14, 0.88, 0.7, cor * 0.92)
    c.caixa(0.86, 0.12, 0.66, 0.88, 0.88, 0.7, cor * 0.92)
    return c.render()


def engradados(seed=87):
    c = kl.Cena()
    rnd = np.random.default_rng(seed)
    cores = [np.array([196, 40, 36.0]), np.array([236, 180, 30.0])]
    z = 0.0
    for k in range(4):
        cor = cores[k % 2]
        x0 = 0.16 + 0.02 * rnd.random()
        y0 = 0.22 + 0.02 * rnd.random()
        c.caixa(x0, y0, z, x0 + 0.66, y0 + 0.46, z + 0.3, cor, brilho=0.3)
        for i in range(6):
            for j in range(4):
                x, y = x0 + 0.08 + i * 0.1, y0 + 0.08 + j * 0.1
                c.haste((x, y, z + 0.3), (x, y, z + 0.34), 0.012, np.array([96, 52, 22.0]), 0.7)
                c.haste((x, y, z + 0.34), (x, y, z + 0.35), 0.013, np.array([210, 180, 80.0]), 0.7)
        z += 0.3
    return c.render()


def pilha_cadeiras(cor):
    c = kl.Cena()
    cor = np.array(cor, float)
    for x, y in ((0.3, 0.32), (0.7, 0.32), (0.3, 0.72), (0.7, 0.72)):
        c.haste((x + (x - 0.5) * 0.15, y + (y - 0.52) * 0.15, 0.0), (x, y, 0.42), 0.022, cor, 0.5)
    for k in range(6):
        dz = k * 0.07
        c.caixa(0.27, 0.3, 0.42 + dz, 0.73, 0.76, 0.46 + dz, cor * (1 - 0.03 * (k % 2)), brilho=0.5)
        c.caixa(0.27, 0.27, 0.46 + dz, 0.73, 0.32, 0.9 + dz, cor * (0.97 - 0.03 * (k % 2)), brilho=0.5)
    return c.render()


# -- peças de parede (desenhadas na parede norte, saindo para o sul; `girar` "L" põe na parede oeste)
def letreiro(metade):
    """Letreiro do bar em 2 tiles (metade 0 = esquerda na tela)."""
    c = kl.Cena()
    img = texto_img([(NOME_BAR, (196, 30, 30), 0.5, FONTE),
                     ("BEBIDAS  •  PETISCOS  •  PF", (30, 110, 64), 0.22, FONTE)],
                    1600, 260, (246, 244, 236), ((30, 110, 64), 10))

    def frente(u, v, face):
        if face != "y1":
            return np.broadcast_to(np.array([200, 198, 190.0]), np.shape(u) + (3,))
        return amostra(img, (u + metade) / 2, (v - 2.15) / 0.62)
    c.caixa(0.0, 0.0, 2.15, 1.0, 0.07, 2.77, None, frente, brilho=0.25)
    for x in (0.2, 0.8):  # mão-francesa
        c.haste((x, 0.0, 2.1), (x, 0.06, 2.15), 0.01, np.array([90, 90, 92.0]))
    return c


def lousa():
    c = kl.Cena()
    img = texto_img([("CARDÁPIO", (250, 250, 240), 0.16, FONTE),
                     ("PF ............ 18,00", (250, 250, 240), 0.13, FONTE_GIZ),
                     ("PASTEL ......... 8,00", (250, 240, 140), 0.13, FONTE_GIZ),
                     ("CERVEJA 600 ... 12,00", (250, 250, 240), 0.13, FONTE_GIZ),
                     ("CAIPIRINHA .... 15,00", (170, 230, 170), 0.13, FONTE_GIZ),
                     ("TORRESMO ...... 10,00", (250, 250, 240), 0.13, FONTE_GIZ)],
                    500, 560, (34, 58, 44))
    madeira = np.array([120, 80, 46.0])

    def frente(u, v, face):
        if face != "y1":
            return np.broadcast_to(madeira, np.shape(u) + (3,))
        return amostra(img, (u - 0.24) / 0.52, (v - 1.25) / 0.66)
    c.caixa(0.22, 0.0, 1.23, 0.78, 0.03, 1.93, madeira, brilho=0.2)
    c.caixa(0.24, 0.0, 1.25, 0.76, 0.035, 1.91, None, frente)
    return c


def _ondulado(base):
    def f(u, v, face):
        onda = np.sin(v * 2 * math.pi / 0.06)
        cor = base * (0.9 + 0.1 * onda)[..., None]
        fer = tf.vn(u % 1, (v / 3) % 1, 20, 12, 3) > 0.9
        return np.where(fer[..., None], np.array([132, 100, 78.0]), cor)
    return f


def porta_enrolar(fechada):
    c = kl.Cena()
    aco = np.array([150, 154, 158.0])
    for x in (0.03, 0.93):  # trilhos
        c.caixa(x, -0.02, 0.0, x + 0.04, 0.06, 2.2, aco * 0.8, brilho=0.4)
    if fechada:
        c.caixa(0.06, 0.0, 0.0, 0.94, 0.05, 2.2, None, _ondulado(aco), brilho=0.4)
        c.caixa(0.44, 0.05, 0.05, 0.56, 0.07, 0.12, np.array([60, 60, 62.0]), brilho=0.6)    # fechadura
    else:
        c.caixa(0.06, 0.0, 2.02, 0.94, 0.05, 2.2, None, _ondulado(aco), brilho=0.4)          # ponta abaixo do rolo
    c.caixa(0.02, -0.04, 2.2, 0.98, 0.14, 2.48, aco * 0.85, brilho=0.4)                      # caixa do rolo
    return c


def _parede(c, lado):
    return girar(c, "S" if lado == "N" else "L").render(sombra=0)


SOLIDO = [["BlocksPlacement", ""], ["solid", ""]]
LADOS_JOGO = {"S": "S", "L": "E", "N": "N", "O": "W"}


def _props_de(defs, folha, i, trocas=None):
    props = [list(p) for p in (defs[folha]["pecas"][i] or [])]
    out = []
    for k, v in props:
        if trocas and k in trocas:
            v = trocas[k]
        if k in ("SpriteGridPos",):
            continue
        out.append([k, v])
    return out


def objetos(defs, saida: Path) -> dict:
    bar = "location_restaurant_bar_01"
    gel = "appliances_refrigeration_01"
    cad = "furniture_seating_outdoor_01"
    lista = []
    for lado, i in (("S", 5), ("L", 7), ("N", 1), ("O", 3)):
        lista.append((f"balcao_azulejo_{lado.lower()}", f"balcão de azulejo, frente para {lado}",
                      lambda lado=lado: balcao(lado), _props_de(defs, bar, i, {"GroupName": "Botequim"})))
    for lado, i in (("S", 5), ("L", 7), ("N", 1), ("O", 3)):
        lista.append((f"balcao_estufa_{lado.lower()}", f"balcão com estufa de salgados, frente para {lado}",
                      lambda lado=lado: balcao(lado, True), _props_de(defs, bar, i, {"GroupName": "Botequim Estufa"})))
    for lado, i in (("S", 48), ("L", 49), ("N", 50), ("O", 51)):
        lista.append((f"freezer_sorvete_{lado.lower()}", f"freezer de sorvete, frente para {lado}",
                      lambda lado=lado: freezer(lado), _props_de(defs, gel, i, {"GroupName": "Sorvete"})))
    for lado, i in (("S", 22), ("L", 23)):
        lista.append((f"cervejeira_{lado.lower()}", f"cervejeira de porta de vidro, frente para {lado}",
                      lambda lado=lado: cervejeira(lado), _props_de(defs, gel, i, {"GroupName": "Cervejeira"})))
    for nome_cor, cor in (("amarela", AMARELO), ("branca", BRANCO_P)):
        for lado, i in (("S", 17), ("L", 16), ("N", 18), ("O", 19)):
            lista.append((f"cadeira_plastico_{nome_cor}_{lado.lower()}", f"cadeira de plástico {nome_cor}, virada para {lado}",
                          lambda lado=lado, cor=cor: cadeira(lado, cor), _props_de(defs, cad, i)))
    for nome_cor, cor in (("amarela", AMARELO), ("branca", BRANCO_P)):
        lista.append((f"mesa_plastico_{nome_cor}", f"mesa de plástico {nome_cor}", lambda cor=cor: mesa(cor),
                      [["BlocksPlacement", ""], ["CustomName", "Table"], ["GroupName", "Plastic"], ["IsTable", ""],
                       ["IsMoveAble", ""], ["PickUpWeight", "60"], ["Surface", str(round(0.74 * PX_M / 2))],
                       ["solidtrans", ""]]))
    lista.append(("engradados_cerveja", "engradados de cerveja empilhados", engradados, SOLIDO))
    lista.append(("pilha_cadeiras_amarela", "pilha de cadeiras de plástico", lambda: pilha_cadeiras(AMARELO),
                  [["BlocksPlacement", ""], ["solidtrans", ""]]))
    for parede in ("N", "O"):
        f = "sul" if parede == "N" else "leste"
        for m in (0, 1):
            lista.append((f"letreiro_{parede.lower()}_{m + 1}", f"letreiro '{NOME_BAR}' (parte {m + 1} de 2), na parede {parede}, fachada para o {f}",
                          lambda m=m, parede=parede: _parede(letreiro(m), parede), []))
        lista.append((f"lousa_cardapio_{parede.lower()}", f"lousa de cardápio, na parede {parede}",
                      lambda parede=parede: _parede(lousa(), parede), []))
        lista.append((f"porta_enrolar_aberta_{parede.lower()}", f"porta de enrolar aberta (rolo), na porta da parede {parede}",
                      lambda parede=parede: _parede(porta_enrolar(False), parede), []))
        lista.append((f"porta_enrolar_fechada_{parede.lower()}", f"porta de enrolar fechada, sobre a parede {parede}",
                      lambda parede=parede: _parede(porta_enrolar(True), parede), []))
    nome = "rsb_botequim_01"
    linhas = (len(lista) + 7) // 8
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = []
    for n, (chave, desc, f, props) in enumerate(lista):
        folha.alpha_composite(f(), ((n % 8) * 128, (n // 8) * 256))
        pecas.append({"peca": f"{nome}_{n}", "nome": chave, "descricao": desc, "props": props})
        print(n, chave, flush=True)
    pecas += [{"peca": f"{nome}_{n}", "props": []} for n in range(len(lista), linhas * 8)]
    return kf._gravar(folha, nome, "objeto", pecas, saida, {})


if __name__ == "__main__":
    tiles2x, tdefs, saida = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    defs = {d["nome"]: d for d in kit_tiles.ler_definicoes(tdefs)}
    so = sys.argv[4] if len(sys.argv) > 4 else "tudo"
    res = []
    if so in ("tudo", "paredes"):
        res.append(paredes(tiles2x, saida))
    if so in ("tudo", "pisos"):
        res.append(pisos(tiles2x, saida))
    if so in ("tudo", "objetos"):
        res.append(objetos(defs, saida))
    print(json.dumps(res, ensure_ascii=False))
