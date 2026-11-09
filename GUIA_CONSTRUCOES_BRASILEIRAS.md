# Guia de construções brasileiras (BuildingEd)

Para o usuário fazer à mão as construções do Kit Brasil (Etapa 5, antecipada em parte a pedido dele em 08/11/2026). Cada construção feita aqui entra no gerador do mesmo jeito que as cópias do jogo original entram hoje (`kits/lojas/`, D-38).

## 1. Existe IA que faça isso?

Não conheço nenhuma ferramenta de IA reconhecida que gere prédios de Project Zomboid com qualidade. As que existem fazem o que o KnoxMap já faz: plantas simples, com pouco detalhe (foi o que você viu na farmácia e na loja de armas feitas por regra). Os prédios bons do jogo, os do Knox County e os dos mapas famosos da Workshop, foram feitos à mão no **BuildingEd**.

O caminho para não fazer tudo do zero:

1. **Partir de uma cópia do jogo original.** As cópias que o projeto já tem (`kits/lojas/vanilla/*.tbx`) abrem direto no BuildingEd. Você troca fachada, telhado, piso e móveis e ganha um prédio "abrasileirado" com os cômodos (e o loot) já certos.
2. **Fazer à mão só o que se repete muito no mapa.** Poucas plantas boas, repetidas com variação de cor e telhado pelo gerador, enchem o mapa inteiro. A lista abaixo está em ordem de quanto cada uma aparece.
3. **O resto continua com as cópias do jogo original** (delegacia, quartel, mercado), como você aprovou, até ter tempo para elas.

## 1.1 O editor de prédios do próprio KnoxMap (comparado com o BuildingEd)

O KnoxMap (desde a versão 1.7) tem um editor de prédios dele: abra o `KnoxMap.bat`, e na barra de ferramentas da esquerda escolha o editor de prédios ("building editor"). Ele abre uma folha quadriculada em branco.

