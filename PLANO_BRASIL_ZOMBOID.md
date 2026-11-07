# Plano mestre: Real Sudeste Brasil (mod de mapa para Project Zomboid)

> **Claude, comece por aqui. Este arquivo é a memória do projeto.**
>
> 1. Em cada sessão, leia só a seção 1 (Estado atual) e a etapa em andamento (seção 7). O resto só quando precisar.
> 2. Nunca mude uma decisão marcada como DECIDIDO sem perguntar ao usuário.
> 3. No fim de cada sessão, atualize a seção 1 e o Registro (seção 12) e, se alguma decisão mudou, o `AGENTS.md`.
> 4. Quando este arquivo crescer demais, divida em PLANO.md (estável) + PROGRESSO.md (log).
> 5. O `AGENTS.md` (e o `CLAUDE.md`, que só aponta para ele) é o resumo curto para qualquer IA. Se ele e este plano discordarem, vale este plano.

Criado em 05/11/2026 (planejamento feito pelo celular). Última atualização: 07/11/2026. Idioma do projeto: pt-BR.

---

## 1. Estado atual

- **Fase:** planejamento encerrado em 05/11/2026 → próxima: Etapa 0 (fundação e testes técnicos).
- **Lançamento (D-33):** RJ primeiro (beta pública só com o RJ, fim da Etapa 4); depois SP, MG e ES entram como atualizações do mesmo mod (Etapa 7).
- **Próxima ação (atualizada em 07/11/2026, noite):** Etapa 0.2 em andamento. **T1 passou** (Urca jogada; problemas U1–U11 em `PROBLEMAS_CONHECIDOS.md`, quase todos resolvidos no nosso gerador ou no Kit Brasil). **T7: não** (o gerador de cidades será nosso; KnoxMap como montador). **Mapa independente decidido (D-36)** e testado: o jogo funciona só com o nosso mapa. **T2 e T8: parte 1 passou.** **T7c passou** (gerador nosso + KnoxMap; aprovado em jogo). **T9 não passou** com o KnoxMap como está: o desenho de curvas será nosso (detalhes no Registro). Decididos D-36 (mapa independente) e D-37 (assinatura do KnoxMap uma vez só). Próximos, nesta ordem: **T2 parte 2** (célula mais distante), nomes de rua no mar (U8), resto do T8 e T4. T5 e T6 esperam o PC potente. O projeto vive em `C:\Users\yanbe\Zomboid\RealSudesteBrasil\`.
- **Ambiente atual (07/11/2026):** estamos no **notebook Acer Nitro V15** (8 GB de RAM, RTX 3050), **não no PC potente** (Ryzen 7 5700X3D, RTX 5060 Ti 16 GB, 32 GB de RAM, NVMe de 2 TB). Aqui só se adianta o que é leve: preparar ferramentas e dados, documentos, modelos pelo Tripo (na nuvem), testes minúsculos (T1 e T7 num bairro) e, no jogo, **testar só a visão isométrica por enquanto** (o 3D do Viewpoint e o T6 podem não rodar bem). Gerar e compilar o RJ inteiro, rodar mapa grande no jogo e IA 3D local ficam para o PC potente. A pasta do projeto está na Área de Trabalho do notebook; para levar ao PC potente, usar o Git (0.1) ou copiar a pasta.
- **Pendente do usuário:** nada que bloqueie a Etapa 0. Todas as perguntas do planejamento foram respondidas (a P7, sobre o hardware, Claude verifica na Etapa 0).
- **Ainda PROPOSTO (aguardam confirmação ou teste):** D-30 (Pão de Açúcar visitável) e a escolha da altura do relevo, 1:10 ou 1:15 (D-26/D-27), saem depois de ver em jogo, na Etapa 2.7; D-32 (tiles e modelos de drogas decorativos) depende de conferir as regras de conteúdo da Workshop antes de implementar; D-34 (atualização que muda o mapa pede save novo) o usuário confirma antes da beta pública; D-35 (cidades de rodovia com recursos variáveis) depende do teste de viagem no T8/T6.
- **Fora do plano, com o usuário:** revisar e salvar a skill `novo-movel-3d` (substitui o antigo "Básico 01") e, quando quiser, apagar a cópia antiga da Área de Trabalho (`C:\Users\yanbe\OneDrive\Área de Trabalho\RealSudesteBrasil\`). A pasta oficial agora é `C:\Users\yanbe\Zomboid\RealSudesteBrasil\` (seção 6).
- **Versão de referência do jogo:** B42 estável **42.22** (informada pelo usuário em 06/11/2026; em 05/11 a referência era a 42.21 estável, com a 42.22 em pré-lançamento). O mod sempre acompanha a versão mais recente do jogo (D-12).

---

## 2. Objetivo

**Real Sudeste Brasil:** mod de mapa inspirado no Real USA, com o Sudeste do Brasil em escala reduzida (1:15) e as cidades nas posições reais.

- O escopo é **só o Sudeste** (SP, RJ, MG, ES), na escala 1:15 (decisão de 06/11/2026). **O RJ é lançado primeiro**, como beta; SP, MG e ES entram depois como atualizações do mesmo mod (D-33). Outras regiões ficam fora do escopo atual; se um dia vierem, serão projetos à parte (por exemplo, "Real Sul Brasil"), reaproveitando scripts e kits, com grade e escala próprias.
- Será publicado na Steam Workshop.
- Compatível com o Viewpoint (primeira pessoa) desde o início.

---

## 3. Contexto (pesquisa de 05/11/2026)

### Real USA (autor MaQari, Workshop 3829712469)

- Os EUA contíguos a 1:40 (1 tile = 40 m): 472×304 células, ~9 GB, 665 cidades.
- As cidades grandes são malhas de ruas com os prédios do próprio jogo, mais marcos.
- Placas e monumentos próprios têm 3D para o Viewpoint.
- Tem uma parte em Java (via ZombieBuddy) que dá ao campo entre as cidades a vegetação real, faz o clima por região e aumenta o buffer de save. Sem o Java, cidades e estradas funcionam, mas o campo vira a mata padrão do jogo.
- Dados usados: OSM, ESA WorldCover, USGS/AWS (relevo), Natural Earth, Overture, NOAA.
- As cidades grandes pesam (engasgos e carregamento lento).
- Circulou um boato de minerador de cripto no Real USA; o autor diz que a Steam liberou o mod. A Indie Stone publicou um aviso sobre os riscos de mods em Java, e o ZombieBuddy exige instalação manual, fora da Workshop. **Lição: o mapa principal fica sem Java.**
- *Correção (05/11, 22h40):* uma versão anterior deste plano dizia que o Real USA e o ZombieBuddy tinham sido "removidos da Workshop". Isso era um erro de leitura: o aviso de "removido" é um texto escondido que aparece em qualquer página da Workshop lida pelas ferramentas do Claude, até na de mods comuns. Não use esse aviso como prova de remoção.

### Ferramentas

- As ferramentas oficiais da B42 (WorldZed, TileZed, AnimZed) foram prometidas para depois do lançamento estável e ainda não saíram. As comunitárias funcionam para a B42 (PZwiki).
- Formato da B42: células de 256×256 tiles (eram 300×300 na B41). Os arquivos compilados são `.lotheader` e `.lotpack`.
- **KnoxMap** (GitHub CalvyPZ/knoxmap, autores euclid80tr e CalvyPZ, baseado no Knoxify de arytek):
  - Transforma dados do OpenStreetMap em mapa B42 jogável, com prédios mobiliados gerados, densidade de zumbis pela população e mapa in-game com nomes de ruas.
  - Roda por linha de comando (`knoxmap_cli.py build/compile/install`), usa os extratos da Geofabrik e tem escala ajustável (metros por tile).
  - Divide áreas grandes em pedaços de 25×25 células, cada um um mod.
  - Compilador: PZ Mapping Tools (Alree/Unjammer, GPL).
  - Licença mista: partes em MIT, compilador em GPL e arquivos do Knoxify sem licença. → Usar como ferramenta; não copiar código do Knoxify para o nosso projeto.
  - Limitações: multiplayer não testado, interiores genéricos, ruas sinuosas ficam "em degraus" (nós resolvemos isso com o nosso próprio desenho de ruas, D-21). Versão 1.8.4.1 em 04/11/2026.
- **KnoxMap na prática (aprendido nos testes de 07/11/2026, v1.8.5.2):**
  - **Versão em uso:** pacote oficial v1.8.5.2 em `ferramentas\knoxmap-1.8.5.2\` (traz `knoxlots.exe`, o compilador de células, e `knoxroute.exe`, o roteador de ruas, já prontos). O `git clone` do CalvyPZ não serve: pede compilar o compilador em Rust. Exige Python 3.12 64 bits e Visual C++ ≥ 14.51.
  - **Setup** (`knoxmap_setup.py`, uma vez só): baixa as PZ Mapping Tools (40 MB) e o PZWorldEd_cli (6 MB), acha o jogo na Steam e copia 543 folhas de tiles **do jogo instalado** (não podem ser redistribuídas). Leva alguns minutos.
  - **Fonte dos dados:** no modo "auto" ele baixa o extrato da Geofabrik que cobre a área. Para o Rio, o menor extrato é o do **Sudeste inteiro (863 MB)**. No notebook, deixamos `"osm_source": "overpass"` no `knoxmap_config.json` (baixa só a área, ~10 min por bairro na internet móvel). No PC potente, com internet boa, o extrato é melhor (baixa uma vez e serve para o RJ inteiro). Também desligamos `auto_update` e `discord_presence`.
  - **Etapas:** gerar (baixa o OSM e desenha o chão) → prédios (plantas e móveis) → compilar (`.lotheader`/`.lotpack`) → instalar (cria o mod em `Zomboid\mods\`). Rodamos sem janela com `scripts\knoxmap_pipeline.py` + um arquivo de configuração por teste (`scripts\testes\*.json`). Mapas ficam em `ferramentas\knoxmap-1.8.5.2\output\`.
  - **Comportamentos que importam:** gira o mapa para alinhar as ruas ao grid (na Urca, 32°; dá para desligar em *Straighten streets*); escolhe sozinho a célula de origem (a Urca foi para a célula 70,0); escala de 0,5 a 100 m/tile, mas o "normal" é 1–8; desenhos próprios entram como elementos do OSM (GeoJSON com `kind` da paleta: ruas, áreas, prédios), e o resto do processo os trata como reais.
  - **Limites confirmados:** não inventa ruas nem bairros (T7); só completa buracos entre prédios existentes. Prédios reais somem em escalas grandes (a 15 m/tile, uma casa vira menos de 1 tile).
  - **Ferramentas de conferência:** `tools\render_lots.py` desenha o mapa compilado como o jogo desenha (bom para checar sem abrir o jogo); o `*_preview.png` de cada mapa mostra o chão visto de cima.
- **PZ Reverse Mapper** (Nexus 337): converte mapas compilados (inclusive B42) de volta para projeto WorldEd. Serve para estudar o mapa vanilla.
- A Geofabrik tem os extratos prontos do Brasil por região: Sudeste, Sul, Centro-Oeste, Nordeste e Norte. Só o do Sudeste interessa a este projeto.

### Limitação do jogo

No jogo base o terreno é plano (não há altura de terreno). No isométrico, o relevo só entra de forma indireta: mata densa, rocha ou estruturas em andares.

A B42 subiu o limite de altura das estruturas de 8 para **32 andares** (fontes de terceiros, ver seção 14). A visibilidade em 32 níveis aumenta bastante a memória usada, então andares em excesso pesam.

### Relevo no Viewpoint (pesquisa de 05/11/2026)

- O Viewpoint 0.1.6 trouxe o "Terrain relief" (morros e vales), ainda experimental. Os autores dizem que não deveria vir ligado por padrão; liga e desliga em World → Detail.
- Addons de relevo:
  - **Viewpoint Better Terrain** (Jailow): relevo com física para veículos, jogadores e zumbis, e prédios em fundações niveladas. Multiplayer não validado.
  - **Viewpoint Rolling Hills** (What2_Call_It, licença MIT): relevo visual, com um addon de física à parte. As cidades grandes ficam na altura original.
- Os dois foram feitos para o mapa vanilla: não aceitam relevo de mapas de outros autores e não usam altitudes reais.
- Todos exigem Viewpoint + ZombieBuddy (Java). O relevo só existe dentro do Viewpoint; no isométrico, tudo continua plano.

### Contas de tamanho (retângulo envolvente do Sudeste ≈ 1.408 × 1.229 km)

| Escala | Sudeste (células) | SP→RJ pela Dutra no jogo |
|---|---|---|
| 1:40 | 138 × 121 | ~11 km |
| 1:20 (era a escolha até 06/11) | 275 × 241 | ~21,5 km |
| **1:15 (escolhida)** | 367 × 321 | ~28,7 km |

A 1:15, só pela área de cada município: São Paulo ≈ 10×10 células, Rio ≈ 9×9, BH ≈ 4,8×4,8, Vitória ≈ 2,7×2,7.

**Área final no jogo a 1:15** (a área cai 225×; no jogo, 1 tile ≈ 1 m):

| Área | Real (km²) | No jogo (km²) | Células de terra |
|---|---|---|---|
| RJ | 43.750 | ~194 | ~2.970 |
| ES | 46.074 | ~205 | ~3.130 |
| SP | 248.219 | ~1.103 | ~16.830 |
| MG | 586.513 | ~2.607 | ~39.780 |
| **Sudeste** | 924.556 | **~4.109** | **~62.700** |

O retângulo que envolve o Sudeste dá ~7.700 km² no jogo, contando mar e partes de outros estados. Comparação: o Real USA tem ~5.050 km² de terra no jogo. O Sudeste a 1:15 dá cerca de 81% disso. (A 1:20 eram ~2.311 km², cerca de 46%.)

---

## 4. Quem faz o quê

**Claude consegue:**

- Escrever e rodar scripts (Python) que baixam e processam dados geográficos e geram imagens de terreno.
- Operar o KnoxMap pela linha de comando.
- Gerar os arquivos do mod: map.info, spawns, objetos, mapa in-game, traduções e Lua.
- Gerar prédios por regras (os arquivos são texto).
- Fazer modelos 3D simples/estilizados por script, como no Living Props.
- Escrever a documentação e a página da Workshop.

**O usuário:**

- Roda o jogo e testa (Claude não vê o jogo).
- Manda prints e feedback.
- Toma as decisões de gosto.
- Abre o WorldEd/TileZed quando algo precisar de edição visual.
- Publica na Workshop pela conta dele.

**Limites:** arte detalhada (tiles bonitos) é difícil para o Claude; o estilizado fica bom. O processamento pesado roda no PC do usuário (a nuvem do Claude não baixa esses dados).

---

## 5. Decisões

| ID | Decisão | Status | Motivo / observação |
|---|---|---|---|
| D-01 | Escala **1:15** (1 tile = 15 m), só para o Sudeste | DECIDIDO | Escolha do usuário em 06/11/2026 (antes: 1:20 para o Brasil inteiro). Mudar depois = refazer tudo. Ver risco R1. Se o usuário quiser mais detalhe só no RJ, dá para fazer uma versão 1:10 do RJ à parte (ideia futura, não decidida). |
| D-02 | Grade fixa: projeção SIRGAS 2000 / Brazil Polyconic (EPSG:5880), norte para cima, origem cobrindo o Sudeste | PROPOSTO | Escopo só do Sudeste (D-01). A origem exata sai do teste T2. |
| D-03 | Cidades genéricas: contorno real em 1:15, preenchido com ruas e prédios em escala de jogo, mais marcos feitos à parte | DECIDIDO | Igual ao Real USA. |
| D-04 | Publicar na Workshop → só conteúdo nosso, de dados abertos ou com permissão; créditos corretos (OSM/ODbL etc.) | DECIDIDO | Por isso o Building Pool V3 (de terceiros) fica de fora sem permissão. |
| D-05 | Cidade piloto: Rio de Janeiro | DECIDIDO | |
| D-06 | Java só se não houver outro jeito | DECIDIDO | Mods Java exigem instalação manual (ZombieBuddy), e a Indie Stone alertou sobre os riscos. Tentar sempre Lua/arquivos de mapa primeiro. A exceção aprovada é o addon de relevo (D-26). |
| D-07 | Viewpoint desde o início: toda tile ou objeto novo nasce com modelo 3D registrado; toda etapa é testada no isométrico e no Viewpoint | DECIDIDO | O Real USA provou que dá (placas e monumentos próprios em 3D). Mesmo método do Living Props. |
| D-08 | Dados de hoje (OSM atual), sem tentar recriar 1993 | DECIDIDO | Detalhes de época (marcas, carros) podem ser ajustados depois. |
| D-09 | Visual brasileiro: tiles do jogo arrumadas no jeito brasileiro (muro + portão, laje, cores) + tiles brasileiras novas (placas em português, fachadas, calçada de pedra portuguesa, orelhão…). Toda tile nova tem de aparecer em 3D no Viewpoint. As essenciais entram já no piloto, depois que o T5 provar o 3D; o kit completo vem na Etapa 5 | DECIDIDO | Resposta do usuário em 05/11. Móveis continuam sendo só os do jogo (D-16). |
| D-10 | Tudo gerado por script a partir de dados + kits. Só os marcos são feitos à mão, guardados como "carimbos" separados | PROPOSTO | Princípio anti-retrabalho: mudou uma regra → roda de novo, não refaz à mão. |
| D-11 | Estrutura: **um mod só** para o jogador (um item na Workshop), não um mod por estado. Por dentro, ele só se divide em partes (ex.: Core + mapa) se o T6 mostrar que o tamanho exige; o jogador não precisa montar nada | DECIDIDO | Decisão do usuário em 06/11/2026 (antes: Core + um mod de mapa por estado, PROPOSTO). A divisão interna, se houver, sai do T3/T6. |
| D-12 | Alvo: **sempre a versão mais recente do Project Zomboid** (hoje, B42.22). Registrar a versão usada em cada teste. Quando sair versão nova, avisar o usuário e checar a compatibilidade (inclusive a do Viewpoint) antes de seguir | DECIDIDO | Pedido do usuário em 06/11/2026 (antes: "B42 estável atual"). Ver risco R7. |
| D-13 | Ferramentas: KnoxMap (ferramenta/base), PZ Mapping Tools (compilador), WorldEd/TileZed comunitários; avaliar os oficiais quando saírem | PROPOSTO | T1 (07/11/2026): KnoxMap v1.8.5.2 gera, compila e instala de ponta a ponta. T7: não gera cidades inventadas; vira só montador/compilador do nosso gerador. T7c (07/11/2026): o nosso gerador desenha ruas e lotes em escala de jogo e o KnoxMap monta, mobilia, compila e instala; funciona. Confirmar depois de ver o T7c em jogo. |
| D-14 | Nome do mod: Real Sudeste Brasil | DECIDIDO | Escolha do usuário (P2). |
| D-15 | Survival friendly: tudo saqueável, recursos de sobrevivência garantidos, zumbis pela população (ajustável no sandbox) | DECIDIDO | Pedido do usuário. Detalhes na seção 6.1. |
| D-16 | Casas com plantas e mobília realistas no jeito brasileiro, usando os nomes de cômodo do jogo para o loot funcionar | DECIDIDO | Só a mobília do jogo, arrumada para parecer uma casa brasileira. Não vamos criar móveis novos, para não pesar o jogo (pedido do usuário). |
| D-17 | Eventos do jogo base funcionando no mapa todo (zonas geradas automaticamente) + eventos brasileiros próprios | DECIDIDO | Teste T8. |
| D-18 | Cenas do cotidiano brasileiro (lista de P8) + cenas características de cada cidade (Av. Brasil confirmada) | DECIDIDO | As demais cenas por cidade são confirmadas estado por estado. |
| D-19 | Armas: equilíbrio do jogo base, por enquanto | DECIDIDO | Resposta de P9. Pode ser revisto na Etapa 6. |
| D-21 | Ruas e estradas com curvas como no jogo base, nunca "em degraus": caminho suavizado + peças de curva e diagonal do próprio jogo + acabamento automático das bordas | DECIDIDO | Pedido do usuário. Detalhes na seção 6.1; teste T9. |
| D-20 | O mod é só mapa: sem veículos novos e sem móveis novos. As cenas usam só veículos do jogo base. Tiles novas podem, sempre com 3D no Viewpoint | DECIDIDO | Pedido do usuário. |
| D-26 | Relevo real no Viewpoint: addon opcional ("Real Sudeste Brasil – Relevo", em Java via ZombieBuddy) que lê um arquivo de altitudes gerado de dados reais de satélite e o aplica ao terreno do Viewpoint. Por enquanto só visual (estética), sem física. O mapa principal continua plano e sem Java. Prioridade: primeiro o mapa funcionar bem com o Viewpoint base; o relevo vem depois (Etapa 2.7) | DECIDIDO | Pedido do usuário. Base provável: a parte visual do Rolling Hills (MIT). Física fica para o futuro, se o usuário pedir. A decisão final de usar o relevo só sai depois de ver como fica em jogo (Etapa 2.7; usuário, 06/11/2026). |
| D-27 | Altura do relevo 1:10 (1,5× a proporção horizontal de 1:15): Corcovado ~71 m (com o Cristo, ~110 m), Pão de Açúcar ~40 m | DECIDIDO | Escolha do usuário. Confirmar no protótipo do Rio (Etapa 2.7). **Na 2.7, testar lado a lado 1:10 e 1:15** (Corcovado ~71 m vs ~47 m; Pão de Açúcar ~40 m vs ~26 m; o Cristo, como modelo, soma ~38 m em cima) e o usuário escolhe vendo em jogo (06/11/2026). |
| D-28 | Morros e marcos, forma mista: Cristo = modelo 3D + tile; Corcovado = relevo visual, com estrada até o topo; Pão de Açúcar, Dedo de Deus e Pedra da Gávea = rocha esculpida em 3D, sem escalada | DECIDIDO | Detalhes na seção 6.1. Plano B para o Corcovado se o relevo falhar na Etapa 2.7. **Para o Pão de Açúcar, ver o teste D-30; se ele falhar, vale este D-28.** |
| D-29 | Modelos 3D a partir de fotos com o Tripo (feitos pelo usuário). O Claude limpa, reduz e registra no Viewpoint. Crédito ao Tripo na Workshop | DECIDIDO | O mod é gratuito, não será vendido. Lista de ferramentas na seção 10. |
| D-22 | Localidades: entram todas as possíveis (sedes municipais, distritos e vilarejos). Todo vilarejo ganha um núcleo mínimo (praça, igreja, venda e algumas casas) e os turísticos ganham um bônus (mais pousadas e comércio), conforme os dados reais (pousadas e cachoeiras no OSM) | DECIDIDO | P5. A mesma regra vale para o mapa todo, para ficar coerente. |
| D-23 | Estradas de serra com curvas exageradas: mais fechadas do que a escala daria, mantendo a direção real da estrada | DECIDIDO | Na escala pura, as curvas de serra sumiriam. |
| D-24 | Ordem de produção: RJ → SP → MG → ES | DECIDIDO | P6. O RJ sai primeiro como beta (D-33). |
| D-25 | Repositório Git privado na conta GitHub do usuário | DECIDIDO | P3. Serve de backup e economiza tokens. |
| D-30 | **Pão de Açúcar visitável (teste):** em vez de só rocha sem escalada, tentar um trajeto a pé (trilha/escadaria com patamares, sem construir a montanha inteira em andares) até um mirante com vista do alto: Morro da Urca (~22 m, ≈ 7 andares) e topo (~40 m, ≈ 13 andares). O bondinho continua como cenário. A montanha aparece como relevo visual (D-26/D-27) | PROPOSTO | Pedido do usuário em 06/11/2026: poder visitar e ver a vista de cima. Ele topou testar começando pelo Pão de Açúcar (o menor). Decisão final só depois de ver em jogo (Etapa 2.7). Andares são estimativa (≈ 3 m por andar; conferir). Se falhar (FPS, visual ou física): vale o D-28. |
| D-31 | **Casa de "chefe do morro" (favelas do RJ):** construção especial e rara, de ostentação (laje com piscina e churrasqueira, sala com TV grande e som, bebidas, dinheiro, joias) e com o "arsenal" e o material do tráfico dentro. Tudo montado com móveis e itens do jogo base (D-16, D-20). **Sorteada por regra** em favelas de porte médio/grande do RJ, sem ligar a casa a nomes de comunidades reais | DECIDIDO | Pedido do usuário em 06/11/2026; local decidido em P11 (mesmo dia). Itens: só os do jogo base (o T8 lista o que existe); armas no equilíbrio do jogo base (D-19). Ver D-32 e risco R15. |
| D-33 | **Lançamento em fases:** RJ primeiro (beta pública só com o estado do RJ, na grade do Sudeste em 1:15); SP, MG e ES entram depois como **atualizações do mesmo mod** (D-11), não como mods separados | DECIDIDO | Decisão do usuário em 06/11/2026. Dá feedback real mais cedo e um mod jogável no meio do caminho; a grade do Sudeste (D-02) garante que o RJ não muda de lugar quando os outros estados entrarem. Atualizações que mudam o mapa pedem save novo (D-34, R16). |
| D-34 | **Política de atualizações:** atualização que muda o mapa (estado novo, kit novo, mapa gerado de novo) = **save novo recomendado**, avisado no changelog e na descrição da Workshop. Juntar as mudanças de mapa em poucas versões grandes (ex.: RJ; RJ + SP; …). Correções que não mexem no mapa (Lua, traduções, modelos 3D do Viewpoint) não pedem save novo; mudanças de loot só valem para o que ainda não foi aberto | PROPOSTO | Pesquisa de 06/11/2026, confirmando o que o usuário já sabia: um save só recebe mapa novo em áreas **nunca visitadas**; áreas visitadas ficam com a versão antiga (dá para limpar com ferramentas de "chunk cleaner", apagando o que havia ali). Por isso mapas grandes, como o Raven Creek, pedem jogo novo a cada atualização. |
| D-32 | Tiles e modelos 3D **decorativos** representando drogas, usados só nos ambientes do tráfico (casa de chefe, D-31). Cenário, não item usável. Como toda tile nova, com 3D no Viewpoint (D-07, D-09) | PROPOSTO | Ideia do usuário em 06/11/2026, por enquanto só proposta. Conferir as regras de conteúdo da Steam Workshop antes de publicar. |
| D-35 | **Cidades de rodovia com recursos variáveis:** cada cidade ou vila nas rodovias principais (ex.: Dutra, Rio–SP) recebe, **na hora de gerar o mapa**, um nível fixo de recursos: completa (posto, comércio e farmácia), parcial ou "seca" (só casas). Sorteado por regra, como no D-31. **Trava:** distância máxima seguida sem posto de gasolina, para a viagem ser difícil, mas possível (valor definido no T8/T6). As construções ficam iguais em todos os saves; a variação entre saves vem do que o jogo já sorteia (loot nos recipientes, veículos, eventos, D-17) | PROPOSTO | Ideia do usuário em 07/11/2026 (não deixar a viagem Rio–SP fácil demais). Dúvida do usuário, correta: construção faz parte do mapa, não é uma entidade sorteada em jogo; por isso o sorteio acontece uma vez, na geração. Cidades pequenas ficam pequenas em 1:15 (ex.: Queluz com uns 100 tiles de lado, estimativa), então o gerador precisa de um tamanho mínimo que comporte posto, comércio e farmácia. Testar a viagem inteira no T8/T6. |
| D-36 | **Mapa independente:** o Real Sudeste Brasil é o mundo inteiro; o Knox County (Muldraugh, Louisville etc.) **não** é carregado junto. No servidor, `Map=` lista só o nosso mapa | DECIDIDO | Decisão do usuário em 07/11/2026, depois de ver a Urca de teste aparecer acima de Louisville. O KnoxMap já tem esse modo ("Standalone": mapa na célula 0,0, sem o Knox County). Muda o T2: em vez de "convive com o Knox County?", testar se o jogo carrega o nosso mapa sozinho (loot, zonas e nascimento funcionando) e se aceita a célula mais distante do Sudeste. Também libera a origem (D-02): não precisa desviar do mapa original. |
| D-37 | **Assinatura do KnoxMap no chão:** manter o crédito "KNOXMAP BY EUCLID80TR" escrito no chão, mas **uma vez só no mapa todo**, num lugar escolhido pelo usuário (não mais perto de onde o jogador nasce). O crédito escrito continua no `ATTRIBUTION.txt` e na página da Workshop | DECIDIDO (o lugar ainda será escolhido) | Decisão do usuário em 07/11/2026, depois do T9. Técnica: mudar em `knoxbuild\credit_ground.py` (MIT) o ponto de busca para um ponto nosso e desligar nos outros pedaços; sem isso, cada pedaço do mapa montado pelo KnoxMap ganharia uma assinatura. Implementar na Etapa 2. |

---

## 6. Arquitetura (como o mod é montado)

Camadas, de baixo para cima:

1. **Dados:** OSM Sudeste (Geofabrik); IBGE (malha municipal, população do Censo 2022, áreas urbanizadas); cobertura do solo (ESA WorldCover ou MapBiomas, conferir licença).
2. **Grade (D-02):** converte qualquer latitude/longitude em tile.

   ```
   tile_x = floor((E − E0) / 15) + OFFSET_X
   tile_y = floor((N0 − N) / 15) + OFFSET_Y
   célula = tile // 256
   ```

   E0, N0 e os OFFSETs serão gravados aqui na Etapa 1.
3. **Macro:** costa, rios, lagos, rodovias, ferrovias e tipo de campo (pasto, cana, eucalipto, Mata Atlântica, cerrado).
4. **Cidades:** contorno real + malha de jogo (ruas, quadras, lotes, prédios). O kit é trocável: começa com os prédios do jogo e depois ganha os brasileiros, só rodando o gerador de novo.
5. **Marcos:** carimbos feitos à mão, cada um com versão 3D para o Viewpoint.
6. **Jogabilidade:** zumbis pela população, loot por tipo de lugar, spawns e mapas de papel por cidade.
7. **Empacotamento:** um mod só para o jogador (D-11); divisão interna só se o T6 exigir. Só se compila célula que tem conteúdo; o resto fica com a mata do jogo.

**Pastas sugeridas no PC:**

```
C:\Users\yanbe\Zomboid\RealSudesteBrasil\   (pasta oficial desde 07/11/2026; fora do OneDrive)
  PLANO_BRASIL_ZOMBOID.md   ← este arquivo
  AGENTS.md                 ← resumo para qualquer IA
  CLAUDE.md                 ← só aponta para o AGENTS.md
  GUIA_PROMPTS_TRIPO.md     ← guia de prompts do Tripo (D-29)
  dados\    (downloads grandes; fora do Git)
  scripts\
  kits\     (regras de cidade, prédios)
  marcos\   (carimbos + modelos 3D)
  saida\    (gerado; pode apagar e gerar de novo)
