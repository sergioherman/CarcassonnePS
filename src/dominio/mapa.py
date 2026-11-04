from dominio.jogada import Jogada
from dominio.posicao import Posicao
from dominio.territorio import Monasterio

ROTACOES = (0, 90, 180, 270)
CASAS_AO_REDOR = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]


class Mapa:
    def __init__(self, pecaInicial):
        self.matriz = {(0, 0): pecaInicial}

    def jogadasLegais(self, peca):
        rotacaoOriginal = peca.rotacao
        legais = []
        for x, y in self._casasCandidatas():
            for rotacao in ROTACOES:
                self._girarAte(peca, rotacao)
                if self._encaixa(peca, x, y):
                    legais.append(Jogada(x, y, rotacao))
        self._girarAte(peca, rotacaoOriginal)
        return legais

    def colocarPeca(self, peca, jogada):
        self._girarAte(peca, jogada.rotacao)
        x, y = jogada.posicaoX, jogada.posicaoY
        self.matriz[(x, y)] = peca
        for lado in Posicao:
            vizinha = self.matriz.get(self._casaAdjacente(x, y, lado))
            if vizinha is None:
                continue
            territorioNovo = peca.segmentoNoLado(lado).territorio
            territorioNovo.unir(vizinha.segmentoNoLado(lado.oposta()).territorio)
        self._registrarVizinhosDeMonasterios(peca, x, y)

    def vizinhos(self, x, y):
        casas = [self._casaAdjacente(x, y, lado) for lado in Posicao]
        return [self.matriz[casa] for casa in casas if casa in self.matriz]

    def territoriosAfetados(self, peca):
        x, y = self.posicaoDe(peca)
        territorios = [segmento.territorio for segmento in peca.segmentos]
        for vizinha in self._pecasAoRedor(x, y):
            territorios.extend(self._monasterios(vizinha))
        return _semRepeticao(territorios)

    def territorios(self):
        return _semRepeticao(
            segmento.territorio for peca in self.matriz.values() for segmento in peca.segmentos
        )

    def posicaoDe(self, peca):
        return next(casa for casa, colocada in self.matriz.items() if colocada is peca)

    def _encaixa(self, peca, x, y):
        for lado in Posicao:
            vizinha = self.matriz.get(self._casaAdjacente(x, y, lado))
            if vizinha is None:
                continue
            if not peca.segmentoNoLado(lado).compativel(vizinha.segmentoNoLado(lado.oposta())):
                return False
        return True

    def _casasCandidatas(self):
        candidatas = {
            self._casaAdjacente(x, y, lado)
            for x, y in self.matriz
            for lado in Posicao
        }
        return sorted(candidatas - self.matriz.keys())

    def _registrarVizinhosDeMonasterios(self, peca, x, y):
        for vizinha in self._pecasAoRedor(x, y):
            for monasterio in self._monasterios(peca) + self._monasterios(vizinha):
                monasterio.registrarVizinho()

    def _pecasAoRedor(self, x, y):
        casas = [(x + dx, y + dy) for dx, dy in CASAS_AO_REDOR]
        return [self.matriz[casa] for casa in casas if casa in self.matriz]

    @staticmethod
    def _monasterios(peca):
        return [s.territorio for s in peca.segmentos if isinstance(s.territorio, Monasterio)]

    @staticmethod
    def _casaAdjacente(x, y, lado):
        dx, dy = lado.deslocamento()
        return x + dx, y + dy

    @staticmethod
    def _girarAte(peca, rotacao):
        while peca.rotacao != rotacao:
            peca.rotacionar()


def _semRepeticao(territorios):
    vistos = {}
    for territorio in territorios:
        vistos.setdefault(id(territorio), territorio)
    return list(vistos.values())
