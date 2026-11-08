"""Zonas que ligam as histórias do jogo base (T8, eventos; D-17).

O KnoxMap só grava dois tipos de zona no objects.lua: vagas (ParkingStall) e
área urbana (TownZone). As histórias do jogo dependem de outras (ver
catalogo/HISTORIAS.md, lido do Java do jogo com scripts/ler_classe_java.py):

- histórias de ESTRADA (batida, bloqueio policial, pneu furado...): zona "Nav"
  retangular sobre o asfalto, com mais de 30 tiles de comprimento e menos de
  13 de largura (pelo menos 5). Cada zona recebe no máximo UMA história, por
  isso as ruas são divididas em trechos;
- histórias de ZONA (acampamento, churrasco, piquenique...): zona do tipo
  "ZoneStory" com nome "Forest", "Beach" ou "Lake", de tamanho mínimo por
  história (até 13 x 13), sem água dentro;
- engarrafamento: vaga (ParkingStall) com nome "trafficjamw/e/n/s" ao longo
  de uma faixa (opcional, D-18);
- histórias de CASA não precisam de zona: dependem dos nomes de cômodo
  (quarto + cozinha ou sala + banheiro). Aqui só contamos as casas que servem.

Lê o mapa compilado (.lotheader/.lotpack em output/<mapa>/lots) e acrescenta as
zonas no objects.lua do mod instalado, entre marcas, para poder rodar de novo.

Uso (Python com Pillow, ex.: o .venv do KnoxMap):
    python -X utf8 zonas_historias.py <pasta lots> <objects.lua> [figura.png] [config.json]
"""
from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

CELL, CHUNKS, CHUNK = 256, 32, 8
INICIO = "  -- RSB: zonas de historia (inicio)"
FIM = "  -- RSB: zonas de historia (fim)"

# Padrões do teste; o config pode trocar ("zonasHistorias": {...}).
PADRAO = {
    "navTrecho": 48,          # comprimento alvo de cada zona Nav (> 30)
    "navLarguraMin": 5,       # o jogo exige >= 5 de largura de pista
    "navLarguraMax": 12,      # e < 13
    "historias": [            # [nome, largura, altura, quantas]
        ["Forest", 16, 16, 6],
        ["Beach", 14, 14, 1],
        ["Lake", 14, 14, 1],
    ],
    "margem": 2,              # quadrados livres em volta de cada zona de história
    "engarrafamento": True,   # uma rua com engarrafamento (trafficjam)
}


# ---------------------------------------------------------------- leitura
def _linha(data: bytes, pos: int):
    fim = data.index(b"\n", pos)
    return data[pos:fim].decode("latin-1"), fim + 1


def ler_cabecalho(path: Path):
    data = path.read_bytes()
    pos = 8 if data[:4] == b"LOTH" else 4
    (n,) = struct.unpack_from("<i", data, pos); pos += 4
    nomes = []
    for _ in range(n):
        s, pos = _linha(data, pos)
        nomes.append(s)
    _cw, _ch, lo, hi = struct.unpack_from("<4i", data, pos); pos += 16
    (nr,) = struct.unpack_from("<i", data, pos); pos += 4
    comodos = []
    for _ in range(nr):
        nome, pos = _linha(data, pos)
        _nivel, nrect = struct.unpack_from("<2i", data, pos); pos += 8
        pos += 16 * nrect
        (nobj,) = struct.unpack_from("<i", data, pos); pos += 4
        pos += 12 * nobj
        comodos.append(nome)
    (nb,) = struct.unpack_from("<i", data, pos); pos += 4
    predios = []
    for _ in range(nb):
        (k,) = struct.unpack_from("<i", data, pos); pos += 4
        predios.append(list(struct.unpack_from(f"<{k}i", data, pos))); pos += 4 * k
    return nomes, lo, hi, comodos, predios


