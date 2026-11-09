"""Texturas com relevo para o Kit Brasil (favela): paredes e pisos.

Cada textura devolve cor (RGB) e altura (em pixels do jogo: positivo sai da
superfície, negativo afunda). A luz é calculada em cima da altura (relevo), como
nas peças pintadas à mão do jogo: tijolo saliente com borda clara em cima e
sombra embaixo, argamassa funda, ranhuras, rachaduras, tinta descascando em
camadas. Tudo é periódico (emenda entre tiles e entre andares).

Paredes: grade (u, z): u = posição ao longo da parede (0..1 por tile), z =
altura em pixels (0..192 por andar). Pisos: grade (s, t) de 0..1 por tile.
"""
from __future__ import annotations

import math

import numpy as np

PX_M = 192 / 2.8                  # pixels de altura por metro
WALL_U, WALL_Z = 189, 576         # amostras por tile (3 por pixel) e por andar
PISO_N = 256                      # amostras por lado do tile no piso


# ---------------------------------------------------------------- ruído periódico
def _h(a, b, s=0):
    a = np.asarray(a, dtype=np.int64)
    b = np.asarray(b, dtype=np.int64)
    h = (a * 374761393 + b * 668265263 + (s + 1) * 2246822519) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFFFFFF) / 4294967295.0


def vn(u, v, ku, kv, seed=0):
    """Ruído de valor suave, periódico: ku células em u (0..1) e kv em v (0..1)."""
    gu, gv = u * ku, v * kv
    iu, iv = np.floor(gu).astype(np.int64), np.floor(gv).astype(np.int64)
    fu, fv = gu - iu, gv - iv
    fu, fv = fu * fu * (3 - 2 * fu), fv * fv * (3 - 2 * fv)
    a = _h(iu % ku, iv % kv, seed)
    b = _h((iu + 1) % ku, iv % kv, seed)
    c = _h(iu % ku, (iv + 1) % kv, seed)
    d = _h((iu + 1) % ku, (iv + 1) % kv, seed)
    return (a * (1 - fu) + b * fu) * (1 - fv) + (c * (1 - fu) + d * fu) * fv


def fbm(u, v, base_u, base_v, oitavas=4, seed=0):
    tot, amp, soma = 0.0, 1.0, 0.0
    for o in range(oitavas):
        tot = tot + amp * vn(u, v, base_u * 2 ** o, base_v * 2 ** o, seed + o * 17)
        soma += amp
        amp *= 0.5
    return tot / soma


def pontos(u, v, ku, kv, raio, prob, seed):
    """Manchinhas redondas (poros, pedrinhas): (máscara 0..1, índice da célula)."""
    gu, gv = u * ku, v * kv
    iu, iv = np.floor(gu).astype(np.int64), np.floor(gv).astype(np.int64)
    cx = iu + 0.2 + 0.6 * _h(iu % ku, iv % kv, seed)
    cy = iv + 0.2 + 0.6 * _h(iu % ku, iv % kv, seed + 1)
    d = np.hypot(gu - cx, gv - cy)
    tem = _h(iu % ku, iv % kv, seed + 2) < prob
    r = raio * (0.6 + 0.8 * _h(iu % ku, iv % kv, seed + 3))
    return np.where(tem, np.clip(1 - d / r, 0, 1), 0.0), (iu % ku) * 7919 + (iv % kv)


def rachaduras(u, v, sx, sy, n, passos, seed, galhos=True):
    """Distância (em px) até rachaduras finas: passeios aleatórios num toro.
    sx, sy: pixels por unidade de u e de v."""
    rnd = np.random.default_rng(seed)
    segs = []
    for _ in range(n):
        p = rnd.random(2)
        ang = rnd.random() * 2 * math.pi
        for k in range(passos):
            ang += rnd.normal(0, 0.55)
            q = p + np.array([math.cos(ang) * 6 / sx, math.sin(ang) * 6 / sy])
            segs.append((p.copy(), q.copy()))
            if galhos and rnd.random() < 0.08:
                b, ab = q.copy(), ang + rnd.choice([-1, 1]) * 0.9
                for _k in range(rnd.integers(2, 6)):
                    ab += rnd.normal(0, 0.5)
                    b2 = b + np.array([math.cos(ab) * 5 / sx, math.sin(ab) * 5 / sy])
                    segs.append((b.copy(), b2.copy()))
                    b = b2
            p = q
    d = np.full(np.shape(u), 1e9)
    for a, b in segs:
        ax, ay = (u - a[0] + 0.5) % 1.0 - 0.5, (v - a[1] + 0.5) % 1.0 - 0.5
        bx, by = (b[0] - a[0]) * sx, (b[1] - a[1]) * sy
        px, py = ax * sx, ay * sy
        L2 = bx * bx + by * by or 1e-9
        t = np.clip((px * bx + py * by) / L2, 0, 1)
        d = np.minimum(d, np.hypot(px - t * bx, py - t * by))
    return d


def sstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def mistura(c1, c2, t):
    t = np.asarray(t, dtype=float)
    if t.ndim == np.ndim(c1) - 1 or (np.ndim(c1) == 3 and t.ndim == 2):
        t = t[..., None]
    return c1 * (1 - t) + c2 * t


def relevo(h, passo_u, passo_v, luz):
    """Fator de luz pelo relevo (grade periódica). luz = (lu, lv, ln): componentes
    nos eixos u, v da grade e para fora da superfície."""
    hu = (np.roll(h, -1, axis=1) - np.roll(h, 1, axis=1)) / (2 * passo_u)
    hv = (np.roll(h, -1, axis=0) - np.roll(h, 1, axis=0)) / (2 * passo_v)
    lu, lv, ln = luz
    n = np.sqrt(hu * hu + hv * hv + 1)
    dif = (-hu * lu - hv * lv + ln) / n
    return np.clip(dif / ln, 0.45, 1.5)


def oclusao(h, prof=2.0):
    """Escurece o que está fundo (argamassa, frestas, rachaduras)."""
    return np.clip(1 + h / prof * 0.22, 0.55, 1.08)


# ---------------------------------------------------------------- paredes
def grade_parede():
    u = (np.arange(WALL_U) + 0.5) / WALL_U
    z = (np.arange(WALL_Z) + 0.5) / WALL_Z * 192
    return np.meshgrid(u, z)          # U, Z com forma (WALL_Z, WALL_U)


def _sujeira_base(U, Z, cor, h, seed, forca=1.0):
    """Sujeira de chão (respingo de lama), mofo e escorrido de chuva."""
    v = Z / 192
    m = Z / PX_M
    lama = sstep(0.55, 0.0, m) * (0.55 + 0.45 * fbm(U, v, 6, 3, 4, seed)) * forca
    resp, _ = pontos(U, v, 40, 30, 0.45, 0.35, seed + 1)
    resp = resp * sstep(0.9, 0.1, m)
    cor = mistura(cor, np.array([74, 62, 50.0]), np.clip(lama * 0.55 + resp * 0.5 * forca, 0, 0.8))
    mofo = sstep(0.35, 0.0, m) * (fbm(U, v, 8, 4, 4, seed + 3) > 0.55) * forca
    cor = mistura(cor, np.array([52, 64, 46.0]), mofo * 0.45)
    # escorrido: listras verticais que descem do alto (mais fortes em cima)
    lista = vn(U, v * 0.25, 23, 1, seed + 5) ** 4 * (0.3 + 0.7 * vn(U, v, 23, 3, seed + 6))
    cor = cor * (1 - 0.35 * lista * sstep(0.2, 1.0, v) * forca)[..., None]
    return cor, h


