# Real Sudeste Brasil — instruções para agentes de IA

Mod de mapa para Project Zomboid, inspirado no Real USA, que recria o Sudeste do Brasil. Gratuito, publicado na Steam Workshop.

## Leia antes de qualquer tarefa
- `PLANO_BRASIL_ZOMBOID.md`: plano completo, decisões (D-xx) e etapas. É a fonte da verdade. Se este arquivo e o plano discordarem, siga o plano e avise o usuário.
- Nunca mude uma decisão marcada como DECIDIDO no plano sem perguntar ao usuário.
- Ao mudar uma decisão no plano, atualize também este arquivo.
- Último ponto registrado (07/11/2026): planejamento encerrado; pasta do projeto criada no notebook; próximo passo é a Etapa 0 (no notebook só o leve; o resto no PC potente).

## Ambiente de trabalho (07/11/2026)
- Pasta do projeto (desde 07/11/2026, decisão do usuário): `C:\Users\yanbe\Zomboid\RealSudesteBrasil\`, fora do OneDrive e sem acento no caminho (notebook Acer Nitro V15: 7,7 GB de RAM, RTX 3050 de 6 GB, SSD com 355 GB livres). A cópia da Área de Trabalho (`C:\Users\yanbe\OneDrive\Área de Trabalho\RealSudesteBrasil\`) ficou só como cópia antiga; não edite lá.
- **Este notebook não é o PC potente.** O PC potente (alvo do desenvolvimento) tem Ryzen 7 5700X3D, RTX 5060 Ti 16 GB, 32 GB de RAM e NVMe de 2 TB. Confira em qual máquina você está antes de tarefas pesadas.
- No notebook, adiantar só o leve: ferramentas, dados pequenos, scripts, documentos, modelos 3D pelo Tripo (nuvem) e testes minúsculos (T1/T7 num bairro). No jogo, testar só a visão isométrica por enquanto; o 3D do Viewpoint e o T6 (tamanho e desempenho) esperam o PC potente, a menos que um teste pequeno rode bem.
- Não fazer no notebook: gerar ou compilar o RJ inteiro, rodar mapa grande no jogo, IA 3D local (TRELLIS.2, Hunyuan3D).
- A pasta do projeto já está fora do OneDrive. Dados grandes (`dados`, `saida`) ficam fora do Git (`.gitignore`).
- Internet do notebook (07/11/2026): o usuário está em alto mar, nos dados móveis do celular, conexão lenta e limitada. Não baixe nada grande (KnoxMap, compilador, extrato da Geofabrik) sem ele autorizar. O winget falhou (erro de conexão); Python, Git e GitHub CLI seguem não instalados até haver sinal melhor.
- Versão do jogo: o jogo instalado está na 42.21 (Steam, ramo público). A 42.22 está em pré-lançamento; o usuário disse que pode desenvolver em qualquer uma das duas (07/11/2026).
- Para levar o trabalho ao PC potente, use o repositório Git privado (D-25).

## Como trabalhar com o usuário
- Ele não programa. Explique tudo em português simples, passo a passo, sem jargão.
- Modelo e esforço: confira a tabela do plano (seção 10) no começo de cada tarefa, mas só avise o usuário quando for necessário trocar o modelo ou o esforço. Se o atual serve, trabalhe normalmente. Quando avisar, espere ele trocar ou dizer "continue com o modelo atual" / "continue mesmo assim".
- Trabalhe em etapas, como no plano, para evitar retrabalho e economizar tokens. Não pule etapas sem combinar.
- Se algo não estiver decidido no plano, pergunte antes de decidir.
- Registre toda decisão nova no plano (tabela de decisões e Registro).
- Antes de mudanças grandes, garanta que o trabalho atual está salvo no GitHub (commit), para poder desfazer.

## Decisões fixas
- Versão do jogo (D-12): o mod sempre acompanha a versão mais recente do Project Zomboid. Hoje: Build 42.22. Quando sair versão nova, avise o usuário e verifique a compatibilidade (inclusive a do Viewpoint) antes de seguir.
- Escopo: só o Sudeste (SP, RJ, MG, ES). Outras regiões estão fora do projeto.
- Um mod só para o jogador (D-11), não um mod por estado. Divisão interna só se o teste de tamanho (T6) exigir.
- Lançamento em fases (D-33): o RJ sai primeiro como beta na Workshop; SP, MG e ES entram depois como atualizações do mesmo mod. Atualizações que mudam o mapa pedem save novo (D-34, PROPOSTO): o jogo só carrega mapa novo em áreas nunca visitadas.
- Escala do mapa 1:15, 1 tile = 15 m (D-01, decidido em 06/11/2026); altura dos morros 1:10 (D-27), com 1:15 testado lado a lado na Etapa 2.7; o usuário escolhe vendo em jogo.
- Cidades genéricas: contorno real + malha de ruas em escala de jogo; marcos famosos feitos à parte (D-03).
- Dados atuais, não 1993 (D-08).
- Ordem dos estados: RJ → SP → MG → ES (D-24). Cidade piloto: Rio de Janeiro (D-05). Beta pública: só o RJ (D-33).
- Cidades de rodovia com recursos variáveis (D-35, PROPOSTO): nível de recursos (completa, parcial ou seca) sorteado por regra na geração do mapa, fixo entre saves, com trava de distância máxima sem posto. Não implementar antes de o usuário confirmar.
- Modelos 3D dos marcos gerados a partir de fotos com o Tripo (D-29). Prompts e ajustes: `GUIA_PROMPTS_TRIPO.md`. Itens do D-32 não entram nesse guia até o usuário aprovar.
- Java só se não houver outro jeito (D-06). A exceção é o addon opcional de relevo (D-26).

## Restrições
- É só um MAPA (D-20): sem veículos novos (só os do jogo base); armas no equilíbrio do jogo base (D-19).
- Compatível com o Viewpoint desde o início (D-07): toda tile nova precisa aparecer em 3D no Viewpoint sem bugar, sem mudar nada no isométrico.
- Casas usam só móveis padrão do jogo; nada de modelos de móveis próprios, para não pesar (D-16).
- Ruas com curvas como no jogo base, sem ficarem pixeladas ou em degraus (D-21).

## Jogabilidade
- "Survival friendly": casas saqueáveis e zumbis para combater (D-15).
- Eventos do jogo base espalhados pelo mapa (D-17).
- Casas no estilo brasileiro, com cômodos e mobília realistas (D-16).
- Cenas características de cada cidade, ex.: engarrafamento na Av. Brasil, no RJ (D-18).

## Destaques do Rio de Janeiro
- Cidade do Rio e Baixada Fluminense.
- Região Serrana (Petrópolis, Teresópolis, Lumiar, Sana), integrada de forma coerente com o resto do mapa.
- Marcos obrigatórios: Cristo Redentor, Pão de Açúcar, Igreja da Candelária (e outros pontos famosos, em ondas).

## Casa de "chefe do morro" (D-31)
- Construção especial e rara nas favelas do RJ: visual de ostentação, com riquezas, armas e itens do tráfico, tudo com móveis e itens do jogo base (D-16, D-20).
- Local: sorteada por regra em favelas de porte médio/grande do RJ, sem ligar a casa a nomes de comunidades reais.
- Proposta (D-32, ainda não decidida): tiles e modelos 3D decorativos representando drogas, só nesses ambientes. Não implementar antes de o usuário aprovar.

## Morros e marcos (relevo e vista do alto)
- Relevo real no Viewpoint (D-26/D-27), só visual. A decisão final de usar só sai depois de ver como fica em jogo (Etapa 2.7 do plano).
- Cristo: modelo 3D + tile; primeiro teste em chão plano (T5c). Corcovado: relevo visual com estrada até o topo (D-28).
- Pão de Açúcar (D-30, PROPOSTO, em teste): o usuário quer visitar e ver a vista do alto. Não construir a montanha inteira em andares; fazer só um trajeto (trilha/escadaria com patamares) até um mirante, com a montanha como relevo visual. É o primeiro a ser prototipado na Etapa 2.7. Se falhar (FPS, visual), vale o D-28: rocha esculpida sem escalada.
- Limite de altura da B42: 32 andares. Andares em excesso pesam na memória.
