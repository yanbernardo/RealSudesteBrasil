"""Baixa da Overpass o que o gerador de cidade (Etapa 2) usa, só no recorte pedido.

Camadas (um JSON cada em <pasta dados>/osm_<nome>/):
- vias: motorway/trunk/primary/secondary/tertiary (+ _link), sem exigir `ref` (G6);
- comercio: lojas e serviços (pontos ou centro do contorno);
- areas: praia, mata, rocha, parque, gramado, cemitério, campo.
As ruas residenciais NÃO são baixadas: o preenchimento é do nosso gerador (D-03).

Uso: python scripts/dados/baixar_osm_cidade.py <pasta dados> <nome> <sul> <oeste> <norte> <leste>
"""
import pathlib
import sys
import time

from baixar_osm_rj import baixar

AMENIDADES = ("pharmacy|bar|pub|restaurant|cafe|fast_food|fuel|police|fire_station|hospital|clinic|doctors|"
              "school|college|university|place_of_worship|bank|marketplace|library|townhall")


def camadas(bb):
    return {
        "vias": f'way["highway"~"^(motorway|trunk|primary|secondary|tertiary)(_link)?$"]{bb};out tags geom;',
        "comercio": f'(nwr["shop"]{bb};nwr["amenity"~"^({AMENIDADES})$"]{bb};);out tags center;',
        "areas": (f'(nwr["natural"~"^(beach|wood|bare_rock|cliff|scrub|sand)$"]{bb};'
                  f'nwr["leisure"~"^(park|pitch|garden|stadium)$"]{bb};'
                  f'nwr["landuse"~"^(forest|grass|cemetery|military)$"]{bb};);out tags geom;'),
        # Lagoas e lagos com o contorno (a relação da Lagoa Rodrigo de Freitas veio
        # sem contorno no lagoas.json da Etapa 1; aqui "out geom" traz as linhas).
        "agua": f'(way["natural"="water"]{bb};relation["natural"="water"]{bb};);out geom;',
    }


if __name__ == "__main__":
    pasta = pathlib.Path(sys.argv[1]) / f"osm_{sys.argv[2]}"
    s, w, n, e = sys.argv[3:7]
    pasta.mkdir(parents=True, exist_ok=True)
    for nome, q in camadas(f"({s},{w},{n},{e})").items():
        for tentativa in range(3):
            try:
                baixar(nome, q, pasta)
                break
            except Exception as erro:  # servidor público: às vezes recusa (429/504)
                print(f"{nome}: falhou ({erro}); tentando de novo em 30 s", flush=True)
                time.sleep(30)