def tijolo_baiano(seed=1, sujo=False):
    U, Z = grade_parede()
    v = Z / 192
    fiadas, por_tile = 14, 3
    fz = Z / (192 / fiadas)
    linha = np.floor(fz).astype(np.int64)
    gu = U * por_tile + 0.5 * (linha % 2)
    col = np.floor(gu).astype(np.int64)
    du, dz = gu - col, fz - linha
    colm = col % por_tile
    junta_u, junta_z = 2.4 / 21.0, 2.4 / 13.7            # argamassa ~2,4 px
    eu = np.minimum(du, 1 - du) * 21.0                    # distância à borda, em px
    ez = np.minimum(dz, 1 - dz) * 13.7
    borda = np.minimum(eu, ez)
    meia = 1.2
    tijolo = borda > meia
    # cor por tijolo: laranja com queimados e claros
    paleta = np.array([[192, 110, 68], [184, 100, 60], [202, 122, 78], [170, 90, 56], [150, 76, 50],
                       [208, 134, 92], [188, 96, 70]], dtype=float)
    k = (_h(colm, linha, seed) * len(paleta)).astype(int) % len(paleta)
    cor = paleta[k] * (0.92 + 0.16 * _h(colm, linha, seed + 1))[..., None]
    cor = cor * (0.9 + 0.2 * du * (_h(colm, linha, seed + 2) > 0.5))[..., None]   # um lado mais escuro
    cor = cor * (0.93 + 0.14 * fbm(U, v, 21, 14, 3, seed + 3))[..., None]       # mosqueado do barro
    h = -1.1 * (1 - sstep(meia, meia + 1.6, borda))                                 # quina arredondada
    # ranhuras do tijolo baiano (3 frisos ao longo da face)
    for f in (0.28, 0.5, 0.72):
        fr = np.abs(dz - f) * 13.7
        h = h - 0.25 * np.clip(1 - fr / 0.6, 0, 1) * tijolo
    # canto lascado
    canto = _h(colm, linha, seed + 4) < 0.3
    cx = np.where(_h(colm, linha, seed + 5) < 0.5, du, 1 - du) * 21
    cz = np.where(_h(colm, linha, seed + 6) < 0.5, dz, 1 - dz) * 13.7
    lasca = canto & (cx + cz < 3.5 + 2 * _h(colm, linha, seed + 7))
    h = np.where(lasca, h - 1.0, h)
    cor = np.where(lasca[..., None], cor * 0.82 + 20, cor)
    # argamassa: funda, áspera, com areia; às vezes escorrida por cima do tijolo
    arg_cor = np.array([156, 150, 138.0]) * (0.9 + 0.2 * vn(U, v, 60, 120, seed + 8))[..., None]
    areia, _ = pontos(U, v, 90, 260, 0.6, 0.5, seed + 9)
    arg_cor = arg_cor * (1 - 0.18 * areia)[..., None]
    h_arg = -2.2 + 0.7 * vn(U, v, 50, 150, seed + 10)
    bolha = (fbm(U, v, 30, 60, 3, seed + 11) > 0.62) & (borda < meia + 2.6)          # massa escorrida
    em_arg = ~tijolo | bolha
    cor = np.where(em_arg[..., None], arg_cor, cor)
    h = np.where(~tijolo, h_arg, h)
    h = np.where(bolha, 0.5 + 0.4 * vn(U, v, 60, 120, seed + 12), h)
    # massa borrada por cima do tijolo (pedreiro de favela)
    borrao = sstep(0.6, 0.75, fbm(U, v, 6, 10, 4, seed + 13))
    cor = mistura(cor, arg_cor, borrao * 0.55 * tijolo)
    h = h + 0.2 * borrao * tijolo
    cor, h = _sujeira_base(U, Z, cor, h, seed + 20, 1.0 if sujo else 0.35)
    if sujo:
        eflo = sstep(0.62, 0.72, fbm(U, v, 8, 6, 4, seed + 30)) * sstep(1.1, 0.2, Z / PX_M)
        cor = mistura(cor, np.array([214, 210, 198.0]), eflo * 0.5)
        cor = cor * 0.9
    return cor, h


def bloco_concreto(seed=3):
    U, Z = grade_parede()
    v = Z / 192
    fiadas, por_tile = 12, 2
    fz = Z / (192 / fiadas)
    linha = np.floor(fz).astype(np.int64)
    gu = U * por_tile + 0.5 * (linha % 2)
    col = np.floor(gu).astype(np.int64)
    du, dz = gu - col, fz - linha
    colm = col % por_tile
    eu, ez = np.minimum(du, 1 - du) * 31.5, np.minimum(dz, 1 - dz) * 16.0
    borda = np.minimum(eu, ez)
    bloco = borda > 0.9
    cor = np.array([150, 148, 142.0]) * (0.9 + 0.14 * _h(colm, linha, seed))[..., None]
    cor = cor * (0.92 + 0.12 * fbm(U, v, 30, 24, 3, seed + 1))[..., None]
    poro, _ = pontos(U, v, 120, 300, 0.55, 0.45, seed + 2)
    cor = cor * (1 - 0.35 * poro)[..., None]
    h = -0.7 * poro - 0.8 * (1 - sstep(0.9, 2.2, borda))
    canto = (_h(colm, linha, seed + 3) < 0.25) & (np.minimum(eu, 31.5) + ez < 4.5)
    h = np.where(canto, h - 1.2, h)
    arg = np.array([138, 134, 126.0]) * (0.92 + 0.16 * vn(U, v, 60, 120, seed + 4))[..., None]
    cor = np.where(bloco[..., None], cor, arg)
    h = np.where(bloco, h, -1.6 + 0.5 * vn(U, v, 60, 140, seed + 5))
    borrao = sstep(0.62, 0.76, fbm(U, v, 6, 10, 4, seed + 6))
    cor = mistura(cor, arg, borrao * 0.5 * bloco)
    cor, h = _sujeira_base(U, Z, cor, h, seed + 20, 0.6)
    return cor, h


