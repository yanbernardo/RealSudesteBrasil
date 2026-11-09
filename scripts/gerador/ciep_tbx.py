"""CIEP ("Brizolão") desenhado à mão para o BuildingEd (pedido do usuário, 09/11/2026).

Bloco de 36 x 14 tiles, 3 andares, frente para o sul, como os CIEPs das fotos
(Cascadura, Belford Roxo, Mesquita): corredor no meio, cômodos dos dois lados,
térreo com cozinha, refeitório, consultório, secretaria, diretoria, sala dos
professores e um pátio coberto que abre para a rua por 5 arcos com portão de
grade; 1º e 2º andares com salas de aula (carteira universitária e quadro
verde), banheiros e biblioteca; escada no meio; laje com caixa d'água.
Peças: Kit Brasil (CIEP, casa de laje, botequim, laje) e móveis do jogo (mesa,
fogão, geladeira, pia, vaso, estante), que dão o loot certo pelo nome do cômodo.

Uso: python -I -X utf8 ciep_tbx.py <saída.tbx> [prévia.png] [pasta Tiles/2x]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tbx_mao import Predio  # noqa: E402

W, H, ANDARES = 36, 14, 3


def pecas8(folha, b):
    n = lambda i: f"{folha}_{i:03d}"
    return {"West": n(b), "North": n(b + 1), "NorthWest": n(b + 2), "SouthEast": n(b + 3),
            "WestWindow": n(b + 8), "NorthWindow": n(b + 9), "WestDoor": n(b + 10), "NorthDoor": n(b + 11)}


# móveis do jogo (mesmos nomes de peça do catálogo do KnoxMap; orient = lado das costas)
JOGO = {
    "mesa": {"W": {"0,0": "location_business_office_generic_01_001", "0,1": "location_business_office_generic_01_000"},
             "N": {"0,0": "location_business_office_generic_01_005", "1,0": "location_business_office_generic_01_006"},
             "E": {"0,0": "location_business_office_generic_01_014", "0,1": "location_business_office_generic_01_013"},
             "S": {"0,0": "location_business_office_generic_01_008", "1,0": "location_business_office_generic_01_010"}},
    "cadeira_escritorio": {"W": {"0,0": "furniture_seating_indoor_01_049"}, "N": {"0,0": "furniture_seating_indoor_01_050"},
                           "E": {"0,0": "furniture_seating_indoor_01_048"}, "S": {"0,0": "furniture_seating_indoor_01_051"}},
    "balcao": {"W": {"0,0": "fixtures_counters_01_003"}, "N": {"0,0": "fixtures_counters_01_005"},
               "E": {"0,0": "fixtures_counters_01_007"}, "S": {"0,0": "fixtures_counters_01_001"}},
    "fogao": {"W": {"0,0": "appliances_cooking_01_000"}, "N": {"0,0": "appliances_cooking_01_001"},
              "E": {"0,0": "appliances_cooking_01_002"}, "S": {"0,0": "appliances_cooking_01_003"}},
    "geladeira": {"W": {"0,0": "appliances_refrigeration_01_001"}, "N": {"0,0": "appliances_refrigeration_01_000"},
                  "E": {"0,0": "appliances_refrigeration_01_003"}, "S": {"0,0": "appliances_refrigeration_01_002"}},
    "pia_cozinha": {"W": {"0,0": "fixtures_sinks_01_004"}, "N": {"0,0": "fixtures_sinks_01_005"},
                    "E": {"0,0": "fixtures_sinks_01_006"}, "S": {"0,0": "fixtures_sinks_01_007"}},
    "vaso": {"W": {"0,0": "fixtures_bathroom_01_001"}, "N": {"0,0": "fixtures_bathroom_01_000"},
             "E": {"0,0": "fixtures_bathroom_01_002"}, "S": {"0,0": "fixtures_bathroom_01_003"}},
    "pia_banheiro": {"N": {"0,0": "fixtures_sinks_01_012"}, "W": {"0,0": "fixtures_sinks_01_013"},
                     "E": {"0,0": "fixtures_sinks_01_029"}, "S": {"0,0": "fixtures_sinks_01_028"}},
    "estante": {"W": {"0,0": "furniture_shelving_01_041"}, "N": {"0,0": "furniture_shelving_01_040"},
                "E": {"0,0": "furniture_shelving_01_042"}, "S": {"0,0": "furniture_shelving_01_043"}},
    "prateleira": {"W": {"0,0": "furniture_shelving_01_002"}, "N": {"0,0": "furniture_shelving_01_001"},
                   "E": {"0,0": "furniture_shelving_01_003"}, "S": {"0,0": "furniture_shelving_01_004"}},
    "mesa_refeitorio": {"W": {"0,0": "furniture_tables_high_01_000", "1,0": "furniture_tables_high_01_001"},
                        "N": {"0,0": "furniture_tables_high_01_003", "0,1": "furniture_tables_high_01_002"}},
    "cadeira": {"W": {"0,0": "furniture_seating_indoor_02_004"}, "N": {"0,0": "furniture_seating_indoor_02_005"},
                "E": {"0,0": "furniture_seating_indoor_02_006"}, "S": {"0,0": "furniture_seating_indoor_02_007"}},
}
OB = "rsb_objetos_ciep_01"
NOSSOS = {
    # orient = costas: costas a leste = virada para oeste (peça "_o"), etc.
    "carteira": ({"W": {"0,0": f"{OB}_001"}, "N": {"0,0": f"{OB}_000"}, "E": {"0,0": f"{OB}_003"}, "S": {"0,0": f"{OB}_002"}}, "Furniture"),
    "bebedouro": ({"W": {"0,0": f"{OB}_005"}, "N": {"0,0": f"{OB}_004"}}, "Furniture"),
    "quadro": ({"W": {"0,0": f"{OB}_011", "0,1": f"{OB}_010"}, "N": {"0,0": f"{OB}_006", "1,0": f"{OB}_007"}}, "WallFurniture"),
    "caixa_dagua": ({o: {"0,0": "rsb_objetos_laje_01_000"} for o in "WNES"}, "Furniture"),
}


def montar() -> Predio:
    p = Predio(W, H, ANDARES)
    E = p.entrada
    ext_pecas = pecas8("rsb_paredes_ciep_01", 4)                          # peitoril vermelho e faixa amarela
    ext_pecas.update({"WestWindow1": "rsb_paredes_ciep_01_052", "NorthWindow1": "rsb_paredes_ciep_01_053",
                      "WestWindow2": "rsb_paredes_ciep_01_054", "NorthWindow2": "rsb_paredes_ciep_01_055"})
    ext = E("exterior_walls", ext_pecas)
    porta = E("doors", {"West": "fixtures_doors_01_000", "North": "fixtures_doors_01_001",
                        "WestOpen": "fixtures_doors_01_002", "NorthOpen": "fixtures_doors_01_003"})
    moldura = E("door_frames", {"West": "fixtures_doors_frames_01_000", "North": "fixtures_doors_frames_01_001"})
    janela = E("windows", {"West": "fixtures_windows_01_000", "North": "fixtures_windows_01_001"})
    # janela larga do CIEP (2 tiles): metade 1 no tile de x/y menor, metade 2 no seguinte
    larga1 = E("windows", {"West": "rsb_janelas_ciep_01_000", "North": "rsb_janelas_ciep_01_001"})
    larga2 = E("windows", {"West": "rsb_janelas_ciep_01_002", "North": "rsb_janelas_ciep_01_003"})
    p.formas = {larga1: "1", larga2: "2"}
    escada = E("stairs", {"West1": "fixtures_stairs_01_000", "West2": "fixtures_stairs_01_001", "West3": "fixtures_stairs_01_002",
                          "North1": "fixtures_stairs_01_008", "North2": "fixtures_stairs_01_009", "North3": "fixtures_stairs_01_010"})
    int_verde = E("interior_walls", pecas8("rsb_paredes_ciep_01", 20))
    int_azul = E("interior_walls", pecas8("rsb_paredes_ciep_01", 32))
    int_azulejo = E("interior_walls", pecas8("rsb_paredes_botequim_01", 4))
    pav_bege = E("floors", {"Floor": "rsb_pisos_ciep_01_000"})
    pav_cinza = E("floors", {"Floor": "rsb_pisos_ciep_01_001"})
    cim_patio = E("floors", {"Floor": "rsb_pisos_ciep_01_002"})
    granilite = E("floors", {"Floor": "rsb_pisos_botequim_01_002"})
    ceramica = E("floors", {"Floor": "rsb_pisos_casa_01_003"})
    topo = E("roof_tops", {k: "rsb_lajes_01_000" for k in ("West1", "West2", "West3", "North1", "North2", "North3")})
    cap = E("roof_caps", {"CapRiseE1": "walls_exterior_roofs_01_096", "CapRiseE2": "walls_exterior_roofs_01_097",
                          "CapRiseE3": "walls_exterior_roofs_01_098", "CapFallE1": "walls_exterior_roofs_01_104",
                          "CapFallE2": "walls_exterior_roofs_01_105", "CapFallE3": "walls_exterior_roofs_01_106",
                          "CapRiseS1": "walls_exterior_roofs_01_109", "CapRiseS2": "walls_exterior_roofs_01_108",
                          "CapRiseS3": "walls_exterior_roofs_01_107", "CapFallS1": "walls_exterior_roofs_01_101",
                          "CapFallS2": "walls_exterior_roofs_01_100", "CapFallS3": "walls_exterior_roofs_01_099"})
    slope = E("roof_slopes", {"SlopeS1": "roofs_01_000", "SlopeS2": "roofs_01_001", "SlopeS3": "roofs_01_002",
                              "SlopeE1": "roofs_01_005", "SlopeE2": "roofs_01_004", "SlopeE3": "roofs_01_003"})
    forro = E("ceiling", {"Ceiling": "ceilings_01_000"})
    portao = E("doors", {"West": "rsb_portoes_casa_01_000", "North": "rsb_portoes_casa_01_001",
                         "WestOpen": "rsb_portoes_casa_01_002", "NorthOpen": "rsb_portoes_casa_01_003"})
    p.attrs = {"ExteriorWall": ext, "ExteriorWallTrim": 0, "Door": porta, "DoorFrame": moldura, "Window": janela,
               "Curtains": 0, "Shutters": 0, "Stairs": escada, "RoofCap": cap, "RoofSlope": slope, "RoofTop": topo,
               "GrimeWall": 0}

    M = {k: p.movel(k, v) for k, v in JOGO.items()}
    M.update({k: p.movel(k, v, c) for k, (v, c) in NOSSOS.items()})

    def com(nome, cor, parede, piso):
        return p.comodo(nome, cor, parede, piso, forro)
    CORES = {"classroom": "124 133 52", "hall": "37 228 228", "kitchen": "220 140 60", "cafeteria": "230 190 80",
             "bathroom": "60 120 220", "medical": "230 80 80", "office": "150 90 200", "schoolstorage": "120 120 120",
             "storage": "110 110 110", "library": "120 70 30"}

    def sala(nivel, nome, x, y, w, h, parede=int_verde, piso=pav_bege):
        c = com(nome, CORES[nome], parede, piso)
        p.sala(nivel, c, x, y, w, h)
        return (x, y, w, h)

    def par(nivel, x, y, d):
        p.janela(nivel, x, y, d, larga1)
        p.janela(nivel, x + (d == "N"), y + (d == "W"), d, larga2)

    def janelas_fachada(nivel, salas_norte, salas_sul, pular=()):
        """Janelas largas aos pares, a cada 3 tiles, sem passar da sala (a parede interna encosta ali)."""
        for (x, y, w, h) in salas_norte:
            for xx in range(x + 1, x + w - 1, 3):
                par(nivel, xx, 0, "N")
        for (x, y, w, h) in salas_sul:
            for xx in range(x + 1, x + w - 1, 3):
                if xx not in pular and xx + 1 not in pular:
                    par(nivel, xx, H, "N")

    # ------------------------------------------------ térreo
    n0 = [sala(0, "kitchen", 0, 0, 8, 6, int_azulejo, ceramica), sala(0, "cafeteria", 8, 0, 12, 6, int_verde, granilite),
          sala(0, "storage", 20, 0, 3, 6, int_azulejo, ceramica), sala(0, "hall", 23, 0, 4, 6, int_verde, granilite),
          sala(0, "bathroom", 27, 0, 4, 6, int_azulejo, ceramica), sala(0, "medical", 31, 0, 5, 6, int_azul, pav_cinza)]
    sala(0, "hall", 0, 6, W, 2, int_verde, granilite)                     # corredor
    s0 = [sala(0, "office", 0, 8, 6, 6, int_azul, pav_cinza), sala(0, "office", 6, 8, 4, 6, int_azul, pav_cinza),
          sala(0, "hall", 10, 8, 16, 6, int_verde, cim_patio),            # pátio coberto
          sala(0, "office", 26, 8, 5, 6, int_azul, pav_cinza), sala(0, "schoolstorage", 31, 8, 5, 6, int_verde, pav_cinza)]
    janelas_fachada(0, [n0[0], n0[1], n0[4], n0[5]], [s0[0], s0[1], s0[3], s0[4]], pular=(8, 9))
    for xx in (11, 14, 17, 20, 23):                                        # arcos do pátio, com portão de grade
        p.porta(0, xx, H, "N", portao, 0)
    for (x, y, w, h) in n0:
        p.porta(0, x + w // 2, 6, "N", porta, moldura)
    for (x, y, w, h) in s0:
        if w < 16:
            p.porta(0, x + w // 2, 8, "N", porta, moldura)
    for xx in (12, 18, 24):                                                 # pátio aberto para o corredor
        p.porta(0, xx, 8, "N", porta, moldura)
    p.porta(0, 0, 6, "W", porta, moldura)
    p.porta(0, W, 7, "W", porta, moldura)
    p.porta(0, 3, 0, "N", porta, moldura)                                   # porta de serviço da cozinha
    for y in (2, 10):
        par(0, 0, y, "W")
        par(0, W, y, "W")
    p.escada(0, 24, 1, "N", escada)
    # cozinha
    for x in range(1, 7):
        p.mob(0, M["balcao"], x, 0, "N")
    p.mob(0, M["fogao"], 2, 0, "N"); p.mob(0, M["fogao"], 3, 1, "N")
    p.mob(0, M["pia_cozinha"], 5, 0, "N"); p.mob(0, M["geladeira"], 7, 0, "N"); p.mob(0, M["geladeira"], 7, 1, "E")
    # refeitório
    for x in (9, 12, 15):
        for y in (1, 3):
            p.mob(0, M["mesa_refeitorio"], x, y, "W")
            p.mob(0, M["cadeira"], x, y - 1 if y == 1 else y + 1, "N" if y == 1 else "S")
            p.mob(0, M["cadeira"], x + 1, y - 1 if y == 1 else y + 1, "N" if y == 1 else "S")
    # despensa e almoxarifado
    for y in range(0, 5):
        p.mob(0, M["prateleira"], 22, y, "E")
    for x in range(31, 36):
        p.mob(0, M["prateleira"], x, 13, "S")
    # banheiro
    for x in (27, 28, 29, 30):
        p.mob(0, M["vaso"], x, 0, "N")
    p.mob(0, M["pia_banheiro"], 28, 5, "S"); p.mob(0, M["pia_banheiro"], 29, 5, "S")
    # consultório, secretaria, diretoria, professores
    for (x, y) in ((32, 2), (1, 10), (7, 10), (27, 10)):
        p.mob(0, M["mesa"], x, y, "N")
        p.mob(0, M["cadeira_escritorio"], x, y + 1, "S")
    for (x, y, o) in ((35, 0, "N"), (0, 13, "S"), (4, 13, "S"), (30, 13, "S")):
        p.mob(0, M["estante"], x, y, o)
    p.mob(0, M["bebedouro"], 30, 6, "N")
    # letreiro na fachada, sobre a diretoria (sem janela em x = 9)
    p.peca_parede(0, 8, H, f"{OB}_008")
    p.peca_parede(0, 9, H, f"{OB}_009")

    # ------------------------------------------------ 1º e 2º andares
    for nivel in (1, 2):
        norte = [sala(nivel, "library" if nivel == 2 else "classroom", 0, 0, 8, 6, int_verde, pav_cinza if nivel == 2 else pav_bege),
                 sala(nivel, "classroom", 8, 0, 8, 6), sala(nivel, "classroom", 16, 0, 7, 6),
                 sala(nivel, "hall", 23, 0, 4, 6, int_verde, granilite),
                 sala(nivel, "bathroom", 27, 0, 4, 6, int_azulejo, ceramica),
                 sala(nivel, "classroom", 31, 0, 5, 6, int_azul)]
        sala(nivel, "hall", 0, 6, W, 2, int_verde, granilite)
        sul = [sala(nivel, "classroom", x, 8, 9, 6, int_azul if i % 2 else int_verde) for i, x in enumerate((0, 9, 18, 27))]
        janelas_fachada(nivel, norte, sul)
        for y in (2, 6, 10):
            par(nivel, 0, y, "W")
            par(nivel, W, y, "W")
        for (x, y, w, h) in norte:
            p.porta(nivel, x + w - 2, 6, "N", porta, moldura)
        for (x, y, w, h) in sul:
            p.porta(nivel, x + w - 2, 8, "N", porta, moldura)
        if nivel == 1:
            p.escada(1, 24, 1, "N", escada)
        p.mob(nivel, M["bebedouro"], 30, 6, "N")
        for x in (27, 28, 29, 30):
            p.mob(nivel, M["vaso"], x, 0, "N")
        p.mob(nivel, M["pia_banheiro"], 28, 5, "S"); p.mob(nivel, M["pia_banheiro"], 29, 5, "S")
        salas = [r for r in norte if r[0] not in (23, 27)] + sul
        for (x, y, w, h) in salas:
            if nivel == 2 and (x, y) == (0, 0):                            # biblioteca
                for xx in range(1, 7):
                    p.mob(nivel, M["estante"], xx, 0, "N")
                for xx in (2, 5):
                    p.mob(nivel, M["mesa_refeitorio"], xx, 3, "W")
                continue
            # quadro na parede oeste da sala; carteiras viradas para ele (costas a leste)
            p.mob(nivel, M["quadro"], x, y + 2, "W")
            p.mob(nivel, M["mesa"], x + 1, y + 1, "E")
            fileiras = [r for r in range(y + 1, y + h - 1)]
            for cx in range(x + 3, x + w - 1):
                for cy in fileiras:
                    if (cx - x) % 2 == 1 or w <= 5:
                        p.mob(nivel, M["carteira"], cx, cy, "E")

    # ------------------------------------------------ laje e caixa d'água
    p.laje(2, 0, 0, W, H, topo, cap, slope)
    p.mob(3, M["caixa_dagua"], 24, 3, "N")
    p.mob(3, M["caixa_dagua"], 12, 3, "N")
    return p


# ---------------------------------------------------------------- prévia (imagem isométrica)
def previa(p: Predio, tiles2x: Path, kit: Path, destino: Path) -> None:
    from PIL import Image
    cache = {}

    def peca(nome):
        if nome not in cache:
            folha, i = nome.rsplit("_", 1)
            arq = kit / f"{folha}.png" if folha.startswith("rsb_") else tiles2x / f"{folha}.png"
            im = cache.setdefault(("f", folha), Image.open(arq).convert("RGBA")) if ("f", folha) not in cache else cache[("f", folha)]
            i = int(i)
            cache[nome] = im.crop(((i % 8) * 128, (i // 8) * 256, (i % 8) * 128 + 128, (i // 8) * 256 + 256))
        return cache[nome]
    ent = {i + 1: t for i, (_c, t) in enumerate(p.entradas)}
    ext = ent[p.attrs["ExteriorWall"]]
    img = Image.new("RGBA", ((W + H) * 64 + 128, (W + H) * 32 + 4 * 192 + 300), (96, 112, 92, 255))
    ox, oy = H * 64, 4 * 192 + 40
    camadas = {}

    def add(z, x, y, ordem, im):
        camadas.setdefault((z, x + y, x, ordem), []).append(im)
    import re
    for z, nv in enumerate(p.niveis):
        g = nv["grade"]
        objs = [dict(re.findall(r'(\w+)="([^"]*)"', a)) for _t, a in nv["obj"]]
        portas = {(int(o["x"]), int(o["y"]), o["dir"]): o for o in objs if o["type"] == "door"}
        janelas = {(int(o["x"]), int(o["y"]), o["dir"]): o for o in objs if o["type"] == "window"}
        cel = lambda x, y: g[y][x] if 0 <= x < W and 0 <= y < H else 0
        furos = set()
        if z > 0:
            for o in [dict(re.findall(r'(\w+)="([^"]*)"', a)) for _t, a in p.niveis[z - 1]["obj"]]:
                if o["type"] == "stairs":
                    furos |= {(int(o["x"]), int(o["y"]) + k) for k in range(3)}
        for y in range(H + 1):
            for x in range(W + 1):
                c = cel(x, y)
                if c and (x, y) not in furos:
                    add(z, x, y, 0, peca(ent[p.comodos[c - 1]["Floor"]]["Floor"]))
                for d, viz in (("W", cel(x - 1, y)), ("N", cel(x, y - 1))):
                    if viz == c:
                        continue
                    estilo = ext if (viz == 0 or c == 0) else ent[p.comodos[c - 1]["InteriorWall"]]
                    base = "West" if d == "W" else "North"
                    papel = base + ("Door" if (x, y, d) in portas else "Window" if (x, y, d) in janelas else "")
                    if (x, y, d) in janelas and (viz == 0 or c == 0):
                        papel += getattr(p, "formas", {}).get(int(janelas[(x, y, d)]["Tile"]), "")
                    add(z, x, y, 1, peca(estilo[papel]))
                    if (x, y, d) in portas:
                        add(z, x, y, 2, peca(ent[int(portas[(x, y, d)]["Tile"])][base]))
                    if (x, y, d) in janelas:
                        add(z, x, y, 2, peca(ent[int(janelas[(x, y, d)]["Tile"])][base]))
        for o in objs:
            if o["type"] == "furniture":
                _n, _c, ors = p.moveis[int(o["FurnitureTiles"])]
                for k, nome in ors[o["orient"]].items():
                    dx, dy = map(int, k.split(","))
                    add(z, int(o["x"]) + dx, int(o["y"]) + dy, 3, peca(nome))
            elif o["type"] == "stairs":
                for k in range(3):
                    add(z, int(o["x"]), int(o["y"]) + k, 3, peca(ent[int(o["Tile"])][f"North{k + 1}"]))
            elif o["type"] == "roof":
                for yy in range(int(o["y"]), int(o["y"]) + int(o["height"])):
                    for xx in range(int(o["x"]), int(o["x"]) + int(o["width"])):
                        add(z + 1, xx, yy, 0, peca(ent[int(o["TopTiles"])]["West1"]))
        for (x, y), nome in nv["user"].items():
            add(z, x, y, 4, peca(nome))
    for k in sorted(camadas):
        z, _s, x, _o = k
        y = k[1] - x
        for im in camadas[k]:
            img.alpha_composite(im, (ox + (x - y) * 64, oy + (x + y) * 32 - z * 192))
    img.convert("RGB").save(destino)


if __name__ == "__main__":
    p = montar()
    saida = Path(sys.argv[1])
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(p.texto(), encoding="utf-8")
    print("gravado", saida, len(p.comodos), "cômodos")
    if len(sys.argv) > 3:
        raiz = Path(__file__).resolve().parents[2]
        previa(p, Path(sys.argv[3]), raiz / "kits" / "tiles", Path(sys.argv[2]))
        print("prévia", sys.argv[2])
