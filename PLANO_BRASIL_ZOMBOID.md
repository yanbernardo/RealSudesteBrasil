# Plano mestre: Real Sudeste Brasil (mod de mapa para Project Zomboid)

> **Claude, comece por aqui. Este arquivo é a memória do projeto.**
>
> 1. Em cada sessão, leia só a seção 1 (Estado atual) e a etapa em andamento (seção 7). O resto só quando precisar.
> 2. Nunca mude uma decisão marcada como DECIDIDO sem perguntar ao usuário.
> 3. No fim de cada sessão, atualize a seção 1 e o Registro (seção 12) e, se alguma decisão mudou, o `AGENTS.md`.
> 4. Quando este arquivo crescer demais, divida em PLANO.md (estável) + PROGRESSO.md (log).
> 5. O `AGENTS.md` (e o `CLAUDE.md`, que só aponta para ele) é o resumo curto para qualquer IA. Se ele e este plano discordarem, vale este plano.

Criado em 05/11/2026 (planejamento feito pelo celular). Última atualização: 08/11/2026. Idioma do projeto: pt-BR.

---

## 1. Estado atual

- **Fase:** planejamento encerrado em 05/11/2026 → próxima: Etapa 0 (fundação e testes técnicos).
- **Lançamento (D-33):** RJ primeiro (beta pública só com o RJ, fim da Etapa 4); depois SP, MG e ES entram como atualizações do mesmo mod (Etapa 7).
- **Próxima ação (atualizada em 08/11/2026, fim da noite):** Etapa 0.2 quase fechada. Passaram T1, T2, T4, T7/T7c e **T8** (catálogo, loot de loja, D-38, histórias de casa/estrada/zona em jogo, viagem de rodovia: combustível não aperta a 1:15, D-35 decidido só como sabor). T9 respondido (curvas nossas, K15). **Faltam:** T5 (Viewpoint: (a) prédios gerados em 3D, (b) tile nova com 3D, (c) Cristo), T6 (tamanho e desempenho, PC potente) e T3 (só se o T6 pedir); confirmar D-13 (KnoxMap como montador do nosso gerador) e, com o T6, D-11; D-02 fecha na Etapa 1. **Sugestão de próximo passo no notebook:** T5a, teste pequeno do Viewpoint com o mapa do T8c (ver em 3D os prédios gerados, as lojas copiadas e os carros); depois começar a Etapa 1 (grade e dados leves) enquanto o T6 espera o PC potente. O teste da Dutra (T8d) está pausado pelo usuário. **Escolha do usuário (08/11/2026, fim da sessão): começar já a Etapa 1**; T5a, D-13 e T6 ficam pendentes da Etapa 0 (não bloqueiam a Etapa 1, que é só dados). Trabalho da sessão juntado ao `main`. **Etapa 1 começou (08/11/2026):** D-02 decidido (policônica centrada em 45° W; origem na seção 6; `scripts/grade.py`) e lista de dados do RJ com tamanhos (Etapa 1, "Andamento"). Dados do RJ baixados (autorizado), **mapa-guia do RJ v1** (`saida/etapa1_rj/mapa_guia_rj.png`) e **regras de localidades v1** (`kits/localidades/regras_v1.json`, PROPOSTA) prontos. **Próximo:** P19–P21 respondidas e aplicadas (regras v1 e mapa-guia gerados de novo). **Etapa 1 aprovada pelo usuário (08/11/2026)** para o RJ: mapa-guia e regras de localidades v1. **Próximo:** Etapa 2 (Rio piloto; começar medindo a densidade de zumbis de Louisville, P19) ou T5a, à escolha do usuário. Novo (D-39): menu de teleporte do modo debug pronto; falta conferir em jogo que ele aparece (mod `rsb_t8c_historias`, jogo em modo debug). O projeto vive em `C:\Users\yanbe\Zomboid\RealSudesteBrasil\`.
- **Ambiente atual (07/11/2026):** estamos no **notebook Acer Nitro V15** (8 GB de RAM, RTX 3050), **não no PC potente** (Ryzen 7 5700X3D, RTX 5060 Ti 16 GB, 32 GB de RAM, NVMe de 2 TB). Aqui só se adianta o que é leve: preparar ferramentas e dados, documentos, modelos pelo Tripo (na nuvem), testes minúsculos (T1 e T7 num bairro) e, no jogo, **testar só a visão isométrica por enquanto** (o 3D do Viewpoint e o T6 podem não rodar bem). Gerar e compilar o RJ inteiro, rodar mapa grande no jogo e IA 3D local ficam para o PC potente. A pasta do projeto está na Área de Trabalho do notebook; para levar ao PC potente, usar o Git (0.1) ou copiar a pasta.
- **Pendente do usuário:** nada que bloqueie a Etapa 0. Todas as perguntas do planejamento foram respondidas (a P7, sobre o hardware, Claude verifica na Etapa 0).
- **Ainda PROPOSTO (aguardam confirmação ou teste):** D-30 (Pão de Açúcar visitável) e a escolha da altura do relevo, 1:10 ou 1:15 (D-26/D-27), saem depois de ver em jogo, na Etapa 2.7; D-32 (tiles e modelos de drogas decorativos) depende de conferir as regras de conteúdo da Workshop antes de implementar; D-34 (atualização que muda o mapa pede save novo) o usuário confirma antes da beta pública. (D-35 foi decidido em 08/11/2026: níveis de recursos só como sabor, sem trava.)
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
| D-02 | Grade fixa: SIRGAS 2000, **policônica (a do IBGE) com o meridiano central em 45° W** (meio do Sudeste), norte para cima, origem no canto noroeste do Sudeste com folga. Números na seção 6; script `scripts/grade.py` | DECIDIDO | Escolha do usuário em 08/11/2026 (Etapa 1), depois de ver as implicações. A EPSG:5880 do plano antigo tem o centro em 54° W (MS): giraria o Rio 4,2° e Vitória 4,7° e esticaria o norte–sul em 1,5–2,8%. Centrada em 45° W: Rio 0,7°, SP 0,6°, BH 0,4°, Vitória 1,6°, erro de distância < 0,1% nas capitais. O T2 provou que o canto sudeste cabe. **Não mudar depois que o mapa começar a ser gerado** (tudo muda de lugar). |
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
| D-35 | **Cidades de rodovia com recursos variáveis (só "sabor"):** cada cidade ou vila nas rodovias principais (ex.: Dutra, Rio–SP) recebe, **na hora de gerar o mapa**, um nível fixo de recursos: completa (posto, comércio e farmácia), parcial ou "seca" (só casas). Sorteado por regra, como no D-31; as construções ficam iguais em todos os saves, e a variação entre saves vem do que o jogo já sorteia (loot, veículos, eventos, D-17). **Sem trava de distância sem posto:** a dificuldade da viagem fica com o sandbox do jogo (consumo de combustível, carros achados com pouca gasolina) | DECIDIDO | Ideia do usuário em 07/11/2026 (não deixar a viagem Rio–SP fácil demais). Cidades pequenas ficam pequenas a 1:15, então o gerador precisa de um tamanho mínimo que comporte posto, comércio e farmácia. **Teste T8d (08/11/2026):** 30 km reais de Dutra gastaram 0,78 de 49 unidades de gasolina no consumo padrão (Rio–SP inteira: ~20% do tanque), então a trava proposta quase não teria efeito; **o usuário decidiu (P18): manter os níveis só como sabor e deixar a dificuldade com o sandbox.** |
| D-36 | **Mapa independente:** o Real Sudeste Brasil é o mundo inteiro; o Knox County (Muldraugh, Louisville etc.) **não** é carregado junto. No servidor, `Map=` lista só o nosso mapa | DECIDIDO | Decisão do usuário em 07/11/2026, depois de ver a Urca de teste aparecer acima de Louisville. O KnoxMap já tem esse modo ("Standalone": mapa na célula 0,0, sem o Knox County). Muda o T2: em vez de "convive com o Knox County?", testar se o jogo carrega o nosso mapa sozinho (loot, zonas e nascimento funcionando) e se aceita a célula mais distante do Sudeste. Também libera a origem (D-02): não precisa desviar do mapa original. |
| D-37 | **Assinatura do KnoxMap no chão:** manter o crédito "KNOXMAP BY EUCLID80TR" escrito no chão, mas **uma vez só no mapa todo**, num lugar escolhido pelo usuário (não mais perto de onde o jogador nasce). O crédito escrito continua no `ATTRIBUTION.txt` e na página da Workshop | DECIDIDO (o lugar ainda será escolhido) | Decisão do usuário em 07/11/2026, depois do T9. Técnica: mudar em `knoxbuild\credit_ground.py` (MIT) o ponto de busca para um ponto nosso e desligar nos outros pedaços; sem isso, cada pedaço do mapa montado pelo KnoxMap ganharia uma assinatura. Implementar na Etapa 2. |
| D-38 | **Lojas comerciais iguais às do jogo original até o Kit Brasil:** farmácias, lojas de armas e demais comércios usam **cópias inteiras** de prédios do mapa original (estrutura, móveis, cômodos e loot do jogo), escolhidas pelo tipo de loja (etiqueta `shop=`/`amenity=` do OSM) e pelo lado da rua. Decoração e estrutura brasileiras só quando houver o Kit Brasil (Etapa 5). As nossas plantas (`kits/lojas/plantas/`) ficam só como reserva onde não houver cópia que sirva | DECIDIDO | Decisão do usuário em 08/11/2026, depois de 4 rodadas do T8 com plantas nossas (móveis e estrutura não convenciam) e do teste `rsb_t8b_vanilla` (cópia da "Pharmahug" e de uma loja de armas). Ferramentas: `scripts/gerador/copiar_predio_vanilla.py` e `scripts/gerador/kit_lojas.py`; ver `kits/lojas/LEIA-ME.md`. Pendências: cópias para cada tipo de loja e cada lado da rua (a cópia não gira), e a P14 (publicar cópias na Workshop). |
| D-39 | **Menu de teleporte do modo debug (como no Real USA):** no modo debug, o menu do botão direito no chão ganha "Real Sudeste Brasil: teleporte", com marcos e cidades em grupos (Rio, Serra, Costa Verde, Lagos, interior; capitais dos outros estados). Só aparece em debug (ou, no servidor, para quem pode usar o menu de debug). Pontos fora do mapa carregado ficam desativados, com aviso | DECIDIDO | Pedido do usuário em 08/11/2026. Lista editável em `kits/marcos/teleporte.json`; `scripts/gerador/teleporte_debug.py` converte pela grade (D-02), confere se o ponto cai em terra e gera `RSB_TeleporteDebug.lua`; o `knoxmap_pipeline.py` o instala em todo mod RSB. Teleporte igual ao do menu de debug do jogo (`teleportTo` / `/teleportto`). Os marcos ganham pontos novos conforme forem construídos (Etapa 2.4). |

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

   **Valores fixos (D-02, gravados em 08/11/2026; script `scripts/grade.py`):**
   - Projeção: `+proj=poly +lat_0=0 +lon_0=-45 +x_0=0 +y_0=0 +ellps=GRS80 +units=m` (SIRGAS 2000, policônica centrada em 45° W). Entrada em lat/lon SIRGAS 2000 (EPSG:4674; para o nosso uso, igual ao WGS84 do OSM).
   - **E0 = −860.000 m** (26 km a oeste do Pontal do Paranapanema, ponto mais a oeste de SP).
   - **N0 = −1.550.000 m** (24 km ao norte do ponto mais ao norte de MG).
   - **OFFSET_X = 0, OFFSET_Y = 0.** 1 tile = 15 m; célula = 256 tiles. Para o KnoxMap, `"cell"` = tile // 300 (K16).
   - Resultado: o Sudeste ocupa as células **6–369 (x) × 6–326 (y)**; no KnoxMap, até 315 × 278 (teto 400). As ilhas de Trindade e Martim Vaz (ES, ~1.100 km mar adentro) ficam fora.
   - Pontos de conferência (`python scripts/grade.py --conferir`): Rio (Centro) tile 69.829 × 65.691 = célula 272 × 256; São Paulo (Sé) 46.216 × 70.430 = célula 180 × 275; BH 64.770 × 43.566 = célula 253 × 170; Vitória 89.963 × 46.949 = célula 351 × 183. Rio–SP em linha reta: ~24.080 tiles = 361 km (real ~357 km).
   - Observação: a célula mais ao sul (Ilha do Cardoso, y 326) fica um pouco além da testada no T2 (y 319–321), mas bem abaixo do teto do KnoxMap (469); o RJ ocupa as células ~226–333 (x) × ~195–269 (y).
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
- **Teto (P19, usuário, 08/11/2026):** nenhum lugar passa da densidade máxima de Louisville no mapa original. O Rio e as cidades grandes chegam no máximo a esse teto, para ficar jogável como o jogo base (medir o valor nos arquivos do jogo na Etapa 2.1).
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

**Andamento (08/11/2026, notebook):**
- ✔ **Grade (D-02 decidido):** `scripts/grade.py` converte lat/lon ↔ tile, dá a célula do jogo e a do KnoxMap; ida e volta conferida. Origem na seção 6.
- ✔ **Lista de dados do RJ (tamanhos conferidos no servidor, sem baixar):**

| # | Dado | Para quê | Fonte | Tamanho | Quando |
|---|---|---|---|---|---|
| 1 | Malha municipal do RJ 2024 (contorno do estado e dos 92 municípios) | Contorno do estado, limites, nomes dos municípios | IBGE, `RJ_Municipios_2024.zip` | 5,1 MB | Agora |
| 2 | Localidades 2022 (cidades, vilas, povoados, lugarejos, com coordenadas) | Lista de localidades para a regra D-22 | IBGE, `Localidades_Brasil_gpkg.zip` (Brasil todo; serve depois para SP, MG e ES) | 6,2 MB | Agora |
| 3 | Áreas urbanizadas 2019 (manchas urbanas desenhadas sobre satélite) | Contornos urbanos (D-03) e tamanho de cada cidade | IBGE, `AreasUrbanizadas2019_Brasil.zip` (Brasil todo) | 37 MB | Agora |
| 4 | População do Censo 2022 por município | Categoria das cidades e zumbis | IBGE (API SIDRA, tabela pequena) | < 0,2 MB | Agora |
| 5 | OSM do RJ, só o que o mapa-guia usa: rodovias (25.552 trechos motorway/trunk/primary/secondary), rios (2.629), linha da costa (1.443) e nomes de lugares (3.370 pontos) | Costa, rios, rodovias, nomes; pousadas e cachoeiras (bônus turístico, D-22) | Overpass (contagem feita; consulta só do RJ) | ~20–35 MB (estimativa pela contagem) | Agora |
| 6 | Relevo Copernicus GLO-90 (90 m por ponto ≈ 6 tiles) | Relevo visual (D-26/D-27) | AWS, ~12 blocos de 1° × 1° de ~5,5 MB | ~65 MB | Depois (só serve na Etapa 2.7; não entra no mapa-guia) |
| 6b | Relevo Copernicus GLO-30 (30 m ≈ 2 tiles) | Idem, mais fino | AWS, ~12 blocos de ~46 MB | ~550 MB | Só no PC potente, se o 90 m não bastar |
| 7 | Cobertura do solo (MapBiomas ou ESA WorldCover) | Tipo de campo (Etapa 3) | — | a medir | Depois (Etapa 3) |
| — | Extrato OSM do Sudeste inteiro (Geofabrik) | Tudo do OSM | Geofabrik | 863 MB | Só no PC potente |

  Total para o mapa-guia do RJ (itens 1–5): **~70–85 MB**. Espera a autorização do usuário (internet móvel).
- ✔ **Dados baixados (autorizados pelo usuário, 08/11/2026):** IBGE 71 MB em `dados/ibge/` (municípios do RJ, localidades 2022, áreas urbanizadas 2019, população do Censo 2022) e OSM ~8 MB pela rede (37 MB no disco) em `dados/osm_rj/` (rodovias, rios, costa, lagoas, lugares, turismo). Script `scripts/dados/baixar_osm_rj.py`.
- ✔ **Mapa-guia do RJ v1:** `saida/etapa1_rj/mapa_guia_rj.png` (1 pixel = 16 tiles, 0,5 MB) e `mapa_guia_rj_detalhe_8.png` (1 pixel = 8 tiles, 1 MB, mais nomes). Já na grade do jogo, com linhas a cada 10 células e o número da célula na borda. O RJ fica nas células 221–339 × 189–275. Script `scripts/dados/mapa_guia_rj.py` (leitores próprios em `scripts/dados/leitores.py`, sem geopandas).
- ✔ **Regras de localidades v1 (D-22), com P19–P21 aplicadas (os números abaixo são da 1ª rodada; sem as repetições do IBGE ficaram 1.268 localidades, 577 vilarejos, 90 bairros e 337 só nome):** `kits/localidades/regras_v1.json`, aplicadas por `scripts/dados/regras_localidades.py` → `saida/etapa1_rj/localidades_rj.csv` (nome, município, tipo do IBGE, categoria, tile, célula, turística, área urbana no jogo). Resultado no RJ (1.341 localidades do IBGE): 1 metrópole (Rio), 7 grandes (≥ 300 mil hab.), 29 médias (≥ 50 mil), 55 pequenas, 172 distritos (vilas do IBGE), 631 vilarejos (núcleos, povoados, lugarejos, quilombolas, aldeias), 93 viram bairro de uma cidade (estão dentro da mancha urbana dela) e 353 ficam só como nome no mapa ("outras localidades" do IBGE sem mancha urbana: condomínios, fazendas). **46 turísticas** (≥ 3 pousadas/hotéis/campings/cachoeiras do OSM a até 2 km; sedes ≥ 5): entre elas Lumiar, São Pedro da Serra, Sana, Visconde de Mauá, Penedo, Paraty, Trindade, Búzios, Arraial, Petrópolis, Teresópolis. Ruído conhecido: "CADIM da Marinha" e "Condomínio Agro Industrial" saíram turísticos; duas localidades vêm repetidas no IBGE. A mancha urbana contínua do Grande Rio dá ~6,1 milhões de tiles no jogo (~93 células).
- ✔ **Etapa 1 aprovada pelo usuário (08/11/2026)** para o RJ (mapa-guia e regras v1). **Ficam para depois, sem bloquear:** relevo (adiado, Etapa 2.7); rodovias e rios escolhidos para o corredor (Etapa 3); catálogo de células por estado (o RJ já tem a faixa de células).

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
- P14 (nova, 08/11/2026): pode publicar na Workshop prédios copiados do mapa do jogo (D-38)? Os tiles são do jogo que o jogador já tem, mas a planta e a decoração são conteúdo da The Indie Stone. Conferir a política de mods da TIS (e o que mods de mapa grandes, como o Real USA, fazem) antes da beta pública (D-33).
- P15 (nova, 08/11/2026): cópias de lojas originais para todos os lados da rua. A cópia não gira; ou achamos no mapa original uma loja do mesmo tipo com a frente para cada lado (N, S, L, O), ou fazemos uma tabela de "tile girado" (cada parede, porta, janela e móvel tem sua versão em cada direção). Resolver na Etapa 2, junto com o gerador.
- P16 (nova, 08/11/2026): loot da farmácia. No jogo base, as prateleiras da farmácia dão bastante comida e bebida; remédios garantidos só nos balcões e no estoque. Manter assim ou fazer um ajuste de loot para a "drogaria" brasileira? Decidir com o Kit Brasil.
- P17 respondida (08/11/2026, noite): usar a Dutra real (T8d gerado; ver Registro). Pergunta original: pode montar como proposto: estrada reta desenhada por nós (sem baixar nada), ~2.000 tiles (≈ 30 km reais), cidade "completa" numa ponta e "seca" na outra? Ou prefere a forma real de um trecho da Dutra (download pequeno da Overpass, mas as curvas ainda saem em degraus, K15)?
- P18 respondida (08/11/2026, noite): **(a), "só sabor, sandbox decide"** (D-35 DECIDIDO sem trava). Pergunta original: D-35 e combustível. No T8d, 30 km reais de Dutra gastaram 0,78 de 49 unidades de gasolina (consumo padrão do jogo); Rio–SP inteira gastaria uns 20% do tanque. A "trava de distância máxima sem posto" quase não teria efeito. O que fazer: (a) manter o D-35 só pelo sabor (cidades completas/parciais/secas) e deixar a dificuldade com o sandbox (consumo de combustível, carros achados com pouca gasolina); (b) postos raros e bombas com pouco combustível; (c) outra ideia do usuário.
- P19 respondida (08/11/2026): cortes mantidos (metrópole ≥ 1 milhão, grande ≥ 300 mil, média ≥ 50 mil, pequena abaixo). O usuário lembrou que o tamanho influencia os zumbis e quer **equilíbrio igual ao do jogo base: o teto de densidade de zumbis é a densidade máxima de Louisville** (a maior cidade do mapa original); cidades grandes chegam no máximo a isso, o resto proporcionalmente menos. Medir o valor de Louisville nos arquivos do jogo na Etapa 2.1.
- P20 respondida (08/11/2026): "outras localidades" sem mancha urbana ficam **só com o nome, discreto** (pequeno e cinza), e só se estiverem afastadas (≥ 3 km reais) de localidades construídas; se o nome bater no de uma cidade maior, fica de fora. Resultado no RJ: 199 com nome, 138 sem.
- P21 respondida (08/11/2026): aldeias indígenas e comunidades quilombolas são **representadas** como vilarejos, com o nome no mapa quando couber (sem brigar com nomes maiores).

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
  - **U8 (nomes de rua no mar) resolvido (usuário, 08/11/2026):** não aparece mais nos mapas independentes; vinha do gerador antigo/ruas reais do OSM giradas. Próximo: T4 (o que o jogo faz além das células compiladas), testado andando para fora da borda do `rsb_t2b_longe`.
  - **T4 (campo sem Java), parcial (usuário, 08/11/2026, 42.21):** teleportado para x=92419, y=81962 (célula 361 × 320, **não compilada**; o mod só tem 369–370 × 319–321): o jogo gerou sozinho mata e grama (`e_newgrass_1_42`, árvores e arbustos do jogo base) e deixou ir até lá sem erro. **Conclusão provisória:** células vazias entre as cidades não precisam ser compiladas; a vegetação é a genérica do jogo (não dá para escolher Mata Atlântica, cana ou pasto sem compilar células ou usar Java, D-06). **Falta:** zumbis e FPS nessas áreas vazias, e o peso de células de campo compiladas (T6, PC potente).
  - **T4 respondido (usuário, 08/11/2026):** nas células vazias há zumbis e o FPS fica estável em 60, igual ao da cidade. **Conclusão:** o espaço entre as cidades fica sem célula compilada (o jogo gera mata e zumbis). Só se compila campo se quisermos vegetação própria (Etapa 3/T6). **Escopo reafirmado pelo usuário:** por ora só o RJ (D-33); se entrarem outros estados depois, o mapa cresce. Isso casa com a grade do Sudeste (D-02), que mantém o RJ no mesmo lugar quando o mapa crescer.
  - **T8, catálogo do jogo base (08/11/2026):** `scripts\catalogo_jogo.py` lê os arquivos Lua do jogo 42.21 e grava `catalogo\CATALOGO.md` (35 KB, consulta rápida) e `catalogo\catalogo_jogo.json` (460 KB). Contém: ~386 tipos de cômodo com seus contêineres (ex.: `bedroom`, `pharmacy`, `bakery`), esconderijos e bolsas, 1.420 listas de loot procedurais (com os itens mais comuns), 68 zonas de zumbi (tipos do WorldEd, com roupas) e 55 zonas de veículo. **Limite:** as histórias de casa/veículo (eventos) ficam no Java do jogo, não em Lua; só o lixo de cena (`StoryClutter`) está no catálogo. Para o resto, só testando em jogo. Falta do T8: eventos/histórias em jogo, loot comercial (lojas) e a viagem de rodovia (D-35).
  - **Comércio por localização real e loot de loja (08/11/2026, HIPÓTESE, reversível):** pergunta do usuário: dá para pôr farmácias e lojas nos lugares reais? Leitura do código do KnoxMap (`knoxbuild/uses.py`): ele transforma as etiquetas do OSM dentro de um prédio (`shop=pharmacy`, `amenity=bakery` etc.) em nomes de cômodo do jogo (`pharmacy`, `bakery`…), então o loot é o do jogo base. **Caminho provável:** nosso gerador põe `tags` (ex.: `{"shop": "pharmacy"}`) nos prédios do `sketch`, escolhidos pelos pontos reais do OSM (posição proporcional no bairro encolhido, com amostragem por tipo). **Ainda não testado:** se o KnoxMap aceita essas etiquetas em prédios desenhados (o T7c só usou `building:levels`). Plano B: o gerador renomeia os cômodos com o catálogo (`catalogo/CATALOGO.md`). Nada disso é decisão; só entra no jogo depois de um teste e da aprovação do usuário, e dá para desfazer (ponto de volta: commit `bf68dd4`; nenhum arquivo do mapa foi alterado).
  - **T8 lojas (08/11/2026, gerado; falta o usuário conferir):** mod `rsb_t8_lojas` ("RSB Teste T8 - Lojas"), config `scripts/testes/t8_lojas.json`. O `knoxmap_pipeline.py` ganhou `"extraTags": [...]` (amplia as etiquetas que o KnoxMap deixa passar no `sketch`, sem mexer nos arquivos dele). Cinco lojas do bairro do T7c, cada uma de um tipo: farmácia (`pharmacy`), padaria (`bakery`), loja de armas (`weapons`), ferragens (`hardware`) e roupas (`clothes`). Conferido nos arquivos: padaria, armas, ferragens e roupas viraram os cômodos `bakery`, `gunstore`, `toolstore` e `clothingstore`. **A farmácia saiu como prédio "medical" com planta de casa** (camas, banheiro), não como loja: o KnoxMap trata `pharmacy` como prédio médico. Pode ser um problema para o loot de farmácia; o teste em jogo mostra. Esperado em jogo: o loot de cada loja condiz com o tipo.
  - **T8 lojas no jogo (usuário, 08/11/2026):** o **loot** de cada loja condiz com o tipo (padaria, armas, ferragens, roupas, farmácia). **Mas** a construção e os móveis não condizem: a farmácia parecia uma casa; a loja de armas parecia loja de posto. Causas: (1) farmácia: `shop=pharmacy` vira prédio médico com planta de casa (K17); trocado para `shop=chemist` e conferido (agora `shop`, com o cômodo `pharmacy`); (2) o resto é a decoração genérica do KnoxMap (U17): a loja de armas usa as peças da loja de ferragens. Ajuste feito: `storeOverrides` no pipeline (vitrines e balcão na loja de armas), só com peças do jogo base. **Conclusão para o plano:** etiquetar prédios com o tipo certo dá o **loot** certo; a **aparência** de cada tipo de loja (fachada, planta, móveis) é trabalho do Kit Brasil (Etapa 5). Versão corrigida compilada, falta instalar (jogo aberto, K18) e o usuário conferir de novo.
  - **Kit de lojas, piloto (08/11/2026, HIPÓTESE; pedido do usuário: interiores fáceis de redecorar com o Kit Brasil):** o usuário apontou que quase todas as lojas do T8 tinham construção e móveis que não condizem (só a de roupas, talvez por acaso). Rota escolhida (temporária): plantas próprias, estampadas pelo recurso "prédios feitos à mão" (presets) do KnoxMap. Tudo em `kits/lojas/` (ver o `LEIA-ME.md` de lá): plantas em JSON (cômodos por retângulo), decoração em **papéis** de móvel (o Kit Brasil só troca os papéis e acrescenta tiles) e um mapa etiqueta `shop=` → planta. O `knoxmap_pipeline.py` (chave `kitLojas`) grava as plantas e cria uma **zona** por loja, que é como o KnoxMap deixa escolher o preset por loja (ele só escolhe por categoria). Plantas feitas: farmácia (`chemist`) e loja de armas (`weapons`), com sala de vendas, estoque e escritório/banheiro; móveis novos pelos papéis: `gun_locker` e `shop_case` na loja de armas. Conferido: o KnoxMap estampou as duas (`hand-built: 2 stamped`). O desenho de prévia mostra a mesma densidade de móveis das lojas geradas; a qualidade final é limitada pelo terreno de 8 × 12 tiles e pelos papéis do jogo base. Mod `rsb_t8_lojas` reinstalado. **Falta o usuário jogar** e dizer se melhorou; se sim, fazer as outras lojas (padaria, ferragens, mercado…) do mesmo jeito; se não, o acabamento vai para o Kit Brasil com BuildingEd.
  - **Kit de lojas, rodada 2 (usuário jogou o piloto, 08/11/2026):** erros: estoque da farmácia e da loja de armas com material de construção; vitrine (que é de loja de armas e joias) na farmácia; expositor só de revistas; escritório da farmácia e porta das duas voltados para os fundos; prateleiras de mercado na loja de armas. Correções (K19–K21): cômodos `pharmacystorage` e `gunstorestorage` (do jogo base, loot de remédio e de munição); farmácia só com prateleiras, geladeiras e balcão (um expositor de revistas só); loja de armas com vitrines, armários e balcão; planta com a sala de vendas na rua, em duas versões (rua ao norte e ao sul), a certa escolhida pela rua mais próxima da loja; escritório da farmácia removido. Mod reinstalado. Esperado em jogo: porta pela rua e loot condizente. **Falta o usuário conferir.**
  - **Conferência com o jogo base (08/11/2026, a pedido do usuário):** `scripts/analise_lojas_vanilla.py` lê os arquivos do mapa original (Knox County; usa os leitores do KnoxMap) e conta, dentro dos cômodos de cada tipo, quais móveis o jogo base usa (`catalogo/LOJAS_VANILLA.md` e `.json`; 7 s por rodada, serve para qualquer cômodo: `... <KnoxMap> padaria`-style, passando o nome do cômodo). Resultado: loja de armas = vitrines (`shop_case`, em 50% das lojas), armários de arma, balcão; farmácia = corredores `shop_aisle`, prateleiras `shop_shelf`, balcões; estoque da farmácia = prateleira de metal, geladeira branca, balcão; estoque de armas = armário de arma, prateleira de metal, caixote. Isso confirmou a escolha da rodada 2 e corrigiu o estoque (tirei mesa e arquivo, que eu tinha chutado). Reinstalado. **Método para as próximas lojas:** rodar essa análise para o tipo e usar só os papéis que aparecem; sem papel no KnoxMap = candidato ao Kit Brasil.
  - **Kit de lojas, rodada 3 (08/11/2026; troca para o Opus a pedido do usuário):** o usuário achou a farmácia "só geladeiras" e com a porta ainda nos fundos, e a loja de armas pobre e com a porta para o lado errado. Causas: (1) cache de prédios do KnoxMap (K22): as duas últimas versões nem chegaram ao jogo; (2) decoração sorteada repetia peças (K23). Correções: o pipeline limpa o cache; os móveis passam a ser **posicionados à mão** em cada planta, tomando como referência lojas reais do jogo base desenhadas com `render_lots --world` (farmácia: prateleiras brancas nas paredes, 2 corredores no meio, 3 geladeiras só no fundo, balcão e caixa perto da porta, planta, lixeira, relógio; estoque com prateleiras de metal, 2 geladeiras e balcão; loja de armas: 10 armários de arma nas paredes, 4 vitrines no meio, manequim, cartazes, relógio, lixeira e planta; estoque com armários, prateleira e caixotes). Itens de parede têm lista por versão (K24). **Conferido nos arquivos compilados antes de entregar:** as duas lojas com porta e vitrines para a rua (norte), salas e estoques no lugar. Mod reinstalado. Falta o usuário jogar.
  - **Kit de lojas, rodada 4 (08/11/2026, Opus):** usuário: a farmácia melhorou, mas as prateleiras davam comida, havia um expositor de feira (era o `shop_bin`, que eu tinha posto como "lixeira"), uma geladeira trancava uma porta e as paredes pareciam de posto. Achados: (1) **comida na farmácia é do jogo base**: as prateleiras da `pharmacy` sorteiam entre remédios, cosméticos, bebidas, salgadinhos e limpeza; os remédios garantidos ficam no **balcão** (`MedicalClinicDrugs`) e no estoque. (2) Faixa xadrez = estilo de parede `shop~painted` (Gas2Go); `shop~panel` tira a faixa de dentro, mas por fora todos os estilos de loja do KnoxMap a têm. Correções na nossa planta: balcão de remédios (`counter_6`, o mais comum nas farmácias do jogo) no fundo, lixeira de verdade, móveis afastados 2 quadrados de cada porta (automático), estilo `shop~panel`.
  - **Cópia de prédios do mapa original (08/11/2026, pedido do usuário: copiar a estrutura inteira, não só loot e móveis):** `scripts/gerador/copiar_predio_vanilla.py` lê um prédio do Knox County (arquivos `.lotheader`/`.lotpack`) e grava um `.tbx` com cada quadrado como pilha de tiles pintados e os cômodos com os nomes do jogo; o KnoxMap estampa como preset. Copiadas: farmácia "Pharmahug" (célula 46_26, 14 × 19) e loja de armas (14_33, 13 × 13), ambas com a frente a oeste. Teste `rsb_t8b_vanilla` (`scripts/testes/t8b_lojas_vanilla.json`): rua a oeste, dois terrenos maiores que os prédios. **Conferido no compilado:** igual ao original (letreiro, vitrine e porta para a rua, balcões, laboratório, estoque, telhado) e cômodos `pharmacy`/`pharmacystorage`/`gunstore`/`gunstorestorage` (loot do jogo). Instalado; falta o usuário jogar. **Limites:** a cópia não gira (só serve onde a rua fica do lado da frente dela; outras orientações pedem outras lojas originais ou uma tabela de tiles girados) e precisa de terreno maior que ela. **A decidir (P14):** publicar na Workshop prédios copiados do mapa do jogo; os tiles são do jogo que o jogador já tem, mas a cópia da planta é conteúdo da The Indie Stone; conferir a política de mods da TIS antes do lançamento.
  - **Fim da sessão (08/11/2026, notebook):** **D-38 decidida**: lojas comerciais como cópias inteiras das lojas do jogo original até existir o Kit Brasil. Perguntas novas: P14 (Workshop e cópias), P15 (cópias para todos os lados da rua), P16 (loot da farmácia). Situação da Etapa 0.2: T1 ✔; T2 ✔ (parte 2: célula no extremo do Sudeste carrega); T4 ✔ (células vazias: o jogo gera mata e zumbis, 60 FPS → não compilar o campo entre cidades); T7/T7c ✔; T9 ✘ (curvas nossas, K15); U8 ✔; T8 em andamento: ✔ catálogo do jogo (`catalogo/`), ✔ análise de móveis por loja (`scripts/analise_lojas_vanilla.py`), ✔ loot de loja pela etiqueta `shop=`, ✔ cópia de lojas originais (D-38); **faltam** eventos/histórias em jogo e a viagem de rodovia (D-35). Também faltam T3 (só se o T6 pedir) e T5/T6 (PC potente). Mods de teste em `Zomboid\mods`: `rsb_t1_urca`, `rsb_t7b_ruas`, `rsb_t7c_botafogo`, `rsb_t2b_longe`, `rsb_t8_lojas` (plantas nossas, abandonadas pela D-38), `rsb_t8b_vanilla` (cópias originais; o usuário ainda não jogou esta versão). Trabalho no ramo `claude/t2-parte2-celula-sudeste-947d21`, juntado ao `main`. Próximo passo: resto do T8 (eventos/histórias e viagem de rodovia).
  - **Nova regra de trabalho (pedido do usuário):** criado `PROBLEMAS_CONHECIDOS.md`, com 18 erros já vistos (ambiente, KnoxMap, jogo), a causa e a solução de cada um. Leitura obrigatória antes de cada tarefa (AGENTS.md e seção 8).
- **08/11/2026 (noite, notebook, jogo 42.21; ramo `claude/t8-eventos-historias-rodovia-62e528`): resto do T8.** Conferido antes: o commit da D-38 está no `main` do GitHub e a pasta estava em dia.
  - **Como o jogo decide onde aparecem as histórias (lido do Java do jogo):** o decompilador externo (CFR, 2 MB) foi bloqueado pelo modo automático, então foi feito um leitor próprio, `scripts/ler_classe_java.py`, que só lê o `projectzomboid.jar` como dados. Regras completas em `catalogo/HISTORIAS.md`. Resumo: (1) **casas**: não precisam de zona; o prédio precisa de `bedroom` + (`kitchen` ou `livingroom`) + `bathroom` (sem isso não ganha nem a bagunça normal); a casa de nascimento fica de fora; no padrão, ~10% viram "construção modificada" (queimada, saqueada, esconderijo…) e 25% das outras ganham um sobrevivente morto; prédios comerciais têm histórias pelo nome do cômodo (bar, café, escritório, loja saqueada, cerco à loja de armas…). (2) **zona** (acampamento, churrasco, piquenique…): zona `ZoneStory` com nome `Forest`, `Beach` ou `Lake`, de tamanho mínimo (até 13 × 13). (3) **estrada** (batidas, bloqueio policial, pneu furado…): zona `Nav` retangular sobre o asfalto, comprimento > 30, largura 5–12, sem carro estacionado no pedaço; as rurais (cervo, animal atropelado, rebanho) pedem também estar fora da cidade e perto de zonas de mata/fazenda. Toda história é sorteada quando o pedaço carrega pela primeira vez (área já vista não ganha) e **cada zona recebe no máximo uma**. (4) **engarrafamento** (D-18): vagas com nome `trafficjamw/e/n/s` em faixas de 3 tiles.
  - **Achado principal:** o KnoxMap só grava vagas (`ParkingStall`) e área urbana (`TownZone`), **sem** `Nav` e `ZoneStory`: nos nossos mapas atuais **não haveria histórias de estrada nem de zona** (só as de casa). Solução: `scripts/gerador/zonas_historias.py` lê o mapa compilado e acrescenta essas zonas ao `objects.lua` (ruas divididas em trechos de ~48 tiles; zonas de mata fora da área urbana; engarrafamento na rua horizontal mais longa) e desenha uma figura de conferência. No pipeline: `"zonasHistorias": {}`.
  - **Teste `rsb_t8c_historias`** ("RSB Teste T8c - Historias", config `scripts/testes/t8c_historias.json`): o mesmo Botafogo do T7c + 18 zonas de estrada, 6 `Forest`, 1 `Beach`, 1 `Lake` e um engarrafamento (2 faixas de 160 tiles). **Conferido antes de entregar:** as zonas caem sobre o asfalto e o gramado certos (figura `saida/rsb_t8c_historias/zonas_historias.png`); tamanhos parecidos com os do mapa original (zonas `Nav`: largura 6 e comprimento ~36 no original; aqui 6–9 e ~55). Casas: 39 de 44 servem para histórias; 5 não (faltam quarto e/ou banheiro; corrigir no gerador). **Falta o usuário jogar** (sandbox com histórias de estrada e de zona em "Sempre que possível" e construções modificadas em "Muito frequente").
  - **Plano do teste de rodovia (T8d, D-35; espera o "pode fazer", P17):** mapa pequeno e leve para o notebook, sem baixar nada. (1) Rodovia reta e alinhada ao grid (as curvas esperam o nosso desenho, K15), desenhada por nós como estrada principal, com ~2.000 tiles (≈ 30 km reais a 1:15; ~8–10 células compiladas, poucos MB). (2) Cidade A numa ponta, nível "completa": ~10 casas, **posto copiado do mapa original** (D-38), mercadinho e farmácia (Pharmahug), vagas para achar carro. (3) Cidade B na outra ponta, nível "seca": só casas. (4) No meio, campo fora da área urbana: zonas `Nav` a cada ~48 tiles (~40), zonas de vegetação `Forest`/`FarmLand` dos lados (para as histórias rurais) e alguns acampamentos (`ZoneStory Forest`). Fora da faixa, o jogo gera a mata sozinho (T4). (5) No jogo, o usuário mede: tempo de A até B, **quanto do tanque um carro comum gasta**, travadas e FPS dirigindo, histórias vistas na estrada, zumbis na pista e a rodovia no mapa de papel. **Para que serve:** a autonomia medida define a trava do D-35 ("distância máxima sem posto"); a Dutra Rio–SP inteira (~400 km reais ≈ 26,7 km no jogo) é ~13× o teste.
  - **T8c no jogo (usuário, 42.21): só histórias de casa** (casas queimadas, portas quebradas); nenhuma de estrada nem ao redor do bairro. **Causa (K30):** o `objects.lua` gerado tinha uma vírgula faltando; o jogo recusou o arquivo inteiro e nenhuma zona carregou (`console.txt`: "Max #ZONES on one chunk is 0"). O mesmo registro confirma que o sandbox estava certo (estrada e zona em 7, "Sempre que possível"). Corrigido no script (vírgula + conferência da estrutura antes de gravar) e no mod instalado (só o `objects.lua`, com o jogo aberto). Conferido no Java: as histórias de estrada são tentadas logo depois de o jogo pôr os carros estacionados num pedaço nunca visto, e as de zona em todo pedaço que carrega; não há outra condição. **Falta o usuário jogar de novo, em jogo novo.**
  - **T8c, 2ª tentativa (usuário): tela preta** (a tecla M só faz o som; ouvem-se zumbis). Registro sem erro; as zonas carregaram (o save tem 30 carros, 29 deles no engarrafamento, ou seja, as zonas funcionam). **Causa provável (J3):** dois mapas de teste ativos juntos (`rsb_t8b_vanilla` + `rsb_t8c_historias`), os dois na célula 0,0. Pedido ao usuário: ativar só o `rsb_t8c_historias` e jogo novo.
  - **T8c, 3ª tentativa (usuário, 42.21, só o `rsb_t8c_historias` ativo): passou.** O mapa abriu normal (confirma o J3: a tela preta vinha dos dois mapas juntos). Apareceram histórias de casa, de estrada (carros batidos e abandonados) e as cenas no mapa; até veados andando pela cidade (animais do B42). **Único defeito: o engarrafamento** saiu bagunçado (carros tortos, atravessados nos cruzamentos). **Causa (K31):** no jogo, cada faixa de engarrafamento tem uma ponta arrumada e os carros ficam cada vez mais tortos longe dela (até ~115° depois de 40 tiles); a minha faixa tinha 160 tiles, passava por 4 cruzamentos e pelo pátio de concreto que o KnoxMap põe em volta dos prédios (K12). No mapa original são 630 trechos, quase todos de 5 a 30 tiles. **Correção:** trechos de até 30 tiles, só entre cruzamentos e pátios (a 2 tiles deles); aplicada no mod instalado (3 trechos nas duas mãos). **Para o gerador (Etapa 2):** zonas de estrada em trechos, zonas de mata/praia/lago fora da área urbana, engarrafamento em trechos curtos; as cenas da Av. Brasil (D-18) serão uma sequência de trechos curtos. Falta conferir o engarrafamento corrigido em jogo (opcional).
  - **P17 respondida (usuário): usar a Dutra real.** **T8d gerado e instalado** (`rsb_t8d_dutra`, "RSB Teste T8d - Dutra"; gerador `scripts/testes/t8d_dutra.py`, config `scripts/testes/t8d_dutra.json`). Traçado real da BR-116 baixado da Overpass (93 KB, autorizado; `dados/contornos/dutra_pirai_vr.json`), encolhido a 1:15 e cortado entre os pontos mais perto de Piraí e de Volta Redonda: **1.976 tiles = 29,6 km reais**, nas posições reais (Volta Redonda a noroeste, Piraí a sudeste). As duas pistas reais ficam a 1–3 tiles uma da outra a 1:15, então viram uma rodovia só, de 4 faixas (14 tiles), sem calçada; curvas no modo "como no mapa" (em degraus, K15). **Vila A, Piraí ("completa", D-35):** 12 casas, posto (ponto "fuel" do KnoxMap: loja `gasstore`, cobertura e 6 bombas Gas 2 Go do jogo, com combustível), farmácia **cópia original Pharmahug** (D-38) e mercadinho. **Vila B, Volta Redonda ("seca"):** 24 casas, nada mais. **Zonas:** 41 zonas de estrada em forma de **linha** (como as 265 do mapa original; `zonas_historias.py` ganhou linhas e a conversão pela mesma projeção do KnoxMap; conferido: 100% sobre o asfalto), 15 matas (`Forest`) dos lados, para as histórias rurais (cervo, animal atropelado), e 5 acampamentos (`ZoneStory Forest`). Mapa de 2.100 × 900 tiles, 36 células compiladas, 26 MB; compilação em 10 s. **Conferido antes de entregar:** figura `saida/rsb_t8d_dutra/zonas_historias.png` e desenho da vila de Piraí com `render_lots` (posto com bombas, letreiro da Pharmahug, mercadinho, casas). **Falta o usuário jogar** e medir: tempo e combustível de Piraí a Volta Redonda, travadas/FPS, histórias na estrada, mapa de papel.
  - **T8d no jogo (usuário, 42.21, consumo de combustível do sandbox no padrão 1,0):** viagem Piraí → Volta Redonda (~2.000 tiles, 29,6 km reais) com um Chevalier Nyala 100%: **gasolina 49 → 48,22 (0,78 unidade) em ~1 minuto de relógio real.** Extrapolação: a Dutra Rio–SP inteira (~13× o trecho) gastaria ~10 unidades, uns 20% do tanque desse carro, em ~15 min. **Conclusão para o D-35:** a 1:15, combustível não aperta a viagem; a "trava de distância máxima sem posto" quase não teria efeito. A dificuldade terá de vir de outra coisa (P18). Críticas do usuário: (1) Piraí "completa" parecia seca: quarteirões só com as lojas; (2) mercadinho vazio e com estoque de material de obra (não era cópia do original, D-38); (3) casas com a rua ao sul com a porta nos fundos; (4) pista sem acabamento, sem guard-rail nem mureta de concreto; faixas pintadas tortas ou sumindo nas diagonais; pista estreita (um carro por faixa); curvas frequentes demais. Lembrete do usuário: tudo isto é base para o mapa inteiro (fazer peças do gerador, não ajustes de um teste só).
  - **Correções (mesma sessão):** (3) era erro nosso (K33): o ajuste de porta do kit de lojas valia para todas as casas e mandava a porta para o norte; agora só vale para as nossas plantas, e as 37 casas com rua ficaram com a porta da frente para a rua (conferido no compilado). (2) mercado de bairro **copiado do mapa original** (célula 52_8, prédio 191: `grocery` + `grocerystorage` + banheiro, vitrine ao sul) em `kits/lojas/vanilla/mercado_52_8.tbx`, ligado às etiquetas `shop=convenience` e `shop=greengrocer` no `lojas.json`. (1) Piraí refeita: cada loja (posto, mercado, farmácia) num quarteirão de casas, com grama em vez de concreto (16 casas). (4) rodovia virou peça do gerador, `scripts/gerador/rodovia.py`: traçado real **suavizado** (tira detalhes menores que 20 tiles ≈ 300 m reais e arredonda as quinas; 1.840 tiles) e **pista dupla** (duas pistas de mão única de 10 tiles com 2 faixas cada e canteiro de 4); zonas de estrada em linha por pista (76). Guard-rail e mureta New Jersey não existem no jogo base: **lista do Kit Brasil** (Etapa 5, com 3D no Viewpoint). Bordas e faixas em degraus nas diagonais continuam até o nosso desenho de curvas (K15, Etapa 2). Reinstalado; conferido com `render_lots` (vila e trecho da pista).
  - **Pergunta do usuário: as cidades ficam quadradas, com quarteirões certinhos; na vida real as ruas não são curvas?** Resposta: são; a grade é só do gerador simples do T7c, usado para os testes. O gerador de verdade (Etapa 2.1, D-03) usa o contorno real **e as ruas principais reais como esqueleto** (o "eixo" já previsto no Registro do T7c), com o preenchimento em escala de jogo entre elas, e as curvas desenhadas por nós com as peças de curva do jogo (D-21/K15). A grade quadrada não vai para o mapa final.
  - **P18 respondida (usuário): "só sabor, sandbox decide".** D-35 passa a DECIDIDO, sem a trava de distância máxima sem posto: as cidades de rodovia continuam com níveis completa/parcial/seca sorteados na geração (variedade e sabor), e a dificuldade da viagem fica com as opções do sandbox do jogo. AGENTS.md atualizado.
  - **T8d corrigido no jogo (usuário):** o quarteirão da farmácia ficou grande demais para só a farmácia e 2 casas, e todo cimentado em volta. Causa: o gerador simples dos testes (quarteirão aumentado para caber a cópia da Pharmahug com a rua a oeste, com folga em volta) e o pátio de concreto que o KnoxMap põe em volta de lojas (K12). **Para o gerador da Etapa 2:** quarteirões densos, lote do tamanho de cada prédio (cópia original ou casa), lojas misturadas às casas e sem pátio de concreto onde não houver estacionamento de verdade.
  - **Ideia do usuário: estacionamento no lugar do concreto vazio.** Testado no T8d: área "parking" do KnoxMap ao lado da farmácia (ele põe vagas dentro, e o jogo põe carros nelas); o preenchimento de casas agora só pula o pedaço da loja que está na fileira da casa (a casa de trás da farmácia voltou). Conferido no compilado (`saida/rsb_t8d_dutra/farmacia_estacionamento.png`). Falta: entrada rebaixada ligando o estacionamento à rua e faixas pintadas das vagas (o KnoxMap não desenha). **Regra para o gerador (Etapa 2, junto com a P13):** comércio com sobra de terreno ganha estacionamento com vagas, ligado à rua, em vez de pátio de concreto (K12).
  - **Correção do usuário:** o estacionamento ficou solto no quarteirão (a 2 tiles da farmácia); a ideia é ser **o estacionamento da loja**, colado nela, como o do Gigamart do jogo original. **Regra do gerador (Etapa 2):** o estacionamento encosta na loja (de preferência na frente ou na lateral da frente), tem entrada pela rua da frente e fica no mesmo lote dela; a cópia original continua escolhida pela rua da frente (D-38). **O usuário pausou o teste da Dutra (T8d)** antes desta correção: o mapa instalado ainda tem o estacionamento solto; a regra vale para o gerador, não vale a pena refazer o teste agora.

- **08/11/2026 (notebook) — Etapa 1 começou.**
  - Conferido: o `main` tinha o commit "Fim da sessao: proximo passo Etapa 1"; trabalho no ramo `claude/etapa-1-sudeste-grid-c51de8`.
  - **D-02 decidido (usuário):** comparadas três projeções (EPSG:5880, policônica centrada em 45° W, transversa de Mercator em 46,5° W). A EPSG:5880 giraria o Rio 4,2° e esticaria o norte–sul em 1,5% (Vitória: 4,7° e 2,8%); a policônica centrada em 45° W deixa as capitais com menos de 1° de giro (Vitória 1,6°) e erro de distância < 0,1%. O usuário pediu as implicações de cada opção e escolheu a centrada. Origem gravada na seção 6 (E0 = −860.000 m, N0 = −1.550.000 m, OFFSET 0): Sudeste nas células 6–369 × 6–326; o Rio (Centro) na célula 272 × 256. Script `scripts/grade.py` (ida e volta conferida; rodar com o Python do `.venv` do KnoxMap, que tem o `pyproj`).
  - **Lista de dados do RJ** com tamanhos conferidos no servidor (tabela na Etapa 1): ~70–85 MB para o mapa-guia; relevo (~65 MB a 90 m) adiado para quando servir (Etapa 2.7); extrato do Sudeste (863 MB) só no PC potente. Espera autorização.
  - **Download autorizado pelo usuário.** Internet móvel a ~14 KB/s no começo; a conexão caiu duas vezes (G3) e o download da Overpass falhou e foi refeito. Erro nosso na consulta das rodovias (G5): expressas e tronco tinham ficado de fora; corrigido e baixado de novo. Mapa-guia v1 e regras v1 prontos (Etapa 1, "Andamento"); o desenho de terra e mar precisou de três correções (G4). Perguntas novas P19–P21 (cortes de tamanho, "outras localidades", aldeias e quilombos).
  - **P19–P21 respondidas pelo usuário** (ver seção 9): cortes mantidos, teto de zumbis = densidade máxima de Louisville; "outras localidades" isoladas com nome discreto; aldeias e quilombos representados. Aplicado em `kits/localidades/regras_v1.json`, `regras_localidades.py` (também tira 73 repetições do IBGE: agora 1.268 localidades; 577 vilarejos, 90 bairros, 337 só nome) e `mapa_guia_rj.py` (vilarejos e "só nome" com rótulo, os menores só onde não brigam com os maiores). Mapas gerados de novo e conferidos.
  - **D-39 (pedido do usuário): menu de teleporte do modo debug**, como no Real USA. 40 pontos em 7 grupos (`kits/marcos/teleporte.json`), convertidos pela grade; o script avisa se um ponto cair no mar (a Urca caiu, foi corrigida). Lua `RSB_TeleporteDebug.lua` feito com as mesmas funções do menu de debug do próprio jogo (`addDebugOption`, `teleportTo`, `/teleportto` no servidor, `isValidChunk` para desativar pontos fora do mapa). Instalado no mod de teste `rsb_t8c_historias` e incluído na instalação de todo mod RSB pelo `knoxmap_pipeline.py`. **Falta conferir em jogo:** nos mapas de teste atuais os pontos do Rio ficam fora do mapa (devem aparecer desativados, em cinza); o teste de verdade dos teleportes vem com o Rio da Etapa 2.
  - **Etapa 1 aprovada pelo usuário** (mapa-guia e regras de localidades v1 do RJ). Trabalho do ramo `claude/etapa-1-sudeste-grid-c51de8` juntado ao `main`. Próximo: Etapa 2 (Rio piloto) ou T5a.

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