def _reboco_base(U, Z, seed, aspero=1.0):
    v = Z / 192
    grao = vn(U, v, 160, 480, seed) - 0.5
    grao2 = vn(U, v, 80, 240, seed + 1) - 0.5
    h = aspero * (0.55 * grao + 0.35 * grao2)
    # arcos da desempenadeira
    arco = np.sin((U * 9 + vn(U, v, 4, 6, seed + 2) * 2.5 + v * 4) * 2 * math.pi)
    h = h + 0.18 * arco * (vn(U, v, 3, 5, seed + 3) > 0.5)
    cor = np.array([152, 148, 140.0]) * (0.9 + 0.15 * fbm(U, v, 5, 8, 4, seed + 4))[..., None]
    cor = cor * (1 + 0.06 * grao)[..., None]
    return cor, h


def reboco_cru(seed=4):
    U, Z = grade_parede()
    v = Z / 192
    cor, h = _reboco_base(U, Z, seed, 1.4)
    # chapisco: pontos ásperos mais escuros
    chap, _ = pontos(U, v, 70, 210, 0.5, 0.55, seed + 6)
    cor = cor * (1 - 0.22 * chap)[..., None]
    h = h + 0.6 * chap
    rac = rachaduras(U, v, 63, 192, 1, 14, seed + 7, galhos=False)
    fio = np.clip(1 - rac / 0.55, 0, 1)
    cor = cor * (1 - 0.28 * fio)[..., None]
    h = h - 0.5 * fio
    # remendos de massa mais nova (mais clara e lisa)
    rem = sstep(0.66, 0.7, fbm(U, v, 4, 6, 3, seed + 8))
    cor = mistura(cor, np.array([170, 166, 158.0]), rem * 0.6)
    h = h * (1 - 0.6 * rem) + 0.3 * rem
    cor, h = _sujeira_base(U, Z, cor, h, seed + 20, 0.8)
    return cor, h


def reboco_pintado(tinta, seed=5, descasca=0.12, tijolo=None):
    """Reboco com tinta barata desbotada, descascando em duas camadas: a tinta sai e
    mostra o reboco cinza; onde o reboco também caiu, aparece o tijolo."""
    U, Z = grade_parede()
    v = Z / 192
    reb, h_reb = _reboco_base(U, Z, seed, 0.7)
    tinta = np.array(tinta, dtype=float)
    tinta = 0.8 * tinta + 0.2 * tinta.mean()
    sol = 1.0 + 0.08 * v                                         # desbota mais em cima (sol)
    manchas = fbm(U, v, 4, 6, 4, seed + 1)
    cor = tinta * (sol * (0.9 + 0.2 * manchas))[..., None]
    cor = mistura(cor, np.array([228, 226, 218.0]), sstep(0.55, 0.85, fbm(U, v, 3, 4, 3, seed + 2)) * 0.25)  # giz
    cor = cor * (1 + 0.04 * h_reb)[..., None]
    h = h_reb * 0.6
    # descascado: tinta sai (reboco aparece), e no meio o reboco cai (tijolo aparece)
    n1 = fbm(U, v, 7, 12, 5, seed + 3)
    sai_tinta = n1 > (0.78 - descasca)
    sai_reboco = n1 > (0.86 - descasca * 0.6)
    borda_tinta = sstep(0.0, 0.02, n1 - (0.78 - descasca)) * sai_tinta
    cor = np.where(sai_tinta[..., None], reb * 1.02, cor)
    h = np.where(sai_tinta, h_reb - 0.45, h)
    cor = np.where((sai_tinta & ~(borda_tinta > 0.6))[..., None], cor, cor)
    if tijolo is not None:
        tc, th = tijolo
        cor = np.where(sai_reboco[..., None], tc * 0.95, cor)
        h = np.where(sai_reboco, th - 2.2, h)
    # lasquinhas de tinta soltando na borda (claras)
    lasca = (np.abs(n1 - (0.78 - descasca)) < 0.006)
    cor = np.where(lasca[..., None], np.minimum(cor * 1.25, 255), cor)
    # rachaduras finas e escorrido
    rac = rachaduras(U, v, 63, 192, 1, 12, seed + 7, galhos=False)
    fio = np.clip(1 - rac / 0.5, 0, 1)
    cor = cor * (1 - 0.25 * fio)[..., None]
    h = h - 0.5 * fio
    cor, h = _sujeira_base(U, Z, cor, h, seed + 20, 0.9)
    return cor, h


