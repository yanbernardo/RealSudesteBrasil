# Kit Brasil: lista de peças (tiles) úteis, por grupo

Lista só dos nomes, para o usuário escolher a ordem dos grupos (08/11/2026). Nenhuma peça deste arquivo foi feita ainda, exceto o que está marcado como **pronto**.

Como cada peça é feita (coluna "Como"):
- **Estilo (D-46, 09/11/2026):** toda peça pronta passa pelo filtro de estilo do jogo (`scripts/gerador/estilo_pz.py`), para combinar com as peças originais.
- **Script**: piso desenhado por script, sem trabalho manual (como o calçadão).
- **Textura**: sai de uma foto/textura livre pelo TileSetZ (guia, seção 6.2): parede, telhado, piso.
- **Desenho**: peça de objeto (poste, banca, orelhão), desenhada à mão ou a partir de modelo 3D; a mais trabalhosa. Toda peça nova precisa também de 3D no Viewpoint (D-07).

## 1. Calçadas e pisos de rua
| Peça | Como |
|---|---|
| Calçadão de Copacabana, pedra portuguesa em ondas (66 peças) | **pronto** (Script) |
| Pedra portuguesa lisa: branca, preta, cinza (2 variações cada) | Script |
| Paralelepípedo (rua antiga, Centro e Santa Teresa) | Script |
| Calçada de placas de concreto 2 × 2 (calçada carioca comum), nova e desgastada | Script |
| Piso tátil de alerta e direcional (amarelo) | Script |
| Ciclovia vermelha (Copacabana, Aterro, Lagoa) e sua faixa branca | Script |
| Meio-fio pintado de amarelo e de branco | Script |
| Rampa de calçada (acessibilidade) | Desenho |
| Bueiro e tampa de concessionária | Desenho |

## 2. Pisos de casa e comércio
| Peça | Como |
|---|---|
| Lajota de barro vermelha (2 tons) | **pronto** (1 tom, botequim) |
| Cerâmica bege e cinza-clara com rejunte | Script |
| Cimento queimado vermelho e cinza | Script |
| Ladrilho hidráulico (azul e branco, vermelho e creme) | **pronto** o vermelho e creme (botequim); falta o azul |
| Azulejo de cozinha e banheiro (parede) | **pronto** (Script, botequim) |
| Piso de granilite (escola, repartição) | **pronto** (Script, botequim) |
| Pedra miracema, ardósia, cerâmica de garagem, cerâmica branca 45, cimentado, bloquete | **pronto** (Script, casa de laje) |
| Taco de madeira (apartamentos antigos) | Textura |

## 3. Paredes e fachadas
| Peça | Como |
|---|---|
| Reboco pintado liso (bege, verde-água, rosa, azul, branco) | Textura |
| Reboco descascado e com mofo | Textura |
| Tijolo baiano aparente (favela, obra) | Textura |
| Bloco de concreto sem reboco | Textura |
| Azulejo português de fachada (Centro, Santa Teresa, Lapa) | Textura |
| Pastilha de fachada de prédio (anos 70) | Textura |
| Pichação e grafite (placas sobrepostas) | Desenho |
| Cartaz lambe-lambe | Desenho |
| Portão de ferro, de garagem, de grade | **pronto** (social de grade e de chapa; garagem de chapa em 3 peças) |
| Muro baixo com grade; muro com cacos de vidro | **pronto** o muro com grade e os muros de 2 m (tijolo, chapiscado, pintados); falta o de cacos de vidro |

## 4. Telhados e topos
| Peça | Como |
|---|---|
| Telha colonial (barro) | Textura |
| Telha de fibrocimento (amianto) | Textura |
| Laje descoberta com caixa d'água | Desenho |
| Caixa d'água de polietileno (azul, cinza) | Desenho |
| Antena parabólica; antena de TV | Desenho |
| Cobertura de zinco (barraco) | Textura |

## 5. Mobiliário urbano
| Peça | Como |
|---|---|
| Orelhão | Desenho |
| Banca de jornal | Desenho |
| Ponto de ônibus coberto | Desenho |
| Poste com fiação enrolada (emaranhado de cabos) | Desenho |
| Lixeira de rua laranja (Comlurb) e contêiner de lixo | Desenho |
| Placa de rua em português (azul e branco), sem texto | Desenho |
| Placa de trânsito brasileira (pare, proibido estacionar etc.) | Desenho |
| Lombada pintada, faixa de pedestre brasileira | Script |
| Semáforo brasileiro | Desenho |
| Banco de praça e de calçadão | Desenho |
| Bebedouro, chuveirão de praia | Desenho |

## 6. Praia
| Peça | Como |
|---|---|
| Guarda-sol de praia (cores) | Desenho |
| Cadeira de praia e barraca | Desenho |
| Quiosque de orla | Desenho |
| Rede de vôlei e de futevôlei (já existe com peças do jogo) | pronto (jogo base) |
| Posto de salva-vidas | Desenho |
| Carrinho de coco e de pipoca | Desenho |

