"""Baixa da Overpass so o que o mapa-guia do RJ usa (Etapa 1).

Grava um JSON por camada em dados/osm_rj/. Nao baixa de novo o que ja existe.
Uso: python scripts/dados/baixar_osm_rj.py <pasta dados>
"""
import gzip
import pathlib
import sys
import time
import urllib.parse
import urllib.request

URL = "https://overpass-api.de/api/interpreter"
AREA = 'area["ISO3166-2"="BR-RJ"]->.a;'
# Retangulo com folga em volta do RJ (costa e rios cruzam a divisa)
BBOX = "(-23.45,-45.00,-20.70,-40.90)"

CAMADAS = {
    # Atencao (G5): varias consultas seguidas precisam de "( ... );" em volta, senao so a ultima sai
    "rodovias": AREA + '(way["highway"~"^(motorway|trunk)(_link)?$"](area.a);'
                       'way["highway"~"^(primary|secondary)$"]["ref"](area.a););out tags geom;',
    "rios": AREA + 'way["waterway"="river"](area.a);out tags geom;',
    "costa": 'way["natural"="coastline"]' + BBOX + ';out geom;',
    "lagoas": AREA + '(way["natural"="water"]["water"~"^(lagoon|lake|reservoir)$"](area.a);'
                     'relation["natural"="water"]["water"~"^(lagoon|lake|reservoir)$"](area.a););out tags geom;',
    "lugares": AREA + 'node["place"~"^(city|town|village|hamlet|suburb|quarter|neighbourhood|locality|isolated_dwelling)$"](area.a);out;',
    "turismo": AREA + '(nwr["tourism"~"^(guest_house|hotel|hostel|chalet|camp_site|motel)$"](area.a);'
                      'node["waterway"="waterfall"](area.a);'
                      'nwr["natural"="beach"]["name"](area.a););out tags center;',
}


def baixar(nome, q, pasta):
    alvo = pasta / f"{nome}.json"
    if alvo.exists() and alvo.stat().st_size > 100:
        print(f"{nome}: ja existe ({alvo.stat().st_size/1e6:.1f} MB)")
        return
    corpo = urllib.parse.urlencode({"data": "[out:json][timeout:300];" + q}).encode()
    req = urllib.request.Request(URL, data=corpo, headers={
        "User-Agent": "RealSudesteBrasil-mapa/0.1", "Accept-Encoding": "gzip"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        dados = r.read()
        recebido = len(dados)
        if r.headers.get("Content-Encoding") == "gzip":
            dados = gzip.decompress(dados)
    alvo.write_bytes(dados)
    print(f"{nome}: {recebido/1e6:.1f} MB pela rede, {len(dados)/1e6:.1f} MB no disco, {time.time()-t:.0f} s")


if __name__ == "__main__":
    pasta = pathlib.Path(sys.argv[1]) / "osm_rj"
    pasta.mkdir(parents=True, exist_ok=True)
    for nome, q in CAMADAS.items():
        for tentativa in range(3):
            try:
                baixar(nome, q, pasta)
                break
            except Exception as e:  # servidor publico: as vezes recusa (429/504)
                print(f"{nome}: falhou ({e}); tentando de novo em 30 s")
                time.sleep(30)
