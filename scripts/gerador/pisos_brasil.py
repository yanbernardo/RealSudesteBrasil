"""Kit Brasil: folha de pisos brasileiros feita por script (`rsb_pisos_01`).

Cada piso é um desenho plano (função de s, t em 0..1 dentro do tile) projetado no
losango do jogo com a mesma conta do `calcadao.py`. Cada padrão tem 2 peças: a
"A" e a "B" (cor ou posição diferente), para variar sem repetir o mesmo desenho.
Peça 0..N em `PISOS`; o que cada uma é fica no `.json` ao lado da folha.

Uso (Python do .venv do KnoxMap):
    python -I -X utf8 pisos_brasil.py <pasta Tiles/2x> <pasta kits/tiles>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import calcadao as cal  # noqa: E402

NOME = "rsb_pisos_01"


def _hash(a, b, seed=0):
    h = (a * 374761393 + b * 668265263 + seed * 2246822519) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return (h ^ (h >> 16)) / 4294967295.0


def pedrinhas(s, t, n, cores, seed):
    """Pedra portuguesa: n x n células com semente deslocada, rejunte entre elas."""
    gx, gy = s * n, t * n
    ix, iy = np.floor(gx).astype(int), np.floor(gy).astype(int)
    f1 = np.full(s.shape, 9.0)
    f2 = np.full(s.shape, 9.0)
    cor = np.zeros(s.shape + (3,))
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            i, j = ix + di, iy + dj
            px = i + 0.5 + (_hash(i % n, j % n, seed) - 0.5) * 0.7
            py = j + 0.5 + (_hash(i % n, j % n, seed + 7) - 0.5) * 0.7
            d = np.hypot(gx - px, gy - py)
            menor = d < f1
            f2 = np.where(menor, f1, np.minimum(f2, d))
            k = (_hash(i % n, j % n, seed + 3) * len(cores)).astype(int) % len(cores)
            var = 0.92 + 0.16 * _hash(i % n, j % n, seed + 5)
            cor = np.where(menor[..., None], np.array(cores, dtype=float)[k] * var[..., None], cor)
            f1 = np.where(menor, d, f1)
    junta = np.clip(((f2 - f1) / 2 - 0.03) / 0.05, 0, 1)[..., None]
    return np.array([112, 106, 98.0]) * (1 - junta) + cor * junta


def blocos(s, t, nx, ny, cores, junta=0.05, escalonado=False, seed=0, cor_junta=(96, 92, 86)):
    gx, gy = s * nx, t * ny
    iy = np.floor(gy).astype(int)
    if escalonado:
        gx = gx + 0.5 * (iy % 2)
    ix = np.floor(gx).astype(int)
    fx, fy = gx - ix, gy - iy
    var = 0.9 + 0.2 * _hash(ix % (2 * nx), iy % ny, seed)
    k = (_hash(ix % (2 * nx), iy % ny, seed + 1) * len(cores)).astype(int) % len(cores)
    cor = np.array(cores, dtype=float)[k] * var[..., None]
    borda = np.minimum(np.minimum(fx, 1 - fx) * nx, np.minimum(fy, 1 - fy) * ny) / max(nx, ny) * max(nx, ny)
    mascara = np.clip((borda - junta * 0.5) / (junta * 0.5), 0, 1)[..., None]
    return np.array(cor_junta, dtype=float) * (1 - mascara) + cor * mascara


def ruido(s, t, base, forca=6, seed=0):
    n = np.floor(s * 64).astype(int), np.floor(t * 64).astype(int)
    r = (_hash(n[0], n[1], seed) - 0.5) * 2 * forca
    return np.array(base, dtype=float) + r[..., None]


def tatil(s, t, fundo, bolinhas=True):
    """Piso tátil (alerta): bolinhas em grade sobre fundo amarelo; direcional: barras."""
    cor = ruido(s, t, fundo, 4, 11)
    if bolinhas:
        u, v = (s * 5) % 1 - 0.5, (t * 5) % 1 - 0.5
        pino = np.hypot(u, v) < 0.28
        cor = np.where(pino[..., None], np.array(fundo, dtype=float) * 1.12, cor * 0.9)
    else:
        barra = ((s * 4) % 1 > 0.25) & ((s * 4) % 1 < 0.75)
        cor = np.where(barra[..., None], np.array(fundo, dtype=float) * 1.12, cor * 0.9)
    return np.clip(cor, 0, 255)


def hidraulico(s, t, c1, c2, c3):
    """Ladrilho hidráulico: 2 x 2 motivos de losango e quadrado em 3 cores."""
    u, v = (s * 2) % 1 - 0.5, (t * 2) % 1 - 0.5
    losango = np.abs(u) + np.abs(v) < 0.34
    miolo = np.maximum(np.abs(u), np.abs(v)) < 0.12
    borda = np.maximum(np.abs(u), np.abs(v)) > 0.46
    cor = np.where(losango[..., None], np.array(c2, dtype=float), np.array(c1, dtype=float))
    cor = np.where(miolo[..., None], np.array(c3, dtype=float), cor)
    cor = np.where(borda[..., None], np.array(c3, dtype=float) * 0.8, cor)
    return cor + (_hash(np.floor(s * 128).astype(int), np.floor(t * 128).astype(int), 5)[..., None] - 0.5) * 8


# (nome, o que é, função (s, t) -> rgb)
PISOS = [
    ("pedra_branca_a", "pedra portuguesa branca (calcário), lisa", lambda s, t: pedrinhas(s, t, 11, [(214, 208, 192), (204, 198, 182)], 1)),
    ("pedra_branca_b", "pedra portuguesa branca, variação", lambda s, t: pedrinhas(s, t, 11, [(222, 216, 200), (198, 192, 178)], 2)),
    ("pedra_preta_a", "pedra portuguesa preta (basalto), lisa", lambda s, t: pedrinhas(s, t, 11, [(58, 56, 55), (70, 67, 65)], 3)),
    ("pedra_preta_b", "pedra portuguesa preta, variação", lambda s, t: pedrinhas(s, t, 11, [(50, 49, 49), (66, 63, 60)], 4)),
    ("pedra_cinza_a", "pedra portuguesa cinza (calçada comum)", lambda s, t: pedrinhas(s, t, 11, [(150, 146, 138), (128, 124, 118), (170, 164, 154)], 5)),
    ("pedra_cinza_b", "pedra portuguesa cinza, variação", lambda s, t: pedrinhas(s, t, 11, [(140, 136, 130), (160, 156, 146), (122, 118, 112)], 6)),
    ("paralelepipedo_a", "paralelepípedo de granito (rua antiga)", lambda s, t: blocos(s, t, 3, 5, [(124, 122, 118), (108, 106, 104), (138, 134, 126)], 0.09, True, 7)),
    ("paralelepipedo_b", "paralelepípedo, variação", lambda s, t: blocos(s, t, 3, 5, [(118, 114, 110), (102, 100, 98), (134, 128, 120)], 0.09, True, 8)),
    ("lajota_a", "lajota de barro vermelha (quintal, varanda)", lambda s, t: blocos(s, t, 2, 2, [(168, 82, 60), (158, 74, 54), (176, 92, 68)], 0.05, False, 9, (150, 140, 128))),
    ("lajota_b", "lajota de barro, mais escura", lambda s, t: blocos(s, t, 2, 2, [(146, 66, 48), (138, 62, 46), (156, 76, 56)], 0.05, False, 10, (140, 130, 118))),
    ("ceramica_a", "cerâmica bege com rejunte (cozinha, área)", lambda s, t: blocos(s, t, 3, 3, [(224, 214, 190), (216, 206, 182)], 0.04, False, 11, (190, 184, 170))),
    ("ceramica_b", "cerâmica cinza-clara (banheiro, comércio)", lambda s, t: blocos(s, t, 3, 3, [(200, 202, 202), (192, 194, 196)], 0.04, False, 12, (160, 160, 158))),
    ("cimento_queimado_a", "cimento queimado vermelho (garagem, varanda)", lambda s, t: ruido(s, t, (178, 58, 48), 9, 13)),
    ("cimento_queimado_b", "cimento queimado cinza liso (quintal)", lambda s, t: ruido(s, t, (170, 168, 162), 9, 14)),
    ("tatil_alerta", "piso tátil de alerta (amarelo, bolinhas)", lambda s, t: tatil(s, t, (226, 190, 40), True)),
    ("tatil_direcional", "piso tátil direcional (amarelo, barras)", lambda s, t: tatil(s, t, (226, 190, 40), False)),
    ("hidraulico_a", "ladrilho hidráulico azul e branco", lambda s, t: hidraulico(s, t, (226, 224, 214), (58, 92, 150), (30, 52, 100))),
    ("hidraulico_b", "ladrilho hidráulico vermelho e creme", lambda s, t: hidraulico(s, t, (230, 220, 196), (176, 62, 48), (92, 40, 34))),
    ("placas_concreto_a", "calçada de placas de concreto 2 x 2", lambda s, t: blocos(s, t, 2, 2, [(176, 174, 168), (168, 166, 160)], 0.035, False, 15, (120, 118, 112))),
    ("placas_concreto_b", "calçada de placas, desgastada", lambda s, t: blocos(s, t, 2, 2, [(158, 156, 148), (150, 148, 142)], 0.04, False, 16, (112, 108, 102))),
    ("ciclovia_a", "ciclovia de asfalto vermelho", lambda s, t: ruido(s, t, (150, 66, 58), 10, 17)),
    ("ciclovia_b", "ciclovia, desgastada", lambda s, t: ruido(s, t, (138, 76, 68), 12, 18)),
]


def peca(func, tiles2x: Path, ss: int = 3) -> Image.Image:
    ys, xs = np.mgrid[192:256, 0:128]
    acc = np.zeros(xs.shape + (3,))
    for a in range(ss):
        for b in range(ss):
            X, Y = xs + (a + 0.5) / ss, ys + (b + 0.5) / ss
            u, v = (X - cal.CX) / cal.MEIA_L, (Y - cal.TOPO) / cal.MEIA_A
            s, t = (u + v) / 2, (v - u) / 2
            acc += func(np.clip(s, 0, 1), np.clip(t, 0, 1))
    out = np.zeros((256, 128, 4), dtype=np.uint8)
    out[192:256, :, :3] = np.clip(acc / (ss * ss), 0, 255).astype(np.uint8)
    out[..., 3] = cal.mascara(tiles2x)
    return Image.fromarray(out, "RGBA")


def gerar(tiles2x: Path, saida: Path) -> int:
    linhas = (len(PISOS) + 7) // 8
    im = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    for n, (_nome, _desc, f) in enumerate(PISOS):
        im.alpha_composite(peca(f, tiles2x), ((n % 8) * 128, (n // 8) * 256))
    saida.mkdir(parents=True, exist_ok=True)
    im.save(saida / f"{NOME}.png")
    (saida / f"{NOME}.json").write_text(json.dumps(
        {"folha": NOME, "tipo": "piso",
         "pecas": [{"peca": f"{NOME}_{n}", "nome": nome, "descricao": desc,
                    "props": [["diamondFloor", ""], ["exterior", ""], ["solidfloor", ""]]}
                   for n, (nome, desc, _f) in enumerate(PISOS)]}, ensure_ascii=False, indent=1), encoding="utf-8")
    prev = Image.new("RGBA", (8 * 132, linhas * 70), (45, 45, 45, 255))
    for n in range(len(PISOS)):
        prev.alpha_composite(im.crop(((n % 8) * 128, (n // 8) * 256 + 192, (n % 8) * 128 + 128, (n // 8) * 256 + 256)),
                             ((n % 8) * 132 + 2, (n // 8) * 70 + 3))
    prev.save(saida / f"{NOME}_previa.png")
    return len(PISOS)


if __name__ == "__main__":
    print(gerar(Path(sys.argv[1]), Path(sys.argv[2])), "pisos")
