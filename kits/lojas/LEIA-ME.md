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

Copiadas: farmácia "Pharmahug" (14 × 19, frente a oeste), loja de armas (13 × 13, frente a oeste), mercado de bairro (52_8, 11 × 14, frente ao sul; `shop=convenience`/`greengrocer`), delegacia (9_54, prédio 40, 11 × 13, frente a **leste**; chave `police`) e quartel de Louisville (23_20, prédio 51, 26 × 20, portões ao sul; chave `fire`). Polícia e bombeiros não têm etiqueta `shop`: o gerador marca o lote com `rsb_copia`.

Regras (K35):
- **Conferir a frente no render do Knox County** (`render_lots --world`, com uns 15 tiles de entorno) antes de cadastrar: a porta e a rua do original dizem o lado. Não chutar.
- O KnoxMap encosta a cópia no canto noroeste do lote e não estica nem gira: no gerador (`COPIAS`/`COPIAS_ESP` em `cidade.py`) o lote tem, no lado da rua, o tamanho exato do prédio; senão a cópia fica longe da calçada.
- 3 tiles livres em volta (`VAO_COPIA`), senão o jogo junta a cópia com o vizinho num prédio só.
- No retângulo do prédio a cópia leva tudo menos o chão (as paredes de fora podem ser de qualquer conjunto de peças, ex.: `industry_`).
- A cópia não gira: para ter o mesmo tipo virado para outros lados, copiar outro prédio original virado para lá.