def ler_chao(pack: Path, nomes, lo, hi, ox, oy, chao, quartos):
    """Preenche chao[(x, y)] = [tiles] do térreo e quartos[(x, y)] = id do cômodo."""
    data = pack.read_bytes()
    pos = 8 if data[:4] == b"LOTP" else 4
    (n,) = struct.unpack_from("<i", data, pos); pos += 4
    offs = struct.unpack_from(f"<{n}q", data, pos)
    for cx in range(CHUNKS):
        for cy in range(CHUNKS):
            p = offs[cx * CHUNKS + cy]
            if p < 0:
                continue
            pular = 0
            for z in range(lo, hi + 1):
                for x in range(CHUNK):
                    for y in range(CHUNK):
                        if pular > 0:
                            pular -= 1
                            continue
                        (c,) = struct.unpack_from("<i", data, p); p += 4
                        if c == -1:
                            (pular,) = struct.unpack_from("<i", data, p); p += 4
                            pular -= 1
                            continue
                        (sala,) = struct.unpack_from("<i", data, p); p += 4
                        ids = struct.unpack_from(f"<{c - 1}i", data, p); p += 4 * (c - 1)
                        if z == 0:
                            k = (ox + cx * CHUNK + x, oy + cy * CHUNK + y)
                            chao[k] = [nomes[i] for i in ids]
                            if sala >= 0:
                                quartos[k] = sala


def ler_mapa(lots: Path):
    chao, ocupado, casas = {}, set(), {"total": 0, "servem": 0, "faltam": {}}
    for cab in sorted(lots.glob("*.lotheader")):
        cx, cy = (int(v) for v in cab.stem.split("_"))
        nomes, lo, hi, comodos, predios = ler_cabecalho(cab)
        quartos = {}
        ler_chao(lots / f"world_{cx}_{cy}.lotpack", nomes, lo, hi, cx * CELL, cy * CELL, chao, quartos)
        ocupado.update(quartos)
        for ids in predios:
            nomes_c = {comodos[i] for i in ids if 0 <= i < len(comodos)}
            if not nomes_c & {"bedroom", "kitchen", "livingroom", "bathroom"}:
                continue          # loja, escritório etc.: histórias próprias
            casas["total"] += 1
            falta = []
            if "bedroom" not in nomes_c:
                falta.append("quarto")
            if not nomes_c & {"kitchen", "livingroom"}:
                falta.append("cozinha/sala")
            if "bathroom" not in nomes_c:
                falta.append("banheiro")
            if falta:
                chave = " + ".join(falta)
                casas["faltam"][chave] = casas["faltam"].get(chave, 0) + 1
            else:
                casas["servem"] += 1
    return chao, ocupado, casas


# ---------------------------------------------------------------- zonas Nav
def e_rua(pilha) -> bool:
    return bool(pilha) and pilha[0].startswith("blends_street")


