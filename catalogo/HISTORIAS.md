# Histórias do jogo base: onde e por que aparecem (T8, D-17)

Lido do Java do jogo 42.21 (`projectzomboid.jar`, pacote `zombie.randomizedWorld`) com
`scripts/ler_classe_java.py` (leitor próprio, não executa nada do jogo). Rodar de novo
quando o jogo mudar de versão (D-12):

```
python -X utf8 scripts/ler_classe_java.py "<jogo>/projectzomboid.jar" zombie/randomizedWorld/ saida.txt
```

Quem cria as zonas no nosso mapa: `scripts/gerador/zonas_historias.py` (o KnoxMap só grava
`ParkingStall` e `TownZone`). No pipeline: chave `"zonasHistorias": {}` no config do teste.

## Regras gerais (valem para os três tipos)

- A história é sorteada **quando o pedaço do mapa carrega pela primeira vez**, antes de o
  jogador ver. Área já visitada não ganha história nova (D-34: save novo).
- Cada zona (de estrada ou de história) recebe **no máximo uma** história. Por isso as ruas
  são divididas em trechos (~48 tiles cada).
- Zona com água dentro não serve. Zona com construção do jogador também não.
- Frequência pelo sandbox (jogo novo → Opções avançadas):

| Opção do sandbox (pt-BR) | Nunca | Extr. rara | **Rara (padrão)** | Às vezes | Frequente | Muito freq. | Sempre que possível |
|---|---|---|---|---|---|---|---|
| Chance de Construções Modificadas (casas) | 0 | 5% | **10%** | 15% | 20% | 30% | 100% |
| Chance de Histórias Aleatórias de Zona (por zona) | 0 | 2% | **6%** | 12% | 20% | 40% | 100% |
| Chance de Histórias Aleatórias de Estrada (por pedaço de 8×8 com zona Nav) | 0 | 1,25% | **2,5%** | 4,2% | 7,1% | 25% | 100% |

Casas: além da "construção modificada", toda casa normal válida tem **25%** de ganhar uma
história de sobrevivente morto (ex.: zumbi no banheiro, festa em casa).

## 1. Histórias de casa (não precisam de zona)

**Regra principal:** o prédio precisa ter os cômodos `bedroom` + (`kitchen` ou `livingroom`)
+ `bathroom`. Sem isso, a casa não ganha nem a bagunça normal (louça, roupas). Ficam de fora:
a casa onde o jogador nasce, esconderijos de mapa (stash) e prédios já explorados.

- **Construções modificadas (todas as casas válidas):** queimada (3), queimada com corpos (3),
  queimada com bombeiro (2), saqueada (10), destruída/"Trashed" (5), esconderijo de
  sobrevivente/Safehouse (10; não vale com cômodo `derelict` ou `empty`), outra (1).
- **Sobrevivente morto (25% das casas normais):** zumbi no banheiro (12), no quarto (7),
  alvejante (10, depois de 60 dias), bêbado (10), zumbis comendo (7), pacto (7), polícia na
  casa (4), festa (4, precisa de `livingroom`), pôquer (4, precisa de `kitchen`), noite de
  estudantes (4), noite de futebol (5, `livingroom`), banda na garagem (10, precisa de `garage`,
  `shed` ou `garagestorage`), garagem com recursos (10, garagem e área rural), entre outras.
- **Pelo nome do cômodo (prédios comerciais):** bar (`bar`), café (`cafe`), clínica (`medical`,
  `clinic`), escritório (`office`), escola (`classroom`), salão (`aesthetic`), igreja
  (`church`), loja saqueada (qualquer loja, 2), cerco à loja de armas (`gunstore`, 10, única),
  delegacia barricada (`policestorage`, 5, única), assalto a banco (`bank`, 10, única),
  pizzaria (`pizzawhirled`, `italianrestaurant`), lanchonete (`spiffo_dining`), boate
  (`stripclub`), celeiro (`barn`, `stables`, `farmstorage`).
- Nomes próprios do Knox County (Twiggy, Nolans, juiz, prefeito de West Point...) só
  existem com os cômodos especiais deles; não usamos.

Teste Botafogo (`rsb_t8c_historias`): 44 casas, **39 servem**; 5 não (4 sem quarto e banheiro,
1 sem quarto). Corrigir no gerador (seção 6.1 do plano: toda casa com cozinha, banheiro e quarto).

