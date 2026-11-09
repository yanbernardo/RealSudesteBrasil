"""Kit Brasil, CIEP ("Brizolão") (item 9 da lista do guia, 09/11/2026).

Referências: fotos do Commons (CIEP em Cascadura, CIEP Vinicius de Moraes em
Belford Roxo, CIEP Nelson Ramos em Mesquita): bloco comprido de 3 andares de
concreto pré-moldado claro, painéis com juntas, janelas de cantos arredondados
com uma faixa curva de peitoril pintada embaixo (verde, vermelha com faixa
amarela, azul) e arcos no térreo.

Folhas em `kits/tiles/` (D-46 e D-47: filtro de estilo, paredes limpas):
- `rsb_paredes_ciep_01` (parede, 8 peças por estilo): fachada de concreto com
  peitoril verde, vermelho e amarelo, e azul (janela de cantos arredondados; a
  porta vira arco de volta inteira); parede interna de escola com barra de tinta
  a óleo verde e azul até 1,3 m.
  Recortes para a janela larga (formatos 1 e 2, peças 48-59): a janela do CIEP
  ocupa 2 tiles, como as janelas largas do jogo (a de igreja): cada metade tem
  `WindowShape` 1 ou 2 e a parede tem o recorte do mesmo número
  (WestWindow1/NorthWindow1, WestWindow2/NorthWindow2 na entrada do BuildingEd).
- `rsb_janelas_ciep_01` (janela): janela basculante de alumínio de 2 tiles
  (metade 1 no tile de x ou y menor, metade 2 no seguinte), oeste e norte;
  quebrada (+64) e sem vidro (+96), com as propriedades da janela de igreja
  (`fixtures_windows_church` 0-3: não abre, quebra, tira o vidro).
- `rsb_pisos_ciep_01` (piso): paviflex bege e marrom, paviflex cinza, cimentado
  liso do pátio coberto.
- `rsb_objetos_ciep_01` (objeto): carteira universitária (4 lados; propriedades
  da cadeira de plástico do jogo), quadro verde de giz (2 peças) e letreiro "CIEP 501" de 3 peças
  e 2 m de altura (paredes norte e oeste), bebedouro de inox (é pia, tem água).

Uso: python -I -X utf8 kit_ciep.py <pasta Tiles/2x> <newtiledefinitions.tiles> <kits/tiles>
"""
from __future__ import annotations

import json
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
NOME_ESCOLA = "CIEP 501"


# ================================================================ texturas
def concreto_painel(seed):
    """Concreto pré-moldado claro, pintado, com juntas dos painéis."""
    U, Z = tf.grade_parede()
    v = Z / 192
    cor = np.array([218, 212, 196.0]) * (0.95 + 0.07 * tf.fbm(U, v, 4, 6, 4, seed))[..., None]
    poro, _ = tf.pontos(U, v, 80, 240, 0.4, 0.25, seed + 1)
    cor = cor * (1 - 0.05 * poro)[..., None]
    h = 0.3 * poro
    # sem junta vertical a cada tile (pedido do usuário: as emendas viravam linhas na fachada)
    junta_v = np.zeros_like(U, dtype=bool)
    junta_h = (Z < 2.0) | (np.abs(Z - 188) < 1.0)
    j = junta_v | junta_h
    cor = np.where(j[..., None], cor * 0.78, cor)
    h = np.where(j, -1.0, h)
    return cor, h


def barra_escola(cor_barra, seed):
    U, Z = tf.grade_parede()
    v = Z / 192
    alto = 1.3 * PX_M
    branco = np.array([232, 230, 222.0]) * (0.96 + 0.05 * tf.fbm(U, v, 3, 5, 3, seed))[..., None]
    barra = np.array(cor_barra, float) * (0.95 + 0.06 * tf.fbm(U, v, 3, 5, 3, seed + 1))[..., None]
    brilho = tf.sstep(0.55, 0.95, tf.vn(U, v, 4, 8, seed + 2)) * 0.08        # tinta a óleo
    barra = barra * (1 + brilho)[..., None]
    em = Z < alto
    cor = np.where(em[..., None], barra, branco)
    linha = np.abs(Z - alto) < 1.2
    cor = np.where(linha[..., None], np.array(cor_barra, float) * 0.55, cor)
    rodape = Z < 5
    cor = np.where(rodape[..., None], np.array(cor_barra, float) * 0.7, cor)
    return cor, np.where(em, 0.15, 0.0)


