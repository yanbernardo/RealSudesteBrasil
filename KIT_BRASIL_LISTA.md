# Kit Brasil: lista de peças (tiles) úteis, por grupo

Lista só dos nomes, para o usuário escolher a ordem dos grupos (08/11/2026). Nenhuma peça deste arquivo foi feita ainda, exceto o que está marcado como **pronto**.

Como cada peça é feita (coluna "Como"):
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
| Lajota de barro vermelha (2 tons) | Script |
| Cerâmica bege e cinza-clara com rejunte | Script |
| Cimento queimado vermelho e cinza | Script |
| Ladrilho hidráulico (azul e branco, vermelho e creme) | Script |
| Azulejo de cozinha e banheiro (parede) | Textura |
| Piso de granilite (escola, repartição) | Script |
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
| Portão de ferro, de garagem, de grade | Desenho |
| Muro baixo com grade; muro com cacos de vidro | Desenho |

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
| Peça | Como |
|---|---|
| Fachada de casa de laje, de casa com muro e garagem | Desenho + Textura |
| Sobrado geminado | Desenho |
| Bar de esquina, padaria, lanchonete, açougue, quitanda | Desenho |
| Placa de loja em português (letreiros sem marca) | Desenho |
| Toldo de comércio | Desenho |

## 8. Morro e favela
**Feito em 08/11/2026 (peças para construir casas; só as peças):** `scripts/gerador/kit_favela.py` → `kits/tiles/`, já registradas no BuildingEd (listas de parede externa e interna, piso, telhado plano, telhado inclinado, escada):
- Paredes, 10 estilos × 8 peças (oeste, norte, quina, pilar, janela e porta nos dois lados): tijolo baiano limpo e sujo, bloco de concreto, reboco cru, reboco desbotado e descascando (rosa, azul, verde-água, amarelo, branco encardido), tábuas de barraco (`rsb_paredes_favela_01`).
- Pisos: contrapiso (2), laje de concreto (2, uma também como telhado plano), cimento queimado vermelho e verde, cerâmica barata vermelha e bege (`rsb_pisos_favela_01`).
- Escada maciça de concreto e de cimento queimado vermelho (`rsb_escadas_favela_01`).
- Portas e janelas: as do jogo.
- **Muros de quintal (09/11/2026, `scripts/gerador/kit_muros.py`, `rsb_muros_favela_01`):** muro de 2 m liso (tijolo baiano, tijolo sujo, bloco, reboco cru, reboco branco, reboco amarelo), com cacos de vidro no topo (tijolo, reboco branco) e mureta com grade de ferro (bloco, reboco branco). No BuildingEd: móveis, grupos "Kit Brasil - Muros de quintal".
- **Laje e terraço (09/11/2026, `scripts/gerador/kit_laje.py`):** favela não tem telha inclinada (o telhado de fibrocimento/zinco feito antes foi tirado a pedido do usuário). Lajes de cobertura (`rsb_lajes_01`, 12, também na lista "Roof Tops" do BuildingEd): laje crua lisa, com poça, rachada com musgo e com entulho; manta asfáltica (2) e com remendo de alumínio; laje com ralo; terraço de cerâmica vermelha e bege (2 cada). Muretas de laje em meia altura, baixa e inacabada em degraus, em tijolo baiano, bloco, reboco cru e reboco branco (`rsb_muretas_favela_01`, puláveis como as do jogo; colocar no modo de peças). Objetos da laje (`rsb_objetos_laje_01`, 11): caixa d'água azul 1000 L e 500 L (frisos, tampa nervurada, canos e registro), caixa velha de amianto, churrasqueira de tijolo (2 lados; bancada, grelha, carvão, fuligem, chapéu na chaminé), pilar com ferro de espera (ferro nervurado e enferrujado, estribos), ferro de espera saindo da laje quebrada, antena parabólica (4 lados), varal com roupas (2 lados) e pilha de tijolos.
- **Refeito com mais detalhe (09/11/2026, pedido do usuário):** texturas com relevo iluminado (`scripts/gerador/texturas_favela.py`): tijolo com ranhuras, quinas lascadas e massa escorrida; bloco com poros; reboco com chapisco, rachaduras finas, tinta desbotada descascando em duas camadas (reboco e tijolo por baixo), mofo, lama e escorrido de chuva; madeira com veio, nós, tinta velha, frestas, sarrafos e pregos com ferrugem; pisos com marca de forma, poros, brita, rachaduras, poça; cerâmica com bisotê, esmalte e lascas; 9 amostras por pixel. Objetos com luz, brilho, oclusão e sombra no chão. Peças com mancha grande (poça, remendo) são para pôr de vez em quando, não em toda a laje.

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

## Onde achar no BuildingEd (09/11/2026)
O Kit Brasil fica separado das peças do jogo:
- **Paredes** (lista de parede externa e interna), **pisos**, **telhado plano / laje** ("Roof Tops") e **escadas**: os estilos do Kit Brasil vêm **primeiro** em cada lista, antes dos do jogo.
- **Objetos e muretas** (lista de móveis, "Furniture"): grupos "Kit Brasil - ..." no topo, por tema (Laje: caixas d'água; Laje: churrasco; Laje: antena e varal; Laje: obra; Muretas de laje: um grupo por acabamento), seguidos do divisor "------ fim do Kit Brasil ------". Objetos com lados (antena, churrasqueira, varal) giram como os móveis do jogo.
- Registro feito por `kit_tiles.buildinged()` (refaz sozinho; cópia original dos arquivos em `.antes_rsb`).

