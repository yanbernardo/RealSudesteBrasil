"""Calçadão de Copacabana: pedra portuguesa em ondas (Kit Brasil, 1ª peça nova).

Como é o calçadão de verdade (fotos do Wikimedia Commons, 08/11/2026): listras
pretas e brancas TRANSVERSAIS (cruzam a largura da calçada), cada uma ondulando
uma vez de um lado ao outro, todas em fase ("mar largo").

Como o script faz caber isso em peças quadradas do jogo:

1. Campo contínuo no mapa. O desenho é uma função do lugar no mapa, periódica:
   numa avenida reta ao longo de x ele se repete a cada poucos tiles ao longo e
   através, então bastam poucas peças e cada uma encaixa perfeitamente nas
   vizinhas. Uma "família" de peças por direção (ver CONJUNTOS): "4dir" (retas
   e diagonais, listras largas, 68 peças) ou "8dir" (também 1 x 2 tiles, 26,6°,
   listras mais finas, 132 peças; a Av. Atlântica usa só 4 famílias = 66).
2. Trechos. Cada trecho da avenida usa a família mais perto da direção dele
   (as listras ficam um pouco inclinadas, como um campo que a calçada
   "recorta": até 22,5° no "4dir", 13° no "8dir"). Trechos curtos são juntados.
3. Costura. Onde a família muda, a fase da família nova (deslocamento do
   campo, que não pede peça nova) e a linha da costura são escolhidas para
   errar o mínimo: corte mínimo num grafo (cada tile da janela de troca é
   "família de trás" ou "da frente"; o custo de uma borda entre os dois é
   quantas cores não batem nela).
4. Pedra portuguesa. Pedrinhas (diagrama de Voronoi periódico no mesmo campo,
   ~11 por tile) com rejunte e cor levemente variada; a cor de cada pedra vem
   do campo no centro dela, então a borda da listra segue as pedras, como na
   calçada real. Peça de 128 x 256 com o piso no losango de baixo, recortado
   com a máscara exata de um piso do jogo (`floors_exterior_street_01_0`).

Uso (Python do .venv do KnoxMap):
    python -I -X utf8 calcadao.py folha <pasta Tiles/2x> <pasta de saída>
    python -I -X utf8 calcadao.py simular <pasta Tiles/2x> <pasta lots> <ruas_debug.json> <pasta de saída>
"""
from __future__ import annotations

import json
import math
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

R2 = math.sqrt(2)
LARGURA = 6               # largura do calçadão em tiles (uma onda inteira de lado a lado)
NOME_FOLHA = "rsb_calcadao_01"

# Cada família: direção da calçada (`ang`, graus, x para leste e y para sul), matriz M
# que leva (x, y) a p = ao longo e q = através (em "unidades p": |linha de M| por tile),
# P = período ao longo (2 listras) e Q = período da onda através, inteiros, para o
# desenho repetir em tiles inteiros. Duas opções:
CONJUNTOS = {
    # 4 direções, listras largas (1,5 tile nas retas, 1,41 nas diagonais), onda ~6:
    # 68 peças; a listra pode ficar até 22,5° torta em relação à calçada.
    "4dir": {"amp": 0.6, "familias": {
        "f000": {"ang": 0.0, "P": 3, "Q": 6, "M": ((1, 0), (0, 1))},
        "f045": {"ang": 45.0, "P": 4, "Q": 8, "M": ((1, 1), (-1, 1))},
        "f090": {"ang": 90.0, "P": 3, "Q": 6, "M": ((0, 1), (1, 0))},
        "f135": {"ang": 135.0, "P": 4, "Q": 8, "M": ((-1, 1), (1, 1))},
    }},
    # 8 direções (também as de 1 x 2 tiles, 26,6°), listras de ~1,06 tile, onda ~6:
    # 132 peças; a listra fica no máximo 13° torta. As de 26,6° só saem baratas
    # (15 peças) com P e Q múltiplos de 5, daí as listras mais finas em todas.
    "8dir": {"amp": 0.85, "familias": {
        "f000": {"ang": 0.0, "P": 2, "Q": 6, "M": ((1, 0), (0, 1))},
        "f027": {"ang": math.degrees(math.atan2(1, 2)), "P": 5, "Q": 15, "M": ((2, 1), (-1, 2))},
        "f045": {"ang": 45.0, "P": 3, "Q": 8, "M": ((1, 1), (-1, 1))},
        "f063": {"ang": math.degrees(math.atan2(2, 1)), "P": 5, "Q": 15, "M": ((1, 2), (-2, 1))},
        "f090": {"ang": 90.0, "P": 2, "Q": 6, "M": ((0, 1), (1, 0))},
        "f117": {"ang": math.degrees(math.atan2(2, -1)), "P": 5, "Q": 15, "M": ((-1, 2), (2, 1))},
        "f135": {"ang": 135.0, "P": 3, "Q": 8, "M": ((-1, 1), (1, 1))},
        "f153": {"ang": math.degrees(math.atan2(1, -2)), "P": 5, "Q": 15, "M": ((-2, 1), (1, 2))},
    }},
}
FAMILIAS: dict = {}
ORDEM: list = []
AMP = 0.6                 # ondulação da borda da listra, em larguras de listra


