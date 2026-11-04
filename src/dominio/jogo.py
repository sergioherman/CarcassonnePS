import random

from dominio.catalogo import criarPecaInicial
from dominio.estrategia import EstrategiaAleatoria, EstrategiaGulosa
from dominio.jogador import JogadorHumano, JogadorIA
from dominio.mapa import Mapa
from dominio.monte import Monte

CORES = ("vermelho", "azul")
ESTRATEGIAS = {"Gulosa": EstrategiaGulosa, "Aleatória": EstrategiaAleatoria}


class Jogo:
    @classmethod
    def nomesDeEstrategias(cls):
        return list(ESTRATEGIAS)

    @classmethod
    def comEstrategias(cls, nomes, rng=None):
        return cls([None if nome is None else ESTRATEGIAS[nome]() for nome in nomes], rng)

    def __init__(self, estrategias, rng=None, pecaInicial=None, pecas=None):
        if len(estrategias) != len(CORES):
            raise ValueError("A partida tem exatamente 2 jogadores")
        self._estrategias = estrategias
        self._rng = rng or random.Random()
        self._pecaInicial = pecaInicial
        self._pecas = pecas
        self.jogadores = []
        self.jogadorAtual = None
        self.mapa = None
        self.monte = None
        self.pecaDaVez = None
        self.legais = []

    def iniciar(self):
        self.mapa = Mapa(self._pecaInicial if self._pecaInicial is not None else criarPecaInicial())
        self.monte = Monte(self._pecas, self._rng)
        self.jogadores = [self._criarJogador(cor, estrategia) for cor, estrategia in zip(CORES, self._estrategias)]
        self.jogadorAtual = self._rng.choice(self.jogadores)
        self.pecaDaVez = None
        self.legais = []

    def comprarPeca(self):
        if self.pecaDaVez is not None:
            raise ValueError("A peça da vez ainda não foi jogada")
        while not self.monte.vazio():
            peca = self.monte.comprar()
            legais = self.mapa.jogadasLegais(peca)
            if legais:
                self.pecaDaVez, self.legais = peca, legais
                return peca
        return None

    def jogar(self, jogada):
        if self.pecaDaVez is None or self.pecaDaVezColocada():
            raise ValueError("Não há peça aguardando jogada")
        if jogada not in self.legais:
            raise ValueError("RF-09: jogada fora das jogadas legais")
        self.mapa.colocarPeca(self.pecaDaVez, jogada)

    def segmentosParaMeeple(self):
        if self.pecaDaVez is None:
            return []
        return self.jogadorAtual.segmentosParaMeeple(self.pecaDaVez)

    def colocarMeeple(self, segmento):
        if self.pecaDaVez is None or not self.pecaDaVezColocada():
            raise ValueError("A peça da vez ainda não foi colocada")
        if segmento is not None:
            self._validarMeeple(segmento)
            self.jogadorAtual.meepleLivre().segmento = segmento
        for territorio in self.mapa.territoriosAfetados(self.pecaDaVez):
            if territorio.estaCompleta():
                territorio.calcularPontuacao()
        self.pecaDaVez = None
        self.legais = []
        self._trocarJogador()

    def executarTurno(self):
        if self.jogadorAtual.ehHumano():
            raise ValueError("O turno do jogador humano é conduzido pela interface")
        peca = self.comprarPeca()
        if peca is None:
            return
        self.jogar(self.jogadorAtual.escolherJogada(peca, self.legais))
        self.colocarMeeple(self.jogadorAtual.escolherSegmentoMeeple(peca))

    def pecaDaVezColocada(self):
        return any(colocada is self.pecaDaVez for colocada in self.mapa.matriz.values())

    def terminou(self):
        return self.monte.vazio() and self.pecaDaVez is None

    def pontuarFinal(self):
        for territorio in self.mapa.territorios():
            if territorio.meeples():
                territorio.calcularPontuacaoFinal()

    def vencedor(self):
        maior = max(jogador.pontos for jogador in self.jogadores)
        lideres = [jogador for jogador in self.jogadores if jogador.pontos == maior]
        return lideres[0] if len(lideres) == 1 else None

    def _criarJogador(self, cor, estrategia):
        if estrategia is None:
            return JogadorHumano(cor)
        return JogadorIA(cor, estrategia, self.mapa)

    def _validarMeeple(self, segmento):
        if segmento not in self.pecaDaVez.segmentos:
            raise ValueError("RN-04: meeple só na peça recém-colocada")
        if not segmento.territorio.aceitaMeeple():
            raise ValueError("RN-05: campo não aceita meeple")
        if self.jogadorAtual.meeplesDisponiveis() == 0:
            raise ValueError("RF-13: jogador sem meeples na reserva")
        if segmento.territorio.meeples():
            raise ValueError("RN-06: território já ocupado")

    def _trocarJogador(self):
        indice = self.jogadores.index(self.jogadorAtual)
        self.jogadorAtual = self.jogadores[(indice + 1) % len(self.jogadores)]
