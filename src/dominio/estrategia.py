import copy
import random
from abc import ABC, abstractmethod

MEEPLES_GUARDADOS_PELA_GULOSA = 2


class EstrategiaIA(ABC):
    @abstractmethod
    def escolherJogada(self, peca, legais, mapa):
        pass

    @abstractmethod
    def escolherSegmentoMeeple(self, peca, jogador):
        pass


class EstrategiaAleatoria(EstrategiaIA):
    def __init__(self, rng=None):
        self._rng = rng or random.Random()

    def escolherJogada(self, peca, legais, mapa):
        return self._rng.choice(legais)

    def escolherSegmentoMeeple(self, peca, jogador):
        return self._rng.choice(jogador.segmentosParaMeeple(peca) + [None])


class EstrategiaGulosa(EstrategiaIA):
    def __init__(self, rng=None):
        self._rng = rng or random.Random()

    def escolherJogada(self, peca, legais, mapa):
        avaliacoes = [(self._pontosCompletados(peca, jogada, mapa), jogada) for jogada in legais]
        melhor = max(pontos for pontos, _ in avaliacoes)
        return self._rng.choice([jogada for pontos, jogada in avaliacoes if pontos == melhor])

    def escolherSegmentoMeeple(self, peca, jogador):
        candidatos = jogador.segmentosParaMeeple(peca)
        completos = [s for s in candidatos if s.territorio.estaCompleta()]
        if completos:
            return max(completos, key=lambda s: s.territorio.pontosPorPeca())
        if not candidatos or jogador.meeplesDisponiveis() <= MEEPLES_GUARDADOS_PELA_GULOSA:
            return None
        return max(candidatos, key=lambda s: s.territorio.pontosPorPecaFinal())

    @staticmethod
    def _pontosCompletados(peca, jogada, mapa):
        memo = {id(meeple.dono): meeple.dono for t in mapa.territorios() for meeple in t.meeples()}
        mapaSimulado, pecaSimulada = copy.deepcopy((mapa, peca), memo)
        mapaSimulado.colocarPeca(pecaSimulada, jogada)
        return sum(
            territorio.pontosPorPeca()
            for territorio in mapaSimulado.territoriosAfetados(pecaSimulada)
            if territorio.estaCompleta()
        )
