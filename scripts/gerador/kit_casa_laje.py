"""Kit Brasil, casa de laje do subúrbio e da Baixada (item 3 da ordem do guia, 09/11/2026).

Referências: fotos de ruas de Belford Roxo e Nova Iguaçu (Wikimedia Commons, guia
seção 4): reboco pintado em cores claras, muro de tijolo aparente ou rebocado,
portão de chapa de aço, laje com caixa d'água. Aproveita do que já existe:
lajes, muretas, caixa d'água, varal, churrasqueira (kit_laje), paredes de reboco
e tijolo e pisos de cerâmica (kit_favela), lajota (kit_botequim).

Folhas novas em `kits/tiles/`:
- `rsb_paredes_casa_01` (parede, 8 peças por estilo, molde do jogo): grafiato
  amarelo, verde-claro e pêssego, branco novo, fachada com barra de pedra
  miracema, cerâmica de filete.
- `rsb_muros_casa_01` (cerca alta): muro de 2 m de tijolo baiano, chapiscado,
  rebocado amarelo, rebocado branco e muro baixo com grade em cima; 4 peças por
  estilo (norte, oeste, quina, pilar), propriedades do muro alto de madeira do
  jogo (`fencing_01` 8, 10, 12, 13: bloqueia, dá para pular com esforço).
- `rsb_portoes_casa_01` (porta): portão social de grade preta, de chapa branca e
  de grade verde (4 peças cada: fechado O/N, aberto O/N, como o portão de cerca
  `fixtures_doors_fences_01` 16-19) e portão de garagem de chapa branca e marrom
  em 3 tiles (fechado 0-5, aberto 8-13, como `walls_garage_02`).
- `rsb_pisos_casa_01` (piso): pedra miracema, ardósia, cerâmica rústica de
  garagem, cerâmica branca 45, cimentado de garagem, bloquete.
- `rsb_objetos_casa_01` (objeto): tanque de lavar (é pia, tem água; do tanque
  industrial `fixtures_sinks_01` 32-35), botijão de gás, relógio de luz,
  grade de janela (2 desenhos), interfone com número e caixa de correio (peças de
  parede, norte e oeste), vaso de espada-de-são-jorge, cadeira de fio (4 lados).

Uso: python -I -X utf8 kit_casa_laje.py <pasta Tiles/2x> <newtiledefinitions.tiles> <kits/tiles>
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit_botequim as kb  # noqa: E402
import kit_favela as kf  # noqa: E402
import kit_laje as kl  # noqa: E402
import kit_tiles  # noqa: E402
import texturas_favela as tf  # noqa: E402

PX_M = tf.PX_M


# ================================================================ texturas de parede
def grafiato(tinta, seed):
    """Reboco com grafiato: riscos verticais finos e irregulares, tinta nova."""
    U, Z = tf.grade_parede()
    v = Z / 192
    risco = tf.vn(U, v * 0.3, 150, 3, seed)           # riscos finos e curtos
    h = (risco - 0.5) * 0.45 + 0.5 * (tf.vn(U, v, 180, 60, seed + 1) - 0.5)
    tinta = np.array(tinta, float)
    cor = tinta * (0.93 + 0.1 * tf.fbm(U, v, 4, 6, 4, seed + 2))[..., None]
    cor = cor * (1 + 0.015 * (risco - 0.5))[..., None]
    return tf._sujeira_base(U, Z, cor, h, seed + 3, 0.45)


def branco_novo(seed=91):
    cor, h = tf.reboco_pintado((236, 234, 226), seed, 0.0, None)
    return cor, h * 0.5


def pedras(U, Z, seed, cores, larg_u, alt_px, junta=(70, 66, 60)):
    """Pedra miracema / São Tomé: placas retangulares irregulares em fiadas."""
    gz = Z / alt_px
    j = np.floor(gz)
    desl = tf._h(j.astype(np.int64), j.astype(np.int64) * 0 + 7, seed)
    gu = U / larg_u + desl
    i = np.floor(gu)
    fu, fz = gu - i, gz - j
    borda = np.minimum(np.minimum(fu, 1 - fu) * larg_u * 63, np.minimum(fz, 1 - fz) * alt_px)
    k = tf._h((i.astype(np.int64)) % 997, j.astype(np.int64), seed + 1)
    cores = np.array(cores, float)
    cor = cores[(k * len(cores)).astype(int) % len(cores)]
    cor = cor * (0.85 + 0.25 * tf.fbm(U * 3 % 1, gz % 1, 6, 3, 3, seed + 2))[..., None]
    peca = borda > 0.9
    h = np.where(peca, 0.6 * tf.vn(U * 4 % 1, gz % 1, 12, 4, seed + 3), -1.4)
    cor = np.where(peca[..., None], cor, np.array(junta, float))
    return cor, h


MIRACEMA = [(150, 150, 132), (128, 130, 118), (164, 156, 132), (118, 122, 112), (172, 160, 140)]


def barra_miracema(tinta, seed):
    U, Z = tf.grade_parede()
    barra = 1.0 * PX_M
    ct, ht = grafiato(tinta, seed)
    cp, hp = pedras(U, Z, seed + 5, MIRACEMA, 0.36, 192 / 26)
    em = Z < barra
    cor = np.where(em[..., None], cp, ct)
    h = np.where(em, hp, ht)
    h = np.where(np.abs(Z - barra) < 1.5, h + 1.2, h)        # pingadeira
    return cor, h


def ceramica_filete(seed=95):
    """Cerâmica de fachada 5 x 20 deitada, tons de bege e marrom."""
    U, Z = tf.grade_parede()
    cores = [(176, 132, 96), (160, 116, 84), (190, 150, 110), (146, 104, 76)]
    cor, h = pedras(U, Z, seed, cores, 0.25, 192 / 48, junta=(196, 190, 176))
    brilho = tf.sstep(0.6, 1.0, tf.vn(U, Z / 192, 6, 20, seed + 4))
    return cor * (1 + 0.06 * brilho)[..., None], h * 0.6


ESTILOS_PAREDE = [
    ("grafiato_amarelo", "fachada de grafiato amarelo", "Plaster", lambda: grafiato((224, 196, 104), 81)),
    ("grafiato_verde_claro", "fachada de grafiato verde-claro", "Plaster", lambda: grafiato((172, 204, 160), 82)),
    ("grafiato_pessego", "fachada de grafiato pêssego", "Plaster", lambda: grafiato((230, 178, 144), 83)),
    ("branco_novo", "reboco pintado de branco, pintura nova", "Plaster", branco_novo),
    ("barra_miracema_azul", "barra de pedra miracema e grafiato azul-claro", "Stone",
     lambda: barra_miracema((168, 196, 218), 84)),
    ("ceramica_filete", "cerâmica de fachada em filetes (bege e marrom)", "Ceramic", ceramica_filete),
]


def _paredes_folha(nome, estilos, tiles2x, saida):
    molde_im = Image.open(tiles2x / f"{kf.MOLDE_PAREDE[0]}.png").convert("RGBA")
    base = kf.MOLDE_PAREDE[1]
    w = kf._celula(molde_im, base)
    Lref = np.median(kf._lum(w)[w[..., 3] > 200])
    linhas = ((len(estilos) + 1) // 2) * 2
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{nome}_{i}", "props": []} for i in range(linhas * 8)]
    entradas = []
    for k, (chave, desc, material, f) in enumerate(estilos):
        texs = kb._iluminar(*f())
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
    return kf._gravar(folha, nome, "parede", pecas, saida, {"exterior_walls": entradas, "interior_walls": entradas})


def paredes(tiles2x: Path, saida: Path) -> dict:
    return _paredes_folha("rsb_paredes_casa_01", ESTILOS_PAREDE, tiles2x, saida)


# ================================================================ muros
MURO_M = 2.0
GRADE_DE_M = 1.1          # muro com grade: alvenaria até aqui, grade até MURO_M + 0.2


def _uz(face):
    """u (0..1 ao longo) e z (px) de cada pixel da peça, como em kit_favela."""
    Y, X = np.mgrid[0:256, 0:128].astype(float)
    X, Y = X + 0.5, Y + 0.5
    uw = np.clip((63 - X) / 63, 0, 0.9999)
    un = np.clip((X - 63) / 63, 0, 0.9999)
    zw, zn = 192 + 32 * uw - Y, 192 + 32 * un - Y
    if face == "W":
        oeste = np.ones_like(X, dtype=bool)
    elif face == "N":
        oeste = np.zeros_like(X, dtype=bool)
    else:
        oeste = X < 63
    return np.where(oeste, uw, un), np.where(oeste, zw, zn)


def _muro_tex(base, capa=(196, 192, 182)):
    """Textura do muro com a capa (pingadeira de cimento) no alto."""
    cor, h = base
    U, Z = tf.grade_parede()
    topo = MURO_M * PX_M
    capa_m = (Z > topo - 7) & (Z <= topo)
    cor = np.where(capa_m[..., None], np.array(capa, float) * (0.9 + 0.15 * tf.vn(U, Z / 192, 30, 30, 5))[..., None], cor)
    h = np.where(capa_m, 1.5, h)
    return cor, h


def _muro_grade_tex():
    cor, h = tf.reboco_pintado((232, 230, 222), 97, 0.05, None)
    U, Z = tf.grade_parede()
    topo = GRADE_DE_M * PX_M
    capa_m = (Z > topo - 6) & (Z <= topo)
    cor = np.where(capa_m[..., None], np.array([200, 196, 186.0]), cor)
    return cor, np.where(capa_m, 1.5, h)


ESTILOS_MURO = [
    ("muro_tijolo", "muro de tijolo baiano aparente", "Brick", lambda: _muro_tex(tf.tijolo_baiano(101, True)), False),
    ("muro_chapiscado", "muro chapiscado cinza", "Plaster", lambda: _muro_tex(tf.reboco_cru(102)), False),
    ("muro_amarelo", "muro rebocado e pintado de amarelo", "Plaster",
     lambda: _muro_tex(tf.reboco_pintado((222, 194, 112), 103, 0.08, tf.tijolo_baiano(1))), False),
    ("muro_branco", "muro rebocado branco encardido", "Plaster",
     lambda: _muro_tex(tf.reboco_pintado((222, 220, 210), 104, 0.06, tf.tijolo_baiano(1))), False),
    ("muro_grade", "muro baixo branco com grade preta em cima", "Plaster", _muro_grade_tex, True),
]
MOLDE_MURO = "fencing_01"
PAPEIS_MURO = [(8, "N", 1), (10, "W", 0), (12, "NW", 2), (13, "SE", 3)]   # (peça no molde, face, peça no molde de parede)


def peca_muro(molde_parede, face, texs, Lref, grade):
    im = np.array(kf.peca_parede_tex(molde_parede, face, texs, Lref))
    U, Z = _uz(face)
    a = im[..., 3].astype(float)
    if not grade:
        a = np.where(Z > MURO_M * PX_M, 0, a)
    else:
        alv = Z <= GRADE_DE_M * PX_M
        zona = (Z > GRADE_DE_M * PX_M) & (Z <= (MURO_M + 0.2) * PX_M)
        barra = (np.abs(((U * 9) % 1) - 0.5) > 0.42)
        trilho = (np.abs(Z - (MURO_M + 0.18) * PX_M) < 2.0) | (np.abs(Z - (GRADE_DE_M + 0.12) * PX_M) < 1.5)
        lanca = (np.abs(((U * 9) % 1) - 0.5) > 0.36) & (Z > (MURO_M + 0.12) * PX_M) & (Z <= (MURO_M + 0.26) * PX_M)
        ferro = zona & (barra | trilho) | lanca
        im[..., :3] = np.where(ferro[..., None], np.array([34, 34, 36], np.uint8), im[..., :3])
        a = np.where(alv | ferro, a, 0)
        # grade mais fina: só a frente (não a espessura) na zona de ferro
        a = np.where(ferro & (a > 0), 255, a)
    im[..., 3] = a.astype(np.uint8)
    return Image.fromarray(im, "RGBA")


def muros(tiles2x: Path, defs: dict, saida: Path) -> dict:
    nome = "rsb_muros_casa_01"
    molde_im = Image.open(tiles2x / f"{kf.MOLDE_PAREDE[0]}.png").convert("RGBA")
    base = kf.MOLDE_PAREDE[1]
    w = kf._celula(molde_im, base)
    Lref = np.median(kf._lum(w)[w[..., 3] > 200])
    sd = defs[MOLDE_MURO]
    linhas = ((len(ESTILOS_MURO) + 1) // 2)
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{nome}_{i}", "props": []} for i in range(linhas * 8)]
    for k, (chave, desc, material, f, grade) in enumerate(ESTILOS_MURO):
        texs = kb._iluminar(*f())
        b = (k // 2) * 8 + (k % 2) * 4
        novo = {velho: b + j for j, (velho, _f, _o) in enumerate(PAPEIS_MURO)}
        novo[9], novo[11] = novo[8], novo[10]          # variantes do molde apontam para a mesma peça
        for j, (velho, face, off) in enumerate(PAPEIS_MURO):
            i = b + j
            folha.alpha_composite(peca_muro(kf._celula(molde_im, base + off), face, texs, Lref, grade),
                                  ((i % 8) * 128, (i // 8) * 256))
            props = []
            for p, v in sd["pecas"][velho] or []:
                if p in ("SnowTile", "BurntTile"):
                    continue
                if v.startswith(MOLDE_MURO + "_"):
                    v = f"{nome}_{novo[int(v.rsplit('_', 1)[1])]}"
                if p == "Material":
                    v = "MetalBars" if grade else "Stone"
                if p in ("Material2", "MaterialType"):
                    continue
                props.append([p, v])
            props.append(["MaterialType", "Concrete" if material != "Brick" else "Brick"])
            pecas[i] = {"peca": f"{nome}_{i}", "nome": f"{chave} {face}", "descricao": desc, "props": props}
    return kf._gravar(folha, nome, "cerca", pecas, saida, {})


# ================================================================ portões
def _chapa(cor, nerv=24):
    # a face voltada para a rua (sul/leste) recebe pouca luz no renderizador: compensa
    cor = np.array(cor, float) * 1.8

    def f(u, v, face):
        onda = np.abs(((u * nerv) % 1) - 0.5) < 0.12
        c = cor * np.where(onda, 0.86, 1.0)[..., None]
        sujo = tf.sstep(0.5, 0.0, v) * 0.25
        return c * (1 - sujo)[..., None]
    return f


def portao_social(estilo, aberto):
    """Desenhado na parede norte (painel em y = 0). Aberto: painel girado 90°."""
    c = kl.Cena()
    alt = 2.1
    preto = np.array([36, 36, 38.0])
    verde = np.array([40, 92, 60.0])
    ferro = verde if estilo == "grade_verde" else preto

    def painel(x0, y0, x1, y1):
        dx, dy = x1 - x0, y1 - y0
        if estilo == "chapa_branca":
            if abs(dx) > abs(dy):
                c.caixa(min(x0, x1), y0, 0.05, max(x0, x1), y0 + 0.025, alt * 0.7, None, _chapa((250, 250, 246)), brilho=0.4)
            else:
                c.caixa(x0, min(y0, y1), 0.05, x0 + 0.025, max(y0, y1), alt * 0.7, None, _chapa((250, 250, 246)), brilho=0.4)
            zb = alt * 0.7
        else:
            zb = 0.05
        for k in range(10):          # barras verticais
            t = 0.05 + k * 0.1
            x, y = x0 + dx * t, y0 + dy * t
            c.haste((x, y, zb), (x, y, alt), 0.009, ferro, 0.5)
        for z in (0.05, zb, alt * 0.5 if estilo != "chapa_branca" else zb, alt):
            c.haste((x0, y0, z), (x1, y1, z), 0.011, ferro, 0.5)
        c.haste((x0, y0, 0.0), (x0, y0, alt + 0.05), 0.02, ferro, 0.5)
        c.haste((x1, y1, 0.0), (x1, y1, alt + 0.05), 0.02, ferro, 0.5)
    if aberto:
        painel(0.04, 0.02, 0.04, 0.98)
    else:
        painel(0.02, 0.02, 0.98, 0.02)
    return c


def portao_garagem(cor, pos, aberto):
    """Portão de correr de chapa, 3 tiles; `pos` 0, 1, 2 (esquerda, meio, direita)."""
    c = kl.Cena()
    alt = 2.2
    perfil = np.array([70, 70, 74.0])
    if not aberto:
        c.caixa(0.0, 0.0, 0.03, 1.0, 0.035, alt, None, _chapa(cor, 18), brilho=0.4)
        c.haste((0.0, 0.04, 1.1), (1.0, 0.04, 1.1), 0.008, np.array(cor, float) * 0.8, 0.4)
        if pos == 1:
            c.caixa(0.46, 0.035, 1.0, 0.54, 0.055, 1.08, perfil, brilho=0.6)          # fechadura
    # trilho no chão e guia em cima (aparecem aberto ou fechado)
    c.caixa(0.0, -0.01, 0.0, 1.0, 0.05, 0.03, perfil, brilho=0.5)
    c.caixa(0.0, -0.01, alt, 1.0, 0.06, alt + 0.05, perfil, brilho=0.5)
    if pos in (0, 2):
        x = 0.0 if pos == 0 else 0.96
        c.caixa(x, -0.02, 0.0, x + 0.04, 0.07, alt + 0.05, perfil * 1.1, brilho=0.5)
    return c


def _parede(c, lado):
    return kb.girar(c, "S" if lado == "N" else "L").render(sombra=0)


def portoes(defs: dict, saida: Path) -> dict:
    nome = "rsb_portoes_casa_01"
    gate, gar = "fixtures_doors_fences_01", "walls_garage_02"
    linhas = 6
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{nome}_{i}", "props": []} for i in range(linhas * 8)]

    def por(i, img, chave, desc, molde, j):
        folha.alpha_composite(img, ((i % 8) * 128, (i // 8) * 256))
        props = [list(p) for p in (defs[molde]["pecas"][j] or [])]
        pecas[i] = {"peca": f"{nome}_{i}", "nome": chave, "descricao": desc, "props": props}
    # portões sociais: blocos de 4 (fechado O, fechado N, aberto O, aberto N), como o molde 16-19
    for b, estilo in ((0, "grade_preta"), (4, "chapa_branca"), (8, "grade_verde")):
        for k, (aberto, lado) in enumerate(((False, "O"), (False, "N"), (True, "O"), (True, "N"))):
            por(b + k, _parede(portao_social(estilo, aberto), lado),
                f"portao_social_{estilo}_{'aberto' if aberto else 'fechado'}_{lado.lower()}",
                f"portão social ({estilo.replace('_', ' ')}), {'aberto' if aberto else 'fechado'}, parede {lado}",
                gate, 16 + k)
    # portões de garagem: fechado 0-5, aberto 8-13 a partir de 16 e 32, como walls_garage_02
    for b, (nc, cor) in ((16, ("branco", (250, 250, 246))), (32, ("marrom", (120, 76, 52)))):
        for aberto, off in ((False, 0), (True, 8)):
            for lado, l0 in (("O", 0), ("N", 3)):
                for pos in range(3):
                    j = off + l0 + pos
                    por(b + j, _parede(portao_garagem(cor, pos, aberto), lado),
                        f"portao_garagem_{nc}_{'aberto' if aberto else 'fechado'}_{lado.lower()}_{pos + 1}",
                        f"portão de garagem de chapa {nc}, {'aberto' if aberto else 'fechado'}, parede {lado}, parte {pos + 1} de 3",
                        gar, j)
    return kf._gravar(folha, nome, "porta", pecas, saida, {})


# ================================================================ pisos
def piso_pedras(cores, larg, alt, seed, junta=(96, 92, 84), exterior=True):
    S, T = tf.grade_piso()
    j = np.floor(T * alt)
    desl = tf._h(j.astype(np.int64) % alt, j.astype(np.int64) * 0 + 3, seed)
    gs = S * larg + desl
    i = np.floor(gs)
    fs, ft = gs - i, T * alt - j
    borda = np.minimum(np.minimum(fs, 1 - fs) * tf.PX_PISO / larg, np.minimum(ft, 1 - ft) * tf.PX_PISO / alt)
    k = tf._h(i.astype(np.int64) % larg, j.astype(np.int64) % alt, seed + 1)
    cores = np.array(cores, float)
    cor = cores[(k * len(cores)).astype(int) % len(cores)]
    cor = cor * (0.86 + 0.24 * tf.fbm(S, T, 8, 8, 4, seed + 2))[..., None]
    peca = borda > 0.7
    cor = np.where(peca[..., None], cor, np.array(junta, float))
    h = np.where(peca, 0.5 * tf.vn(S, T, 30, 30, seed + 3), -1.0)
    return cor, h


def ardosia(seed=111):
    S, T = tf.grade_piso()
    n = 2
    fs, ft = S * n % 1, T * n % 1
    k = tf._h(np.floor(S * n).astype(np.int64), np.floor(T * n).astype(np.int64), seed)
    base = np.array([70, 74, 76.0]) * (0.85 + 0.25 * k)[..., None]
    camadas = tf.fbm((S * n) % 1, (T * n) % 1, 3, 9, 4, seed + 1)
    cor = base * (0.85 + 0.3 * camadas)[..., None]
    borda = np.minimum(np.minimum(fs, 1 - fs), np.minimum(ft, 1 - ft)) * tf.PX_PISO / n
    junta = borda < 0.6
    cor = np.where(junta[..., None], np.array([150, 146, 138.0]), cor)
    return cor, np.where(junta, -0.8, 0.8 * (camadas - 0.5))


def cimentado_garagem(seed=112):
    cor, h = tf.contrapiso(seed)
    S, T = tf.grade_piso()
    oleo = tf.sstep(0.62, 0.8, tf.fbm(S, T, 2, 2, 4, seed + 1))
    cor = tf.mistura(cor, np.array([58, 56, 54.0]), oleo * 0.5)
    corte = (np.minimum(S, 1 - S) * tf.PX_PISO < 0.8)        # junta de dilatação a cada tile
    return np.where(corte[..., None], cor * 0.6, cor), np.where(corte, -1.0, h)


def bloquete(seed=113):
    """Piso intertravado de concreto (bloquete), cinza, em espinha simples."""
    S, T = tf.grade_piso()
    return piso_pedras([(150, 148, 142), (138, 136, 132), (160, 156, 148)], 4, 8, seed, junta=(96, 92, 84))


PISOS = [
    ("pedra_miracema", "pedra miracema (quintal e garagem)",
     lambda: piso_pedras(MIRACEMA, 4, 8, 114), True),
    ("ardosia", "ardósia cinza-escura (varanda e sala)", ardosia, False),
    ("ceramica_rustica_garagem", "cerâmica rústica antiderrapante (garagem)",
     lambda: tf.ceramica([(150, 96, 70), (140, 88, 64), (158, 104, 76)], 115, (110, 100, 90), por_tile=3, quebrada=0.04), True),
    ("ceramica_branca_45", "cerâmica branca 45 x 45 (sala e quartos)",
     lambda: tf.ceramica([(226, 222, 212), (220, 216, 206)], 116, (190, 184, 170), por_tile=2, quebrada=0.02), False),
    ("cimentado_garagem", "cimentado de garagem com mancha de óleo", cimentado_garagem, True),
    ("bloquete", "bloquete (piso intertravado de concreto)", bloquete, True),
]


def pisos(tiles2x: Path, saida: Path) -> dict:
    nome = "rsb_pisos_casa_01"
    folha = Image.new("RGBA", (1024, 256), (0, 0, 0, 0))
    pecas = []
    for n, (chave, desc, f, ext) in enumerate(PISOS):
        folha.alpha_composite(kf.peca_piso(f(), tiles2x), ((n % 8) * 128, 0))
        pecas.append({"peca": f"{nome}_{n}", "nome": chave, "descricao": desc,
                      "props": [["diamondFloor", ""], ["solidfloor", ""]] + ([["exterior", ""]] if ext else [])})
    pecas += [{"peca": f"{nome}_{n}", "props": []} for n in range(len(PISOS), 8)]
    return kf._gravar(folha, nome, "piso", pecas, saida, {"floors": [{"Floor": i} for i in range(len(PISOS))]})


# ================================================================ objetos
def tanque(lado, seed=121):
    """Tanque de lavar roupa de concreto/granilite com esfregador, torneira e pé."""
    c = kl.Cena()
    gran = kb.granito(seed)
    cinza = lambda u, v, face: np.broadcast_to(np.array([176, 172, 164.0]), np.shape(u) + (3,)) * (
        0.9 + 0.15 * tf.vn(u % 1, v % 1, 40, 40, seed))[..., None]
    for x in (0.2, 0.74):                                    # pés
        c.caixa(x, 0.5, 0.0, x + 0.08, 0.6, 0.7, None, cinza)
    c.caixa(0.14, 0.42, 0.7, 0.88, 0.92, 0.9, None, cinza)   # cuba
    c.caixa(0.18, 0.46, 0.86, 0.54, 0.88, 0.901, np.array([110, 108, 104.0]), faces=("topo",))
    for k in range(9):                                       # esfregador (estrias)
        y = 0.47 + k * 0.045
        c.caixa(0.56, y, 0.88, 0.84, y + 0.02, 0.905, np.array([196, 192, 184.0]), faces=("topo", "y1"))
    c.haste((0.36, 0.42, 1.2), (0.36, 0.42, 0.98), 0.012, np.array([180, 180, 184.0]), 0.8)      # cano
    c.haste((0.36, 0.42, 0.98), (0.36, 0.52, 0.98), 0.012, np.array([180, 180, 184.0]), 0.8)     # torneira
    c.caixa(0.33, 0.39, 0.99, 0.39, 0.45, 1.03, np.array([200, 40, 40.0]), brilho=0.5)
    c.caixa(0.6, 0.62, 0.905, 0.72, 0.7, 0.95, np.array([60, 140, 210.0]), brilho=0.4)         # sabão em barra azul
    return kb.girar(c, lado).render()


def botijao(seed=122):
    c = kl.Cena()
    lar = np.array([200, 96, 40.0])
    c.revolucao(0.5, 0.5, lambda z: 0.17 * np.sqrt(np.clip(1 - ((z - 0.3) / 0.32) ** 8, 0, 1)), 0.04, 0.62, lar, brilho=0.5)
    c.revolucao(0.5, 0.5, lambda z: np.full_like(z, 0.15), 0.0, 0.05, lar * 0.8)
    c.revolucao(0.5, 0.5, lambda z: np.full_like(z, 0.035), 0.6, 0.7, np.array([150, 150, 152.0]), brilho=0.7)
    c.haste((0.5, 0.5, 0.7), (0.62, 0.42, 0.5), 0.01, np.array([40, 40, 40.0]), 0.3)          # mangueira
    for ang in (0, math.pi):                                                                   # alça
        c.haste((0.5 + 0.12 * math.cos(ang), 0.5 + 0.12 * math.sin(ang), 0.6), (0.5 + 0.12 * math.cos(ang), 0.5 + 0.12 * math.sin(ang), 0.72), 0.01, lar * 0.9)
    return c.render()


def relogio_luz():
    """Padrão de energia no muro: caixa cinza com visor do medidor e disjuntor."""
    c = kl.Cena()
    c.caixa(0.3, 0.0, 1.1, 0.7, 0.16, 1.62, np.array([168, 170, 172.0]), brilho=0.4)
    c.caixa(0.38, 0.16, 1.3, 0.62, 0.165, 1.5, np.array([190, 210, 220.0]), brilho=0.9)       # visor
    c.caixa(0.44, 0.165, 1.36, 0.56, 0.17, 1.42, np.array([30, 30, 30.0]))
    c.haste((0.5, 0.08, 1.62), (0.5, 0.08, 2.6), 0.022, np.array([60, 62, 64.0]), 0.4)         # eletroduto
    return c


def grade_janela(desenho):
    """Grade de ferro na frente da janela (vão da janela do molde do jogo)."""
    c = kl.Cena()
    preto = np.array([36, 36, 38.0])
    x0, x1, z0, z1 = 0.2, 0.8, 0.95, 2.05
    y = 0.03
    for x in (x0, x1):
        c.haste((x, y, z0), (x, y, z1), 0.012, preto, 0.4)
    for z in (z0, z1):
        c.haste((x0, y, z), (x1, y, z), 0.012, preto, 0.4)
    if desenho == "reta":
        for k in range(1, 6):
            x = x0 + (x1 - x0) * k / 6
            c.haste((x, y, z0), (x, y, z1), 0.008, preto, 0.4)
        c.haste((x0, y, (z0 + z1) / 2), (x1, y, (z0 + z1) / 2), 0.008, preto, 0.4)
    else:  # losangos
        n = 4
        for k in range(-n, n + 1):
            a = (x0 + (x1 - x0) * (k / n), z0)
            pts1 = [(a[0] + t * (x1 - x0) / 2, y, z0 + t * (z1 - z0)) for t in np.linspace(0, 1, 30)]
            pts2 = [(a[0] - t * (x1 - x0) / 2 + (x1 - x0) / 2 * 0, y, z0 + t * (z1 - z0)) for t in np.linspace(0, 1, 30)]
            for pts in (pts1, pts2):
                dentro = [p for p in pts if x0 <= p[0] <= x1]
                if len(dentro) > 1:
                    c.curva(dentro, 0.007, preto, 0.4)
    return c


def interfone():
    """Número da casa, interfone e caixa de correio no muro."""
    c = kl.Cena()
    img = kb.texto_img([("157", (30, 30, 30), 0.7, kb.FONTE)], 200, 120, (236, 232, 220))
    c.caixa(0.2, 0.0, 1.55, 0.42, 0.02, 1.68, None,
            lambda u, v, face: kb.amostra(img, (u - 0.2) / 0.22, (v - 1.55) / 0.13) if face == "y1"
            else np.broadcast_to(np.array([200, 196, 186.0]), np.shape(u) + (3,)), brilho=0.4)
    c.caixa(0.5, 0.0, 1.25, 0.6, 0.05, 1.45, np.array([220, 220, 216.0]), brilho=0.5)            # interfone
    c.caixa(0.53, 0.05, 1.37, 0.57, 0.055, 1.42, np.array([60, 60, 64.0]))
    c.caixa(0.64, 0.0, 1.0, 0.86, 0.1, 1.28, np.array([40, 92, 60.0]), brilho=0.5)               # caixa de correio
    c.caixa(0.67, 0.1, 1.2, 0.83, 0.105, 1.23, np.array([20, 20, 20.0]))
    return c


def espada_sao_jorge(seed=124):
    c = kl.Cena()
    terracota = np.array([170, 90, 58.0])
    c.revolucao(0.5, 0.5, lambda z: 0.13 + 0.06 * (z / 0.32), 0.0, 0.32, terracota, brilho=0.2)
    c.disco(0.5, 0.5, 0.17, lambda R, T: np.full_like(R, 0.3), np.array([70, 50, 36.0]))
    rnd = np.random.default_rng(seed)
    for k in range(13):
        ang = rnd.random() * 2 * math.pi
        r = 0.09 * rnd.random()
        bx, by = 0.5 + r * math.cos(ang), 0.5 + r * math.sin(ang)
        alt = 0.55 + 0.45 * rnd.random()
        inc = 0.08 * rnd.random()
        topo = (bx + inc * math.cos(ang), by + inc * math.sin(ang), 0.3 + alt)
        verde = np.array([52, 104, 48.0]) * (0.8 + 0.4 * rnd.random())
        c.haste((bx, by, 0.3), topo, 0.022, verde, 0.3,
                cor_f=lambda T, A, verde=verde: verde * (1 + 0.25 * (np.sin(T * 40) > 0.6))[..., None]
                + np.where((A < 0.4)[..., None], np.array([60, 60, 0.0]), 0))
    return c.render()


def cadeira_fio(lado, cor):
    """Cadeira de fio (varanda): armação de ferro e fios coloridos trançados."""
    c = kl.Cena()
    cor = np.array(cor, float)
    ferro = np.array([50, 50, 52.0])
    for x, y in ((0.25, 0.25), (0.75, 0.25), (0.25, 0.78), (0.75, 0.78)):
        c.haste((x, y, 0.0), (x, y, 0.42), 0.01, ferro, 0.4)
    # assento (concha) em fios
    for k in range(12):
        y = 0.28 + k * 0.042
        c.haste((0.25, y, 0.42), (0.75, y, 0.42 - 0.05 * math.sin(math.pi * 0.5)), 0.009, cor, 0.5)
    # encosto inclinado para trás (norte)
    for k in range(12):
        z = 0.45 + k * 0.042
        y = 0.27 - 0.1 * (z - 0.45)
        c.haste((0.25, y, z), (0.75, y, z), 0.009, cor * (0.95 + 0.1 * (k % 2)), 0.5)
    c.curva([(0.25, 0.27, 0.42), (0.25, 0.22, 0.95), (0.75, 0.22, 0.95), (0.75, 0.27, 0.42)], 0.012, ferro, 0.4)
    c.curva([(0.25, 0.27, 0.42), (0.25, 0.8, 0.42), (0.75, 0.8, 0.42), (0.75, 0.27, 0.42)], 0.012, ferro, 0.4)
    return kb.girar(c, lado).render()


def objetos(defs: dict, saida: Path) -> dict:
    pia, cad = "fixtures_sinks_01", "furniture_seating_outdoor_01"
    facing_pia = {dict(defs[pia]["pecas"][i] or []).get("Facing"): i for i in range(32, 36)}
    lista = []
    for lado, fj in (("S", "S"), ("L", "E"), ("N", "N"), ("O", "W")):
        if fj not in facing_pia:
            continue
        lista.append((f"tanque_{lado.lower()}", f"tanque de lavar roupa, frente para {lado}",
                      lambda lado=lado: tanque(lado), kb._props_de(defs, pia, facing_pia[fj], {"GroupName": "Tanque"})))
    lista.append(("botijao_gas", "botijão de gás", botijao, [["BlocksPlacement", ""], ["solidtrans", ""]]))
    lista.append(("espada_sao_jorge", "vaso de espada-de-são-jorge", espada_sao_jorge, [["BlocksPlacement", ""]]))
    for nome_cor, cor in (("vermelha", (196, 46, 40)), ("azul", (40, 96, 190)), ("verde", (40, 150, 90))):
        for lado, i in (("S", 17), ("L", 16), ("N", 18), ("O", 19)):
            lista.append((f"cadeira_fio_{nome_cor}_{lado.lower()}", f"cadeira de fio {nome_cor}, virada para {lado}",
                          lambda lado=lado, cor=cor: cadeira_fio(lado, cor), kb._props_de(defs, cad, i, {"GroupName": "Fio"})))
    for parede in ("N", "O"):
        lista.append((f"relogio_luz_{parede.lower()}", f"padrão de energia (relógio de luz), parede {parede}",
                      lambda parede=parede: _parede(relogio_luz(), parede), []))
        lista.append((f"interfone_numero_{parede.lower()}", f"número, interfone e caixa de correio, parede {parede}",
                      lambda parede=parede: _parede(interfone(), parede), []))
        for d in ("reta", "losango"):
            lista.append((f"grade_janela_{d}_{parede.lower()}", f"grade de janela ({d}), parede {parede}",
                          lambda parede=parede, d=d: _parede(grade_janela(d), parede), []))
    nome = "rsb_objetos_casa_01"
    linhas = (len(lista) + 7) // 8
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = []
    for n, (chave, desc, f, props) in enumerate(lista):
        folha.alpha_composite(f(), ((n % 8) * 128, (n // 8) * 256))
        pecas.append({"peca": f"{nome}_{n}", "nome": chave, "descricao": desc, "props": props})
    pecas += [{"peca": f"{nome}_{n}", "props": []} for n in range(len(lista), linhas * 8)]
    return kf._gravar(folha, nome, "objeto", pecas, saida, {})


if __name__ == "__main__":
    tiles2x, tdefs, saida = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    defs = {d["nome"]: d for d in kit_tiles.ler_definicoes(tdefs)}
    so = sys.argv[4] if len(sys.argv) > 4 else "tudo"
    res = []
    for parte, f in (("paredes", lambda: paredes(tiles2x, saida)), ("muros", lambda: muros(tiles2x, defs, saida)),
                     ("portoes", lambda: portoes(defs, saida)), ("pisos", lambda: pisos(tiles2x, saida)),
                     ("objetos", lambda: objetos(defs, saida))):
        if so in ("tudo", parte):
            res.append(f())
            print(parte, "ok", flush=True)
    print(json.dumps(res, ensure_ascii=False))
