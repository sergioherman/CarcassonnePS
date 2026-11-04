VOLTA_COMPLETA = 360
GRAUS_POR_ROTACAO = 90


class Peça:
    def __init__(self, segmentos, tipo=None):
        self.tipo = tipo
        self.rotacao = 0
        self.segmentos = list(segmentos)
        for segmento in self.segmentos:
            segmento.peca = self

    def rotacionar(self):
        self.rotacao = (self.rotacao + GRAUS_POR_ROTACAO) % VOLTA_COMPLETA

    def segmentosLivres(self):
        return [
            segmento
            for segmento in self.segmentos
            if segmento.territorio.aceitaMeeple() and not segmento.territorio.meeples()
        ]

    def segmentoNoLado(self, lado):
        return next((segmento for segmento in self.segmentos if segmento.ocupaLado(lado)), None)
