import math

import pygame

from interface.camera import Camera
from interface.componentes import (
    Botao, ControleDeslizante, cartao, iconeAvancar, iconeGirar, iconeMais, iconeMenos, iconePausar, iconeTocar,
    texto, textoEmPartes, textoEspacado,
)
from interface.desenho_peca import desenharMeeple, desenharPeca, pontoDoSegmento
from interface.escala import Escala
from interface.estilo import (
    BARRA_FUNDO, CASA_LEGAL, CASA_LEGAL_SOBRE, CORES_JOGADOR, CREME, CREME_BORDA, DESTAQUE, GRADE,
    LARGURA_BASE, ALTURA_BASE, MADEIRA, MADEIRA_BORDA, NOMES_JOGADOR, TABULEIRO, TEXTO, TEXTO_SUAVE, TRACEJADO,
    VEU,
)

RET_TABULEIRO = pygame.Rect(36, 36, 1276, 1036)
AREA_TABULEIRO = RET_TABULEIRO.inflate(-8, -8)
RET_CARTAO_PECA = pygame.Rect(1344, 36, 552, 348)
RET_CARTAO_PLACAR = pygame.Rect(1344, 412, 552, 376)
RET_CARTAO_IA = pygame.Rect(1344, 816, 552, 160)
RET_ABANDONAR = pygame.Rect(1344, 1004, 552, 66)
RET_STATUS = pygame.Rect(36, 1084, 1848, 80)
RET_PREVIA = pygame.Rect(1374, 102, 176, 176)
RET_RESULTADO = pygame.Rect(0, 0, 720, 470)
RET_RESULTADO.center = AREA_TABULEIRO.center

TAMANHO_PREVIA = 176
TAMANHO_TRACO = 10
ESPACO_TRACO = 7
RAIO_ALVO = 0.13
TAMANHO_MEEPLE = 0.3
ALFA_MEEPLE_FANTASMA = 110
MAIOR_ALTURA_OPCAO = 52
ALTURA_AREA_OPCOES = 176
NOME_DO_TERRITORIO = {"Cidade": "Cidade", "Estrada": "Estrada", "Monasterio": "Monastério"}
NOME_DO_LADO = {"NORTE": "norte", "LESTE": "leste", "SUL": "sul", "OESTE": "oeste"}
ATRASO_IA_MS = 700
INTERVALO_IA_MAIS_LENTO_MS = 1600
INTERVALO_IA_MAIS_RAPIDO_MS = 25
VELOCIDADE_INICIAL = 0.55
ESCALA_MINIMA_PLACAR = 50
PASSO_TECLADO = 40
GRAUS_POR_GIRO = 90
VOLTA = 360

TECLAS_DESLOCAMENTO = {
    pygame.K_LEFT: (1, 0), pygame.K_a: (1, 0),
    pygame.K_RIGHT: (-1, 0), pygame.K_d: (-1, 0),
    pygame.K_UP: (0, 1), pygame.K_w: (0, 1),
    pygame.K_DOWN: (0, -1), pygame.K_s: (0, -1),
}