Mods instalados: C:\Users\yanbe\Zomboid\mods\
```

**Local do projeto (07/11/2026, decidido pelo usuário):** o desenvolvimento foi movido para `C:\Users\yanbe\Zomboid\RealSudesteBrasil\`. Fica fora do OneDrive e sem acento no caminho, o que resolve o cuidado anterior (a Área de Trabalho está no OneDrive e acento pode quebrar WorldEd/TileZed e scripts). `dados` e `saida` ficam fora do Git. A cópia antiga da Área de Trabalho não deve mais ser editada.

### 6.1 Jogabilidade e realismo (diretrizes fixas)

**Survival friendly acima de tudo.** O mapa tem que ser bom de jogar: lugares para lootear, zumbis para enfrentar, carros para achar e eventos espalhados, como no jogo base.

#### Casas e prédios realistas por dentro

- **Plantas no jeito brasileiro:** sala, cozinha, quarto(s), banheiro, área de serviço com tanque, quintal/varanda/laje e garagem quando couber.
- **Tipos de moradia:** casa térrea, sobrado, casa geminada ou de vila, apartamento (com área de serviço), quitinete, casa de comunidade (menor e mais apertada), sítio/fazenda.
- **Comércio e serviços:** padaria, mercadinho, supermercado, farmácia, boteco, açougue, loja de material de construção, oficina, posto, igreja, escola, UPA/posto de saúde, hospital, delegacia/batalhão da PM, quartel.
- **Mobília: só a do jogo.** Não criamos móveis novos, para não pesar o jogo. O realismo vem da escolha e da arrumação: por exemplo, a pia ou a máquina de lavar do jogo na área de serviço fazendo o papel do tanque, o rack com TV na sala, a mesa de cozinha com cadeiras, o guarda-roupa no quarto.
- **Nomes de cômodo:** os cômodos usam os nomes de cômodo do jogo (cozinha = kitchen etc.), porque é pelo nome que o jogo decide o loot. Cômodo brasileiro sem equivalente usa o mais próximo (ex.: área de serviço → lavanderia do jogo). O catálogo de nomes e de loot é extraído dos arquivos do jogo no T8.
- Toda casa tem pelo menos cozinha, banheiro e quarto: algumas histórias de casa do jogo só acontecem em casas com esses três cômodos.

#### Loot e recursos

- Todo prédio é saqueável, com loot coerente com o tipo do lugar.
- Garantir os recursos de que a sobrevivência precisa:
  - comida: mercados, padarias, Ceasa;
  - remédios: farmácias, UPAs, hospitais;
  - ferramentas e material: lojas de construção, oficinas;
  - combustível: postos;
  - armas: delegacias, batalhões, quartéis, na quantidade do jogo base (D-19);
  - carros: estacionamentos, garagens, concessionárias.

#### Zumbis

- A densidade segue a população real (Censo 2022): cidade grande tem muito zumbi; o interior, pouco. Ajustável no sandbox.
- Mais zumbis onde a história pede: rodoviárias, estádios, hospitais, engarrafamentos.

#### Eventos do jogo base (precisam funcionar sozinhos)

O jogo monta cenas aleatórias quando o mapa tem as zonas certas:

- histórias de veículo nas estradas: batidas, bloqueio policial, obras, pneu furado;
- histórias de zona em matas e parques: acampamento, churrasco;
- histórias de casa: sobrevivente morto, casa queimada, festa;
- carros estacionados nas zonas de veículo: estacionamento, polícia, ambulância, engarrafamento.

O gerador cria essas zonas automaticamente em todo o mapa. Teste T8.

#### Cenas do cotidiano brasileiro (escolhidas em P8; eventos aleatórios próprios, em Lua, na Etapa 6)

Como funciona: o gerador cria os lugares (laje, campinho de terra, rua de feira, praia, cachoeira, barraca na rodovia). Depois, a cena aleatória coloca objetos, zumbis com roupas do jogo e, quando for o caso, veículos do jogo base (D-20).

- **Trânsito e estrada:**
  - caminhão tombado: veículo de carga do jogo base virado, com a carga espalhada (bom ponto de loot);
  - fila no posto: carros abandonados na fila da bomba;
  - família fugindo: carro do jogo base cheio de malas e bolsas, abandonado na saída da cidade.
- **Bairro:** churrasco na laje; pelada no campinho; festa junina (bandeirinhas, barracas, fogueira; combina com o começo do jogo em 9 de julho, época de festa julina); boteco lotado.
- **Comércio e rua:** feira livre abandonada (bom ponto de comida); camelôs na calçada; mercado saqueado.
- **Praia, interior e natureza:** praia lotada (em todas as praias); barraca de beira de estrada (queijo, doce, fruta); cachoeira com acampamento; romaria a pé a caminho de Aparecida.
- **Ficaram de fora:** ônibus lotado parado e fila na lotérica/banco.
- **Mobiliário urbano (ideia do usuário, 07/11/2026, depois do T7c):** calçadas largas e praças não ficam vazias. O gerador espalha, onde fizer sentido, orelhões, bancas de jornal, pontos de ônibus e mesas e cadeiras de bar (na frente de bares e lanchonetes). Peças do jogo base onde existirem; orelhão e banca entram no Kit Brasil (Etapa 5), com 3D no Viewpoint (D-07).

#### Cenas características das cidades (carimbos fixos, feitos à mão)

Lugares marcantes que o jogador reconhece. A Av. Brasil está confirmada; as outras são sugestões, a confirmar estado por estado (RJ na Etapa 4; SP, MG e ES na Etapa 7). Sempre com veículos do jogo base, nunca veículos novos (D-20):

- **RJ:** engarrafamento na Av. Brasil (carros e utilitários do jogo base abandonados, com zumbis no meio; usa a zona de engarrafamento que o jogo já tem); Ponte Rio–Niterói travada; Linha Vermelha; Copacabana lotada; Maracanã em dia de jogo; Central do Brasil lotada; Rodoviária Novo Rio; bloqueios do Exército nas saídas da cidade.
- **SP:** Marginais Tietê e Pinheiros congestionadas; Av. Paulista; Rodoviária do Tietê; Mercadão e Ceagesp; Porto de Santos com contêineres; Bandeirantes/Anhanguera travadas; Basílica de Aparecida com romeiros.
- **MG:** Mineirão; Mercado Central de BH; ladeiras e igrejas de Ouro Preto; BR-381 travada.
- **ES:** Terceira Ponte travada; Convento da Penha; Porto de Tubarão.

Cada cena entra junto com a sua cidade (Etapas 2, 4 e 7). O que for tile nova ganha 3D no Viewpoint.

#### Localidades (D-22)

- Entram todas as localidades possíveis: sedes municipais, distritos e vilarejos.
- A 1:15 a área encolhe 225×, mas as casas continuam no tamanho do jogo. Um vilarejo de ~0,5 km² daria só 7 a 10 casas, por isso existe o núcleo mínimo, com bônus para os turísticos.
- Lugares que o usuário quer em destaque (com a mesma regra do resto do mapa, sem tratamento especial fora dela): cidade do Rio; Baixada Fluminense (Duque de Caxias, Nova Iguaçu, Belford Roxo, São João de Meriti, Nilópolis, Mesquita, Queimados, Japeri, Magé etc., formando uma mancha urbana contínua com o Rio); Região Serrana: Petrópolis, Teresópolis, Nova Friburgo, Lumiar (distrito de Nova Friburgo) e Sana (distrito de Macaé).
- **Relevo:** no isométrico o terreno é plano, e a serra aparece por mata atlântica densa, rochas, rios e cachoeiras. No Viewpoint, com o addon de relevo (D-26), morros e serras ficam com a altura real na escala 1:10 (D-27). Combina com a cena "cachoeira com acampamento", bem típica de Lumiar e Sana.

#### Morros e marcos (D-28, com o teste D-30)

Cada um feito do jeito que funciona melhor.

- **Cristo:** modelo 3D + tile, como os monumentos do Real USA. Funciona com e sem relevo.
- **Corcovado:** relevo real só visual (D-26), com estrada em curvas até o topo. No Viewpoint, o personagem e o carro aparecem subindo o morro até o Cristo, mas sem física de ladeira (não desce embalado, não pesa na subida). A física fica para o futuro, se for pedida. Do topo, a vista é a do Viewpoint: com o mapa em 1:15, a cidade fica compacta e boa parte do Rio cabe no campo de visão (o alcance real depende da distância de visão e precisa ser testado).
- **Pão de Açúcar, Dedo de Deus, Pedra da Gávea (e Dois Irmãos, se precisar):** rocha esculpida em 3D, porque o relevo não faz paredão vertical nem formas marcantes. Não dá para escalar: a base fica bloqueada com rocha. O bondinho do Pão de Açúcar aparece só como cenário, igual a ir de bondinho na vida real.
- **Teste D-30 (Pão de Açúcar visitável):** o usuário quer poder visitar e ver a vista do alto. Em vez de montar a montanha inteira em andares (pesado: a B42 já gasta bem mais memória com 32 níveis visíveis), fazemos só um **trajeto** (trilha/escadaria com patamares de descanso) colado na lateral, até um mirante. A montanha em si continua como relevo visual no Viewpoint. Os patamares podem ter loot e zumbis, para a subida virar uma pequena expedição. O jogo não tem rampas: a subida é por escadas. Estimativa: Morro da Urca ~22 m ≈ 7 andares; topo ~40 m ≈ 13 andares (≈ 3 m por andar, a conferir). O limite da B42 é 32 andares.
- No isométrico, todos aparecem como rocha e mata no chão plano, com o Cristo como tile.
- **Plano B para o Corcovado, se o relevo falhar na Etapa 2.7:** (a) "morro de andares", com patamares de rocha ligados por escadas e trilhas. Sobe a pé no isométrico, no Viewpoint e em multiplayer, sem Java, mas não de carro e fica com aspecto de degraus. Ou (b) só modelo 3D, sem subida. *Atenção:* o morro a 1:10 (~71 m) + a estátua (~38 m) somam ~109 m, algo como 36 andares (estimativa), acima do limite de 32 da B42. Se o plano B (a) for usado, talvez seja preciso reduzir a altura só nesse caso. Verificar antes.
- **Ordem de teste:** primeiro o Cristo como modelo em chão plano (T5c), garantindo que tudo funciona no Viewpoint base. O relevo visual vem só depois do Rio aprovado (Etapa 2.7); lá, o protótipo da Zona Sul começa pelo **Pão de Açúcar** (o menor), incluindo o teste do trajeto visitável (D-30), e só depois vai para o Corcovado. Sempre mostrando ao usuário antes de seguir.

#### Casa de "chefe do morro" (D-31; tiles de drogas: D-32, PROPOSTO)

Construção especial e rara nas favelas do RJ, para dar história e um bom ponto de risco e recompensa.

- **Visual de ostentação:** casa grande no alto do morro, com laje, piscina, churrasqueira, garagem, fachada chamativa (tiles brasileiras novas são permitidas, com 3D no Viewpoint, D-09) e dentro sala com TV grande, som, bar e quartos bem mobiliados. Só móveis do jogo base (D-16).
- **Loot:** riquezas (dinheiro, joias, eletrônicos, bebidas), armas e itens ligados ao tráfico. Armas no equilíbrio do jogo base (D-19). Itens só os que o jogo base tiver; o catálogo de itens sai do T8 (D-20: o mod é só mapa).
- **Cenário do tráfico (D-32, PROPOSTO):** tiles e modelos 3D decorativos representando drogas, só nesses ambientes. São cenário, não itens usáveis, e ganham 3D no Viewpoint como toda tile nova.
- **Zumbis:** mais densos em volta da casa, como num ponto de história do jogo.
- **Onde (decidido em P11):** sorteadas por regra em favelas de porte médio/grande do RJ (as favelas aparecem no mapa com a forma real, a partir dos dados abertos), sem ligar a casa a nomes de comunidades reais.
- É um carimbo feito à mão (D-10), que o gerador encaixa nos lugares escolhidos.

#### Marcos (P4)

- **Rio, obrigatórios:** Cristo Redentor, Pão de Açúcar (o bondinho entra como cenário fixo, não como veículo), Igreja da Candelária.
- **Rio, outros famosos (em ondas, mostrando antes de construir):** Maracanã, Arcos da Lapa, Escadaria Selarón, Theatro Municipal, Catedral Metropolitana, Mosteiro de São Bento, calçadão e Forte de Copacabana, Lagoa Rodrigo de Freitas, Museu do Amanhã, Ponte Rio–Niterói, Sambódromo, Jardim Botânico, Quinta da Boa Vista, Aeroporto Santos Dumont.
- **Região Serrana (sugestões):** Museu Imperial, Catedral São Pedro de Alcântara e Palácio Quitandinha (Petrópolis); Dedo de Deus e a sede do Parque Nacional da Serra dos Órgãos (Teresópolis); cachoeiras e pousadas de Lumiar e Sana.
- **Baixada (sugestão):** a refinaria de Duque de Caxias (Reduc), que é um ótimo ponto de combustível para sobreviver.

#### Ruas e estradas com curvas (D-21)

- O jogo é uma grade de quadrados, mas as estradas do jogo base têm curvas montadas com peças próprias de diagonal e de curva (no conjunto `blends_streets_01`). É esse visual que queremos.
- O nosso gerador desenha as ruas em três passos:
  1. **Suavizar o caminho:** tirar o "tremido" do traçado real e impor um raio mínimo de curva para cada tipo de via. Retas longas ficam retas; as curvas viram trechos retos e diagonais bem distribuídos.
  2. **Desenhar a pista** na largura certa para o tipo de via (rua, avenida, rodovia).
  3. **Acabamento automático:** para cada quadradinho da borda, escolher a peça do jogo que encaixa (reta, diagonal, curva, esquina), igual ao que o jogo base faz.
- Nas cidades genéricas, o traçado é nosso, já pensado para a grade: ruas retas e curvas suaves. Nas rodovias, que seguem o traçado real, a suavização é o que mais importa.
- Antes de desenhar, estudamos como o jogo base monta as curvas dele (pelo mapa vanilla aberto no WorldEd) e catalogamos as peças.
- **Estradas de serra (D-23):** Rio–Petrópolis (BR-040), Rio–Teresópolis, Friburgo–Lumiar e similares ganham curvas mais fechadas do que a escala daria, seguindo a direção real, para manter o clima de serra.
- **Limite honesto:** curva perfeitamente redonda não existe nem no jogo base. A meta é ficar tão bom quanto as estradas do jogo. Se faltar alguma peça, avaliamos criar uma tile nova (com 3D no Viewpoint, se precisar).

---

## 7. Etapas

**Regra geral:** teste pequeno antes de grande. Nenhuma etapa termina sem teste no isométrico e no Viewpoint, e sem o feedback do usuário.

### Etapa 0: Fundação e testes técnicos (go/no-go)

**0.1 Preparação:** Claude verifica RAM, CPU e espaço em disco; instala Python 3.10+, Git, o KnoxMap e as ferramentas comunitárias da B42; cria a pasta do projeto e o repositório Git privado na conta GitHub do usuário (D-25). O usuário só precisa fazer o login uma vez. Se a sessão for no notebook, instalar só o que cabe nele (ver "Ambiente atual" na seção 1).

**0.2 Testes** (registrar cada resultado na seção 12, com a versão do jogo usada, D-12):

- **T1 Caminho completo:** gerar e compilar um pedaço minúsculo (1 a 4 células de um bairro do Rio) com o KnoxMap e jogar.
- **T2 Coordenadas:** uma célula de teste no ponto mais distante do Sudeste a 1:15 (~célula 370 × 320 a partir da origem). O jogo carrega? ~~Convive com o Knox Country na lista `Map=`?~~ Com o mapa independente (D-36), testar se o jogo carrega o nosso mapa **sozinho**, com loot, zonas e pontos de nascimento funcionando → define a origem (D-02).
- **T3 Partes combinadas:** se o mod precisar ser dividido por dentro (D-11), as partes (ex.: Core + mapa) carregam juntas num mundo só?
- **T4 Campo sem Java:** o que o jogo faz com células vazias? Dá para escolher a vegetação sem Java? Se não der, quanto pesa compilar células de campo de verdade?
- **T5 Viewpoint:** (a) os prédios gerados aparecem certo em 3D? (b) uma tile nova (placa em português) com modelo 3D registrado aparece no Viewpoint sem mudar nada no isométrico? (c) o Cristo como modelo 3D + tile em chão plano, como primeiro marco, mostrado ao usuário (D-28).
- **T6 Tamanho e desempenho:** quantos MB pesa uma célula de cidade e uma de campo → estimativa do Sudeste → define se o mod único precisa de divisão interna (D-11).
- **T7 KnoxMap no modo "inventado":** ele aceita um contorno (polígono) e o enche de ruas e prédios de jogo, funcionando a 1:15? Se sim, vira o motor das cidades. Se não, fazemos o nosso gerador.
- **T8 Eventos, loot e zonas:** num pedaço gerado, aparecem histórias de veículo, de casa e de zona, carros estacionados e loot nos cômodos? Extrair dos arquivos do jogo o catálogo de nomes de cômodo, listas de loot e tipos de zona e de veículo. Ele vira um índice de consulta (economiza tokens). Testar também a viagem de ponta a ponta numa rodovia (D-35).
- **T9 Curvas:** estudar como o jogo base monta as curvas e desenhar uma rua bem sinuosa de teste (sugestão: um trecho da Av. Niemeyer, no Rio). Comparar com uma curva do jogo base, no isométrico e no Viewpoint. Só passa se não ficar "em degraus".
- (O antigo T10, do relevo, foi movido para a Etapa 2.7: primeiro o mapa precisa funcionar bem com o Viewpoint base.)
- (Saves e atualizações de mapa não precisam de teste: o comportamento já é conhecido de outros mods de mapa. Ver D-34.)

**Pronto quando:** T1–T9 respondidos e D-02, D-11 e D-13 confirmados.

### Etapa 1: Grade e esqueleto do Sudeste (só dados, nada compilado)

- Script de conversão lat/lon → tile, com a origem gravada na seção 6.
- Baixar os dados da camada 1 e o modelo de altitude (Copernicus DEM ou SRTM, gratuitos). Converter as altitudes para a nossa grade (D-02) na escala 1:10 (D-27).
- Gerar um mapa-guia (PNG leve) do Sudeste: costa, rios, rodovias, contornos urbanos e nomes.
- Regras: todas as localidades possíveis, classificadas por categoria (metrópole, grande, média, pequena, vilarejo), com o núcleo mínimo e o bônus turístico (D-22); quais rodovias e rios.
- Catálogo de células com conteúdo, separado por estado (para gerar o RJ primeiro e os outros depois).

**Pronto quando:** o usuário aprovar o mapa-guia e as regras.

### Etapa 2: Cidade piloto, Rio de Janeiro (ponta a ponta)

- **2.1** Kit de cidade v1: malha de ruas com curvas no padrão do jogo base (D-21), quadras e lotes; plantas de casa brasileiras com cômodos e mobília do jogo (seção 6.1); comércio e serviços essenciais; estilo brasileiro com tiles do jogo + as primeiras tiles brasileiras novas, cada uma com 3D no Viewpoint (D-09); zumbis pela população; zonas de veículos e de eventos.
- **2.2** Gerar um pedaço (ex.: Centro + Zona Sul) → compilar → testar → feedback → ajustar o kit.
- **2.3** Geografia: baía, praias, lagoa e morros. No isométrico, os morros aparecem como rocha e mata; no Viewpoint, como relevo real (D-26/D-27), com as ruas e os prédios das encostas em patamares nivelados.
- **2.4** Marcos do Rio (começando pelos obrigatórios da seção 6.1: Cristo, Pão de Açúcar, Candelária), seguindo o procedimento da seção 8, já com 3D.
- **2.5** Cena piloto: engarrafamento na Av. Brasil. É o primeiro teste de cena característica.
- **2.6** Rio completo + spawns + mapa in-game + mapa de papel.

**Pronto quando:** o usuário jogar no Rio (isométrico e Viewpoint) e aprovar: dá para lootear as casas, há zumbis para enfrentar e os eventos aparecem. Aí o kit v1 é congelado.

**Depois do Rio aprovado: 2.7 Relevo visual (addon opcional, D-26/D-27/D-28/D-30)**

1. Descobrir como o Viewpoint guarda a altura do terreno e como a parte visual do Rolling Hills (MIT) mexe nela.
2. Protótipo da Zona Sul do Rio (Corcovado + Pão de Açúcar) com altitudes reais, só visual, sem física. **Gerar as duas versões do arquivo de altitudes (altura 1:10 e 1:15) e comparar lado a lado**; o usuário escolhe vendo em jogo. **Começar pelo Pão de Açúcar** (o menor, ~40 m).
3. Conferir se fica bonito, se os prédios das encostas ficam em patamares, a distância de visão, se o isométrico continua intacto e se tudo continua funcionando no Viewpoint base com o addon desligado.
4. **Teste D-30:** no Pão de Açúcar, montar o trajeto visitável (escadaria/trilha com patamares até o mirante). Medir o FPS e o peso (memória) com os andares, conferir o visual da subida e a **vista do alto** no Viewpoint (quanto da cidade aparece, distância de visão), e se nada muda no isométrico.
5. Mostrar ao usuário antes de seguir. Se o relevo falhar, usar o plano B do Corcovado (seção 6.1). Se o trajeto do Pão de Açúcar falhar, voltar ao D-28 (rocha sem escalada). Só depois de aprovado, repetir a ideia no Corcovado.

### Etapa 3: Entre cidades (corredor de teste)

- Corredor: Rio → Baixada → Petrópolis pela BR-040. Testa a cidade emendada na Baixada, a estrada de serra com curvas exageradas (D-23) e a representação da serra. Alternativa: a Ponte Rio–Niterói (~890 tiles a 1:15).
- Rodovias com postos, pedágios, acostamento e placas; histórias de veículo nas estradas; rios e pontes; o campo conforme o resultado do T4; cidades pequenas automáticas no caminho.

**Pronto quando:** a viagem pelo corredor for aprovada.

### Etapa 4: RJ completo e beta pública

- Rodar o gerador no resto do estado do RJ (D-24). Revisar com atenção especial a Baixada e a Região Serrana (Petrópolis, Teresópolis, Nova Friburgo/Lumiar, Macaé/Sana).
- Marcos principais e cenas características do RJ (P8).
- Revisão por amostragem: o usuário visita algumas cidades do estado.
- Publicar a **beta pública na Workshop, só com o RJ** (D-33): descrição bilíngue explicando que SP, MG e ES virão em atualizações, créditos (OSM/ODbL, IBGE, cobertura do solo, KnoxMap/compilador se usados, Tripo), teste em servidor dedicado, changelog, tag WIP.

**Pronto quando:** o RJ inteiro carregar, for jogável e a beta estiver publicada.

### Etapa 5: Kit Brasil (tiles novas + 3D)

Pode começar logo depois da beta; cada melhoria sai como atualização.

- Placas em português, fachadas (padaria, farmácia, boteco, posto, mercadinho), orelhão, ponto de ônibus, banca etc.
- Móveis ficam de fora: a mobília é sempre a do jogo (D-16).
- Cada tile nova ganha modelo 3D no Viewpoint.
- Trocar no kit e gerar de novo (sem trabalho manual). Para quem já joga, as mudanças só aparecem num save novo (D-34).

### Etapa 6: Jogabilidade e acabamento

- Eventos brasileiros próprios (seção 6.1).
- Equilíbrio de loot e zumbis, spawns por cidade, mapas de papel, traduções pt-BR/EN, opções de sandbox.
- Desempenho das cidades grandes.
- Ajustes pedidos pelos jogadores da beta.

### Etapa 7: Expansão do Sudeste (atualizações do mesmo mod)

- Rodar o gerador estado por estado: SP → MG → ES (D-24), já com o kit melhorado das Etapas 5 e 6.
- Marcos principais e cenas características de cada estado (P8).
- Revisão por amostragem: o usuário visita algumas cidades de cada estado.
- Cada estado sai como uma versão grande do mesmo mod, com aviso de que pede save novo (D-34).

**Pronto quando:** o Sudeste inteiro carregar e for jogável.

### Etapa 8: Versão completa (1.0)

- Revisão geral, changelog, descrição final na Workshop; tirar a tag WIP quando o usuário decidir.

### Fora do escopo atual: outras regiões

Sul, Centro-Oeste, Nordeste e Norte não fazem parte deste projeto (decisão de 06/11/2026). Se um dia vierem, serão projetos à parte, reaproveitando scripts e kits, com a própria grade e escala.

---

## 8. Regras de trabalho para o Claude

- Responder em pt-BR e explicar sem jargão: o usuário não programa.
- **Problemas conhecidos (pedido do usuário em 07/11/2026):** manter `PROBLEMAS_CONHECIDOS.md` com cada erro já visto, a causa e a solução. Ler antes de cada tarefa e acrescentar todo erro novo resolvido na mesma sessão, para não repetir os mesmos bugs.
- Mostrar antes de refazer; não refazer modelos automaticamente.
- Modelos 3D: mostrar também em primeira pessoa de frente, direita, trás e esquerda (sem cima/baixo). Basta estilizado; precisão de pixel só se o usuário pedir.
- Atualizar os arquivos direto no PC, sem zips.
- O mod é só mapa (D-20): sem veículos novos e sem móveis novos. Tiles novas podem, sempre com 3D no Viewpoint.
- O 3D de uma tile nova só aparece no Viewpoint; o isométrico continua sendo a sprite.
- **Versão do jogo (D-12):** o mod acompanha sempre a versão mais recente do Project Zomboid (hoje, B42.22). Quando sair versão nova, avisar o usuário e checar a compatibilidade (inclusive a do Viewpoint) antes de seguir.
- Procedimento para cada marco ou tile nova (adaptado do "Básico 01" do Living Props):
  1. Definir a sprite isométrica (todas as direções).
  2. Ver se já existe algo parecido no jogo ou no Viewpoint para reaproveitar.
  3. Ver se um modelo serve para as 4 direções.
  4. Modelar.
  5. Registrar no Viewpoint sem editar arquivos de outros mods.
  6. Montar um exemplo no jogo e pedir feedback.
- Teste pequeno antes de grande.
- Fim de sessão: atualizar a seção 1 e o registro (e o `AGENTS.md`, se alguma decisão mudou).
- **Modelo e esforço (regra de 06/11/2026):** conferir a tabela da seção 10 no começo de cada tarefa, mas só avisar o usuário quando for **necessário trocar** o modelo ou o esforço (para um mais forte ou para um mais leve). Se o atual serve, trabalhar normalmente, sem pedir confirmação. Quando avisar, esperar o usuário trocar ou dizer "continue com o modelo atual" / "continue mesmo assim".

---

## 9. Perguntas em aberto

- P1 respondida: tiles brasileiras novas podem, sempre com 3D no Viewpoint (D-09).
- P2 respondida: o nome é Real Sudeste Brasil (D-14).
- P3 respondida: o usuário tem conta no GitHub, então usamos um repositório privado (D-25).
- P4 respondida: Cristo, Pão de Açúcar, Candelária e outros pontos famosos (seção 6.1).
- P5 respondida: entram todas as localidades possíveis, com núcleo mínimo e bônus turístico (D-22).
- P6 respondida: RJ → SP → MG → ES (D-24).
- P7: hardware do PC. Claude verifica sozinho na Etapa 0.
- P8 respondida: a lista de cenas do cotidiano está na seção 6.1 (D-18).
- P9 respondida: armas no equilíbrio do jogo base, por enquanto (D-19).
- P10 (nova, 06/11/2026): o Pão de Açúcar visitável (D-30) e o relevo real (D-26) valem a pena depois de ver em jogo? Resposta só na Etapa 2.7.
- P11 respondida (06/11/2026): a casa de chefe é sorteada por regra em favelas de porte médio/grande do RJ, sem nomear comunidades (D-31). Itens: só os do jogo base; tiles/modelos 3D decorativos de drogas ficam como proposta (D-32).
- P12 (nova, 07/11/2026): densidade da mata. Menos densa (dá para ver e andar) ou mais densa (realismo da Mata Atlântica)? Na Urca de teste, mesmo com a mata reduzida à metade, o usuário achou que se vê pouco à frente. Decidir na Etapa 2, vendo em jogo na escala 1:15.
- P13 (nova, 07/11/2026): vagas de carro fidedignas. O usuário não quer vagas onde não existe algo parecido na vida real (há ruas no RJ sem lugar para estacionar). Ideia a testar: usar o que o OSM marca (`parking:lane`/`parking:both`/`parking:left`/`parking:right` nas ruas e `amenity=parking` nos estacionamentos) e, onde o OSM não diz nada, uma regra por tipo de rua (ex.: via expressa sem vaga; rua residencial com vaga). Resolver no nosso gerador (Etapa 2).

---

## 10. Como economizar tokens

1. Comece cada sessão assim: "Leia o PLANO_BRASIL_ZOMBOID.md e continue". Não precisa explicar o projeto de novo.
2. Uma conversa por tarefa. Conversa longa fica cara, porque todo o histórico é reprocessado a cada mensagem. Terminou uma tarefa ou a conversa ficou grande? Peça "atualize o plano" e abra uma conversa nova.
3. Junte o feedback numa mensagem só, em lista numerada, em vez de várias mensagens curtas.
4. Prints com moderação. Imagem custa bem mais que texto. Recorte no que importa; um print mostrando várias coisas vale mais que vários prints.
5. Não cole arquivos nem logs grandes. Diga onde o arquivo está, e o Claude lê só o trecho necessário (por exemplo, só o erro do console.txt).
6. Scripts em vez de conversa. Trabalho repetitivo vira script; o Claude lê só o resumo do resultado.
7. Testes pequenos primeiro. Um erro em 1 célula custa pouco para achar; em 100 células custa muito.
8. As decisões ficam neste arquivo. Não precisa rediscutir. Se algo mudar, é só atualizar a tabela.
9. Índices em vez de vasculhar. O catálogo de tiles e prédios é gerado uma vez por script, e o Claude consulta o catálogo em vez de varrer os arquivos do jogo toda vez.
10. Git: com repositório, o Claude vê só o que mudou em vez de reler tudo.
11. Modelo certo para cada tarefa: os modelos mais leves gastam menos do seu limite. Use o mais forte para planejar e resolver bugs difíceis, e um mais leve para tarefas mecânicas (rodar scripts, ajustes simples).
12. Peça respostas curtas quando só quiser o resultado.

### Modelo e esforço recomendados por tarefa

> **Como mudar:** clique no nome do modelo, ao lado do botão de enviar → Esforço (Effort). Os níveis vão de Baixo (Low) e Médio (Medium) até Alto (High), Extra alto (xhigh) e Máximo (Max).
> **Regra de bolso:** quanto mais alto o esforço, melhor o raciocínio, mas mais tokens gastos. Médio para rotina; Alto como padrão para trabalho difícil; Extra alto só em programação longa e complexa; Máximo só se travar.

| Tarefa | Modelo | Esforço |
|---|---|---|
| 0.1 Instalar ferramentas, criar pasta e repositório | Sonnet | Médio |
| Testes T1–T9 (Etapa 0) | Opus | Alto |
| Etapa 2.7: relevo visual (desvendar o Viewpoint, addon) | Opus | Extra alto |
| Etapa 1: grade, projeção e regras | Opus | Alto |
| Etapa 1: baixar e processar dados, mapa-guia | Sonnet | Médio |
| Etapa 2: primeira versão do gerador e do desenho de ruas (D-21) | Opus | Extra alto |
| Etapa 2: kit de casas e primeiro marco (Cristo) | Opus | Alto |
| Etapa 2: ajustes do kit, marcos seguintes, cena da Av. Brasil | Sonnet | Alto |
| Etapa 3: estradas de serra | Opus | Alto |
| Etapa 3: ajustes do corredor | Sonnet | Médio |
| Etapas 4 e 7: rodar o gerador (resto do RJ; depois SP, MG, ES) | Sonnet | Médio |
| Etapas 4 e 7: corrigir problemas achados na revisão | Sonnet | Alto (Opus Alto se não resolver) |
| Etapa 5: tiles brasileiras + 3D | Sonnet | Alto (Opus Alto na primeira de um tipo novo) |
| Etapa 6: primeiro evento brasileiro (o molde) | Opus | Alto |
| Etapa 6: demais eventos, equilíbrio de loot e zumbis | Sonnet | Médio |
| Etapas 4, 7 e 8: textos da Workshop, empacotar, publicar | Sonnet | Médio |
| Qualquer etapa: conferir arquivos, atualizar o plano, traduções simples | Haiku | Baixo ou Médio |
| Bug difícil que travou depois de 2 tentativas | Opus | Máximo (ou Fable, se disponível no plano) |

### Estimativa de esforço (inicial; revisar depois da Etapa 0)

Uma "sessão" é uma conversa focada numa tarefa.

| Etapa | Sessões |
|---|---|
| 0 | 8–15 |
| 1 | 4–8 |
| 2 | 15–30 |
| 3 | 5–10 |
| 4 (RJ completo + beta) | 5–10 |
| 5 | 10–20 |
| 6 | 10–15 |
| 7 (SP, MG, ES) | 12–25 |
| 8 (1.0) | 2–4 |
| **Total** | **~70–135** |

A **beta do RJ** (fim da Etapa 4) fica em ~37–73 sessões: cerca de 3 a 6 meses a 3 sessões por semana, ou 2 a 3,5 meses a 5 por semana (estimativa de 06/11/2026). A Etapa 0 é a mais incerta e vai calibrar o resto.

### Ferramentas externas (usadas pelo usuário, para poupar tokens)

- **Tripo (D-29):** gerar modelos 3D a partir de fotos (estátuas, monumentos, objetos). O usuário gera o modelo base e o Claude só limpa, reduz e registra no Viewpoint.
  - No plano grátis, o limite de downloads é baixo: escolha antes de gerar uma versão de modelo que o plano grátis deixa baixar.
  - Os modelos ficam públicos na galeria do Tripo.
  - Colocar crédito ao Tripo na descrição da Workshop.
  - Usar fotos próprias ou com licença livre (Wikimedia Commons).
  - Alternativas: TRELLIS 2 (licença MIT) e Meshy (CC BY 4.0).
  - Guia de prompts, ajustes e exemplos: `GUIA_PROMPTS_TRIPO.md` (criado em 06/11/2026). Usar antes de gerar qualquer modelo.
- **Blender:** conferir modelos nas 4 direções, simplificar (Decimate) e exportar em OBJ.
- **QGIS:** ver o mapa-guia e ajustar contornos à mão.
- **Google Earth e Street View:** referências de marcos e de casas brasileiras.
- **WorldEd/TileZed (PZ Mapping Tools):** consertos pequenos e visuais no mapa.
- **GIMP, Krita ou LibreSprite:** desenhar e retocar tiles brasileiras.
- **GitHub Desktop:** ver o que mudou e desfazer.
- **VS Code ou Notepad++:** abrir o console.txt do jogo e mandar ao Claude só as linhas do erro.
- **Win + Shift + S:** recortar prints.

---

## 11. Riscos

| ID | Risco | O que fazemos |
|---|---|---|
| R1 | 1:15 no Sudeste (~367×321 células; ~62.700 de terra) fica abaixo do Real USA (472×304; ~5.050 km²), mas ainda é grande e as cidades pesam | T2 testa as coordenadas extremas; T6 mede o peso; só compilar onde tem conteúdo |
| R2 | As ferramentas oficiais da B42 ainda não saíram | Usar as comunitárias; avaliar a migração quando as oficiais saírem |
| R3 | Desconfiança e denúncias contra mods em Java (houve boato de minerador no Real USA) | Mapa principal sem Java; o Java fica só no addon opcional de relevo; código aberto no GitHub; créditos corretos; nada de terceiros sem permissão |
| R4 | Download gigante (o Real USA tem ~9 GB) | Medir no T6; só compilar o que tem conteúdo; divisão interna do mod único só se precisar (D-11) |
| R5 | Tiles novas quebrarem no Viewpoint | T5 logo no início; toda tile nova com modelo 3D |
| R6 | Licenças (ODbL do OSM; licença mista do KnoxMap) | Atribuição no mod; não copiar código sem licença |
| R7 | Atualização do jogo mudar o formato do mapa ou quebrar mods (o alvo é sempre a versão mais recente, D-12) | Registrar a versão usada; checar a compatibilidade a cada versão nova (inclusive a do Viewpoint); tudo é regerável por script (D-10) |
| R8 | Cidades grandes pesadas (engasgos) | Medir no piloto (o Rio é grande); ajustar a densidade no kit |
| R9 | Compilar demora (um processo por vez) | Compilar só as células que mudaram |
| R10 | Eventos e loot dependem de zonas e nomes de cômodo corretos | T8; o gerador sempre cria as zonas; toda casa tem cozinha, banheiro e quarto |
| R11 | Curvas ficarem "em degraus" (problema conhecido do KnoxMap) | Desenho de ruas próprio (D-21), testado logo no T9 |
| R13 | O relevo depende do jeito interno do Viewpoint, que está em alpha e muda rápido | Addon separado, opcional e só visual (o mapa funciona sem ele no Viewpoint base); feito só depois do Rio aprovado (2.7); registrar a versão do Viewpoint testada |
| R12 | Cristo Redentor: os direitos patrimoniais são da Arquidiocese do Rio, que já vetou usos que considerou desrespeitosos. Por outro lado, a Justiça do RJ já decidiu que a reprodução só ilustrativa de obra em local público não precisa de autorização (art. 48 da Lei 9.610/98) | Representar com respeito (nada de destruir ou profanar a estátua) e em versão estilizada, num mod gratuito. Se surgir reclamação, basta gerar o mapa de novo sem esse carimbo (D-10). Pedir autorização à Arquidiocese é opcional. Não é parecer jurídico. |
| R14 | Pão de Açúcar visitável (D-30) pesar demais (muitos andares visíveis) ou ficar feio com degraus | Medir FPS e memória no protótipo (2.7), começando pelo Pão de Açúcar; trajeto estreito em vez da montanha inteira; se falhar, voltar ao D-28 |
| R16 | Atualizações de mapa (estado novo, kit novo) não aparecerem nos saves antigos: confirmado por pesquisa (06/11/2026), o jogo só carrega mapa novo em áreas nunca visitadas | D-34: save novo recomendado nas versões que mudam o mapa; poucas versões grandes; aviso claro no changelog e na descrição |
| R15 | Casa de chefe (D-31) ligada a nomes de comunidades reais: estigma contra quem mora lá e risco de reclamações ou denúncias na Workshop | Sorteio por regra, sem nomear comunidades reais (decidido em P11); o "chefe" é uma figura fictícia; tiles de drogas (D-32) só decorativas e conferidas com as regras da Workshop antes de publicar |

---

## 12. Registro

- **05/11/2026:** planejamento pelo celular. Pesquisa inicial (Real USA, KnoxMap, estado das ferramentas da B42). Decididos D-01, D-03 a D-08 e D-12. Próximo passo: Etapa 0.
- **05/11/2026 (22h):** adicionadas as diretrizes de jogabilidade (D-15 a D-18, seção 6.1): casas com cômodos e mobília realistas, mapa survival friendly, eventos do jogo e brasileiros, cenas características (ex.: Av. Brasil). Novo teste T8 e perguntas P8–P9. Ainda no mesmo dia, o usuário decidiu: nada de móveis novos, só a mobília do jogo arrumada no jeito brasileiro.
- **05/11/2026 (22h10):** P8 respondida, com a lista de cenas do cotidiano na seção 6.1. P9 respondida: armas no equilíbrio do jogo base (D-19). Nova regra D-20: o mod é só mapa, sem veículos novos (só os do jogo base); tiles novas podem, com 3D no Viewpoint.
- **05/11/2026 (22h20):** D-21: ruas e estradas com curvas como no jogo base, nunca "em degraus". Novo teste T9 e risco R11.
- **05/11/2026 (22h23):** D-09 confirmado: tiles brasileiras novas permitidas, sempre exibidas em 3D no Viewpoint.
- **05/11/2026 (22h35):** nome Real Sudeste Brasil (D-14); GitHub privado (D-25); marcos do Rio (Cristo, Pão de Açúcar, Candelária + outros); todas as localidades com núcleo mínimo e bônus turístico (D-22); destaques: Rio, Baixada e Região Serrana (Petrópolis, Teresópolis, Lumiar, Sana); serra com curvas exageradas (D-23); ordem RJ → SP → MG → ES (D-24); corredor de teste Rio → Petrópolis; risco R12 (Cristo). Pasta do projeto renomeada para RealSudesteBrasil.
- **05/11/2026 (22h45):** corrigido o erro sobre a "remoção" do Real USA e do ZombieBuddy (era texto escondido das páginas da Workshop). Relevo real no Viewpoint como addon opcional em Java (D-26), com altura 1:10 (D-27). Novo teste T10 e risco R13.
- **05/11/2026 (22h50):** D-28: morros e marcos em forma mista (Cristo como modelo; Corcovado com relevo para subir a pé e de carro; Pão de Açúcar, Dedo de Deus e Pedra da Gávea como rocha esculpida em 3D; plano B do morro de andares). Teste T5c. Modelo recomendado por etapa e estimativa de esforço na seção 10. Planejamento encerrado; próximo passo: Etapa 0 no PC.
- **05/11/2026 (22h55):** tabela de modelo + esforço por tarefa (seção 10) e nova regra: o Claude recomenda modelo e esforço no começo de cada tarefa (seção 8).
- **05/11/2026 (23h):** D-29: o Tripo gera modelos 3D a partir de fotos (mod gratuito, com crédito ao Tripo). Lista de ferramentas externas na seção 10.
- **05/11/2026 (23h26):** relevo só visual, sem física por enquanto; prioridade é o mapa funcionar bem com o Viewpoint base. O teste de relevo (antigo T10) saiu da Etapa 0 e virou a Etapa 2.7, depois do Rio aprovado.
- **06/11/2026:**
  - D-12 atualizado: o mod acompanha sempre a versão mais recente do jogo; hoje, B42.22 (seção 1, seção 8 e risco R7).
  - Relevo real no Viewpoint continua (D-26/D-27), mas a decisão final só sai depois de ver como fica em jogo (Etapa 2.7).
  - Novo D-30 (PROPOSTO): testar um Pão de Açúcar visitável (trajeto de escadas até um mirante, com vista do alto), começando por ele no protótipo da Etapa 2.7. D-28 continua valendo se o teste falhar. Novos: pergunta P10 e risco R14. Anotado também o limite de 32 andares da B42 e o cuidado com o plano B do Corcovado (~36 andares com a estátua, a verificar).
  - Criados o `AGENTS.md` e o `CLAUDE.md` do projeto (resumo para qualquer IA ler automaticamente).
  - Regra de modelo/esforço ajustada (seção 8): o Claude só avisa quando for necessário trocar; se o atual serve, trabalha normalmente.
  - **D-01 mudou:** escala **1:15** (1 tile = 15 m) e escopo **só o Sudeste** (antes: 1:20 para o Brasil inteiro). Atualizados: tabelas de tamanho (seção 3), D-02, D-03, D-27, fórmula da grade (seção 6), T2, T7, corredor da Etapa 3, R1 e glossário. Outras regiões saíram do escopo. Tamanho novo: ~4.109 km² e ~62.700 células de terra (≈ 81% do Real USA). O relevo continua em 1:10 (D-27), agora 1,5× a proporção horizontal.
  - Relevo: na Etapa 2.7 vamos testar os dois, altura 1:10 e 1:15, lado a lado (D-27); o usuário escolhe vendo em jogo. O arquivo de altitudes é gerado por script, então trocar é barato. O Cristo continua sendo um modelo 3D à parte (D-28/D-29), colocado sobre o topo do Corcovado.
  - Novo D-31 (PROPOSTO): casa de "chefe do morro" nas favelas do RJ (ostentação, riquezas, armas e itens do tráfico). Nova pergunta P11 (onde e quais itens) e risco R15.
  - D-33 DECIDIDO: RJ primeiro (beta só do RJ, fim da Etapa 4), depois SP, MG e ES como atualizações do mesmo mod, em 1:15. Etapas 4 a 8 reorganizadas; risco R16; estimativas atualizadas.
  - D-34 (PROPOSTO): atualizações que mudam o mapa pedem save novo. O usuário avisou e a pesquisa confirmou que outros mods de mapa não conseguem manter o save (mapa novo só aparece em áreas nunca visitadas). O T10 (expansão e saves), criado no mesmo dia, foi retirado.
  - D-11 DECIDIDO: um mod só para o jogador, não um mod por estado (divisão interna só se o T6 exigir). T3, T6, R1, R4 e a seção 6 ajustados.
  - P11 respondida: casa de chefe sorteada por regra, sem nomear comunidades; D-31 passa a DECIDIDO. Novo D-32 (PROPOSTO): tiles e modelos 3D decorativos representando drogas, só nesses ambientes.
- **06/11/2026 (encerramento da sessão):** criados a imagem conceitual do RJ (`RJ_mapa_conceito.png`, só ilustração, não é do jogo) e o `GUIA_PROMPTS_TRIPO.md`. Revisão final do plano e do `AGENTS.md`. Seção 1 atualizada com a lista do que ainda está PROPOSTO (D-30, D-32, D-34, altura do relevo). Nenhuma decisão DECIDIDO foi alterada nesta revisão. Próxima ação: Etapa 0.1 no PC (Claude verifica o hardware e instala as ferramentas). Sem pendência técnica aberta.
- **07/11/2026:** discutidos o post do Reddit sobre o mapa 1:10 da Europa com KnoxMap (sem mudança no plano), a troca para 1:10 (**não decidida**; D-01 continua em 1:15) e distâncias no jogo base (West Point–Louisville: ~4,8 km em linha reta, ~6 km por estrada, estimativa). Novo D-35 (PROPOSTO): cidades de rodovia com recursos variáveis, definidas na geração do mapa.
- **07/11/2026 (tarde, notebook):** criada a pasta do projeto no notebook Acer Nitro V15, na Área de Trabalho (`C:\Users\yanbe\OneDrive\Área de Trabalho\RealSudesteBrasil\`), com `PLANO_BRASIL_ZOMBOID.md`, `AGENTS.md`, `CLAUDE.md`, `GUIA_PROMPTS_TRIPO.md` e as subpastas `dados`, `scripts`, `kits`, `marcos` e `saida` (cada uma com um `LEIA-ME.txt`). Uma primeira cópia foi criada em `C:\Users\yanbe\Zomboid\RealSudesteBrasil\`; o usuário deve apagá-la (Claude não tem como apagar daqui). Registrado o ambiente atual: notebook, não o PC potente; adiantar só o leve e testar só o isométrico por enquanto (seção 1 e `AGENTS.md`). A Área de Trabalho está no OneDrive: decidir na 0.1 onde ficam os dados grandes e o repositório Git. Nenhuma decisão DECIDIDO foi alterada. O usuário vai continuar o trabalho numa nova sessão no Claude Code.
- **07/11/2026 (tarde, Etapa 0.1 no notebook):** hardware verificado: Acer Nitro ANV15-51, i5-13420H (8 núcleos), 7,7 GB de RAM, RTX 3050 de 6 GB, SSD de 477 GB com 355 GB livres. Instalados: só Project Zomboid (jogo na 42.21, ramo público) e o Viewpoint (Workshop 3809306528). Faltam Python, Git, GitHub CLI, KnoxMap e ferramentas de mapa (TileZed/WorldEd/BuildingEd); Real USA não está baixado. **Decisão do usuário:** desenvolver em `C:\Users\yanbe\Zomboid\RealSudesteBrasil\` (fora do OneDrive), e a Área de Trabalho vira cópia antiga; documentos copiados de lá (versão mais nova). Usuário confirmou que dá para desenvolver tanto na 42.21 quanto na 42.22 (pré-lançamento), pois não corrompeu mapa algum. O usuário aprovou instalar Python 3.12, Git e GitHub CLI; o winget falhou por falta de conexão (usuário em alto mar, nos dados móveis). **Combinado:** trabalhar offline por enquanto (organização, `.gitignore`, documentos) e instalar tudo quando houver sinal melhor; nada grande é baixado pelos dados móveis sem autorização. Nenhuma decisão DECIDIDO foi alterada.
- **07/11/2026 (Etapa 0.1, parte 1 concluída):** na segunda tentativa a conexão aguentou e foram instalados Python 3.12.10, Git 2.56.0 e GitHub CLI 2.103.3. Login no GitHub feito pelo navegador (conta `yanbernardo`; o primeiro código expirou por causa da internet lenta). Criado o repositório **privado** `https://github.com/yanbernardo/RealSudesteBrasil` (D-25) com o primeiro commit; `.gitignore` deixa `dados`, `saida` e `ferramentas` fora do Git. Autor dos commits configurado só neste repositório. **Pendente da 0.1:** KnoxMap (`CalvyPZ/knoxmap`), compilador e ferramentas de mapa da B42 (download grande; esperar autorização do usuário e conexão melhor). Não achei página oficial das ferramentas TileZed/WorldEd/BuildingEd da B42; só o fork `Unjammer/TileZed`. O instalador automático do Roblox foi encerrado a pedido do usuário (consumia a banda).
- **07/11/2026 (fim da sessão no notebook):** o usuário vai atualizar o app do Claude (v4.23118.0) e abrir uma sessão nova. Tudo está salvo e enviado ao GitHub. Modelo atual: Sonnet, esforço Médio (serve para a 0.1; os testes T1–T9 pedem Opus Alto, avisar na hora). Pendências para a próxima sessão: (1) KnoxMap e compilador: listar tamanho, pedir autorização, baixar com `git clone` em `ferramentas\`; (2) a 42.22 em pré-lançamento: o usuário disse que dá para desenvolver em qualquer uma das duas, mas registrar a versão usada em cada teste (D-12); o jogo instalado está na 42.21; (3) Real USA (Workshop 3829712469) não está baixado e serve só de referência: perguntar antes de baixar; (4) apagar a cópia antiga da Área de Trabalho é com o usuário; (5) skill `novo-movel-3d` segue com o usuário.
- **07/11/2026 (Etapa 0.1 concluída no notebook):** KnoxMap (CalvyPZ/knoxmap, ~17 MB) clonado em `ferramentas\knoxmap\`, com dependências num ambiente isolado (`.venv`). Ferramentas de edição (PZ Mapping Tools, BuildingEd Studio) adiadas. Jogo na 42.21. Real USA não baixado. Um `C:\Projetos\RealSudesteBrasil` criado por engano pode ser apagado pelo usuário. (Esta entrada estava solta no fim do arquivo, depois das Fontes; foi movida para cá.)
- **07/11/2026 (Etapa 0.2: T1 e T7 no notebook, jogo 42.21):**
  - **Troca de versão do KnoxMap:** o clone do `CalvyPZ/knoxmap` (10/10/2026) exigia compilar o compilador em Rust (instalar Rust + ferramentas de C++, vários GB). O pacote oficial **v1.8.5.2** (`spytheeuclidean-a11y/knoxmap`, 06/11/2026, 3 MB) já traz os compiladores prontos (`knoxlots.exe`, `knoxroute.exe`). Instalado em `ferramentas\knoxmap-1.8.5.2\`. O clone antigo ficou em `ferramentas\knoxmap\` só como referência de código.
  - **Downloads autorizados pelo usuário (~95 MB no total):** PZ Mapping Tools 43.00B260909 (40 MB), PZWorldEd_cli (6 MB), pacotes Python fixados (~22 MB), Visual C++ 14.51 da Microsoft (18 MB; o KnoxMap novo exige ≥ 14.51 e o notebook tinha 14.42) e os dados do bairro pela Overpass (poucos MB). **Não** foi baixado o extrato do Sudeste da Geofabrik (863 MB).
  - **T1 (caminho completo): passou na parte técnica, falta jogar.** Urca, retângulo de ~830 × 770 m a 2 m/tile: 901 elementos do OSM, 359 prédios mobiliados, 9 células (600 × 600 tiles), compilação em 10 s, mod instalado com 9,9 MB em `Zomboid\mods\rsb_t1_urca` (com mapa de papel, 8 pontos de nascimento e 31 vagas de carro). A imagem do mapa compilado (`saida\t1_urca\urca_compilada.png`) mostra prédios de vários andares, calçadas e grama. O KnoxMap girou o mapa 32° para alinhar as ruas (o norte não fica para cima) e o colocou sozinho a partir da célula 70,0 (assunto do T2). Download do bairro pela Overpass: ~10 min (internet móvel). Primeira tentativa errou o retângulo (pegou mar); corrigido com a contagem de prédios do OSM. **Pendente:** o usuário abrir o jogo, ativar o mod "RSB Teste T1 - Urca", começar um jogo novo e conferir na visão isométrica.
  - **T7 (modo "inventado" a 1:15): não.** (a) Só o contorno, desenhado como área de casas a 15 m/tile: chão vazio, 0 ruas, 0 prédios. (b) Contorno + 6 ruas desenhadas à mão: as ruas aparecem e compila (4 células, 1,4 MB), mas 0 prédios. O código confirma: o preenchimento do KnoxMap (`infill`) só completa buracos entre prédios que já existem numa rua ("não funda uma cidade"); casas extras só vêm de endereços do OSM ou da Overture. Ele aceita 15 m/tile (limite 0,5–100), mas avisa que o normal é 1–8 m/tile; a 15 m/tile um prédio real de 10 m vira menos de 1 tile. **Conclusão:** o "motor das cidades" (D-03) terá de ser nosso: um gerador que desenhe ruas e lotes em escala de jogo dentro do contorno real. O KnoxMap continua útil como **montador**: recebe ruas e prédios como se fossem do OSM (formato `sketch`/GeoJSON), mobilia, compila e instala. A ser confirmado num T7c (nosso gerador simples + KnoxMap montando).
  - Mods de teste instalados: `rsb_t1_urca` e `rsb_t7b_ruas` (só aparecem se forem ativados no jogo).
  - **T1 no jogo (usuário, jogo 42.21, notebook): passou.** O mapa carrega; há loot, móveis, interruptores e zumbis (bastantes); o mapa de papel mostra as ruas. Problemas achados (U1–U11 em `PROBLEMAS_CONHECIDOS.md`): mureta da orla virou muro alto; paredes incompletas em prédios girados; prédio suspenso sobre a rua virou cômodo no meio da rua; prédios de um cômodo só; visual americano; ruas finas e orla como concreto; nenhum carro; nomes de rua no mar no mapa de papel; mata densa demais; travadas (notebook). **Combinado:** não polir a Urca. Ela foi feita a 2 m/tile com prédios reais, e o mod final é 1:15 com o nosso gerador (T7), então quase tudo isso se resolve no gerador (Etapa 2) e no Kit Brasil (Etapa 5). O que vale para qualquer escala (carros, nomes no mar, densidade de mata) será investigado no T8 e no T7c.
  - **Urca independente (D-36) testada no jogo pelo usuário (42.21):** gerada de novo como mapa independente (células 0,0 a 2,2, sem Knox County), com vagas no máximo (`parking_density` 4.0: 54 vagas, eram 31) e mata reduzida (`forest_density` 0.5, `tree_density` 0.7). Resultado: carrega só a Urca; nascimento, loot e zumbis funcionam **sem o mapa original**; carros apareceram (com a frequência de veículos do jogo em Muito alta), então as vagas funcionam e o problema era só quantidade. Continuam: nomes de rua no mar no mapa de papel (U8) e mata ainda densa (virou a P12).
  - **T2: parte 1 passou** (o jogo aceita o nosso mapa sozinho, D-36). Falta a parte 2: uma célula no ponto mais distante do Sudeste a 1:15.
  - **T8: parte 1 passou** (loot residencial normal; carros aparecem nas vagas). Faltam: eventos/histórias, loot comercial, catálogo de cômodos/loot/zonas e a viagem de rodovia (D-35).
  - **T7c (gerador simples nosso + KnoxMap como montador): o mecanismo funciona.** `scripts\gerador\gerador_t7c.py` pega o contorno real de Botafogo (Nominatim, 2,6 KB, em `dados\contornos\`), encolhe a 1:15 (4,79 km² → 220 × 180 tiles) e enche de ruas e lotes em escala de jogo: malha alinhada ao grid (norte para cima, D-02), quarteirões de ~46 × 38 tiles, avenida a cada 3 ruas e lotes de casa (7–9 × 8–10 tiles, 1–2 andares), prédio (3–6 andares) e loja. **Truque de escala:** o desenho vai ao KnoxMap num espaço "falso" de 1 m por tile, então as ruas saem com a largura do jogo (~7 tiles, com calçada, meio-fio e faixa) e o bairro inteiro mantém o tamanho real a 1:15. Resultado: 8 ruas, 10 quarteirões, 53 prédios mobiliados, 4 células, compilado em 5 s e instalado como `rsb_t7c_botafogo` (independente). Imagem: `saida\t7c\botafogo_trecho.png`. **Observações:** (1) a 1:15, Botafogo inteiro cabe em ~10 quarteirões de jogo, enquanto o real tem bem mais; é a consequência esperada do D-01 e do D-03, mostrar ao usuário; (2) os lotes ficaram espaçados demais e alguns quarteirões viraram piso de concreto (o KnoxMap pavimenta em volta de loja e prédio); (3) não recorta mar e morro: o contorno é enchido todo. Próximos ajustes do gerador ficam para a Etapa 2 (lotes mais cheios, plantas brasileiras, vagas fidedignas P13, recorte de água e morro, ruas reais principais como eixo).
  - **T7c no jogo (usuário, 42.21): passou.** O tamanho ficou bom para um bairro (o usuário aprovou o "Botafogo resumido" a 1:15); ruas em tamanho certo; prédios entram e têm móveis. Achados U12–U16: mapa de papel sem ruas (corrigido no `knoxmap_pipeline.py`; faltam nomes e áreas verdes), faixas fora do centro, subsolo com 10+ máquinas de lavar, áreas pavimentadas vazias e acabamento americano. **Ideia do usuário (mobiliário urbano):** orelhões, bancas de jornal, pontos de ônibus, mesas e cadeiras de bar nas calçadas largas, onde fizer sentido; jogo base onde houver, Kit Brasil para o resto. Nas bordas, o bairro termina em gramado (esperado; os vizinhos preenchem no mapa grande). **Com isso o T7 está respondido:** o motor das cidades é o nosso gerador + KnoxMap como montador (D-13).
  - **T9 (curvas): não passou com o KnoxMap como está.** Teste: Av. Niemeyer real (Overpass, 30 KB, `dados\contornos\niemeyer.json`) encolhida a 1:15 (245 tiles de comprimento), desenhada como avenida e montada nos 4 modos de rua do KnoxMap (`straight_roads`), mais variantes (`scripts\testes\t9_niemeyer.py`; imagens em `saida\t9\`). Comparada com uma curva do jogo original (Oak St, Muldraugh, desenhada com `render_lots --world`). **Como o jogo base faz curvas:** trechos retos em 16 direções (reto, 2:1, 45°, 1:2) ligados por peças de curva, e as bordas das diagonais usam tiles cortados na diagonal, então ficam **lisas**. Cada trecho entre dois cruzamentos tem no máximo 1 ou 2 curvas. **Resultados:** modo 0 (como no mapa) segue a Niemeyer, mas tudo em degraus e com faixas quebradas; modo 1 (45°, Knox County) vira quinas; modos 2 e 3 (curvas do B42) dão a forma lisa do jogo, mas resumem a avenida a um "V" (perde as curvas reais), e a calçada continua em degraus. Variantes com acessos laterais (para criar cruzamentos) e com área urbana em volta (para a rua seguir o traçado de perto) não mudaram o resultado. **Conclusão:** o desenho de curvas vai ser nosso (D-21 e R11 confirmados): (1) o nosso gerador quebra a rua real em trechos de 16 direções com as curvas do jogo, mantendo o traçado; (2) as bordas diagonais precisam dos tiles cortados do jogo base. Falta descobrir se o KnoxMap tem esses tiles (ver a regra de meio-fio e chão) ou se fazemos esse acabamento nós. Vai para a Etapa 2 (antes de qualquer rua sinuosa do Rio).
  - **Assinatura do KnoxMap no chão:** o KnoxMap escreve "KNOXMAP BY EUCLID80TR" com piso no gramado perto de onde o jogador nasce (`knoxbuild\credit_ground.py`); apareceu no T9. Não há opção para desligar; essa parte é MIT (pode ser modificada). O crédito também vai no `ATTRIBUTION.txt` e na página da Workshop. **Decidido (D-37):** manter, mas uma vez só, num lugar escolhido pelo usuário.
  - **Fim da sessão (07/11/2026, noite):** o trabalho desta sessão está no ramo `claude/knoxmap-t1-t7-tests-a1a6a9` do GitHub (ainda não juntado ao `main`). Situação da Etapa 0.2: T1 ✔ (jogado); T7 ✔ respondido (não; motor = gerador nosso + KnoxMap); T7c ✔ (jogado); T9 ✘ (curvas serão nossas, K15); T2 parte 1 ✔ (mapa independente, D-36), **parte 2 pendente** (célula no ponto mais distante do Sudeste a 1:15); T8 parte 1 ✔ (loot residencial, carros nas vagas), resto pendente (eventos, loot comercial, catálogo de cômodos/loot/zonas, viagem de rodovia); T4 pendente; T3 só se o T6 pedir divisão; T5 e T6 esperam o PC potente. Decisões novas: D-36 (mapa independente) e D-37 (assinatura do KnoxMap uma vez só, em lugar a escolher). Perguntas novas: P12 (densidade da mata) e P13 (vagas fidedignas). Mods de teste instalados em `Zomboid\mods`: `rsb_t1_urca`, `rsb_t7b_ruas`, `rsb_t7c_botafogo` (ativar um por vez; todos são independentes). O usuário vai continuar num chat novo, começando pelo T2 parte 2.
  - **T2 parte 2 (08/11/2026, notebook): gerado e instalado; falta o usuário jogar.** O `main` já tinha o trabalho da sessão anterior. Reaproveitado o Botafogo do T7c (4 → 6 células compiladas, 2,1 MB) e **posicionado** pelo KnoxMap na célula **315,273** (a unidade do KnoxMap é a célula de 300 tiles, o teto é 400) = tile ~94.500 × 81.900 = células compiladas de 256 **369–370 × 319–321**, ou seja, o canto sudeste do Sudeste a 1:15 (~370 × 320). Nascimento em ~(94.640, 82.075), vagas e mapa de papel nas mesmas coordenadas (conferido nos arquivos). Mod `rsb_t2b_longe` ("RSB Teste T2b - Celula distante"). `scripts\knoxmap_pipeline.py` ganhou a opção `"cell": [x, y]` no config (usa `/api/placement`). Config: `scripts\testes\t2b_celula_distante.json`. **A confirmar em jogo:** o jogo carrega a célula longe da origem, sem Knox County, com nascimento, loot e zumbis. Se passar, **D-02** fica com origem no canto noroeste do retângulo do Sudeste (a calcular na Etapa 1 com o OFFSET que faz o canto sudeste cair em ≤ célula 400 de 300 tiles = 469 células de 256; folga boa: o Sudeste usa ~316 × 273 células de 300).
  - **T2 parte 2 no jogo (usuário, 42.21): passou.** A célula no canto sudeste do Sudeste (arquivos 369–370 × 319–321) carrega sem travar, sozinha; nascimento em casa de Botafogo, loot, móveis e zumbis normais; mapa de papel com ruas (sem nomes, já registrado em U12). **T2 respondido:** o jogo aceita coordenadas no extremo do Sudeste a 1:15 com mapa independente; D-02 pode ser fechado na Etapa 1. Ideia do usuário: o gerador colocar farmácias, lojas etc. nos lugares compatíveis com a vida real (dados de comércio do OSM); Etapa 2: comércio por posição proporcional, com amostragem por tipo.
  - **Nova regra de trabalho (pedido do usuário):** criado `PROBLEMAS_CONHECIDOS.md`, com 18 erros já vistos (ambiente, KnoxMap, jogo), a causa e a solução de cada um. Leitura obrigatória antes de cada tarefa (AGENTS.md e seção 8).

---

## 13. Glossário rápido

- **Tile:** um quadradinho do chão do jogo. Aqui, 1 tile = 15 m reais.
- **Célula:** bloco de 256×256 tiles (B42). O mapa é montado célula por célula.
- **Compilar:** transformar o projeto do mapa nos arquivos que o jogo lê (`.lotheader` / `.lotpack`).
- **OSM / OpenStreetMap:** mapa livre do mundo (ruas, prédios, rios). O arquivo `.osm.pbf` é o download compactado.
- **KnoxMap:** programa que transforma dados do OSM em mapa do PZ.
- **WorldEd / TileZed:** editores de mapa e de tiles do PZ.
- **Kit:** conjunto de regras e prédios que o gerador usa para montar as cidades.
- **Carimbo:** pedaço feito à mão (um marco ou uma cena) que o gerador encaixa no lugar certo.
- **Zona:** área marcada no mapa que diz ao jogo o que existe ali (estrada, mata, estacionamento) e quais eventos e carros podem aparecer.
- **Histórias (eventos):** cenas aleatórias que o jogo monta sozinho, como batidas de carro, acampamentos ou casas com sobreviventes mortos.
- **Viewpoint:** mod de primeira pessoa que mostra o mundo em 3D.
- **Modelo de altitude (DEM):** arquivo com a altura real de cada ponto do terreno, medida por satélite. É dele que sai o relevo.

---

## 14. Fontes

- Real USA (Workshop): https://steamcommunity.com/sharedfiles/filedetails/?id=3829712469
- KnoxMap: https://github.com/CalvyPZ/knoxmap
- Matéria sobre o KnoxMap: https://www.fixgamingchannel.com/knoxmap-project-zomboid-real-world-maps/
- PZ Reverse Mapper: https://www.nexusmods.com/projectzomboid/mods/337
- Mapa vanilla B42 em formato WorldEd: https://github.com/Unjammer/PZ_Vanilla_map_b42
- Planos da Indie Stone (ferramentas de mapa): https://projectzomboid.com/blog/news/2026/07/next-steps-2/
- PZwiki, Mapping: https://pzwiki.net/wiki/Mapping
- Extratos do Brasil por região (Geofabrik): https://download.geofabrik.de/south-america/brazil.html
- Viewpoint e o Terrain relief (guia): https://pzfans.com/project-zomboid-3d-viewpoint/
- Viewpoint Better Terrain: https://steamcommunity.com/sharedfiles/filedetails/?id=3815223174
- Viewpoint Rolling Hills: https://steamcommunity.com/sharedfiles/filedetails/?id=3815630947
- Mapa novo em save existente (D-34): https://pzfans.com/ProjectZomboidAddModsMidGame/ ; https://supercraft.host/wiki/project-zomboid/chunk-cleaner ; https://steamcommunity.com/workshop/filedetails/discussion/3507117617/595153277396555477
- Limite de 32 andares da B42 (fonte de terceiros): https://supercraft.host/wiki/project_zomboid/build_42_features/
- Peso/memória da B42 com 32 níveis visíveis (fonte de terceiros): https://supercraft.host/wiki/project-zomboid/b42-performance-tuning/
- Tripo 3.1 e Multi View (4 vistas, Smart Low Poly): https://help.scenario.com/articles/4692888910-tripo-family-the-complete-guide ; https://www.scenario.com/blog/tripo-image-to-3d-model-ai-2026