## 2. Histórias de zona (acampamento, churrasco, piquenique...)

**Regra:** zona do tipo `ZoneStory` no `objects.lua`, com **nome** `Forest`, `Beach` ou
`Lake`, do tamanho mínimo da história. No mapa original: 128 `Forest` (mediana 21 × 20),
12 `Lake`, 6 `Beach`, colocadas à mão em matas, lagos e beiras de rio.

| Nome da zona | Histórias (chance relativa; mín. L × A) |
|---|---|
| `Forest` | acampamento básico (10; 6×6), acampamento devorado (10; 10×6, após 30 dias), fogueira velha (10; 5×5), festa caipira (10; 6×6), caçador (5; 6×6), acampamento (5; 9×9), abrigo velho (5; 4×4), acampamento triste (5; 4×4), bomba d'água (5; 5×5), carro queimado (5; 4×4), armadilheiro (7; 6×6), enterro (7; 6×6, após 20 dias), colchão (3; 4×4), eremita (2), sobrevivencialista (2), piquenique trágico (2), filhote órfão (2), ritual (1), cena de crime (1), lixão (1), carvoeiro (1), guarda florestal (1), animais fugidos (após 30 dias) |
| `Beach` | churrasco (10; 12×12), festa na praia (10; 13×13), pescaria (10; 8×8), jovens roqueiros (5; 6×6), casal (5; 5×5) |
| `Lake` | as mesmas da praia + van acampada (2; 6×6) |

Os nomes `Baseball`, `MusicFest`, `JackieJaye` etc. são cenas únicas do Knox County.
**Para o Brasil:** praias do RJ = `Beach` (Copacabana: churrasco e festa na praia combinam);
lagoas e represas = `Lake`; Mata Atlântica, Tijuca, serra = `Forest`.

## 3. Histórias de estrada (batidas, bloqueios, pneu furado...)

**Regra:** zona do tipo `Nav` (nome vazio) sobre o asfalto, **retangular**, comprida no
sentido da rua: comprimento **> 30** e largura **< 13** (pelo menos 5). O centro do pedaço
de 8×8 precisa ter chão de rua (`blends_street...`), cascalho ou areia, e **nenhum carro** já
estacionado nele. No mapa original: 5.104 zonas `Nav`, largura típica 6, comprimento típico 36.

| História | Mín. (largura × comprimento) | Exige |
|---|---|---|
| Batida simples, ambulância batida | 5 × 7 | — |
| Batida com corpo | 6 × 11 | — |
| Capotado, horda na batida, bloqueio policial (com/sem tiroteio), veículo de serviço | 8 × 8–9 | pista larga (≥ 8) |
| Bandidos na estrada | 7 × 9 | — |
| Carro queimado | 2 × 5 | — |
| Troca de pneu, rua sem saída, "Plonkies", motorista rico | 5 × 5 | — |
| Trailer batido, trailer de gado | 5 × 12 | — |
| Obras na pista | 6 × 6 | asfalto liso (não terra) |
| Veículo de profissão da região | 2 × 5 | região "municipal" |
| Batida com cervo, animal pequeno atropelado | 5 × 11 | **fora da cidade** (sem `TownZone`/`TrailerPark` a 15 tiles) e mata/fazenda perto (zonas `Forest`, `DeepForest`, `Farm`, `FarmLand`) |
| Animal na estrada, rebanho, gado atropelado | 2–5 × 2–12 | fazenda perto (`Farm`, `FarmLand`, `Ranch`) |

**Consequências para o gerador (Etapa 2/3):** rodovias e avenidas com zona `Nav` a cada
~48 tiles; para as histórias rurais, zonas de vegetação `Forest`/`FarmLand` ao lado das
estradas fora das cidades (o KnoxMap também não grava essas).

## 4. Engarrafamento (D-18, Av. Brasil)

Vaga (`ParkingStall`) com **nome** `trafficjamn`/`s`/`e`/`w` (sentido dos carros), uma por
faixa de 3 tiles, ao longo da pista. No mapa original há trechos de até 195 tiles. Liga com a
opção do sandbox "Engarrafamentos" (ligada por padrão).
