from abc import ABC, abstractmethod

from dominio.meeple import Meeple

MEEPLES_POR_JOGADOR = 7


class Jogador(ABC):
    def __init__(self, cor):
        self.cor = cor
        self.pontos = 0
        self.meeples = [Meeple(self) for _ in range(MEEPLES_POR_JOGADOR)]

    def meeplesDisponiveis(self):
        return sum(1 for meeple in self.meeples if meeple.segmento is None)

    def meepleLivre(self):
        return next(meeple for meeple in self.meeples if meeple.segmento is None)

    def segmentosParaMeeple(self, peca):
        return peca.segmentosLivres() if self.meeplesDisponiveis() > 0 else []

    def addPontos(self, pontos):
        self.pontos += pontos

    @abstractmethod
    def ehHumano(self):
        pass


class JogadorHumano(Jogador):
    def ehHumano(self):
        return True


class JogadorIA(Jogador):
    def __init__(self, cor, estrategia, mapa):
        super().__init__(cor)
        self.estrategia = estrategia
        self.mapa = mapa

    def ehHumano(self):
        return False

    def escolherJogada(self, peca, legais):
        return self.estrategia.escolherJogada(peca, legais, self.mapa)

    def escolherSegmentoMeeple(self, peca):
        return self.estrategia.escolherSegmentoMeeple(peca, self)
