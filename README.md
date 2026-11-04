# Carcassonne

Versão digital do jogo de tabuleiro Carcassonne (jogo base), para **2 jogadores numa mesma máquina**,
feita em Python e pygame. Trabalho final da disciplina **Projeto de Software** (UFF).

É possível jogar em três modos:

- **Humano × Humano:** duas pessoas se revezam no mesmo computador;
- **Humano × IA:** uma pessoa contra o computador;
- **IA × IA:** o computador joga contra si mesmo, e dá para pausar, avançar turno a turno e ajustar a velocidade.

## Como jogar

O jogo usa as 72 peças do jogo base: a peça inicial já começa no tabuleiro e as outras 71 formam o monte,
embaralhado. Quem começa é sorteado. Cada jogador tem 7 meeples.

Cada turno tem dois passos.

1. **Colocar a peça.** O jogo compra uma peça e destaca as casas onde ela cabe. Clique numa casa, gire a peça
   se precisar (**Rotacionar** ou tecla `R`) e clique em **Confirmar posição**. A peça só encaixa ao lado de
   outra (nunca na diagonal) e com os lados combinando: cidade com cidade, estrada com estrada, campo com campo.
   Se a peça não couber em lugar nenhum, ela é descartada e o jogo compra outra.
2. **Colocar um meeple (opcional).** Escolha um lugar na peça que você acabou de colocar. Pode clicar no meeple
   claro sobre a peça, na prévia ao lado ou no botão com o nome do lugar. Depois clique em
   **Confirmar meeple**, ou em **Continuar sem meeple**. O meeple só pode ir para uma cidade, estrada ou
   monastério que ainda não tenha nenhum meeple, contando a extensão inteira dela.

Ao final do turno, toda cidade, estrada ou monastério que foi completado é pontuado na hora, e os meeples
dele voltam para os donos.

| Estrutura | Completa quando | Pontos na hora | Pontos no fim (incompleta) |
| --- | --- | --- | --- |
| Cidade | não tem mais borda aberta | 2 por peça + 2 por escudo | 1 por peça + 1 por escudo |
| Estrada | as duas pontas terminam (cruzamento, cidade, monastério) ou fecha um circuito | 1 por peça | 1 por peça |
| Monastério | as 8 casas ao redor estão ocupadas | 9 | 1 + 1 por peça vizinha |

Quem tiver mais meeples numa estrutura leva os pontos. Em caso de empate, todos os empatados levam os
pontos inteiros. A partida termina quando o monte acaba. Aí as estruturas incompletas que têm meeple são
pontuadas e vence quem tiver mais pontos; pontos iguais dão empate.

**Fora desta versão:** fazendeiros (pontuação de campos), expansões e partidas com mais de 2 jogadores.

### Controles

| Ação | Mouse | Teclado |
| --- | --- | --- |
| Escolher casa / lugar do meeple | clique | |
| Girar a peça | botão **Rotacionar** | `R` |
| Confirmar | botão **Confirmar** | `Enter` |
| Continuar sem meeple | botão **Continuar sem meeple** | `Espaço` |
| Mover o tabuleiro | arrastar com o botão direito | setas ou `W` `A` `S` `D` |
| Zoom | roda do mouse ou botões **−** / **+** | `+` / `-` |
| IA × IA: pausar e continuar / avançar um turno | botões do cartão "Partida IA vs IA" | `Espaço` / `N` |

## Inteligência artificial

As jogadas do computador são escolhidas por uma de duas estratégias, selecionadas no menu inicial:

- **Gulosa:** testa cada jogada possível numa cópia do tabuleiro e escolhe a que completa mais pontos naquele
  turno. Coloca meeples em estruturas que acabou de completar ou nas de maior valor, guardando sempre alguns
  na reserva. Cada decisão leva no máximo ~0,2 s;
- **Aleatória:** escolhe uma jogada e um lugar para o meeple ao acaso.

## Executando

### Sem instalar nada (Windows)

Baixe o `Carcassonne.exe` e abra. Ele não precisa de Python nem do código do projeto. Como o arquivo não é
assinado, na primeira vez o Windows pode mostrar "O Windows protegeu o computador". Para abrir, clique em
**Mais informações** e depois em **Executar assim mesmo**.

### A partir do código

Requer **Python 3.11**.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/main.py
```

Rode os comandos a partir da raiz do repositório. Em macOS ou Linux, ative o ambiente com
`source .venv/bin/activate`.

### Gerando o executável

```powershell
.\gerar_executavel.ps1
```

O script instala o PyInstaller (`requirements-dev.txt`) e gera `dist\Carcassonne.exe`. O PyInstaller só gera
executável para o sistema em que roda; para macOS ou Linux, rode o mesmo comando do PyInstaller numa máquina
com esse sistema.

## Estrutura do repositório

```
src/
  main.py            ponto de entrada
  dominio/           regras do jogo (Jogo, Mapa, Monte, Peça, Territorio, estratégias, catálogo)
  interface/         telas em pygame, desenho das peças e meeples, componentes visuais
assets/              imagens de referência das peças (o jogo desenha as peças por código)
gerar_executavel.ps1 geração do executável com PyInstaller
requirements.txt     dependências para jogar (pygame)
requirements-dev.txt dependências para gerar o executável (PyInstaller)
```

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).
