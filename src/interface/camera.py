import math

TAMANHOS = (64, 80, 96, 112, 128, 144, 160, 192, 224)
TAMANHO_INICIAL = 6


class Camera:
    def __init__(self, centro):
        self._indice = TAMANHO_INICIAL
        self.origem = (centro[0] - self.tamanho / 2, centro[1] - self.tamanho / 2)

    @property
    def tamanho(self):
        return TAMANHOS[self._indice]

    def paraTela(self, x, y):
        return int(self.origem[0] + x * self.tamanho), int(self.origem[1] + y * self.tamanho)

    def casaEm(self, ponto):
        return (
            math.floor((ponto[0] - self.origem[0]) / self.tamanho),
            math.floor((ponto[1] - self.origem[1]) / self.tamanho),
        )

    def deslocar(self, dx, dy):
        self.origem = (self.origem[0] + dx, self.origem[1] + dy)

    def ampliar(self, passos, ponto):
        novoIndice = max(0, min(len(TAMANHOS) - 1, self._indice + passos))
        if novoIndice == self._indice:
            return
        mundoX = (ponto[0] - self.origem[0]) / self.tamanho
        mundoY = (ponto[1] - self.origem[1]) / self.tamanho
        self._indice = novoIndice
        self.origem = (ponto[0] - mundoX * self.tamanho, ponto[1] - mundoY * self.tamanho)