def madeira_barraco(seed=10):
    U, Z = grade_parede()
    v = Z / 192
    m = Z / PX_M
    n_tab = 5
    larg = np.array([0.75 + 0.5 * _h(i, 0, seed) for i in range(n_tab)])
    bordas = np.concatenate([[0], np.cumsum(larg)]) / larg.sum()
    idx = np.clip(np.searchsorted(bordas, U, side="right") - 1, 0, n_tab - 1)
    esq, dir_ = bordas[idx], bordas[idx + 1]
    du = (U - esq) / (dir_ - esq)
    paleta = np.array([[120, 104, 84], [108, 94, 78], [132, 116, 92], [98, 88, 76], [126, 108, 86]], float)
    cor = paleta[(idx + seed) % len(paleta)]
    # tábua com resto de tinta velha (azul / verde / vermelha) descascando
    tinta = np.array([[78, 112, 146], [86, 128, 92], [152, 64, 52]], float)
    pintada = _h(idx, 1, seed + 1) < 0.4
    resto = fbm(U, v, 12, 10, 4, seed + 2) > 0.48
    cor = np.where((pintada & resto)[..., None], tinta[(idx + seed) % 3] * 0.85, cor)
    # veio: linhas ao longo da tábua (vertical), com ondulação
    veio = np.sin((du * (9 + 4 * _h(idx, 2, seed)) + 0.9 * fbm(U, v, 10, 3, 3, seed + 3)) * 2 * math.pi)
    h = 0.35 * veio
    cor = cor * (0.94 + 0.06 * veio)[..., None]
    cor = cor * (0.88 + 0.22 * vn(U, v, 40, 6, seed + 4))[..., None]
    # nós
    nu, nv = 0.3 + 0.4 * _h(idx, 3, seed), 0.15 + 0.7 * _h(idx, 4, seed)
    dn = np.hypot((du - nu) * (dir_ - esq) * 63, (v - nv) * 192 * 0.45)
    no = (_h(idx, 5, seed) < 0.5) & (dn < 3.2)
    cor = np.where(no[..., None], cor * (0.62 + 0.08 * np.sin(dn * 2.4) + 0.12 * dn / 3.2)[..., None], cor)
    h = np.where(no, h - 0.4, h)
    # pé da tábua apodrecido e escuro
    cor = cor * (1 - 0.35 * sstep(0.35, 0.0, m))[..., None]
    # frestas entre tábuas
    borda_px = np.minimum(U - esq, dir_ - U) * 63
    fresta = borda_px < 0.9
    h = np.where(fresta, -3.0, h - 0.6 * (1 - sstep(0.9, 2.0, borda_px)))
    cor = np.where(fresta[..., None], np.array([30, 25, 22.0]), cor)
    # travessas horizontais (sarrafos) com pregos
    for alt in (0.35, 2.15):
        dist = np.abs(m - alt) * PX_M
        trav = dist < 4.5
        h = np.where(trav, 2.6 - 0.8 * (dist / 4.5) ** 4, h)
        cor = np.where(trav[..., None], np.array([112, 98, 80.0]) * (0.9 + 0.2 * vn(U, v, 30, 4, seed + 6))[..., None], cor)
        for cx in bordas[:-1] + (bordas[1:] - bordas[:-1]) / 2:
            dp = np.hypot((U - cx) * 63, (m - alt) * PX_M)
            prego = dp < 1.1
            cor = np.where(prego[..., None], np.array([70, 62, 56.0]), cor)
            h = np.where(prego, 3.1, h)
            ferr = (np.abs(U - cx) * 63 < 0.9) & (m < alt) & (m > alt - 0.25)
            cor = np.where((ferr & ~trav)[..., None], cor * 0.8 + np.array([20, 4, -6.0]), cor)
    return cor, h


def textura_parede(nome: str):
    """(cor, altura) na grade da parede para cada estilo."""
    tij = tijolo_baiano(1)
    tabela = {
        "tijolo_baiano": lambda: tij,
        "tijolo_baiano_sujo": lambda: tijolo_baiano(2, True),
        "bloco_concreto": lambda: bloco_concreto(3),
        "reboco_cru": lambda: reboco_cru(4),
        "reboco_rosa": lambda: reboco_pintado((206, 152, 150), 5, 0.12, tij),
        "reboco_azul": lambda: reboco_pintado((132, 166, 198), 6, 0.08, tij),
        "reboco_verde_agua": lambda: reboco_pintado((142, 192, 174), 7, 0.10, tij),
        "reboco_amarelo": lambda: reboco_pintado((216, 192, 114), 8, 0.10, tij),
        "reboco_branco_encardido": lambda: reboco_pintado((212, 208, 196), 9, 0.06, tij),
        "madeira_barraco": lambda: madeira_barraco(10),
    }
    return tabela[nome]()


