from abc import ABC, abstractmethod
from collections import Counter

BORDAS_FECHADAS_POR_LADO = 2
VIZINHOS_DO_MONASTERIO = 8
PONTOS_MONASTERIO_COMPLETO = 9


class Territorio(ABC):
    def __init__(self):
        self.segmentos = []
        self.bordasAbertas = 0

    @property
    def qtdPecas(self):
        return len({id(segmento.peca) for segmento in self.segmentos})

    def adicionar(self, segmento):
        self.segmentos.append(segmento)
        self.bordasAbertas += len(segmento.posicoes)

    def aceitaMeeple(self):
        return True

    def meeples(self):
        return [segmento.meeple for segmento in self.segmentos if segmento.meeple is not None]

    def vencedores(self):
        meeplesPorDono = Counter(meeple.dono for meeple in self.meeples())
        if not meeplesPorDono:
            return []
        maioria = max(meeplesPorDono.values())
        return [dono for dono, quantidade in meeplesPorDono.items() if quantidade == maioria]

    def calcularPontuacao(self):
        self._distribuirPontos(self.pontosPorPeca())
        for meeple in self.meeples():
            meeple.segmento = None

    def calcularPontuacaoFinal(self):
        self._distribuirPontos(self.pontosPorPecaFinal())

    def _distribuirPontos(self, pontos):
        for jogador in self.vencedores():
            jogador.addPontos(pontos)

    def unir(self, outro):
        self.bordasAbertas -= BORDAS_FECHADAS_POR_LADO
        if outro is self:
            return
        for segmento in outro.segmentos:
            segmento.territorio = self
        self.segmentos.extend(outro.segmentos)
        self.bordasAbertas += outro.bordasAbertas
        outro.segmentos = []
        outro.bordasAbertas = 0

    @abstractmethod
    def estaCompleta(self):
        pass

    @abstractmethod
    def pontosPorPeca(self):
        pass

    @abstractmethod
    def pontosPorPecaFinal(self):
        pass


class Cidade(Territorio):
    def __init__(self, escudos=0):
        super().__init__()
        self.escudos = escudos

    def unir(self, outro):
        if outro is not self:
            self.escudos += outro.escudos
            outro.escudos = 0
        super().unir(outro)

    def estaCompleta(self):
        return self.bordasAbertas == 0

    def pontosPorPeca(self):
        return 2 * self.qtdPecas + 2 * self.escudos

    def pontosPorPecaFinal(self):
        return self.qtdPecas + self.escudos


class Estrada(Territorio):
    def estaCompleta(self):
        return self.bordasAbertas == 0

    def pontosPorPeca(self):
        return self.qtdPecas

    def pontosPorPecaFinal(self):
        return self.qtdPecas


class Monasterio(Territorio):
    def __init__(self):
        super().__init__()
        self.vizinhosPresentes = 0

    def registrarVizinho(self):
        self.vizinhosPresentes += 1

    def estaCompleta(self):
        return self.vizinhosPresentes == VIZINHOS_DO_MONASTERIO

    def pontosPorPeca(self):
        return PONTOS_MONASTERIO_COMPLETO

    def pontosPorPecaFinal(self):
        return 1 + self.vizinhosPresentes


class Campo(Territorio):
    def aceitaMeeple(self):
        return False

    def estaCompleta(self):
        return False

    def pontosPorPeca(self):
        return 0

    def pontosPorPecaFinal(self):
        return 0