# ================================================================ janelas e arcos
def _vao(molde_im, idx, face):
    """Limites (u0, u1, z0, z1) do vão (janela ou porta) da peça do molde."""
    a = kf._celula(molde_im, idx)[..., 3]
    U, Z = _uz(face)
    furo = (a == 0) & (U > 0.04) & (U < 0.96) & (Z > 4) & (Z < 186)
    if face == "W":
        furo &= np.mgrid[0:256, 0:128][1] < 63
    else:
        furo &= np.mgrid[0:256, 0:128][1] > 64
    # só o que tem parede em cima e embaixo (o vão de verdade)
    cols = np.where(furo.any(0))[0]
    us, zs = U[furo], Z[furo]
    return float(us.min()), float(us.max()), float(zs.min()), float(zs.max())


def _uz(face):
    Y, X = np.mgrid[0:256, 0:128].astype(float)
    X, Y = X + 0.5, Y + 0.5
    uw = np.clip((63 - X) / 63, 0, 0.9999)
    un = np.clip((X - 63) / 63, 0, 0.9999)
    zw, zn = 192 + 32 * uw - Y, 192 + 32 * un - Y
    oeste = np.ones_like(X, bool) if face == "W" else np.zeros_like(X, bool) if face == "N" else X < 63
    return np.where(oeste, uw, un), np.where(oeste, zw, zn)


def _fora_arredondado(U, Z, u0, u1, z0, z1, r_px, so_topo=False):
    """True onde (u, z) fica fora do retângulo de cantos arredondados (raio em px)."""
    x = U * 63
    x0, x1 = u0 * 63, u1 * 63
    cx = np.clip(x, x0 + r_px, x1 - r_px)
    cz = np.clip(Z, z0 + (0 if so_topo else r_px), z1 - r_px)
    canto = (np.abs(x - cx) > 0) & (np.abs(Z - cz) > 0)
    return canto & (np.hypot(x - cx, Z - cz) > r_px)


def peca_vao(molde, face, texs, Lref, vao, tipo):
    """Peça de janela ou porta: forma do molde, com o vão arredondado."""
    im = np.array(kf.peca_parede_tex(molde, face, texs, Lref))
    U, Z = _uz(face)
    u0, u1, z0, z1 = vao
    w_px, h_px = (u1 - u0) * 63, z1 - z0
    r = w_px / 2 if tipo == "arco" else 0.32 * min(w_px, h_px)
    dentro = (U >= u0) & (U <= u1) & (Z >= z0) & (Z <= z1) & (im[..., 3] == 0)
    if face == "W":
        dentro &= np.mgrid[0:256, 0:128][1] < 63
    else:
        dentro &= np.mgrid[0:256, 0:128][1] > 64
    encher = dentro & _fora_arredondado(U, Z, u0, u1, z0, z1, r, so_topo=(tipo == "arco"))
    tex = texs["W" if face == "W" else "N"]
    cor = tf.amostrar_parede(tex, U, np.clip(Z, 0, 191.9))
    im[..., :3] = np.where(encher[..., None], np.clip(cor, 0, 255).astype(np.uint8), im[..., :3])
    im[..., 3] = np.where(encher, 255, im[..., 3])
    return Image.fromarray(im, "RGBA")


def tex_peitoril(base, vao, cor_peitoril, cor_faixa=None):
    """Textura da peça de janela: o concreto + a faixa curva do peitoril embaixo do vão."""
    cor, h = base
    U, Z = tf.grade_parede()
    u0, u1, z0, z1 = vao
    a, b = u0 - 0.04, u1 + 0.04
    pz0, pz1 = z0 - 0.55 * PX_M, z0 - 0.02 * PX_M
    em = (U >= a) & (U <= b) & (Z >= pz0) & (Z <= pz1)
    em &= ~_fora_arredondado(U, Z, a, b, pz0, pz1 + 30, 0.35 * (b - a) * 63)
    cp = np.array(cor_peitoril, float) * (1 + 0.1 * tf.sstep(pz0, pz1, Z))[..., None]   # curva (luz)
    cor = np.where(em[..., None], cp, cor)
    h = np.where(em, 1.2, h)
    if cor_faixa is not None:
        fx = (Z >= z1 + 0.05 * PX_M) & (Z <= z1 + 0.25 * PX_M)
        cor = np.where(fx[..., None], np.array(cor_faixa, float), cor)
    return cor, h