def parede_iluminada(nome: str):
    """Duas texturas prontas (face oeste e face norte), com o relevo iluminado."""
    cor, h = textura_parede(nome)
    passo_u = 63.0 / WALL_U          # pixels por amostra ao longo
    passo_v = 192.0 / WALL_Z
    out = {}
    for face, lu in (("W", 0.35), ("N", -0.35)):
        luz = np.array([lu, 0.55, 0.76])
        luz = luz / np.linalg.norm(luz)
        f = relevo(h, passo_u, passo_v, luz) * oclusao(h)
        out[face] = np.clip(cor * f[..., None], 0, 255)
    return out


def amostrar_parede(tex, u, z):
    """Lê a textura pronta nas posições (u em 0..1 por tile, z em px)."""
    iu = np.floor(np.mod(u, 1.0) * WALL_U).astype(int) % WALL_U
    iz = np.clip(np.floor(z / 192 * WALL_Z).astype(int), 0, WALL_Z - 1)
    return tex[iz, iu]


# ---------------------------------------------------------------- pisos
def grade_piso():
    s = (np.arange(PISO_N) + 0.5) / PISO_N
    return np.meshgrid(s, s)          # S (ao longo de x), T (de y); forma (t, s)


PX_PISO = 89.0                        # pixels por tile ao longo de cada eixo do piso


def laje_crua(seed, poca=False, rachada=False, entulho=False):
    S, T = grade_piso()
    base = np.array([162, 160, 154.0])
    cor = base * (0.9 + 0.16 * fbm(S, T, 3, 3, 5, seed))[..., None]
    # marca da forma: tábuas de 1/4 de tile ao longo de x, com veio de madeira impresso
    tab = np.floor(T * 4).astype(np.int64)
    ft = T * 4 - tab
    emenda = np.minimum(ft, 1 - ft) * PX_PISO / 4 < 0.7
    veio = np.sin((S * (14 + 6 * _h(tab % 4, 0, seed)) + 1.4 * fbm(S, T, 4, 16, 3, seed + 1)) * 2 * math.pi)
    h = 0.12 * veio - 0.5 * emenda
    cor = cor * (0.97 + 0.03 * veio)[..., None] * (1 - 0.06 * emenda)[..., None]
    cor = cor * (0.96 + 0.08 * _h(tab % 4, 1, seed))[..., None]
    # poros e brita aparente
    poro, _ = pontos(S, T, 70, 70, 0.4, 0.45, seed + 2)
    cor = cor * (1 - 0.35 * poro)[..., None]
    h = h - 0.6 * poro
    brita, _ = pontos(S, T, 34, 34, 0.45, 0.25, seed + 3)
    cor = mistura(cor, np.array([132, 128, 122.0]), brita * 0.5)
    h = h + 0.35 * brita
    # manchas de água / umidade com borda
    mancha = fbm(S, T, 2, 2, 5, seed + 4)
    m1 = sstep(0.56, 0.62, mancha)
    cor = cor * (1 - 0.14 * m1 - 0.08 * (np.abs(mancha - 0.59) < 0.01))[..., None]
    # ferrugem pingada
    fer, _ = pontos(S, T, 9, 9, 0.35, 0.15, seed + 5)
    cor = mistura(cor, np.array([140, 84, 52.0]), fer * 0.55)
    if poca:
        p = sstep(0.62, 0.66, fbm(S, T, 2, 2, 4, seed + 6))
        cor = mistura(cor, cor * 0.62 + np.array([0, 2, 6.0]), p)
        h = h * (1 - 0.8 * p)
        borda = np.abs(fbm(S, T, 2, 2, 4, seed + 6) - 0.66) < 0.008
        cor = cor * (1 - 0.15 * borda)[..., None]
    rac = rachaduras(S, T, PX_PISO, PX_PISO, 3 if rachada else 1, 30 if rachada else 10, seed + 7, galhos=rachada)
    fio = np.clip(1 - rac / (0.8 if rachada else 0.5), 0, 1)
    cor = cor * (1 - (0.5 if rachada else 0.25) * fio)[..., None]
    h = h - (1.0 if rachada else 0.4) * fio
    if rachada:
        musgo = (rac < 1.6) * (fbm(S, T, 8, 8, 3, seed + 8) > 0.5)
        cor = mistura(cor, np.array([70, 92, 54.0]), musgo * 0.6)
    if entulho:
        pedra, i = pontos(S, T, 18, 18, 0.55, 0.3, seed + 9)
        tom = 0.75 + 0.5 * _h(i, 0, seed)
        cor = mistura(cor, np.array([150, 146, 138.0]) * tom[..., None], sstep(0.0, 0.15, pedra))
        h = h + 2.2 * np.sqrt(pedra)
    return cor, h


