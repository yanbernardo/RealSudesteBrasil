"""Rodovias de pista dupla a partir do traçado real (peça do gerador; T8d, D-35).

Regras (feedback do usuário no T8d, 08/11/2026):
- Traçado real, mas SUAVIZADO: a 1:15 as curvinhas reais ficam frequentes demais.
  Primeiro tira os detalhes menores que `tolerancia` tiles, depois arredonda as
  quinas (Chaikin), mantendo a direção geral da estrada.
- Pista dupla: duas pistas de mão única, uma por sentido (no Brasil se anda
  pela direita), cada uma com `faixas` faixas largas, e um canteiro no meio.
- Sem calçada (KnoxMap "motorway").
- Guard-rail e mureta de concreto não existem no jogo base: Kit Brasil (Etapa 5).
- As bordas diagonais e as faixas pintadas ainda saem "em degraus" até o nosso
  desenho de curvas (K15, Etapa 2).

Tudo em tiles (y para o norte); `feature`/`proj` vêm do gerador_t7c.
"""
from __future__ import annotations

from shapely.geometry import LineString

PISTA = 10            # largura de cada pista (2 faixas de ~4 + acostamento)
CANTEIRO = 4          # grama entre as pistas
FAIXAS = 2            # faixas por sentido
TOLERANCIA = 20       # tiles (= 300 m reais): detalhe menor que isto some
CHAIKIN = 3           # passadas de arredondamento das quinas


def suavizar(linha: LineString, tolerancia: float = TOLERANCIA, passadas: int = CHAIKIN) -> LineString:
    pts = list(linha.simplify(tolerancia).coords)
    for _ in range(passadas):
        novo = [pts[0]]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            novo.append((0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1))
            novo.append((0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1))
        novo.append(pts[-1])
        pts = novo
    return LineString(pts)


def pista_dupla(eixo: LineString, nome: str, proj, feature,
                pista: int = PISTA, canteiro: int = CANTEIRO, faixas: int = FAIXAS):
    """Duas pistas de mão única dos dois lados do eixo.

    Devolve (desenhos para o KnoxMap, linhas para as zonas de estrada). A pista
    "ida" segue o sentido do eixo, à direita dele; a "volta", à esquerda, no
    sentido contrário."""
    desloc = (pista + canteiro) / 2
    feats, rodovias = [], []
    for lado, sentido in ((-desloc, 1), (desloc, -1)):     # negativo = direita
        linha = eixo.offset_curve(lado, join_style="round")
        coords = list(linha.coords)[::sentido]
        f = feature("motorway", LineString(coords), proj,
                    {"name": nome, "width": str(pista), "lanes": str(faixas), "oneway": "yes"})
        feats.append(f)
        rodovias.append({"coords": f["geometry"]["coordinates"], "largura": pista - 2})
    return feats, rodovias
