"""Kit Brasil: manchas de parede como sobreposição ("grime"), separadas da parede.

Regra do usuário (09/11/2026): parede sempre limpa; o que é mancha vira uma peça
por cima, que se põe depois (no BuildingEd: "Grime" do prédio, ou no modo de
peças, camada de sobreposição de parede):

- `rsb_overlay_grime_wall_01`: SUJEIRA, sai com a limpeza do jogo. A ação
  "Limpar sangue" (água sanitária + pano, vassoura ou esfregão) chama
  `IsoGridSquare.removeGrime()`, que apaga toda sobreposição de parede cujo nome
  contém "overlay_grime" (lido no projectzomboid.jar, 42.21). Variações: lama na
  base, escorrido de chuva, mofo na base, gordura e fuligem (cozinha, bar).
- `rsb_desgaste_parede_02`: REBOCO ESTRAGADO (o _01 é o de `kit_desgaste.py`, da favela), permanente (o nome não tem
  "overlay_grime", "overlay_graffiti" nem "overlay_messages", então nenhuma
  limpeza apaga). Variações: tinta descascando, reboco caído mostrando o tijolo,
  rachaduras, buraco grande de reboco com rachaduras. As manchas mostram o
  material de baixo (reboco cinza, tijolo), então servem em parede de qualquer cor.

Cada variação tem as 8 peças da parede (oeste, norte, quina, pilar, janela e porta
nos dois lados), recortadas pela forma da parede do jogo; propriedades da sujeira
original (`overlay_grime_wall_01`: WallOverlay, attachedW/N). Registradas na lista
"grime_wall" do BuildingEd.

Uso: python -I -X utf8 kit_grime.py <pasta Tiles/2x> <newtiledefinitions.tiles> <kits/tiles>
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
import kit_tiles  # noqa: E402
import texturas_favela as tf  # noqa: E402

PX_M = tf.PX_M
MOLDE_GRIME = "overlay_grime_wall_01"


# ---------------------------------------------------------------- manchas: (cor, altura, alfa) na grade da parede
def lama_base(seed=131):
    U, Z = tf.grade_parede()
    v, m = Z / 192, Z / PX_M
    lama = tf.sstep(0.6, 0.0, m) * (0.55 + 0.45 * tf.fbm(U, v, 6, 3, 4, seed))
    resp, _ = tf.pontos(U, v, 40, 30, 0.45, 0.35, seed + 1)
    resp = resp * tf.sstep(0.9, 0.1, m)
    a = np.clip(lama * 0.6 + resp * 0.55, 0, 0.85)
    cor = np.array([74, 62, 50.0]) * (0.85 + 0.3 * tf.vn(U, v, 30, 20, seed + 2))[..., None]
    return cor, 0.2 * a, a


def escorrido(seed=132):
    U, Z = tf.grade_parede()
    v = Z / 192
    lista = tf.vn(U, v * 0.25, 23, 1, seed) ** 4 * (0.3 + 0.7 * tf.vn(U, v, 23, 3, seed + 1))
    a = np.clip(0.75 * lista * tf.sstep(0.15, 1.0, v) + 0.15 * tf.sstep(0.85, 1.0, v), 0, 0.7)
    cor = np.array([62, 60, 56.0]) * np.ones(U.shape + (1,))
    return cor, np.zeros_like(U), a


def mofo_base(seed=133):
    U, Z = tf.grade_parede()
    v, m = Z / 192, Z / PX_M
    nuvem = tf.fbm(U, v, 8, 4, 4, seed)
    a = tf.sstep(0.55, 0.0, m) * tf.sstep(0.45, 0.65, nuvem)
    pint, _ = tf.pontos(U, v, 60, 60, 0.5, 0.3, seed + 1)
    a = np.clip(a * 0.7 + pint * tf.sstep(0.9, 0.2, m) * 0.5, 0, 0.8)
    cor = tf.mistura(np.array([52, 64, 46.0]) * np.ones(U.shape + (1,)), np.array([30, 34, 30.0]),
                     tf.vn(U, v, 20, 20, seed + 2))
    return cor, 0.1 * a, a


def gordura(seed=134):
    U, Z = tf.grade_parede()
    v, m = Z / 192, Z / PX_M
    gord = tf.sstep(0.55, 0.85, tf.fbm(U, v, 3, 4, 4, seed)) * tf.sstep(0.6, 1.0, m) * tf.sstep(2.2, 1.5, m)
    fuli = tf.sstep(1.8, 2.7, m) * (0.5 + 0.5 * tf.fbm(U, v, 4, 3, 3, seed + 1))
    a = np.clip(gord * 0.45 + fuli * 0.55, 0, 0.75)
    cor = tf.mistura(np.array([150, 126, 84.0]) * np.ones(U.shape + (1,)), np.array([40, 36, 32.0]),
                     np.clip(fuli / (gord + fuli + 1e-3), 0, 1))
    return cor, np.zeros_like(U), a


def _reboco_cinza(seed):
    U, Z = tf.grade_parede()
    return tf._reboco_base(U, Z, seed, 1.0)


def tinta_descascando(seed=141):
    U, Z = tf.grade_parede()
    v = Z / 192
    n = tf.fbm(U, v, 7, 12, 5, seed)
    sai = n > 0.66
    borda = np.abs(n - 0.66) < 0.008
    reb, h_reb = _reboco_cinza(seed + 1)
    cor = np.where(borda[..., None], np.array([232, 230, 222.0]), reb)
    h = np.where(sai, h_reb - 0.5, 0.6)
    a = np.where(sai | borda, 1.0, 0.0)
    return cor, h, a


def reboco_caido(seed=142, grande=False):
    U, Z = tf.grade_parede()
    v, m = Z / 192, Z / PX_M
    if grande:
        n = tf.fbm(U, v, 3, 5, 4, seed) + 0.35 * tf.sstep(1.2, 0.0, m)
        lim_t, lim_r = 0.72, 0.8
    else:
        n = tf.fbm(U, v, 6, 10, 5, seed)
        lim_t, lim_r = 0.68, 0.76
    sai_tinta = n > lim_t
    sai_reboco = n > lim_r
    reb, h_reb = _reboco_cinza(seed + 1)
    tij, h_tij = tf.tijolo_baiano(1, limpo=True)
    cor = np.where(sai_reboco[..., None], tij * 0.95, reb)
    h = np.where(sai_reboco, h_tij - 2.4, h_reb - 0.4)
    borda = np.abs(n - lim_t) < 0.008
    cor = np.where(borda[..., None], np.array([232, 230, 222.0]), cor)
    a = np.where(sai_tinta | borda, 1.0, 0.0)
    if grande:
        cor2, h2, a2 = rachaduras_m(seed + 5, n=3)
        cor = np.where((a2 > a)[..., None], cor2, cor)
        h = np.where(a2 > a, h2, h)
        a = np.maximum(a, a2)
    return cor, h, a


def rachaduras_m(seed=143, n=2):
    U, Z = tf.grade_parede()
    v = Z / 192
    rac = tf.rachaduras(U, v, 63, 192, n, 16, seed, galhos=True)
    fio = np.clip(1 - rac / 0.6, 0, 1)
    cor = np.array([58, 54, 50.0]) * np.ones(U.shape + (1,))
    return cor, -1.0 * fio, np.clip(fio * 0.7, 0, 0.7)


SUJEIRA = [
    ("lama_base", "sujeira de rua na base (respingo de lama)", lama_base),
    ("escorrido_chuva", "escorrido de chuva", escorrido),
    ("mofo_base", "mofo na base", mofo_base),
    ("gordura_fuligem", "gordura e fuligem (cozinha, bar)", gordura),
]
DESGASTE = [
    ("tinta_descascando", "tinta descascando (aparece o reboco)", tinta_descascando),
    ("reboco_caido", "reboco caído (aparece o tijolo)", reboco_caido),
    ("rachaduras", "rachaduras", rachaduras_m),
    ("reboco_caido_grande", "buraco grande no reboco, com rachaduras", lambda: reboco_caido(144, True)),
]


# ---------------------------------------------------------------- peças
def _uz(face):
    Y, X = np.mgrid[0:256, 0:128].astype(float)
    X, Y = X + 0.5, Y + 0.5
    uw = np.clip((63 - X) / 63, 0, 0.9999)
    un = np.clip((X - 63) / 63, 0, 0.9999)
    zw, zn = 192 + 32 * uw - Y, 192 + 32 * un - Y
    oeste = np.ones_like(X, bool) if face == "W" else np.zeros_like(X, bool) if face == "N" else X < 63
    return np.where(oeste, uw, un), np.where(oeste, zw, zn)


def peca(molde, face, texs, Lref, alfa_grade):
    im = np.array(kf.peca_parede_tex(molde, face, texs, Lref))
    U, Z = _uz(face)
    Zs = np.clip(np.abs(Z), 0, 191.9)
    a = tf.amostrar_parede(alfa_grade[..., None], U, Zs)[..., 0]
    a = np.where(Z > 188, 0, a)                      # nada no topo da parede
    im[..., 3] = (im[..., 3].astype(float) * a).astype(np.uint8)
    return Image.fromarray(im, "RGBA")


def folha(nome, variacoes, tiles2x, defs, saida):
    molde_im = Image.open(tiles2x / f"{kf.MOLDE_PAREDE[0]}.png").convert("RGBA")
    base = kf.MOLDE_PAREDE[1]
    w = kf._celula(molde_im, base)
    Lref = np.median(kf._lum(w)[w[..., 3] > 200])
    linhas = ((len(variacoes) + 1) // 2) * 2
    img = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    pecas = [{"peca": f"{nome}_{i}", "props": []} for i in range(linhas * 8)]
    entradas = []
    for k, (chave, desc, f) in enumerate(variacoes):
        cor, h, a = f()
        texs = kb._iluminar(cor, h)
        b = (k // 2) * 16 + (k % 2) * 4
        papel = {}
        for off, face, prop in kf.PAPEIS:
            i = b + off
            img.alpha_composite(peca(kf._celula(molde_im, base + off), face, texs, Lref, a),
                                ((i % 8) * 128, (i // 8) * 256))
            papel[prop] = i
            props = [list(p) for p in (defs[MOLDE_GRIME]["pecas"][off] or [])] or [["WallOverlay", ""]]
            pecas[i] = {"peca": f"{nome}_{i}", "nome": f"{chave} {prop}", "descricao": desc, "props": props}
        entradas.append({"West": papel["WallW"], "North": papel["WallN"], "NorthWest": papel["WallNW"],
                         "SouthEast": papel["WallSE"], "WestWindow": papel["WindowW"],
                         "NorthWindow": papel["WindowN"], "WestDoor": papel["DoorWallW"],
                         "NorthDoor": papel["DoorWallN"]})
    return kf._gravar(img, nome, "sobreposicao", pecas, saida, {"grime_wall": entradas})


if __name__ == "__main__":
    tiles2x, tdefs, saida = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    defs = {d["nome"]: d for d in kit_tiles.ler_definicoes(tdefs)}
    res = [folha("rsb_overlay_grime_wall_01", SUJEIRA, tiles2x, defs, saida),
           folha("rsb_desgaste_parede_02", DESGASTE, tiles2x, defs, saida)]
    print(json.dumps(res, ensure_ascii=False))