def manta(seed, remendo=False, bolhas=True):
    S, T = grade_piso()
    grao = vn(S, T, 180, 180, seed) - 0.5
    cor = np.array([50, 50, 52.0]) * (0.86 + 0.28 * fbm(S, T, 3, 3, 4, seed + 1))[..., None]
    cor = cor * (1 + 0.25 * grao)[..., None]
    h = 0.35 * grao
    # rolos de manta a cada meio tile, sobrepostos (borda derretida mais escura)
    f = (S * 2) % 1
    sobre = f < 0.07
    h = h + 0.7 * sobre
    borda = np.abs(f - 0.07) * PX_PISO / 2 < 0.8
    cor = np.where(borda[..., None], cor * 0.62, cor)
    cor = np.where(sobre[..., None], cor * 1.08, cor)
    # poeira acinzentada
    poeira = sstep(0.5, 0.8, fbm(S, T, 3, 3, 4, seed + 2))
    cor = mistura(cor, np.array([110, 108, 104.0]), poeira * 0.35)
    if bolhas:
        b, _ = pontos(S, T, 6, 6, 0.42, 0.35, seed + 3)
        h = h + 2.6 * np.sqrt(b)
    if remendo:
        r = sstep(0.6, 0.63, fbm(S, T, 3, 3, 3, seed + 4))
        amassado = vn(S, T, 60, 60, seed + 5) + 0.5 * vn(S, T, 120, 120, seed + 6)
        alu = np.array([186, 188, 192.0]) * (0.85 + 0.25 * amassado)[..., None]
        cor = mistura(cor, alu, r)
        h = h * (1 - r) + r * (1.2 * amassado + 0.6)
    return cor, h


def ralo(seed):
    cor, h = laje_crua(seed)
    S, T = grade_piso()
    d = np.hypot(S - 0.5, T - 0.5) * PX_PISO
    molhado = sstep(16, 6, d)
    cor = cor * (1 - 0.3 * molhado)[..., None]
    aro = (d > 7.5) & (d < 9.5)
    grelha = d < 7.5
    ang = np.arctan2(T - 0.5, S - 0.5)
    fenda = grelha & (np.sin(ang * 8) > 0.2) & (d > 2)
    cor = np.where(aro[..., None], np.array([78, 76, 74.0]), cor)
    cor = np.where(grelha[..., None], np.array([92, 88, 84.0]), cor)
    cor = np.where(fenda[..., None], np.array([22, 22, 22.0]), cor)
    h = np.where(aro, 1.0, np.where(fenda, -2.5, np.where(grelha, 0.4, h - 0.6 * molhado)))
    return cor, h