def faixas(rua: set, horizontal: bool, cfg) -> list[tuple[int, int, int, int]]:
    """Retângulos de asfalto contínuo (comprimento > 30, largura 5-12).

    Coluna a coluna (para ruas horizontais): cada trecho de asfalto com 5 a 12
    de altura é uma "semente" da rua; ela se estende para os lados enquanto
    houver asfalto cobrindo a mesma altura inteira (atravessa cruzamentos).
    Meio-fio solto, calçada e entrada de garagem não estreitam a rua."""
    if not rua:
        return []
    # trabalha sempre como se a rua fosse horizontal: a = ao longo, b = largura
    pts = {(x, y) if horizontal else (y, x) for x, y in rua}
    colunas = {}
    for a, b in pts:
        colunas.setdefault(a, []).append(b)
    corridas = {}
    for a, bs in colunas.items():
        bs.sort()
        ini = ant = bs[0]
        out = []
        for b in bs[1:] + [None]:
            if b is not None and b == ant + 1:
                ant = b
                continue
            out.append((ini, ant + 1))
            if b is not None:
                ini = ant = b
        corridas[a] = out

    def cobre(a, b0, b1):
        return any(r0 <= b0 and b1 <= r1 for r0, r1 in corridas.get(a, ()))

    segs = set()
    for a, rs in corridas.items():
        for b0, b1 in rs:
            if not cfg["navLarguraMin"] <= b1 - b0 <= cfg["navLarguraMax"]:
                continue
            a0 = a
            while cobre(a0 - 1, b0, b1):
                a0 -= 1
            a1 = a + 1
            while cobre(a1, b0, b1):
                a1 += 1
            if a1 - a0 > 30:
                segs.add((a0, a1, b0, b1))
    # tira os repetidos: um trecho dentro de outro maior (mesma rua, sementes vizinhas)
    segs = sorted(segs, key=lambda s: -(s[1] - s[0]) * (s[3] - s[2]))
    ficam = []
    for s in segs:
        dentro = False
        for t in ficam:
            sobre_b = min(s[3], t[3]) - max(s[2], t[2])
            sobre_a = min(s[1], t[1]) - max(s[0], t[0])
            if sobre_b >= (s[3] - s[2]) / 2 and sobre_a >= (s[1] - s[0]) * 0.8:
                dentro = True
                break
        if not dentro:
            ficam.append(s)
    out = []
    for a0, a1, b0, b1 in ficam:
        if horizontal:
            out.append((a0, b0, a1 - a0, b1 - b0))
        else:
            out.append((b0, a0, b1 - b0, a1 - a0))
    return out


def vagas_de_rua(rua: set, cfg) -> list[tuple[int, int, int, int]]:
    """K11: vagas de carro (ParkingStall de 5 x 3, como as 7 mil do mapa
    original) encostadas no meio-fio, de 7 em 7 tiles. Rua estreita (< 8) só
    de um lado, para sobrar pista; nunca dentro de cruzamento (o lado de fora
    da vaga tem de ser calçada, não asfalto)."""
    out = []
    passo, longe = cfg.get("vagasPasso", 7), 4
    for horizontal in (True, False):
        for x, y, w, h in faixas(rua, horizontal, cfg):
            comp, larg = (w, h) if horizontal else (h, w)
            a0, b0 = (x, y) if horizontal else (y, x)
            lados = [(b0, b0 - 1)] + ([(b0 + larg - 3, b0 + larg)] if larg >= 8 else [])
            for b, fora in lados:
                for a in range(a0 + longe, a0 + comp - longe - 5, passo):
                    if horizontal:
                        calcada = all((a + i, fora) not in rua for i in range(-2, 7))
                        r = (a, b, 5, 3)
                    else:
                        calcada = all((fora, a + i) not in rua for i in range(-2, 7))
                        r = (b, a, 3, 5)
                    if calcada:
                        out.append(r)
    return out