def usar(conjunto: str, so: list | None = None) -> None:
    """Escolhe o conjunto; `so` limita às famílias que a folha leva (as outras
    direções caem na família disponível mais perto)."""
    global FAMILIAS, ORDEM, AMP
    FAMILIAS = CONJUNTOS[conjunto]["familias"]
    ORDEM = [f for f in FAMILIAS if not so or f in so]
    AMP = CONJUNTOS[conjunto]["amp"]
    _PEDRAS.clear()


# Peças do jogo: asfalto e calçada de concreto saem da mesma folha (blends_street_01);
# 96-103 são calçada. Meio-fio (street_curbs_01) na calçada, na borda que dá para o
# asfalto: 40 oeste, 41 norte, 42 sul, 43 leste; quinas 44 (O+N), 45 (O+S), 46 (N+L), 2 (S+L).
CALCADA_CONCRETO = set(range(96, 104))
MEIO_FIO = {"W": 40, "N": 41, "S": 42, "E": 43}
QUINAS = {frozenset("WN"): 44, frozenset("WS"): 45, frozenset("NE"): 46, frozenset("SE"): 2}


def e_asfalto(pilha) -> bool:
    if not pilha or not pilha[0].startswith("blends_street_01_"):
        return False
    return int(pilha[0].rsplit("_", 1)[1]) not in CALCADA_CONCRETO


def meio_fio(k, asfalto) -> list[str]:
    """Peças de meio-fio de um tile do calçadão, pelas bordas que dão para o asfalto."""
    x, y = k
    lados = {s for s, v in (("W", (x - 1, y)), ("N", (x, y - 1)), ("E", (x + 1, y)), ("S", (x, y + 1)))
             if asfalto(v)}
    out = []
    for par, n in QUINAS.items():
        if par <= lados:
            out.append(n)
            lados -= par
    out += [MEIO_FIO[s] for s in sorted(lados)]
    return [f"street_curbs_01_{n}" for n in out]

PRETO = np.array([60, 58, 57], dtype=float)       # basalto (apagado, como o jogo)
BRANCO = np.array([201, 196, 183], dtype=float)   # calcário
REJUNTE = np.array([118, 112, 102], dtype=float)
PEDRA_TILE = 0.09         # tamanho de uma pedrinha, em tiles

# losango do piso numa peça 128 x 256 (igual ao do jogo): topo (63,192),
# direita (126,224), base (63,256), esquerda (0,224)
CX, TOPO, MEIA_L, MEIA_A = 63.0, 192.0, 63.0, 32.0


# ---------------------------------------------------------------- o campo
def pq(f: str, x, y):
    (a, b), (c, d) = FAMILIAS[f]["M"]
    return a * x + b * y, c * x + d * y


def preta(f: str, p, q):
    F = FAMILIAS[f]
    return np.floor(2 * p / F["P"] + AMP * np.sin(2 * math.pi * q / F["Q"])).astype(int) % 2 == 0


def chave(f: str, x: int, y: int) -> tuple[int, int]:
    """Classe da peça de um tile (canto (x, y)) no campo sem deslocamento."""
    F = FAMILIAS[f]
    p, q = pq(f, x, y)
    return p % F["P"], q % F["Q"]


def classes(f: str) -> dict:
    """{chave: tile representante}, na ordem em que aparecem."""
    out = {}
    for y in range(24):
        for x in range(24):
            out.setdefault(chave(f, x, y), (x, y))
    return out


def catalogo() -> list[tuple[str, tuple[int, int], tuple[int, int]]]:
    """Todas as peças da folha: (família, chave, tile representante)."""
    return [(f, k, rep) for f in ORDEM for k, rep in classes(f).items()]