def ceramica(cores, seed, junta_cor=(170, 164, 150), por_tile=3, quebrada=0.06):
    S, T = grade_piso()
    gs, gt = S * por_tile, T * por_tile
    i, j = np.floor(gs).astype(np.int64), np.floor(gt).astype(np.int64)
    fs, ft = gs - i, gt - j
    lado = PX_PISO / por_tile
    borda = np.minimum(np.minimum(fs, 1 - fs), np.minimum(ft, 1 - ft)) * lado
    peca = borda > 0.8
    im, jm = i % por_tile, j % por_tile
    cores = np.array(cores, dtype=float)
    cor = cores[(_h(im, jm, seed) * len(cores)).astype(int) % len(cores)]
    cor = cor * (0.95 + 0.1 * _h(im, jm, seed + 1))[..., None]
    # textura do esmalte (pontilhado leve) e brilho
    cor = cor * (0.96 + 0.08 * vn(S, T, 90, 90, seed + 2))[..., None]
    brilho = sstep(0.55, 0.95, (1 - fs) * 0.5 + (1 - ft) * 0.5)
    cor = cor * (1 + 0.08 * brilho)[..., None]
    h = -0.9 * (1 - sstep(0.8, 2.0, borda))
    # peça trincada e canto lascado
    trinca = _h(im, jm, seed + 3) < quebrada
    rac = rachaduras(S, T, PX_PISO, PX_PISO, 4, 12, seed + 4, galhos=False)
    fio = trinca & (rac < 0.6)
    cor = np.where(fio[..., None], cor * 0.55, cor)
    h = np.where(fio, h - 0.7, h)
    lasca = (_h(im, jm, seed + 5) < 0.2) & (np.minimum(fs, 1 - fs) * lado + np.minimum(ft, 1 - ft) * lado < 3.0)
    cor = np.where(lasca[..., None], np.array([150, 140, 126.0]), cor)
    h = np.where(lasca, h - 0.8, h)
    junta = np.array(junta_cor, dtype=float) * (0.8 + 0.25 * vn(S, T, 50, 50, seed + 6))[..., None]
    cor = np.where(peca[..., None], cor, junta)
    h = np.where(peca, h, -1.0)
    sujeira = sstep(0.55, 0.8, fbm(S, T, 3, 3, 4, seed + 7))
    cor = cor * (1 - 0.12 * sujeira)[..., None]
    return cor, h


def cimento_queimado(cor0, seed, rachado=False):
    S, T = grade_piso()
    cor0 = np.array(cor0, dtype=float)
    mosq = fbm(S, T, 4, 4, 5, seed)
    cor = cor0 * (0.84 + 0.3 * mosq)[..., None]
    # marcas da colher de pedreiro (arcos)
    arco = np.sin((S * 3 + T * 2 + fbm(S, T, 3, 3, 3, seed + 1) * 3.0) * 2 * math.pi)
    cor = cor * (1 + 0.018 * arco)[..., None]
    h = 0.03 * arco
    # desgaste (mais claro onde se pisa) e junta plástica na borda do tile
    gasto = sstep(0.55, 0.75, fbm(S, T, 2, 2, 4, seed + 2))
    cor = mistura(cor, cor0 * 1.25, gasto * 0.4)
    junta = (np.minimum(S, 1 - S) * PX_PISO < 0.6) | (np.minimum(T, 1 - T) * PX_PISO < 0.6)
    cor = np.where(junta[..., None], cor * 0.6, cor)
    h = np.where(junta, -0.6, h)
    if rachado:
        rac = rachaduras(S, T, PX_PISO, PX_PISO, 1, 18, seed + 3)
        fio = np.clip(1 - rac / 0.6, 0, 1)
        cor = cor * (1 - 0.45 * fio)[..., None]
        h = h - 0.8 * fio
    return cor, h


def contrapiso(seed, rachado=False):
    S, T = grade_piso()
    grao = vn(S, T, 150, 150, seed) - 0.5
    cor = np.array([150, 146, 138.0]) * (0.88 + 0.22 * fbm(S, T, 3, 3, 5, seed + 1))[..., None]
    cor = cor * (1 + 0.14 * grao)[..., None]
    h = 0.5 * grao
    arcos = np.sin((S * 5 + T * 3 + fbm(S, T, 3, 3, 3, seed + 2) * 4.0) * 2 * math.pi)
    h = h + 0.12 * arcos * (vn(S, T, 3, 3, seed + 5) > 0.45)
    brita, _ = pontos(S, T, 40, 40, 0.45, 0.3, seed + 3)
    cor = mistura(cor, np.array([118, 114, 108.0]), brita * 0.45)
    h = h + 0.5 * brita
    if rachado:
        rac = rachaduras(S, T, PX_PISO, PX_PISO, 1, 22, seed + 4)
        fio = np.clip(1 - rac / 0.6, 0, 1)
        cor = cor * (1 - 0.4 * fio)[..., None]
        h = h - 0.8 * fio
    return cor, h


def piso_iluminado(cor, h):
    """Relevo do piso com a luz vindo do noroeste (como os pisos do jogo)."""
    passo = PX_PISO / PISO_N
    luz = np.array([-0.4, -0.4, 0.82])
    luz = luz / np.linalg.norm(luz)
    f = relevo(h, passo, passo, luz) * oclusao(h)
    return np.clip(cor * f[..., None], 0, 255)


def amostrar_piso(tex, s, t):
    i = np.floor(np.mod(s, 1.0) * PISO_N).astype(int) % PISO_N
    j = np.floor(np.mod(t, 1.0) * PISO_N).astype(int) % PISO_N
    return tex[j, i]
