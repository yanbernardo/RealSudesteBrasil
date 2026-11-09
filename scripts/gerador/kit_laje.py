"""Kit Brasil, morro e favela: a laje (telhado plano de concreto) e o que tem nela.

Favela brasileira não tem telha inclinada: o teto é laje de concreto, com mureta
em volta, caixa d'água, ferro de espera para o próximo andar, churrasqueira,
varal e antena (pedido do usuário, 08/11/2026). Folhas em `kits/tiles/`:

- `rsb_lajes_01` (piso): laje crua, com manta asfáltica, com remendo de
  alumínio, com ralo, terraço de cerâmica vermelha e bege. No BuildingEd: na
  lista de pisos e de telhado plano ("Roof Tops").
- `rsb_muretas_favela_01` (parede): mureta de laje de meia altura, mureta baixa
  e parede inacabada em degraus, em 4 acabamentos; molde: as muretas do jogo
  (`walls_exterior_house_low_01`), mesma forma, sombra e propriedades (pulável).
- `rsb_objetos_laje_01` (objeto): desenhados por um renderizador 3D simples no
  ângulo do jogo: caixa d'água azul (1000 e 500 L), caixa d'água velha de
  amianto, churrasqueira de tijolo (2 lados), pilar com ferro de espera, ferro
  de espera solto, antena parabólica, varal (2 lados).

Uso: python -I -X utf8 kit_laje.py <pasta Tiles/2x> <newtiledefinitions.tiles> <kits/tiles>
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit_favela as kf  # noqa: E402
import kit_tiles  # noqa: E402
import pisos_brasil as pb  # noqa: E402

PX_M = kf.PX_M


# ---------------------------------------------------------------- lajes
def manta(s, t, seed, remendo=False):
    n = kf.fbm(s, t, seed)
    cor = np.array([48, 48, 50.0]) * (0.85 + 0.3 * n)[..., None]
    emenda = np.abs((s * 2) % 1 - 0.5) > 0.48                    # rolos de manta a cada meio tile
    cor = np.where(emenda[..., None], cor * 0.75, cor)
    if remendo:
        r = kf.fbm(s, t, seed + 9) > 0.6
        cor = np.where(r[..., None], np.array([178, 180, 182.0]) * (0.9 + 0.2 * n)[..., None], cor)
    return cor + kf.grao(s, t, 5, seed)[..., None]


def ralo(s, t):
    cor = kf.laje(s, t, 31)
    d = np.hypot(s - 0.5, t - 0.5)
    grade = (d < 0.09) & ((np.floor(s * 60) % 2) == 0)
    aro = (d < 0.11) & (d > 0.09)
    cor = np.where(aro[..., None], cor * 0.7, cor)
    return np.where(grade[..., None], np.array([40, 40, 40.0]), cor)


LAJES = [
    ("laje_crua_a", "laje de concreto crua", lambda s, t: kf.laje(s, t, 41)),
    ("laje_crua_b", "laje de concreto crua com mancha de água", lambda s, t: kf.laje(s, t, 42, True)),
    ("laje_manta", "laje com manta asfáltica preta", lambda s, t: manta(s, t, 43)),
    ("laje_manta_remendo", "laje com manta e remendo de alumínio", lambda s, t: manta(s, t, 44, True)),
    ("laje_ralo", "laje com ralo", ralo),
    ("terraco_ceramica_vermelha", "terraço de cerâmica vermelha", lambda s, t: pb.blocos(s, t, 3, 3, [(150, 64, 48), (142, 60, 46), (158, 70, 52)], 0.04, False, 45, (176, 170, 156))),
    ("terraco_ceramica_bege", "terraço de cerâmica bege", lambda s, t: pb.blocos(s, t, 3, 3, [(206, 192, 164), (198, 184, 158)], 0.04, False, 46, (166, 160, 146))),
]


def lajes(tiles2x: Path, saida: Path) -> dict:
    nome = "rsb_lajes_01"
    folha = Image.new("RGBA", (1024, 256), (0, 0, 0, 0))
    pecas = []
    for n, (chave, desc, f) in enumerate(LAJES):
        folha.alpha_composite(pb.peca(f, tiles2x), ((n % 8) * 128, 0))
        pecas.append({"peca": f"{nome}_{n}", "nome": chave, "descricao": desc,
                      "props": [["diamondFloor", ""], ["exterior", ""], ["solidfloor", ""]]})
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
    # cada acabamento ocupa 4 colunas x 3 linhas; dois por faixa de 3 linhas
    linhas = ((len(ACABAMENTOS) + 1) // 2) * 3
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{nome}_{i}", "props": []} for i in range(linhas * 8)]
    for k, (chave, desc, material, tex) in enumerate(ACABAMENTOS):
        base = (k // 2) * 24 + (k % 2) * 4
        novo_de = {}
        for j, (velho, face) in enumerate(PECAS_MURETA):
            novo_de[velho] = base + (j // 4) * 8 + j % 4
        for velho, face in PECAS_MURETA:
            cel = kf._celula(molde, velho)
            if not (cel[..., 3] > 0).any():
                continue
            cor, L, alfa = kf.peca_parede(cel, face, tex)
            rgb = np.clip(cor * np.clip(L / Lref, 0.35, 1.7)[..., None], 0, 255)
            img = np.zeros((256, 128, 4), dtype=np.uint8)
            img[..., :3] = rgb.astype(np.uint8)
            img[..., 3] = alfa.astype(np.uint8)
            i = novo_de[velho]
            folha.alpha_composite(Image.fromarray(img, "RGBA"), ((i % 8) * 128, (i // 8) * 256))
            props = []
            for p, v in sd["pecas"][velho]:
                if v.startswith(MOLDE_MURETA):
                    v = f"{nome}_{novo_de[int(v.rsplit('_', 1)[1])]}"
                props.append([p, v])
            if any(p == "wall" for p, _v in props):
                props.append(["MaterialType", material])
            altura = {0: "meia altura", 1: "baixa", 2: "inacabada em degraus"}[PECAS_MURETA.index((velho, face)) // 4]
            pecas[i] = {"peca": f"{nome}_{i}", "nome": f"mureta {altura} {chave} {face}", "descricao": desc, "props": props}
    return kf._gravar(folha, nome, "parede", pecas, saida, {})


# ---------------------------------------------------------------- renderizador 3D
class Cena:
    """Pontos 3D (x, y em tiles dentro do tile; z em metros) com cor e normal,
    desenhados no ângulo do jogo com z-buffer, em 2x e reduzidos (antisserrilhado)."""
    SS = 3

    def __init__(self):
        self.p, self.c, self.n = [], [], []

    def add(self, pts, cor, nor):
        self.p.append(pts.reshape(-1, 3))
        self.c.append(np.broadcast_to(np.asarray(cor, dtype=float), pts.shape).reshape(-1, 3))
        self.n.append(np.broadcast_to(np.asarray(nor, dtype=float), pts.shape).reshape(-1, 3))

    def caixa(self, x0, y0, z0, x1, y1, z1, cor, tex=None, passo=0.004):
        cor_f = (lambda u, v, face: np.broadcast_to(np.asarray(cor, float), u.shape + (3,))) if tex is None else tex
        us = np.arange(0, 1 + 1e-9, passo)
        for face, (a, b, nrm) in {
                "topo": ((x0, x1, y0, y1), None, (0, 0, 1)), "x1": (None, None, (1, 0, 0)),
                "y1": (None, None, (0, 1, 0)), "x0": (None, None, (-1, 0, 0)), "y0": (None, None, (0, -1, 0))}.items():
            if face == "topo":
                u, v = np.meshgrid(np.arange(x0, x1, passo), np.arange(y0, y1, passo), indexing="ij")
                pts = np.stack([u, v, np.full_like(u, z1)], -1)
                cu, cv = u, v
            elif face in ("x0", "x1"):
                X = x1 if face == "x1" else x0
                u, v = np.meshgrid(np.arange(y0, y1, passo), np.arange(z0, z1, passo * 1.0), indexing="ij")
                pts = np.stack([np.full_like(u, X), u, v], -1)
                cu, cv = u, v
            else:
                Y = y1 if face == "y1" else y0
                u, v = np.meshgrid(np.arange(x0, x1, passo), np.arange(z0, z1, passo * 1.0), indexing="ij")
                pts = np.stack([u, np.full_like(u, Y), v], -1)
                cu, cv = u, v
            if pts.size:
                self.add(pts, cor_f(cu, cv, face), nrm)

    def cilindro(self, cx, cy, r, z0, z1, cor, tampa=True, passo=0.004, cor_tampa=None):
        th = np.arange(0, 2 * math.pi, passo / max(r, 0.01))
        zz = np.arange(z0, z1, passo)
        T, Z = np.meshgrid(th, zz, indexing="ij")
        pts = np.stack([cx + r * np.cos(T), cy + r * np.sin(T), Z], -1)
        nor = np.stack([np.cos(T), np.sin(T), np.zeros_like(T)], -1)
        self.add(pts, cor, nor)
        if tampa:
            rr = np.arange(0, r, passo)
            R, T2 = np.meshgrid(rr, np.arange(0, 2 * math.pi, passo / max(r, 0.01)), indexing="ij")
            pts = np.stack([cx + R * np.cos(T2), cy + R * np.sin(T2), np.full_like(R, z1)], -1)
            self.add(pts, cor_tampa if cor_tampa is not None else cor, (0, 0, 1))

    def haste(self, x0, y0, z0, x1, y1, z1, r, cor):
        n = max(2, int(math.dist((x0, y0, z0 / 2), (x1, y1, z1 / 2)) / 0.003))
        t = np.linspace(0, 1, n)
        th = np.linspace(0, 2 * math.pi, 10, endpoint=False)
        T, A = np.meshgrid(t, th, indexing="ij")
        px = x0 + (x1 - x0) * T + r * np.cos(A)
        py = y0 + (y1 - y0) * T + r * np.sin(A)
        pz = z0 + (z1 - z0) * T
        nor = np.stack([np.cos(A), np.sin(A), np.zeros_like(A)], -1)
        self.add(np.stack([px, py, pz], -1), cor, nor)

    def pano(self, x0, y0, x1, y1, z1, alt, cor):
        """Pano pendurado (roupa no varal), plano vertical entre (x0,y0) e (x1,y1)."""
        u, v = np.meshgrid(np.linspace(0, 1, 60), np.linspace(0, 1, 80), indexing="ij")
        pts = np.stack([x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, z1 - alt * v], -1)
        nx, ny = -(y1 - y0), x1 - x0
        nn = math.hypot(nx, ny) or 1
        self.add(pts, cor, (nx / nn, ny / nn, 0))

    def render(self) -> Image.Image:
        P = np.concatenate(self.p)
        C = np.concatenate(self.c)
        N = np.concatenate(self.n)
        luz = np.array([-0.35, 0.45, 0.82])
        luz = luz / np.linalg.norm(luz)
        Nn = N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-6)
        sombra = 0.55 + 0.5 * np.clip(Nn @ luz, 0, 1)
        cor = np.clip(C * sombra[:, None], 0, 255)
        s = self.SS
        X = (63 + 63 * (P[:, 0] - P[:, 1])) * s
        Y = (192 + 32 * (P[:, 0] + P[:, 1]) - P[:, 2] * PX_M) * s
        prof = P[:, 0] + P[:, 1] + P[:, 2] * 2 / 0.933
        ix, iy = X.astype(int), Y.astype(int)
        ok = (ix >= 0) & (ix < 128 * s) & (iy >= 0) & (iy < 256 * s)
        ix, iy, prof, cor = ix[ok], iy[ok], prof[ok], cor[ok]
        ordem = np.argsort(prof)                      # os da frente ficam por último
        img = np.zeros((256 * s, 128 * s, 4), dtype=float)
        img[iy[ordem], ix[ordem], :3] = cor[ordem]
        img[iy[ordem], ix[ordem], 3] = 255
        im = Image.fromarray(img.astype(np.uint8), "RGBA")
        # fecha furinhos entre pontos (1 px) antes de reduzir
        from PIL import ImageFilter
        cheio = im.filter(ImageFilter.MaxFilter(3))
        a = np.array(im)
        b = np.array(cheio)
        buraco = (a[..., 3] == 0) & (b[..., 3] > 0)
        viz = np.array(im.filter(ImageFilter.MaxFilter(3)))
        a[buraco] = viz[buraco]
        return Image.fromarray(a, "RGBA").resize((128, 256), Image.LANCZOS)


def _tijolo_face(u, v, face):
    if face == "topo":
        return np.broadcast_to(np.array([150, 146, 138.0]), u.shape + (3,)) + kf.grao(u, v, 6, 3)[..., None]
    z = v * PX_M
    return kf.TIJOLO(u % 1.0, z)


AZUL = (40, 92, 168)


def caixa_dagua(r, h):
    c = Cena()
    c.cilindro(0.5, 0.5, r, 0.0, h, AZUL, cor_tampa=(48, 104, 180))
    c.cilindro(0.5, 0.5, r * 1.04, h - 0.04, h + 0.02, (36, 84, 156), cor_tampa=(54, 110, 186))   # tampa
    c.cilindro(0.5, 0.5, r * 0.25, h + 0.02, h + 0.05, (60, 120, 196))
    c.haste(0.5 - r * 0.7, 0.5 + r * 0.7, 0.15, 0.5 - r * 0.7, 0.5 + r * 1.25, 0.15, 0.015, (200, 200, 200))   # cano
    return c.render()


def caixa_amianto():
    c = Cena()
    c.caixa(0.18, 0.18, 0.0, 0.82, 0.82, 0.75, (150, 150, 144))
    c.caixa(0.15, 0.15, 0.75, 0.85, 0.85, 0.79, (128, 128, 122))
    c.haste(0.18, 0.6, 0.12, -0.05, 0.6, 0.12, 0.015, (110, 110, 110))
    return c.render()


def churrasqueira(lado):
    """Churrasqueira de alvenaria: base de tijolo, boca virada para sul (S) ou leste (E), chaminé."""
    c = Cena()
    if lado == "S":
        c.caixa(0.15, 0.3, 0.0, 0.85, 0.8, 0.9, None, _tijolo_face)
        c.caixa(0.25, 0.79, 0.35, 0.75, 0.81, 0.75, (30, 26, 24))          # boca
        c.caixa(0.3, 0.35, 0.9, 0.7, 0.7, 1.25, None, _tijolo_face)       # coifa
        c.caixa(0.42, 0.42, 1.25, 0.58, 0.58, 1.9, None, _tijolo_face)    # chaminé
    else:
        c.caixa(0.3, 0.15, 0.0, 0.8, 0.85, 0.9, None, _tijolo_face)
        c.caixa(0.79, 0.25, 0.35, 0.81, 0.75, 0.75, (30, 26, 24))
        c.caixa(0.35, 0.3, 0.9, 0.7, 0.7, 1.25, None, _tijolo_face)
        c.caixa(0.42, 0.42, 1.25, 0.58, 0.58, 1.9, None, _tijolo_face)
    return c.render()


FERRO = (96, 62, 44)


def pilar_ferro():
    c = Cena()
    c.caixa(0.0, 0.0, 0.0, 0.16, 0.16, 0.35, (156, 154, 148))            # toco de pilar (canto NO)
    for dx, dy in ((0.04, 0.04), (0.12, 0.04), (0.04, 0.12), (0.12, 0.12)):
        c.haste(dx, dy, 0.35, dx + 0.01, dy - 0.005, 1.25, 0.008, FERRO)
    return c.render()


def ferro_solto():
    c = Cena()
    for dx, dy, h in ((0.05, 0.05, 1.1), (0.12, 0.05, 0.9), (0.05, 0.12, 1.0), (0.12, 0.12, 1.2)):
        c.haste(dx, dy, 0.0, dx + 0.02, dy + 0.01, h, 0.008, FERRO)
    return c.render()


def antena():
    c = Cena()
    c.haste(0.5, 0.5, 0.0, 0.5, 0.5, 0.9, 0.02, (90, 90, 92))
    # prato: calota inclinada virada para o norte-oeste
    us, vs = np.meshgrid(np.linspace(-1, 1, 160), np.linspace(-1, 1, 160), indexing="ij")
    dentro = us ** 2 + vs ** 2 <= 1
    us, vs = us[dentro], vs[dentro]
    r = 0.3
    prof = 0.06 * (us ** 2 + vs ** 2)
    # base do prato: plano inclinado com normal (−0.5, −0.5, 0.7)
    e1 = np.array([0.7, -0.7, 0.0])
    e2 = np.array([-0.4, -0.4, 0.82])
    nrm = np.cross(e1, e2)
    pts = np.array([0.5, 0.5, 1.0]) + r * (us[:, None] * e1 + vs[:, None] * e2) + prof[:, None] * nrm
    c.add(pts.reshape(-1, 1, 3), (206, 206, 202), nrm)
    c.haste(0.5, 0.5, 1.0, 0.5 + nrm[0] * 0.3, 0.5 + nrm[1] * 0.3, 1.0 + nrm[2] * 0.3, 0.01, (80, 80, 80))
    return c.render()


ROUPAS = [(196, 52, 48), (240, 236, 226), (52, 92, 170), (236, 196, 56), (64, 140, 84)]


def varal(lado):
    c = Cena()
    if lado == "x":       # ao longo de x
        a, b = (0.05, 0.5), (0.95, 0.5)
    else:
        a, b = (0.5, 0.05), (0.5, 0.95)
    for (x, y) in (a, b):
        c.haste(x, y, 0.0, x, y, 1.7, 0.012, (120, 120, 120))
    c.haste(a[0], a[1], 1.65, b[0], b[1], 1.65, 0.004, (220, 220, 220))
    for k, cor in enumerate(ROUPAS):
        t0, t1 = 0.12 + k * 0.16, 0.12 + k * 0.16 + 0.12
        x0, y0 = a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0
        x1, y1 = a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1
        c.pano(x0, y0, x1, y1, 1.65, 0.35 + 0.1 * (k % 2), cor)
    return c.render()


SOLIDO = [["BlocksPlacement", ""], ["solid", ""]]
OBJETOS = [
    ("caixa_dagua_1000", "caixa d'água azul de 1000 L", lambda: caixa_dagua(0.42, 0.85), SOLIDO),
    ("caixa_dagua_500", "caixa d'água azul de 500 L", lambda: caixa_dagua(0.33, 0.7), SOLIDO),
    ("caixa_dagua_amianto", "caixa d'água velha de amianto", caixa_amianto, SOLIDO),
    ("churrasqueira_s", "churrasqueira de tijolo, boca para o sul", lambda: churrasqueira("S"), SOLIDO),
    ("churrasqueira_e", "churrasqueira de tijolo, boca para o leste", lambda: churrasqueira("E"), SOLIDO),
    ("pilar_ferro_espera", "pilar com ferro de espera (canto do tile)", pilar_ferro, [["BlocksPlacement", ""], ["solidtrans", ""]]),
    ("ferro_espera", "ferro de espera saindo da laje", ferro_solto, []),
    ("antena_parabolica", "antena parabólica", antena, [["BlocksPlacement", ""]]),
    ("varal_x", "varal com roupa (leste-oeste)", lambda: varal("x"), []),
    ("varal_y", "varal com roupa (norte-sul)", lambda: varal("y"), []),
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
    return kf._gravar(folha, nome, "objeto", pecas, saida, {})


if __name__ == "__main__":
    tiles2x, tdefs, saida = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    defs = {d["nome"]: d for d in kit_tiles.ler_definicoes(tdefs)}
    import json
    print(json.dumps([lajes(tiles2x, saida), muretas(tiles2x, defs, saida), objetos(saida)], ensure_ascii=False))
