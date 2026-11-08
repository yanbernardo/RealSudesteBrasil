"""Menu de teleporte do modo debug (D-39): gera o Lua a partir de kits/marcos/teleporte.json.

Converte cada ponto (lat/lon ou nome de localidade) em tile pela grade (D-02), confere se
cai em terra do RJ (avisa se cair no mar) e grava RSB_TeleporteDebug.lua.

Uso (Python do .venv do KnoxMap):
    python -I scripts/gerador/teleporte_debug.py <pasta dados> <pasta saida> [--instalar <pasta do mod>]
O --instalar copia o Lua para <mod>/common/media/lua/client/RSB/ (ex.: um mod de teste).
"""
import argparse
import csv
import json
import pathlib
import shutil
import sys
import unicodedata

from shapely.geometry import Point
from shapely.ops import unary_union

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(AQUI.parent))
sys.path.insert(0, str(AQUI.parent / "dados"))
import grade  # noqa: E402
from leitores import ler_shapefile_zip  # noqa: E402

ORDEM_CAT = ["metropole", "grande", "media", "pequena", "distrito", "vilarejo", "bairro", "so_nome"]

LUA = r'''-- Real Sudeste Brasil: menu de teleporte do modo debug (D-39).
-- Gerado por scripts/gerador/teleporte_debug.py a partir de kits/marcos/teleporte.json. Nao editar a mao.
-- Aparece no menu do botao direito no chao so no modo debug (ou, no servidor, para quem pode usar o menu de debug).

RSB_Teleporte = RSB_Teleporte or {}
RSB_Teleporte.grupos = {
%(grupos)s
}

local function podeUsar(playerObj)
    if isClient() then
        return playerObj and playerObj:getRole() and playerObj:getRole():hasCapability(Capability.UseDebugContextMenu)
    end
    return isDebugEnabled()
end

function RSB_Teleporte.dentroDoMapa(x, y)
    -- mesma conferencia do mapa do jogo (ISWorldMap usa isValidChunk); na B42 o pedaco tem 8 tiles,
    -- mas o mapa do jogo ainda divide por 10: aceita se qualquer das duas contas disser que vale
    local ok, valido = pcall(function()
        local mg = getWorld():getMetaGrid()
        return mg:isValidChunk(math.floor(x / 8), math.floor(y / 8)) or mg:isValidChunk(math.floor(x / 10), math.floor(y / 10))
    end)
    return (not ok) or valido
end

function RSB_Teleporte.ir(_, x, y, z)
    -- igual ao teleporte do proprio menu de debug do jogo (DebugContextMenu.onTeleportValid)
    if isClient() then
        SendCommandToServer("/teleportto " .. x .. "," .. y .. "," .. z)
    else
        getPlayer():teleportTo(x + 0.5, y + 0.5, z)
    end
end

function RSB_Teleporte.menu(player, context, worldobjects, test)
    if test then return end
    local playerObj = getSpecificPlayer(player)
    if not podeUsar(playerObj) then return end
    local opcao = context:addDebugOption("Real Sudeste Brasil: teleporte", worldobjects, nil)
    local sub = ISContextMenu:getNew(context)
    context:addSubMenu(opcao, sub)
    for _, g in ipairs(RSB_Teleporte.grupos) do
        local og = sub:addOption(g.nome, worldobjects, nil)
        local subg = ISContextMenu:getNew(sub)
        sub:addSubMenu(og, subg)
        for _, p in ipairs(g.pontos) do
            local op = subg:addOption(p[1], worldobjects, RSB_Teleporte.ir, p[2], p[3], p[4])
            if not RSB_Teleporte.dentroDoMapa(p[2], p[3]) then
                -- ponto fora das celulas carregadas (ex.: mapa de teste pequeno): nao manda para o vazio
                op.notAvailable = true
                local dica = ISToolTip:new()
                dica:initialise()
                dica:setVisible(false)
                dica.description = "Fora do mapa carregado (esta parte do Sudeste ainda nao existe neste mod)."
                op.toolTip = dica
            end
        end
    end
end

Events.OnFillWorldObjectContextMenu.Add(RSB_Teleporte.menu)
'''


def chave(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dados")
    ap.add_argument("saida")
    ap.add_argument("--instalar")
    a = ap.parse_args()
    dados, saida = pathlib.Path(a.dados), pathlib.Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)

    kit = json.load(open(RAIZ / "kits/marcos/teleporte.json", encoding="utf-8"))
    locs = list(csv.DictReader(open(saida.parent / "etapa1_rj/localidades_rj.csv", encoding="utf-8")))
    rj = unary_union([g for _, g in ler_shapefile_zip(dados / "ibge/municipios_rj/RJ_Municipios_2024.zip")])

    blocos, avisos, total = [], [], 0
    for g in kit["grupos"]:
        linhas = []
        for p in g["pontos"]:
            if "localidade" in p:
                cand = [r for r in locs if chave(r["nome"]) == chave(p["localidade"])
                        and ("municipio" not in p or chave(r["municipio"]) == chave(p["municipio"]))]
                if not cand:
                    avisos.append(f"nao achei a localidade '{p['localidade']}'")
                    continue
                r = min(cand, key=lambda r: ORDEM_CAT.index(r["categoria"]))
                tx, ty = int(r["tile_x"]), int(r["tile_y"])
                lat, lon = grade.tile_para_latlon(tx + 0.5, ty + 0.5)
                nome = p.get("nome", r["nome"])
            else:
                lat, lon = p["lat"], p["lon"]
                tx, ty = grade.latlon_para_tile(lat, lon)
                nome = p["nome"]
            nome = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()  # menu so com ASCII
            if "Outros estados" not in g["grupo"] and not rj.contains(Point(lon, lat)):
                avisos.append(f"'{nome}' cai fora da terra do RJ (mar?) em {lat:.4f},{lon:.4f}")
            cx, cy = grade.celula(tx, ty)
            rotulo = f"{nome} (celula {cx},{cy})"
            linhas.append(f'        {{"{rotulo}", {tx}, {ty}, 0}},')
            total += 1
        blocos.append(f'    {{ nome = "{g["grupo"]}", pontos = {{\n' + "\n".join(linhas) + "\n    }},")

    lua = LUA % {"grupos": "\n".join(blocos)}
    arq = saida / "RSB_TeleporteDebug.lua"
    arq.write_text(lua, encoding="utf-8")
    print(f"{arq}: {total} pontos em {len(blocos)} grupos")
    for av in avisos:
        print("AVISO:", av)
    if a.instalar:
        destino = pathlib.Path(a.instalar) / "common/media/lua/client/RSB"
        destino.mkdir(parents=True, exist_ok=True)
        shutil.copy(arq, destino / arq.name)
        print("Instalado em", destino / arq.name)


if __name__ == "__main__":
    main()