def picotar(r, horizontal: bool, trecho: int):
    """Divide uma faixa longa em trechos (> 30 cada): uma história por trecho."""
    x, y, w, h = r
    comp = w if horizontal else h
    n = max(1, comp // trecho)
    passo = comp / n
    out = []
    for i in range(n):
        a0 = int(round(i * passo))
        a1 = int(round((i + 1) * passo))
        if a1 - a0 <= 30:
            continue
        out.append((x + a0, y, a1 - a0, h) if horizontal else (x, y + a0, w, a1 - a0))
    return out


# ----------------------------------------------------------- engarrafamento
def engarrafamento(rua: set, faixa, cfg) -> list:
    """Trechos de engarrafamento numa rua horizontal, como no mapa original.

    Regra do jogo (IsoChunk.AddVehicles_TrafficJam_*): um carro a cada ~6 tiles
    e a cada 3 de largura; quanto mais longe da ponta "arrumada" da faixa, mais
    torto (até ~115 graus depois de 40 tiles). No mapa original, 630 trechos,
    quase todos de 5 a 30 tiles. Por isso: trechos de até `jamMax` tiles, sem
    passar por cima dos cruzamentos (a 2 tiles deles)."""
    x, y, w, h = faixa
    jmax = cfg.get("jamMax", 30)

    def cruza(c):
        acima = all((c, y - k) in rua for k in range(1, 6))
        abaixo = all((c, y + h - 1 + k) in rua for k in range(1, 6))
        return acima or abaixo

    livres, ini = [], None
    for c in range(x, x + w + 1):
        ok = c < x + w and not cruza(c)
        if ok and ini is None:
            ini = c
        elif not ok and ini is not None:
            livres.append((ini + 2, c - 2))      # 2 tiles longe do cruzamento
            ini = None
    meio = y + h // 2
    out = []
    for a0, a1 in livres:
        comp = a1 - a0
        if comp < 10:
            continue
        n = -(-comp // jmax)
        passo = comp / n
        for i in range(n):
            s0, s1 = a0 + int(round(i * passo)), a0 + int(round((i + 1) * passo))
            out.append((s0, meio - 3, s1 - s0, 3, "trafficjamw"))
            out.append((s0, meio, s1 - s0, 3, "trafficjame"))
    return out


# ---------------------------------------------------------- zonas de história
LIVRE = ("blends_natural_01", "blends_grassoverlays")


def livre(pilha) -> bool:
    return bool(pilha) and pilha[0].startswith("blends_natural_01") and all(
        t.startswith(LIVRE) for t in pilha[1:])


def natural(pilha) -> bool:
    """Chão de terra/grama, com ou sem árvores e arbustos (sem água, rua ou prédio)."""
    return bool(pilha) and pilha[0].startswith("blends_natural_01") and all(
        t.startswith(LIVRE + ("e_", "vegetation_")) for t in pilha[1:])


def zonas_cidade(objects: Path) -> list[tuple[int, int, int, int]]:
    """Retângulos TownZone (área urbana) já gravados pelo KnoxMap."""
    import re
    out = []
    for m in re.finditer(r'type = "TownZone", x = (\d+), y = (\d+), z = 0, width = (\d+), height = (\d+)',
                         objects.read_text(encoding="utf-8")):
        out.append(tuple(int(v) for v in m.groups()))
    return out


def escolher_areas(chao, pedidos, margem, centro, cidade=()):
    """Zonas de história espalhadas em volta do bairro (as mais perto primeiro).

    "Forest" aceita árvores (o jogo limpa a área da cena); praia e lago, só
    gramado livre. Margem de chão livre em volta, 8 tiles entre zonas e fora
    da área urbana (TownZone), como no mapa original."""
    xs = [x for x, _ in chao]
    ys = [y for _, y in chao]
    X0, Y0, X1, Y1 = min(xs), min(ys), max(xs) + 1, max(ys) + 1
    W, H = X1 - X0, Y1 - Y0

    def acumulada(ok):
        S = [[0] * (W + 1) for _ in range(H + 1)]
        for j in range(H):
            acc = 0
            for i in range(W):
                acc += 0 if ok(chao.get((X0 + i, Y0 + j))) else 1
                S[j + 1][i + 1] = S[j][i + 1] + acc
        return S

    tabelas = {"livre": acumulada(livre), "natural": acumulada(natural)}

    def ruins(S, i, j, w, h):
        return S[j + h][i + w] - S[j][i + w] - S[j + h][i] + S[j][i]

    escolhidas = []

    def fora_da_cidade(i, j, w, h):
        x, y = X0 + i, Y0 + j
        return all(not (x < a + c + 4 and a < x + w + 4 and y < b + d + 4 and b < y + h + 4)
                   for (a, b, c, d) in cidade)

    def longe(i, j, w, h):
        for (a, b, c, d, _) in escolhidas:
            if i < a + c + 8 and a < i + w + 8 and j < b + d + 8 and b < j + h + 8:
                return False
        return True

    cx, cy = centro[0] - X0, centro[1] - Y0
    m = margem
    for nome, w, h, qtd in pedidos:
        S = tabelas["natural" if nome == "Forest" else "livre"]
        cands = [(i, j) for j in range(m, H - h - m, 2) for i in range(m, W - w - m, 2)]
        cands.sort(key=lambda p: (p[0] + w / 2 - cx) ** 2 + (p[1] + h / 2 - cy) ** 2)
        feitos = 0
        for i, j in cands:
            if feitos >= qtd:
                break
            if (ruins(S, i - m, j - m, w + 2 * m, h + 2 * m) == 0 and longe(i, j, w, h)
                    and fora_da_cidade(i, j, w, h)):
                escolhidas.append((i, j, w, h, nome))
                feitos += 1
    return [(X0 + i, Y0 + j, w, h, nome) for (i, j, w, h, nome) in escolhidas]


# ------------------------------------------------------------------- saída
def linha_lua(nome, tipo, x, y, w, h):
    return (f'  {{ name = "{nome}", type = "{tipo}", x = {x}, y = {y}, z = 0, '
            f"width = {w}, height = {h} }},")


def gravar(objects: Path, linhas: list[str]) -> None:
    txt = objects.read_text(encoding="utf-8")
    if INICIO in txt:
        a = txt.index(INICIO)
        b = txt.index(FIM) + len(FIM) + 1
        txt = txt[:a] + txt[b:]
    fim = txt.rstrip().rfind("}")
    antes = txt[:fim].rstrip()
    # A última zona do KnoxMap vem sem vírgula; sem ela o jogo recusa o arquivo
    # inteiro (K30) e nenhuma zona carrega, nem as vagas.
    if not antes.endswith((",", "{")):
        antes += ","
    bloco = "\n".join([INICIO] + linhas + [FIM]) + "\n"
    txt = antes + "\n" + bloco + txt[fim:]
    validar_lua(txt)
    objects.write_text(txt, encoding="utf-8")


def validar_lua(txt: str) -> None:
    """Confere a estrutura do objects.lua (tabela de tabelas) antes de gravar:
    chaves equilibradas e vírgula entre as zonas. Para com erro se estiver ruim."""
    import re
    sem_coment = re.sub(r"--[^\n]*", "", txt)
    sem_texto = re.sub(r'"[^"\n]*"', '""', sem_coment)
    nivel, linha, esperando_virgula = 0, 1, False
    for ch in sem_texto:
        if ch == "\n":
            linha += 1
            continue
        if ch.isspace():
            continue
        if esperando_virgula and ch not in ",}":
            raise ValueError(f"objects.lua: falta vírgula antes da linha {linha}")
        esperando_virgula = False
        if ch == "{":
            nivel += 1
        elif ch == "}":
            nivel -= 1
            if nivel < 0:
                raise ValueError(f"objects.lua: '}}' sobrando na linha {linha}")
            if nivel == 1:
                esperando_virgula = True
    if nivel != 0:
        raise ValueError("objects.lua: chaves '{' e '}' não fecham")


def desenhar(png: Path, chao, ocupado, nav, areas, jams, polis=(), matas=()):
    from PIL import Image, ImageDraw
    xs = [x for x, _ in chao]
    ys = [y for _, y in chao]
    X0, Y0 = min(xs), min(ys)
    W, H = max(xs) - X0 + 1, max(ys) - Y0 + 1
    k = 3 if W * H < 400_000 else 1          # mapa grande: figura em escala 1
    img = Image.new("RGB", (W * k, H * k), (40, 40, 40))
    px = ImageDraw.Draw(img)
    for (x, y), p in chao.items():
        if (x, y) in ocupado:
            cor = (150, 110, 80)
        elif e_rua(p):
            cor = (90, 90, 95)
        elif livre(p):
            cor = (110, 160, 90)
        elif p and p[0].startswith("blends_natural"):
            cor = (60, 110, 55)
        else:
            cor = (170, 170, 160)
        px.rectangle([(x - X0) * k, (y - Y0) * k, (x - X0) * k + k - 1, (y - Y0) * k + k - 1], fill=cor)

    def ret(x, y, w, h, cor, larg):
        px.rectangle([(x - X0) * k, (y - Y0) * k, (x - X0 + w) * k - 1, (y - Y0 + h) * k - 1],
                     outline=cor, width=larg)
    for (x, y, w, h) in matas:
        ret(x, y, w, h, (20, 70, 20), 2)
    for (x, y, w, h) in nav:
        ret(x, y, w, h, (60, 140, 255), 2)
    for i, (pontos, _larg) in enumerate(polis):
        cor = (60, 140, 255) if i % 2 == 0 else (255, 255, 255)
        px.line([((a - X0) * k, (b - Y0) * k) for a, b in pontos], fill=cor, width=max(2, k))
    for (x, y, w, h, _) in jams:
        ret(x, y, w, h, (255, 60, 60), 2)
    cores = {"Forest": (255, 170, 0), "Beach": (255, 240, 120), "Lake": (0, 220, 220)}
    for (x, y, w, h, nome) in areas:
        ret(x, y, w, h, cores.get(nome, (255, 255, 255)), 3)
        px.text(((x - X0) * k + 4, (y - Y0) * k + 4), nome, fill=(0, 0, 0))
    img.save(png)


# ------------------------------------------------- rodovias (linhas com largura)
def picotar_linha(pontos, trecho: int):
    """Divide a linha da rodovia em pedaços de ~`trecho` tiles (uma história cada)."""
    from shapely.geometry import LineString
    from shapely.ops import substring
    g = LineString(pontos)
    n = max(1, int(g.length // trecho))
    passo = g.length / n
    out = []
    for i in range(n):
        s = substring(g, i * passo, (i + 1) * passo)
        out.append([(int(round(x)), int(round(y))) for x, y in s.coords])
    return out


def linha_lua_poli(nome, tipo, pontos, largura):
    pts = ", ".join(f"{x}, {y}" for x, y in pontos)
    return (f'  {{ name = "{nome}", type = "{tipo}", z = 0, geometry = "polyline", '
            f"lineWidth = {largura}, points = {{ {pts} }} }},")


def matas_rurais(pontos, largura, chao, rua, cidade, passo=110, lado=26, n_historia=3):
    """Zonas de mata ("Forest") dos dois lados da rodovia, fora da cidade.

    O jogo pede mata/fazenda a até ~15 tiles do pedaço para as histórias rurais
    (batida com cervo, animal atropelado) e fora da área urbana. Uma em cada
    `n_historia` ganha também uma zona de história de mata (acampamento)."""
    from shapely.geometry import LineString
    g = LineString(pontos)
    matas, historias = [], []
    d, i = passo / 2, 0
    while d < g.length:
        p, q = g.interpolate(d), g.interpolate(min(g.length, d + 1))
        dx, dy = q.x - p.x, q.y - p.y
        n = (dx * dx + dy * dy) ** 0.5 or 1
        nx, ny = -dy / n, dx / n
        for sinal in (1, -1):
            off = largura / 2 + 4 + lado / 2
            cx, cy = p.x + sinal * nx * off, p.y + sinal * ny * off
            x, y = int(cx - lado / 2), int(cy - lado / 2)
            quad = [(a, b) for a in range(x, x + lado) for b in range(y, y + lado)]
            if any(k in rua for k in quad) or any(k not in chao for k in quad):
                continue
            if not all(x + lado + 15 < a or a + c + 15 < x or y + lado + 15 < b or b + e + 15 < y
                       for (a, b, c, e) in cidade):
                continue
            if sum(1 for k in quad if natural(chao[k])) < 0.8 * len(quad):
                continue
            matas.append((x, y, lado, lado))
            if i % n_historia == 0:
                historias.append((x + 5, y + 5, 16, 16, "Forest"))
            i += 1
        d += passo
    return matas, historias


def aplicar(lots: Path, objects: Path, png: Path | None = None, cfg: dict | None = None) -> dict:
    cfg = {**PADRAO, **(cfg or {})}
    chao, ocupado, casas = ler_mapa(lots)
    rua = {k for k, p in chao.items() if e_rua(p) and k not in ocupado}
    nav = []
    if cfg.get("navAuto", True):
        for horizontal in (True, False):
            for r in faixas(rua, horizontal, cfg):
                nav += picotar(r, horizontal, cfg["navTrecho"])
    cidade = zonas_cidade(objects)
    areas = []
    if cfg["historias"]:
        centro = (sum(x for x, _ in rua) // max(1, len(rua)), sum(y for _, y in rua) // max(1, len(rua)))
        areas = escolher_areas(chao, cfg["historias"], cfg["margem"], centro, cidade)
    # Zonas postas pelo gerador onde elas fazem sentido (ex.: "Beach" na areia
    # da praia, U18): [[nome, x, y, largura, altura], ...] em tiles do mundo.
    areas += [(x, y, w, h, nome) for nome, x, y, w, h in cfg.get("areasFixas", [])]
    # Rodovias: zonas de estrada em forma de linha (como as 265 do mapa
    # original), em pedaços, e mata dos lados para as histórias rurais.
    polis, matas = [], []
    for r in cfg.get("navPolilinhas", []):
        for pedaco in picotar_linha(r["pontos"], cfg["navTrecho"]):
            polis.append((pedaco, r["largura"]))
        if cfg.get("matasRurais"):
            m, h = matas_rurais(r["pontos"], r["largura"], chao, rua, cidade)
            matas += m
            areas += h
    jams = []
    if cfg.get("engarrafamento"):
        # a faixa horizontal mais longa vira engarrafamento (duas pistas de 3,
        # trafficjamw / trafficjame), em trechos curtos ENTRE os cruzamentos.
        horiz = [r for r in faixas(rua, True, cfg)]
        if horiz:
            jams = engarrafamento(rua, max(horiz, key=lambda r: r[2]), cfg)
    linhas = [linha_lua("", "Nav", *r) for r in nav]
    linhas += [linha_lua_poli("", "Nav", pts, larg) for pts, larg in polis]
    linhas += [linha_lua("", "Forest", *r) for r in matas]
    linhas += [linha_lua(nome, "ZoneStory", x, y, w, h) for (x, y, w, h, nome) in areas]
    linhas += [linha_lua(nome, "ParkingStall", x, y, w, h) for (x, y, w, h, nome) in jams]
    vagas = vagas_de_rua(rua, cfg) if cfg.get("vagasRua") else []
    linhas += [linha_lua("", "ParkingStall", *v) for v in vagas]
    gravar(objects, linhas)
    if png:
        desenhar(png, chao, ocupado, nav, areas, jams, polis, matas)
    # Conferência: quanto da linha da rodovia cai sobre asfalto de verdade.
    sobre = []
    for pts, _l in polis:
        from shapely.geometry import LineString
        g = LineString(pts)
        amostras = [g.interpolate(t) for t in range(0, int(g.length) + 1, 2)]
        sobre.append(sum(1 for a in amostras if any((int(a.x) + i, int(a.y) + j) in rua
                                                   for i in (-1, 0, 1) for j in (-1, 0, 1))) / len(amostras))
    return {"nav": len(nav), "nav_linhas": len(polis),
            "nav_linhas_sobre_asfalto": round(min(sobre), 2) if sobre else None,
            "matas": len(matas), "historias": [(n, x, y, w, h) for (x, y, w, h, n) in areas],
            "engarrafamento": [(n, x, y, w, h) for (x, y, w, h, n) in jams], "vagas_rua": len(vagas),
            "casas": casas}


if __name__ == "__main__":
    a = sys.argv[1:]
    cfg = json.loads(Path(a[3]).read_text(encoding="utf-8")) if len(a) > 3 else None
    res = aplicar(Path(a[0]), Path(a[1]), Path(a[2]) if len(a) > 2 else None, cfg)
    print(json.dumps(res, ensure_ascii=False, indent=1))
