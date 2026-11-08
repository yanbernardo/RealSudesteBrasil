# Guia de construções brasileiras (BuildingEd)

Para o usuário fazer à mão as construções do Kit Brasil (Etapa 5, antecipada em parte a pedido dele em 08/11/2026). Cada construção feita aqui entra no gerador do mesmo jeito que as cópias do jogo original entram hoje (`kits/lojas/`, D-38).

## 1. Existe IA que faça isso?

Não conheço nenhuma ferramenta de IA reconhecida que gere prédios de Project Zomboid com qualidade. As que existem fazem o que o KnoxMap já faz: plantas simples, com pouco detalhe (foi o que você viu na farmácia e na loja de armas feitas por regra). Os prédios bons do jogo, os do Knox County e os dos mapas famosos da Workshop, foram feitos à mão no **BuildingEd**.

O caminho para não fazer tudo do zero:

1. **Partir de uma cópia do jogo original.** As cópias que o projeto já tem (`kits/lojas/vanilla/*.tbx`) abrem direto no BuildingEd. Você troca fachada, telhado, piso e móveis e ganha um prédio "abrasileirado" com os cômodos (e o loot) já certos.
2. **Fazer à mão só o que se repete muito no mapa.** Poucas plantas boas, repetidas com variação de cor e telhado pelo gerador, enchem o mapa inteiro. A lista abaixo está em ordem de quanto cada uma aparece.
3. **O resto continua com as cópias do jogo original** (delegacia, quartel, mercado), como você aprovou, até ter tempo para elas.

## 2. Qual fazer primeiro

**A casa de laje térrea com muro e portão** (item 1 da lista). É o prédio que mais se repete no Rio inteiro: subúrbio, Zona Norte, Zona Oeste e Baixada inteira. Uma boa planta dela, com 2 ou 3 variações, muda a cara de metade do mapa. No Rio piloto (Zona Sul) quase não aparece, mas a beta (D-33) é o RJ inteiro.

Se preferir começar pelo que aparece no teste atual: o **botequim de esquina** (item 4), que é pequeno (um cômodo grande, banheiro e depósito), fácil para aprender e que entra na orla no lugar das casas (U31).

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

### 5.5 Regras para o gerador conseguir usar
- **A porta da frente define o lado da rua.** Faça a porta da frente virada para baixo/esquerda da tela (lado sul) ou avise qual lado é; o gerador não gira o prédio (K35).
- **Tamanho fixo:** anote o tamanho; o gerador reserva um lote exatamente desse tamanho.
- **Nada encostado na borda:** deixe a borda livre para a calçada; o muro e o quintal entram depois como "entorno".
- **Um prédio por arquivo**, com 2 ou 3 variações (cores, telhado) em arquivos separados.

### 5.6 Como me entregar
Salve o `.tbx` na pasta `kits\lojas\brasil\` e me diga: o que é, o lado da porta da frente e em que bairros ele deve aparecer. Eu ligo no gerador, instalo e coloco o lugar no grupo TESTE do teleporte para você conferir em jogo.

## 6. Fontes
- Fotos: Wikimedia Commons (links acima; cada foto tem a licença e o autor na página dela).
- BuildingEd/TileZed/WorldEd: edição comunitária "PZTools Unofficial", que vem com o KnoxMap (`vendor\PZMappingTools\README.md`), continuação das ferramentas de Tim Baker ([pzworlded](https://github.com/timbaker/pzworlded), [tiled](https://github.com/timbaker/tiled)); outra edição comunitária: [Unjammer/TileZed](https://github.com/Unjammer/TileZed). A The Indie Stone anunciou que vai lançar as ferramentas oficiais da Build 42; quando sair, conferir.
