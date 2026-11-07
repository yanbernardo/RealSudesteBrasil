# Guia de prompts do Tripo (modelos 3D do Real Sudeste Brasil)

Criado em 06/11/2026. Complementa a decisão D-29 do plano (Tripo gera o modelo base; o Claude limpa, reduz e registra no Viewpoint).
Os nomes dos botões do Tripo podem mudar com o tempo. Se algo não bater com a tela, vale o que a tela mostra.

---

## 1. Qual caminho usar no Tripo

| Quando | Caminho | Por quê |
|---|---|---|
| Marco famoso com fotos boas (Cristo, Arcos da Lapa, Candelária) | **Foto → 3D** (uma imagem) | Fica mais fiel ao real que descrever por texto |
| Marco importante que será visto de todos os lados | **Multi-vista** (4 imagens: frente, esquerda, costas, direita) | O Tripo 3.1 Multi View aceita as 4 vistas e erra menos na parte de trás. **Só nos planos pagos** (a partir do Professional) |
| Objeto comum (orelhão, quiosque, caixa d'água, banca) | **Texto → 3D** | Rápido, sem precisar de foto |

Regra de ouro: **gerar custa crédito e baixar tem limite no plano grátis** (plano, seção 10). Prepare bem a foto ou o texto antes de gerar, e gire o modelo no visualizador do site antes de baixar.

---

## 2. Como preparar a foto (Foto → 3D)

- Um objeto só, **inteiro** na foto, sem cortar nenhuma parte.
- Fundo simples (céu limpo, parede lisa). Sem pessoas, carros ou cabos na frente.
- Luz suave e pareja, sem sombra forte. Foto de frente ou de 3/4, de altura parecida com a do objeto.
- Boa resolução, sem filtro.
- Para multi-vista: as 4 fotos na mesma distância e luz, com o objeto do mesmo tamanho em todas.
- Licença: fotos suas ou livres (Wikimedia Commons). Crédito ao Tripo na descrição da Workshop (plano, seção 10).

---

## 3. Prompt base (Texto → 3D)

Escreva em **inglês** (costuma funcionar melhor). Troque só o que está entre colchetes.

```
[OBJECT, with its key shapes and proportions], [MATERIALS AND COLORS],
single object, centered, full object visible,
realistic low-poly game asset, clean simple shapes, matte materials,
even neutral lighting, plain white background,
no ground, no shadow, no text, no logos, no people
```

Dicas:
- Descreva **forma, material e cor**, não a história do objeto.
- Diga o que é simétrico ("symmetrical") quando for o caso.
- Evite pedir letras, placas com texto e logos: saem borrados e ainda criam problema de marca.
- Detalhe muito fino (fios, grades finas) some ou vira massa. Peça formas simples.
- Mudou algo? Gere de novo trocando **uma coisa por vez**, para saber o que ajudou.

---

## 4. Ajustes recomendados (na tela do Tripo)

- **Low poly inteligente (Smart Low Poly):** ligado, se o seu plano tiver (no plano grátis não tem).
- **Limite de faces:** comece com cerca de 8.000 para monumentos e 2.000 a 3.000 para objetos pequenos. O Claude simplifica mais no Blender se precisar.
- **Textura:** a padrão basta. O jogo provavelmente só usa a cor, então PBR e qualidade extra não compensam o crédito.
- **Quad mesh:** deixe desligado (só serve para animação).

---

## 5. Exemplos prontos

**Cristo Redentor (foto ou texto)**
```
Christ the Redeemer statue, Art Deco style, light grey-green soapstone,
arms fully outstretched horizontally forming a cross, long robe, calm face looking forward,
symmetrical, standing on a square stone pedestal,
single object, centered, full object visible,
realistic low-poly game asset, matte materials, even neutral lighting, plain white background,
no ground, no shadow, no text, no people
```
Foto ideal: de frente e um pouco de baixo, com céu limpo ao fundo. Se a base aparecer, tudo bem: o Claude corta no Blender. O tamanho dele no jogo sai do teste T5c.

**Arcos da Lapa (foto/multi-vista, ou texto)**
```
white colonial stone aqueduct viaduct, two tiers of round arches,
six large arches on the lower tier and eleven smaller arches on the upper tier,
flat top with a railing, weathered cream-white plaster, dark openings,
single object, centered, full object visible,
realistic low-poly game asset, matte materials, even neutral lighting, plain white background,
no ground, no shadow, no text, no people
```

**Orelhão (texto)**
```
Brazilian public payphone booth called orelhão, large half-egg-shaped fiberglass hood
mounted on a short grey metal post, painted orange-yellow, small dark opening in front,
single object, centered, full object visible,
realistic low-poly game asset, clean simple shapes, matte materials,
even neutral lighting, plain white background, no ground, no shadow, no text, no logos, no people
```

**Quiosque de praia (texto)**
```
small Brazilian beach kiosk, rectangular snack bar with brick walls,
open front with a wooden counter, thatched palm-leaf roof, wooden posts,
single object, centered, full object visible,
realistic low-poly game asset, clean simple shapes, matte materials,
even neutral lighting, plain white background, no ground, no shadow, no text, no logos, no people
```

**Caixa d'água (texto)**
```
round blue plastic water tank with a small grey lid, short cylinder shape,
sitting on a flat concrete slab, single object, centered, full object visible,
realistic low-poly game asset, clean simple shapes, matte materials,
even neutral lighting, plain white background, no ground, no shadow, no text, no logos
```

Outros bons candidatos no mesmo molde: banca de jornal, ponto de ônibus, carrinho de pipoca, banco do calçadão, poste de luz brasileiro, container de lixo, placa de rua (sem texto).

---

## 6. Como pedir ao Claude (em português)

Se não quiser montar o prompt sozinho, mande algo assim:

> Claude, preciso de um modelo no Tripo de **[objeto]**. Tenho **[uma foto / 4 fotos / nenhuma foto]**. Me dê o prompt em inglês, a configuração recomendada e como devo escolher as fotos.

Depois de gerar e baixar (de preferência em **GLB**; OBJ ou FBX também servem), mande:
1. O arquivo.
2. O nome do objeto.
3. A **altura real em metros** (ex.: orelhão ≈ 2 m). O Claude ajusta a escala.

O Claude confere o modelo nas 4 direções (frente, direita, costas, esquerda), simplifica no Blender, ajusta a escala e registra no Viewpoint. Primeiro mostra o resultado; só refaz se você pedir.

---

## 7. Cuidados

- **Itens do D-32 (tiles e modelos decorativos de drogas):** ainda é só proposta. Não gerar nada disso antes da sua aprovação. Antes, conferir as regras de conteúdo da Workshop e as do Tripo, porque no plano grátis os modelos ficam públicos na galeria do Tripo.
- **Sem marcas e sem texto** nos modelos (logos, placas, nomes de empresas).
- **Sem veículos** (D-20: o mapa não traz veículos novos).
- Todo objeto precisa aparecer bem em 3D no Viewpoint e sem mudar nada no isométrico (D-07).
- Cada modelo novo entra no Registro do plano (nome, fonte da foto ou do prompt, data).

---

## 8. Fontes consultadas (06/11/2026)

- Guia da família Tripo (Scenario): https://help.scenario.com/articles/4692888910-tripo-family-the-complete-guide
- Tripo 3.1 e Multi View (Scenario): https://www.scenario.com/blog/tripo-image-to-3d-model-ai-2026
- Tripo P1 (ComfyUI): https://docs.comfy.org/tutorials/partner-nodes/tripo/tripo-p1