EXTERNOS = [
    ("ciep_peitoril_verde", "fachada de CIEP: concreto claro, peitoril verde", (70, 150, 120), None),
    ("ciep_peitoril_vermelho", "fachada de CIEP: concreto claro, peitoril vermelho e faixa amarela", (206, 60, 44), (236, 176, 40)),
    ("ciep_peitoril_azul", "fachada de CIEP: concreto claro, peitoril azul", (60, 110, 186), None),
]
INTERNOS = [
    ("escola_barra_verde", "parede de escola com barra verde a óleo", (52, 112, 78)),
    ("escola_barra_azul", "parede de escola com barra azul a óleo", (52, 92, 150)),
]


def paredes(tiles2x: Path, saida: Path) -> dict:
    nome = "rsb_paredes_ciep_01"
    molde_im = Image.open(tiles2x / f"{kf.MOLDE_PAREDE[0]}.png").convert("RGBA")
    base = kf.MOLDE_PAREDE[1]
    w = kf._celula(molde_im, base)
    Lref = np.median(kf._lum(w)[w[..., 3] > 200])
    vaos = {off: _vao(molde_im, base + off, face) for off, face in ((8, "W"), (9, "N"), (10, "W"), (11, "N"))}
    estilos = len(EXTERNOS) + len(INTERNOS)
    linhas = 9                                     # 0-43 estilos, 48-59 recortes da janela larga, 60-63 arco, 64-67 arco largo
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{nome}_{i}", "props": []} for i in range(linhas * 8)]
    ext, inter = [], []
    for k in range(estilos):
        externo = k < len(EXTERNOS)
        if externo:
            chave, desc, cp, cf = EXTERNOS[k]
            base_ch = concreto_painel(150 + k)
            material = "Concrete"
        else:
            chave, desc, cb = INTERNOS[k - len(EXTERNOS)]
            base_ch = barra_escola(cb, 160 + k)
            material = "Plaster"
        texs = kb._iluminar(*base_ch)
        b = (k // 2) * 16 + (k % 2) * 4
        papel = {}
        for off, face, prop in kf.PAPEIS:
            i = b + off
            molde = kf._celula(molde_im, base + off)
            if externo and prop.startswith("Window"):
                t = kb._iluminar(*tex_peitoril(base_ch, vaos[off], cp, cf))
                img = peca_vao(molde, face, t, Lref, vaos[off], "janela")
            elif externo and prop.startswith("DoorWall"):
                img = peca_vao(molde, face, texs, Lref, vaos[off], "arco")
            else:
                img = kf.peca_parede_tex(molde, face, texs, Lref)
            folha.alpha_composite(img, ((i % 8) * 128, (i // 8) * 256))
            papel[prop] = i
            props = ([["MaterialType", material], [prop, ""], ["wall", ""]] if prop.startswith("Wall")
                     else [[prop, ""], ["wall", ""]])
            pecas[i] = {"peca": f"{nome}_{i}", "nome": f"{chave} {prop}", "descricao": desc, "props": props}
        nw = papel["WallNW"]
        pecas[nw]["props"] = [["CornerNorthWall", f"{nome}_{papel['WallN']}"],
                              ["CornerWestWall", f"{nome}_{papel['WallW']}"]] + pecas[nw]["props"]
        e = {"West": papel["WallW"], "North": papel["WallN"], "NorthWest": nw, "SouthEast": papel["WallSE"],
             "WestWindow": papel["WindowW"], "NorthWindow": papel["WindowN"],
             "WestDoor": papel["DoorWallW"], "NorthDoor": papel["DoorWallN"]}
        if externo:                                 # recortes da janela larga (formatos 1 e 2)
            for j, (forma, face) in enumerate(((1, "W"), (1, "N"), (2, "W"), (2, "N"))):
                i = 48 + k * 4 + j
                img = recorte_largo(kf._celula(molde_im, base + (0 if face == "W" else 1)), face, base_ch,
                                    Lref, vaos[8], forma, cp, cf)
                folha.alpha_composite(img, ((i % 8) * 128, (i // 8) * 256))
                prop = "WindowW" if face == "W" else "WindowN"
                pecas[i] = {"peca": f"{nome}_{i}", "nome": f"{chave} janela larga {forma} {face}", "descricao": desc,
                            "props": [["MaterialType", material], ["WindowShape", str(forma)], [prop, ""], ["wall", ""]]}
                e[f"{'West' if face == 'W' else 'North'}Window{forma}"] = i
        (ext if externo else inter).append(e)
        if k == 0:                                  # galeria do térreo: arco vazado (peças 60-63)
            arco = {}
            for i, (face, prop, off) in zip((60, 61), (("W", "DoorWallW", 0), ("N", "DoorWallN", 1))):
                folha.alpha_composite(peca_arco(kf._celula(molde_im, base + off), face, texs, Lref),
                                      ((i % 8) * 128, (i // 8) * 256))
                pecas[i] = {"peca": f"{nome}_{i}", "nome": f"ciep_arcada {prop}",
                            "descricao": "galeria do térreo do CIEP: arco vazado de concreto (passa por ele)",
                            "props": [["MaterialType", "Concrete"], [prop, ""], ["wall", ""]]}
                arco[face] = i
            folha.alpha_composite(kf.peca_parede_tex(kf._celula(molde_im, base + 3), "SE", texs, Lref),
                                  ((63 % 8) * 128, (63 // 8) * 256))
            pecas[63] = {"peca": f"{nome}_63", "nome": "ciep_arcada pilar", "descricao": "pilar da galeria",
                         "props": [["WallSE", ""], ["wall", ""]]}
            ext.append({"West": arco["W"], "North": arco["N"], "NorthWest": papel["WallNW"], "SouthEast": 63,
                        "WestDoor": arco["W"], "NorthDoor": arco["N"],
                        "WestWindow": papel["WindowW"], "NorthWindow": papel["WindowN"]})
            # arco largo de 2 tiles (pedido do usuário): metade 1 no tile de x/y menor, metade 2 no seguinte
            for forma in (1, 2):
                larga = {}
                for face, prop, off in (("W", "DoorWallW", 0), ("N", "DoorWallN", 1)):
                    i = 64 + (forma - 1) * 2 + (0 if face == "W" else 1)
                    folha.alpha_composite(peca_arco_largo(kf._celula(molde_im, base + off), face, texs, Lref, forma),
                                          ((i % 8) * 128, (i // 8) * 256))
                    pecas[i] = {"peca": f"{nome}_{i}", "nome": f"ciep_arco_largo {forma} {prop}",
                                "descricao": f"galeria do CIEP: arco largo de 2 tiles, metade {forma} (passa por ele)",
                                "props": [["MaterialType", "Concrete"], [prop, ""], ["wall", ""]]}
                    larga[face] = i
                ext.append({"West": larga["W"], "North": larga["N"], "NorthWest": papel["WallNW"], "SouthEast": 63,
                            "WestDoor": larga["W"], "NorthDoor": larga["N"],
                            "WestWindow": papel["WindowW"], "NorthWindow": papel["WindowN"]})
    return kf._gravar(folha, nome, "parede", pecas, saida, {"exterior_walls": ext, "interior_walls": inter})


ARCO_LARGO = (0.15, 1.85)  # vão do arco largo ao longo dos 2 tiles (u de 0 a 2)
ARCO_LARGO_TOPO_M = 2.6


def peca_arco_largo(molde, face, texs, Lref, forma):
    """Metade de um arco de volta inteira que ocupa 2 tiles, aberto até o chão."""
    im = np.array(kf.peca_parede_tex(molde, face, texs, Lref))
    U, Z = _uz(face)
    ug = U + (0.0 if forma == 1 else 1.0)
    a, b = ARCO_LARGO
    r = (b - a) * 63 / 2
    topo = ARCO_LARGO_TOPO_M * PX_M
    nasce = topo - r
    centro = (a + b) / 2 * 63
    dentro = (ug >= a) & (ug <= b) & ((Z <= nasce) | (np.hypot(ug * 63 - centro, Z - nasce) <= r))
    im[..., 3] = np.where(dentro, 0, im[..., 3])
    return Image.fromarray(im, "RGBA")


ARCO_U = (0.1, 0.9)        # vão do arco ao longo do tile (sobra pilar de 0,2 tile entre dois arcos)
ARCO_TOPO_M = 2.45         # altura do alto do arco


def peca_arco(molde, face, texs, Lref):
    """Parede de concreto com um arco de volta inteira aberto até o chão (galeria)."""
    im = np.array(kf.peca_parede_tex(molde, face, texs, Lref))
    U, Z = _uz(face)
    u0, u1 = ARCO_U
    r = (u1 - u0) * 63 / 2
    topo = ARCO_TOPO_M * PX_M
    furo = (U >= u0) & (U <= u1) & (Z <= topo) & ~_fora_arredondado(U, Z, u0, u1, -60, topo, r, so_topo=True)
    im[..., 3] = np.where(furo, 0, im[..., 3])
    return Image.fromarray(im, "RGBA")


U_A = 0.2          # a janela larga começa a 0,2 tile da ponta de fora


def _vao_largo(forma):
    """Faixa de u do vão largo na peça: forma 1 = do U_A até a emenda (u = 1), forma 2 = da emenda (u = 0).
    Vale para as duas faces: u cresce de norte para sul (oeste) e de oeste para leste (norte)."""
    return (U_A, 1.6) if forma == 1 else (-0.6, 1 - U_A)


def recorte_largo(molde, face, base_ch, Lref, vao, forma, cp, cf):
    _u0, _u1, z0, z1 = vao
    a, b = _vao_largo(forma)
    cor, h = base_ch
    U, Z = tf.grade_parede()
    pz0, pz1 = z0 - 0.55 * PX_M, z0 - 0.02 * PX_M
    em = (U >= a - 0.04) & (U <= b + 0.04) & (Z >= pz0) & (Z <= pz1)
    em &= ~_fora_arredondado(U, Z, a - 0.04, b + 0.04, pz0, pz1 + 30, 0.3 * 63)
    cor = np.where(em[..., None], np.array(cp, float) * (1 + 0.1 * tf.sstep(pz0, pz1, Z))[..., None], cor)
    # sem relevo na faixa: a textura é periódica e o relevo "dava a volta" na emenda, virando um traço escuro
    if cf is not None:
        fx = (Z >= z1 + 0.05 * PX_M) & (Z <= z1 + 0.25 * PX_M) & (U >= a - 0.04) & (U <= b + 0.04)
        cor = np.where(fx[..., None], np.array(cf, float), cor)
    im = np.array(kf.peca_parede_tex(molde, face, kb._iluminar(cor, h), Lref))
    Up, Zp = _uz(face)
    furo = (Up >= a) & (Up <= b) & (Zp >= z0) & (Zp <= z1) & ~_fora_arredondado(Up, Zp, a, b, z0, z1, 0.3 * (z1 - z0))
    im[..., 3] = np.where(furo, 0, im[..., 3])
    return Image.fromarray(im, "RGBA")


# ================================================================ janela larga (objeto janela)
def _janela_larga(face, forma, estado, vao, seed=0):
    """Janela de vidro limpo no vão largo (pedido do usuário: sem basculante/frestas):
    vidro grande com reflexo, caixilho fino de alumínio (moldura, uma bandeira em cima e
    um montante). estado: inteira, quebrada (buraco no meio, cacos na borda), sem_vidro."""
    _u0, _u1, z0, z1 = vao
    a, b = _vao_largo(forma)
    a, b = max(a, 0.0), min(b, 1.0)
    za, zb = z0 / PX_M + 0.02, z1 / PX_M - 0.02
    c = kl.Cena()
    K = 2.0                                          # a face voltada para a câmera recebe metade da luz: compensa
    alu = np.array([214, 216, 220.0]) * K
    # u "global" ao longo da janela inteira (0 a 2), para o reflexo seguir de uma metade para a outra
    g0 = 0.0 if forma == 1 else 1.0

    def tex_vidro(A, B, f):
        ug = A + g0
        t = (B - za) / (zb - za)
        cor = np.array([136, 176, 196.0]) * (0.92 + 0.14 * t)[..., None]          # céu refletido, mais claro em cima
        faixa = np.abs(((ug * 0.9 + t * 0.7) % 0.9) - 0.3) < 0.07                  # reflexos diagonais
        fina = np.abs(((ug * 0.9 + t * 0.7) % 0.9) - 0.42) < 0.02
        cor = np.where((faixa | fina)[..., None], np.array([214, 230, 238.0]), cor)
        return cor * K

    def cx(u0, u1, d0, d1, z0_, z1_, cor, brilho=0.6, tex=None):
        if face == "N":
            c.caixa(u0, d0, z0_, u1, d1, z1_, cor, brilho=brilho, faces=("y1", "topo"),
                    tex=None if tex is None else (lambda A, B, f: tex(A, B, f)))
        else:
            c.caixa(d0, u0, z0_, d1, u1, z1_, cor, brilho=brilho, faces=("x1", "topo"),
                    tex=None if tex is None else (lambda A, B, f: tex(A, B, f)))
    if estado == "inteira":
        cx(a, b, 0.0, 0.01, za, zb, None, 0.9, tex_vidro)
    elif estado == "quebrada":
        rnd = np.random.default_rng(seed + forma)
        cu, cz = (a + b) / 2 + 0.1 * (rnd.random() - 0.5), za + (zb - za) * (0.4 + 0.2 * rnd.random())
        passo = 0.03
        for u0 in np.arange(a, b, passo):
            for z0_ in np.arange(za, zb, passo):
                ang = np.arctan2(z0_ - cz, (u0 - cu) * 2.0)
                raio = 0.42 + 0.12 * np.sin(ang * 5 + seed) + 0.06 * np.sin(ang * 11)
                if np.hypot((u0 - cu) * 1.6, (z0_ - cz) * 0.9) > raio:
                    cx(u0, min(u0 + passo, b), 0.0, 0.01, z0_, min(z0_ + passo, zb), None, 0.9, tex_vidro)
    # caixilho: moldura, bandeira (travessa a 25% do alto) e montante no meio de cada metade
    cx(a, b, 0.0, 0.035, za - 0.02, za + 0.025, alu)
    cx(a, b, 0.0, 0.035, zb - 0.025, zb + 0.02, alu)
    zt = zb - 0.25 * (zb - za)
    cx(a, b, 0.0, 0.03, zt - 0.012, zt + 0.012, alu)
    fora = a if forma == 1 else b - 0.03
    cx(fora, fora + 0.03, 0.0, 0.035, za, zb, alu)
    meio = (a + b) / 2
    cx(meio - 0.01, meio + 0.01, 0.0, 0.03, za, zt, alu)
    return c.render(sombra=0)


def janelas(defs: dict, vao, saida: Path) -> dict:
    nome = "rsb_janelas_ciep_01"
    molde = "fixtures_windows_church"
    linhas = 13
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{nome}_{i}", "props": []} for i in range(linhas * 8)]
    for desloc, estado in ((0, "inteira"), (64, "quebrada"), (96, "sem_vidro")):
        for j, (forma, face) in enumerate(((1, "W"), (1, "N"), (2, "W"), (2, "N"))):
            i = desloc + j
            folha.alpha_composite(_janela_larga(face, forma, estado, vao, seed=i), ((i % 8) * 128, (i // 8) * 256))
            props = [[k, v] for k, v in (defs[molde]["pecas"][i] or []) if k != "SnowTile"]
            props = [[k, "CIEP" if k == "GroupName" else v] for k, v in props]
            pecas[i] = {"peca": f"{nome}_{i}", "nome": f"janela larga CIEP {estado} {forma} {face}",
                        "descricao": f"janela basculante larga do CIEP ({estado}), metade {forma}, face {face}", "props": props}
    return kf._gravar(folha, nome, "janela", pecas, saida, {})


# ================================================================ pisos
def paviflex(c1, c2, seed):
    S, T = tf.grade_piso()
    n = 3
    i, j = np.floor(S * n), np.floor(T * n)
    cor = np.where((((i + j) % 2) == 0)[..., None], np.array(c1, float), np.array(c2, float))
    cor = cor * (0.93 + 0.08 * tf.fbm(S, T, 6, 6, 4, seed))[..., None]
    pint, _ = tf.pontos(S, T, 90, 90, 0.4, 0.3, seed + 1)
    cor = cor * (1 - 0.06 * pint)[..., None]
    fs, ft = S * n - i, T * n - j
    borda = np.minimum(np.minimum(fs, 1 - fs), np.minimum(ft, 1 - ft)) * tf.PX_PISO / n
    j_ = borda < 0.35
    cor = np.where(j_[..., None], cor * 0.85, cor)
    return cor, np.where(j_, -0.4, 0.0)


def cimentado_patio(seed=173):
    S, T = tf.grade_piso()
    cor = np.array([176, 174, 168.0]) * (0.92 + 0.1 * tf.fbm(S, T, 3, 3, 4, seed))[..., None]
    junta = (np.minimum(S, 1 - S) * tf.PX_PISO < 0.7) | (np.minimum(T, 1 - T) * tf.PX_PISO < 0.7)
    return np.where(junta[..., None], cor * 0.7, cor), np.where(junta, -0.8, 0.0)


PISOS = [
    ("paviflex_bege_marrom", "paviflex bege e marrom (sala de aula, corredor)",
     lambda: paviflex((206, 190, 158), (138, 104, 76), 171), False),
    ("paviflex_cinza", "paviflex cinza (secretaria, biblioteca)",
     lambda: paviflex((186, 186, 180), (150, 152, 148), 172), False),
    ("cimentado_patio", "cimentado liso do pátio coberto", cimentado_patio, True),
]


def pisos(tiles2x: Path, saida: Path) -> dict:
    nome = "rsb_pisos_ciep_01"
    folha = Image.new("RGBA", (1024, 256), (0, 0, 0, 0))
    pecas = []
    for n, (chave, desc, f, ext) in enumerate(PISOS):
        folha.alpha_composite(kf.peca_piso(f(), tiles2x), ((n % 8) * 128, 0))
        pecas.append({"peca": f"{nome}_{n}", "nome": chave, "descricao": desc,
                      "props": [["diamondFloor", ""], ["solidfloor", ""]] + ([["exterior", ""]] if ext else [])})
    pecas += [{"peca": f"{nome}_{n}", "props": []} for n in range(len(PISOS), 8)]
    return kf._gravar(folha, nome, "piso", pecas, saida, {"floors": [{"Floor": i} for i in range(len(PISOS))]})


# ================================================================ objetos
def carteira(lado):
    """Carteira universitária: cadeira de fórmica com prancheta no braço direito."""
    c = kl.Cena()
    ferro = np.array([60, 62, 66.0])
    madeira = np.array([200, 160, 110.0])
    azul = np.array([40, 80, 150.0])
    for x, y in ((0.3, 0.35), (0.68, 0.35), (0.3, 0.72), (0.68, 0.72)):
        c.haste((x, y, 0.0), (x, y, 0.44), 0.012, ferro, 0.5)
    c.caixa(0.27, 0.33, 0.44, 0.71, 0.75, 0.47, azul, brilho=0.4)                       # assento
    c.caixa(0.27, 0.3, 0.52, 0.71, 0.34, 0.86, azul, brilho=0.4)                        # encosto
    c.haste((0.3, 0.33, 0.47), (0.3, 0.32, 0.86), 0.01, ferro, 0.5)
    c.haste((0.68, 0.33, 0.47), (0.68, 0.32, 0.86), 0.01, ferro, 0.5)
    c.caixa(0.62, 0.46, 0.7, 0.86, 0.9, 0.725, madeira, brilho=0.4)                     # prancheta
    c.haste((0.7, 0.5, 0.47), (0.7, 0.55, 0.7), 0.01, ferro, 0.5)
    c.caixa(0.32, 0.4, 0.12, 0.66, 0.7, 0.14, ferro * 1.2)                                # porta-livros
    return kb.girar(c, lado).render()


def quadro(metade):
    """Quadro verde de giz em 2 peças (metade 0 = esquerda), com moldura e calha."""
    c = kl.Cena()
    img = kb.texto_img([("09/11", (236, 236, 228), 0.14, kb.FONTE_GIZ),
                        ("Língua Portuguesa", (236, 236, 228), 0.16, kb.FONTE_GIZ),
                        ("", (0, 0, 0), 0.1, kb.FONTE_GIZ),
                        ("Dever de casa: pág. 42", (236, 236, 200), 0.13, kb.FONTE_GIZ)],
                       1200, 500, (40, 86, 62))
    madeira = np.array([150, 108, 64.0])

    def frente(u, v, face):
        if face != "y1":
            return np.broadcast_to(madeira, np.shape(u) + (3,))
        return kb.amostra(img, (u + metade) / 2, (v - 0.9) / 1.1)
    x0, x1 = (0.08, 1.0) if metade == 0 else (0.0, 0.92)
    c.caixa(x0, 0.0, 0.88, x1, 0.04, 2.02, madeira, brilho=0.2)
    c.caixa(x0 + (0.03 if metade == 0 else 0), 0.0, 0.9, x1 - (0.03 if metade else 0), 0.045, 2.0, None, frente)
    c.caixa(x0, 0.0, 0.84, x1, 0.09, 0.88, madeira, brilho=0.2)                         # calha do giz
    return c


LETREIRO_PARTES = 3                 # 3 tiles de largura e 2 m de altura (pedido do usuário)
LETREIRO_Z = (0.5, 2.5)


def letreiro(parte):
    c = kl.Cena()
    z0, z1 = LETREIRO_Z
    img = kb.texto_img([(NOME_ESCOLA, (40, 70, 140), 0.36, kb.FONTE),
                        ("ESCOLA ESTADUAL", (40, 40, 40), 0.15, kb.FONTE),
                        ("DE TEMPO INTEGRAL", (40, 40, 40), 0.15, kb.FONTE)],
                       2400, 1600, (238, 236, 228), ((40, 70, 140), 26))
    K = 1.9                                           # a face voltada para a câmera recebe metade da luz

    def frente(u, v, face):
        if face != "y1":
            return np.broadcast_to(np.array([200, 198, 190.0]), np.shape(u) + (3,))
        return kb.amostra(img, (u + parte) / LETREIRO_PARTES, (v - z0) / (z1 - z0)) * K
    # só as pontas de fora do letreiro têm lateral (as laterais internas viravam linhas nas emendas)
    faces = ('y1', 'topo') + (('x0',) if parte == 0 else ()) + (('x1',) if parte == LETREIRO_PARTES - 1 else ())
    c.caixa(0.0, 0.0, z0, 1.0, 0.06, z1, None, frente, brilho=0.15, faces=faces)
    return c


def bebedouro(lado):
    c = kl.Cena()
    inox = np.array([196, 200, 206.0])
    c.caixa(0.3, 0.3, 0.0, 0.7, 0.7, 0.9, inox, brilho=0.8)
    c.caixa(0.26, 0.26, 0.9, 0.74, 0.74, 0.98, inox * 1.05, brilho=0.9)
    c.caixa(0.32, 0.32, 0.96, 0.68, 0.68, 0.981, np.array([120, 124, 130.0]), faces=("topo",))
    c.haste((0.42, 0.62, 0.98), (0.42, 0.62, 1.04), 0.012, np.array([220, 220, 224.0]), 0.9)   # esguicho
    c.haste((0.58, 0.62, 0.98), (0.58, 0.62, 1.04), 0.012, np.array([220, 220, 224.0]), 0.9)
    c.caixa(0.36, 0.7, 0.75, 0.64, 0.71, 0.82, np.array([60, 60, 64.0]))                        # botão
    return kb.girar(c, lado).render()


def _parede(c, lado):
    return kb.girar(c, "S" if lado == "N" else "L").render(sombra=0)


def objetos(defs: dict, saida: Path) -> dict:
    cad, pia = "furniture_seating_outdoor_01", "fixtures_sinks_01"
    facing_pia = {dict(defs[pia]["pecas"][i] or []).get("Facing"): i for i in range(32, 36)}
    lista = []
    for lado, i in (("S", 17), ("L", 16), ("N", 18), ("O", 19)):
        lista.append((f"carteira_{lado.lower()}", f"carteira universitária, virada para {lado}",
                      lambda lado=lado: carteira(lado), kb._props_de(defs, cad, i, {"GroupName": "Carteira"})))
    for lado, fj in (("S", "S"), ("L", "E")):
        if fj in facing_pia:
            lista.append((f"bebedouro_{lado.lower()}", f"bebedouro de inox, frente para {lado}",
                          lambda lado=lado: bebedouro(lado), kb._props_de(defs, pia, facing_pia[fj], {"GroupName": "Bebedouro"})))
    for parede in ("N", "O"):
        for m in (0, 1):
            lista.append((f"quadro_verde_{parede.lower()}_{m + 1}", f"quadro verde de giz (parte {m + 1} de 2), parede {parede}",
                          lambda m=m, parede=parede: _parede(quadro(m), parede), []))
        for m in range(LETREIRO_PARTES):
            lista.append((f"letreiro_ciep_{parede.lower()}_{m + 1}",
                          f"letreiro '{NOME_ESCOLA}' (parte {m + 1} de {LETREIRO_PARTES}, 2 m de altura), parede {parede}",
                          lambda m=m, parede=parede: _parede(letreiro(m), parede), []))
    nome = "rsb_objetos_ciep_01"
    linhas = (len(lista) + 7) // 8
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = []
    for n, (chave, desc, f, props) in enumerate(lista):
        folha.alpha_composite(f(), ((n % 8) * 128, (n // 8) * 256))
        pecas.append({"peca": f"{nome}_{n}", "nome": chave, "descricao": desc, "props": props})
    pecas += [{"peca": f"{nome}_{n}", "props": []} for n in range(len(lista), linhas * 8)]
    return kf._gravar(folha, nome, "objeto", pecas, saida, {})


def _vao_padrao(tiles2x):
    molde_im = Image.open(tiles2x / f"{kf.MOLDE_PAREDE[0]}.png").convert("RGBA")
    return _vao(molde_im, kf.MOLDE_PAREDE[1] + 8, "W")


if __name__ == "__main__":
    tiles2x, tdefs, saida = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    defs = {d["nome"]: d for d in kit_tiles.ler_definicoes(tdefs)}
    so = sys.argv[4] if len(sys.argv) > 4 else "tudo"
    res = []
    for parte, f in (("paredes", lambda: paredes(tiles2x, saida)), ("pisos", lambda: pisos(tiles2x, saida)),
                     ("objetos", lambda: objetos(defs, saida)),
                     ("janelas", lambda: janelas(defs, _vao_padrao(tiles2x), saida))):
        if so in ("tudo", parte):
            res.append(f())
    print(json.dumps(res, ensure_ascii=False))
