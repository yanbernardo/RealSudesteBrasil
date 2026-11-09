"""Kit Brasil, morro e favela: a laje (telhado plano de concreto) e o que tem nela.

Favela brasileira não tem telha inclinada: o teto é laje de concreto, com mureta
em volta, caixa d'água, ferro de espera para o próximo andar, churrasqueira,
varal e antena (pedido do usuário, 08/11/2026; refeito com mais detalhe em
09/11/2026). Folhas em `kits/tiles/`:

- `rsb_lajes_01` (piso): laje crua em 4 variações (lisa, com poça, rachada com
  musgo, com entulho), manta asfáltica (2), manta com remendo de alumínio, laje
  com ralo, terraço de cerâmica vermelha e bege (2 cada). Texturas com relevo
  (`texturas_favela.py`). No BuildingEd: pisos e telhado plano ("Roof Tops").
- `rsb_muretas_favela_01` (parede): mureta de laje de meia altura, baixa e
  parede inacabada em degraus, em 4 acabamentos; molde: as muretas do jogo
  (`walls_exterior_house_low_01`), mesma forma, sombra e propriedades (pulável).
- `rsb_objetos_laje_01` (objeto): renderizador 3D no ângulo do jogo, com luz,
  brilho, sombra no chão e oclusão: caixa d'água azul (1000 e 500 L, com
  frisos, tampa nervurada, canos e registro), caixa velha de amianto,
  churrasqueira de tijolo (2 lados, com bancada, grelha, carvão, fuligem e
  chapéu na chaminé), pilar com ferro de espera (ferro nervurado e enferrujado,
  estribos), ferro de espera solto, antena parabólica (nervuras, braço, LNB,
  cabo), varal com roupas (2 lados) e pilha de tijolos.

Uso: python -I -X utf8 kit_laje.py <pasta Tiles/2x> <newtiledefinitions.tiles> <kits/tiles>
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit_favela as kf  # noqa: E402
import kit_tiles  # noqa: E402
import texturas_favela as tf  # noqa: E402

PX_M = tf.PX_M


# ---------------------------------------------------------------- lajes
LAJES = [
    ("laje_crua_a", "laje de concreto crua", lambda: tf.laje_crua(41)),
    ("laje_crua_b", "laje crua com poça (usar de vez em quando)", lambda: tf.laje_crua(42, poca=True)),
    ("laje_crua_c", "laje crua rachada, com musgo", lambda: tf.laje_crua(43, rachada=True)),
    ("laje_crua_d", "laje crua com entulho miúdo", lambda: tf.laje_crua(44, entulho=True)),
    ("laje_manta_a", "laje com manta asfáltica", lambda: tf.manta(45)),
    ("laje_manta_b", "laje com manta asfáltica, sem bolhas", lambda: tf.manta(46, bolhas=False)),
    ("laje_manta_remendo", "manta com remendo de alumínio (usar de vez em quando)", lambda: tf.manta(47, remendo=True)),
    ("laje_ralo", "laje com ralo", lambda: tf.ralo(48)),
    ("terraco_ceramica_vermelha_a", "terraço de cerâmica vermelha",
     lambda: tf.ceramica([(150, 66, 50), (142, 60, 46), (158, 72, 54)], 49, (176, 170, 156), quebrada=0.0)),
    ("terraco_ceramica_vermelha_b", "terraço de cerâmica vermelha, variação",
     lambda: tf.ceramica([(146, 62, 48), (156, 70, 52), (138, 58, 44)], 50, (170, 164, 150), quebrada=0.1)),
    ("terraco_ceramica_bege_a", "terraço de cerâmica bege",
     lambda: tf.ceramica([(208, 194, 166), (200, 186, 160)], 51, (160, 154, 140), quebrada=0.0)),
    ("terraco_ceramica_bege_b", "terraço de cerâmica bege, variação",
     lambda: tf.ceramica([(202, 188, 160), (212, 198, 170)], 52, (156, 150, 136), quebrada=0.1)),
]


def lajes(tiles2x: Path, saida: Path) -> dict:
    nome = "rsb_lajes_01"
    linhas = (len(LAJES) + 7) // 8
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = []
    for n, (chave, desc, f) in enumerate(LAJES):
        folha.alpha_composite(kf.peca_piso(f(), tiles2x), ((n % 8) * 128, (n // 8) * 256))
        pecas.append({"peca": f"{nome}_{n}", "nome": chave, "descricao": desc,
                      "props": [["diamondFloor", ""], ["exterior", ""], ["solidfloor", ""]]})
    pecas += [{"peca": f"{nome}_{n}", "props": []} for n in range(len(LAJES), linhas * 8)]
    topos = [{"West1": i, "West2": i, "West3": i, "North1": i, "North2": i, "North3": i, "_offset": True}
             for i in range(len(LAJES))]
    return kf._gravar(folha, nome, "piso", pecas, saida,
                      {"floors": [{"Floor": i} for i in range(len(LAJES))], "roof_tops": topos})


# ---------------------------------------------------------------- muretas
MOLDE_MURETA = "walls_exterior_house_low_01"
# (peça no molde, face): meia altura 8-11, baixa 0-3, inacabada em degraus 16-19
PECAS_MURETA = [(8, "W"), (9, "N"), (10, "NW"), (11, "SE"), (0, "W"), (1, "N"), (2, "NW"), (3, "SE"),
                (16, "W"), (17, "N"), (18, "NW"), (19, "SE")]
ACABAMENTOS = [kf.ESTILOS[0], kf.ESTILOS[2], kf.ESTILOS[3], kf.ESTILOS[8]]   # tijolo, bloco, reboco cru, branco


def muretas(tiles2x: Path, defs: dict, saida: Path) -> dict:
    nome = "rsb_muretas_favela_01"
    molde = Image.open(tiles2x / f"{MOLDE_MURETA}.png").convert("RGBA")
    sd = defs[MOLDE_MURETA]
    ref = kf._celula(molde, 8)
    Lref = np.median(kf._lum(ref)[ref[..., 3] > 200])
    linhas = ((len(ACABAMENTOS) + 1) // 2) * 3
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{nome}_{i}", "props": []} for i in range(linhas * 8)]
    for k, (chave, desc, material, _tex) in enumerate(ACABAMENTOS):
        texs = kf.texturas_estilo(chave, True)
        base = (k // 2) * 24 + (k % 2) * 4
        novo_de = {velho: base + (j // 4) * 8 + j % 4 for j, (velho, _f) in enumerate(PECAS_MURETA)}
        for j, (velho, face) in enumerate(PECAS_MURETA):
            cel = kf._celula(molde, velho)
            if not (cel[..., 3] > 0).any():
                continue
            i = novo_de[velho]
            folha.alpha_composite(kf.peca_parede_tex(cel, face, texs, Lref), ((i % 8) * 128, (i // 8) * 256))
            props = []
            for p, v in sd["pecas"][velho]:
                if v.startswith(MOLDE_MURETA):
                    v = f"{nome}_{novo_de[int(v.rsplit('_', 1)[1])]}"
                props.append([p, v])
            if any(p == "wall" for p, _v in props):
                props.append(["MaterialType", material])
            altura = {0: "meia altura", 1: "baixa", 2: "inacabada em degraus"}[j // 4]
            pecas[i] = {"peca": f"{nome}_{i}", "nome": f"mureta {altura} {chave} {face}", "descricao": desc, "props": props}
    moveis = []
    for k, (chave, desc, _m, _t) in enumerate(ACABAMENTOS):
        base = (k // 2) * 24 + (k % 2) * 4
        itens = []
        for linha in range(3):              # meia altura, baixa, inacabada
            w, n, nw = base + linha * 8, base + linha * 8 + 1, base + linha * 8 + 2
            itens.append([{"orient": "W", "tiles": {"0,0": w}}, {"orient": "N", "tiles": {"0,0": n}}])
            itens.append([{"orient": "W", "tiles": {"0,0": nw}}])                # quina
        moveis.append({"grupo": f"Kit Brasil - Muretas de laje: {desc.split(',')[0].split('(')[0].strip()}",
                       "camada": "Walls", "itens": itens})
    return kf._gravar(folha, nome, "parede", pecas, saida, {}, moveis=moveis)


# ---------------------------------------------------------------- renderizador 3D
LUZ = np.array([-0.55, -0.25, 0.80])
LUZ = LUZ / np.linalg.norm(LUZ)
OLHO = np.array([1.0, 1.0, 0.933])
OLHO = OLHO / np.linalg.norm(OLHO)


class Cena:
    """Pontos 3D (x, y em tiles dentro do tile; z em metros) com cor, normal e
    brilho, desenhados no ângulo do jogo com profundidade, sombra no chão e
    oclusão perto do chão; SS x maior e reduzido (antisserrilhado)."""
    SS = 4

    def __init__(self):
        self.p, self.c, self.n, self.b = [], [], [], []

    def add(self, pts, cor, nor, brilho=0.0):
        pts = np.asarray(pts, dtype=float).reshape(-1, 3)
        k = len(pts)
        self.p.append(pts)
        self.c.append(np.broadcast_to(np.asarray(cor, dtype=float), (k, 3)) if np.ndim(cor) == 1
                      else np.asarray(cor, dtype=float).reshape(-1, 3))
        self.n.append(np.broadcast_to(np.asarray(nor, dtype=float), (k, 3)) if np.ndim(nor) == 1
                      else np.asarray(nor, dtype=float).reshape(-1, 3))
        self.b.append(np.full(k, float(brilho)))

    # -- formas
    def caixa(self, x0, y0, z0, x1, y1, z1, cor, tex=None, passo=0.003, brilho=0.0, faces="all"):
        """Caixa alinhada. `tex(u, v, face)` -> cor por ponto (u, v em tiles/metros na face)."""
        defs = {
            "topo": (lambda a, b: (a, b, np.full_like(a, z1)), (x0, x1, y0, y1), (0, 0, 1)),
            "x1": (lambda a, b: (np.full_like(a, x1), a, b), (y0, y1, z0, z1), (1, 0, 0)),
            "y1": (lambda a, b: (a, np.full_like(a, y1), b), (x0, x1, z0, z1), (0, 1, 0)),
            "x0": (lambda a, b: (np.full_like(a, x0), a, b), (y0, y1, z0, z1), (-1, 0, 0)),
            "y0": (lambda a, b: (a, np.full_like(a, y0), b), (x0, x1, z0, z1), (0, -1, 0)),
        }
        for face, (f, (a0, a1, b0, b1), nrm) in defs.items():
            if faces != "all" and face not in faces:
                continue
            pz = passo if face == "topo" else passo * 0.8
            A, B = np.meshgrid(np.arange(a0, a1, passo), np.arange(b0, b1, pz), indexing="ij")
            if not A.size:
                continue
            X, Y, Z = f(A, B)
            c = cor if tex is None else tex(A, B, face)
            self.add(np.stack([X, Y, Z], -1), c, nrm, brilho)

    def revolucao(self, cx, cy, perfil, z0, z1, cor, passo=0.003, brilho=0.0, cor_f=None):
        """Superfície de revolução: raio = perfil(z)."""
        zz = np.arange(z0, z1, passo * 0.7)
        rmax = max(perfil(zz).max(), 0.01)
        th = np.arange(0, 2 * math.pi, passo / rmax)
        T, Z = np.meshgrid(th, zz, indexing="ij")
        R = perfil(Z)
        dR = (perfil(Z + 0.002) - perfil(Z - 0.002)) / 0.004
        pts = np.stack([cx + R * np.cos(T), cy + R * np.sin(T), Z], -1)
        nor = np.stack([np.cos(T), np.sin(T), -dR], -1)
        c = cor if cor_f is None else cor_f(T, Z)
        self.add(pts, c, nor, brilho)

    def disco(self, cx, cy, r, altura_f, cor, passo=0.003, brilho=0.0, cor_f=None):
        """Tampa: z = altura_f(rho, theta)."""
        rr = np.arange(0, r, passo)
        R, T = np.meshgrid(rr, np.arange(0, 2 * math.pi, passo / max(r, 0.01)), indexing="ij")
        Z = altura_f(R, T)
        dzr = (altura_f(R + 0.002, T) - altura_f(np.maximum(R - 0.002, 0), T)) / 0.004
        dzt = (altura_f(R, T + 0.02) - altura_f(R, T - 0.02)) / 0.04 / np.maximum(R, 0.01)
        nx = -dzr * np.cos(T) + dzt * np.sin(T)
        ny = -dzr * np.sin(T) - dzt * np.cos(T)
        pts = np.stack([cx + R * np.cos(T), cy + R * np.sin(T), Z], -1)
        c = cor if cor_f is None else cor_f(R, T)
        self.add(pts, c, np.stack([nx, ny, np.ones_like(nx)], -1), brilho)

    def haste(self, a, b, r, cor, brilho=0.0, nervura=0.0, cor_f=None):
        a, b = np.asarray(a, float), np.asarray(b, float)
        d = b - a
        L = np.linalg.norm(d * np.array([1, 1, 0.5]))
        n = max(2, int(L / 0.0025))
        t = np.linspace(0, 1, n)
        k = max(8, int(2 * math.pi * r / 0.002))
        th = np.linspace(0, 2 * math.pi, k, endpoint=False)
        T, A = np.meshgrid(t, th, indexing="ij")
        dn = d / (np.linalg.norm(d) or 1)
        e1 = np.cross(dn, [0, 0, 1.0]) if abs(dn[2]) < 0.95 else np.cross(dn, [1.0, 0, 0])
        e1 = e1 / np.linalg.norm(e1)
        e2 = np.cross(dn, e1)
        rr = r * (1 + nervura * (np.sin(T * np.linalg.norm(d) * 160) > 0.3))
        nor = np.cos(A)[..., None] * e1 + np.sin(A)[..., None] * e2
        pts = a + T[..., None] * d + rr[..., None] * nor
        c = cor if cor_f is None else cor_f(T, A)
        self.add(pts, c, nor, brilho)

    def curva(self, pontos, r, cor, brilho=0.0):
        for a, b in zip(pontos, pontos[1:]):
            self.haste(a, b, r, cor, brilho)

    def pano(self, x0, y0, x1, y1, z1, alt, mascara, cor_f, ondas=6.0):
        """Roupa pendurada: plano vertical entre (x0,y0) e (x1,y1), com dobras."""
        u, v = np.meshgrid(np.linspace(0, 1, 90), np.linspace(0, 1, 110), indexing="ij")
        dentro = mascara(u, v)
        u, v = u[dentro], v[dentro]
        dob = 0.012 * np.sin(u * ondas * 2 * math.pi + v * 1.5)
        nx, ny = -(y1 - y0), x1 - x0
        nn = math.hypot(nx, ny) or 1
        nx, ny = nx / nn, ny / nn
        px = x0 + (x1 - x0) * u + nx * dob
        py = y0 + (y1 - y0) * u + ny * dob
        pz = z1 - alt * v
        tang = np.array([x1 - x0, y1 - y0, 0]) / (nn or 1)
        incl = np.cos(u * ondas * 2 * math.pi + v * 1.5) * 0.6
        nor = np.stack([nx + tang[0] * incl, ny + tang[1] * incl, np.zeros_like(u)], -1)
        self.add(np.stack([px, py, pz], -1), cor_f(u, v), nor)

    # -- desenho
    def render(self, sombra=0.42) -> Image.Image:
        P = np.concatenate(self.p)
        C = np.concatenate(self.c)
        N = np.concatenate(self.n)
        B = np.concatenate(self.b)
        Nn = N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-6)
        dif = np.clip(Nn @ LUZ, 0, 1)
        H = (LUZ + OLHO) / np.linalg.norm(LUZ + OLHO)
        esp = np.clip(Nn @ H, 0, 1) ** 40 * B
        ao = 1 - 0.28 * np.exp(-P[:, 2] / 0.12) * (Nn[:, 2] < 0.7)          # escurece rente ao chão
        cor = np.clip(C * (0.5 + 0.62 * dif)[:, None] * ao[:, None] + 255 * esp[:, None], 0, 255)
        s = self.SS
        W, Hh = 128 * s, 256 * s

        def tela(X3):
            X = (63 + 63 * (X3[:, 0] - X3[:, 1])) * s
            Y = (192 + 32 * (X3[:, 0] + X3[:, 1]) - X3[:, 2] * PX_M) * s
            return X.astype(int), Y.astype(int)

        img = np.zeros((Hh, W, 4), dtype=float)
        # sombra projetada no chão (z = 0), suave
        if sombra:
            alto = P[:, 2] > 0.01
            Q = P[alto].copy()
            Q[:, 0] -= Q[:, 2] * LUZ[0] / LUZ[2] * 0.55
            Q[:, 1] -= Q[:, 2] * LUZ[1] / LUZ[2] * 0.55
            Q[:, 2] = 0
            sx, sy = tela(Q)
            ok = (sx >= 0) & (sx < W) & (sy >= 0) & (sy < Hh)
            m = np.zeros((Hh, W), dtype=np.uint8)
            m[sy[ok], sx[ok]] = 255
            mi = Image.fromarray(m).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(3 * s))
            img[..., 3] = np.array(mi, dtype=float) * sombra
        X, Y = tela(P)
        prof = P[:, 0] + P[:, 1] + P[:, 2] * 2 / 0.933
        ok = (X >= 0) & (X < W) & (Y >= 0) & (Y < Hh)
        X, Y, prof, cor = X[ok], Y[ok], prof[ok], cor[ok]
        ordem = np.argsort(prof, kind="stable")
        obj = np.zeros((Hh, W, 4), dtype=float)
        obj[Y[ordem], X[ordem], :3] = cor[ordem]
        obj[Y[ordem], X[ordem], 3] = 255
        o = Image.fromarray(obj.astype(np.uint8), "RGBA")
        a = np.array(o)
        cheio = np.array(o.filter(ImageFilter.MaxFilter(3)))
        buraco = (a[..., 3] == 0) & (cheio[..., 3] > 0)
        a[buraco] = cheio[buraco]
        som = Image.fromarray(img.astype(np.uint8), "RGBA")
        som.alpha_composite(Image.fromarray(a, "RGBA"))
        return som.resize((128, 256), Image.LANCZOS)


# ---------------------------------------------------------------- texturas para objetos
_TIJ = {}


def tijolo_tex(u, v, face):
    """Tijolo baiano (mesma textura das paredes) numa face da caixa."""
    if not _TIJ:
        _TIJ.update(tf.parede_iluminada("tijolo_baiano"))
    if face == "topo":
        return np.broadcast_to(np.array([150, 146, 138.0]), np.shape(u) + (3,)) * (
            0.9 + 0.2 * tf.vn(u % 1, v % 1, 40, 40, 3))[..., None]
    t = _TIJ["W" if face in ("x0", "y1") else "N"]
    return tf.amostrar_parede(t, u, (v * PX_M) % 192)


def concreto_tex(seed, base=(156, 154, 148)):
    def f(u, v, face):
        n = tf.fbm(u % 1, (v / 3) % 1, 8, 8, 4, seed)
        tab = np.abs(((v * 6 if face != "topo" else u * 6) % 1) - 0.5) > 0.47   # marca de forma
        c = np.array(base, float) * (0.86 + 0.25 * n)[..., None]
        poro, _ = tf.pontos(u % 1, (v / 3) % 1, 90, 90, 0.5, 0.4, seed + 1)
        c = c * (1 - 0.3 * poro)[..., None]
        return np.where(tab[..., None], c * 0.9, c)
    return f


AZUL = np.array([34, 88, 166.0])


def caixa_dagua(r, h, seed=0):
    c = Cena()
    cx = cy = 0.52
    # base: tablado de concreto
    c.caixa(cx - r * 0.95, cy - r * 0.95, 0.0, cx + r * 0.95, cy + r * 0.95, 0.05, None, concreto_tex(seed + 1))

    def perfil(z):
        zr = (z - 0.05) / h
        base_r = r * (0.9 + 0.1 * zr)
        friso = sum(0.012 * np.exp(-((zr - f) / 0.02) ** 2) for f in (0.22, 0.45, 0.68))
        return base_r - friso

    def cor_corpo(T, Z):
        zr = (Z - 0.05) / h
        poeira = 0.08 * tf.vn((T / (2 * math.pi)) % 1, zr % 1, 12, 6, seed)
        return AZUL * (0.94 + 0.12 * tf.vn((T / (2 * math.pi)) % 1, zr % 1, 30, 10, seed + 2))[..., None] + 120 * poeira[..., None]
    c.revolucao(cx, cy, perfil, 0.05, 0.05 + h, AZUL, brilho=0.35, cor_f=cor_corpo)
    # aba da tampa
    rt = r * 1.0 + 0.02
    c.revolucao(cx, cy, lambda z: np.full_like(z, rt), 0.05 + h - 0.035, 0.05 + h + 0.01, AZUL * 0.9, brilho=0.4)
    # tampa abaulada com nervuras radiais e tampinha central
    topo = 0.05 + h + 0.01

    def alt_tampa(R, T):
        return topo + 0.07 * (1 - (R / rt) ** 2) + 0.006 * (np.cos(T * 16) > 0.85) * (R > rt * 0.3)
    c.disco(cx, cy, rt, alt_tampa, AZUL * 1.05, brilho=0.4,
            cor_f=lambda R, T: AZUL * (1.03 + 0.05 * tf.vn((T / (2 * math.pi)) % 1, R % 1, 16, 4, seed + 3))[..., None] + 18)
    c.revolucao(cx, cy, lambda z: np.full_like(z, rt * 0.22), topo + 0.06, topo + 0.1, AZUL * 1.1, brilho=0.5)
    c.disco(cx, cy, rt * 0.22, lambda R, T: np.full_like(R, topo + 0.1), AZUL * 1.15, brilho=0.5)
    # saída de água (PVC marrom) com registro, descendo para a laje
    marrom = np.array([150, 92, 52.0])
    ax = cx + perfil(np.array([0.15]))[0]
    c.curva([(ax - 0.01, cy + 0.08, 0.15), (ax + 0.16, cy + 0.08, 0.15), (ax + 0.16, cy + 0.08, 0.02)], 0.018, marrom, 0.3)
    c.caixa(ax + 0.05, cy + 0.055, 0.12, ax + 0.1, cy + 0.105, 0.18, np.array([170, 150, 90.0]), brilho=0.5)
    c.haste((ax + 0.075, cy + 0.08, 0.18), (ax + 0.075, cy + 0.08, 0.215), 0.006, np.array([150, 150, 150.0]), 0.6)
    c.disco(ax + 0.075, cy + 0.08, 0.022, lambda R, T: np.full_like(R, 0.215), np.array([190, 40, 36.0]), brilho=0.5)
    # ladrão (PVC branco) perto do alto
    branco = np.array([214, 212, 204.0])
    zl = 0.05 + h * 0.85
    by = cy - perfil(np.array([zl]))[0]
    c.curva([(cx - 0.06, by + 0.01, zl), (cx - 0.06, by - 0.14, zl), (cx - 0.06, by - 0.14, 0.02)], 0.014, branco, 0.4)
    return c.render()


def caixa_amianto(seed=5):
    c = Cena()
    cinza = np.array([150, 150, 144.0])

    def tex(u, v, face):
        n = tf.fbm(u % 1, (v / 2) % 1, 6, 6, 4, seed)
        cor = cinza * (0.85 + 0.25 * n)[..., None]
        escorre = tf.vn(u % 1, (v / 4) % 1, 30, 1, seed + 1) ** 3 * (face != "topo")
        cor = cor * (1 - 0.35 * escorre)[..., None]
        musgo = (v < 0.18) * (tf.vn(u % 1, v % 1, 20, 6, seed + 2) > 0.45) * (face != "topo")
        return tf.mistura(cor, np.array([74, 96, 58.0]), musgo * 0.65)
    c.caixa(0.14, 0.14, 0.0, 0.84, 0.84, 0.05, None, concreto_tex(seed + 3))
    c.caixa(0.2, 0.2, 0.05, 0.8, 0.8, 0.78, None, tex)
    c.caixa(0.17, 0.17, 0.74, 0.83, 0.83, 0.8, None, tex)                 # borda
    # tampa em duas placas, uma quebrada no canto
    c.caixa(0.19, 0.19, 0.8, 0.5, 0.81, 0.83, cinza * 0.95)
    c.caixa(0.51, 0.19, 0.8, 0.81, 0.62, 0.83, cinza * 0.92)
    c.caixa(0.51, 0.62, 0.8, 0.66, 0.81, 0.83, cinza * 0.9)
    c.curva([(0.2, 0.55, 0.12), (0.0, 0.55, 0.12), (0.0, 0.55, 0.02)], 0.016, np.array([120, 118, 112.0]), 0.2)
    return c.render()


def churrasqueira(lado, seed=7):
    """Churrasqueira de alvenaria com bancada de concreto, boca com grelha e
    carvão, fuligem, coifa, chaminé e chapéu. Boca para o sul (S) ou leste (E)."""
    c = Cena()
    S = lado == "S"

    def tr(x0, y0, x1, y1):
        return (x0, y0, x1, y1) if S else (y0, x0, y1, x1)

    def fuligem_tex(base):
        def f(u, v, face):
            cor = base(u, v, face)
            frente = face == ("y1" if S else "x1")
            fum = frente * np.clip((v - 0.6) / 0.8, 0, 1) * (0.55 + 0.45 * tf.vn(u % 1, (v / 2) % 1, 8, 4, seed))
            return cor * (1 - 0.6 * fum)[..., None]
        return f
    tex = fuligem_tex(tijolo_tex)
    c.caixa(*tr(0.12, 0.28, 0.88, 0.82)[:2], 0.0, *tr(0.12, 0.28, 0.88, 0.82)[2:], 0.82, None, tex)
    # bancada de concreto (com sobra na frente)
    c.caixa(*tr(0.08, 0.24, 0.92, 0.88)[:2], 0.82, *tr(0.08, 0.24, 0.92, 0.88)[2:], 0.87, None, concreto_tex(seed + 1))
    # boca: recuo escuro, carvão e grelha
    bx0, bx1, bz0, bz1 = 0.24, 0.76, 0.42, 0.74
    if S:
        c.caixa(bx0, 0.818, bz0, bx1, 0.822, bz1, np.array([26, 22, 20.0]))
        carvao = np.array([40, 38, 36.0])
        c.caixa(bx0 + 0.02, 0.6, bz0, bx1 - 0.02, 0.83, bz0 + 0.035, carvao, faces=("topo",))
        for k in range(9):
            x = bx0 + 0.03 + k * (bx1 - bx0 - 0.06) / 8
            c.haste((x, 0.6, bz0 + 0.12), (x, 0.84, bz0 + 0.12), 0.004, np.array([110, 110, 112.0]), 0.6)
    else:
        c.caixa(0.818, bx0, bz0, 0.822, bx1, bz1, np.array([26, 22, 20.0]))
        carvao = np.array([40, 38, 36.0])
        c.caixa(0.6, bx0 + 0.02, bz0, 0.83, bx1 - 0.02, bz0 + 0.035, carvao, faces=("topo",))
        for k in range(9):
            y = bx0 + 0.03 + k * (bx1 - bx0 - 0.06) / 8
            c.haste((0.6, y, bz0 + 0.12), (0.84, y, bz0 + 0.12), 0.004, np.array([110, 110, 112.0]), 0.6)
    # coifa (afunila) e chaminé
    c.caixa(*tr(0.22, 0.34, 0.78, 0.74)[:2], 0.87, *tr(0.22, 0.34, 0.78, 0.74)[2:], 1.12, None, tex)
    c.caixa(*tr(0.32, 0.42, 0.68, 0.68)[:2], 1.12, *tr(0.32, 0.42, 0.68, 0.68)[2:], 1.32, None, tex)
    c.caixa(*tr(0.41, 0.47, 0.59, 0.63)[:2], 1.32, *tr(0.41, 0.47, 0.59, 0.63)[2:], 1.95, None, tex)
    # chapéu da chaminé: placa de concreto sobre 4 tijolinhos, topo escurecido
    for dx, dy in ((0.41, 0.47), (0.56, 0.47), (0.41, 0.6), (0.56, 0.6)):
        q = tr(dx, dy, dx + 0.03, dy + 0.03)
        c.caixa(q[0], q[1], 1.95, q[2], q[3], 2.02, np.array([90, 70, 60.0]))
    q = tr(0.37, 0.43, 0.63, 0.67)
    c.caixa(q[0], q[1], 2.02, q[2], q[3], 2.05, np.array([92, 90, 86.0]))
    return c.render()


FERRO = np.array([104, 62, 42.0])


def ferro_cor(seed):
    def f(T, A):
        n = tf.vn(T % 1, (A / (2 * math.pi)) % 1, 18, 6, seed)
        cor = FERRO * (0.75 + 0.45 * n)[..., None]
        laranja = (n > 0.72)
        return np.where(laranja[..., None], np.array([156, 86, 44.0]), cor)
    return f


def pilar_ferro(seed=11):
    c = Cena()
    c.caixa(0.0, 0.0, 0.0, 0.18, 0.18, 0.38, None, concreto_tex(seed))
    # lascado no canto de cima
    c.caixa(0.13, 0.13, 0.33, 0.18, 0.18, 0.38, np.array([128, 126, 120.0]), faces=("topo", "x1", "y1"))
    bar = [(0.045, 0.045), (0.135, 0.045), (0.045, 0.135), (0.135, 0.135)]
    for k, (x, y) in enumerate(bar):
        c.haste((x, y, 0.38), (x + (x - 0.09) * 0.25, y + (y - 0.09) * 0.25, 1.3 - 0.05 * k), 0.007,
                FERRO, 0.15, nervura=0.25, cor_f=ferro_cor(seed + k))
    for z in (0.62, 0.95):                       # estribos amarrados
        q = [(0.035, 0.035, z), (0.145, 0.035, z), (0.145, 0.145, z), (0.035, 0.145, z), (0.035, 0.035, z)]
        c.curva(q, 0.003, FERRO * 0.9)
        c.haste((0.145, 0.035, z), (0.16, 0.025, z - 0.03), 0.0025, np.array([90, 88, 86.0]))   # arame
    return c.render()


def ferro_solto(seed=13):
    c = Cena()
    # pedaço de laje quebrado com os ferros saindo
    c.caixa(0.02, 0.02, 0.0, 0.26, 0.2, 0.08, None, concreto_tex(seed))
    c.caixa(0.05, 0.18, 0.0, 0.2, 0.28, 0.05, None, concreto_tex(seed + 1))
    rnd = np.random.default_rng(seed)
    for k in range(6):
        x, y = 0.05 + 0.035 * k, 0.07 + 0.06 * (k % 2)
        h = 0.8 + 0.4 * rnd.random()
        dobra = rnd.choice([0, 1])
        topo = (x + 0.02, y + 0.01, h)
        c.haste((x, y, 0.06), topo, 0.007, FERRO, 0.15, nervura=0.25, cor_f=ferro_cor(seed + k))
        if dobra:
            c.haste(topo, (topo[0] + 0.12, topo[1] + 0.05, topo[2] - 0.08), 0.007, FERRO, 0.15,
                    nervura=0.25, cor_f=ferro_cor(seed + k + 10))
    return c.render()


def antena(lado="W", seed=17):
    """Antena parabólica com o prato apontando para `lado` (W, N, E, S)."""
    c = Cena()
    d = {"W": (-1.0, 0.0), "N": (0.0, -1.0), "E": (1.0, 0.0), "S": (0.0, 1.0)}[lado]
    cinza = np.array([150, 152, 156.0])
    # base: bloco de concreto, mastro com braçadeira
    c.caixa(0.4, 0.4, 0.0, 0.62, 0.62, 0.14, None, concreto_tex(seed))
    c.haste((0.51, 0.51, 0.14), (0.51, 0.51, 0.95), 0.018, cinza * 0.8, 0.4)
    c.caixa(0.48, 0.48, 0.86, 0.54, 0.54, 0.93, cinza * 0.7, brilho=0.4)
    # prato (paraboloide), virado para o lado pedido e inclinado 35° para cima
    el = math.radians(35)
    nrm = np.array([d[0] * math.cos(el), d[1] * math.cos(el), math.sin(el)])
    e1 = np.array([-d[1], d[0], 0.0])
    e2 = np.cross(nrm, e1)
    if e2[2] < 0:
        e2 = -e2
    centro = np.array([0.5, 0.5, 1.02])
    r = 0.3
    us, vs = np.meshgrid(np.linspace(-1, 1, 220), np.linspace(-1, 1, 220), indexing="ij")
    dentro = us ** 2 + vs ** 2 <= 1
    us, vs = us[dentro], vs[dentro]
    prof = 0.07 * (us ** 2 + vs ** 2)
    pts = centro + r * (us[:, None] * e1 + vs[:, None] * e2) + prof[:, None] * nrm
    nor = nrm - 2 * 0.07 / r * (us[:, None] * e1 + vs[:, None] * e2)
    ang = np.arctan2(vs, us)
    nerv = np.cos(ang * 12) > 0.96
    ferrugem = (tf.vn((ang / (2 * math.pi)) % 1, np.hypot(us, vs) % 1, 40, 12, seed) > 0.8) & (vs < 0.2)
    cor = np.where(nerv[:, None], np.array([176, 178, 180.0]), np.array([206, 206, 202.0]))
    cor = np.where(ferrugem[:, None], np.array([168, 140, 118.0]), cor)
    cor = cor * (0.95 + 0.08 * tf.vn((ang / (2 * math.pi)) % 1, np.hypot(us, vs) % 1, 20, 6, seed + 1))[:, None]
    c.add(pts, cor, nor, 0.3)
    # costas do prato (aparecem quando ele aponta para longe de quem olha)
    c.add(pts - 0.006 * nrm, cor * 0.82, -nor, 0.2)
    # aro
    th = np.linspace(0, 2 * math.pi, 120)
    aro = [tuple(centro + r * (math.cos(t) * e1 + math.sin(t) * e2) + 0.07 * nrm) for t in th]
    c.curva(aro, 0.006, np.array([170, 170, 168.0]), 0.4)
    # braço e LNB
    base_b = centro - r * 0.95 * e2 + 0.07 * nrm
    foco = centro + 0.32 * nrm - 0.05 * e2
    c.haste(tuple(base_b), tuple(foco), 0.008, cinza * 0.85, 0.4)
    c.haste(tuple(foco), tuple(foco + 0.07 * (-nrm)), 0.022, np.array([60, 60, 64.0]), 0.5)
    c.caixa(foco[0] - 0.02, foco[1] - 0.02, foco[2] - 0.02, foco[0] + 0.02, foco[1] + 0.02, foco[2] + 0.03,
            np.array([70, 70, 74.0]), brilho=0.4)
    # cabo preto descendo pelo mastro até a laje
    cabo = [tuple(foco), (0.53, 0.53, 0.9), (0.53, 0.53, 0.2), (0.6, 0.62, 0.06),
            (0.51 - d[1] * 0.2 + 0.1, 0.51 + d[0] * 0.2 + 0.1, 0.0)]
    c.curva(cabo, 0.005, np.array([28, 28, 30.0]), 0.3)
    return c.render()


def _camiseta(u, v):
    corpo = (u > 0.2) & (u < 0.8)
    manga = (v < 0.32) & ((u <= 0.2) | (u >= 0.8))
    gola = (v < 0.06) & (np.abs(u - 0.5) < 0.12)
    return (corpo | manga) & ~gola


def _calca(u, v):
    cintura = v < 0.2
    pernas = (np.abs(u - 0.5) > 0.05)
    return cintura | pernas


def _toalha(u, v):
    return np.ones_like(u, dtype=bool)


def _bermuda(u, v):
    return (v < 0.25) | (np.abs(u - 0.5) > 0.06)


ROUPAS = [
    (_camiseta, lambda u, v: np.broadcast_to(np.array([190, 50, 46.0]), u.shape + (3,)), 0.42),
    (_toalha, lambda u, v: np.where((np.abs(((v * 6) % 1) - 0.5) < 0.18)[..., None], np.array([236, 196, 56.0]), np.array([48, 120, 180.0])), 0.5),
    (_calca, lambda u, v: np.array([58, 82, 128.0]) * (0.9 + 0.15 * (np.abs(u - 0.5) > 0.3))[..., None], 0.55),
    (_camiseta, lambda u, v: np.broadcast_to(np.array([232, 230, 222.0]), u.shape + (3,)), 0.4),
    (_bermuda, lambda u, v: np.broadcast_to(np.array([66, 132, 82.0]), u.shape + (3,)), 0.3),
]


def varal(lado, seed=19):
    c = Cena()
    a, b = ((0.04, 0.5), (0.96, 0.5)) if lado == "x" else ((0.5, 0.04), (0.5, 0.96))
    cano = np.array([160, 162, 164.0])
    for (x, y) in (a, b):
        c.caixa(x - 0.04, y - 0.04, 0.0, x + 0.04, y + 0.04, 0.06, None, concreto_tex(seed))
        c.haste((x, y, 0.06), (x, y, 1.72), 0.012, cano, 0.4)
    # dois fios com barriga
    for off in (-0.025, 0.025):
        pts = []
        for t in np.linspace(0, 1, 30):
            x = a[0] + (b[0] - a[0]) * t + (off if lado == "y" else 0)
            y = a[1] + (b[1] - a[1]) * t + (off if lado == "x" else 0)
            pts.append((x, y, 1.66 - 0.06 * math.sin(math.pi * t)))
        c.curva(pts, 0.0025, np.array([206, 206, 200.0]))
    pos = 0.1
    for k, (masc, corf, alt) in enumerate(ROUPAS):
        larg = 0.16 if masc is not _toalha else 0.18
        t0, t1 = pos, pos + larg
        pos = t1 + 0.012
        x0, y0 = a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0
        x1, y1 = a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1
        zt = 1.66 - 0.06 * math.sin(math.pi * (t0 + t1) / 2)
        c.pano(x0, y0, x1, y1, zt, alt, masc, corf)
        for t in (t0 + 0.02, t1 - 0.02):          # pregadores
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            cp = np.array([[220, 60, 60], [60, 160, 220], [240, 200, 40]][k % 3], float)
            c.caixa(px - 0.006, py - 0.006, zt - 0.02, px + 0.006, py + 0.006, zt + 0.015, cp, brilho=0.4)
    return c.render()


def pilha_tijolos(seed=23):
    c = Cena()
    c.caixa(0.15, 0.2, 0.0, 0.85, 0.8, 0.04, np.array([118, 92, 66.0]))       # palete/tábua
    rnd = np.random.default_rng(seed)
    pal = [np.array(p, float) for p in ([192, 110, 68], [184, 100, 60], [202, 122, 78], [170, 90, 56])]
    z = 0.04
    for camada in range(5):
        for i in range(3):
            for j in range(4 if camada % 2 == 0 else 3):
                if camada == 4 and rnd.random() < 0.4:
                    continue
                if camada % 2 == 0:
                    x0, y0, x1, y1 = 0.17 + i * 0.22, 0.22 + j * 0.14, 0.17 + i * 0.22 + 0.2, 0.22 + j * 0.14 + 0.13
                else:
                    x0, y0, x1, y1 = 0.17 + j * 0.22, 0.22 + i * 0.18, 0.17 + j * 0.22 + 0.2, 0.22 + i * 0.18 + 0.17
                cor = pal[rnd.integers(len(pal))] * (0.9 + 0.2 * rnd.random())
                furo = cor * 0.45

                def tex(u, v, face, cor=cor, furo=furo):
                    if face in ("x0", "x1"):
                        # ponta do tijolo baiano: furos
                        fu, fv = (u * 30) % 1, (v * 22) % 1
                        f = (np.abs(fu - 0.5) < 0.28) & (np.abs(fv - 0.5) < 0.3)
                        return np.where(f[..., None], furo, cor)
                    return np.broadcast_to(cor, np.shape(u) + (3,)) * (0.92 + 0.12 * tf.vn(u % 1, v % 1, 30, 30, 5))[..., None]
                c.caixa(x0, y0, z, x1 - 0.004, y1 - 0.004, z + 0.09, None, tex, passo=0.0025)
        z += 0.09
    return c.render()


SOLIDO = [["BlocksPlacement", ""], ["solid", ""]]
OBJETOS = [
    ("caixa_dagua_1000", "caixa d'água azul de 1000 L, com canos e registro", lambda: caixa_dagua(0.42, 0.82, 1), SOLIDO),
    ("caixa_dagua_500", "caixa d'água azul de 500 L", lambda: caixa_dagua(0.33, 0.66, 2), SOLIDO),
    ("caixa_dagua_amianto", "caixa d'água velha de amianto", caixa_amianto, SOLIDO),
    ("churrasqueira_s", "churrasqueira de tijolo, boca para o sul", lambda: churrasqueira("S"), SOLIDO),
    ("churrasqueira_e", "churrasqueira de tijolo, boca para o leste", lambda: churrasqueira("E"), SOLIDO),
    ("pilar_ferro_espera", "pilar com ferro de espera (canto do tile)", pilar_ferro, [["BlocksPlacement", ""], ["solidtrans", ""]]),
    ("ferro_espera", "ferro de espera saindo da laje quebrada", ferro_solto, []),
    ("antena_parabolica_w", "antena parabólica, prato para o oeste", lambda: antena("W"), [["BlocksPlacement", ""]]),
    ("antena_parabolica_n", "antena parabólica, prato para o norte", lambda: antena("N"), [["BlocksPlacement", ""]]),
    ("antena_parabolica_e", "antena parabólica, prato para o leste", lambda: antena("E"), [["BlocksPlacement", ""]]),
    ("antena_parabolica_s", "antena parabólica, prato para o sul", lambda: antena("S"), [["BlocksPlacement", ""]]),
    ("varal_x", "varal com roupa (leste-oeste)", lambda: varal("x"), []),
    ("varal_y", "varal com roupa (norte-sul)", lambda: varal("y"), []),
    ("pilha_tijolos", "pilha de tijolos baianos (obra)", pilha_tijolos, SOLIDO),
]


def objetos(saida: Path) -> dict:
    nome = "rsb_objetos_laje_01"
    linhas = (len(OBJETOS) + 7) // 8
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = []
    for n, (chave, desc, f, props) in enumerate(OBJETOS):
        folha.alpha_composite(f(), ((n % 8) * 128, (n // 8) * 256))
        pecas.append({"peca": f"{nome}_{n}", "nome": chave, "descricao": desc, "props": props})
    pecas += [{"peca": f"{nome}_{n}", "props": []} for n in range(len(OBJETOS), linhas * 8)]
    i = {chave: n for n, (chave, *_r) in enumerate(OBJETOS)}
    um = lambda k: [{"orient": "W", "tiles": {"0,0": i[k]}}]
    moveis = [
        {"grupo": "Kit Brasil - Laje: caixas d'água", "itens": [um("caixa_dagua_1000"), um("caixa_dagua_500"), um("caixa_dagua_amianto")]},
        {"grupo": "Kit Brasil - Laje: churrasco", "itens": [[{"orient": "S", "tiles": {"0,0": i["churrasqueira_s"]}},
                                                              {"orient": "E", "tiles": {"0,0": i["churrasqueira_e"]}}]]},
        {"grupo": "Kit Brasil - Laje: antena e varal", "itens": [
            [{"orient": o, "tiles": {"0,0": i[f"antena_parabolica_{o.lower()}"]}} for o in "WNES"],
            [{"orient": "W", "tiles": {"0,0": i["varal_y"]}}, {"orient": "N", "tiles": {"0,0": i["varal_x"]}}]]},
        {"grupo": "Kit Brasil - Laje: obra", "itens": [um("pilar_ferro_espera"), um("ferro_espera"), um("pilha_tijolos")]},
    ]
    return kf._gravar(folha, nome, "objeto", pecas, saida, {}, moveis=moveis)


if __name__ == "__main__":
    tiles2x, tdefs, saida = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    defs = {d["nome"]: d for d in kit_tiles.ler_definicoes(tdefs)}
    import json
    print(json.dumps([lajes(tiles2x, saida), muretas(tiles2x, defs, saida), objetos(saida)], ensure_ascii=False))