# ---------------------------------------------------------------- pedras
class Pedras:
    """Voronoi periódico no toro [0,P) x [0,Q) da família (em unidades p)."""

    def __init__(self, f: str, semente: int):
        F = FAMILIAS[f]
        esc = math.hypot(*F["M"][0])                 # unidades p por tile
        self.f, self.P, self.Q, self.esc = f, F["P"], F["Q"], esc
        g = PEDRA_TILE * esc
        self.nP, self.nQ = max(1, round(self.P / g)), max(1, round(self.Q / g))
        self.gp, self.gq = self.P / self.nP, self.Q / self.nQ
        rnd = np.random.default_rng(semente)
        jit = rnd.uniform(-0.38, 0.38, size=(self.nP, self.nQ, 2))
        ii, jj = np.meshgrid(np.arange(self.nP), np.arange(self.nQ), indexing="ij")
        self.sp = (ii + 0.5 + jit[..., 0]) * self.gp
        self.sq = (jj + 0.5 + jit[..., 1]) * self.gq
        cor = np.where(preta(f, self.sp, self.sq)[..., None], PRETO, BRANCO)
        self.cor = cor * rnd.normal(1.0, 0.045, size=(self.nP, self.nQ, 1))
        self.cor += rnd.normal(0, 3.0, size=(self.nP, self.nQ, 3))

    def cores(self, p, q):
        p, q = np.mod(p, self.P), np.mod(q, self.Q)
        i0, j0 = np.floor(p / self.gp).astype(int), np.floor(q / self.gq).astype(int)
        f1 = np.full(p.shape, np.inf)
        f2 = np.full(p.shape, np.inf)
        idx = np.zeros(p.shape + (2,), dtype=int)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                i, j = i0 + di, j0 + dj
                wi, wj = np.mod(i, self.nP), np.mod(j, self.nQ)
                # posição da semente com a volta do toro
                spx = self.sp[wi, wj] + (i - wi) / self.nP * self.P
                sqy = self.sq[wi, wj] + (j - wj) / self.nQ * self.Q
                d = np.hypot(p - spx, q - sqy)
                menor = d < f1
                f2 = np.where(menor, f1, np.minimum(f2, d))
                idx[..., 0] = np.where(menor, wi, idx[..., 0])
                idx[..., 1] = np.where(menor, wj, idx[..., 1])
                f1 = np.where(menor, d, f1)
        base = self.cor[idx[..., 0], idx[..., 1]]
        # pedra levemente abaulada: mais clara no meio
        r = f1 / (0.62 * self.gp)
        base = base * np.clip(1.07 - 0.2 * r * r, 0.82, 1.08)[..., None]
        borda = (f2 - f1) / 2 / self.esc                  # distância até o rejunte, em tiles
        t = np.clip((borda - 0.0045) / 0.007, 0, 1)[..., None]
        return REJUNTE * (1 - t) + base * t


_PEDRAS: dict = {}


def pedras(f: str) -> Pedras:
    if f not in _PEDRAS:
        _PEDRAS[f] = Pedras(f, 1000 + ORDEM.index(f))
    return _PEDRAS[f]


# ---------------------------------------------------------------- peças
_MASCARA = None


def mascara(tiles2x: Path) -> np.ndarray:
    """Alfa exato do piso do jogo (peça 128 x 256)."""
    global _MASCARA
    if _MASCARA is None:
        im = Image.open(tiles2x / "floors_exterior_street_01.png").convert("RGBA")
        _MASCARA = np.array(im.crop((0, 0, 128, 256)))[..., 3]
    return _MASCARA


