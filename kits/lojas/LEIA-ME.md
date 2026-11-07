# Kit de lojas (plantas próprias por tipo de loja)

Temporário, feito para o Kit Brasil (Etapa 5) poder redecorar sem mexer em código.

| Arquivo | O que é | Como o Kit Brasil troca |
|---|---|---|
| `plantas/<nome>.json` | Desenho da loja: retângulos de cômodos (`x, y, w, h, kind`). O tipo do cômodo (`pharmacy`, `gunstore`, `storage`…) decide o loot, o piso e os móveis. | Mudar tamanhos e cômodos, ou trocar o desenho por um `.tbx` feito no BuildingEd (colocar em `presets/buildings` do KnoxMap). |
| `decoracao.json` | Móveis por tipo de cômodo, em **papéis** (`shop_case`, `gun_locker`…), não em tiles. | Registrar papéis novos (com seus tiles) no catálogo e trocar os nomes aqui. |
| `lojas.json` | Etiqueta `shop=` do OSM → planta. | Acrescentar uma linha por tipo de loja nova. |

Como funciona: `scripts/knoxmap_pipeline.py` com `"kitLojas": "kits/lojas"` no config grava as plantas como presets do KnoxMap, cria uma zona em volta de cada loja desenhada com etiqueta conhecida e a zona diz qual planta usar. O código está em `scripts/gerador/kit_lojas.py`.

Regras e limites:
- A planta é usada **como desenhada**, sem esticar nem girar: tem de caber no terreno da loja (hoje 8–10 × 12 tiles). Se não couber, o KnoxMap gera a loja sozinho.
- A planta é desenhada com a frente ao sul (`"frente": "S"`); o script grava também a versão virada (rua ao norte) e escolhe pela rua mais próxima. Móveis em `"moveis"` (posição fixa), itens de parede em `"parede"` por versão; nada fica a menos de 2 quadrados de uma porta.
- O loot é pelo nome do cômodo e não muda com o desenho.
- Lojas ainda sem planta própria (padaria, ferragens, roupas) saem com o gerador do KnoxMap.
- Plantas feitas: farmácia (`chemist`/`pharmacy`) e loja de armas (`weapons`). Não usar `shop=pharmacy` sem planta: vira prédio médico (K17).

## Cópias do mapa original (preferidas)

`scripts/gerador/copiar_predio_vanilla.py` copia um prédio inteiro do Knox County (piso, paredes, portas, vitrine, móveis, letreiro, telhado e os cômodos com os nomes do jogo, que decidem o loot) para `vanilla/<nome>.tbx`. No `lojas.json`, a chave `"vanilla"` diz o arquivo e a `"frente"` (lado da porta). A cópia só é usada onde a rua fica desse lado; senão entra a nossa planta.

    <python do KnoxMap> -I scripts/gerador/copiar_predio_vanilla.py <KnoxMap> listar pharmacy gunstore
    <python do KnoxMap> -I scripts/gerador/copiar_predio_vanilla.py <KnoxMap> copiar 46_26 32 "Nome" kits/lojas/vanilla/x.tbx

Copiadas: farmácia "Pharmahug" (14 × 19, frente a oeste) e loja de armas (13 × 13, frente a oeste). Limites: a cópia não gira (precisa de uma loja original com a frente para cada lado, ou de uma tabela de tiles girados) e o terreno precisa ser maior que o prédio. O `.tbx` abre no BuildingEd, então o Kit Brasil pode redecorar a cópia.