class TelaPartida:
    def __init__(self, jogo, descricoes, iaContraIa):
        self.jogo = jogo
        self._descricoes = dict(zip(jogo.jogadores, descricoes))
        self._iaContraIa = iaContraIa
        self._camera = Camera(AREA_TABULEIRO.center)
        self._rotacaoPrevia = 0
        self._casaSelecionada = None
        self._segmentoSelecionado = None
        self._arrastando = False
        self._pausado = False
        self._proximoTurnoIa = 0
        self._ultimaCasa = None
        self._resultado = None
        self.voltarAoMenu = False
        self._botaoGirar = Botao((1582, 110, 284, 78), "Rotacionar", icone=self._iconeGirar)
        self._botaoConfirmar = Botao((1374, 294, 492, 74), "Confirmar posição", escuro=True)
        self._botaoTocar = Botao((1374, 892, 64, 56), icone=iconeTocar)
        self._botaoPausar = Botao((1450, 892, 64, 56), icone=iconePausar)
        self._botaoAvancar = Botao((1526, 892, 64, 56), icone=iconeAvancar)
        self._velocidade = ControleDeslizante(1622, 1866, 920, VELOCIDADE_INICIAL)
        self._botaoAbandonar = Botao(RET_ABANDONAR, "Abandonar partida")
        self._botaoMenos = Botao((1232, 916, 56, 56), icone=iconeMenos)
        self._botaoMais = Botao((1232, 992, 56, 56), icone=iconeMais)
        self._botaoVoltar = Botao((0, 0, 360, 70), "Voltar ao menu", escuro=True)
        self._botaoVoltar.retangulo.midbottom = (RET_RESULTADO.centerx, RET_RESULTADO.bottom - 36)
        for botao in (self._botaoTocar, self._botaoPausar, self._botaoAvancar):
            botao.ativo = iaContraIa
        self._velocidade.ativo = iaContraIa
        self._agendarIa(pygame.time.get_ticks())

    def tratarEvento(self, evento):
        self._velocidade.tratarEvento(evento)
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button in (2, 3):
            self._arrastando = True
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button in (2, 3):
            self._arrastando = False
        elif evento.type == pygame.MOUSEMOTION and self._arrastando:
            self._camera.deslocar(*evento.rel)
        elif evento.type == pygame.MOUSEWHEEL and AREA_TABULEIRO.collidepoint(Escala.mouse()):
            self._camera.ampliar(evento.y, Escala.mouse())
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            self._clique(evento.pos)
        elif evento.type == pygame.KEYDOWN:
            self._tecla(evento.key)

    def atualizar(self, agora):
        if self._resultado is not None:
            return
        if self.jogo.terminou():
            self._encerrar()
            return
        if self.jogo.jogadorAtual.ehHumano():
            self._prepararTurnoHumano()
            return
        if self._iaContraIa and self._pausado:
            return
        if agora >= self._proximoTurnoIa:
            self._executarTurnoIa()

    def desenhar(self, superficie):
        mouse = Escala.mouse()
        superficie.fill(MADEIRA)
        pygame.draw.rect(superficie, MADEIRA_BORDA, superficie.get_rect(), 8)
        self._desenharTabuleiro(superficie, mouse)
        self._desenharCartaoPeca(superficie, mouse)
        self._desenharCartaoPlacar(superficie)
        self._desenharCartaoIa(superficie, mouse)
        self._botaoAbandonar.ativo = self._resultado is None
        self._botaoAbandonar.desenhar(superficie, mouse)
        self._desenharStatus(superficie)
        if self._resultado is not None:
            self._desenharResultado(superficie, mouse)

    def _prepararTurnoHumano(self):
        if self.jogo.pecaDaVez is None:
            if self.jogo.comprarPeca() is not None:
                self._rotacaoPrevia = 0
                self._casaSelecionada = None
                self._segmentoSelecionado = None

    def _executarTurnoIa(self):
        casasAntes = set(self.jogo.mapa.matriz)
        self.jogo.executarTurno()
        novas = set(self.jogo.mapa.matriz) - casasAntes
        self._ultimaCasa = next(iter(novas), self._ultimaCasa)
        self._agendarIa(pygame.time.get_ticks())

    def _finalizarTurnoHumano(self, segmento):
        self.jogo.colocarMeeple(segmento)
        self._segmentoSelecionado = None
        self._agendarIa(pygame.time.get_ticks())

    def _agendarIa(self, agora):
        if self._iaContraIa:
            proporcao = INTERVALO_IA_MAIS_RAPIDO_MS / INTERVALO_IA_MAIS_LENTO_MS
            intervalo = INTERVALO_IA_MAIS_LENTO_MS * proporcao ** self._velocidade.valor
        else:
            intervalo = ATRASO_IA_MS
        self._proximoTurnoIa = agora + intervalo

    def _encerrar(self):
        antes = {jogador: jogador.pontos for jogador in self.jogo.jogadores}
        self.jogo.pontuarFinal()
        self._resultado = [
            (jogador, antes[jogador], jogador.pontos - antes[jogador], jogador.pontos)
            for jogador in self.jogo.jogadores
        ]

    def _humanoColocandoPeca(self):
        return (
            self._resultado is None and self.jogo.jogadorAtual.ehHumano()
            and self.jogo.pecaDaVez is not None and not self.jogo.pecaDaVezColocada()
        )

    def _humanoColocandoMeeple(self):
        return (
            self._resultado is None and self.jogo.jogadorAtual.ehHumano()
            and self.jogo.pecaDaVez is not None and self.jogo.pecaDaVezColocada()
        )

    def _clique(self, ponto):
        if self._resultado is not None:
            if self._botaoVoltar.contem(ponto):
                self.voltarAoMenu = True
            return
        opcaoDeMeeple = self._opcaoDeMeepleEm(ponto)
        if self._botaoAbandonar.contem(ponto):
            self.voltarAoMenu = True
        elif opcaoDeMeeple is not None:
            self._alternarSegmento(opcaoDeMeeple)
        elif self._humanoColocandoPeca() and self._botaoGirar.contem(ponto):
            self._girarPrevia()
        elif self._botaoConfirmar.contem(ponto):
            self._confirmar()
        elif self._botaoTocar.contem(ponto):
            self._pausado = False
        elif self._botaoPausar.contem(ponto):
            self._pausado = True
        elif self._botaoAvancar.contem(ponto):
            self._avancarUmTurno()
        elif self._botaoMenos.contem(ponto):
            self._camera.ampliar(-1, AREA_TABULEIRO.center)
        elif self._botaoMais.contem(ponto):
            self._camera.ampliar(1, AREA_TABULEIRO.center)
        elif AREA_TABULEIRO.collidepoint(ponto):
            self._cliqueNoTabuleiro(ponto)

    def _cliqueNoTabuleiro(self, ponto):
        if self._humanoColocandoPeca():
            casa = self._camera.casaEm(ponto)
            rotacoes = self._rotacoesLegaisEm(casa)
            if rotacoes:
                self._casaSelecionada = casa
                if self._rotacaoPrevia not in rotacoes:
                    self._rotacaoPrevia = self._proximaRotacao(rotacoes, incluirAtual=True)
        elif self._humanoColocandoMeeple():
            segmento = self._segmentoSob(ponto)
            if segmento is not None:
                self._alternarSegmento(segmento)

    def _alternarSegmento(self, segmento):
        self._segmentoSelecionado = None if segmento is self._segmentoSelecionado else segmento

    def _opcaoDeMeepleEm(self, ponto):
        if not self._humanoColocandoMeeple():
            return None
        for botao, segmento in self._botoesDeMeeple():
            if botao.contem(ponto):
                return segmento
        raio = TAMANHO_PREVIA * RAIO_ALVO
        for segmento in self.jogo.segmentosParaMeeple():
            cx, cy = self._pontoNaPrevia(segmento)
            if math.hypot(ponto[0] - cx, ponto[1] - cy) <= raio:
                return segmento
        return None

    def _botoesDeMeeple(self):
        segmentos = self.jogo.segmentosParaMeeple()
        if not segmentos:
            return []
        espaco = 8
        altura = min(MAIOR_ALTURA_OPCAO, (ALTURA_AREA_OPCOES - espaco * (len(segmentos) - 1)) // len(segmentos))
        botoes = []
        for indice, segmento in enumerate(segmentos):
            botao = Botao((1582, 102 + indice * (altura + espaco), 284, altura), _nomeDoSegmento(segmento), tamanhoFonte=22)
            botao.escuro = segmento is self._segmentoSelecionado
            botoes.append((botao, segmento))
        return botoes

    def _pontoNaPrevia(self, segmento):
        u, v = pontoDoSegmento(segmento)
        return int(RET_PREVIA.left + u * TAMANHO_PREVIA), int(RET_PREVIA.top + v * TAMANHO_PREVIA)

    def _confirmar(self):
        if self._humanoColocandoPeca() and self._podeConfirmarPeca():
            self.jogo.jogar(self._jogadaLegal(self._casaSelecionada, self._rotacaoPrevia))
            self._ultimaCasa = self._casaSelecionada
            self._casaSelecionada = None
            self._segmentoSelecionado = None
        elif self._humanoColocandoMeeple():
            self._finalizarTurnoHumano(self._segmentoSelecionado)

    def _tecla(self, tecla):
        if tecla == pygame.K_ESCAPE and self._resultado is not None:
            self.voltarAoMenu = True
        elif tecla == pygame.K_r and self._humanoColocandoPeca():
            self._girarPrevia()
        elif tecla in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._confirmar()
        elif tecla == pygame.K_SPACE and self._humanoColocandoMeeple():
            self._finalizarTurnoHumano(None)
        elif tecla == pygame.K_SPACE and self._iaContraIa:
            self._pausado = not self._pausado
        elif tecla == pygame.K_n and self._iaContraIa:
            self._avancarUmTurno()
        elif tecla in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
            self._camera.ampliar(1, AREA_TABULEIRO.center)
        elif tecla in (pygame.K_MINUS, pygame.K_KP_MINUS):
            self._camera.ampliar(-1, AREA_TABULEIRO.center)
        elif tecla in TECLAS_DESLOCAMENTO:
            dx, dy = TECLAS_DESLOCAMENTO[tecla]
            self._camera.deslocar(dx * PASSO_TECLADO, dy * PASSO_TECLADO)

    def _avancarUmTurno(self):
        self._pausado = True
        if not self.jogo.terminou():
            self._executarTurnoIa()

    def _girarPrevia(self):
        if self._casaSelecionada is None:
            self._rotacaoPrevia = (self._rotacaoPrevia + GRAUS_POR_GIRO) % VOLTA
            return
        rotacoes = self._rotacoesLegaisEm(self._casaSelecionada)
        self._rotacaoPrevia = self._proximaRotacao(rotacoes, incluirAtual=False)

    def _proximaRotacao(self, rotacoes, incluirAtual):
        inicio = 0 if incluirAtual else GRAUS_POR_GIRO
        return min(rotacoes, key=lambda r: (r - self._rotacaoPrevia - inicio) % VOLTA)

    def _podeConfirmarPeca(self):
        return self._casaSelecionada is not None and self._rotacaoPrevia in self._rotacoesLegaisEm(self._casaSelecionada)

    def _rotacoesLegaisEm(self, casa):
        return [j.rotacao for j in self.jogo.legais if (j.posicaoX, j.posicaoY) == casa]

    def _jogadaLegal(self, casa, rotacao):
        return next(j for j in self.jogo.legais if (j.posicaoX, j.posicaoY) == casa and j.rotacao == rotacao)

    def _pontoNaTela(self, segmento, casa):
        u, v = pontoDoSegmento(segmento)
        x, y = self._camera.paraTela(*casa)
        tamanho = self._camera.tamanho
        return int(x + u * tamanho), int(y + v * tamanho)

    def _segmentoSob(self, ponto):
        casa = self.jogo.mapa.posicaoDe(self.jogo.pecaDaVez)
        raio = self._camera.tamanho * RAIO_ALVO
        for segmento in self.jogo.segmentosParaMeeple():
            cx, cy = self._pontoNaTela(segmento, casa)
            if math.hypot(ponto[0] - cx, ponto[1] - cy) <= raio:
                return segmento
        return None

    def _desenharTabuleiro(self, superficie, mouse):
        pygame.draw.rect(superficie, MADEIRA_BORDA, RET_TABULEIRO)
        superficie.fill(TABULEIRO, AREA_TABULEIRO)
        superficie.set_clip(AREA_TABULEIRO)
        self._desenharGrade(superficie)
        tamanho = self._camera.tamanho
        for casa, peca in self.jogo.mapa.matriz.items():
            posicao = self._camera.paraTela(*casa)
            if AREA_TABULEIRO.colliderect((*posicao, tamanho, tamanho)):
                superficie.blit(desenharPeca(peca, peca.rotacao, tamanho), posicao)
        if self._humanoColocandoPeca():
            self._desenharCasasLegais(superficie, mouse)
        if self._ultimaCasa in self.jogo.mapa.matriz and not self._humanoColocandoPeca():
            pygame.draw.rect(superficie, DESTAQUE, (*self._camera.paraTela(*self._ultimaCasa), tamanho, tamanho), 3)
        self._desenharMeeples(superficie)
        if self._humanoColocandoMeeple():
            self._desenharAlvosDeMeeple(superficie, mouse)
        superficie.set_clip(None)
        for botao in (self._botaoMenos, self._botaoMais):
            botao.desenhar(superficie, mouse)

    def _desenharGrade(self, superficie):
        tamanho = self._camera.tamanho
        x = AREA_TABULEIRO.left + (self._camera.origem[0] - AREA_TABULEIRO.left) % tamanho
        while x < AREA_TABULEIRO.right:
            pygame.draw.line(superficie, GRADE, (x, AREA_TABULEIRO.top), (x, AREA_TABULEIRO.bottom))
            x += tamanho
        y = AREA_TABULEIRO.top + (self._camera.origem[1] - AREA_TABULEIRO.top) % tamanho
        while y < AREA_TABULEIRO.bottom:
            pygame.draw.line(superficie, GRADE, (AREA_TABULEIRO.left, y), (AREA_TABULEIRO.right, y))
            y += tamanho

    def _desenharCasasLegais(self, superficie, mouse):
        tamanho = self._camera.tamanho
        casaSobMouse = self._camera.casaEm(mouse)
        camada = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        for casa in {(j.posicaoX, j.posicaoY) for j in self.jogo.legais}:
            if casa == self._casaSelecionada:
                continue
            camada.fill(CASA_LEGAL_SOBRE if casa == casaSobMouse else CASA_LEGAL)
            x, y = self._camera.paraTela(*casa)
            superficie.blit(camada, (x, y))
            _retanguloTracejado(superficie, pygame.Rect(x, y, tamanho, tamanho), TRACEJADO)
        if self._casaSelecionada is not None:
            x, y = self._camera.paraTela(*self._casaSelecionada)
            superficie.blit(desenharPeca(self.jogo.pecaDaVez, self._rotacaoPrevia, tamanho), (x, y))
            pygame.draw.rect(superficie, DESTAQUE, (x, y, tamanho, tamanho), 4)

    def _desenharMeeples(self, superficie):
        tamanhoMeeple = int(self._camera.tamanho * TAMANHO_MEEPLE)
        for casa, peca in self.jogo.mapa.matriz.items():
            for segmento in peca.segmentos:
                if segmento.meeple is not None:
                    imagem = desenharMeeple(CORES_JOGADOR[segmento.meeple.dono.cor], tamanhoMeeple)
                    superficie.blit(imagem, imagem.get_rect(center=self._pontoNaTela(segmento, casa)))

    def _desenharAlvosDeMeeple(self, superficie, mouse):
        casa = self.jogo.mapa.posicaoDe(self.jogo.pecaDaVez)
        sobMouse = self._segmentoSob(mouse)
        tamanho = self._camera.tamanho
        for segmento in self.jogo.segmentosParaMeeple():
            self._desenharAlvo(superficie, self._pontoNaTela(segmento, casa), tamanho, segmento, segmento is sobMouse)

    def _desenharAlvo(self, superficie, centro, tamanhoPeca, segmento, sobMouse):
        cor = CORES_JOGADOR[self.jogo.jogadorAtual.cor]
        tamanhoMeeple = int(tamanhoPeca * TAMANHO_MEEPLE)
        imagem = desenharMeeple(cor, tamanhoMeeple)
        if segmento is self._segmentoSelecionado:
            superficie.blit(imagem, imagem.get_rect(center=centro))
            return
        raio = int(tamanhoPeca * RAIO_ALVO)
        pygame.draw.circle(superficie, DESTAQUE if sobMouse else CREME, centro, raio)
        pygame.draw.circle(superficie, cor, centro, raio, 3)
        fantasma = imagem.copy()
        fantasma.set_alpha(ALFA_MEEPLE_FANTASMA)
        superficie.blit(fantasma, fantasma.get_rect(center=centro))

    def _desenharCartaoPeca(self, superficie, mouse):
        cartao(superficie, RET_CARTAO_PECA)
        colocandoMeeple = self._humanoColocandoMeeple()
        textoEspacado(superficie, "Meeple (opcional)" if colocandoMeeple else "Peça da vez", (1374, 62), 26)
        if self.jogo.jogadorAtual.ehHumano() and self._resultado is None:
            passo = "Passo 2 de 2" if colocandoMeeple else "Passo 1 de 2"
            texto(superficie, passo, (1866, 64), 22, TEXTO_SUAVE, ancora="topright")
        peca, rotacao = self._pecaExibida()
        pygame.draw.rect(superficie, CREME_BORDA, RET_PREVIA)
        if peca is not None:
            superficie.blit(desenharPeca(peca, rotacao, TAMANHO_PREVIA), RET_PREVIA)
        pygame.draw.rect(superficie, MADEIRA_BORDA, RET_PREVIA.inflate(4, 4), 3)
        if colocandoMeeple:
            self._desenharOpcoesDeMeeple(superficie, mouse)
            return
        colocandoPeca = self._humanoColocandoPeca()
        self._botaoGirar.ativo = colocandoPeca
        self._botaoGirar.desenhar(superficie, mouse)
        legenda = f"Rotação: {rotacao}°" if peca is not None else ""
        texto(superficie, legenda, (1582, 202), 24, TEXTO_SUAVE)
        if colocandoPeca:
            texto(superficie, "Depois: meeple (opcional)", (1582, 236), 20, TEXTO_SUAVE)
        self._botaoConfirmar.rotulo = "Confirmar posição"
        self._botaoConfirmar.ativo = colocandoPeca and self._podeConfirmarPeca()
        self._botaoConfirmar.desenhar(superficie, mouse)

    def _desenharOpcoesDeMeeple(self, superficie, mouse):
        segmentos = self.jogo.segmentosParaMeeple()
        for segmento in segmentos:
            centro = self._pontoNaPrevia(segmento)
            sobMouse = math.hypot(mouse[0] - centro[0], mouse[1] - centro[1]) <= TAMANHO_PREVIA * RAIO_ALVO
            self._desenharAlvo(superficie, centro, TAMANHO_PREVIA, segmento, sobMouse)
        if segmentos:
            for botao, _ in self._botoesDeMeeple():
                botao.desenhar(superficie, mouse)
        else:
            motivo = (
                ["Você não tem meeples", "na reserva."] if self.jogo.jogadorAtual.meeplesDisponiveis() == 0
                else ["Nenhum lugar livre", "para meeple nesta peça."]
            )
            for indice, linha in enumerate(motivo):
                texto(superficie, linha, (1582, 130 + indice * 32), 24, TEXTO_SUAVE)
        self._botaoConfirmar.rotulo = "Confirmar meeple" if self._segmentoSelecionado else "Continuar sem meeple"
        self._botaoConfirmar.ativo = True
        self._botaoConfirmar.desenhar(superficie, mouse)

    def _pecaExibida(self):
        if self.jogo.pecaDaVez is not None and self.jogo.jogadorAtual.ehHumano():
            if self.jogo.pecaDaVezColocada():
                return self.jogo.pecaDaVez, self.jogo.pecaDaVez.rotacao
            return self.jogo.pecaDaVez, self._rotacaoPrevia
        ultima = self.jogo.mapa.matriz.get(self._ultimaCasa)
        return (ultima, ultima.rotacao) if ultima is not None else (None, 0)

    def _desenharCartaoPlacar(self, superficie):
        cartao(superficie, RET_CARTAO_PLACAR)
        textoEspacado(superficie, "Placar", (1374, 438), 26)
        maior = max(jogador.pontos for jogador in self.jogo.jogadores)
        escala = max(ESCALA_MINIMA_PLACAR, math.ceil(maior / ESCALA_MINIMA_PLACAR) * ESCALA_MINIMA_PLACAR)
        ordem = sorted(self.jogo.jogadores, key=lambda j: j is not self.jogo.jogadorAtual)
        for indice, jogador in enumerate(ordem):
            y = 490 + indice * 108
            cor = CORES_JOGADOR[jogador.cor]
            superficie.blit(desenharMeeple(cor, 42), (1374, y + 4))
            nome = NOMES_JOGADOR[jogador.cor]
            if not jogador.ehHumano() or self._iaContraIa:
                nome += f" ({self._descricoes[jogador]})"
            texto(superficie, nome, (1434, y), 30, TEXTO)
            reserva = jogador.meeplesDisponiveis()
            texto(superficie, f"{reserva} meeple{'s' if reserva != 1 else ''} na reserva", (1434, y + 44), 22, TEXTO_SUAVE)
            texto(superficie, str(jogador.pontos), (1866, y + 26), 42, TEXTO, ancora="midright")
            barra = pygame.Rect(1374, y + 84, 492, 12)
            pygame.draw.rect(superficie, BARRA_FUNDO, barra, border_radius=6)
            preenchida = barra.copy()
            preenchida.width = int(barra.width * min(1.0, jogador.pontos / escala))
            if preenchida.width:
                pygame.draw.rect(superficie, cor, preenchida, border_radius=6)
        pygame.draw.line(superficie, CREME_BORDA, (1374, 716), (1866, 716), 2)
        texto(superficie, f"Monte: {self.jogo.monte.pecasRestantes()} peças restantes", (1374, 730), 22, TEXTO_SUAVE)

    def _desenharCartaoIa(self, superficie, mouse):
        cartao(superficie, RET_CARTAO_IA)
        textoEspacado(superficie, "Partida IA vs IA", (1374, 842), 26)
        for botao in (self._botaoTocar, self._botaoPausar, self._botaoAvancar):
            botao.desenhar(superficie, mouse)
        self._velocidade.desenhar(superficie)

    def _desenharStatus(self, superficie):
        cartao(superficie, RET_STATUS)
        y = RET_STATUS.centery
        if self._resultado is not None:
            vencedor = self.jogo.vencedor()
            if vencedor is None:
                partes = [("Fim de partida — empate!", TEXTO, False)]
            else:
                partes = [
                    ("Fim de partida — ", TEXTO, False),
                    (NOMES_JOGADOR[vencedor.cor], CORES_JOGADOR[vencedor.cor], True),
                    (f" venceu com {vencedor.pontos} pontos", TEXTO, False),
                ]
        else:
            atual = self.jogo.jogadorAtual
            partes = [
                ("Turno de ", TEXTO, False),
                (NOMES_JOGADOR[atual.cor], CORES_JOGADOR[atual.cor], True),
                (" — " + self._acaoDoTurno(), TEXTO, False),
            ]
        textoEmPartes(superficie, partes, (70, y), 30)

    def _acaoDoTurno(self):
        if self._humanoColocandoPeca():
            if self._casaSelecionada is None:
                return "escolha onde colocar a peça"
            return "gire se quiser e confirme a posição; depois você poderá colocar um meeple"
        if self._humanoColocandoMeeple():
            if self.jogo.jogadorAtual.meeplesDisponiveis() == 0:
                return "você não tem meeples na reserva; clique em Continuar sem meeple"
            if not self.jogo.segmentosParaMeeple():
                return "não há onde colocar meeple nesta peça; clique em Continuar sem meeple"
            if self._segmentoSelecionado is None:
                return "clique num meeple claro na peça (ou numa opção ao lado) para colocá-lo, ou continue sem meeple"
            return "confirme o meeple ou clique nele de novo para desfazer"
        if self._iaContraIa and self._pausado:
            return "partida pausada"
        return "a IA está pensando..."

    def _desenharResultado(self, superficie, mouse):
        veu = pygame.Surface((LARGURA_BASE, ALTURA_BASE), pygame.SRCALPHA)
        veu.fill(VEU)
        superficie.blit(veu, (0, 0))
        cartao(superficie, RET_RESULTADO)
        textoEspacado(superficie, "Fim de partida", (RET_RESULTADO.left + 40, RET_RESULTADO.top + 34), 26)
        vencedor = self.jogo.vencedor()
        titulo = "Empate!" if vencedor is None else f"{NOMES_JOGADOR[vencedor.cor]} venceu!"
        corTitulo = TEXTO if vencedor is None else CORES_JOGADOR[vencedor.cor]
        texto(superficie, titulo, (RET_RESULTADO.centerx, RET_RESULTADO.top + 112), 56, corTitulo, True, "center")
        colunas = (RET_RESULTADO.left + 40, RET_RESULTADO.left + 400, RET_RESULTADO.left + 510, RET_RESULTADO.left + 680)
        for coluna, rotulo, ancora in zip(colunas, ("Jogador", "Partida", "Final", "Total"), ("topleft", "topright", "topright", "topright")):
            texto(superficie, rotulo, (coluna, RET_RESULTADO.top + 172), 22, TEXTO_SUAVE, ancora=ancora)
        for indice, (jogador, durante, final, total) in enumerate(self._resultado):
            y = RET_RESULTADO.top + 214 + indice * 56
            cor = CORES_JOGADOR[jogador.cor]
            superficie.blit(desenharMeeple(cor, 34), (colunas[0], y))
            texto(superficie, f"{NOMES_JOGADOR[jogador.cor]} ({self._descricoes[jogador]})", (colunas[0] + 46, y + 2), 28)
            texto(superficie, str(durante), (colunas[1], y + 2), 28, ancora="topright")
            texto(superficie, f"+{final}", (colunas[2], y + 2), 28, ancora="topright")
            texto(superficie, str(total), (colunas[3], y), 32, cor, True, "topright")
        self._botaoVoltar.desenhar(superficie, mouse)

    @staticmethod
    def _iconeGirar(superficie, retangulo, cor):
        iconeGirar(superficie, retangulo.center, 11, cor)


def _nomeDoSegmento(segmento):
    nome = NOME_DO_TERRITORIO.get(type(segmento.territorio).__name__, "Segmento")
    lados = [NOME_DO_LADO[lado.name] for lado in segmento.ladosOcupados()]
    if not lados or len(lados) == len(NOME_DO_LADO):
        return nome
    if len(lados) == 1:
        return f"{nome} ({lados[0]})"
    return f"{nome} ({', '.join(lados[:-1])} e {lados[-1]})"


def _retanguloTracejado(superficie, retangulo, cor):
    for inicio, fim in (
        (retangulo.topleft, retangulo.topright), (retangulo.topright, retangulo.bottomright),
        (retangulo.bottomright, retangulo.bottomleft), (retangulo.bottomleft, retangulo.topleft),
    ):
        comprimento = math.dist(inicio, fim)
        dx, dy = (fim[0] - inicio[0]) / comprimento, (fim[1] - inicio[1]) / comprimento
        posicao = 0
        while posicao < comprimento:
            final = min(posicao + TAMANHO_TRACO, comprimento)
            pygame.draw.line(
                superficie, cor,
                (inicio[0] + dx * posicao, inicio[1] + dy * posicao),
                (inicio[0] + dx * final, inicio[1] + dy * final), 3,
            )
            posicao += TAMANHO_TRACO + ESPACO_TRACO
