# Prompt para a próxima instância (atualizado em 09/11/2026)

## Novo desde 08/11/2026 (sessão "Etapa 2.2 – zonas de estrada nas diagonais")
Leia também `KIT_BRASIL_LISTA.md` e, em `PROBLEMAS_CONHECIDOS.md`, K37 a K40, U43 e U44; decisão nova D-45.
- **Instalado no Rio piloto, sem teste em jogo:** zonas de estrada nas avenidas diagonais (U43); calçadão de Copacabana em pedra portuguesa (D-45; grupo TESTE do teleporte: "Calcadao de Copacabana - meio / troca de direcao / perto do Leme"); Kit Brasil (404 peças, 11 folhas). Ao testar: jogo novo, só o mod `rsb_rio_piloto` ativo.
- **Kit Brasil:** folhas em `kits/tiles/` (cada uma com `.json`: peças, propriedades, entradas do BuildingEd e grupos de móveis). Geradores: `calcadao.py`, `kit_favela.py` (paredes limpas e desgastadas, pisos, escadas), `kit_laje.py` (lajes, muretas, objetos), `kit_muros.py`, `kit_desgaste.py` (sujeira que sai com limpeza: nome com "overlay_grime"; desgaste fixo), texturas em `texturas_favela.py`. `kit_tiles.py` empacota tudo e registra no BuildingEd (Kit Brasil primeiro nas listas e em grupos de móveis "Kit Brasil - ..."; cópia original dos arquivos de config em `.antes_rsb`). O pipeline empacota e instala sozinho quando o config tem `"calcadao"`.
- **Pedidos do usuário a lembrar:** favela tem laje plana (não fazer telha inclinada para favela); evitar desenhos grandes que repetem em todo tile (usar peças avulsas ou variações, K39); ele escolhe a ordem dos grupos do Kit Brasil; o lugar da assinatura do KnoxMap é escolha dele (D-37).
- **Próximos passos:** o usuário testar em jogo o que está instalado; escolher o próximo grupo do Kit Brasil; escolher o lugar da assinatura; teste do Viewpoint (T5a) com as peças novas, só com autorização.

---

## Texto anterior (08/11/2026)

Leia primeiro `AGENTS.md`, `PLANO_BRASIL_ZOMBOID.md` (as decisões D-41 a D-44 são as mais novas) e `PROBLEMAS_CONHECIDOS.md` (U18 a U42, J4, K35, K36).

Regras de trabalho: o usuário não programa; explique em português simples. **Feche o jogo antes de instalar o mapa** (J4: instalar com o jogo aberto quebra o mapa). Só instale quando ele pedir; use `--sem-instalar` do `knoxmap_pipeline.py` para compilar sem instalar. Todo local novo a testar entra no grupo TESTE do teleporte debug (`kits/marcos/teleporte.json`) até o OK dele.

## Estado do Rio piloto (`rsb_rio_piloto`, Centro + Zona Sul)
Feito e aprovado pelo usuário em jogo: legenda do mapa como a original (D-42), visão de satélite (D-41), ruas internas moldadas em trechos retos com calçada e avenidas no traçado real (D-43), ruas soltas ligadas (túneis), orla sem casas, quadra de vôlei na areia, quartel de Louisville, delegacias copiadas com estacionamento.

## Instalado em 08/11/2026 (jogo fechado), ainda sem feedback do usuário em jogo
- Praias de Flamengo, Botafogo e Vermelha (D-44) e ponta de areia afinando em todas as praias (U42).
- Quadra de vôlei com contorno de linhas brancas.
- Meios-tiles em triângulo nas diagonais desligados (`semCalcadaDiagonal` falso): o usuário não gostou; avenida diagonal fica com calçada em degraus até o Kit Brasil.
- Casa de laje de exemplo removida do mapa (U40).

Para instalar de novo no futuro: o usuário fecha o jogo; regere o desenho com `scripts/gerador/cidade.py <KnoxMap> dados kits/cidades/rio_piloto.json scripts/testes/rio_piloto.json saida/rio_piloto/desenho.png`; rode `scripts/knoxmap_pipeline.py <KnoxMap> scripts/testes/rio_piloto.json` (sem `--sem-instalar`); depois `scripts/gerador/teleporte_debug.py dados saida/teleporte --instalar <pasta do mod>`. Tudo com o Python do `.venv` do KnoxMap, `-I`.

## Pedidos e observações do usuário a lembrar
1. **Todas as praias com areia na vida real** do Rio devem ter faixa de areia (D-44). Copacabana foi só o teste. Ao gerar o RJ inteiro, tirar as praias dos dados (OSM `natural=beach`), não só dos pontos escritos no kit.
2. **Túneis:** as ruas hoje só ligadas (`ligar_ilhas` em `cidade.py`) devem virar túneis de concreto de verdade no acabamento final (Etapa 5).
3. **Ruas que acabam em morro:** serão tratadas com o Terrain Relief do Viewpoint (Etapa 2.7); lembrar o usuário disso sempre que o assunto voltar.
4. **Estacionamento das delegacias copiadas sem saída** (U41): na versão definitiva (delegacia da Polícia Militar feita pelo usuário), reservar a saída do estacionamento e ligá-la à rua com rampa de concreto; não gerar lote em frente à saída.
5. **Casas e comércios brasileiros:** o usuário os faz no BuildingEd (`GUIA_CONSTRUCOES_BRASILEIRAS.md`: lista, direções, fotos). O script `predio_desenhado.py` não serve para casas (paredes invisíveis por dentro, U40). Ele quer variar só a cor das paredes (fora e dentro) e a decoração de parede (plantas, quadros, fotos) por sorteio em script: ver a resposta dada na conversa (troca de peças no `.tbx`).
6. O hotel inspirado no Copacabana Palace (`kits/marcos/hotel_atlantida*.tbx`) saiu do mapa; o usuário vai reformá-lo.
7. O teste do Viewpoint (T5a) ainda não foi feito: o mod não está instalado no notebook, e não instalar sem autorização.
8. O usuário disse que a pista em degraus é melhor que a com triângulos; não reintroduzir triângulos.

## Próximos passos sugeridos
Zonas de estrada nas avenidas diagonais (histórias de carro); assinatura do KnoxMap uma vez só (D-37); a 3ª delegacia do Rio piloto ficou genérica (não coube nenhuma cópia); estacionamentos e calçadão de Copacabana (peça nova do Kit Brasil, que passa pelo caminho TileSetZ → Viewpoint).