## 7. Casas e comércio brasileiros (usuário no BuildingEd)
**Botequim de esquina, feito em 09/11/2026** (`scripts/gerador/kit_botequim.py` → `kits/tiles/`, registrado no BuildingEd). Nome do bar: **"Bar Ponto Certo"** (fictício; trocar em `NOME_BAR` e rodar de novo):
- Paredes, 4 estilos × 8 peças (`rsb_paredes_botequim_01`): azulejo branco com faixa verde e tinta creme (salão), azulejo verde-claro (cozinha e banheiro), fachada amarela e fachada verde com barra de cerâmica vermelha.
- Pisos (`rsb_pisos_botequim_01`): ladrilho hidráulico, xadrez preto e branco, granilite, lajota vermelha.
- Objetos (`rsb_botequim_01`, 36 peças): balcão de azulejo com tampo de granito e balcão com estufa de salgados (4 lados cada; funcionam como o balcão de bar do jogo), freezer de sorvete (4 lados), cervejeira de porta de vidro (2 lados; é geladeira), cadeira de plástico amarela e branca (4 lados), mesa de plástico amarela e branca, engradados de cerveja, pilha de cadeiras, letreiro do bar (2 peças, fachada para o sul ou para o leste), lousa de cardápio, porta de enrolar aberta (rolo) e fechada (paredes norte e oeste).

| Peça | Como |
|---|---|
| Fachada de casa de laje, de casa com muro e garagem | **pronto** (Script, `kit_casa_laje.py`, 09/11/2026) |
| Sobrado geminado | Desenho |
| Bar de esquina | **pronto** (Script) |
| Padaria, lanchonete, açougue, quitanda | Desenho |
| Placa de loja em português (letreiros sem marca) | Desenho |
| Toldo de comércio | Desenho |

## 8. Morro e favela
**Feito em 08/11/2026 (peças para construir casas; só as peças):** `scripts/gerador/kit_favela.py` → `kits/tiles/`, já registradas no BuildingEd (listas de parede externa e interna, piso, telhado plano, telhado inclinado, escada):
- Paredes, 10 estilos × 8 peças (oeste, norte, quina, pilar, janela e porta nos dois lados): tijolo baiano limpo e sujo, bloco de concreto, reboco cru, reboco desbotado e descascando (rosa, azul, verde-água, amarelo, branco encardido), tábuas de barraco (`rsb_paredes_favela_01`).
- Pisos: contrapiso (2), laje de concreto (2, uma também como telhado plano), cimento queimado vermelho e verde, cerâmica barata vermelha e bege (`rsb_pisos_favela_01`).
- Escada maciça de concreto e de cimento queimado vermelho (`rsb_escadas_favela_01`).
- Portas e janelas: as do jogo.
- **Laje e terraço (09/11/2026, `scripts/gerador/kit_laje.py`):** favela não tem telha inclinada (o telhado de fibrocimento/zinco feito antes foi tirado a pedido do usuário). Lajes de cobertura: crua (2), com manta asfáltica, com remendo de alumínio, com ralo, terraço de cerâmica vermelha e bege (`rsb_lajes_01`, também na lista "Roof Tops" do BuildingEd). Muretas de laje em meia altura, baixa e inacabada em degraus, em tijolo baiano, bloco, reboco cru e reboco branco (`rsb_muretas_favela_01`, puláveis como as do jogo; colocar no modo de peças). Objetos da laje: caixa d'água azul 1000 L e 500 L, caixa velha de amianto, churrasqueira de tijolo (2 lados), pilar com ferro de espera, ferro de espera solto, antena parabólica, varal com roupa (2 lados) (`rsb_objetos_laje_01`).

| Peça | Como |
|---|---|
| Escadaria de concreto no morro (degraus em patamar) | Desenho |
| Bica d'água e valão | Desenho |
| Casas de tijolo e de madeira empilhadas | Desenho |
| Fiação (gato de luz) | Desenho |
| Casa de chefe do morro (D-31, só com peças do jogo, D-16) | Desenho |

## 9. Vegetação e terreno
| Peça | Como |
|---|---|
| Palmeira imperial e coqueiro (se o jogo não tiver) | Desenho |
| Amendoeira, flamboyant, mangueira (árvores de rua) | Desenho |
| Mata atlântica densa com bananeira e samambaia | Desenho |
| Pedra de granito exposta (morros) | Desenho |
| Capim-colonião e brejo | Textura |

## 10. Rodovia e estrada
| Peça | Como |
|---|---|
| Pórtico de pedágio, placa verde de rodovia | Desenho |
| Barreira "New Jersey" de concreto | Desenho |
| Mureta e guard-rail | Desenho |
| Ponto de ônibus rodoviário, posto de beira de estrada | Desenho |

## O que já está pronto para o Kit Brasil
- Empacotador das folhas (`scripts/gerador/kit_tiles.py`) e editor de células (`scripts/gerador/lots.py`).
- Calçadão de Copacabana (D-45).
- Script de pisos (`scripts/gerador/pisos_brasil.py`) com 22 pisos do grupo 1 e 2 (pedra branca, preta, cinza; paralelepípedo; lajota; cerâmica; cimento queimado; tátil; hidráulico; placas; ciclovia), **sem entrar** na folha do mod até o usuário escolher.