**Como ele funciona:** você dá o tamanho, diz o que o prédio é (casa, delegacia, padaria…) e desenha só os **cômodos** como retângulos, escolhendo o nome de cada um (a lista já traz primeiro os cômodos daquele tipo de prédio). A borracha recorta o contorno (prédio em L). O botão "Lay it out for me" faz uma planta pronta para você mexer. **Todo o resto ele faz sozinho:** paredes no estilo escolhido, portas, porta da rua, janelas, escada, telhado e móveis de cada cômodo. Ele salva um `.tbx` comum (em `ferramentas\knoxmap-1.8.5.2\presets\buildings\`), que abre no BuildingEd.

| | Editor do KnoxMap | BuildingEd |
|---|---|---|
| Rapidez | Muito rápido: uma planta em 5 minutos | Lento: tudo à mão |
| Cômodos com o nome certo (loot) | Sim, sempre | Sim, se você nomear certo |
| Onde fica cada móvel | Ele decide (pelo cômodo) | Você decide |
| Paredes, pisos e janelas | Só os estilos dele, todos do jogo americano | Qualquer peça, **inclusive as do Kit Brasil** (paredes de favela, lajes, muretas, caixas d'água) |
| Muro, portão, grade, garagem, quintal | Não | Sim |
| Telhado | Só o que ele escolhe | Laje, telhado inclinado, o que quiser |
| Resultado | Prédio "de regra", como a farmácia e a loja de armas que você achou pobres | Prédio com cara de Brasil |

**Conclusão: não é melhor que o BuildingEd, mas é um ótimo rascunho.** É o mesmo motor que eu usei para o "Grande Hotel Atlântida" e para a casa de laje de exemplo. O jeito mais rápido de trabalhar é:

1. No editor do KnoxMap, desenhe a **planta** (cômodos e tamanho) e salve.
2. Copie o `.tbx` de `ferramentas\knoxmap-1.8.5.2\presets\buildings\` para `kits\lojas\brasil\`, já com o nome certo (seção 5.6).
3. Abra no BuildingEd e faça o que dá a cara brasileira: troque paredes e pisos pelas peças do Kit Brasil, ponha laje, muro, portão, grade, e arrume os móveis.

Assim você pula a parte chata (paredes, portas, escada) e gasta o tempo no que importa. Esse caminho não gasta nenhum token meu.

## 2. Ordem para ir adiantando (atualizada em 09/11/2026)

Faça na ordem; cada item ensina algo para o próximo. Comece sempre pela versão **frente para o sul** (`_S`); os outros lados podem ficar para depois (seção 3.1).

| Ordem | Construção (nº da tabela abaixo) | Por que agora |
|---|---|---|
| 1 | **Botequim de esquina** (4) | Pequeno, poucos cômodos: bom para aprender o BuildingEd. Aparece no Rio piloto. |
| 2 | **Casa de favela** (15), 2 ou 3 bem pequenas | As peças do Kit Brasil para isso **já existem** (paredes de tijolo e reboco, lajes, muretas, caixa d'água, escada de concreto) e a Zona Sul do piloto tem favelas (Santa Marta, Babilônia, Cantagalo, Vidigal, Rocinha). |
| 3 | **Casa de laje térrea** (1), 2 plantas (pequena e média) | O prédio que mais se repete no RJ inteiro. Usa as mesmas lajes e muretas da favela, mais muro e portão. |
| 4 | **Padaria** (5) | Comércio de todo bairro; parte da cópia de uma padaria do jogo. |
| 5 | **Farmácia de rede** (6) | Parte da Pharmahug que já temos; é só fachada e cores. |
| 6 | **Sobrado de rua comercial** (2) | Loja embaixo e casa em cima: junta o que você aprendeu em 3 e 4. |
| 7 | **Quiosque de praia** (8) | Bem pequeno; enche a orla do piloto. |
| 8 | **Térreo do prédio de orla** (7) e **do prédio de bairro** (3) | Só o térreo (portaria e lojas); os andares o gerador faz. |
| 9 em diante | CIEP, UPA, igreja/templo, casarão, delegacia, bombeiros | Uma planta só cada, mas grandes. Deixe para quando já estiver rápido. |

Mais casas de laje (até 5 ou 6 plantas) e mais casas de favela podem entrar a qualquer momento entre os itens: elas são as que mais enchem o mapa.

## 3. Lista de construções, por prioridade

Tamanho em tiles (1 tile = 15 m no mapa, mas a construção é feita em escala de jogo, como as do Knox County). "Cômodos" são os nomes que decidem o loot (lista completa em `catalogo/CATALOGO.md`). "Começar de" é a cópia do jogo original que mais ajuda.

| # | Construção | Onde aparece | Tamanho | Cômodos (nomes do jogo) | Começar de |
|---|---|---|---|---|---|
| 1 | **Casa de laje térrea** (muro, portão de ferro, garagem coberta, laje com caixa d'água, às vezes um 2º andar "em obra") | Baixada inteira, Zona Norte, Zona Oeste, interior | 7–9 × 9–12 | `livingroom`, `kitchen`, `bedroom` (1–2), `bathroom`, `laundry` (área de serviço) | uma casa pequena do Knox County |
| 2 | **Sobrado de rua comercial** (loja embaixo, casa em cima, porta de enrolar) | Madureira, Centro de Nova Iguaçu, Caxias, Bangu, Meriti | 6–8 × 12 | térreo: `generalstore`/`clothingstore`/`bakery`…; em cima: casa | o mercado 52_8 (`kits/lojas/vanilla/mercado_52_8.tbx`) |
| 3 | **Prédio residencial de bairro** (4–6 andares, pilotis ou loja no térreo) | Tijuca, Méier, Copacabana interna, Botafogo | 10–14 × 12–16 | `bedroom`, `kitchen`, `bathroom`, `livingroom` por apartamento | o KnoxMap já gera; fazer só o térreo (portaria, lojas) |
| 4 | **Botequim / boteco de esquina** (balcão de azulejo, portas de enrolar abertas para a calçada, mesas de plástico) | Rio inteiro e Baixada | 6–8 × 8 | `bar`, `kitchen`, `bathroom`, `storage` | o bar de um posto ou lanchonete do Knox County |
| 5 | **Padaria** (balcão de vidro, vitrine de pães, mesas) | Rio inteiro | 8–10 × 10–12 | `bakery`, `kitchen`, `storage`, `bathroom` | uma padaria/café do Knox County |
| 6 | **Farmácia de rede** (fachada colorida, corredor de prateleiras, balcão de remédios) | Rio inteiro | 8–10 × 12–14 | `pharmacy`, `pharmacystorage`, `bathroom` | a Pharmahug (`farmacia_pharmahug.tbx`) |
| 7 | **Prédio de orla** (térreo com lojas, portaria, 10–14 andares) | Copacabana, Ipanema, Leblon, Flamengo | 14–20 × 16 | térreo: `bar`/`cafe`/`generalstore` + `hall`; andares: apartamentos | o KnoxMap gera os andares; fazer o térreo |
| 8 | **Quiosque de praia** (e guarda-sóis na areia: ideia sua do 2º teste) | Toda a orla | 3–4 × 3–4 | `bar` ou `cafe` | peça pequena; feita do zero |
| 9 | **CIEP ("Brizolão")** (o prédio de concreto da escola pública, sempre igual) | Rio inteiro e Baixada (centenas, todos iguais) | 40 × 16 aprox. | `classroom`, `office`, `kitchen`, `bathroom`, `medical` | uma escola do Knox County |
| 10 | **Delegacia (DP) brasileira** | Rio inteiro | 12–16 × 14 | `policeoffice`, `policegunstorage`, `prisoncells`, `bathroom` | a delegacia já copiada (9_54, com estacionamento) |
| 11 | **Quartel do Corpo de Bombeiros (CBMERJ)** | Rio e Baixada | 20–26 × 20 | `firegarage`, `firestorage`, `kitchen`, `bedroom`, `gym` | o quartel de Louisville já copiado (23_20) |
| 12 | **UPA 24h** (pronto atendimento, padrão do governo) | Rio inteiro e Baixada | 20 × 16 aprox. | `medical`, `medicalstorage`, `office`, `bathroom` | uma clínica do Knox County |
| 13 | **Igreja de bairro / templo evangélico** | Rio inteiro; templos muito comuns na Baixada | 10–14 × 16–20 | `church`, `office`, `bathroom` | uma igreja do Knox County |
| 14 | **Casarão antigo** (Santa Teresa, Laranjeiras, Petrópolis) | Santa Teresa, Glória, Serra | 12–16 × 14 | casa grande: `livingroom`, `bedroom`, `kitchen`… | uma casa grande do Knox County |
| 15 | **Casa de favela** (alvenaria aparente, empilhada, laje) e a casa de "chefe do morro" (D-31) | Favelas do RJ | 5–7 × 6–8 | casa mínima | item 1, simplificado |

### 3.1 Quantas plantas de cada uma, e para que lados

**Por que os lados importam:** o gerador não gira os prédios (o KnoxMap usa o arquivo como foi desenhado). Um prédio desenhado com a porta para o sul só entra onde a rua fica ao sul do lote. Foi por isso que a delegacia sumiu do mapa quando as ruas mudaram: só havia a versão "porta para o leste". Então cada planta precisa de **uma versão para cada lado da rua (norte, sul, leste, oeste)**; prédio raro pode ter só 1 ou 2 lados.

**Como fazer as versões sem redesenhar:** no BuildingEd, menu **Building → girar (rotate) / espelhar (mirror)**. Paredes, portas, janelas, escada e móveis colocados pelas ferramentas giram junto e ficam certos (cada móvel tem um desenho para cada direção). O que foi **pintado à mão no Tile Mode** mantém o mesmo desenho e pode ficar virado errado: confira esses itens depois de girar (placas, letreiros, peças de parede pintadas, móvel que não tem as 4 direções). Salve cada versão com o lado no nome: `casa_laje_01_S.tbx`, `casa_laje_01_N.tbx`, `casa_laje_01_L.tbx` (leste), `casa_laje_01_O.tbx` (oeste); o lado é onde fica a rua, a porta da frente (regras completas na seção 5.6).

**Cores e acabamentos ficam comigo:** você faz uma planta e eu gero as variações de cor da fachada (trocando as peças de parede no arquivo, como fiz no hotel), para a rua não ficar com casas todas iguais.

| # | Construção | Plantas diferentes (ideal) | Lados |
|---|---|---|---|
| 1 | Casa de laje térrea | **5 a 6**: pequena (7×9), média (9×11), com garagem, sobrado de 2 andares, com "puxadinho" na laje, de esquina | 4 lados cada |
| 2 | Sobrado de rua comercial | 3 (loja estreita, loja larga, duas lojas embaixo) | 4 |
| 3 | Prédio de bairro (só o térreo: portaria e lojas) | 2 a 3 | 4 |
| 4 | Botequim de esquina | 2 a 3 | 4 |
| 5 | Padaria | 2 | 4 |
| 6 | Farmácia de rede | 2 | 4 |
| 7 | Prédio de orla (térreo com lojas) | 2 | 4 (a orla muda de direção ao longo da praia) |
| 8 | Quiosque de praia | 1 a 2 | 2 (virado para a areia) |
| 9 | CIEP | **1** (na vida real são todos iguais) | 4 |
| 10 | Delegacia (DP) | 1 a 2 (já temos cópias do jogo original) | 4 |
| 11 | Quartel do Corpo de Bombeiros | 1 | 4 |
| 12 | UPA 24h | **1** (projeto padrão do governo) | 4 |
| 13 | Igreja / templo evangélico | 2 a 3 | 4 |
| 14 | Casarão antigo | 2 | 2 a 4 |
| 15 | Casa de favela | 4 a 6 bem pequenas | 4 |

Somando: cerca de 35 plantas, cada uma com até 4 lados (os lados saem pelo giro, não precisam ser desenhados de novo). Comece pela casa de laje: com 2 plantas nos 4 lados já dá para testar no gerador.

Mais tarde (não urgente): banca de jornal, orelhão e ponto de ônibus (calçadões vazios, U15), posto de gasolina brasileiro, supermercado de rede, feira livre, estação de trem (SuperVia), lojas do Saara.

## 4. Fotos de referência reais (Wikimedia Commons, fotos livres)

As "categorias" são galerias com dezenas a centenas de fotos do lugar; os "arquivos" são fotos escolhidas.

### Zona Sul (Copacabana, Ipanema, Leblon): o que já está no Rio piloto
- Galerias: [Avenida Atlântica](https://commons.wikimedia.org/wiki/Category:Avenida_Atl%C3%A2ntica_(Rio_de_Janeiro)) (61 fotos), [Copacabana](https://commons.wikimedia.org/wiki/Category:Copacabana_(Rio_de_Janeiro)), [Ipanema](https://commons.wikimedia.org/wiki/Category:Ipanema), [Leblon](https://commons.wikimedia.org/wiki/Category:Leblon).
- Prédio de orla (item 7): [Edifício nº 4160 da Av. Atlântica](https://commons.wikimedia.org/wiki/File:Edif%C3%ADcio_n%C2%BA._4160_-_Av._Atl%C3%A2ntica.JPG), [Edifício Araguaya](https://commons.wikimedia.org/wiki/File:Edif%C3%ADcio_Araguaya.JPG), [Edifício Jangada](https://commons.wikimedia.org/wiki/File:Edif%C3%ADcio_Jangada.jpg).
- Prédio de bairro (item 3): [Prédio na Rua Barata Ribeiro, Copacabana](https://commons.wikimedia.org/wiki/File:Pr%C3%A9dio_na_Rua_Barata_Ribeiro,_Copacabana_-_Rio_de_Janeiro.jpg), [Edifício Estrela do Rio](https://commons.wikimedia.org/wiki/File:Edif%C3%ADcio_Estrela_do_Rio.jpg).
- Botequim (item 4): [Botequim Informal, Copacabana](https://commons.wikimedia.org/wiki/File:Botequim_Informal_-_Copacabana.JPG), [Botequim Gato Preto](https://commons.wikimedia.org/wiki/File:Botequim_Gato_Preto.jpg).
- Quiosque (item 8): [Quiosque na orla](https://commons.wikimedia.org/wiki/File:Quiosque_da_Coca-Cola.jpg) (a marca sai no Kit Brasil, por direitos).
- Delegacia (item 10): [14ª DP (Leblon)](https://commons.wikimedia.org/wiki/File:14%C2%BA_DP_(5304885756).jpg), [13ª DP (Copacabana)](https://commons.wikimedia.org/wiki/File:13%C2%BA_DP_(5310671762).jpg).

### Centro
- Sobrado comercial e Saara (item 2): [Saara, Centro do Rio](https://commons.wikimedia.org/wiki/File:Saara,_Centro_do_Rio_de_Janeiro-RJ.jpg), [Centro (Saara)](https://commons.wikimedia.org/wiki/File:Centro_(SAARA)_(23573470834).jpg).
- Bombeiros (item 11): [Quartel do Comando Geral do CBMERJ](https://commons.wikimedia.org/wiki/File:Quartel_do_Comando_Geral_do_Corpo_de_Bombeiros_-_CBMERJ.jpg) (é a sede histórica; o quartel de bairro é mais simples).
- Padaria (item 5): [Padaria Mar e Terra (acervo IMS)](https://commons.wikimedia.org/wiki/File:Padaria_Mar_e_Terra,_Acervo_do_Instituto_Moreira_Salles.jpg), [Padaria popular](https://commons.wikimedia.org/wiki/File:Padaria_popular_(49255316546).jpg).

### Santa Teresa e Zona Norte
- Casarão (item 14): galeria de [Santa Teresa](https://commons.wikimedia.org/wiki/Category:Santa_Teresa_(Rio_de_Janeiro)) (215 fotos).
- Subúrbio e comércio de rua (itens 1 e 2): galerias de [Madureira](https://commons.wikimedia.org/wiki/Category:Madureira) e [Bangu](https://commons.wikimedia.org/wiki/Category:Bangu).
- CIEP (item 9): [CIEP em Cascadura](https://commons.wikimedia.org/wiki/File:CIEP_Professor_Manoel_Maur%C3%ADcio_de_Albuquerque.JPG), [os CIEPs do Brizola](https://commons.wikimedia.org/wiki/File:Centros_Integrados_de_Educa%C3%A7%C3%A3o_P%C3%BAblica_-_CIEPs_do_Brizola.jpg).
- Favela (item 15): galeria da [Rocinha](https://commons.wikimedia.org/wiki/Category:Rocinha) (187 fotos).

### Baixada Fluminense
- Galerias: [Nova Iguaçu](https://commons.wikimedia.org/wiki/Category:Nova_Igua%C3%A7u) (149 fotos), [Duque de Caxias](https://commons.wikimedia.org/wiki/Category:Duque_de_Caxias_(Rio_de_Janeiro)) (171), [Belford Roxo](https://commons.wikimedia.org/wiki/Category:Belford_Roxo) (88), [Nilópolis](https://commons.wikimedia.org/wiki/Category:Nil%C3%B3polis), [São João de Meriti](https://commons.wikimedia.org/wiki/Category:S%C3%A3o_Jo%C3%A3o_de_Meriti), [Mesquita](https://commons.wikimedia.org/wiki/Category:Mesquita_(Rio_de_Janeiro)).
- Rua de casas (item 1): [Rua Paiva Couceiro, Belford Roxo](https://commons.wikimedia.org/wiki/File:Brasil_-_Rio_de_Janeiro_-_Belford_Roxo_-_Rua_Paiva_Couceiro.jpg), [Chacrinha, Nova Iguaçu](https://commons.wikimedia.org/wiki/File:Chacrinha_-_Nova_Igua%C3%A7u,_RJ.jpg), [Rua Uruaçu, Nova Iguaçu](https://commons.wikimedia.org/wiki/File:Rua_Urua%C3%A7u_-_panoramio.jpg).
- Comércio de rua (item 2): [Cruzamento da Rua Dr. Barros Júnior com a Via Light, Nova Iguaçu](https://commons.wikimedia.org/wiki/File:Cruzamento_Rua_Dr_Barros_Junior_Via_Light_Nova_Igua%C3%A7u.jpg), [Via Light no Centro de Nova Iguaçu](https://commons.wikimedia.org/wiki/File:Rodovia_Via_Light_no_Centro_de_Nova_Igua%C3%A7u.jpg).
- CIEP (item 9): [CIEP Vinicius de Moraes, Belford Roxo](https://commons.wikimedia.org/wiki/File:CIEP_Brizol%C3%A3o_Vinicius_de_Moraes_2024-06-13.jpg), [CIEP 172, Nova Iguaçu](https://commons.wikimedia.org/wiki/File:2011-06-12_CIEP_Brizol%C3%A3o_172_N%C3%A9lson_Rodrigues.JPG), [CIEP Nelson Ramos, Mesquita](https://commons.wikimedia.org/wiki/File:CIEP_Nelson_Ramos.JPG).

Outra fonte boa, sem baixar nada: o **Street View do Google Maps** na rua exata (ex.: qualquer rua de Belford Roxo ou do Leblon). Para a fachada da casa de laje, ele é melhor que qualquer foto avulsa.

## 5. Tutorial: como fazer uma construção no BuildingEd

### 5.1 Onde está
O BuildingEd **já está no seu computador**: veio junto com o KnoxMap, em
`ferramentas\knoxmap-1.8.5.2\vendor\PZMappingTools\bin\BuildingEd.exe`
(é a edição "PZTools Unofficial", mantida pela comunidade, com suporte à Build 42 e a prédios de até 32 andares). As imagens das peças do jogo ficam em `...\PZMappingTools\Tiles`.

### 5.2 Primeira vez
1. Abra o `BuildingEd.exe`. Na primeira vez ele pergunta onde estão as peças (Tiles): aponte para a pasta `Tiles` ao lado do `bin` (se ele já abrir com as peças carregadas, pule).
2. Para aprender, **abra uma cópia pronta**: *File → Open* e escolha `kits\lojas\vanilla\mercado_52_8.tbx` (o mercado do Knox County). Veja como ele é montado antes de fazer o seu. Salve com outro nome (*File → Save As*) antes de mexer.

### 5.3 Os conceitos (o que cada coisa faz)
- **Andares (floors):** cada andar é uma grade. Troque de andar pelo painel de andares ou com Page Up/Page Down.
- **Cômodos (rooms):** você pinta o chão de cada cômodo com a ferramenta de cômodo. **O nome do cômodo decide o loot**: um cômodo chamado `pharmacy` vira farmácia no jogo, `bar` vira bar, `kitchen` vira cozinha. Os nomes ficam em *Building → Rooms* (use os da tabela da seção 3; a lista inteira está em `catalogo/CATALOGO.md`).
- **Paredes:** as paredes de fora e de dentro saem sozinhas na borda dos cômodos; o estilo (tijolo, reboco, azulejo) é escolhido por cômodo e para a fachada.
- **Portas e janelas:** ferramentas próprias; clique na parede onde quer.
- **Escada:** ferramenta de escada; ocupa 3 tiles e liga um andar ao de cima.
- **Móveis e objetos:** painel de mobília (*Furniture*) ou peças soltas (*Tiles*): balcão, geladeira, prateleira, mesa, cama. Use só móveis do jogo (D-16), assim não pesa e aparece no Viewpoint.
- **Telhado:** ferramenta de telhado, desenhada por cima do último andar. Para a laje brasileira, use telhado plano (ou chão de concreto no andar de cima) e uma caixa d'água em cima.

### 5.4 Passo a passo da casa de laje (item 1)
1. *File → New*: tamanho 9 × 12.
2. Pinte os cômodos do térreo: sala (`livingroom`) na frente, cozinha (`kitchen`) atrás, 2 quartos (`bedroom`), banheiro (`bathroom`) e área de serviço (`laundry`) nos fundos. Deixe 2–3 tiles livres na frente para a garagem/quintal.
3. Escolha parede de fora rebocada e pintada (cores claras: bege, verde-água, rosa) e piso de cerâmica.
4. Porta da frente na sala, porta da cozinha para os fundos, janelas nos quartos e na sala.
5. Móveis: sofá e TV na sala; fogão, geladeira, pia e mesa na cozinha; cama e guarda-roupa nos quartos; vaso, pia e chuveiro no banheiro; tanque e máquina de lavar na área.
6. Andar de cima: laje (chão de concreto, sem telhado) com caixa d'água; opcional: um quartinho "em obra" só com paredes.
7. Muro baixo e portão na frente: isso é terreno, não prédio. Por enquanto deixe de fora; depois eu levo o terreno junto, como fiz com o estacionamento da delegacia.
8. *File → Save* como `kits\lojas\brasil\casa_laje_01.tbx` (crie a pasta `brasil`).

### 5.4.1 Laje reta (em vez do telhado inclinado)
O telhado não é o "Ceilings" (isso é o forro, visto por dentro). Use a **ferramenta de telhado (Roof Tool)** com o tipo **Flat Top** cobrindo a casa, com **profundidade (Depth) Three**: a laje vira o chão do andar de cima, onde dá para andar. Na janela **Tiles**, categoria **Roof Tops**, em **Expert Mode**, crie uma entrada com uma peça de concreto em todos os espaços (ex.: `floors_exterior_street_01_016`) e escolha essa entrada no telhado.

**Exemplo pronto:** `kits\lojas\brasil\casa_laje_exemplo.tbx` (abra no BuildingEd). Casa térrea 9 × 10 com laje de concreto, guarda-corpo branco em volta e caixa d'água; também está no mapa (teleporte TESTE: "Casa de laje exemplo - Humaita"). Foi gerada por `scripts/gerador/predio_desenhado.py` (planta `casa_laje_exemplo.json`) e `scripts/gerador/laje.py` (mureta e caixa d'água).

### 5.4.2 Cercas, grades, guarda-corpos e outros objetos ("fixtures")
- No BuildingEd, cerca, grade, guarda-corpo, caixa d'água, ar-condicionado etc. são **móveis (furniture)**: ferramenta **Furniture Tool**, escolher a peça no painel de móveis e clicar. Perto da parede ou da borda, ele escolhe sozinho para que lado a peça fica virada.
- Se a peça não estiver em nenhuma categoria de móveis: janela **Tiles** → crie uma **categoria de móveis** sua (botões embaixo da lista; dois cliques para dar nome, ex.: "Brasil") → arraste a peça da lista de peças para dentro dela. Cada entrada tem uma peça por direção (oeste, norte, leste, sul). Exemplos de folhas: `fixtures_railings_01` (guarda-corpos: a peça 64 é o lado oeste e a 65 o lado norte), `fencing_01` (cercas e muros baixos), `fixtures_doors_fences_01` (portões), `rooftop_furniture` (caixas e aparelhos de telhado).
- Camada (**Layer**, embaixo da lista): "Furniture" é o normal; "Walls" troca a parede por aquela peça (portão de garagem, vitrine larga); "WallOverlay" é para o que fica pintado na parede.
- **Cerca e muro do quintal (fora da casa)** não fazem parte do prédio no BuildingEd: são terreno. Faça a casa sem eles; eu levo o quintal junto como "entorno", como fiz com o estacionamento da delegacia. Se quiser desenhar o quintal você mesmo, dá para fazer a casa com uns tiles a mais e a cerca nessa borda; me avise que eu ajusto o gerador.

### 5.4.3 Casa com muro, portão e garagem a céu aberto (o "combo" da Baixada)
O BuildingEd não junta dois arquivos de prédio num só. O jeito certo é fazer **um arquivo só, do tamanho do terreno inteiro**:
1. *File → New* com o tamanho do lote todo (ex.: 12 × 15 para uma casa de 9 × 10 com quintal e garagem).
2. Pinte os cômodos só onde fica a casa. O resto (quintal, garagem) fica **sem cômodo**: é área de fora, mas dentro do arquivo.
3. **Piso da garagem e do quintal:** no **Tile Mode**, pinte o chão de cimento ou lajota nos quadrados sem cômodo (camada de chão, "Floor").
4. **Muro:** peças de muro ou cerca (ex.: folha `fencing_01`) como móveis ou no Tile Mode, na borda do terreno. **Portão:** `fixtures_doors_fences_01` ou um portão de garagem na camada "Walls".
5. Garagem coberta é um cômodo `garage`; garagem a céu aberto é só o piso, sem cômodo e sem telhado.
6. Salve como uma versão "com muro" da casa (ex.: `casa_laje_01_muro_S.tbx`). Vale ter as duas: com muro (Baixada, subúrbio) e sem muro.

Funciona: o estacionamento da delegacia copiada já é exatamente isso (prédio + terreno com chão e cerca num arquivo só) e saiu certo no mapa. Se preferir fazer a casa e o terreno em arquivos separados, me mande os dois que eu junto por script, mas é mais seguro fazer num arquivo só.

### 5.5 Regras para o gerador conseguir usar
- **A porta da frente define o lado da rua.** Faça a porta da frente virada para baixo/esquerda da tela (lado sul) ou avise qual lado é; o gerador não gira o prédio (K35).
- **Tamanho fixo:** anote o tamanho; o gerador reserva um lote exatamente desse tamanho.
- **Nada encostado na borda:** deixe a borda livre para a calçada; o muro e o quintal entram depois como "entorno".
- **Um prédio por arquivo**, com 2 ou 3 variações (cores, telhado) em arquivos separados.

### 5.6 Nomes dos arquivos e como me entregar

Salve tudo em `kits\lojas\brasil\`. O nome tem 3 partes, separadas por `_`:

`<tipo>_<número da planta>_<lado da rua>.tbx`

- **tipo**: um dos nomes abaixo, sempre igual.
- **número**: `01`, `02`, `03`… uma planta diferente = número novo.
- **lado**: onde fica a rua (a porta da frente): `S` (sul, embaixo na tela do BuildingEd), `N`, `L` (leste) ou `O` (oeste).
- Só letras minúsculas sem acento, números e `_`. Sem espaço, sem `ç`, sem acento (o jogo e os scripts tropeçam neles).

| Construção | tipo no nome | Exemplo |
|---|---|---|
| Casa de laje térrea (ou com 2º andar) | `casa_laje` | `casa_laje_01_S.tbx` |
| Casa de favela | `casa_favela` | `casa_favela_03_S.tbx` |
| Casa do "chefe do morro" (D-31) | `casa_chefe` | `casa_chefe_01_S.tbx` |
| Sobrado de rua comercial | `sobrado_loja` | `sobrado_loja_02_L.tbx` |
| Térreo de prédio de bairro | `predio_bairro` | `predio_bairro_01_S.tbx` |
| Térreo de prédio de orla | `predio_orla` | `predio_orla_01_S.tbx` |
| Botequim | `botequim` | `botequim_01_S.tbx` |
| Padaria | `padaria` | `padaria_01_S.tbx` |
| Farmácia | `farmacia` | `farmacia_01_S.tbx` |
| Quiosque de praia | `quiosque` | `quiosque_01_S.tbx` |
| CIEP | `ciep` | `ciep_01_S.tbx` |
| Delegacia | `delegacia` | `delegacia_01_S.tbx` |
| Bombeiros | `bombeiros` | `bombeiros_01_S.tbx` |
| UPA | `upa` | `upa_01_S.tbx` |
| Igreja / templo | `igreja` / `templo` | `templo_01_S.tbx` |
| Casarão antigo | `casarao` | `casarao_01_S.tbx` |

Regras:
- **Mesma planta, outro lado da rua** = mesmo número, só troca a letra (`casa_laje_01_S` girada vira `casa_laje_01_L`).
- **Mesma planta, só outra cor** não precisa de arquivo: as cores eu faço por script (seção 3.1). Se você quiser uma variação feita à mão (outra fachada, outro telhado), ela ganha número novo.
- **Ainda não terminou?** Ponha `_rascunho` no fim (`padaria_01_S_rascunho.tbx`). Eu não ligo rascunhos no gerador.
- Não renomeie um arquivo que eu já liguei ao gerador; se precisar, me avise.

**Anotações (opcional, mas economiza tempo de conversa):** no mesmo arquivo de texto `kits\lojas\brasil\ANOTACOES.txt`, escreva uma linha por planta, assim:

```
casa_laje_01: Baixada, Zona Norte. Garagem coberta, laje com caixa d'água.
botequim_01: Rio inteiro, de esquina.
```

Quando juntar algumas, me diga "liguei construções novas em kits\lojas\brasil". Eu leio as anotações, ligo no gerador, instalo e coloco os lugares no grupo TESTE do teleporte para você conferir em jogo.

### 5.7 Peças do botequim ("Bar Ponto Certo") no BuildingEd

Prontas desde 09/11/2026 e já registradas no BuildingEd (feche e abra o BuildingEd de novo para ele ler):
- **Paredes:** nas listas de parede externa e interna aparecem 4 estilos novos: azulejo branco com faixa verde (salão), azulejo verde-claro (cozinha e banheiro), fachada amarela e fachada verde, as duas com barra de cerâmica vermelha. Use com a ferramenta de parede, assim eu consigo fazer as variações de cor depois.
- **Pisos:** na lista de pisos: ladrilho hidráulico, xadrez preto e branco, granilite e lajota vermelha.
- **Móveis e objetos:** no modo de peças (Tile Mode), folha `rsb_botequim_01`. O fim do nome diz o lado da frente: `_s` sul, `_l` leste, `_n` norte, `_o` oeste.
  - Balcão de azulejo e balcão com estufa: a frente de azulejo fica para o cliente e as prateleiras com garrafas para quem atende. Guardam coisas como o balcão de bar do jogo.
  - Freezer de sorvete, cervejeira (funciona como geladeira), cadeiras e mesas de plástico, engradados e pilha de cadeiras.
  - **Letreiro** (2 peças, lado a lado): na fachada para o sul, as peças `letreiro_n_1` (à esquerda, no tile a oeste) e `letreiro_n_2` (à direita), postas na **parede norte do tile da calçada**, encostadas na fachada. Na fachada para o leste, as peças `letreiro_o_1` (no tile ao sul) e `letreiro_o_2` (ao norte), na parede oeste do tile da calçada.
  - **Lousa de cardápio:** `lousa_cardapio_n` na parede norte, `lousa_cardapio_o` na parede oeste.
  - **Porta de enrolar:** a "aberta" (só o rolo em cima) vai no tile de uma porta sem folha; a "fechada" vai sobre um pedaço de parede comum (loja fechada).
  - Letreiro, lousa e portas de enrolar são peças de parede: ponha na camada de objetos de parede do modo de peças. Se não aparecerem ali, use a camada de móveis.

### 5.8 Peças da casa de laje no BuildingEd

Prontas desde 09/11/2026 e registradas no BuildingEd (feche e abra de novo). Prévia: `saida\kit_tiles\previa_casa_laje.png`.

**Já existiam e servem para a casa de laje:** laje de cobertura e terraço (lista de telhado plano e de pisos), muretas da laje, caixa d'água, varal, churrasqueira, pilar com ferro de espera (folhas `rsb_lajes_01`, `rsb_muretas_favela_01`, `rsb_objetos_laje_01`), paredes de reboco e de tijolo (`rsb_paredes_favela_01`), cerâmica vermelha e bege e cimento queimado (`rsb_pisos_favela_01`), lajota vermelha (`rsb_pisos_botequim_01`).

**Novas:**
- **Paredes** (listas de parede, use a ferramenta de parede): grafiato amarelo, verde-claro e pêssego, branco com pintura nova, grafiato azul-claro com barra de pedra miracema embaixo, cerâmica de fachada em filetes.
- **Pisos:** pedra miracema (quintal e garagem), ardósia (varanda e sala), cerâmica rústica de garagem, cerâmica branca 45 × 45 (sala e quartos), cimentado de garagem com mancha de óleo, bloquete (calçada).
- **Muros** (folha `rsb_muros_casa_01`, modo de peças, camada de paredes): muro de 2 m de tijolo, chapiscado, amarelo, branco, e muro baixo branco com grade em cima. Cada estilo tem 4 peças: norte, oeste, quina e pilar (ponha o pilar na ponta solta do muro). Funcionam como o muro alto de madeira do jogo: bloqueiam e dá para pular com esforço.
- **Portões** (folha `rsb_portoes_casa_01`, camada de paredes): portão social de grade preta, de chapa branca e de grade verde; use a peça **fechada** da parede certa (`_fechado_n` ou `_fechado_o`): o jogo abre e fecha sozinho. Portão de garagem de chapa branca ou marrom, com 3 peças lado a lado (`_1`, `_2`, `_3`), também fechado; ele abre como o portão de garagem do jogo.
- **Objetos** (folha `rsb_objetos_casa_01`): tanque de lavar (tem água, como pia), botijão de gás, vaso de espada-de-são-jorge, cadeira de fio vermelha, azul e verde (4 lados). Peças de parede (norte e oeste): relógio de luz, número com interfone e caixa de correio (no muro, ao lado do portão), grade de janela reta ou de losangos (na frente da janela).

### 5.9 Manchas e desgaste (por cima da parede)

Desde 09/11/2026 (D-47) todas as paredes do Kit Brasil são **limpas**. Mancha é uma peça à parte, que você põe por cima:
- **Sujeira** (sai quando o jogador limpa com água sanitária e pano, vassoura ou esfregão): lama na base, escorrido de chuva, mofo na base, gordura e fuligem (cozinha, bar). Folha `rsb_overlay_grime_wall_01`.
- **Reboco estragado** (permanente, nenhuma limpeza tira): tinta descascando, reboco caído mostrando o tijolo, rachaduras, buraco grande no reboco. Folha `rsb_desgaste_parede_02`. Servem em parede de qualquer cor.

Como pôr: no BuildingEd, a sujeira do prédio inteiro se escolhe em **Grime** (as 8 opções novas estão na lista); para pôr só num pedaço, use o modo de peças e pinte a peça da mancha por cima da parede (oeste, norte, quina, janela ou porta, como a parede embaixo). Dá para usar uma de cada folha na mesma parede (desgaste + sujeira).

### 5.10 CIEP pronto e peças do CIEP

O CIEP já foi desenhado (09/11/2026): `OneDrive\Área de Trabalho\RealSudesteBrasil\Construcoes BuildingEd\CIEP\ciep_01_S.tbx`, com a prévia `ciep_01_S_previa.png` ao lado. Abra no BuildingEd para ver e mexer.

Peças do CIEP no BuildingEd:
- **Paredes de fora:** concreto com peitoril verde, vermelho com faixa amarela, ou azul. A porta nessas paredes vira arco.
- **Paredes de dentro:** barra a óleo verde ou azul até 1,3 m.
- **Janela larga de 2 tiles, de vidro limpo** (folha `rsb_janelas_ciep_01`): ponha a metade 1 (peças 0 e 1) num tile e a metade 2 (peças 2 e 3) no tile seguinte, à direita na parede norte ou mais ao sul na parede oeste. A parede de concreto do CIEP abre o recorte certo sozinha.
- **Pisos:** paviflex bege e marrom, paviflex cinza, cimentado do pátio.
- **Galeria (térreo vazado):** arco largo de 2 tiles (peças 64 e 65 = metade 1, 66 e 67 = metade 2, como a janela) e arco de 1 tile (60 e 61), com pilar (63). São vãos de porta sem porta: dá para passar. No BuildingEd, ponha com a ferramenta de parede (estilos de parede de fora "arco") na borda da área aberta; a área da galeria fica **sem cômodo**, e o chão você pinta no modo de peças (cimentado do pátio).
- **Objetos:** carteira universitária (4 lados), bebedouro, quadro verde e letreiro "CIEP 501" (3 peças lado a lado, 2 m de altura, parede norte ou oeste).

**Onde fica o BuildingEd:** `C:\Users\yanbe\Zomboid\RealSudesteBrasil\ferramentas\knoxmap-1.8.5.2\vendor\PZMappingTools\bin\BuildingEd.exe`.

## 6. Peças novas (tiles brasileiras)

Para o que o jogo base não tem: telha colonial, azulejo português, pedra portuguesa da calçada, fachada pintada, orelhão, placa em português. Regra do projeto: toda peça nova precisa aparecer em 3D no Viewpoint (D-07, D-09), então cada peça nova passa pelo teste do Viewpoint antes de ser usada em massa.

### 6.1 O formato
- Cada peça é um desenho isométrico de **128 × 256 pixels** (tamanho "2x"; o jogo também usa a metade, 64 × 128). As peças ficam juntas numa **folha** (PNG), em colunas de 8.
- O nome da peça é o nome da folha + o número dela (ex.: `rsb_telhas_01_3`). Use o prefixo `rsb_` para nunca bater com o nome de uma peça do jogo.

### 6.2 Fazer a folha: TileSetZ (já instalado, dentro do TileZed)
1. Abra `ferramentas\knoxmap-1.8.5.2\vendor\PZMappingTools\bin\TileZed.exe` → **Tools → TileSetZ - Create and Edit Tiles**.
2. **File → New Tilesheet**, peça de 128 × 256, 8 colunas.
3. O jeito mais rápido é **gerar a partir de uma textura** (aba *Tilesheets, textures & masks* → **Open Source Texture**), escolhendo o método:
   - **Roofs**: telhado a partir de uma foto ou textura reta de telha (é o caminho para a telha colonial ou de fibrocimento).
   - **Wall masks**: parede a partir de uma textura reta (reboco pintado, azulejo, tijolo aparente). Use **Precut texture into wall tiles** para murais, letreiros e fachadas maiores que uma peça.
   - **Floor masks**: piso (pedra portuguesa, lajota, cimento queimado).
   - **Street curbs**: meio-fio.
   - **Fit inside one tile**: um objeto só (placa, orelhão visto de frente).
4. Confira o resultado (**Generate Preview**, *Assembly check*) e use **Append to Current Sheet** ou **Use as New Sheet**.
5. Também dá para desenhar à mão na aba *Draw tiles* (lápis, borracha, balde, linhas, zoom até 32×).
6. **File → Save As** dentro da pasta `Tiles\2x` das ferramentas (assim o BuildingEd e o TileZed enxergam a folha).

As texturas de origem podem vir de fotos suas ou de bancos livres (o Wikimedia Commons tem texturas de azulejo e pedra portuguesa). Foto de terceiro com direitos não serve.

### 6.3 Dizer ao jogo o que a peça é (propriedades)
No TileZed: **Tools → Tile Definitions** (o editor das "TileDefs"). Ali cada peça recebe as propriedades: se é parede, chão, se bloqueia passagem, de que material é etc. A explicação de cada propriedade está em `vendor\PZMappingTools\docs\TileZed\TileProperties\index.html`. O jeito mais seguro é copiar as propriedades de uma peça parecida do jogo (ex.: a telha nova copia as de uma peça de telhado do jogo).

### 6.4 O que fica comigo
- Empacotar as folhas no formato do jogo (`.pack`), gravar o arquivo de propriedades (`.tiles`) e ligar tudo no mod (`mod.info`, com um número de arquivo de peças só nosso). **Já funciona (08/11/2026):** `scripts/gerador/kit_tiles.py` junta todas as folhas de `kits/tiles/` (cada uma com um `.json` dizendo o que é cada peça) em `rsb_kitbrasil.floor.pack` + `rsb_kitbrasil.tiles`, e o pipeline instala no mod (`pack=rsb_kitbrasil.floor`, `tiledef=rsb_kitbrasil 7391`). A 1ª folha é a do calçadão de Copacabana (`rsb_calcadao_01`, D-45), feita por script. Pisos vão no pacote `.floor` (sem compressão); paredes, telhados e escadas no `rsb_kitbrasil.pack`. Cada peça leva as propriedades da peça equivalente do jogo. `kit_tiles.buildinged()` registra as folhas no TileZed/BuildingEd (`Tilesets.txt` e `BuildingTiles.txt` das ferramentas, com cópia `.antes_rsb` da versão original). **Peças da favela prontas (08/11/2026):** no BuildingEd, os estilos novos aparecem no fim das listas de parede externa/interna, piso, telhado plano (laje) e escada; ver `KIT_BRASIL_LISTA.md`, grupo 8.
- Registrar o 3D no Viewpoint (D-07) e testar no isométrico e no Viewpoint.
- Usar a peça no gerador (estilos de fachada, telhado, calçada).

Então o seu trabalho termina no passo 6.3: me mande a folha PNG e diga o que é cada peça. Comece por **uma** peça (sugestão: a telha colonial, pelo método **Roofs**), para testarmos o caminho inteiro antes de fazer muitas.

## 7. Fontes
- Fotos: Wikimedia Commons (links acima; cada foto tem a licença e o autor na página dela).
- BuildingEd/TileZed/WorldEd: edição comunitária "PZTools Unofficial", que vem com o KnoxMap (`vendor\PZMappingTools\README.md`), continuação das ferramentas de Tim Baker ([pzworlded](https://github.com/timbaker/pzworlded), [tiled](https://github.com/timbaker/tiled)); outra edição comunitária: [Unjammer/TileZed](https://github.com/Unjammer/TileZed). A The Indie Stone anunciou que vai lançar as ferramentas oficiais da Build 42; quando sair, conferir.
