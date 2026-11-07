# Problemas conhecidos e soluções

Lista de erros que já aconteceram no projeto e como evitá-los. **Leia antes de qualquer tarefa** e **acrescente uma entrada sempre que um erro novo for resolvido** (mesmo que pequeno). Cada entrada: o que aconteceu, a causa e o que fazer.

Status: **Resolvido** (já está evitado no fluxo), **Contornado** (há um jeito de evitar, mas o problema existe) ou **Aberto** (ainda sem solução).

---

## Ambiente (Windows, notebook)

| # | Problema | Causa | Como evitar / resolver | Status |
|---|---|---|---|---|
| A1 | `python`, `git` ou `gh` "não encontrado" num terminal novo | O PATH do terminal não foi recarregado depois da instalação | Recarregar o PATH: `$env:Path=[Environment]::GetEnvironmentVariable('Path','Machine')+';'+[Environment]::GetEnvironmentVariable('Path','User')`. O `gh` fica em `C:\Program Files\GitHub CLI\gh.exe`. | Contornado |
| A2 | `python` abre a Microsoft Store | Atalho falso do Windows | Usar o Python 3.12 instalado: `C:\Users\yanbe\AppData\Local\Programs\Python\Python312\python.exe`. | Contornado |
| A3 | O jogo Roblox do usuário foi fechado sem querer | Encerrar processos por nome com padrão amplo | **Nunca** encerrar processos por padrão amplo; só pelo número (PID) exato, depois de conferir. | Resolvido |
| A4 | WebFetch não abre páginas do github.com | Bloqueio do ambiente | Usar `gh` (ex.: `gh api`, `gh release download`) ou `git clone`. | Contornado |
| A5 | Downloads grandes travam ou gastam os dados móveis | Usuário em internet móvel lenta e limitada | Antes de baixar: ver o tamanho (`curl -sIL <url>`, `gh api .../releases`), mostrar ao usuário e esperar autorização. | Resolvido |
| A6 | Texto corrompido em arquivos: "erramentas" no lugar de "ferramentas", tabulação no lugar de `\t` em "scripts\testes" | Caminhos do Windows escritos dentro de código Python/shell: `\f` e `\t` viram caracteres especiais | Em código, escrever caminhos com `/` (o Windows aceita) ou como texto cru (`r"..."`). Depois de editar documento por script, conferir a linha alterada. | Resolvido |
| A7 | Python dá `UnicodeDecodeError` (cp1252) ao ler JSON ou Markdown | O Windows abre arquivos no código de página antigo | Rodar o Python com `-X utf8` (ou `PYTHONUTF8=1`), ou abrir com `encoding="utf-8"`. | Resolvido |
| A8 | Comando longo "estourou o tempo" (600 s) | Download ou geração lenta | Rodar comandos longos em segundo plano (`run_in_background`). | Contornado |

## KnoxMap

| # | Problema | Causa | Como evitar / resolver | Status |
|---|---|---|---|---|
| K1 | O clone do GitHub (`CalvyPZ/knoxmap`) não tem compilador pronto | Essa versão exige compilar o `knox-compile` em Rust (vários GB de ferramentas) | Usar o pacote oficial **v1.8.5.2** (`spytheeuclidean-a11y/knoxmap`, 3 MB, traz `knoxlots.exe` e `knoxroute.exe`), instalado em `ferramentas\knoxmap-1.8.5.2\`. | Resolvido |
| K2 | O KnoxMap ia baixar 863 MB (extrato do Sudeste inteiro) para um bairro | No modo `auto` ele usa o menor extrato da Geofabrik que cobre a área; para o Rio é o Sudeste inteiro | No notebook: `"osm_source": "overpass"` no `knoxmap_config.json` (baixa só a área). No PC potente com internet boa, o extrato pode valer a pena (baixa uma vez para o RJ inteiro). | Resolvido |
| K3 | Setup recusa rodar: "Visual C++ 14.51 ou mais novo" | O KnoxMap 1.8.5.2 exige a versão nova do Visual C++; o notebook tinha 14.42 | Instalar o `vc_redist.x64.exe` oficial da Microsoft (conferir a assinatura digital antes). Já feito no notebook (14.51); **repetir no PC potente se precisar**. | Resolvido no notebook |
| K4 | Compilação falha com `unsupported operand type(s) for /: 'NoneType' and 'str'` | O Setup ainda não tinha terminado (faltava o caminho das ferramentas no config) | Só gerar/compilar depois de o Setup dizer "Setup complete". | Resolvido |
| K5 | O mapa gerado era quase todo mar | Retângulo de coordenadas escolhido "de cabeça", no lugar errado | Antes de gerar: contar os prédios do OSM na área (consulta pequena na Overpass) para achar onde fica o bairro de verdade. Depois de gerar: **sempre olhar o `*_preview.png`** antes de compilar e instalar. | Resolvido |
| K6 | O mapa fica girado (o norte não fica para cima) | *Straighten streets* gira o mapa para alinhar as ruas ao grid do jogo (Urca: 32°) | É de propósito: evita ruas "em degraus". Se precisar do norte para cima, desligar essa opção (as ruas diagonais ficam em degraus). Decidir junto com o T9/D-21. | Aberto (decisão) |
| K7 | O KnoxMap não cria ruas nem casas dentro de um contorno (T7) | Ele só preenche buracos entre prédios que já existem | O gerador das cidades genéricas será nosso; o KnoxMap entra como montador (ruas e prédios em GeoJSON, formato `sketch`). | Aberto (T7c) |
| K8 | A 15 m/tile, prédios reais somem | Uma casa de 10 m vira menos de 1 tile | Nas cidades a 1:15, os prédios vêm do nosso gerador em escala de jogo (D-03), não do OSM. | Aberto (T7c) |
| K9 | Baixar um bairro pela Overpass leva ~10 min | Internet móvel e servidores públicos lentos | Paciência, ou usar o extrato no PC potente. O KnoxMap guarda o que baixou: gerar a mesma área de novo não baixa outra vez. | Contornado |

## Jogo / mod

| # | Problema | Causa | Como evitar / resolver | Status |
|---|---|---|---|---|
| J1 | Mapa novo não aparece num save antigo | O jogo só carrega mapa novo em áreas nunca visitadas (D-34) | Sempre testar com **jogo novo**. | Contornado |
