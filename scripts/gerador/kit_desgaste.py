"""Kit Brasil: desgaste de parede separado da parede (pedido do usuário, 09/11/2026).

Paredes iguais lado a lado repetem o mesmo buraco e a mesma mancha. Por isso a
parede vem limpa (`kit_favela.paredes`) e o desgaste vem por cima, em camada de
"overlay" (como as manchas do jogo, `overlay_grime_wall_01`):

1. Grime de favela (lista "Grime - Walls" do BuildingEd, aplicado por cômodo):
   sujeira suave que pode repetir sem incomodar: lama e respingo na base, mofo
   rente ao chão, escorrido de chuva leve. Dois: leve e forte.
2. Manchas avulsas (lista de móveis, grupos "Kit Brasil - Desgaste de parede"),
   para pôr à mão onde quiser, cada uma num lado (oeste/norte) e em várias
   formas: tinta descascando (4), reboco caído com tijolo aparecendo (3),
   rachadura (3), mofo e infiltração (2), escorrido (2).

Folha `rsb_desgaste_parede_01` em `kits/tiles/`.
Uso: python -I -X utf8 kit_desgaste.py <pasta Tiles/2x> <kits/tiles>
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
NOME = "rsb_desgaste_parede_01"
MOLDE = ("walls_interior_house_01", 4)
PAPEIS = kf.PAPEIS            # (deslocamento, face, papel) das 8 peças de um estilo de parede


def _face(X, Y, face):
    uw = np.clip((63 - X) / 63, 0, 0.9999)
    un = np.clip((X - 63) / 63, 0, 0.9999)
    zw, zn = 192 + 32 * uw - Y, 192 + 32 * un - Y
    if face == "W":
        oeste = np.ones_like(X, dtype=bool)
    elif face == "N":
        oeste = np.zeros_like(X, dtype=bool)
    else:
        oeste = X < 63
    return np.where(oeste, uw, un), np.where(oeste, zw, zn), oeste


def _combinar(camadas):
    """[(cor RGB, alfa 0..1)] -> cor e alfa juntos (uma sobre a outra)."""
    cor = np.zeros(camadas[0][1].shape + (3,))
    alfa = np.zeros(camadas[0][1].shape)
    for c, a in camadas:
        c = np.broadcast_to(np.asarray(c, float), a.shape + (3,))
        cor = cor * (1 - a[..., None]) + c * a[..., None]
        alfa = alfa + a * (1 - alfa)
    return cor, alfa


# ---------------------------------------------------------------- grime
def sujeira(u, z, forca, seed):
    """Cor e alfa da sujeira suave numa posição da parede (u 0..1, z em px)."""
    m, v = z / PX_M, z / 192
    lama = tf.sstep(0.55, 0.0, m) * (0.5 + 0.5 * tf.fbm(u, v, 6, 3, 4, seed)) * 0.55 * forca
    resp, _ = tf.pontos(u, v, 40, 30, 0.45, 0.35, seed + 1)
    resp = resp * tf.sstep(0.9, 0.1, m) * 0.5 * forca
    mofo = tf.sstep(0.4, 0.0, m) * tf.sstep(0.5, 0.62, tf.fbm(u, v, 8, 4, 4, seed + 3)) * 0.45 * forca
    lista = tf.vn(u, v * 0.25, 23, 1, seed + 5) ** 4 * (0.3 + 0.7 * tf.vn(u, v, 23, 3, seed + 6))
    escorre = lista * tf.sstep(0.2, 1.0, v) * 0.32 * forca
    return _combinar([((80, 68, 54), lama), ((70, 58, 46), resp), ((48, 60, 42), mofo), ((44, 40, 36), escorre)])


def peca_grime(molde, face, forca, seed):
    alfa_m = molde[..., 3] / 255.0
    acc_c, acc_a = np.zeros((256, 128, 3)), np.zeros((256, 128))
    Y0, X0 = np.mgrid[0:256, 0:128].astype(float)
    for a in range(kf.SS):
        for b in range(kf.SS):
            X, Y = X0 + (a + 0.5) / kf.SS, Y0 + (b + 0.5) / kf.SS
            u, z, _o = _face(X, Y, face)
            c, al = sujeira(u, np.clip(z, 0, 191.9), forca, seed)
            al = al * (z <= 191)                       # não suja a tampa (topo) da parede
            acc_c += c * al[..., None]
            acc_a += al
    al = acc_a / kf.SS ** 2
    cor = acc_c / np.maximum(acc_a, 1e-6)[..., None]
    out = np.zeros((256, 128, 4), dtype=np.uint8)
    out[..., :3] = np.clip(cor, 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(al * alfa_m * 255, 0, 255).astype(np.uint8)
    return out


# ---------------------------------------------------------------- manchas avulsas
def _blob(U, Z, cu, cz, rw, rh, seed, irregular=0.35):
    v = Z / 192
    d = np.hypot((U - cu) * 63 / rw, (Z - cz) / rh)
    return d + irregular * (tf.fbm(U, v, 6, 10, 4, seed) - 0.5) * 2


def descascado(seed):
    rnd = np.random.default_rng(seed)
    U, Z = tf.grade_parede()
    cu, cz = rnd.uniform(0.35, 0.65), rnd.uniform(45, 150)
    d = _blob(U, Z, cu, cz, rnd.uniform(16, 26), rnd.uniform(24, 44), seed)
    dentro = d < 1
    reb, h_reb = tf._reboco_base(U, Z, seed + 1, 0.8)
    cor = np.where(dentro[..., None], reb * 1.02, 0)
    h = np.where(dentro, h_reb - 0.45, 0.0)
    borda = (d >= 1) & (d < 1.12)                       # lasquinha de tinta levantada
    cor = np.where(borda[..., None], np.array([236, 232, 222.0]), cor)
    h = np.where(borda, 0.25, h)
    alfa = np.where(dentro, 1.0, np.where(borda, 0.55, 0.0))
    # ilhas de tinta que ficaram dentro
    ilha = dentro & (tf.fbm(U, Z / 192, 14, 24, 3, seed + 2) > 0.66)
    alfa = np.where(ilha, 0.0, alfa)
    return cor, h, alfa


def reboco_caido(seed):
    rnd = np.random.default_rng(seed)
    U, Z = tf.grade_parede()
    cu, cz = rnd.uniform(0.35, 0.65), rnd.uniform(40, 140)
    d = _blob(U, Z, cu, cz, rnd.uniform(14, 22), rnd.uniform(20, 36), seed)
    tc, th = tf.tijolo_baiano(1, limpo=True)
    reb, h_reb = tf._reboco_base(U, Z, seed + 1, 1.2)
    fora = d < 1
    tijolo = d < 0.62
    cor = np.where(tijolo[..., None], tc * 0.95, np.where(fora[..., None], reb, 0))
    h = np.where(tijolo, th - 2.4, np.where(fora, h_reb - 0.9, 0.0))
    borda = (d >= 1) & (d < 1.1)
    cor = np.where(borda[..., None], np.array([228, 224, 214.0]), cor)
    alfa = np.where(fora, 1.0, np.where(borda, 0.5, 0.0))
    return cor, h, alfa


def rachadura(seed):
    rnd = np.random.default_rng(seed)
    U, Z = tf.grade_parede()
    x, z = rnd.uniform(0.25, 0.75), rnd.uniform(110, 185)
    ang = math.radians(rnd.uniform(240, 300))        # para baixo, meio inclinada
    pts = [(x, z)]
    galhos = []
    for _ in range(rnd.integers(14, 24)):
        ang += rnd.normal(0, 0.45)
        ang = min(max(ang, math.radians(200)), math.radians(340))
        x2 = min(max(x + math.cos(ang) * 4 / 63, 0.06), 0.94)
        z2 = z + math.sin(ang) * 4
        pts.append((x2, z2))
        if rnd.random() < 0.12:
            galhos.append((x2, z2, ang + rnd.choice([-1, 1]) * 0.8))
        x, z = x2, z2
        if z < 15:
            break
    segs = list(zip(pts, pts[1:]))
    for gx, gz, ga in galhos:
        for _ in range(rnd.integers(2, 5)):
            ga += rnd.normal(0, 0.4)
            g2 = (min(max(gx + math.cos(ga) * 3 / 63, 0.06), 0.94), gz + math.sin(ga) * 3)
            segs.append(((gx, gz), g2))
            gx, gz = g2
    d = np.full(U.shape, 1e9)
    for (ax, az), (bx, bz) in segs:
        px, pz = (U - ax) * 63, Z - az
        vx, vz = (bx - ax) * 63, bz - az
        L2 = vx * vx + vz * vz or 1e-9
        t = np.clip((px * vx + pz * vz) / L2, 0, 1)
        d = np.minimum(d, np.hypot(px - t * vx, pz - t * vz))
    fio = np.clip(1 - d / 0.75, 0, 1)
    lasca = (d < 2.0) & (tf.vn(U, Z / 192, 60, 120, seed) > 0.8)
    cor = np.where(lasca[..., None], np.array([150, 146, 138.0]), np.array([58, 54, 48.0]))
    h = np.where(fio > 0, -0.8 * fio, np.where(lasca, -0.4, 0.0))
    alfa = np.maximum(fio * 0.85, lasca * 0.6)
    return cor, h, alfa


def mofo(seed):
    """Mancha de mofo e infiltração subindo do chão: borda irregular e suave,
    pontinhos escuros, auréola clara de umidade em volta."""
    rnd = np.random.default_rng(seed)
    U, Z = tf.grade_parede()
    v = Z / 192
    cu = rnd.uniform(0.35, 0.65)
    alt = rnd.uniform(40, 80)
    # forma: arco que sobe do chão (mais alto no meio), com borda rasgada
    perfil = alt * np.sqrt(np.clip(1 - ((U - cu) / rnd.uniform(0.26, 0.36)) ** 2, 0, 1))   # meia-lua
    borda = perfil + 14 * (tf.fbm(U, v, 10, 8, 4, seed) - 0.5)
    dentro = tf.sstep(borda + 4, borda - 6, Z)
    textura = 0.5 + 0.5 * tf.fbm(U, v, 24, 36, 4, seed + 2)
    a = dentro * textura * 0.7
    pinta, _ = tf.pontos(U, v, 60, 100, 0.5, 0.45, seed + 3)
    cor = tf.mistura(np.broadcast_to(np.array([52, 66, 42.0]), U.shape + (3,)), np.array([26, 32, 24.0]), pinta)
    aureola = tf.sstep(borda + 16, borda + 4, Z) * (1 - dentro) * (perfil > 6) * (Z > 4) * 0.2
    cor = np.where((aureola > a)[..., None], np.array([150, 138, 116.0]), cor)
    return cor, np.zeros(U.shape), np.clip(np.maximum(a, aureola), 0, 1)


def escorrido(seed):
    """Escorrido de chuva: várias listras finas e irregulares descendo de um
    ponto do alto, mais fortes em cima e sumindo embaixo."""
    rnd = np.random.default_rng(seed)
    U, Z = tf.grade_parede()
    v = Z / 192
    topo = rnd.uniform(150, 188)
    cu = rnd.uniform(0.3, 0.7)
    larg = rnd.uniform(0.2, 0.32)
    faixa = tf.sstep(larg, larg * 0.3, np.abs(U - cu + 0.03 * (tf.fbm(U, v, 4, 6, 3, seed) - 0.5)))
    listras = tf.vn(U, v * 0.15, 70, 1, seed + 1) ** 2
    comp = topo - rnd.uniform(60, 140)
    queda = tf.sstep(topo + 2, topo - 10, Z) * tf.sstep(comp - 10, comp + 40 * listras, Z)
    a = faixa * queda * (0.15 + 0.85 * listras) * 0.42
    return np.broadcast_to(np.array([60, 56, 48.0]), U.shape + (3,)), np.zeros(U.shape), a


TIPOS = [
    ("tinta descascando", descascado, 4),
    ("reboco caído (tijolo aparecendo)", reboco_caido, 3),
    ("rachadura", rachadura, 3),
    ("mofo e infiltração", mofo, 2),
    ("escorrido de chuva", escorrido, 2),
]


def peca_mancha(molde, face, tex_lit, alfa_g):
    alfa_m = molde[..., 3] / 255.0
    acc_c, acc_a = np.zeros((256, 128, 3)), np.zeros((256, 128))
    Y0, X0 = np.mgrid[0:256, 0:128].astype(float)
    for a in range(kf.SS):
        for b in range(kf.SS):
            X, Y = X0 + (a + 0.5) / kf.SS, Y0 + (b + 0.5) / kf.SS
            u, z, _o = _face(X, Y, face)
            dentro = (z >= 0) & (z <= 191)
            c = tf.amostrar_parede(tex_lit, u, np.clip(z, 0, 191.9))
            al = tf.amostrar_parede(alfa_g[..., None], u, np.clip(z, 0, 191.9))[..., 0] * dentro
            acc_c += c * al[..., None]
            acc_a += al
    al = acc_a / kf.SS ** 2
    cor = acc_c / np.maximum(acc_a, 1e-6)[..., None]
    out = np.zeros((256, 128, 4), dtype=np.uint8)
    out[..., :3] = np.clip(cor, 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(al * alfa_m * 255, 0, 255).astype(np.uint8)
    return out


def gerar(tiles2x: Path, saida: Path) -> dict:
    molde_im = Image.open(tiles2x / f"{MOLDE[0]}.png").convert("RGBA")
    n_manchas = sum(n for _t, _f, n in TIPOS)
    linhas = 2 + (n_manchas * 2 + 7) // 8
    folha = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{NOME}_{i}", "props": []} for i in range(linhas * 8)]

    def pos(i, img):
        folha.alpha_composite(Image.fromarray(img, "RGBA"), ((i % 8) * 128, (i // 8) * 256))

    # 1) grime de favela: leve e forte, nas 8 peças de parede
    entradas = []
    for k, (rot, forca) in enumerate((("leve", 0.55), ("forte", 1.0))):
        b = k * 4
        papel = {}
        for off, face, prop in PAPEIS:
            i = b + off
            pos(i, peca_grime(kf._celula(molde_im, MOLDE[1] + off), face, forca, 300 + k))
            papel[prop] = i
            anexo = "attachedW" if face in ("W", "SE") or prop in ("WindowW", "DoorWallW") else "attachedN"
            pecas[i] = {"peca": f"{NOME}_{i}", "nome": f"grime de favela {rot} {prop}",
                        "descricao": f"sujeira de favela {rot} (lama, mofo, escorrido)",
                        "props": [["WallOverlay", ""], [anexo, ""]]}
        nw = papel["WallNW"]
        pecas[nw]["props"] = [["CornerNorthWall", f"{NOME}_{papel['WallN']}"],
                              ["CornerWestWall", f"{NOME}_{papel['WallW']}"]] + pecas[nw]["props"]
        entradas.append({"West": papel["WallW"], "North": papel["WallN"], "NorthWest": nw,
                         "SouthEast": papel["WallSE"], "WestWindow": papel["WindowW"],
                         "NorthWindow": papel["WindowN"], "WestDoor": papel["DoorWallW"],
                         "NorthDoor": papel["DoorWallN"]})
    # 2) manchas avulsas: cada forma em oeste e norte
    moldeW = kf._celula(molde_im, MOLDE[1])
    moldeN = kf._celula(molde_im, MOLDE[1] + 1)
    i = 16
    grupos = []
    for t, (rot, f, n) in enumerate(TIPOS):
        itens = []
        for k in range(n):
            cor, h, alfa = f(500 + t * 10 + k)
            lit = tf.iluminar_parede(np.asarray(cor, float), h)
            iw, iN = i, i + 1
            pos(iw, peca_mancha(moldeW, "W", lit["W"], alfa))
            pos(iN, peca_mancha(moldeN, "N", lit["N"], alfa))
            for j, lado, anexo in ((iw, "oeste", "attachedW"), (iN, "norte", "attachedN")):
                pecas[j] = {"peca": f"{NOME}_{j}", "nome": f"{rot} {k + 1} ({lado})", "descricao": rot,
                            "props": [["WallOverlay", ""], [anexo, ""]]}
            itens.append([{"orient": "W", "tiles": {"0,0": iw}}, {"orient": "N", "tiles": {"0,0": iN}}])
            i += 2
        grupos.append({"grupo": f"Kit Brasil - Desgaste de parede: {rot}", "camada": "WallOverlay", "itens": itens})
    return kf._gravar(folha, NOME, "parede", pecas, saida, {"grime_wall": entradas}, moveis=grupos)


if __name__ == "__main__":
    print(gerar(Path(sys.argv[1]), Path(sys.argv[2])))