def peca(f: str, rep: tuple[int, int], tiles2x: Path, ss: int = 3) -> Image.Image:
    """Peça 128 x 256 do tile `rep` do campo da família `f`."""
    ys, xs = np.mgrid[192:256, 0:128]
    acc = np.zeros(xs.shape + (3,))
    for a in range(ss):
        for b in range(ss):
            X = xs + (a + 0.5) / ss
            Y = ys + (b + 0.5) / ss
            u, v = (X - CX) / MEIA_L, (Y - TOPO) / MEIA_A          # u = s - t, v = s + t
            s, t = (u + v) / 2, (v - u) / 2
            p, q = pq(f, rep[0] + s, rep[1] + t)
            acc += pedras(f).cores(p, q)
    rgb = acc / (ss * ss)
    rgb += np.random.default_rng(hash((f, rep)) & 0xFFFF).normal(0, 2.0, rgb.shape)
    out = np.zeros((256, 128, 4), dtype=np.uint8)
    out[192:256, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    out[..., 3] = mascara(tiles2x)
    return Image.fromarray(out, "RGBA")


def folha(tiles2x: Path, saida: Path) -> list:
    """Folha no formato do jogo (8 colunas de 128 x 256) + lista do que é cada peça."""
    cat = catalogo()
    linhas = (len(cat) + 7) // 8
    im = Image.new("RGBA", (1024, linhas * 256), (0, 0, 0, 0))
    manifesto = []
    for n, (f, k, rep) in enumerate(cat):
        im.alpha_composite(peca(f, rep, tiles2x), ((n % 8) * 128, (n // 8) * 256))
        manifesto.append({"peca": f"{NOME_FOLHA}_{n}", "familia": f, "chave": list(k)})
    saida.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import estilo_pz  # filtro de estilo do jogo (aprovado em 09/11/2026)
    im = estilo_pz.filtrar_folha(im, "piso")
    im.save(saida / f"{NOME_FOLHA}.png")
    (saida / f"{NOME_FOLHA}.json").write_text(json.dumps(
        {"folha": NOME_FOLHA, "estilo": estilo_pz.ESTILO, "familias": {f: {k: v for k, v in FAMILIAS[f].items() if k != "M"} for f in ORDEM},
         "pecas": manifesto}, ensure_ascii=False, indent=1), encoding="utf-8")
    # prévia só com os losangos, para conferir
    prev = Image.new("RGBA", (8 * 132, linhas * 70), (45, 45, 45, 255))
    for n in range(len(cat)):
        cel = im.crop(((n % 8) * 128, (n // 8) * 256 + 192, (n % 8) * 128 + 128, (n // 8) * 256 + 256))
        prev.alpha_composite(cel, ((n % 8) * 132 + 2, (n // 8) * 70 + 3))
    prev.save(saida / f"{NOME_FOLHA}_previa.png")
    return manifesto


# ---------------------------------------------------------------- atribuição
def ang_dif(a: float, b: float) -> float:
    d = abs(a - b) % 180
    return min(d, 180 - d)


def trechos(linha, minimo: int = 14) -> list[dict]:
    """Família de cada pedaço da avenida (por posição t ao longo dela)."""
    n = int(linha.length)
    angs = []
    for t in range(n + 1):
        a, b = linha.interpolate(max(0, t - 6)), linha.interpolate(min(linha.length, t + 6))
        angs.append(math.degrees(math.atan2(b.y - a.y, b.x - a.x)) % 180)
    fam = [min(ORDEM, key=lambda f: ang_dif(a, FAMILIAS[f]["ang"])) for a in angs]
    runs = []
    for t, f in enumerate(fam):
        if runs and runs[-1]["f"] == f:
            runs[-1]["t1"] = t + 1
        else:
            runs.append({"f": f, "t0": t, "t1": t + 1})
    while len(runs) > 1:
        curto = min(range(len(runs)), key=lambda i: runs[i]["t1"] - runs[i]["t0"])
        r = runs[curto]
        if r["t1"] - r["t0"] >= minimo:
            break
        media = angs[(r["t0"] + r["t1"]) // 2]
        viz = [i for i in (curto - 1, curto + 1) if 0 <= i < len(runs)]
        alvo = min(viz, key=lambda i: ang_dif(media, FAMILIAS[runs[i]["f"]]["ang"]))
        runs[alvo]["t0"] = min(runs[alvo]["t0"], r["t0"])
        runs[alvo]["t1"] = max(runs[alvo]["t1"], r["t1"])
        del runs[curto]
        junta = []
        for q in runs:
            if junta and junta[-1]["f"] == q["f"]:
                junta[-1]["t1"] = q["t1"]
            else:
                junta.append(q)
        runs = junta
    runs[0]["t0"], runs[-1]["t1"] = -10 ** 6, 10 ** 6
    for r in runs:
        trecho = angs[max(0, r["t0"]):min(len(angs), r["t1"])]
        r["inclinacao_max"] = round(max(ang_dif(a, FAMILIAS[r["f"]]["ang"]) for a in trecho), 1)
    return runs


AMOSTRAS = 12


def custo_borda(fa, oa, fb, ob, x0, y0, x1, y1) -> int:
    """Quantas das AMOSTRAS cores da borda (x0,y0)-(x1,y1) diferem entre os dois campos."""
    k = (np.arange(AMOSTRAS) + 0.5) / AMOSTRAS
    x, y = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    pa = preta(fa, *pq(fa, x - oa[0], y - oa[1]))
    pb = preta(fb, *pq(fb, x - ob[0], y - ob[1]))
    return int(np.sum(pa != pb))


def borda_comum(u, v):
    """Borda entre dois tiles vizinhos (4-vizinhança)."""
    (x, y), (x2, y2) = u, v
    if x2 == x + 1:
        return x + 1, y, x + 1, y + 1
    if x2 == x - 1:
        return x, y, x, y + 1
    if y2 == y + 1:
        return x, y + 1, x + 1, y + 1
    return x, y, x + 1, y


def corte_minimo(livres, fixos_a, fixos_b, peso):
    """Max-flow (Edmonds-Karp) num grafo pequeno; devolve os livres que ficam do lado A."""
    cap: dict = {}

    def liga(a, b, c):
        cap.setdefault(a, {}).setdefault(b, 0.0)
        cap.setdefault(b, {}).setdefault(a, 0.0)
        cap[a][b] += c
        cap[b][a] += c

    for u in livres:
        x, y = u
        for v in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if v in livres and u < v:
                liga(u, v, peso(u, v))
            elif v in fixos_a:
                liga("S", u, peso(u, v))
            elif v in fixos_b:
                liga(u, "T", peso(u, v))
    if "S" not in cap or "T" not in cap:
        return set(livres) if "T" not in cap else set(), 0.0
    fluxo = 0.0
    while True:
        pai = {"S": None}
        fila = deque(["S"])
        while fila and "T" not in pai:
            a = fila.popleft()
            for b, c in cap[a].items():
                if c > 1e-9 and b not in pai:
                    pai[b] = a
                    fila.append(b)
        if "T" not in pai:
            break
        b, f = "T", math.inf
        while pai[b] is not None:
            f = min(f, cap[pai[b]][b])
            b = pai[b]
        b = "T"
        while pai[b] is not None:
            cap[pai[b]][b] -= f
            cap[b][pai[b]] += f
            b = pai[b]
        fluxo += f
    return {u for u in pai if u not in ("S", "T")}, fluxo


def atribuir(faixa: dict, linha, janela: int = 5) -> tuple[dict, list]:
    """faixa = {(x, y): t}. Devolve {(x, y): (família, deslocamento)} e o relatório das costuras."""
    runs = trechos(linha)
    run_de = {}
    for k, t in faixa.items():
        run_de[k] = next(i for i, r in enumerate(runs) if r["t0"] <= t < r["t1"])
    rotulo = {k: run_de[k] for k in faixa}
    desloc = [(0, 0)] * len(runs)
    rel = []
    for i in range(len(runs) - 1):
        tb0 = runs[i]["t1"]
        fa, fb = runs[i]["f"], runs[i + 1]["f"]
        nos = [k for k in faixa if run_de[k] in (i, i + 1)]
        melhor = None
        # o ponto da troca pode andar alguns tiles (sem deixar trecho curto demais)
        for s in range(-6, 7, 2):
            tb = tb0 + s
            if tb - runs[i]["t0"] < 2 * janela + 2 or runs[i + 1]["t1"] - tb < 2 * janela + 2:
                continue
            livres = {k for k in nos if abs(faixa[k] - tb) <= janela}
            fixa = {k for k in nos if k not in livres and faixa[k] < tb}
            fixb = {k for k in nos if k not in livres and faixa[k] >= tb}
            for _ch, o in classes(fb).items():
                def peso(u, v, o=o):
                    return custo_borda(fa, desloc[i], fb, o, *borda_comum(u, v)) + 0.3
                lado_a, custo = corte_minimo(livres, fixa, fixb, peso)
                if melhor is None or custo < melhor[0]:
                    melhor = (custo, o, lado_a, tb, livres)
        custo, o, lado_a, tb, livres = melhor
        desloc[i + 1] = o
        runs[i]["t1"] = runs[i + 1]["t0"] = tb
        for k in nos:
            if k in livres:
                lado = i if k in lado_a else i + 1
            else:
                lado = i if faixa[k] < tb else i + 1
            rotulo[k] = run_de[k] = lado
        rel.append({"t": round(tb), "de": fa, "para": fb, "erro": round(custo, 1),
                    "tiles_na_janela": len(livres)})
    out = {k: (runs[r]["f"], desloc[r]) for k, r in rotulo.items()}
    return out, rel


def erros_costura(atrib: dict) -> tuple[int, int]:
    """(amostras de cor que não batem, amostras de borda entre tiles de campos diferentes)."""
    ruim = total = 0
    for (x, y), (f, o) in atrib.items():
        for v in ((x + 1, y), (x, y + 1)):
            if v in atrib and atrib[v] != (f, o):
                g, p = atrib[v]
                ruim += custo_borda(f, o, g, p, *borda_comum((x, y), v))
                total += AMOSTRAS
    return ruim, total


def indice_da_peca(f: str, o, x: int, y: int, idx: dict) -> int:
    return idx[(f, chave(f, x - o[0], y - o[1]))]


# ---------------------------------------------------------------- simulação
def ler_chao(lots: Path):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import zonas_historias as zh
    chao, ocupado, _ = zh.ler_mapa(lots)
    return chao, ocupado


def faixa_no_mapa(chao, ocupado, linha):
    """Tiles do calçadão: do lado do mar, colados no asfalto da avenida, LARGURA de largura."""
    from shapely.geometry import Point
    xs, ys = zip(*linha.coords)
    caixa = [(x, y) for x in range(int(min(xs)) - 25, int(max(xs)) + 26)
             for y in range(int(min(ys)) - 25, int(max(ys)) + 26) if (x, y) in chao]
    (x0, y0), (x1, y1) = linha.coords[0], linha.coords[-1]
    sinal_mar = 1 if (-(y1 - y0) + (x1 - x0)) > 0 else -1     # mar para x + y maior (sudeste)
    info = {}
    for k in caixa:
        p = Point(k[0] + 0.5, k[1] + 0.5)
        t = linha.project(p)
        q = linha.interpolate(t)
        a, b = linha.interpolate(max(0, t - 1)), linha.interpolate(min(linha.length, t + 1))
        nx, ny = -(b.y - a.y), b.x - a.x
        lado = (p.x - q.x) * nx + (p.y - q.y) * ny
        info[k] = (t, p.distance(q), lado * sinal_mar > 0)
    asf = lambda k: e_asfalto(chao.get(k))
    # meia largura do asfalto do lado do mar, por pedaço da avenida
    meia = {}
    for k, (t, d, mar) in info.items():
        if mar and asf(k) and d < 14:
            b = int(t)
            meia[b] = max(meia.get(b, 0), d)
    agua = lambda k: any(n.startswith("blends_natural_02") for n in chao[k][:1])
    faixa = {}
    for k, (t, d, mar) in info.items():
        if not mar or asf(k) or k in ocupado or agua(k) or t <= 0.5 or t >= linha.length - 0.5:
            continue
        h = max((meia.get(b, 0) for b in range(int(t) - 2, int(t) + 3)), default=0)
        # da borda de fora do asfalto (calçada de concreto inclusa; 2,5 de folga para os
        # dentes da escada) até LARGURA além. Sem a folga de baixo, a calçada do canteiro
        # central (entre as duas pistas) também virava calçadão.
        if h and h - 2.5 < d <= h + LARGURA:
            faixa[k] = t
    # tira tiles soltos (pontas em degrau com um vizinho só)
    while True:
        soltos = [k for k in faixa
                  if sum((k[0] + dx, k[1] + dy) in faixa for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) <= 1]
        if not soltos:
            break
        for k in soltos:
            del faixa[k]
    return faixa


class Desenhista:
    def __init__(self, tiles2x: Path, escala: float):
        self.dir, self.esc = tiles2x, escala
        self.folhas, self.cache, self.faltam = {}, {}, set()

    def celula(self, nome: str):
        if nome in self.cache:
            return self.cache[nome]
        folha_, _, n = nome.rpartition("_")
        im = None
        try:
            if folha_ not in self.folhas:
                self.folhas[folha_] = Image.open(self.dir / f"{folha_}.png").convert("RGBA")
            f = self.folhas[folha_]
            n = int(n)
            im = f.crop(((n % 8) * 128, (n // 8) * 256, (n % 8) * 128 + 128, (n // 8) * 256 + 256))
        except (OSError, ValueError):
            self.faltam.add(folha_)
        if im is not None and self.esc != 1:
            im = im.resize((max(1, round(128 * self.esc)), max(1, round(256 * self.esc))), Image.LANCZOS)
        self.cache[nome] = im
        return im

    def iso(self, caminho: Path, chao, janela, calc: dict, pecas_calc: list, so_chao=False):
        """Desenha a janela como o jogo: o calçadão no lugar do chão (com meio-fio
        novo) e, no asfalto vizinho, sem a mistura de areia da borda."""
        asfalto = lambda k: e_asfalto(chao.get(k))
        vizinho = {(x + dx, y + dy) for (x, y) in calc for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
        x0, y0, x1, y1 = janela
        e = self.esc
        cel = [p.resize((max(1, round(128 * e)), max(1, round(256 * e))), Image.LANCZOS) if e != 1 else p
               for p in pecas_calc]
        W = int(((x1 - x0) + (y1 - y0)) * 63 * e + 128 * e) + 20
        H = int(((x1 - x0) + (y1 - y0)) * 32 * e + 256 * e) + 20
        im = Image.new("RGBA", (W, H), (58, 96, 128, 255))
        ox = (y1 - y0) * 63 * e + 10
        oy = 10 + 160 * e
        pular = ("e_", "vegetation", "f_bushes", "d_plants", "d_generic")
        for (x, y) in sorted(((x, y) for x in range(x0, x1) for y in range(y0, y1)),
                             key=lambda k: (k[0] + k[1], k[0])):
            pilha = chao.get((x, y))
            if not pilha:
                continue
            sx = ox + ((x - x0) - (y - y0)) * 63 * e - 63 * e
            sy = oy + ((x - x0) + (y - y0)) * 32 * e - 192 * e
            if (x, y) in calc:
                im.alpha_composite(cel[calc[(x, y)]], (int(round(sx)), int(round(sy))))
                resto = [n for n in pilha[1:] if not n.startswith(("blends_", "floors_", "d_", "street_"))]
                resto = meio_fio((x, y), asfalto) + resto
            elif (x, y) in vizinho and asfalto((x, y)):
                resto = [n for n in pilha if not n.startswith("blends_natural")]
            else:
                resto = pilha
            for nome in resto:
                if nome.startswith(pular) or (so_chao and not nome.startswith(("blends_", "floors_", "street_"))):
                    continue
                c = self.celula(nome)
                if c is not None:
                    im.alpha_composite(c, (int(round(sx)), int(round(sy))))
        im.convert("RGB").save(caminho)


def simular(tiles2x: Path, lots: Path, ruas_debug: Path, saida: Path) -> dict:
    from shapely.geometry import LineString
    saida.mkdir(parents=True, exist_ok=True)
    coords = next([tuple(c) for c in r["coords"]] for r in json.loads(ruas_debug.read_text(encoding="utf-8"))["final"]
                  if r["nome"] == "Avenida Atlântica")
    linha = LineString(coords)
    chao, ocupado = ler_chao(lots)
    faixa = faixa_no_mapa(chao, ocupado, linha)
    atrib, rel = atribuir(faixa, linha)
    cat = catalogo()
    idx = {(f, k): n for n, (f, k, _r) in enumerate(cat)}
    calc = {k: indice_da_peca(f, o, k[0], k[1], idx) for k, (f, o) in atrib.items()}
    pecas_calc = [peca(f, rep, tiles2x) for f, _k, rep in cat]
    ruim, total = erros_costura(atrib)
    res = {"tiles": len(faixa), "pecas_na_folha": len(cat), "pecas_usadas": len(set(calc.values())),
           "trechos": [{"familia": r["f"], "inicio": max(0, r["t0"]), "fim": min(round(linha.length), r["t1"]),
                        "inclinacao_max_graus": r["inclinacao_max"]} for r in trechos(linha)],
           "costuras": rel,
           "cores_que_nao_batem_nas_costuras": f"{ruim} de {total}"}
    # vistas: inteira (pequena) e de perto em trechos de cada família e numa costura
    xs, ys = zip(*faixa)
    d = Desenhista(tiles2x, 0.125)
    d.iso(saida / "v2_inteira.png", chao, (min(xs) - 8, min(ys) - 8, max(xs) + 9, max(ys) + 9), calc, pecas_calc, so_chao=True)
    perto = Desenhista(tiles2x, 0.5)
    vistos = set()
    for f in ORDEM:
        ks = sorted(k for k, (g, _o) in atrib.items() if g == f)
        if ks:
            cx, cy = ks[len(ks) // 2]
            perto.iso(saida / f"v2_trecho_{f}.png", chao, (cx - 13, cy - 13, cx + 14, cy + 14), calc, pecas_calc)
            vistos.add(f)
    for n, c in enumerate(rel):
        k = min(faixa, key=lambda k: abs(faixa[k] - c["t"]))
        perto.iso(saida / f"v2_costura_{n}.png", chao, (k[0] - 12, k[1] - 12, k[0] + 13, k[1] + 13), calc, pecas_calc)
    ks = sorted(faixa, key=lambda k: faixa[k])
    k = ks[len(ks) // 3]
    Desenhista(tiles2x, 1.0).iso(saida / "v2_detalhe.png", chao, (k[0] - 5, k[1] - 5, k[0] + 6, k[1] + 6), calc, pecas_calc)
    res["folhas_que_faltam"] = sorted(d.faltam | perto.faltam)
    (saida / "v2_resumo.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return res


TIRAR_DO_CALCADAO = ("blends_", "floors_", "d_", "street_")   # chão, misturas, sujeira, meio-fio velho


def aplicar(lots: Path, calcadoes: list[dict]) -> dict:
    """Depois de compilar: troca o chão da faixa de cada calçadão nas células.

    `calcadoes`: [{"coords": [[x, y], ...] (linha da avenida, tiles do mundo),
    "direcoes": 8, "familias": [...], "largura": 6}]. No calçadão: a peça nova,
    o meio-fio refeito e o que não é chão (postes etc.); no asfalto vizinho, sem
    a mistura de areia da borda. Pode rodar de novo no mesmo mapa (dá o mesmo)."""
    global LARGURA
    from shapely.geometry import LineString
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import lots as _lots
    chao, ocupado = ler_chao(lots)
    asfalto = lambda k: e_asfalto(chao.get(k))
    celulas: dict = {}

    def celula(k):
        c = (k[0] // _lots.CELL, k[1] // _lots.CELL)
        if c not in celulas:
            if not (lots / f"{c[0]}_{c[1]}.lotheader").exists():
                celulas[c] = None
            else:
                celulas[c] = _lots.Celula(lots, *c)
        return celulas[c]

    rel = []
    for cfg in calcadoes:
        usar(f"{cfg.get('direcoes', 8)}dir", cfg.get("familias"))
        LARGURA = int(cfg.get("largura", 6))
        linha = LineString(cfg["coords"])
        faixa = faixa_no_mapa(chao, ocupado, linha)
        atrib, costuras = atribuir(faixa, linha)
        cat = catalogo()
        idx = {(f, k): n for n, (f, k, _r) in enumerate(cat)}
        trocados, usadas = 0, set()
        for k, (f, o) in atrib.items():
            c = celula(k)
            if c is None:
                continue
            peca_ = f"{NOME_FOLHA}_{indice_da_peca(f, o, k[0], k[1], idx)}"
            usadas.add(peca_)
            resto = [n for n in c.nomes_em(*k)[1:] if not n.startswith(TIRAR_DO_CALCADAO)]
            if c.trocar(k[0], k[1], [peca_] + meio_fio(k, asfalto) + resto):
                trocados += 1
        limpos = 0
        for (x, y) in {(x + dx, y + dy) for (x, y) in atrib for dx in (-1, 0, 1) for dy in (-1, 0, 1)}:
            if (x, y) in atrib or not asfalto((x, y)):
                continue
            c = celula((x, y))
            nomes = c.nomes_em(x, y) if c else []
            sem = [n for n in nomes if not n.startswith("blends_natural")]
            if c and len(sem) != len(nomes):
                c.trocar(x, y, sem)
                limpos += 1
        ruim, total = erros_costura(atrib)
        # conferência: objeto de quadra/praia em cima do calçadão (não devia haver)
        sobre = sorted({n.rsplit("_", 1)[0] for k in atrib for n in (celula(k).nomes_em(*k) if celula(k) else [])
                        if not n.startswith((NOME_FOLHA, "street_curbs", "lighting_"))})
        rel.append({"tiles": trocados, "asfalto_limpo": limpos, "pecas_usadas": len(usadas),
                    "costuras": costuras, "cores_que_nao_batem": f"{ruim} de {total}",
                    "outras_pecas_no_calcadao": sobre})
        for k in atrib:                      # o mapa lido passa a ter o calçadão (próximo da lista)
            chao[k] = celula(k).nomes_em(*k) if celula(k) else chao.get(k)
    gravadas = 0
    for c in celulas.values():
        if c is not None:
            c.gravar()
            gravadas += 1
    return {"calcadoes": rel, "celulas_regravadas": gravadas}


if __name__ == "__main__":
    a = sys.argv[1:]
    conj = "4dir"
    if "--direcoes" in a:
        i = a.index("--direcoes")
        conj = f"{a[i + 1]}dir"
        del a[i:i + 2]
    so = None
    if "--familias" in a:
        i = a.index("--familias")
        so = a[i + 1].split(",")
        del a[i:i + 2]
    usar(conj, so)
    if a and a[0] == "folha":
        m = folha(Path(a[1]), Path(a[2]))
        print(conj, len(m), "peças;", {f: sum(1 for x in m if x["familia"] == f) for f in ORDEM})
    elif a and a[0] == "simular":
        print(json.dumps(simular(Path(a[1]), Path(a[2]), Path(a[3]), Path(a[4])), ensure_ascii=False, indent=1))
    else:
        print(__doc__)
